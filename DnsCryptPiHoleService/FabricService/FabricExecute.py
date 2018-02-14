from DnsCryptPiHoleService.FabricService.FabricCommand import FabricCommandClass
from fabric.context_managers import env
from fabric.tasks import execute


class FabricExecuteClass(FabricCommandClass):


    def __init__(self,user: str, password: str,
                 host: str):
        env.user = user
        env.password = password
        env.warn_only = True
        env.colorize_errors = True
        self.host = host
        self.ListenAddress = None



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


    def ExecuteChangeDnsMasq(self):
        FabricCommandClass.CommandChangeDnsMasq.ListenAddress = self.ListenAddress
        FabricCommandClass.CommandChangeDnsMasq.host = self.host
        execute(self.CommandChangeDnsMasq, host=self.host)


    def ExecuteCreateCronJob(self,cronjobminutes: str,cronjobmessage: str):
        FabricCommandClass.CommandCreateCronJob.cronjobminutes = cronjobminutes
        FabricCommandClass.CommandCreateCronJob.cronjobmessage = cronjobmessage
        execute(self.CommandCreateCronJob, host=self.host)

