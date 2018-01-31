
sudo apt-get install python3-pip




	
If you are running pip3 install --editable . it will install to the command to /home/{username}/.local/bin. If you run sudo pip3 install --editable . it will install the command to /usr/local/bin/




DnsCryptPiHoleSetup -h '127.0.0.1' -u 'pi' -p 'raspberry' -e '/tmp' \
 -d 'https://launchpad.net/ubuntu/+archive/primary/+files/dnscrypt-proxy_1.9.5.orig.tar.gz' \
 -r '/usr/local/share/dnscrypt-proxy' -n "['d0wn-random-ns1','d0wn-random-ns2']" \
 -l '127.10.10.1' -t '10' -m 'ERROR'
 
 
 It best to Flush you logs after running this
 
 
 # Default
 /usr/local/lib/python3.5/dist-packages/DnsCryptPiHoleSetup/DefaultConfig.py