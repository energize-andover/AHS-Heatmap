from main import init
from data_tools import init_data_tools, fill_all_rooms
from flask import *
import os

svg_flask_path = os.path.join('static', 'svg_and_conversions', "Andover-HS-level-3.svg")
svg_output_path = svg_flask_path[0:-4] + "_filled_rooms.svg"
svg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), svg_flask_path)

rooms_and_sensors = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('data', 'csv', 'ahs_air.csv'))
current_facility = 'ahs'

# Set up the color values (temperature, co2)
# BLUE_VALUE is the temperatures/co2 levels that will be marked cold/low (with a light blue color)
# GREEN_VALUE is the temperatures/co2 levels that will be marked good (with a green color)
# RED_VALUE is the temperatures/co2 levels that will be marked hot/high (with a light red color)
BLUE_VALUE = (60, 600)
GREEN_VALUE = (70, 800)
RED_VALUE = (80, 1000)

init(svg_path, RED_VALUE, GREEN_VALUE, BLUE_VALUE)
init_data_tools(rooms_and_sensors, 'energize.andoverma.us', '8000')

fill_all_rooms(True)  # First start with temperature

app = Flask(__name__)


@app.route("/")
def load_svg():
    return render_template('svg_output_page.html', title='Andover HS Level 3',
                           svg_path=svg_output_path.replace('\\', '/'))


if __name__ == '__main__':
    app.run()
