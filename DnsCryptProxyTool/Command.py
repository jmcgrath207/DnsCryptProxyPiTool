from DnsCryptProxyTool.DefaultConfig import host,  password, user,dnscryptdownloadlink,\
dnscryptexractdir,loopbackstartaddress, editor
from DnsCryptProxyTool import ClickContextType
from click_help_colors import HelpColorsGroup
from DnsCryptProxyTool.ClickHelperClasses import ShowDefaultSingleQuote
import click
from DnsCryptProxyTool.FabricService.FabricExecute import FabricExecuteClass





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

    # Creates Object when not ran by the main function
    ctx.obj = {}
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
    Fec.ExecuteSystemPackages()
    Fec.ExecuteBuildDNSCrypt(dnscryptexractdir,dnscryptdownloadlink)
    Fec.ExecuteCreateDNSCryptProxies(loopbackstartaddress, dnscryptexractdir)
    Fec.ExecuteChangeDnsMasq(dnscryptexractdir)
    Fec.ExecuteFabric3OpenShellMonkeyPatch()
    click.echo(click.style('DnsCrypt-Proxy 2 config located at /etc/dnscrypt-proxy/dnscrypt-proxy.toml ', fg='green',
                           bold=True))
    click.echo(click.style('DnsCrypt-Proxy 2 install is Complete', fg='green', bold=True))
    ctx.exit()





@mainCommand.command()
@click.confirmation_option(prompt='Are you sure you want to uninstall DnsCrypt-Proxy 2?')
@click.pass_context
def uninstall(ctx: ClickContextType):
    Fec = ctx.obj['Fabric']
    Fec.ExecuteUninstall()
    click.echo(click.style('DnsCrypt-Proxy 2 Uninstall is Complete', fg='green', bold=True))
    click.echo(click.style('The Original PiHole Config has been restored', fg='green', bold=True))
    click.echo(click.style('The Dnsmasq Service has been restarted', fg='green', bold=True))
    ctx.exit()





@mainCommand.command()
@click.option('--editdnscryptproxyconfig','-y',help='Edit Default Config of DnsCrypt Proxy  Toml File',
              show_default=True, is_flag=True)
@click.option('--editdnscryptpiholesetupconfig','-w',help='Edit Default Config of dnscryptpiholesetup command',
              show_default=True, is_flag=True)
@click.option('--showdnscryptproxyconfig','-z',help='show location of Default Config of DnsCrypt Proxy  Toml File',
              show_default=True, is_flag=True)
@click.option('--showdnscryptpiholesetupconfig','-x',help='show location of Default Config of dnscryptpiholesetup command',
              show_default=True, is_flag=True)
@click.option('--editor','-t',help="Supply which Editor you want to use ex. -t 'nano' -y",
              default=editor, show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--restartconfig','-s',help='Restarts DnsMasq, Dnscrypt Service and Proxy. Use this after changing the  Dnscrypt Toml Config ',
              show_default=True, is_flag=True)
@click.option('--updatednscryptproxy','-q',help='Update the DnsCrypt Proxy to Lastest Realease. WARNING: will cause Dnsmasq Restart',
              show_default=True, is_flag=True)
@click.option('--dnscryptexractdir', '-e', default=dnscryptexractdir,
              help='Directory for where the DnsCrypt Proxy is going to be downloaded and extracted at during Install',
              show_default=True,cls=ShowDefaultSingleQuote)
@click.pass_context
def admin(ctx: ClickContextType,showdnscryptproxyconfig: bool, showdnscryptpiholesetupconfig: bool,
           editdnscryptproxyconfig: bool, editdnscryptpiholesetupconfig: bool,editor: str,
          restartconfig: bool, updatednscryptproxy:bool,dnscryptexractdir:str):
    Fec = ctx.obj['Fabric']

    if showdnscryptproxyconfig:
        Fec.ExecuteShowDnsCryptProxyConfig()
        ctx.exit()

    elif showdnscryptpiholesetupconfig:
        Fec.ExecuteShowDnsCryptPiHoleSetupConfig()
        ctx.exit()

    elif editdnscryptpiholesetupconfig:
        Fec.ExecuteEditDnsCryptPiHoleSetupConfig(editor)
        ctx.exit()

    elif editdnscryptproxyconfig:
        Fec.ExecuteEditDnsCryptProxyConfig(editor)
        ctx.exit()

    elif restartconfig:
        Fec.ExecuteRestartConfig()
        ctx.exit()

    elif updatednscryptproxy:
        Fec.ExecuteUpdateCheckDnsCryptProxy(dnscryptexractdir)
        Fec.ExecuteUpgradeDnsCryptProxy(dnscryptexractdir)
        Fec.ExecuteRestartConfig()
        click.echo(
            click.style('DnsCrypt-Proxy 2 Upgrade is Complete', fg='green', bold=True))
        ctx.exit()

    else:
        click.echo(admin.get_help(ctx))
        ctx.exit()





if __name__ == '__main__':
    mainCommand(obj={})

