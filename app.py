from flask import Flask, render_template, request, json
from Main import *
import os
import pandas as pd

app = Flask(__name__)
secret_key_path = os.path.join('data', 'secret_key.txt')

svg_width = None
svg_height = None

csv_path = None

HOSTNAME = '10.12.4.98'
PORT = '8000'

RED_VALUE = (80, 900)
GREEN_VALUE = (65, 600)


with open(secret_key_path) as file:
    key = file.readline()
    app.secret_key = key if key else os.urandom(64)


@app.route("/")
@app.route("/index")
@app.route("/index.html")
def root():
    return render_template('index.html')


@app.route("/getViewBox", methods={"GET"})
def get_view_box():
    global svg_width
    global svg_height

    svg_width = request.args.get("width")
    svg_height = request.args.get("height")

    return json.dumps({'width': svg_width, 'height': svg_height})  # Return to ensure that the data is correct


@app.route("/init")
def init_main():
    success = init(svg_width, svg_height, HOSTNAME, PORT, 'AHS')
    return json.dumps({'status': success})


@app.route("/getAllData", methods={"GET"})
def get_all_data():
    global csv_path
    csv_path = os.path.join('data', 'csv', 'ahs_air.csv')

    df = pd.read_csv(csv_path)

    floor = request.args.get("floor")
    filtered_rooms = df[df['Label'].str.startswith(str(floor))]

    data = get_all_room_data(filtered_rooms, floor)


if __name__ == "__main__":
    app.run()
