import sys
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)
daten = [(1, 'test', 22.5),
         (2, 'test2', "abcs")]


if getattr(sys, 'frozen', False):
    path = Path(sys.executable).resolve().parent
else:
    path = Path(__file__).resolve().parent

datei = path / "passwort.pw"


def write_value(filepath, value):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)

def read_value(filepath):
    try:
        if not Path(filepath).exists():
            return []

        content = Path(filepath).read_text(encoding="utf-8").strip()
        if not content:
            return []

        return json.loads(content)

    except json.JSONDecodeError:
        return []


def clear_file(filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("[]")



@app.route("/")
def index():
    daten = read_value(datei)
    return render_template("index.html",daten=daten)

@app.route("/eingabe", methods=["GET", "POST"])
def eingabe():
    if request.method == "POST":
        name = request.form["name"].strip()
        wert = request.form["wert"]

        daten = read_value(datei)
        daten.append((len(daten) + 1, name, wert))

        write_value(datei, daten)

        return redirect(url_for("index"))

    return render_template("eingabe.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)