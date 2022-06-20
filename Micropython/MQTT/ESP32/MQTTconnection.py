import time
import machine
from umqttsimple import MQTTClient
from machine import Pin
import network as nt
import json


client_id = "ESP32"
#mqtt_server = "778209500d2e429395808690733dbd2a.s1.eu.hivemq.cloud"
mqtt_server = "broker.hivemq.com"
user_mqtt = "LauraM"
password_mqtt = "13g8o5l3d21"

global new_topic
global new_message

new_topic='SI/Petition'
new_message=0


#topic_sub = b'notification'

def restart_and_reconnect():
    print('Failed to connect. Reconnecting...')
    time.sleep(5)
    machine.reset()

def conect_to(SSID, PASSWORD):
    try:
        sta_if = nt.WLAN(nt.STA_IF)
        sta_if.active(True)
        led = Pin(2,Pin.OUT)
        if not sta_if.isconnected():
            sta_if.active(True)
            print("Network name: ", SSID)
            print('Password: ', PASSWORD)
            sta_if.connect(SSID,PASSWORD)
            print("Trying to connect to the network: ",SSID)
            while nt.isconnected() == False:
                pass
        print("Connected")
        led.value(0)
    except OSError as e:
        restart_and_reconnect()
        
def extract_dict_data(dictionary, key='LocalID'): # Key is a string
    result=[]
    try:
        for x in range(len(list(dictionary.items()))):
            if list(dictionary.items())[x-1][0]==key:
                result=list(dictionary.items())[x-1]
        return result
    except AttributeError as e:
        print('Error: Reading str instead of dict')
        print('I give up')

def sub_cb(topic, msg):
    msg_dec =  json.loads(msg)
    global new_topic
    global new_message
    try:
        if type(msg_dec) is dict:
            externalID=extract_dict_data(msg_dec,'LocalID')[1]
            if externalID!=str(2):
                print('Received from topic: ', topic, '. Message: ', msg_dec, '\n')
                new_topic=topic
                new_message=msg_dec
                    
            else:
                print('Published on topic: ', topic, '. Message: ', msg_dec, '\n')
        else:
            print('Message must be dict type')
    except IndexError as e:
        print('Error: message contains no local ID')
        print('I give up')
    
def getValues():
    global new_topic
    global new_message
    return new_topic, new_message


def connect_and_subscribe():
    global client_id, mqtt_server
    client = MQTTClient(client_id,mqtt_server)
    client.connect()
    client.set_callback(sub_cb)
    client.subscribe(b'SI/Petition',1)
    print('Test text')
    client.subscribe(b'Easymeals/#',1)
    print('Connected to %s MQTT broker' % (mqtt_server))
    return client