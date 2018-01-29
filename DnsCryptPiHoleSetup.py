import click
from FabricService import FabricExecuteClass






@click.command()
def cli():
    Fec = FabricExecuteClass.FabricExecuteClass()
    Fec.ExecuteSystemPackages()
    Fec.ExecuteBuildDNSCrypt()
    Fec.ExecuteAddDnsCryptUser()
    Fec.ExecuteDownloadDnsCryptResolvers()
    Fec.ExecuteCreateDNSCryptProxies()
    Fec.ExecuteChangeDnsMasq()
    Fec.ExecuteCreateCronJob()