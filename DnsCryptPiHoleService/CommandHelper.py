
from DnsCryptPiHoleService.DefaultConfig import host,  password, user,dnscryptdownloadlink,\
dnscryptexractdir,loopbackstartaddress, cronjobmessage, cronjobminutes

from DnsCryptPiHoleService.ClickHelperClasses import ShowDefaultSingleQuote

import click

from DnsCryptPiHoleService.FabricService.FabricExecute import FabricExecuteClass





@click.command()
@click.option('--dnscryptexractdir', '-e', default=dnscryptexractdir,
              help='Directory for where the DnsCrypt Proxy is going to be downloaded and extracted at during Install',
              show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--dnscryptdownloadlink', '-d', default=dnscryptdownloadlink,
              help='HTTP address of DNScrypt.tar.gz',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--loopbackstartaddress', '-l', default=loopbackstartaddress,
              help='IPV4 Loopback Address you want to use for the socket unit file. The address will increment by the last octet when multiple proxies are installed',
              show_default=True,cls=ShowDefaultSingleQuote)
def install():
    Fec = FabricExecuteClass(user, password, host)
    Fec.ExecuteSystemPackages()
    Fec.ExecuteBuildDNSCrypt(dnscryptexractdir,dnscryptdownloadlink)
    Fec.ExecuteCreateDNSCryptProxies(loopbackstartaddress, dnscryptexractdir)
    Fec.ExecuteChangeDnsMasq()



@click.command()
@click.option('--cronjobminutes','-t', default=cronjobminutes,
              help=' How often in minutes do you want the Cron Job use for check if there is errors and restarting the individual dnscrypt proxy ex. 10 = */10 * * * *',
              show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--cronjobmessage','-m', default=cronjobmessage,
              help='The Message you want to match on the DnsCrypt Proxy System Log to Trigger a Restart Event',
              show_default=True,cls=ShowDefaultSingleQuote)
def watchdog():
    Fec = FabricExecuteClass(user, password, host)
    Fec.ExecuteCreateCronJob(cronjobminutes, cronjobmessage)





