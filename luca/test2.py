import json
import ssl
import paho.mqtt.client as mqtt

PRINTER_IP = "192.168.13.192"
SERIAL = "01P00C5A0801686"
ACCESS_CODE = "73272102"  # MUSS STRING SEIN

TOPIC = f"device/{SERIAL}/report"

def on_connect(client, userdata, flags, rc):
    print("MQTT Connect Code:", rc)
    if rc == 0:
        client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print("RAW:", msg.payload.decode())

client = mqtt.Client()
client.username_pw_set(SERIAL, ACCESS_CODE)

client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message

client.connect(PRINTER_IP, 8883, 60)
client.loop_forever()
