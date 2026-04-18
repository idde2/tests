from flask_socketio import SocketIO

import requests
from flask import Flask, render_template

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

path = "192.168.0.24"

def getjson(arg):
    resp = requests.post(f"http://{path}/rpc/{arg}", json={})
    return resp.json()

def background_updater():
    while True:
        data = getjson("Shelly.GetStatus")
        power = data["em:0"]["a_act_power"] + data["em:0"]["b_act_power"] + data["em:0"]["c_act_power"]
        power = round(power)
        socketio.emit("update", power)

        socketio.sleep(3)


@app.route("/")
def index():
    data = getjson("Shelly.GetStatus")

    power = data["em:0"]["a_act_power"] + data["em:0"]["b_act_power"] + data["em:0"]["c_act_power"]

    return render_template("index.html", power=power)

socketio.start_background_task(background_updater)
socketio.run(app, host="0.0.0.0",port=5000,allow_unsafe_werkzeug=True,debug=True)