from fabric.api import sudo, cd, run
from fabric.contrib.files import append as fabappend, comment
import re
import ipaddress
from CsvService.CsvClass import CsvClass
from FabricService.StringContainer import DnsCryptService, DnsCryptSocket,\
    DnsCryptConf, DnsCryptSudoer



class FabricCommandClass(CsvClass):



    def CommandSystemPackages(self):
        requiredPackages = "build-essential tcpdump dnsutils libsodium-dev locate " \
                           "bash-completion libsystemd-dev pkg-config python3-dev rng-tools jq"
        returnCode = run("dpkg -l " + requiredPackages)
        if(returnCode.failed):
            sudo('sudo apt-get update')
            sudo('apt-get -y install ' + requiredPackages)



    def CommandBuildDNSCrypt(self):
        """
        Install DnsCrypt Proxy if not present

        :return:
        """



        dnscryptexractdir = FabricCommandClass.CommandBuildDNSCrypt.dnscryptexractdir
        dnscryptdownloadlink = FabricCommandClass.CommandBuildDNSCrypt.dnscryptdownloadlink
        returnCode = run("which dnscrypt-proxy")
        if(returnCode.failed):
            with cd(dnscryptexractdir):
                run('wget' + dnscryptdownloadlink)
                run('tar -xf dnscrypt*.tar.gz -C dnscryptBuild --strip-components=1')
            with cd(dnscryptexractdir + "/dnscryptBuild/"):
                sudo("ldconfig")
                run("./configure --with-systemd")
                run("make")
                sudo("make install")
        else:
            run("mkdir -p " + dnscryptexractdir + "/dnscryptBuild/")

    def CommandAddDnsCryptUser(self):
        """
        Creates  DNS crypt User

        :return:
        """
        returnCode = run("id -u dnscrypt")
        if(returnCode.failed):
            sudo("useradd -r -m -s /usr/sbin/nologin -G systemd-journal dnscrypt")


    def CommandDownloadDnsCryptResolvers(self):
        dnscryptresolvercsvlink = FabricCommandClass.CommandDownloadDnsCryptResolvers.dnscryptresolvercsvlink
        dnscryptresolverdir = FabricCommandClass.CommandDownloadDnsCryptResolvers.dnscryptresolverdir
        with cd(dnscryptresolverdir):
            sudo("wget -N " + dnscryptresolvercsvlink)


    def CommandCreateDNSCryptProxies(self) -> list:

        dnscryptresolverdir =  FabricCommandClass.CommandCreateDNSCryptProxies.dnscryptresolverdir
        dnscryptresolvernames = FabricCommandClass.CommandCreateDNSCryptProxies.dnscryptresolvernames
        dnscryptresolvercsvlink = FabricCommandClass.CommandCreateDNSCryptProxies.dnscryptresolvercsvlink
        loopbackstartaddress  = FabricCommandClass.CommandCreateDNSCryptProxies.loopbackstartaddress
        dnscryptexractdir = FabricCommandClass.CommandCreateDNSCryptProxies.dnscryptexractdir

        AvailableResolvers = self.GetDnsCryptProxyNames(dnscryptresolverdir)



        # Check if Resolver Name is Correct
        #TODO: Check To see if command if look at file correctly.
        for name in dnscryptresolvernames:
            if name not in AvailableResolvers:
                raise ValueError(name + ' Is not a Vaild Resolver Name. Please Check ' + dnscryptresolvercsvlink + ' to ensure the name is correct')

        # Clear Old Files

        with cd(dnscryptexractdir + "/dnscryptBuild/"):
            run("rm dnscrypt-proxy@*")

        # Find a Available Socket LoopBack Address and Create Socket Files

        ListenAddresses = []
        runningSockets = sudo("ss -nlut | awk 'NR>1 {print  $5}'")
        runningSockets = re.sub(r".*[a-zA-Z]+\S","",runningSockets).split()
        for name in dnscryptresolvernames:
            with cd(dnscryptexractdir + "/dnscryptBuild/"):
                while True:
                    if loopbackstartaddress + ":41" not in runningSockets:
                        fabappend("dnscrypt-proxy@" + name + ".socket", DnsCryptSocket.format(loopbackstartaddress))
                        runningSockets.append(loopbackstartaddress + ":41")
                        ListenAddresses.append(loopbackstartaddress)
                        break
                    loopbackstartaddress = str(ipaddress.ip_address(loopbackstartaddress) + 1)
                    if loopbackstartaddress == '127.255.255.254':
                        raise ValueError("No Ip address available in the 127.0.0.0/8 IPV4 Range")


        ### Stop and Remove Old Dns Proxy Services
        sudo("systemctl stop dnscrypt-proxy@\*")
        sudo("systemctl disable dnscrypt-proxy@\*")
        sudo("rm /etc/systemd/system/multi-user.target.wants/dnscrypt-proxy*")
        sudo("rm /etc/systemd/system/sockets.target.wants/dnscrypt-proxy*")
        sudo("rm /etc/systemd/system/dnscrypt-proxy*")
        sudo("systemctl daemon-reload")
        sudo("systemctl reset-failed")



        # Create Service then start and enable them
        with cd(dnscryptexractdir + "/dnscryptBuild/"):
            fabappend('dnscrypt-proxy@.service',DnsCryptService)
            sudo("cp ./dnscrypt-proxy@* /etc/systemd/system/.")
        sudo("systemctl daemon-reload")
        for name in dnscryptresolvernames:
            sudo("systemctl enable dnscrypt-proxy@" + name + ".socket")
            sudo("systemctl enable dnscrypt-proxy@" + name + ".service")
            sudo("systemctl start dnscrypt-proxy@" + name + ".socket")
            sudo("systemctl start dnscrypt-proxy@" + name + ".service")

        return ListenAddresses




    def CommandChangeDnsMasq(self):
        """
        Updates the DnsMasq Configs with the New Proxies and Restarts it

        :return: None
        """

        dnscryptresolvernames = FabricCommandClass.CommandChangeDnsMasq.dnscryptresolvernames
        ListenAddresses = FabricCommandClass.CommandChangeDnsMasq.ListenAddresses
        host = FabricCommandClass.CommandChangeDnsMasq.host

        ListenAddresses = ListenAddresses[host]
        with cd("/etc/dnsmasq.d"):
            sudo("rm -f 02-dnscrypt.conf")
            ConfListenAddresses = ["server=" + ListenAddress + "#41" for ListenAddress in ListenAddresses]
            ConfListenAddresses = '\n'.join(ConfListenAddresses)
            fabappend('02-dnscrypt.conf', DnsCryptConf.format(ConfListenAddresses),use_sudo=True)

        comment('/etc/dnsmasq.d/01-pihole.conf', r'server=.*', use_sudo=True, backup='')
        comment('/etc/pihole/setupVars.conf', r'PIHOLE_DNS.*',use_sudo=True,backup='')
        sudo("sed -i 's/.*dnscrypt.*//g' /etc/hosts")
        ## TODO: need to change Foward Detination Logs in Pihole
        for name,address in zip(dnscryptresolvernames,ListenAddresses):
            sudo("sh -c 'echo \"{0}\t{1} \" >> /etc/hosts'".format(address,name + "-dnscrypt"))




        sudo("service dnsmasq restart")



    def CommandCreateCronJob(self):
        """
        Create Cron Job that Restart a Proxy server when it see a message from the
        Dns Crypt Service

        Defaults are every 5 mines and Look for Message that Contain Error

        :return: None
        """
        cronjobtime = FabricCommandClass.CommandCreateCronJob.cronjobtime
        cronjobmessage = FabricCommandClass.CommandCreateCronJob.cronjobmessage


        with cd("/etc/sudoers.d"):
            sudo("rm -f DnsCryptSudoer")
            fabappend('DnsCryptSudoer', DnsCryptSudoer,use_sudo=True)

        with cd("/etc/cron.d"):
            sudo("rm -f dnscryptCron")

        sudo(r"""
        sudo echo "{0} dnscrypt sudo journalctl -u  dnscrypt-proxy@\* -o json | \
        jq  '. | select(.MESSAGE | tostring |contains(\\"{1}\\")) | \
        ._SYSTEMD_UNIT' | sort | uniq | grep -Pho '(?<=\\").*(?=\.service)' | \
        xargs -I \% bash -c 'sudo systemctl stop \%.socket;sudo systemctl stop \%.service;sudo systemctl start \%.socket;sudo systemctl start \%.service'" | \
        sudo tee -a /etc/cron.d/dnscryptCron > /dev/null 2>&1
        """.format(cronjobtime,cronjobmessage))











