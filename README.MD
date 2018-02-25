# DnsCryptPiHoleSetup


DnsCryptPiHoleSetup is a command line tool to set up Dnscrypt Proxies on PiHole for Raspberry Pi 3.

This tool is meant to be a all in one solution to manage and build your DNS proxies. If you do not like a setup you have configured you can rerun the tool to install new Dns Crypt proxies with no repercussions.

#### Support for 3.2 Pihole only until Bugs are fixed
https://pi-hole.net/2018/02/14/pi-hole-v3-3-released-its-extra-special/
https://discourse.pi-hole.net/t/how-do-i-revert-to-a-previous-version-of-pi-hole/7168
 



## Features

- Installs Dnscrypt software if it doesnt existing.
- Builds Socket and Service Files for your DNS Crypt based on the resolvers name. 
- Edits the PiHole Configuration and restarts the DnsMasq Service.
- Monitors DnsCrypt Proxies and restarts the individual proxy that has shown a error in the last 10 minutes by default.

![ScreenShot](img/PiHoleMainWindow.png)




## Getting Started
#### SSH to your PI Hole

`sudo apt-get install python3-pip`
###### Note: if you do not use Sudo it will install to the `/home/{username}/.local/bin` which is not available by a path in Raspbian Strech by default. Sudo will install the command in `/usr/local/bin/dnscrypt-proxy-pi-tool`. This make it globally available.
`sudo pip3 install DnsCryptProxyPiTool`


#### Find your Proxy of choice

[Default Proxy List can be found here]( https://github.com/dyne/dnscrypt-proxy/blob/master/dnscrypt-resolvers.csv)


### Run the command
###### note: this will setup d0wn-random-ns1 and d0wn-random-ns2 by default which randomized each querie across 18 different servers.

`DnsCryptPiHoleSetup`

From here you will see a bunch of output from linux commands so you can track what is going on.

When it is finish you will see `DNS crypt Setup has Ran Successfully`


#### It best to flush your logs after running this so it accurate remove old information in the pi hole GUI

![ScreenShot](img/FlushLogs.png)


### Test your configuration
#### Note: this output is from the default setup

[DnsLeakTest](https://www.dnsleaktest.com/)

![ScreenShot](img/DnsLeakTest.png)



### Get Stuck? Use Show the help menu

![ScreenShot](img/DnsCryptPiHoleHelpMenu.png)


#### Example of the default config with command options

` DnsCryptPiHoleSetup -h '127.0.0.1' -u 'pi' -p 'raspberry' -e '/tmp' \
 -d 'https://launchpad.net/ubuntu/+archive/primary/+files/dnscrypt-proxy_1.9.5.orig.tar.gz' \
 -r '/usr/local/share/dnscrypt-proxy' -n "['d0wn-random-ns1','d0wn-random-ns2']" \
 -l '127.10.10.1' -t '10' -m 'ERROR' `

#### Show Status

` sudo systemctl status -l dnscrypt-proxy@\* `



 
#### If you wish to override Default, the Default config is found here:

` /usr/local/lib/{Python Version}/dist-packages/DnsCryptPiHoleSetup/DefaultConfig.py`

[View Default Config On Repo Here](DnsCryptProxyPiTool/DefaultConfig.py)


