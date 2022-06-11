from MQTTconnection import *

client_id = "ESP32"
#mqtt_server = "778209500d2e429395808690733dbd2a.s1.eu.hivemq.cloud"
mqtt_server = "broker.mqttdashboard.com"
user_mqtt = "JuanFelipe"
password_mqtt = "xr8_G!pQiw2R6fC"

#topic_sub = b'notification'

last_message = 0
message_interval = 2
received = True
ID = b'CH10537T'
ID = ID.decode('utf8').replace("'", '"')

#conect_to("Juan F","qwertyuiop")
conect_to("Carlos Mario Gonzalez","Carmar15")

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    #client.check_msg()
    if (time.time() - last_message) > message_interval:
        if received:
            client.publish(b'SI/Validar', json.dumps(ID),True,1)
            received = False
        else:
            client.check_msg()
            received = True
        last_message = time.time()
        """client.publish(b'SI/Validar', ID)
        last_message = time.time()"""
  except OSError as e:
    restart_and_reconnect()
