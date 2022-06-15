import paho.mqtt.client as paho

client=paho.Client()
client.connect("test.mosquitto.org", 1883,60)
client.publish("SI/Petition", "101006")