#!/usr/bin/env bash

## Cron Job to Restart the DNS crypt Proxies
journalctl --since "10 minutes ago" -u  dnscrypt-proxy* -o json | jq  '. | select(.MESSAGE | tostring |contains("ERROR")) | ._SYSTEMD_UNIT' | sort | uniq | grep -Pho '(?<=\").*(?=\.service)' | xargs -I % bash -c 'sudo systemctl stop %.socket;sudo systemctl stop %.service;sudo systemctl start %.socket;sudo systemctl start %.service'



# Remove Commands From all Log Files in Toml cofnig
sudo perl -i -p -e "s/#.(?=.*log.*\')//g" /etc/dnscrypt-proxy/dnscrypt-proxy.toml


# Creating Log files based on Toml config

sudo cat toml-example | grep -oP "(?=\/).*\.log" | xargs -I \% bash -c "sudo touch \%; sudo chmod 766 \%"

## Path of Command
cd /home/pi/.local/bin/
