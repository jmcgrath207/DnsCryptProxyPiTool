from DnsCryptProxyPiTool.FabricService.FabricCommand import FabricCommandClass
from fabric.context_managers import env, output
from fabric.tasks import execute


class FabricExecuteClass(FabricCommandClass):


    def __init__(self,user: str, password: str,
                 host: str,verbose: bool):
        if not verbose:
            output['user'] = False
            output['aborts'] = False
            output['running'] = False
            output['exceptions'] = False
            output['warnings'] = False
            output['stderr'] = False
            output['stdout'] = False
            output['status'] = False
            output['debug'] = False


        env.user = user
        env.password = password
        env.warn_only = True
        env.colorize_errors = True
        self.host = host
        self.ListenAddress = None


    def ExecuteFabric3OpenShellMonkeyPatch(self):
        execute(self.CommandFabric3OpenShellMonkeyPatch, host=self.host)

    def ExecuteSystemPackages(self):
        execute(self.CommandSystemPackages, host=self.host)

    def ExecuteBuildDNSCrypt(self, dnscryptexractdir: str,dnscryptdownloadlink: str):
        FabricCommandClass.CommandBuildDNSCrypt.dnscryptexractdir = dnscryptexractdir
        FabricCommandClass.CommandBuildDNSCrypt.dnscryptdownloadlink = dnscryptdownloadlink
        execute(self.CommandBuildDNSCrypt, host=self.host)


    def ExecuteCreateDNSCryptProxies(self,loopbackstartaddress: str, dnscryptexractdir: str):
        FabricCommandClass.CommandCreateDNSCryptProxies.loopbackstartaddress = loopbackstartaddress
        FabricCommandClass.CommandCreateDNSCryptProxies.dnscryptexractdir = dnscryptexractdir
        self.ListenAddress = execute(self.CommandCreateDNSCryptProxies, host=self.host)


    def ExecuteChangeDnsMasq(self, dnscryptexractdir: str):
        FabricCommandClass.CommandChangeDnsMasq.ListenAddress = self.ListenAddress
        FabricCommandClass.CommandChangeDnsMasq.host = self.host
        FabricCommandClass.CommandChangeDnsMasq.dnscryptexractdir = dnscryptexractdir
        execute(self.CommandChangeDnsMasq, host=self.host)

    def ExecuteUninstall(self):
        execute(self.CommandUninstall, host=self.host)


    def ExecuteShowDnsCryptProxyConfig(self):
        execute(self.CommandShowDnsCryptProxyConfig, host=self.host)


    def ExecuteEditDnsCryptProxyConfig(self,editor: str):
        FabricCommandClass.CommandEditDnsCryptProxyConfig.editor = editor
        execute(self.CommandEditDnsCryptProxyConfig, host=self.host)


    def ExecuteShowDnsCryptPiHoleSetupConfig(self):
        execute(self.CommandShowDnsCryptPiHoleSetupConfig, host=self.host)

    def ExecuteEditDnsCryptPiHoleSetupConfig(self,editor: str):
        FabricCommandClass.CommandEditDnsCryptPiHoleSetupConfig.editor = editor
        execute(self.CommandEditDnsCryptPiHoleSetupConfig, host=self.host)

    def ExecuteRestartConfig(self):
        execute(self.CommandRestartConfig, host=self.host)

    def ExecuteUpdateCheckDnsCryptProxy(self,dnscryptexractdir: str):
        FabricCommandClass.CommandUpdateCheckDnsCryptProxy.dnscryptexractdir = dnscryptexractdir
        execute(self.CommandUpdateCheckDnsCryptProxy, host=self.host)


    def ExecuteUpgradeDnsCryptProxy(self, dnscryptexractdir: str):
        FabricCommandClass.CommandUpgradeDnsCryptProxy.dnscryptexractdir = dnscryptexractdir
        execute(self.CommandUpgradeDnsCryptProxy, host=self.host)








