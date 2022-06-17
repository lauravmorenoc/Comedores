from MQTTconnection import *


last_publish_time = 0
message_interval = 2
received = True
ID = b'101006'
ID = ID.decode('utf8').replace("'", '"')

myMsg={
    'LocalID':'2',
    'ID': '101006'
    }

# WLAN network
net_name = "LA.CONSENTIDA"
net_password = "13g8o5l3d21"
#net_name = "UNAL"
#net_password = ""

conect_to(net_name,net_password)

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    #client.check_msg()
    if (time.time() - last_publish_time) > message_interval:
        if received:
            client.publish(b'SI/Petition', json.dumps(ID),True,1)
            received = False
        else:
         #   client.check_msg()
            received = True
        last_publish_time = time.time()
  except OSError as e:
    restart_and_reconnect()
