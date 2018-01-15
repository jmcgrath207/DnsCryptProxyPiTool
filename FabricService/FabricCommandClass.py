from fabric.api import sudo, cd, run
from CsvService.CsvClass import CsvClass



class FabricCommandClass(CsvClass):


    def __init__(self, DnsCryptDownloadLink: str, DnsCryptExractDir: str,
                 DnsCryptResolverCsvLink: str, DnsCryptResolverDir: str):
        self.DnsCryptDownloadLink = DnsCryptDownloadLink
        self.DnsCryptExractDir = DnsCryptExractDir
        self.DnsCryptResolverCsvLink = DnsCryptResolverCsvLink
        self.DnsCryptResolverDir = DnsCryptResolverDir
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


    def CommandCreateDNSCryptProxy(self):
        AvaibleProxies = self.GetDnsCryptProxyNames()
        print("hello")

