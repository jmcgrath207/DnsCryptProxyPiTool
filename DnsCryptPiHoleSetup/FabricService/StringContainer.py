

DnsCryptSocket = """
Description=dnscrypt-proxy listening socket
Documentation=https://github.com/jedisct1/dnscrypt-proxy/wiki
Before=nss-lookup.target
Wants=nss-lookup.target

[Socket]
ListenStream={0}:41
ListenDatagram={0}:41

[Install]
WantedBy=sockets.target
"""


DnsCryptService = """
Description=DNSCrypt client proxy
Documentation=https://github.com/jedisct1/dnscrypt-proxy/wiki
Requires=dnscrypt-proxy.socket
After=network.target
Before=nss-lookup.target
Wants=nss-lookup.target

[Service]
Type=simple
NonBlocking=true
ExecStart=/usr/bin/dnscrypt-proxy --config /etc/dnscrypt-proxy/dnscrypt-proxy.toml
DynamicUser=yes

[Install]
WantedBy=multi-user.target
"""



DnsCryptServiceSysmd235 = """
Description=DNSCrypt client proxy
Documentation=https://github.com/jedisct1/dnscrypt-proxy/wiki
Requires=dnscrypt-proxy.socket
After=network.target
Before=nss-lookup.target
Wants=nss-lookup.target

[Service]
Type=simple
NonBlocking=true
ExecStart=/usr/bin/dnscrypt-proxy --config /etc/dnscrypt-proxy/dnscrypt-proxy.toml
DynamicUser=yes
ProtectHome=true
CacheDirectory=dnscrypt-proxy
LogsDirectory=dnscrypt-proxy

[Install]
WantedBy=multi-user.target
"""


DnsCryptConf = """
# Add other name servers here, with domain specs if they are for
# non-public domains.
{0}
"""


DnsCryptSudoer = """

%dnscrypt ALL= NOPASSWD: /usr/bin/dnscrypt-proxy dnscrypt-proxy*
%dnscrypt ALL= NOPASSWD: /bin/systemctl start dnscrypt-proxy*
%dnscrypt ALL= NOPASSWD: /bin/systemctl stop dnscrypt-proxy*
%dnscrypt ALL= NOPASSWD: /bin/systemctl status dnscrypt-proxy*
%dnscrypt ALL= NOPASSWD: /bin/systemctl restart dnscrypt-proxy*
%dnscrypt ALL= NOPASSWD: /bin/journalctl --since*-u  dnscrypt-proxy* 

"""