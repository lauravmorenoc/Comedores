import time
import json
import paho.mqtt.client as paho
from paho import mqtt


def on_connect(client, userdata, flags, rc, properties=None): # rc=0 means everything is right, else do worry
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid, properties=None): # Succesfully published
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = paho.Client()
client.on_connect = on_connect
client.connect("broker.hivemq.com", 1883,60)

client.on_subscribe = on_subscribe
client.on_message = on_message
#client.on_publish = on_publish

# subscribe 
client.subscribe("SI/Petition", qos=1)
client.subscribe("SI/Easymeals/#", qos=1)

client.loop_start()


while True:
    client.on_message = on_message 