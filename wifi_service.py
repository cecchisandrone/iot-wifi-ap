import json
import time
import atexit
import os
import subprocess
import configparser
from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
config = {}

@atexit.register
def exit():
  print("Terminating...")

# Response example: [{"dbm": -77, "ssid": "dd-wrt"}, {"dbm": -83, "ssid": "Tp-Link"}]
@app.route('/scan', methods=['GET'])
def scan():
  networks = []
  output = subprocess.check_output(["wpa_cli -i wlan0 scan"], stderr=subprocess.STDOUT, shell=True).strip()
  time.sleep(1)
  if output == "OK":
    output = subprocess.check_output(["wpa_cli -i wlan0 scan_results | grep -v P2P | tail -n +2 | cut -f 3,5 | tr '\t' '|'"], stderr=subprocess.STDOUT, shell=True)
    lines = output.splitlines()
    for line in lines:
      arr = line.split('|')
      network = {}
      network["ssid"] = arr[1]
      network["dbm"] = int(arr[0])
      networks.append(network)
  else:
    return 'Unable to scan for wifi networks', 500
  return json.dumps(networks), 200

# Request example: curl -X PUT -H 'Content-Type: application/json' -d '{"ssid":"CECCHI'\''WI-FI","psk":"16071607"}' localhost:6000/connect
@app.route('/connect', methods=['PUT'])
def connect():
  req = request.get_json()
  print("Connecting to network " + req['ssid'] + " with password " + req['psk'])
  network_index = subprocess.check_output(["wpa_cli","-i","wlan0","add_network"], stderr=subprocess.STDOUT, shell=False).strip()
  set_ssid = subprocess.check_output(["wpa_cli","-i","wlan0","set_network",network_index,"ssid","\"" + req["ssid"] + "\""], stderr=subprocess.STDOUT, shell=False).strip()
  set_psk = subprocess.check_output(["wpa_cli","-i","wlan0","set_network",network_index,"psk","\"" + req["psk"] + "\""], stderr=subprocess.STDOUT, shell=False).strip()
  select_network = subprocess.check_output(["wpa_cli -i wlan0 select_network " + network_index], stderr=subprocess.STDOUT, shell=True).strip()
  if set_ssid == "OK" and set_psk == "OK" and select_network == "OK":
    for i in range(5):
      status = subprocess.call(["wpa_cli -i wlan0 status | grep --quiet wpa_state=COMPLETED"], shell=True)
      if status ==  0:
        # Delete old networks
        for j in range(int(network_index)):
          subprocess.check_output(["wpa_cli","-i","wlan0","remove_network",str(j)], stderr=subprocess.STDOUT, shell=False).strip()
        subprocess.check_output(["wpa_cli -i wlan0 save_config"], shell=True)
        return json.dumps({"result":"success"}), 200
      time.sleep(3)
  return json.dumps({"result":"failure"}), 500

# Response example: {"group_cipher": "TKIP", "ssid": "Tp-Link", "bssid": "50:64:2b:2b:36:0e", "p2p_device_address": "aa:e8:af:51:86:c8", "wpa_state": "COMPLETED", "uuid": "ceecde00-5c31-5b88-aa3d-296871497f75", "mode": "station", "address": "b8:27:eb:e0:49:6f", "freq": "2427", "key_mgmt": "WPA2-PSK", "ip_address": "192.168.1.114", "id": "0", "pairwise_cipher": "CCMP"}
@app.route('/wpa-status', methods=['GET'])
def wpa_status():
  dict = {}
  output = subprocess.check_output(["wpa_cli -i wlan0 status"], stderr=subprocess.STDOUT, shell=True)
  lines = output.splitlines()
  for line in lines:
    values = line.split("=")
    dict[values[0]] = values[1]
  return json.dumps(dict), 200

@app.route('/connectivity-status', methods=['GET'])
def connectivity_status():
  output = subprocess.check_output(["curl -sL -o /dev/null -w \"%{http_code}\" " + config['DEFAULT']['CONNECTIVITY_ENDPOINT']], stderr=subprocess.STDOUT, shell=True).strip()
  print(output)
  if output == '200':
    return json.dumps({"result":"success"}), 200
  else:
    return json.dumps({"result":"failure"}), 500

if __name__ == '__main__':
  print("Starting WI-FI service...")
  config = configparser.ConfigParser()
  config.read('wifi_service.cfg')
  app.run(host='0.0.0.0', port=8081)

