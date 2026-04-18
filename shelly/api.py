import threading
import time
import json
import paho.mqtt.client as mqtt


class ShellyPro3MMQTT:
    def __init__(self, broker, device_id, username=None, password=None, on_event=None):
        self.broker = broker
        self.device_id = device_id
        self.username = username
        self.password = password
        self.on_event = on_event

        self.client = mqtt.Client()
        if username and password:
            self.client.username_pw_set(username, password)

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

        self._thread = None
        self._stop = False

    def _on_connect(self, client, userdata, flags, rc):
        print("[Shelly MQTT] Verbunden")

        # Alle EM‑Topics abonnieren
        base = f"{self.device_id}/em/0/#"
        client.subscribe(base)
        print(f"[Shelly MQTT] Subscribed: {base}")

    def _on_disconnect(self, client, userdata, rc):
        print("[Shelly MQTT] Verbindung verloren")

    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        try:
            payload = json.loads(payload)
        except:
            pass

        if self.on_event:
            self.on_event(msg.topic, payload)

    def _run(self):
        while not self._stop:
            try:
                print(f"[Shelly MQTT] Verbinde zu {self.broker} ...")
                self.client.connect(self.broker)
                self.client.loop_forever()
            except Exception as e:
                print(f"[Shelly MQTT] Fehler: {e}")
                time.sleep(3)

    def start(self):
        if self._thread is None:
            self._stop = False
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            print("[Shelly MQTT] Monitoring gestartet")

    def stop(self):
        self._stop = True
        self.client.disconnect()
        print("[Shelly MQTT] Monitoring gestoppt")
