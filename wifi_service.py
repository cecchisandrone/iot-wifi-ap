import json
import time
import atexit
import os
import subprocess
from flask import Flask
from flask import request

app = Flask(__name__)

@atexit.register
def exit():
  print("Exited")

# Response example: {"Tp-Link": -87, "dd-wrt": -83, "CECCHI'S WIFI": -71}
@app.route('/scan', methods=['GET'])
def scan():
  networks = {}
  output = subprocess.check_output(["wpa_cli -i wlan0 scan"], stderr=subprocess.STDOUT, shell=True).strip()
  time.sleep(1)
  if output == "OK":
    output = subprocess.check_output(["wpa_cli -i wlan0 scan_results | grep -v P2P | tail -n +2 | cut -f 3,5 | tr '\t' '|'"], stderr=subprocess.STDOUT, shell=True)
    lines = output.splitlines()
    for line in lines:
      arr = line.split('|')
      networks[arr[1]] = int(arr[0])
  else:
    return 'Unable to scan for wifi networks', 500
  return json.dumps(networks), 200

# Request example: curl -X PUT -H 'Content-Type: application/json' -d '{"ssid":"Cecchi WI-FI","psk":"16071607"}' localhost:6000/connect
@app.route('/connect', methods=['PUT'])
def connect():
  req = request.get_json()
  print(req['ssid'])
  print(req['psk'])
  output = subprocess.check_output(["wpa_cli -i wlan0 scan"], stderr=subprocess.STDOUT, shell=True).strip()
  return 'ok',200

# Response example: {"group_cipher": "TKIP", "ssid": "Tp-Link", "bssid": "50:64:2b:2b:36:0e", "p2p_device_address": "aa:e8:af:51:86:c8", "wpa_state": "COMPLETED", "uuid": "ceecde00-5c31-5b88-aa3d-296871497f75", "mode": "station", "address": "b8:27:eb:e0:49:6f", "freq": "2427", "key_mgmt": "WPA2-PSK", "ip_address": "192.168.1.114", "id": "0", "pairwise_cipher": "CCMP"}
@app.route('/status', methods=['GET'])
def status():
  dict = {}
  output = subprocess.check_output(["wpa_cli -i wlan0 status"], stderr=subprocess.STDOUT, shell=True)
  lines = output.splitlines()
  for line in lines:
    values = line.split("=")
    dict[values[0]] = values[1]
  return json.dumps(dict), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=6000)

