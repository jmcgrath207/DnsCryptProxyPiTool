from fabric.api import sudo, cd, run




class FabricCommandClass(object):


    def __init__(self, DnsCryptDownloadLink: str, DnsCryptExractDir: str):
        self.DnsCryptDownloadLink = DnsCryptDownloadLink
        self.DnsCryptExractDir = DnsCryptExractDir




    def CommandSystemPackages(self):
        requiredPackages = "build-essential tcpdump dnsutils libsodium-dev locate " \
                           "bash-completion libsystemd-dev pkg-config"
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