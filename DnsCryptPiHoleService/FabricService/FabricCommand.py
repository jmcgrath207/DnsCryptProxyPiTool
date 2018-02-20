from fabric.api import sudo, cd, run, open_shell
from fabric.contrib.files import append as fabappend, comment
from fabric.context_managers import env, output
import re
import ipaddress
import click
from DnsCryptPiHoleService.FabricService.StringContainer import DnsCryptService, DnsCryptSocket,\
    DnsCryptConf, DnsCryptSudoer




class FabricCommandClass(object):



    def CommandFabric3OpenShellMonkeyPatch(self):
        # Reported on fixed https://github.com/fabric/fabric/issues/1719
        # Root Cause is https://github.com/fabric/fabric/issues/196 will be fixed in Fabric V2

        click.echo(
            click.style('Applying Fabric Monkey Patch for OpenShell Command', fg='yellow'))


        libInstallPath = run('pip3 show fabric3 | grep -Po "(?<=Location:\s).*"')
        location = re.sub(r'.*\r\n', "", libInstallPath.stdout) + "/fabric"
        locationIopy = location + "/io.py"
        sudo(command="cp " + locationIopy + " " + location + "/io_old.py", user=env.user)
        sudo(command=r'perl -i -p -e "s/import sys/import os\nimport sys/g" ' + locationIopy,user=env.user)
        sudo(command=r'perl -i -p -e "s/sys.stdin.read\(1\)/os.read(sys.stdin.fileno(), 1)/g" '+ locationIopy,user=env.user)




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

            # install Logs setup to log to /var/log/dnscrypt-proxy
            # Remove all Comments from Log files
            # Currently disabled since the same logs are provide through systemd
            #run(r'perl -i -p -e "s/#(?=.*log.*\')//g" example-dnscrypt-proxy.toml')

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

            # install Logs setup to log to /var/log/dnscrypt-proxy
            # Currently disabled since the same logs are provide through systemd
            #sudo('install -dm777 /var/log/dnscrypt-proxy')
            #sudo(r'cat /etc/dnscrypt-proxy/dnscrypt-proxy.toml | grep -oP "(?=\/).*\.log" | xargs -I \% bash -c "sudo touch \%; sudo chmod 766 \%"')



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
        dnscryptexractdir = FabricCommandClass.CommandChangeDnsMasq.dnscryptexractdir

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


        click.echo(click.style('Removed Build Directory at {0}/dnscryptBuild/'.format(dnscryptexractdir),
                               fg='yellow'))

        sudo('rm -Rf {0}/dnscrypt*'.format(dnscryptexractdir))

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
            sudo("apt-get purge -y dnscrypt-proxy")
            sudo("dpkg --purge --force dnscrypt-proxy")
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

            click.echo(click.style("Removing Fabric Monkey Patch for OpenShell Command",fg='yellow'))
            libInstallPath = run('pip3 show fabric3 | grep -Po "(?<=Location:\s).*"')
            location = re.sub(r'.*\r\n', "", libInstallPath.stdout) + "/fabric"
            locationIopy = location + "/io.py"
            sudo(command="mv " + location + "/io_old.py" + " " + locationIopy, user=env.user)
            sudo(command="rm -f " + location + "/io_old.py", user=env.user)

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



    def CommandShowDnsCryptProxyConfig(self):
        click.echo(click.style('/etc/dnscrypt-proxy/dnscrypt-proxy.toml', fg='green',bold=True))



    def CommandEditDnsCryptProxyConfig(self):
        editor = FabricCommandClass.CommandEditDnsCryptProxyConfig.editor
        open_shell(command= editor + ' /etc/dnscrypt-proxy/dnscrypt-proxy.toml; exit')




    def CommandShowDnsCryptPiHoleSetupConfig(self):
        libInstallPath = run('pip3 show fabric3 | grep -Po "(?<=Location:\s).*"')
        location = re.sub(r'.*\r\n', "", libInstallPath.stdout)
        click.echo(click.style(location, fg='green',bold=True))



    def CommandEditDnsCryptPiHoleSetupConfig(self):
        editor = FabricCommandClass.CommandShowDnsCryptPiHoleSetupConfig.editor
        open_shell(command= editor + ' /home/pi/.piHoleRestore/01-pihole.conf.old; exit')


    def CommandRestartConfig(self):

        sudo("systemctl stop dnscrypt-proxy.service")
        sudo("systemctl stop dnscrypt-proxy.socket")
        sudo("service dnsmasq stop")


        sudo("systemctl start dnscrypt-proxy.socket")
        sudo("systemctl start dnscrypt-proxy.service")
        sudo("service dnsmasq start")









