from DnsCryptPiHoleService.FabricService.FabricCommand import FabricCommandClass
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


    def ExecuteShowDefaultConfigLocation(self):
        execute(self.CommandShowDefaultConfigLocation, host=self.host)


    def ExecuteEditDefaultConfig(self):
        execute(self.CommandEditDefaultConfig, host=self.host)

    # New DnsCrypt Proxy seems to self recover well for now. May Need in the future
    #def ExecuteCreateCronJob(self,cronjobminutes: str,cronjobmessage: str):
    #    FabricCommandClass.CommandCreateCronJob.cronjobminutes = cronjobminutes
    #    FabricCommandClass.CommandCreateCronJob.cronjobmessage = cronjobmessage
    #    execute(self.CommandCreateCronJob, host=self.host)

