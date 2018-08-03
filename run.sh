# Stop wpa_supplicant
systemctl stop wpa_supplicant.service

# Create uap0 interface
iw dev wlan0 interface add uap0 type __ap
ifconfig uap0 192.168.27.1
ifconfig uap0 up

# Enable traffic forwarding
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
iptables -A FORWARD -i wlan0 -o uap0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i uap0 -o wlan0 -j ACCEPT
sysctl net.ipv4.ip_forward=1

# Start hostapd
hostapd hostapd.conf > hostapd.log 2>&1 &

# Start dnsmasq
dnsmasq --no-hosts --keep-in-foreground --log-queries --dhcp-range=192.168.27.100,192.168.27.150,1h --dhcp-vendorclass=set:device,IoT --dhcp-authoritative --log-facility=- --interface=lo,uap0 --server=8.8.8.8 --server=4.4.4.4 --no-dhcp-interface=lo,wlan0 > dnsmasq.log 2>&1 &

# Start wpa_supplicant
wpa_supplicant -Dnl80211 -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant_test.conf > wpa_supplicant.log 2>&1 &
