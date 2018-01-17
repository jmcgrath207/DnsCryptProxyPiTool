from FabricService.FabricCommandClass import FabricCommandClass
from FabricService import host,  password, user,DnsCryptDownloadLink,\
    DnsCryptExractDir,DnsCryptResolverCsvLink, DnsCryptResolverDir,\
    DnsCryptResolverNames, LoopBackStartAddress
from fabric.context_managers import env
from fabric.tasks import execute


class FabricExecuteClass(FabricCommandClass):


    def __init__(self,user: str = user, password: str = password,
                 host: str = host):
        env.user = user
        env.password = password
        env.warn_only = True
        self.host = host





    def ExecuteSystemPackages(self):
        execute(self.CommandSystemPackages, host=self.host)

    def ExecuteBuildDNSCrypt(self):
        FabricCommandClass.CommandBuildDNSCrypt.DnsCryptExractDir = DnsCryptExractDir
        FabricCommandClass.CommandBuildDNSCrypt.DnsCryptDownloadLink = DnsCryptDownloadLink
        execute(self.CommandBuildDNSCrypt, host=self.host)

    def ExecuteAddDnsCryptUser(self):
        execute(self.CommandAddDnsCryptUser, host=self.host)

    def ExecuteUpdateDnsCryptResolvers(self):
        FabricCommandClass.CommandUpdateDnsCryptResolvers.DnsCryptResolverCsvLink = DnsCryptResolverCsvLink
        FabricCommandClass.CommandUpdateDnsCryptResolvers.DnsCryptResolverDir = DnsCryptResolverDir
        execute(self.CommandUpdateDnsCryptResolvers, host=self.host)

    def ExecuteCreateDNSCryptProxies(self):
        FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptResolverDir = DnsCryptResolverDir
        FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptResolverNames = DnsCryptResolverNames
        FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptResolverCsvLink = DnsCryptResolverCsvLink
        FabricCommandClass.CommandCreateDNSCryptProxies.LoopBackStartAddress = LoopBackStartAddress
        FabricCommandClass.CommandCreateDNSCryptProxies.DnsCryptExractDir = DnsCryptExractDir
        execute(self.CommandCreateDNSCryptProxies, host=self.host)
