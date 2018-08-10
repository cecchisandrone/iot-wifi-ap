apt-get install hostapd dnsmasq avahi-utils iftop python-pip

pip install -r requirements.txt

# Disable auto wpa_supplicant start for uap0 in dhcpd
echo -e "interface uap0\n  nohook wpa_supplicant" >> /etc/dhcpd.conf

# Disable ipv6 and set interface for avahi
sed -i /etc/avahi/avahi-daemon.conf -e 's/use-ipv6=yes/use-ipv6=no/g'
sed -i /etc/avahi/avahi-daemon.conf -e 's/#allow-interfaces=eth0/allow-interfaces=uap0/g'

systemctl restart dhcpd.service
systemctl mask wpa_supplicant.service
systemctl mask dnsmasq.service
systemctl mask hostapd.service

# Logs dir
mkdir -p /var/log/iot-wifi-ap

# Startup
sed -i /etc/rc.local -e 's#^exit 0#./home/pi/iot-wifi-ap/run.sh\nexit 0#g'
mv wifi_service.cfg.example wifi_service.cfg
