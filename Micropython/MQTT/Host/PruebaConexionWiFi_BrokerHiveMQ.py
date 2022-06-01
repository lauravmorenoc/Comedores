import time
import json
import paho.mqtt.client as paho
from paho import mqtt

ID = ['CH10537T','Cjadgyieb','wdbhef']
m = {
    "Nombre": "Juan Felipe",
    "Permisos": "Si"
}
m1 = ['Juan','Si']
m2_bytes = b'[\'Hola\',\'bien\']'
m2 = m2_bytes.decode('utf8').replace("'", '"')
a = 1


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    #print(str(msg.payload.decode()))
    if msg.topic == 'SI/Validar':
        if json.loads(msg.payload) in ID:
            print("Si está en la base de datos")
            time.sleep(1)
            (rc, mid)= client.publish(msg.topic,json.dumps(m),qos= 1)
        
    elif msg.topic == 'SI/Easyrun/Prestar':
        a = 1
    elif msg.topic == 'SI/Easyrun/Devolver':
        a = 2
    elif msg.topic == 'SI/Easyrun/Distribuir':
        a = 3
    else:
        print("No se envió nada")
        (rc, mid) = client.publish('SI/Validar',json.dumps("Hola"),qos = 1)




# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
# client = paho.Client(client_id="Paco", userdata=None, protocol=paho.MQTTv5)
client = paho.Client("Paco")
client.on_connect = on_connect

# enable TLS for secure connection
# client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
# client.username_pw_set("JuanFelipe", "xr8_G!pQiw2R6fC")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)

client.connect("broker.mqttdashboard.com", 1883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
#client.on_publish = on_publish

# subscribe 
client.subscribe("SI/Validar", qos=1)
client.subscribe("SI/Esayrun/#", qos=1)

client.loop_start()


while True:
    #(rc, mid) = client.publish("SI/Validar", "False", qos=1)
    #time.sleep(5)
    #(rc, mid) = client.publish("notification/holu", "100", qos = 1)
    client.on_message = on_message 