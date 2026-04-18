import json
import ssl
import paho.mqtt.client as mqtt

PRINTER_IP = "192.168.13.192"
SERIAL = "01P00C5A0801686"
ACCESS_CODE = "7c26160b"

TOPIC = f"device/{SERIAL}/report"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        msg = "idle"
    if rc == 4:
        msg = "heating"
    if rc == 5:
        msg = "preparing"
    if rc == 6:
        msg = "printing"
    if rc == 9:
        msg = "paused"
    if rc == 10:
        msg = "finished"

    print("Verbunden,", msg)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        print("RAW:", msg.payload.decode())
        data = json.loads(msg.payload.decode())

        if "print" in data:
            status = data["print"].get("stg_cur")
            progress = data["print"].get("prg")
            print(f"Status: {status}, Fortschritt: {progress}%")

    except Exception as e:
        print("Fehler beim Parsen:", e)


client = mqtt.Client()
client.username_pw_set(SERIAL, ACCESS_CODE)

client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message

client.connect(PRINTER_IP, 8883, 60)
client.loop_forever()
