
from DnsCryptPiHoleSetup.DefaultConfig import host,  password, user,dnscryptdownloadlink,\
dnscryptexractdir,loopbackstartaddress, cronjobmessage, cronjobminutes


from DnsCryptPiHoleSetup.FabricService import FabricExecute





def cli():
    Fec = FabricExecute.FabricExecuteClass(user, password, host)
    Fec.ExecuteSystemPackages()
    #Fec.ExecuteBuildDNSCrypt(dnscryptexractdir,dnscryptdownloadlink)
    Fec.ExecuteCreateDNSCryptProxies(loopbackstartaddress, dnscryptexractdir)
    Fec.ExecuteChangeDnsMasq()
    #Fec.ExecuteCreateCronJob(cronjobminutes,cronjobmessage)

cli()

