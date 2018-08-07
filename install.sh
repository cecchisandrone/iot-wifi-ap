apt-get install hostapd dnsmasq avahi-utils iftop python-pip

pip install -r requirements.txt

systemctl mask wpa_supplicant.service
systemctl mask dnsmasq.service
systemctl mask hostapd.service

# Disable auto wpa_supplicant start for uap0
echo -e "interface uap0\n  nohook wpa_supplicant" >> /etc/dhcpd.conf

systemctl restart dhcpd.service

mkdir -p /var/log/iot-wifi-ap

sed -i /etc/rc.local -e 's#^exit 0#./home/pi/iot-wifi-ap/run.sh\nexit 0#g'
mv wifi_service.cfg.example wifi_service.cfg
