
from DefaultConfig import host,  password, user,dnscryptdownloadlink,\
dnscryptexractdir,dnscryptresolvercsvlink, dnscryptresolverdir,\
    dnscryptresolvernames, loopbackstartaddress, cronjobmessage, \
    cronjobtime

import click
from click_help_colors import  HelpColorsCommand
from FabricService import FabricExecuteClass










@click.command(context_settings=dict(max_content_width=300),
               cls=HelpColorsCommand,help_options_color='blue',help_headers_color='yellow')
@click.option('--host', default=host, help='Host or IP address that the Dnscrypt proxy script will ran against',show_default=True)
@click.option('--user', default=user, help='Username for host that the Dnscrypt proxy script will ran against',show_default=True)
@click.option('--password', default=password, help='Password for host that the Dnscrypt proxy script will ran against',show_default=True)
@click.option('--dnscryptexractdir', default=dnscryptexractdir, help='Directory for where the DnsCrypt Proxy is going to be downloaded and extracted at during Install',show_default=True)
@click.option('--dnscryptdownloadlink', default=dnscryptdownloadlink, help='HTTP address of DNScrypt.tar.gz',show_default=True)
@click.option('--dnscryptresolvercsvlink', default=dnscryptresolvercsvlink, help='HTTP address of the Csv for  DnsCrypt Resolvers',show_default=True)
@click.option('--dnscryptresolverdir', default=dnscryptresolverdir, help='Directory location of where the Csv resolver files are stored',show_default=True)
@click.option('--dnscryptresolvernames', default=dnscryptresolvernames, help='Name of resolvers to be installed',show_default=True,type=list,multiple=True)
@click.option('--loopbackstartaddress', default=loopbackstartaddress, help='IPV4 Loopback Address you want to use for the socket unit file. The address will increment by the last octet when multiple proxies are installed',show_default=True)
@click.option('--cronjobtime', default=cronjobtime, help='CronJob Time that you want to use for check if there is errors and restarting the individual dnscrypt proxy',show_default=True)
@click.option('--cronjobmessage', default=cronjobmessage, help='The Message you want to match on the DnsCrypt Proxy System Log to Trigger a Restart Event',show_default=True)
def cli(host, password, user,dnscryptexractdir,dnscryptdownloadlink,
        dnscryptresolvercsvlink,dnscryptresolverdir,dnscryptresolvernames,
        loopbackstartaddress,cronjobtime,cronjobmessage
        ):
    Fec = FabricExecuteClass.FabricExecuteClass(user,password,host)
    Fec.ExecuteSystemPackages()
    Fec.ExecuteBuildDNSCrypt(dnscryptexractdir,dnscryptdownloadlink)
    Fec.ExecuteAddDnsCryptUser()
    Fec.ExecuteDownloadDnsCryptResolvers(dnscryptresolvercsvlink,dnscryptresolverdir)
    Fec.ExecuteCreateDNSCryptProxies(dnscryptresolverdir,dnscryptresolvernames,dnscryptresolvercsvlink,
                                     loopbackstartaddress, dnscryptexractdir)
    Fec.ExecuteChangeDnsMasq(dnscryptresolvernames)
    Fec.ExecuteCreateCronJob(cronjobtime,cronjobmessage)



