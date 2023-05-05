from machine import Pin
import network
import time
from umqtt.robust import MQTTClient
import sys
led = Pin("LED",Pin.OUT)
led.value(1)
first = Pin(0,Pin.OUT)
second = Pin(1,Pin.OUT)
third = Pin(2,Pin.OUT)
fourth = Pin(3,Pin.OUT)
WIFI_SSID = 'Redmi Note 9 Pro'
WIFI_PASSWORD = '0987654321'

mqtt_client_id = bytes('client_'+'123', 'utf-8') # Just a random client ID

ADAFRUIT_IO_URL = 'io.adafruit.com'  	# Your Adafruit IO credentials
ADAFRUIT_USERNAME = '_slowpoke18'
ADAFRUIT_IO_KEY = 'aio_tdvw90dMqNILPobZh2FShVxik69K'

TOGGLE_FEED_ID = 'robot'

def connect_wifi():# function for connecting your wifi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID,WIFI_PASSWORD)
    if not wifi.isconnected():
        print('connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 15):
            print(15 - timeout)
            timeout = timeout + 1
            time.sleep(1)
    if(wifi.isconnected()):
        print('connected')
    else:
        print('not connected')
        sys.exit()

connect_wifi() # Connecting to WiFi 

client = MQTTClient(client_id=mqtt_client_id,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
try:
    client.connect()				# Connect to MQTT server
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

def cb(topic, msg):
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    recieved_data = str(msg,'utf-8')
    if recieved_data=="backward":
        first.value(1)
        second.value(0)
        third.value(1)
        fourth.value(0)
        time.sleep(1)
    if recieved_data=="forward":
        first.value(0)
        second.value(1)
        third.value(0)
        fourth.value(1)
        time.sleep(1)
    if recieved_data=="right":
        first.value(0)
        second.value(1)
        third.value(1)
        fourth.value(0)
        time.sleep(0.5)
        first.value(0)
        second.value(0)
        third.value(0)
        fourth.value(0)
        time.sleep(1)
    if recieved_data=="left":
        first.value(1)
        second.value(0)
        third.value(0)
        fourth.value(1)
        time.sleep(0.5)
        first.value(0)
        second.value(0)
        third.value(0)
        fourth.value(0)
        time.sleep(1)
    if recieved_data=="stop":
        first.value(0)
        second.value(0)
        third.value(0)
        fourth.value(0)
        time.sleep(1)
    else :
        print("Invalid input.....try again")
        time.sleep(1)

toggle_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID), 'utf-8') # format – usesrname/feeds/led  
client.set_callback(cb)# Callback function               
client.subscribe(toggle_feed) # Subscribing to particular topic

while True:
    try:
        client.check_msg()# non blocking function
    except:
        client.disconnect()
        sys.exit()


