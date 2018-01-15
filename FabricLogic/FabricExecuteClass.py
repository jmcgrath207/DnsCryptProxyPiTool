from FabricLogic.FabricCommandClass import FabricCommandClass
from fabric.context_managers import env
from fabric.tasks import execute


class FabricExecuteClass(FabricCommandClass):


    def __init__(self,user: str = 'pi', password: str ='raspberry', host='localhost'):
        env.user = user
        env.password = password
        self.host = host




    def ExecuteSystemPackages(self):
        execute(self.CommandSystemPackages, host=self.host)

    def ExecuteBuildDNSCrypt(self):
        execute(self.CommandBuildDNSCrypt, host=self.host)

    def ExecuteAddDnsCryptUser(self):
        execute(self.CommandAddDnsCryptUser, host=self.host)