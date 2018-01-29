
from DefaultConfig import host,  password, user,dnscryptdownloadlink,\
dnscryptexractdir,dnscryptresolvercsvlink, dnscryptresolverdir,\
    dnscryptresolvernames, loopbackstartaddress, cronjobmessage, \
    cronjobtime


from FabricService import FabricExecuteClass





def cli():
    Fec = FabricExecuteClass.FabricExecuteClass(user,password,host)
    Fec.ExecuteSystemPackages()
    Fec.ExecuteBuildDNSCrypt(dnscryptexractdir,dnscryptdownloadlink)
    Fec.ExecuteAddDnsCryptUser()
    Fec.ExecuteDownloadDnsCryptResolvers(dnscryptresolvercsvlink,dnscryptresolverdir)
    Fec.ExecuteCreateDNSCryptProxies(dnscryptresolverdir,dnscryptresolvernames,dnscryptresolvercsvlink,
                                     loopbackstartaddress, dnscryptexractdir)
    Fec.ExecuteChangeDnsMasq(dnscryptresolvernames)
    Fec.ExecuteCreateCronJob(cronjobtime,cronjobmessage)





cli()