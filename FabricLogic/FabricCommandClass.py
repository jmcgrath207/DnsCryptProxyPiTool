from fabric.api import sudo, cd, run




class FabricCommandClass(object):




    def CommandSystemPackages(self):
        sudo('sudo apt-get update')
        sudo('apt-get -y install build-essential tcpdump dnsutils libsodium-dev \
             locate bash-completion libsystemd-dev pkg-config')



    def CommandBuildDNSCrypt(self):

        returnCode = run("which dnscrypt-proxy")
        if(returnCode.failed):
            with cd("/tmp"):
                run('wget https://launchpad.net/ubuntu/+archive/primary/+files/dnscrypt-proxy_1.9.5.orig.tar.gz')
                run('tar -xf dnscrypt*.tar.gz')
            with cd("/tmp/dnscrypt*/"):
                sudo("ldconfig")
                run("./configure --with-systemd")
                run("make")
                sudo("make install")

    def CommandAddDnsCryptUser(self):

        returnCode = run("id -u dnscrypt")
        if(returnCode.failed):
            sudo("useradd -r -d /var/dnscrypt -m -s /usr/sbin/nologin dnscrypt")