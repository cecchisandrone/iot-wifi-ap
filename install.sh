apt-get install hostapd dnsmasq avahi-utils iftop

# Disable auto wpa_supplicant start for uap0 
echo -e "interface uap0\n  nohook wpa_supplicant" >> /etc/dhcpd.conf

# Empty file for AP
cp wpa_supplicant /etc/wpa_supplicant/wpa_supplicant_ap.conf

echo -e "sleep 60\n./home/pi/iot-wifi-ap/run.sh"
