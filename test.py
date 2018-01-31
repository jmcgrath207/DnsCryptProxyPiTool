
from DnsCryptPiHoleSetup.DefaultConfig import host,  password, user, cronjobmessage, \
    cronjobminutes


from DnsCryptPiHoleSetup.FabricService import FabricExecute





def cli():
    Fec = FabricExecute.FabricExecuteClass(user, password, host)
    #Fec.ExecuteSystemPackages()
    #Fec.ExecuteBuildDNSCrypt(dnscryptexractdir,dnscryptdownloadlink)
    #Fec.ExecuteAddDnsCryptUser()
    #Fec.ExecuteDownloadDnsCryptResolvers(dnscryptresolvercsvlink,dnscryptresolverdir)
    #Fec.ExecuteCreateDNSCryptProxies(dnscryptresolverdir,dnscryptresolvernames,dnscryptresolvercsvlink,
    #                                 loopbackstartaddress, dnscryptexractdir)
    #Fec.ExecuteChangeDnsMasq(dnscryptresolvernames)
    Fec.ExecuteCreateCronJob(cronjobminutes,cronjobmessage)





cli()

