import json
import time
import atexit
import os
import subprocess
from flask import Flask

app = Flask(__name__)

@atexit.register
def exit():
  print("Exited")

@app.route('/scan', methods=['GET'])
def scan():
  dict = {}
  output = subprocess.check_output(["/sbin/wpa_cli -i wlan0 status"], stderr=subprocess.STDOUT, shell=True)
  lines = output.splitlines()
  for line in lines:
    values = line.split("=")
    dict[values[0]] = values[1]
  return json.dumps(dict), 200

@app.route('/connect', methods=['PUT'])
def connect():
  return 'ok',200

@app.route('/status', methods=['GET'])
def status():
  return 'ok',200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=6000)

