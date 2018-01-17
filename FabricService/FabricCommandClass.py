from fabric.api import sudo, cd, run
from fabric.contrib.files import append as fabappend, exists
import re
import ipaddress
from CsvService.CsvClass import CsvClass
from FabricService.StringContainer import DnsCryptService, DnsCryptSocket



class FabricCommandClass(CsvClass):



    def CommandSystemPackages(self):
        requiredPackages = "build-essential tcpdump dnsutils libsodium-dev locate " \
                           "bash-completion libsystemd-dev pkg-config python3-dev rng-tools"
        returnCode = run("dpkg -l " + requiredPackages)
        if(returnCode.failed):
            sudo('sudo apt-get update')
            sudo('apt-get -y install ' + requiredPackages)



    def CommandBuildDNSCrypt(self):
        DnsCryptExractDir = FabricCommandClass.CommandBuildDNSCrypt.DnsCryptExractDir
        DnsCryptDownloadLink = FabricCommandClass.CommandBuildDNSCrypt.DnsCryptDownloadLink
        returnCode = run("which dnscrypt-proxy")
        if(returnCode.failed):
            with cd(DnsCryptExractDir):
                run('wget' + DnsCryptDownloadLink)
                run('tar -xf dnscrypt*.tar.gz -C dnscryptBuild --strip-components=1')
            with cd(DnsCryptExractDir + "/dnscryptBuild/"):
                sudo("ldconfig")
                run("./configure --with-systemd")
                run("make")
                sudo("make install")
        else:
            run("mkdir -p " + DnsCryptExractDir + "/dnscryptBuild/")

    def CommandAddDnsCryptUser(self):
        returnCode = run("id -u dnscrypt")
        if(returnCode.failed):
            sudo("useradd -r -d /var/dnscrypt -m -s /usr/sbin/nologin dnscrypt")


    def CommandUpdateDnsCryptResolvers(self):
        DnsCryptResolverCsvLink = FabricCommandClass.CommandUpdateDnsCryptResolvers.DnsCryptResolverCsvLink
        DnsCryptResolverDir = FabricCommandClass.CommandUpdateDnsCryptResolvers.DnsCryptResolverDir
        with cd(DnsCryptResolverDir):
            sudo("wget -N " + DnsCryptResolverCsvLink)


    def CommandCreateDNSCryptProxies(self):

        DnsCryptResolverDir =  FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptResolverDir
        DnsCryptResolverNames = FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptResolverNames
        DnsCryptResolverCsvLink = FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptResolverCsvLink
        LoopBackStartAddress  = FabricCommandClass.CommandCreateDNSCryptProxies.LoopBackStartAddress
        DnsCryptExractDir = FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptExractDir

        AvailableResolvers = self.GetDnsCryptProxyNames(DnsCryptResolverDir)

        for name in DnsCryptResolverNames:
            if name not in AvailableResolvers:
                raise ValueError(name + ' Is not a Vaild Resolver Name. Please Check ' + DnsCryptResolverCsvLink + ' to ensure the name is correct')


        runningSockets = sudo("ss -nlut | awk 'NR>1 {print  $5}'")
        runningSockets = re.sub(r".*[a-zA-Z]+\S","",runningSockets).split()
        for name in DnsCryptResolverNames:
            with cd(DnsCryptExractDir + "/dnscryptBuild/"):
                run("rm dnscrypt@*")
                while True:
                    if LoopBackStartAddress + ":41" not in runningSockets:
                        fabappend("dnscrypt-proxy@" + name + ".socket", DnsCryptSocket.format(LoopBackStartAddress))
                        runningSockets.append(LoopBackStartAddress + ":41")
                        break
                    LoopBackStartAddress = str(ipaddress.ip_address(LoopBackStartAddress) + 1)
                    if LoopBackStartAddress == '127.255.255.254':
                        raise ValueError("No Ip address available in the 127.0.0.0/8 IPV4 Range")

        with cd(DnsCryptExractDir + "/dnscryptBuild/"):
            fabappend('dnscrypt-proxy@.service',DnsCryptService)
            sudo("cp ./dnscrypt-proxy@* /etc/systemd/system/.")
        sudo("systemctl daemon-reload")
        for name in DnsCryptResolverNames:
            sudo("")









