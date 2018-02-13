from fabric.api import sudo, cd, run
from fabric.contrib.files import append as fabappend, comment
from fabric.context_managers import env
import re
import ipaddress
from DnsCryptPiHoleSetup.FabricService.StringContainer import DnsCryptService, DnsCryptSocket,\
    DnsCryptConf, DnsCryptSudoer



class FabricCommandClass(object):



    def CommandSystemPackages(self):
        """
        Installs required ssh packages
        :return:
        """
        requiredPackages = "build-essential  " \
                           "bash-completion libsystemd-dev pkg-config python3-dev  jq"
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
                run('wget ' + dnscryptdownloadlink)
                run("mkdir -p " + dnscryptexractdir + "/dnscryptBuild/")
                run('tar -xf dnscrypt*.tar.gz -C dnscryptBuild --strip-components=1')
        else:
            raise ValueError("Dns Crypt is already installed at " + str(returnCode.stdout))



    def CommandCreateDNSCryptProxies(self) -> str:
        """
        Creates Dns Crypt Proxies
        :return: ListenAddress
        """



        loopbackstartaddress  = FabricCommandClass.CommandCreateDNSCryptProxies.loopbackstartaddress
        dnscryptexractdir = FabricCommandClass.CommandCreateDNSCryptProxies.dnscryptexractdir



        # Find a Available Socket LoopBack Address and Create Socket Files


        runningSockets = sudo("ss -nlut | awk 'NR>1 {print  $5}'")
        runningSockets = re.sub(r".*[a-zA-Z]+\S","",runningSockets).split()








        with cd(dnscryptexractdir + "/dnscryptBuild/"):
            # Clear Old Socket and Service Files
            run("rm dnscrypt-proxy.s*")

            # Find a available loopback address
            while True:
                if loopbackstartaddress + ":41" not in runningSockets:
                    fabappend("dnscrypt-proxy.socket", DnsCryptSocket.format(loopbackstartaddress))
                    runningSockets.append(loopbackstartaddress + ":41")
                    ListenAddress = loopbackstartaddress
                    break
                loopbackstartaddress = str(ipaddress.ip_address(loopbackstartaddress) + 1)
                if loopbackstartaddress == '127.255.255.254':
                    raise ValueError("No Ip address available in the 127.0.0.0/8 IPV4 Range")




            #Edit Toml file

            run(r"sed -i 's|\['\''127\.0\.0\.1:53'\'', '\''\[::1\]:53'\''\]|\[\]|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''dnscrypt-proxy\.log'\''|'\''/var/log/dnscrypt-proxy/dnscrypt-proxy\.log'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''forwarding-rules\.txt'\''|'\''/etc/dnscrypt-proxy/forwarding-rules\.txt'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''cloaking-rules\.txt'\''|'\''/etc/dnscrypt-proxy/cloaking-rules\.txt'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''query\.log'\''|'\''/var/log/dnscrypt-proxy/query\.log'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''nx\.log'\''|'\''/var/log/dnscrypt-proxy/nx\.log'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''blacklist\.txt'\''|'\''/etc/dnscrypt-proxy/blacklist\.txt'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''blocked\.log'\''|'\''/var/log/dnscrypt-proxy/blocked\.log'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''ip-blacklist\.txt'\''|'\''/etc/dnscrypt-proxy/ip-blacklist\.txt'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''ip-blocked\.log'\''|'\''/var/log/dnscrypt-proxy/ip-blocked\.log'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''public-resolvers\.md'\''|'\''/var/cache/dnscrypt-proxy/public-resolvers\.md'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''parental-control\.md'\''|'\''/var/cache/dnscrypt-proxy/parental-control\.md'\''|g' example-dnscrypt-proxy.toml")



            # Create Service Unit and Install Files
            fabappend('dnscrypt-proxy.service', DnsCryptService)
            sudo('install -Dm755 "dnscrypt-proxy" "/usr/bin/dnscrypt-proxy"')
            sudo('install -Dm644 "example-dnscrypt-proxy.toml" "/etc/dnscrypt-proxy/dnscrypt-proxy.toml"')
            sudo('install -Dm644 "example-forwarding-rules.txt" "/usr/share/doc/dnscrypt-proxy/example-forwarding-rules.txt"')
            sudo('install -Dm644 "example-blacklist.txt" "/usr/share/doc/dnscrypt-proxy/example-blacklist.txt"')
            sudo('install -Dm644 "example-cloaking-rules.txt" "/usr/share/doc/dnscrypt-proxy/example-cloaking-rules.txt"')
            sudo('install -Dm644 "dnscrypt-proxy.service" "/etc/systemd/system/dnscrypt-proxy.service"')
            sudo('install -Dm644 "dnscrypt-proxy.socket" "/etc/systemd/system/dnscrypt-proxy.socket"')
            sudo('install -Dm644 "LICENSE" "/usr/share/licenses/dnscrypt-proxy/LICENSE"')





            # Enable and Start the DNS Proxy
            sudo("systemctl enable dnscrypt-proxy.socket")
            sudo("systemctl enable dnscrypt-proxy.service")
            sudo("systemctl start dnscrypt-proxy.socket")
            sudo("systemctl start dnscrypt-proxy.service")


        return ListenAddress




    def CommandChangeDnsMasq(self):
        """
        Updates the DnsMasq Configs with the New Proxies and Restarts it

        :return: None
        """


        ListenAddress = FabricCommandClass.CommandChangeDnsMasq.ListenAddress
        host = FabricCommandClass.CommandChangeDnsMasq.host

        #Extract Loopback Address
        ListenAddress = ListenAddress[host]



        with cd("/etc/dnsmasq.d"):
            sudo("rm -f 02-dnscrypt.conf")
            fabappend('02-dnscrypt.conf', DnsCryptConf.format("server=" + ListenAddress + "#41"),use_sudo=True)


        comment('/etc/dnsmasq.d/01-pihole.conf', r'server=.*', use_sudo=True, backup='.old')
        comment('/etc/pihole/setupVars.conf', r'PIHOLE_DNS.*',use_sudo=True,backup='.old')

        # Moving Restore files due to conflict with dnsmasq service
        run("mkdir -p /home/{0}/.piHoleRestore".format(env.user))
        sudo("mv /etc/pihole/setupVars.conf.old /home/{0}/.piHoleRestore/.".format(env.user))
        sudo("mv /etc/dnsmasq.d/01-pihole.conf.old /home/{0}/.piHoleRestore/.".format(env.user))

        sudo("sed -i 's/.*dnscrypt.*//g' /etc/hosts")
        #for name,address in zip(dnscryptresolvernames,ListenAddress):
        #    sudo("sh -c 'echo \"{0}\t{1} \" >> /etc/hosts'".format(address,name + "-dnscrypt"))




        sudo("service dnsmasq restart")
        print(" DNS crypt Setup has Ran Successfully")



    def CommandCreateCronJob(self):
        """
        Create Cron Job that Restart a Proxy server when it see a message from the
        Dns Crypt Service

        Defaults are every 10 minutes and Look for Message that Contain Error

        :return: None
        """
        cronjobminutes = FabricCommandClass.CommandCreateCronJob.cronjobminutes
        cronjobmessage = FabricCommandClass.CommandCreateCronJob.cronjobmessage


        with cd("/etc/sudoers.d"):
            sudo("rm -f DnsCryptSudoer")
            fabappend('DnsCryptSudoer', DnsCryptSudoer,use_sudo=True)

        with cd("/etc/cron.d"):
            sudo("rm -f dnscryptCron")

        sudo(r"""
        sudo echo "*/{0} * * * * dnscrypt sudo journalctl --since \\"{0} minutes ago\\" -u  dnscrypt-proxy* -o json | \
        jq  '. | select(.MESSAGE | tostring |contains(\\"{1}\\")) | \
        ._SYSTEMD_UNIT' | sort | uniq | grep -Pho '(?<=\\").*(?=\.service)' | \
        xargs -I \% bash -c 'sudo systemctl stop \%.socket;sudo systemctl stop \%.service;sudo systemctl start \%.socket;sudo systemctl start \%.service'" | \
        sudo tee -a /etc/cron.d/dnscryptCron > /dev/null 2>&1
        """.format(cronjobminutes,cronjobmessage))

        print(" DNS crypt Setup Cron Watch Dog has Ran Successfully")











