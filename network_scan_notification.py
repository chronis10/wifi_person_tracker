import sys
import subprocess 
import os
from decouple import config
from datetime import datetime
import time
import json
current_day = []

IP_NETWORK = config('IP_NETWORK')
IP_DEVICES = json.loads(config('IP_DEVICES'))
SCAN_DELAY = int(config('SCAN_DELAY'))
TELEGRAM_ID =config('TELEGRAM_ID')
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

def write_log(msg):
  f = open(config('LOG_FILE'), "a")
  f.write(msg + '\n')
  f.close()

def send_notification(msg):
  packet = ['curl','-X','POST','-H','Content-Type: application/json','-d',
            '{"chat_id":"'+ TELEGRAM_ID+'", "text":"'+ msg+'", "disable_notification": "true"}',
            'https://api.telegram.org/bot'+TELEGRAM_TOKEN+'/sendMessage']
  proc = subprocess.Popen( packet, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

def day_check(s_person):
  found = False
  if len(current_day)>0:    
    for person in current_day:
      if person['name'] == s_person['name']:
        found = True
        break
  if not found:
    current_day.append(s_person)
    name = s_person['name']
    dtime = s_person['datetime']
    send_notification(f'{name}, arrived in office. {dtime}')


if __name__ == '__main__':
  try:
    current_date = datetime.now().day
    while True: 
      if current_date !=  datetime.now().day:
        current_date = datetime.now().day
        current_day = []        
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
            day_check({'name':items['name'],'datetime':datetime.now()})
            write_log(msg)
            #print(msg)
      #print(current_day)
      print('Working...')     
      time.sleep(SCAN_DELAY)
  except KeyboardInterrupt:
    print('Script terminated!')
  except Exception as e:
    print(f'Error:\n{e}')
