from DnsCryptPiHoleService.DefaultConfig import host,  password, user,dnscryptdownloadlink,\
dnscryptexractdir,loopbackstartaddress
from DnsCryptPiHoleService import ClickContextType
from click_help_colors import HelpColorsGroup
from DnsCryptPiHoleService.ClickHelperClasses import ShowDefaultSingleQuote
import click
from DnsCryptPiHoleService.FabricService.FabricExecute import FabricExecuteClass





@click.group(context_settings=dict(max_content_width=500),
               cls=HelpColorsGroup, help_options_color='blue', help_headers_color='yellow')
@click.option('--host', '-h', default=host, help='Host or IP address that the Dnscrypt proxy script will ran against',
              show_default=True, cls=ShowDefaultSingleQuote)
@click.option('--user', '-u', default=user, help='Username for host that the Dnscrypt proxy script will ran against',
              show_default=True, cls=ShowDefaultSingleQuote)
@click.option('--password', '-p', default=password,
              help='Password for host that the Dnscrypt proxy script will ran against', show_default=True,
              cls=ShowDefaultSingleQuote)
@click.option('--verbose','-v',help='Shows Linux Commands that are executed', show_default=True, is_flag=True)
@click.pass_context
def mainCommand(ctx: ClickContextType,host: str, user: str, password: str, verbose: bool):
    ctx.obj['Fabric'] = FabricExecuteClass(user, password, host, verbose)







@mainCommand.command()
@click.option('--dnscryptexractdir', '-e', default=dnscryptexractdir,
              help='Directory for where the DnsCrypt Proxy is going to be downloaded and extracted at during Install',
              show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--dnscryptdownloadlink', '-d', default=dnscryptdownloadlink,
              help='HTTP address of DNScrypt.tar.gz',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--loopbackstartaddress', '-l', default=loopbackstartaddress,
              help='IPV4 Loopback Address you want to use for the socket unit file. The address will increment by the last octet when multiple proxies are installed',
              show_default=True,cls=ShowDefaultSingleQuote)
@click.confirmation_option(prompt='Are you sure you want to install DnsCrypt-Proxy 2?')
@click.pass_context
def install(ctx: ClickContextType,dnscryptexractdir: str,dnscryptdownloadlink: str,
            loopbackstartaddress: str):
    Fec = ctx.obj['Fabric']
    Fec.ExecuteFabric3OpenShellMonkeyPatch()
    Fec.ExecuteSystemPackages()
    Fec.ExecuteBuildDNSCrypt(dnscryptexractdir,dnscryptdownloadlink)
    Fec.ExecuteCreateDNSCryptProxies(loopbackstartaddress, dnscryptexractdir)
    Fec.ExecuteChangeDnsMasq(dnscryptexractdir)
    ctx.exit()





@mainCommand.command()
@click.confirmation_option(prompt='Are you sure you want to uninstall DnsCrypt-Proxy 2?')
@click.pass_context
def uninstall(ctx: ClickContextType):
    Fec = ctx.obj['Fabric']
    Fec.ExecuteUninstall()
    ctx.exit()





@mainCommand.command()
@click.option('--editdefault','-y',help='Edit Default Config of dnscryptpiholesetup command', show_default=True, is_flag=True)
@click.option('--showdefaultconfiglocation','-z',help='show location of default config file for dnscryptpiholesetup command', show_default=True, is_flag=True)
@click.pass_context
def config(ctx: ClickContextType,showdefaultconfiglocation: bool, editdefault: bool ):
    Fec = ctx.obj['Fabric']

    #if showdefaultconfiglocation:
    #    Fec.ExecuteShowDefaultConfigLocation()
    #    ctx.exit()
    # Disabled until issue is fixed https://github.com/fabric/fabric/issues/1719
    # Root Cause is https://github.com/fabric/fabric/issues/196 will be fixed in Fabric V2
    if editdefault:
        Fec.ExecuteEditDefaultConfig()
        ctx.exit()
    else:
        click.echo(config.get_help(ctx))
        ctx.exit()





if __name__ == '__main__':
    mainCommand(obj={})

