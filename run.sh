#!/bin/bash

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Set working directory
cd "$(dirname "$0")"

# Stop running services
systemctl stop wpa_supplicant.service
systemctl stop dnsmasq
systemctl stop hostapd
pkill wpa_supplicant
pkill dnsmasq
pkill hostapd
pkill -f wifi_service

# Create uap0 interface
iw dev uap0 del
iw dev wlan0 interface add uap0 type __ap
ifconfig uap0 192.168.27.1
ifconfig uap0 up

# Enable traffic forwarding
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
iptables -A FORWARD -i wlan0 -o uap0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i uap0 -o wlan0 -j ACCEPT
sysctl -q net.ipv4.ip_forward=1

# Start hostapd
hostapd hostapd.conf > /var/log/iot-wifi-ap/hostapd.log 2>&1 &

sleep 3

# Start dnsmasq
dnsmasq --no-hosts --keep-in-foreground --log-queries --dhcp-range=192.168.27.100,192.168.27.150,1h --dhcp-vendorclass=set:device,IoT --dhcp-authoritative --log-facility=- --interface=lo,uap0 --server=8.8.8.8 --server=4.4.4.4 --no-dhcp-interface=lo,wlan0 > /var/log/iot-wifi-ap/dnsmasq.log 2>&1 &

sleep 3

# Start wpa_supplicant
wpa_supplicant -D nl80211 -i wlan0 -c wpa_supplicant_ap.conf > /var/log/iot-wifi-ap/wpa_supplicant.log 2>&1 &

# Start wifi service
python wifi_service.py > /var/log/iot-wifi-ap/wifi_service.log 2>&1 &

