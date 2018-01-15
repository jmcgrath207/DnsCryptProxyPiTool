from fabric.api import sudo, cd, run




class FabricCommandClass(object):




    def CommandSystemPackages(self):
        sudo('sudo apt-get update')
        sudo('apt-get -y install build-essential tcpdump dnsutils libsodium-dev \
             locate bash-completion libsystemd-dev pkg-config')



    def CommandBuildDNSCrypt(self):
        with cd("/tmp"):
            run('wget https://launchpad.net/ubuntu/+archive/primary/+files/dnscrypt-proxy_1.9.5.orig.tar.gz')
            run('tar -xf dnscrypt*.tar.gz')