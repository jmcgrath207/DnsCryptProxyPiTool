
from DnsCryptPiHoleSetup.DefaultConfig import host,  password, user,dnscryptdownloadlink,\
dnscryptexractdir,loopbackstartaddress, cronjobmessage, cronjobminutes

from DnsCryptPiHoleSetup.ClickHelperClasses import ShowDefaultSingleQuote

import click

from DnsCryptPiHoleSetup.FabricService.FabricExecute import FabricExecuteClass



@click.group()
def install():
    pass

@install.command()
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














@click.group()
def setDefaultConfig():
    pass

@setDefaultConfig.command()
def cmd1():
    """Command on cli1"""

@click.group()
def setWatcher():
    pass




@setWatcher.command()
@click.option('--cronjobminutes','-t', default=cronjobminutes,
              help=' How often in minutes do you want the Cron Job use for check if there is errors and restarting the individual dnscrypt proxy ex. 10 = */10 * * * *',
              show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--cronjobmessage','-m', default=cronjobmessage,
              help='The Message you want to match on the DnsCrypt Proxy System Log to Trigger a Restart Event',
              show_default=True,cls=ShowDefaultSingleQuote)
def cmd1():
    Fec = FabricExecuteClass(user, password, host)
    Fec.ExecuteCreateCronJob(cronjobminutes, cronjobmessage)





