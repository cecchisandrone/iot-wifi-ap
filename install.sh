apt-get install hostapd dnsmasq avahi-utils iftop

systemctl mask wpa_supplicant.service
systemctl mask dnsmasq.service
systemctl mask hostapd.service

# Disable auto wpa_supplicant start for uap0 
echo -e "interface uap0\n  nohook wpa_supplicant" >> /etc/dhcpd.conf

# Empty file for AP
#cp wpa_supplicant /etc/wpa_supplicant/wpa_supplicant_ap.conf

# Hostapd conf
#cp hostapd.conf /etc/hostapd/hostapd.conf

mkdir /var/log/iot-wifi-ap

cat /etc/rc.local | sed 's#exit 0#sleep 60\n./home/pi/iot-wifi-ap/run.sh\nexit 0#g' > /etc/rc.local
