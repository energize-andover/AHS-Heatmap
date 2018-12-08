from main import HeatmapMain
from data_tools import init_data_tools, fill_all_rooms, update_air_data
from file_update_tools import update_map
from flask import *
import os
import sched
import time
import datetime as dt
import timeinterval
import threading
import calendar
import datetime
import shutil

svg_file_name = "Andover-HS-level-3.svg"
svg_flask_path = os.path.join('static', 'svg_and_conversions', svg_file_name)
svg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), svg_flask_path)

rooms_and_sensors = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('data', 'csv', 'ahs_air.csv'))

# Set up the color values (temperature, co2)
# BLUE_VALUE is the temperatures/co2 levels that will be marked cold/low (with a light blue color)
# GREEN_VALUE is the temperatures/co2 levels that will be marked good (with a green color)
# RED_VALUE is the temperatures/co2 levels that will be marked hot/high (with a light red color)
BLUE_VALUE = (60, 100)
GREEN_VALUE = (70, 900)
RED_VALUE = (80, 2000)

floor_3 = HeatmapMain(svg_path, RED_VALUE, GREEN_VALUE, BLUE_VALUE)
init_data_tools(rooms_and_sensors)

fill_all_rooms(floor_3, True)  # First start with temperature
fill_all_rooms(floor_3, False)

scheduler = sched.scheduler(time.time, time.sleep)

# Empty out the temporary folder by deleting it and making a new one
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           os.path.join('static', 'temp_update_svgs'))
shutil.rmtree(folder_path)
os.mkdir(folder_path)


def datetime_to_utc(dt):
    """Converts a datetime object to UTC timestamp
        naive datetime will be considered UTC."""

    return calendar.timegm(dt.utctimetuple())


def update_svg():
    print("Updating svg...")
    update_air_data()
    update_map(svg_file_name, svg_path, RED_VALUE, GREEN_VALUE, BLUE_VALUE)


def start_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("index.html", title="Floor Plan", time=get_time())

    @app.route("/ahs/<floor>")
    def load_svg(floor):
        try:
            floor_num = float(floor)
        except ValueError:
            abort(404)

        if 1 <= floor_num <= 4:
            return render_template('svg_output_page.html', title='Andover HS Level {0}'.format(floor),
                                   file_filled_prefix="Andover-HS-level-{0}_filled_rooms_".format(floor),
                                   time=get_time())
        else:
            abort(404)

    app.run()


def get_time():
    return datetime_to_utc(datetime.datetime.now())


def start_svg_auto_updater():
    second = dt.datetime.now().second + 1

    while second != 60:
        time.sleep(1)
        second = dt.datetime.now().second + 1

    print("Seconds synced")

    minute = dt.datetime.now().minute % 10 + 1

    while minute != 4 and minute != 9:
        time.sleep(60)
        minute = dt.datetime.now().minute % 10 + 1

    print("Minutes synced\nStarting update thread...")

    timeinterval.start(5 * 60 * 1000, update_svg)
    update_svg()


if __name__ == '__main__':
    update_thread = threading.Thread(target=start_svg_auto_updater)
    update_thread.start()

    start_app()
