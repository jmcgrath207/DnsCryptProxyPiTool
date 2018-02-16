from fabric.api import sudo, cd, run
from fabric.contrib.files import append as fabappend, comment
from fabric.context_managers import env
import re
import ipaddress
import click
from DnsCryptPiHoleService.FabricService.StringContainer import DnsCryptService, DnsCryptSocket,\
    DnsCryptConf, DnsCryptSudoer




class FabricCommandClass(object):



    def CommandSystemPackages(self):
        """
        Installs required ssh packages
        :return:
        """
        requiredPackages = "build-essential  " \
                           "bash-completion libsystemd-dev pkg-config python3-dev  jq"
        returnCode = run("dpkg -l " + requiredPackages)
        if(returnCode.failed):
            sudo('sudo apt-get update')
            click.echo(click.style('Installing system dependencies: {0} for DNS Crypt Proxy 2'.format(requiredPackages),fg='yellow'))
            sudo('apt-get -y install ' + requiredPackages)



    def CommandBuildDNSCrypt(self):
        """
        Install DnsCrypt Proxy if not present

        :return:
        """


        dnscryptexractdir = FabricCommandClass.CommandBuildDNSCrypt.dnscryptexractdir
        dnscryptdownloadlink = FabricCommandClass.CommandBuildDNSCrypt.dnscryptdownloadlink


        returnCode = run("which dnscrypt-proxy")
        if(returnCode.failed):
            with cd(dnscryptexractdir):

                click.echo(
                    click.style('Downloading DNS Crypt Proxy 2 from: {0}'.format(dnscryptdownloadlink), fg='yellow'))

                click.echo(
                    click.style('Building DNS Crypt Proxy 2 at path: {0}/dnscryptBuild/'.format(dnscryptexractdir),
                                fg='yellow'))

                run('wget ' + dnscryptdownloadlink)
                run("mkdir -p " + dnscryptexractdir + "/dnscryptBuild/")
                run('tar -xf dnscrypt*.tar.gz -C dnscryptBuild --strip-components=1')
        else:
          raise  click.ClickException(click.style("Dns Crypt Proxy 2 is already installed at " + re.sub( r'.*\r\n',"",returnCode.stdout) + \
                ". Aborting Install",fg='red',bold=True))



    def CommandCreateDNSCryptProxies(self) -> str:
        """
        Creates Dns Crypt Proxies
        :return: ListenAddress
        """



        loopbackstartaddress  = FabricCommandClass.CommandCreateDNSCryptProxies.loopbackstartaddress
        dnscryptexractdir = FabricCommandClass.CommandCreateDNSCryptProxies.dnscryptexractdir



        # Find a Available Socket LoopBack Address and Create Socket Files

        click.echo(click.style('finding available loopback address and port for dnscrypt-proxy.socket', fg='yellow'))
        runningSockets = sudo("ss -nlut | awk 'NR>1 {print  $5}'")
        runningSockets = re.sub(r".*[a-zA-Z]+\S","",runningSockets).split()


        with cd(dnscryptexractdir + "/dnscryptBuild/"):
            # Clear Old Socket and Service Files
            run("rm dnscrypt-proxy.s*")

            # Find a available loopback address
            while True:
                if loopbackstartaddress + ":41" not in runningSockets:
                    fabappend("dnscrypt-proxy.socket", DnsCryptSocket.format(loopbackstartaddress))
                    runningSockets.append(loopbackstartaddress + ":41")
                    ListenAddress = loopbackstartaddress
                    click.echo(click.style('Using ' + loopbackstartaddress + ':41 for dnscrypt-proxy.socket',
                                           fg='yellow'))
                    break
                loopbackstartaddress = str(ipaddress.ip_address(loopbackstartaddress) + 1)
                if loopbackstartaddress == '127.255.255.254':
                    click.ClickException(click.style("No Ip address available in the 127.0.0.0/8 IPV4 Range",
                                                     fg='red',bold=True))





            #Edit Toml file
            click.echo(click.style('Preparing dnscrypt-proxy.toml file',fg='yellow'))


            # Remove all Comments from Log files
            run(r'perl -i -p -e "s/#(?=.*log.*\')//g" example-dnscrypt-proxy.toml')

            run(r"sed -i 's|\['\''127\.0\.0\.1:53'\'', '\''\[::1\]:53'\''\]|\[\]|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''dnscrypt-proxy\.log'\''|'\''/var/log/dnscrypt-proxy/dnscrypt-proxy\.log'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''forwarding-rules\.txt'\''|'\''/etc/dnscrypt-proxy/forwarding-rules\.txt'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''cloaking-rules\.txt'\''|'\''/etc/dnscrypt-proxy/cloaking-rules\.txt'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''query\.log'\''|'\''/var/log/dnscrypt-proxy/query\.log'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''nx\.log'\''|'\''/var/log/dnscrypt-proxy/nx\.log'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''blacklist\.txt'\''|'\''/etc/dnscrypt-proxy/blacklist\.txt'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''blocked\.log'\''|'\''/var/log/dnscrypt-proxy/blocked\.log'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''ip-blacklist\.txt'\''|'\''/etc/dnscrypt-proxy/ip-blacklist\.txt'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''ip-blocked\.log'\''|'\''/var/log/dnscrypt-proxy/ip-blocked\.log'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''public-resolvers\.md'\''|'\''/var/cache/dnscrypt-proxy/public-resolvers\.md'\''|g' example-dnscrypt-proxy.toml")
            run(r"sed -i 's|'\''parental-control\.md'\''|'\''/var/cache/dnscrypt-proxy/parental-control\.md'\''|g' example-dnscrypt-proxy.toml")



            # Create Service Unit and Install Files
            click.echo(click.style('Creating dnscrypt-proxy.service',fg='yellow'))
            click.echo(click.style('Creating dnscrypt-proxy.socket',fg='yellow'))
            click.echo(click.style('Installing Dns Crypt Proxy 2',fg='yellow'))

            fabappend('dnscrypt-proxy.service', DnsCryptService)
            sudo('install -Dm755 "dnscrypt-proxy" "/usr/bin/dnscrypt-proxy"')
            sudo('install -Dm644 "example-dnscrypt-proxy.toml" "/etc/dnscrypt-proxy/dnscrypt-proxy.toml"')
            sudo('install -Dm644 "example-forwarding-rules.txt" "/usr/share/doc/dnscrypt-proxy/example-forwarding-rules.txt"')
            sudo('install -Dm644 "example-blacklist.txt" "/usr/share/doc/dnscrypt-proxy/example-blacklist.txt"')
            sudo('install -Dm644 "example-cloaking-rules.txt" "/usr/share/doc/dnscrypt-proxy/example-cloaking-rules.txt"')
            sudo('install -Dm644 "dnscrypt-proxy.service" "/etc/systemd/system/dnscrypt-proxy.service"')
            sudo('install -Dm644 "dnscrypt-proxy.socket" "/etc/systemd/system/dnscrypt-proxy.socket"')
            sudo('install -Dm644 "LICENSE" "/usr/share/licenses/dnscrypt-proxy/LICENSE"')
            sudo('install -dm777 /var/log/dnscrypt-proxy')
            sudo(r'cat /etc/dnscrypt-proxy/dnscrypt-proxy.toml | grep -oP "(?=\/).*\.log" | xargs -I \% bash -c "sudo touch \%; sudo chmod 766 \%"')



            # Enable and Start the DNS Proxy
            click.echo(click.style('Enabling and Starting dnscrypt-proxy.socket and dnscrypt-proxy.service',
                                   fg='yellow'))

            sudo("systemctl enable dnscrypt-proxy.socket")
            sudo("systemctl enable dnscrypt-proxy.service")
            sudo("systemctl start dnscrypt-proxy.socket")
            sudo("systemctl start dnscrypt-proxy.service")


        return ListenAddress




    def CommandChangeDnsMasq(self):
        """
        Updates the DnsMasq Configs with the New Proxies and Restarts it

        :return: None
        """


        ListenAddress = FabricCommandClass.CommandChangeDnsMasq.ListenAddress
        host = FabricCommandClass.CommandChangeDnsMasq.host

        #Extract Loopback Address
        ListenAddress = ListenAddress[host]


        #Creating DNS Crypt Proxy 2 dnsmasq config.

        click.echo(click.style('Creating DNS Crypt Proxy 2 dnsmasq config',
                               fg='yellow'))
        with cd("/etc/dnsmasq.d"):
            sudo("rm -f 02-dnscrypt.conf")
            fabappend('02-dnscrypt.conf', DnsCryptConf.format("server=" + ListenAddress + "#41"),use_sudo=True)




        # Comment out the Old Config and create a backup copy of the old config
        click.echo(click.style('Creating Backup copy of the orignal PiHole config and commented out the old DNS servers',
                               fg='yellow'))
        comment('/etc/dnsmasq.d/01-pihole.conf', r'^server=.*', use_sudo=True, backup='.old')
        comment('/etc/pihole/setupVars.conf', r'^PIHOLE_DNS.*',use_sudo=True,backup='.old')





        # Moving Restore files due to conflict with dnsmasq service
        click.echo(click.style('Moving PiHole backup config to /home/{0}/.piHoleRestore/'.format(env.user),
                               fg='yellow'))
        run("mkdir -p /home/{0}/.piHoleRestore".format(env.user))
        sudo("mv /etc/pihole/setupVars.conf.old /home/{0}/.piHoleRestore/.".format(env.user))
        sudo("mv /etc/dnsmasq.d/01-pihole.conf.old /home/{0}/.piHoleRestore/.".format(env.user))

        sudo("sed -i 's/.*dnscrypt.*//g' /etc/hosts")
        #for name,address in zip(dnscryptresolvernames,ListenAddress):
        #    sudo("sh -c 'echo \"{0}\t{1} \" >> /etc/hosts'".format(address,name + "-dnscrypt"))



        click.echo(click.style('Restarting dnsmasq service',
                               fg='yellow'))
        sudo("service dnsmasq restart")

        click.echo(click.style('DnsCrypt-Proxy 2 located at located at /var/log/dnscrypt-proxy/ ', fg='green', bold=True))
        click.echo(click.style('DnsCrypt-Proxy 2 config located at /etc/dnscrypt-proxy/dnscrypt-proxy.toml ', fg='green', bold=True))
        click.echo(click.style('DnsCrypt-Proxy 2 install is Complete', fg='green', bold=True))



    def CommandUninstall(self):
        """
        Uninstall the DNS Crypt Proxy 2 that was install by this python client,
        Restores the Files of the orignal PI Hole Config,
        then restarts the DNS


        :return: None
        """
        returnCode = run("which dnscrypt-proxy")
        if(returnCode.succeeded):
            click.echo(click.style('Uninstalling DnsCrypt-Proxy 2....', fg='yellow'))
            sudo("systemctl stop dnscrypt-proxy*")
            sudo("systemctl disable dnscrypt-proxy*")
            sudo("rm /etc/systemd/system/multi-user.target.wants/dnscrypt-proxy*")
            sudo("rm /etc/systemd/system/sockets.target.wants/dnscrypt-proxy*")
            sudo("rm -f /etc/systemd/system/timers.target.wants/dnscrypt-proxy*")
            sudo("rm -f /etc/systemd/system/dnscrypt-proxy*")
            sudo("rm -f /usr/lib/systemd/system/dnscrypt-proxy*")
            sudo("rm -f /usr/bin/dnscrypt-proxy")
            sudo("rm -Rf /etc/dnscrypt-proxy")
            sudo("rm -Rf /var/log/dnscrypt-proxy")
            sudo("rm -f /usr/share/doc/dnscrypt-proxy/example-forwarding-rules.txt")
            sudo("rm -f /usr/share/doc/dnscrypt-proxy/example-blacklist.txt")
            sudo("rm -f /usr/share/doc/dnscrypt-proxy/example-cloaking-rules.txt")
            sudo("rm -f /usr/share/licenses/dnscrypt-proxy/LICENSE")
            sudo("systemctl daemon-reload")
            sudo("systemctl reset-failed")

            click.echo(click.style("Moving /home/{0}/.piHoleRestore/setupVars.conf.old to /etc/pihole/setupVars.conf".format(env.user),fg='yellow'))
            sudo("mv  /home/{0}/.piHoleRestore/setupVars.conf.old /etc/pihole/setupVars.conf".format(env.user))

            click.echo(click.style("Moving /home/{0}/.piHoleRestore/01-pihole.conf.old to /etc/dnsmasq.d/01-pihole.conf".format(env.user),fg='yellow'))
            sudo("mv  /home/{0}/.piHoleRestore/01-pihole.conf.old /etc/dnsmasq.d/01-pihole.conf".format(env.user))
            sudo("rm -Rf /home/{0}/.piHoleRestore".format(env.user))
            sudo("rm -f /etc/dnsmasq.d/02-dnscrypt.conf")
            sudo("service dnsmasq restart")


            click.echo(click.style('DnsCrypt-Proxy 2 Uninstall is Complete', fg='green', bold=True))
            click.echo(click.style('The Original PiHole Config has been restored', fg='green', bold=True))
            click.echo(click.style('The Dnsmasq Service has been restarted', fg='green', bold=True))
        else:
           raise click.ClickException(click.style("DnsCrypt-Proxy 2 is not installed. Aborting Uninstall",
                                             fg='red', bold=True))




    def CommandCreateCronJob(self):
        """
        Create Cron Job that Restart a Proxy server when it see a message from the
        Dns Crypt Service

        Defaults are every 10 minutes and Look for Message that Contain Error

        :return: None
        """
        cronjobminutes = FabricCommandClass.CommandCreateCronJob.cronjobminutes
        cronjobmessage = FabricCommandClass.CommandCreateCronJob.cronjobmessage


        with cd("/etc/sudoers.d"):
            sudo("rm -f DnsCryptSudoer")
            fabappend('DnsCryptSudoer', DnsCryptSudoer,use_sudo=True)

        with cd("/etc/cron.d"):
            sudo("rm -f dnscryptCron")

        sudo(r"""
        sudo echo "*/{0} * * * * dnscrypt sudo journalctl --since \\"{0} minutes ago\\" -u  dnscrypt-proxy* -o json | \
        jq  '. | select(.MESSAGE | tostring |contains(\\"{1}\\")) | \
        ._SYSTEMD_UNIT' | sort | uniq | grep -Pho '(?<=\\").*(?=\.service)' | \
        xargs -I \% bash -c 'sudo systemctl stop \%.socket;sudo systemctl stop \%.service;sudo systemctl start \%.socket;sudo systemctl start \%.service'" | \
        sudo tee -a /etc/cron.d/dnscryptCron > /dev/null 2>&1
        """.format(cronjobminutes,cronjobmessage))

        print(" DNS crypt Setup Cron Watch Dog has Ran Successfully")











