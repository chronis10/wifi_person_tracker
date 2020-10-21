# Wifi Person tracker

#### Log persons to file

```network_scan.py```

That script logs the persons of interest with the datetime to the ```wifi_logs.txt``` file.

#### Log persons to file and Telegram notification

```network_scan_notification.py```

That script logs the persons of interest with the datetime to the ```wifi_logs.txt``` file and the same time sends a notification to admin. The script sends one message per day (the first appearance of a person on the network).

#### Settings file

Create a ```settings.ini``` file with the following content.

```
[settings]
IP_DEVICES=[{"name":"User1","ip":"192.168.0.110"}]
IP_NETWORK = 192.168.0.1/24
LOG_FILE = wifi_logs.txt
SCAN_DELAY = 60
TELEGRAM_TOKEN = telegram_bot_token
TELEGRAM_ID = telegram_user_id

```