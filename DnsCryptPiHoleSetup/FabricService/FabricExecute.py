from DnsCryptPiHoleSetup.FabricService.FabricCommand import FabricCommandClass
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

    def ExecuteBuildDNSCrypt(self, dnscryptexractdir: str,dnscryptdownloadlink: str):
        FabricCommandClass.CommandBuildDNSCrypt.dnscryptexractdir = dnscryptexractdir
        FabricCommandClass.CommandBuildDNSCrypt.dnscryptdownloadlink = dnscryptdownloadlink
        execute(self.CommandBuildDNSCrypt, host=self.host)

    def ExecuteAddDnsCryptUser(self):
        execute(self.CommandAddDnsCryptUser, host=self.host)

    def ExecuteDownloadDnsCryptResolvers(self,dnscryptresolvercsvlink: str,dnscryptresolverdir: str):
        FabricCommandClass.CommandDownloadDnsCryptResolvers.dnscryptresolvercsvlink = dnscryptresolvercsvlink
        FabricCommandClass.CommandDownloadDnsCryptResolvers.dnscryptresolverdir = dnscryptresolverdir
        execute(self.CommandDownloadDnsCryptResolvers, host=self.host)

    def ExecuteCreateDNSCryptProxies(self,dnscryptresolverdir:str,dnscryptresolvernames:str,dnscryptresolvercsvlink:str,
                                     loopbackstartaddress: str, dnscryptexractdir: str):
        FabricCommandClass.CommandCreateDNSCryptProxies.dnscryptresolverdir = dnscryptresolverdir
        FabricCommandClass.CommandCreateDNSCryptProxies.dnscryptresolvernames = dnscryptresolvernames
        FabricCommandClass.CommandCreateDNSCryptProxies.dnscryptresolvercsvlink = dnscryptresolvercsvlink
        FabricCommandClass.CommandCreateDNSCryptProxies.loopbackstartaddress = loopbackstartaddress
        FabricCommandClass.CommandCreateDNSCryptProxies.dnscryptexractdir = dnscryptexractdir
        self.ListenAddresses = execute(self.CommandCreateDNSCryptProxies, host=self.host)


    def ExecuteChangeDnsMasq(self,dnscryptresolvernames: str):
        FabricCommandClass.CommandChangeDnsMasq.dnscryptresolvernames = dnscryptresolvernames
        FabricCommandClass.CommandChangeDnsMasq.ListenAddresses = self.ListenAddresses
        FabricCommandClass.CommandChangeDnsMasq.host = self.host
        execute(self.CommandChangeDnsMasq, host=self.host)


    def ExecuteCreateCronJob(self,cronjobminutes: str,cronjobmessage: str):
        FabricCommandClass.CommandCreateCronJob.cronjobminutes = cronjobminutes
        FabricCommandClass.CommandCreateCronJob.cronjobmessage = cronjobmessage
        execute(self.CommandCreateCronJob, host=self.host)

