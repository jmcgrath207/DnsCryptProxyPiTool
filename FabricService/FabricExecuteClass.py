from FabricService.FabricCommandClass import FabricCommandClass
from FabricService import host,  password, user,DnsCryptDownloadLink,\
    DnsCryptExractDir,DnsCryptResolverCsvLink, DnsCryptResolverDir
from fabric.context_managers import env
from fabric.tasks import execute


class FabricExecuteClass(FabricCommandClass):


    def __init__(self,user: str = user, password: str = password,
                 host: str = host,DnsCryptDownloadLink: str = DnsCryptDownloadLink,
                 DnsCryptExractDir: str = DnsCryptExractDir):
        env.user = user
        env.password = password
        self.host = host
        super().__init__(DnsCryptDownloadLink=DnsCryptDownloadLink,
                         DnsCryptExractDir=DnsCryptExractDir,
                         DnsCryptResolverCsvLink=DnsCryptResolverCsvLink,
                         DnsCryptResolverDir=DnsCryptResolverDir)




    def ExecuteSystemPackages(self):
        execute(self.CommandSystemPackages, host=self.host)

    def ExecuteBuildDNSCrypt(self):
        execute(self.CommandBuildDNSCrypt, host=self.host)

    def ExecuteAddDnsCryptUser(self):
        execute(self.CommandAddDnsCryptUser, host=self.host)

    def ExecuteUpdateDnsCryptResolvers(self):
        execute(self.CommandUpdateDnsCryptResolvers, host=self.host)