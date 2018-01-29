
import click
from click_help_colors import  HelpColorsCommand
from FabricService import FabricExecuteClass
from DefaultConfig import host,  password, user,DnsCryptDownloadLink,\
    DnsCryptExractDir,DnsCryptResolverCsvLink, DnsCryptResolverDir,\
    DnsCryptResolverNames, LoopBackStartAddress, CronJobMessage, \
    CronJobTime









@click.command(context_settings=dict(max_content_width=300),
               cls=HelpColorsCommand,help_options_color='blue',help_headers_color='yellow',)
@click.option('--host', default=host, help='Host or IP address that the Dnscrypt proxy script will ran against',show_default=True)
@click.option('--user', default=user, help='Username for host that the Dnscrypt proxy script will ran against',show_default=True)
@click.option('--password', default=password, help='Password for host that the Dnscrypt proxy script will ran against',show_default=True)
@click.option('--DnsCryptExractDir', default=DnsCryptExractDir, help='Directory for where the DnsCrypt Proxy is going to be downloaded and extracted at during Install',show_default=True)
@click.option('--DnsCryptDownloadLink', default=DnsCryptDownloadLink, help='HTTP address of DNScrypt.tar.gz',show_default=True)
@click.option('--DnsCryptResolverCsvLink', default=DnsCryptResolverCsvLink, help='HTTP address of the Csv for  DnsCrypt Resolvers',show_default=True)
@click.option('--DnsCryptResolverDir', default=DnsCryptResolverDir, help='Directory location of where the Csv resolver files are stored',show_default=True)
@click.option('--DnsCryptResolverNames', default=DnsCryptResolverNames, help='Name of resolvers to be installed',show_default=True,type=list,multiple=True)
@click.option('--LoopBackStartAddress', default=LoopBackStartAddress, help='IPV4 Loopback Address you want to use for the socket unit file. The address will increment by the last octet when multiple proxies are installed',show_default=True)
@click.option('--CronJobTime', default=CronJobTime, help='CronJob Time that you want to use for check if there is errors and restarting the individual dnscrypt proxy',show_default=True)
@click.option('--CronJobMessage', default=CronJobMessage, help='The Message you want to match on the DnsCrypt Proxy System Log to Trigger a Restart Event',show_default=True)
def cli():
    Fec = FabricExecuteClass.FabricExecuteClass(user,password,host)
    Fec.ExecuteSystemPackages()
    Fec.ExecuteBuildDNSCrypt(DnsCryptExractDir,DnsCryptDownloadLink)
    Fec.ExecuteAddDnsCryptUser()
    Fec.ExecuteDownloadDnsCryptResolvers(DnsCryptResolverCsvLink,DnsCryptResolverDir)
    Fec.ExecuteCreateDNSCryptProxies(DnsCryptResolverDir,DnsCryptResolverNames,DnsCryptResolverCsvLink,
                                     LoopBackStartAddress, DnsCryptExractDir)
    Fec.ExecuteChangeDnsMasq(DnsCryptResolverNames)
    Fec.ExecuteCreateCronJob(CronJobTime,CronJobMessage)



