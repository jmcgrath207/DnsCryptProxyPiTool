





# SETUP


### SSH to your Pi Hole DNS Server

#### Install the dnscrypt-proxy-pi-tool

###### Note: if you do not use Sudo it will install to the `/home/{username}/.local/bin` which is not available by  path in Raspbian Strech by default. Sudo will install the command in `/usr/local/bin/dnscrypt-proxy-pi-tool`. This make it globally available.
`sudo pip3 install DnsCryptProxyPiTool`


#### Command Line Usage

The dnscrypt-proxy-pi-tool runs by default parameters in a file that be found by showing the path with `dnscrypt-proxy-pi-tool admin -x`.
 
You can also launch the editor with `dnscrypt-proxy-pi-tool admin -x`

[View Default Config On Repo Here](DnsCryptProxyPiTool/DefaultConfig.py)


All default parameters can be overridden with command line arguments if you need to run it one time only.


#### Command Line Help

If you get stuck there is a help context for each command
ex.
`dnscrypt-proxy-pi-tool --help`
`dnscrypt-proxy-pi-tool admin --help`



## INSTALL DnsCrypt Proxy 2


#### For Users that installed the DnsCryptProxyPiHole Setup.

Back up your PiHole Block and White List Configs via web gui.

execute `pihole -r` and do the reconfigure Option.

Then run `dnscrypt-proxy-pi-tool uninstall`. This will uninstall all installation of dnscrypt-proxy new and old.

From here continue to follow the normal  directions.


### Run the command

install Dns Crypt Proxy 2

`dnscrypt-proxy-pi-tool install`

Verbose mode to show the linux commands that are being executed against your server

`dnscrypt-proxy-pi-tool -v install`

Want to override the default config for install?

`dnscrypt-proxy-pi-tool -u 'potato' -p 'salad' install -e '/tmp/something'`

After that the install is complete

#### Show Status

Make sure the Dns Crypt Proxy 2 Service and Socket are running correctly.

` sudo systemctl status -l dnscrypt-proxy.* `

##### It best to flush your logs after running this so it accurately removes old logs in the pi hole GUI

![ScreenShot](img/FlushLogs.png)


### Test your configuration
#### Note: this output is from the default setup

[DnsLeakTest](https://www.dnsleaktest.com/)

If you see something Like this it is working.

![ScreenShot](img/DnsLeakTest.png)


# Edit DnsCrypt Proxy 2 Config

The Dns Crypt Proxy 2 run  by default parameters in a file that be found by showing the path with `dnscrypt-proxy-pi-tool admin -z`.
 
 You can also launch the editor with `dnscrypt-proxy-pi-tool admin -y`


# Upgrade

Want to upgrade to the Newest DnsCrypt Proxy 2 release? Just do this.
##### Note this will restart you DnsMasq Service.

`dnscrypt-proxy-pi-tool admin -q`

# Uninstall

Remove Dnscrypt Proxy 2 and Restore Old Pi Hole config.

`dnscrypt-proxy-pi-tool uninstall`









