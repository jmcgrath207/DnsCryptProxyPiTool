from fabric.api import sudo, cd, run, show, hide
import re
import ipaddress
from CsvService.CsvClass import CsvClass



class FabricCommandClass(CsvClass):


    def __init__(self, DnsCryptDownloadLink: str, DnsCryptExractDir: str,
                 DnsCryptResolverCsvLink: str, DnsCryptResolverDir: str,
                 DnsCryptResolverNames: list, LoopBackStartAddress: str):
        self.DnsCryptDownloadLink = DnsCryptDownloadLink
        self.DnsCryptExractDir = DnsCryptExractDir
        self.DnsCryptResolverCsvLink = DnsCryptResolverCsvLink
        self.DnsCryptResolverDir = DnsCryptResolverDir
        self.DnsCryptResolverNames = DnsCryptResolverNames
        self.LoopBackStartAddress = LoopBackStartAddress
        super().__init__(DnsCryptResolverDir=DnsCryptResolverDir)




    def CommandSystemPackages(self):
        requiredPackages = "build-essential tcpdump dnsutils libsodium-dev locate " \
                           "bash-completion libsystemd-dev pkg-config python3-dev"
        returnCode = run("dpkg -l " + requiredPackages)
        if(returnCode.failed):
            sudo('sudo apt-get update')
            sudo('apt-get -y install ' + requiredPackages)



    def CommandBuildDNSCrypt(self):

        returnCode = run("which dnscrypt-proxy")
        if(returnCode.failed):
            with cd(self.DnsCryptExractDir):
                run('wget' + self.DnsCryptDownloadLink)
                run('tar -xf dnscrypt*.tar.gz')
            with cd(self.DnsCryptExractDir + "/dnscrypt*/"):
                sudo("ldconfig")
                run("./configure --with-systemd")
                run("make")
                sudo("make install")

    def CommandAddDnsCryptUser(self):

        returnCode = run("id -u dnscrypt")
        if(returnCode.failed):
            sudo("useradd -r -d /var/dnscrypt -m -s /usr/sbin/nologin dnscrypt")


    def CommandUpdateDnsCryptResolvers(self):
        with cd(self.DnsCryptResolverDir):
            sudo("wget -N " + self.DnsCryptResolverCsvLink)


    def CommandCreateDNSCryptProxies(self):
        AvailableResolvers = self.GetDnsCryptProxyNames()
        for name in self.DnsCryptResolverNames:
            if name not in AvailableResolvers:
                raise ValueError(name + ' Is not a Vaild Resolver Name. Please Check ' + self.DnsCryptResolverCsvLink + ' to ensure the name is correct')

        runningSockets = sudo("ss -nlut | awk 'NR>1 {print  $5}'")
        runningSockets = re.sub(r".*[a-zA-Z]+\S","",runningSockets).split()
        for name in self.DnsCryptResolverNames:
            with cd(self.DnsCryptExractDir + "/dnscrypt*/"):
                run("cp dnscrypt-proxy.socket dnscrypt-proxy@" + name + ".socket")
                while True:
                    if self.LoopBackStartAddress + ":41" not in runningSockets:
                        run("sed -i 's/127.0.0.1:53/" + self.LoopBackStartAddress + ":41/g' dnscrypt-proxy@"+ name + ".socket")
                        runningSockets.append(self.LoopBackStartAddress + ":41")
                        break
                    self.LoopBackStartAddress = str(ipaddress.ip_address(self.LoopBackStartAddress) + 1)
                    if self.LoopBackStartAddress == '127.255.255.254':
                        raise ValueError(" No Ip address available in the 127.0.0.0/8 IPV4 Range")








