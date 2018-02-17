
from DnsCryptPiHoleService.DefaultConfig import host,  password, user,dnscryptdownloadlink,\
dnscryptexractdir,loopbackstartaddress, cronjobmessage, cronjobminutes


from DnsCryptPiHoleService.FabricService import FabricExecute





def cli():
    Fec = FabricExecute.FabricExecuteClass(user, password, host,verbose=False)
    #Fec.ExecuteSystemPackages()
    #Fec.ExecuteBuildDNSCrypt(dnscryptexractdir,dnscryptdownloadlink)
    #Fec.ExecuteCreateDNSCryptProxies(loopbackstartaddress, dnscryptexractdir)
    #Fec.ExecuteChangeDnsMasq()
    Fec.ExecuteEditDefaultConfig()

    #Fec.ExecuteCreateCronJob(cronjobminutes,cronjobmessage)

cli()

