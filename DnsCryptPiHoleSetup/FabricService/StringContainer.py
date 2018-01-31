

DnsCryptSocket = """
[Unit]
Description=dnscrypt-proxy listening socket

[Socket]
ListenStream={0}:41
ListenDatagram={0}:41

[Install]
WantedBy=sockets.target
"""


DnsCryptService = """
[Unit]
Description=DNSCrypt client proxy
Documentation=man:dnscrypt-proxy(8)
Requires=dnscrypt-proxy@%i.socket
After=network.target
Before=nss-lookup.target

[Install]
Also=dnscrypt-proxy@%i.socket
WantedBy=multi-user.target

[Service]
Type=simple
NonBlocking=true

# Fill in the resolver name with one from dnscrypt-resolvers.csv file
# It is also recommended to create a dedicated system user, for example _dnscrypt
# Additional features, such as ephemeral keys and plugins, can be enabled here as well
ExecStart=/usr/local/sbin/dnscrypt-proxy \
        --resolver-name=%i \
        --user=dnscrypt 

Restart=always
RestartSec=10
"""

DnsCryptServiceEphemeral = """
[Unit]
Description=DNSCrypt client proxy
Documentation=man:dnscrypt-proxy(8)
Requires=dnscrypt-proxy@%i.socket
After=network.target
Before=nss-lookup.target

[Install]
Also=dnscrypt-proxy@%i.socket
WantedBy=multi-user.target

[Service]
Type=simple
NonBlocking=true

# Fill in the resolver name with one from dnscrypt-resolvers.csv file
# It is also recommended to create a dedicated system user, for example _dnscrypt
# Additional features, such as ephemeral keys and plugins, can be enabled here as well
ExecStart=/usr/local/sbin/dnscrypt-proxy \
        --resolver-name=%i \
        --ephemeral-keys \
        --user=dnscrypt

Restart=always
RestartSec=10
"""


DnsCryptConf = """
# Add other name servers here, with domain specs if they are for
# non-public domains.
{0}
"""


DnsCryptSudoer = """


%dnscrypt ALL= NOPASSWD: /bin/systemctl start dnscrypt-proxy@*
%dnscrypt ALL= NOPASSWD: /bin/systemctl stop dnscrypt-proxy@*
%dnscrypt ALL= NOPASSWD: /bin/systemctl status dnscrypt-proxy@*
%dnscrypt ALL= NOPASSWD: /bin/systemctl restart dnscrypt-proxy@*
%dnscrypt ALL= NOPASSWD: /bin/journalctl --since*-u  dnscrypt-proxy@* 

"""