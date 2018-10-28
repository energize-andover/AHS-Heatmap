from main import init, get_value_color, delete_temp_file
from data_tools import init_data_tools, fill_all_rooms, get_new_room_data
from flask import *
import os
import threading
import datetime as dt

svg_flask_path = os.path.join('static', 'svg_and_conversions', "Andover-HS-level-3.svg")
svg_output_path = svg_flask_path[0:-4] + "_filled_rooms.svg"
svg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), svg_flask_path)

rooms_and_sensors = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('data', 'csv', 'ahs_air.csv'))
current_facility = 'ahs'

# Set up the color values (temperature, co2)
# BLUE_VALUE is the temperatures/co2 levels that will be marked cold/low (with a light blue color)
# GREEN_VALUE is the temperatures/co2 levels that will be marked good (with a green color)
# RED_VALUE is the temperatures/co2 levels that will be marked hot/high (with a light red color)
BLUE_VALUE = (60, 100)
GREEN_VALUE = (70, 900)
RED_VALUE = (80, 2000)

init(svg_path, RED_VALUE, GREEN_VALUE, BLUE_VALUE)
init_data_tools(rooms_and_sensors, '10.12.4.98', '8000')

fill_all_rooms(True)  # First start with temperature

current_update_thread = None


class SVG_Update_Thread:
    def __init__(self, is_temperature):
        self.is_temperature = is_temperature
        self.is_busy = False

    def is_busy(self):
        return self.is_busy

    def start(self):
        thread = threading.Thread(target=reload_svg, args=[is_temperature])
        thread.daemon = True
        thread.start()

    def reload_svg(self):
        self.is_busy = True
        delete_temp_file()
        fill_all_rooms(self.is_temperature)
        self.is_busy = False
        print("Updated SVG successfully at {0}.".format(dt.datetime.now()))


app = Flask(__name__)


@app.route("/")
def load_svg():
    return render_template('svg_output_page.html', title='Andover HS Level 3',
                           svg_path=svg_output_path.replace('\\', '/'))


@app.route("/get_room_data", methods=['GET'])
def return_room_data():
    global current_update_thread

    room = request.args.get('room')
    is_temperature = int(request.args.get('temperature')) == 1
    data = get_new_room_data(room)

    if current_update_thread is None or (
            isinstance(current_update_thread, SVG_Update_Thread) and not current_update_thread.is_busy()):
        current_update_thread = SVG_Update_Thread(is_temperature)
        current_update_thread.start()

    value_column = 'temperature' if is_temperature else 'co2'
    value = np.asscalar(data[value_column].iloc[0])
    color = get_value_color(value, is_temperature)
    returned_data = {'status': 'ok', value_column: value,
                     value_column + ' units': data[value_column + ' units'].iloc[0]}
    return jsonify(returned_data)


if __name__ == '__main__':
    app.run()
