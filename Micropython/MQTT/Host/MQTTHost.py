import time
import json
import paho.mqtt.client as paho
from paho import mqtt

usersID=[b"101006",b"100743"]

for x in range(len(usersID)):
    usersID[x-1] = usersID[x-1].decode('utf8').replace("'", '"')

usersData={
    "LocalID":"1",
    "Name":"Laura",
    "Rol":"Student"
    }

def on_connect(client, userdata, flags, rc, properties=None): # rc=0 means everything is right, else do worry
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid, properties=None): # Succesfully published
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print("Received: "+msg.topic+" "+str(msg.payload))
    if msg.topic=='SI/Petition':
        message=json.loads(msg.payload)
       # print('Arrival text', message, 'Type: ', type(message))
       # print('Local text', usersID[0], 'Type: ', type(usersID[0]))
        if message in usersID:
            print('User found')
            #client.publish(b'SI/Petition', json.dumps(usersData),qos= 1)
            client.publish('SI/Petition', json.dumps(usersData),True,0)
          #  (rc, mid)= 
        #else:
         #   client.publish('SI/Petition', json.dumps('Not found'),True,0)

client = paho.Client()
client.on_connect = on_connect
client.connect("broker.hivemq.com", 1883,60)

client.on_subscribe = on_subscribe
client.on_message = on_message
#client.on_publish = on_publish

# subscribe 
client.subscribe("SI/Petition", qos=1)
client.subscribe("Easymeals/#", qos=1)

client.loop_start()


while True:
    client.on_message = on_message 