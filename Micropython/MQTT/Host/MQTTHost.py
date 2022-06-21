import time
import json
import paho.mqtt.client as paho
from paho import mqtt

usersID=[b"101006",b"100743"]

for x in range(len(usersID)):
    usersID[x-1] = usersID[x-1].decode('utf8').replace("'", '"')

usersData={
    "LocalID":"1",
    "Registered": True,
    "Name":"Laura",
    "Rol":"Student"
    }

def extract_dict_data(dictionary, key='LocalID'): # Key is a string
    result=[]
    for x in range(len(list(dictionary.items()))):
        if list(dictionary.items())[x-1][0]==key:
            result=list(dictionary.items())[x-1]
    return result

def on_connect(client, userdata, flags, rc, properties=None): # rc=0 means everything is right, else do worry
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid, properties=None): # Succesfully published
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
  #  print("Received: "+msg.topic+" "+str(msg.payload))
    message=json.loads(msg.payload)
    print('Received: ' + str(list(message.items())) + '. On topic: ' + msg.topic)
    try:
        externalID=extract_dict_data(message,'LocalID')[1]
    except IndexError as e:
        print('Error: message contains no local ID')
        print('I give up')
        pass
    #print ('Reading LocalID: ' + str(extract_dict_data(message,'LocalID')[1]))
    if externalID!=str(1):
        if msg.topic=='SI/Petition':
            data={"LocalID":"1"}
            client.publish(msg.topic, json.dumps(data),True,1)
            print('Sent: ', data, '. Topic: ', msg.topic, '\n')
        elif msg.topic=='Easymeals/Payment':
            try:
                userID=extract_dict_data(message,'ID')[1]
                if userID in usersID:
                    print('User found')
                    usersData["Registered"] = True
                else:
                    usersData["Registered"] = False
                client.publish(msg.topic, json.dumps(usersData),True,1)
                print('Sent: ', usersData, '. Topic: ', msg.topic, '\n')

            except IndexError as e:
                print('Error: message contains no user ID')
                print('I give up')
                pass
        elif msg.topic=='Easymeals/Update':
            try:
                ticket=message["ticket"]
                data={"LocalID":"1",
                      "ticket":ticket,
                      "Comedor": 1
                      }
                client.publish(msg.topic, json.dumps(data),True,1)
            except KeyError as e:
                print('Error: message contains no ticket')
                print('I give up')
                pass
            print('Sent: ', usersData, '. Topic: ', msg.topic, '\n')
            
    else:
        print('I dont really care \n')
        
        '''
        if message in usersID:
            print('User found')
            #client.publish(b'SI/Petition', json.dumps(usersData),qos= 1)
            client.publish('SI/Petition', json.dumps(usersData),True,0)
        '''
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