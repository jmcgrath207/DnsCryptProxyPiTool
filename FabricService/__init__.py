

#Default Values
user = 'pi'
password = 'raspberry'
host = '127.0.0.1'
DnsCryptExractDir = "/tmp"
DnsCryptDownloadLink = "https://launchpad.net/ubuntu/+archive/primary/+files/dnscrypt-proxy_1.9.5.orig.tar.gz"
DnsCryptResolverCsvLink = "https://raw.githubusercontent.com/dyne/dnscrypt-proxy/master/dnscrypt-resolvers.csv"
DnsCryptResolverDir = "/usr/local/share/dnscrypt-proxy"
DnsCryptResolverNames =['d0wn-random-ns1','d0wn-random-ns2']
LoopBackStartAddress = "127.10.10.1"
# https://crontab.guru/every-5-minutes
CronJobTime ="*/1 * * * *"
CronJobMessage = "ERROR"