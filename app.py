from flask import Flask, render_template, request, json, jsonify
from Main import *
import os
import pandas as pd

app = Flask(__name__)
secret_key_path = os.path.join('data', 'secret_key.txt')

svg_width = None
svg_height = None

csv_path = None

temperature_data = None

HOSTNAME = '10.12.4.98'
PORT = '8000'

RED_VALUE = (80, 900)
GREEN_VALUE = (65, 600)
try:
    with open(secret_key_path) as file:
        key = file.readline()
        if key:
            app.secret_key = key
        else:
            raise FileNotFoundError('No secret ket in file!')
except FileNotFoundError:
    app.secret_key = os.urandom(64)

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def root():
    return render_template('index.html')


@app.route("/getViewBox", methods={"GET"})
def get_view_box():
    global svg_width, svg_height

    svg_width = request.args.get("width")
    svg_height = request.args.get("height")

    return json.dumps({'width': svg_width, 'height': svg_height})  # Return to ensure that the data is correct


@app.route("/init")
def init_main():
    success = init(HOSTNAME, PORT, 'AHS')
    return json.dumps({'status': success})


@app.route("/getAllData", methods={"GET"})
def get_all_data():
    global csv_path, temperature_data
    csv_path = os.path.join('data', 'csv', 'ahs_air.csv')

    df = pd.read_csv(csv_path)

    floor = request.args.get("floor")
    filtered_rooms = df[df['Room'].str.startswith(str(floor))]

    # data = get_all_room_data(filtered_rooms, floor)
    temp_data = pd.read_csv(os.path.join('data', 'csv', 'ahs_default_data.csv'))

    common = temp_data.merge(filtered_rooms, on=['Room'])
    temp_data = temp_data.drop(labels=['Unnamed: 0'], axis=1)  # Remove the duplicated index column
    temp_data = temp_data[(temp_data.Room.isin(common.Room))]
    temp_data = temp_data.reset_index(drop=True)  # Reset to count from 0 after dropping

    temperature_data = temp_data

    return json.dumps({'rooms': temp_data['Room'].unique().tolist()})


@app.route("/fillRoom", methods={"GET"})
def fill_room():
    global temperature_data

    if temperature_data is not None:
        room = request.args.get("room")

        selected_row = temperature_data.loc[temperature_data['Room'] == str(room)]

        measure = int(selected_row.iloc[0]['Temperature'])
        units = str(selected_row.iloc[0]['Temperature Units'])

        room_exists = fill_chosen_room(room, measure, units)

        if room_exists:
            return json.dumps({"status": "Ok!"})
        else:
            return json.dumps({"status": "No room labeled \'{0}\' found!".format(room)})

    return json.dumps({"status": "No Data!"})


if __name__ == "__main__":
    app.run()
