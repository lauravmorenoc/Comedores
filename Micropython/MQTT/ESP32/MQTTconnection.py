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

def sub_cb(topic, msg):
    msg_dec =  json.loads(msg)
    #print('El mensaje es del tema %s,  mensaje %s',topic,msg)
    if topic == b'SI/Petition':
        print('Callback message: ', msg_dec)
        #print('Variable type: ', type(msg_dec))
    else:
        print('Callback: Unknown topic')


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

