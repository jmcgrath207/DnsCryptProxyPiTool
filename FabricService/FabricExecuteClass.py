from FabricService.FabricCommandClass import FabricCommandClass
from fabric.context_managers import env
from fabric.tasks import execute


class FabricExecuteClass(FabricCommandClass):


    def __init__(self,user: str, password: str,
                 host: str):
        env.user = user
        env.password = password
        env.warn_only = True
        self.host = host
        self.ListenAddresses = None





    def ExecuteSystemPackages(self):
        execute(self.CommandSystemPackages, host=self.host)

    def ExecuteBuildDNSCrypt(self, DnsCryptExractDir: str,DnsCryptDownloadLink: str):
        FabricCommandClass.CommandBuildDNSCrypt.DnsCryptExractDir = DnsCryptExractDir
        FabricCommandClass.CommandBuildDNSCrypt.DnsCryptDownloadLink = DnsCryptDownloadLink
        execute(self.CommandBuildDNSCrypt, host=self.host)

    def ExecuteAddDnsCryptUser(self):
        execute(self.CommandAddDnsCryptUser, host=self.host)

    def ExecuteDownloadDnsCryptResolvers(self,DnsCryptResolverCsvLink: str,DnsCryptResolverDir: str):
        FabricCommandClass.CommandDownloadDnsCryptResolvers.DnsCryptResolverCsvLink = DnsCryptResolverCsvLink
        FabricCommandClass.CommandDownloadDnsCryptResolvers.DnsCryptResolverDir = DnsCryptResolverDir
        execute(self.CommandDownloadDnsCryptResolvers, host=self.host)

    def ExecuteCreateDNSCryptProxies(self,DnsCryptResolverDir:str,DnsCryptResolverNames:str,DnsCryptResolverCsvLink:str,
                                     LoopBackStartAddress: str, DnsCryptExractDir: str):
        FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptResolverDir = DnsCryptResolverDir
        FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptResolverNames = DnsCryptResolverNames
        FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptResolverCsvLink = DnsCryptResolverCsvLink
        FabricCommandClass.CommandCreateDNSCryptProxies.LoopBackStartAddress = LoopBackStartAddress
        FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptExractDir = DnsCryptExractDir
        self.ListenAddresses = execute(self.CommandCreateDNSCryptProxies, host=self.host)


    def ExecuteChangeDnsMasq(self,DnsCryptResolverNames: str):
        FabricCommandClass.CommandChangeDnsMasq.DnsCryptResolverNames = DnsCryptResolverNames
        FabricCommandClass.CommandChangeDnsMasq.ListenAddresses = self.ListenAddresses
        FabricCommandClass.CommandChangeDnsMasq.host = self.host
        execute(self.CommandChangeDnsMasq, host=self.host)


    def ExecuteCreateCronJob(self,CronJobTime: str,CronJobMessage: str):
        FabricCommandClass.CommandCreateCronJob.CronJobTime = CronJobTime
        FabricCommandClass.CommandCreateCronJob.CronJobMessage = CronJobMessage
        execute(self.CommandCreateCronJob, host=self.host)

