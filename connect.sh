#!/bin/bash

echo "$VPN_PASSWORD" | sudo openconnect "$VPN_ADDRESS" --background --user="$VPN_USER" --passwd-on-stdin --servercert "$VPN_SERVER_CERT"
sleep 5
curl http://api.ipify.org
