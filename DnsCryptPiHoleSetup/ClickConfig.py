
from DnsCryptPiHoleSetup.DefaultConfig import dnscryptdownloadlink,\
dnscryptexractdir,dnscryptresolvercsvlink, dnscryptresolverdir,\
    dnscryptresolvernames, loopbackstartaddress, cronjobmessage, \
    cronjobminutes

from DnsCryptPiHoleSetup.ClickHelperClasses import ShowDefaultSingleQuote, ListArgs

import click

from DnsCryptPiHoleSetup.FabricService.FabricExecute import FabricExecuteClass



@click.group()
def install():
    pass

@install.command()
@click.option('--dnscryptexractdir', '-e', default=dnscryptexractdir, help='Directory for where the DnsCrypt Proxy is going to be downloaded and extracted at during Install',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--dnscryptdownloadlink', '-d', default=dnscryptdownloadlink, help='HTTP address of DNScrypt.tar.gz',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--dnscryptresolvercsvlink','-c', default=dnscryptresolvercsvlink, help='HTTP address of the Csv for  DnsCrypt Resolvers',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--dnscryptresolverdir', '-r',default=dnscryptresolverdir, help='Directory location of where the Csv resolver files are stored',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--dnscryptresolvernames','-n', default=dnscryptresolvernames, help='Name of resolvers to be installed',show_default=True,type=list,cls=ListArgs)
@click.option('--loopbackstartaddress', '-l', default=loopbackstartaddress, help='IPV4 Loopback Address you want to use for the socket unit file. The address will increment by the last octet when multiple proxies are installed',show_default=True,cls=ShowDefaultSingleQuote)
def cmd1():
    """Command on cli1"""


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
    """Command on cli1"""





def cli(host, password, user,dnscryptexractdir,dnscryptdownloadlink,
        dnscryptresolvercsvlink,dnscryptresolverdir,dnscryptresolvernames,
        loopbackstartaddress,cronjobminutes,cronjobmessage
        ):
    Fec = FabricExecuteClass(user, password, host)
    Fec.ExecuteSystemPackages()
    Fec.ExecuteBuildDNSCrypt(dnscryptexractdir,dnscryptdownloadlink)
    Fec.ExecuteAddDnsCryptUser()
    Fec.ExecuteDownloadDnsCryptResolvers(dnscryptresolvercsvlink,dnscryptresolverdir)
    Fec.ExecuteCreateDNSCryptProxies(dnscryptresolverdir,dnscryptresolvernames,dnscryptresolvercsvlink,
                                     loopbackstartaddress, dnscryptexractdir)
    Fec.ExecuteChangeDnsMasq(dnscryptresolvernames)
    Fec.ExecuteCreateCronJob(cronjobminutes,cronjobmessage)



