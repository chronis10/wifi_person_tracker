import sys
import subprocess 
import os
from decouple import config
from datetime import datetime
import time
import json

IP_NETWORK = config('IP_NETWORK')
IP_DEVICES = json.loads(config('IP_DEVICES'))
SCAN_DELAY = config('SCAN_DELAY')

def write_log(msg):
  f = open(config('LOG_FILE'), "a")
  f.write(msg + '\n')
  f.close()


if __name__ == '__main__':
  try:
    while True:
      proc = subprocess.Popen(('fping','-g' , IP_NETWORK), stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
      while True:        
        line = proc.stdout.readline()
        if not line:
          break
        status = line.decode('utf-8').split(' ')[-1].strip()
        current_ip= line.decode('utf-8').split(' ')[0].strip()
        for items in IP_DEVICES:      
          if status == 'alive' and  current_ip == items['ip']:
            msg = f"{datetime.now()} {items['name']} detected to the network"
            write_log(msg)
            print(msg)
      time.sleep(SCAN_DELAY)
  except KeyboardInterrupt:
    print('Script terminated!')
  except Exception as e:
    print(f'Error:\n{e}')
