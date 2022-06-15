from MQTTconnection import *

client_id = "ESP32"
#mqtt_server = "778209500d2e429395808690733dbd2a.s1.eu.hivemq.cloud"
mqtt_server = "test.mosquitto.org"
user_mqtt = "LA.CONSENTIDA"
password_mqtt = "13g8o5l3d21"

#topic_sub = b'notification'

last_message = 0
message_interval = 2
received = True
ID = b'101006'
ID = ID.decode('utf8').replace("'", '"')

#conect_to("Juan F","qwertyuiop")
conect_to(user_mqtt,password_mqtt)

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    #client.check_msg()
    if (time.time() - last_message) > message_interval:
        if received:
            client.publish(b'SI/Petition', json.dumps(ID),True,1)
            received = False
        else:
            client.check_msg()
            received = True
        last_message = time.time()
  except OSError as e:
    restart_and_reconnect()
