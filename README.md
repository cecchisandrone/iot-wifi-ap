# Wireless access point scripts for Raspberry PI (Debian Stretch)
These scripts allow a Raspberry to work as Wi-Fi Access Point with internet connection. 
A set of HTTP APIs are exposed to permit the development of a UI to select which Wi-Fi for internet access.
The main purpose of this project is to give the right isolation to the devices of an IoT network, while giving them the possibility of accessing the outside network.

## Installation & configuration

1. Install Debian Stretch on SD card and login your PI
2. Clone this repo `git clone https://github.com/cecchisandrone/iot-wifi-ap.git` in `/home/pi`
3. Run `sudo install.sh`
4. Edit file `hostapd.conf` to change Wi-Fi preferences (ssid, psk, channel and others)
5. Edit file `wifi_service.cfg` to change wifi service preferences
6. Reboot your PI

## First run
At boot, `run.sh` is executed and the following steps are done:
1. Create AP interface and enable packets forwarding
2. Start `hostapd`
3. Start `dnsmasq`
4. Start `wpa_supplicant`
5. Start `wifi_service` python script to expose APIs (running on port 6000)

At this point the AP network is created, with the parameters defined into `hostapd.conf`. 
You need to call the HTTP APIs to choose which network to join.

## API
The following endpoints are available (Raspberry Pi IP is 192.168.27.1:6000):

- GET /scan - Returns a list of available Wi-Fi networks with signal quality. For example: 
````
[
  {
    "ssid" : "Tp-Link",
    "dbm" : -45
  },
  {
    "ssid" : "My Wifi",
    "ssid" : -76
  } 
]

````
- GET /wpa-status - Returns the wpa_supplicant status. For example:
````
{
  "group_cipher": "CCMP", 
  "ssid": "Tp-Link", 
  "bssid": "ec:08:6b:b5:5e:14", 
  "p2p_device_address": "16:14:48:e2:8f:2d", 
  "wpa_state": "COMPLETED", 
  "uuid": "ceecde00-5c31-5b88-aa3d-296871497f75", 
  "mode": "station", 
  "address": "b8:27:eb:e0:49:6f", 
  "freq": "2427", 
  "key_mgmt": "WPA2-PSK", 
  "ip_address": "192.168.1.114", 
  "id": "0", 
  "pairwise_cipher": "CCMP"
}
````
- GET /connectivity-status - Returns 200 if there is connectivity with CONNECTIVITY_ENDPOINT, 500 otherwise. Useful to check internet connectivity
- PUT /connect - Joins a network with ssid and password, using the following JSON body:
````
{
  "ssid" : "network_ssid",
  "psk" : "network_psk"
}

````

## Logs
You can find logs into folder /var/log/iot-wifi-ap

