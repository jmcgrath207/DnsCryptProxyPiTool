
from DnsCryptPiHoleSetup.DefaultConfig import host,  password, user,dnscryptdownloadlink,\
dnscryptexractdir,loopbackstartaddress


from DnsCryptPiHoleSetup.FabricService import FabricExecute





def cli():
    Fec = FabricExecute.FabricExecuteClass(user, password, host,verbose=False)
    Fec.ExecuteFabric3OpenShellMonkeyPatch()
    #Fec.ExecuteSystemPackages()
    #Fec.ExecuteBuildDNSCrypt(dnscryptexractdir,dnscryptdownloadlink)
    #Fec.ExecuteCreateDNSCryptProxies(loopbackstartaddress, dnscryptexractdir)
    #Fec.ExecuteChangeDnsMasq()
    #Fec.ExecuteEditDefaultConfig()

    #Fec.ExecuteCreateCronJob(cronjobminutes,cronjobmessage)

cli()

