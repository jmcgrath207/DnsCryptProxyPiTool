from DnsCryptProxyPiTool.DefaultConfig import host,  password, user,dnscryptdownloadlink,\
dnscryptexractdir,loopbackstartaddress, editor
from DnsCryptProxyPiTool import ClickContextType
from click_help_colors import HelpColorsGroup
from DnsCryptProxyPiTool.ClickHelperClasses import ShowDefaultSingleQuote
import click
from DnsCryptProxyPiTool.FabricService.FabricExecute import FabricExecuteClass





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
@click.option('--edit_dnscrypt_proxy_config','-y',help='Edit Default Config of DnsCrypt Proxy Toml File',
              show_default=True, is_flag=True)
@click.option('--edit_dnscrypt_proxy_pi_tool_config','-w',help='Edit Default Config of dnscrypt-proxy-pi-tool command',
              show_default=True, is_flag=True)
@click.option('--show_dnscrypt_proxy_config','-z',help='show location of Default Config of DnsCrypt Proxy  Toml File',
              show_default=True, is_flag=True)
@click.option('--show_dnscrypt_proxy_pi_tool_config','-x',help='show location of Default Config of dnscrypt-proxy-pi-tool command',
              show_default=True, is_flag=True)
@click.option('--editor','-t',help="Supply which Editor you want to use ex. -t 'nano' -y",
              default=editor, show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--restart_config','-s',help='Restarts DnsMasq, Dnscrypt Service and Proxy. Use this after changing the  Dnscrypt Toml Config ',
              show_default=True, is_flag=True)
@click.option('--update_dnscrypt_proxy','-q',help='Update the DnsCrypt Proxy to Lastest Realease. WARNING: will cause Dnsmasq Restart',
              show_default=True, is_flag=True)
@click.option('--dnscryptexractdir', '-e', default=dnscryptexractdir,
              help='Directory for where the DnsCrypt Proxy is going to be downloaded and extracted at during Install',
              show_default=True,cls=ShowDefaultSingleQuote)
@click.pass_context
def admin(ctx: ClickContextType,show_dnscrypt_proxy_config: bool, show_dnscrypt_proxy_pi_tool_config: bool,
          edit_dnscrypt_proxy_config: bool, edit_dnscrypt_proxy_pi_tool_config: bool,editor: str,
          restart_config: bool, update_dnscrypt_proxy:bool,dnscryptexractdir:str):
    Fec = ctx.obj['Fabric']

    if show_dnscrypt_proxy_config:
        Fec.ExecuteShowDnsCryptProxyConfig()
        ctx.exit()

    elif show_dnscrypt_proxy_pi_tool_config:
        Fec.ExecuteShowDnsCryptPiHoleSetupConfig()
        ctx.exit()

    elif edit_dnscrypt_proxy_pi_tool_config:
        Fec.ExecuteEditDnsCryptPiHoleSetupConfig(editor)
        ctx.exit()

    elif edit_dnscrypt_proxy_config:
        Fec.ExecuteEditDnsCryptProxyConfig(editor)
        ctx.exit()

    elif restart_config:
        Fec.ExecuteRestartConfig()
        ctx.exit()

    elif update_dnscrypt_proxy:
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

