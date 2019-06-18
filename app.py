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

app
HOST_PREFIX = "/heatmap"

levels = [2, 3, 4]
svg_file_prefix = "Andover-HS-level-"
svg_and_conversions_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        os.path.join('static', 'svg_and_conversions'))

rooms_and_sensors = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('data', 'csv', 'ahs_air.csv'))

# Set up the color values (temperature, co2)
# BLUE_VALUE is the temperatures/co2 levels that will be marked cold/low (with a light blue color)
# GREEN_VALUE is the temperatures/co2 levels that will be marked good (with a green color)
# RED_VALUE is the temperatures/co2 levels that will be marked hot/high (with a light red color)
BLUE_VALUE = (60, 100)
GREEN_VALUE = (70, 900)
RED_VALUE = (80, 2000)

# Empty out the temporary folder by deleting it and making a new one
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('static', 'temp_update_svgs'))

if os.path.exists(folder_path):
    shutil.rmtree(folder_path)

os.mkdir(folder_path)

init_data_tools(rooms_and_sensors)

for level in levels:
    svg_file_name = svg_file_prefix + str(level) + '.svg'
    svg_path = os.path.join(svg_and_conversions_path, svg_file_name)

    heatmap = HeatmapMain(svg_path, RED_VALUE, GREEN_VALUE, BLUE_VALUE)

    fill_all_rooms(heatmap, True)  # First start with temperature
    fill_all_rooms(heatmap, False)

scheduler = sched.scheduler(time.time, time.sleep)


def datetime_to_utc(dt):
    """Converts a datetime object to UTC timestamp
        naive datetime will be considered UTC."""

    return calendar.timegm(dt.utctimetuple())


def update_svg():
    update_air_data()

    for floor_level in levels:
        file_name = svg_file_prefix + str(floor_level) + '.svg'
        file_path = os.path.join(svg_and_conversions_path, file_name)

        update_map(svg_file_name, file_path, RED_VALUE, GREEN_VALUE, BLUE_VALUE)


def start_app():
    global app
    app = Flask(__name__)

    # @app.context_processor
    # def inject_floors_to_all_templates():
    #     return dict(floors=levels)

    @app.context_processor
    def inject_time_to_all_templates():
        return dict(time=get_time())

    @app.context_processor
    def inject_year_to_all_templates():
        return dict(year=get_year())

    @app.route("{0}/".format(HOST_PREFIX))
    def home():
        return render_template("index.html", title="AHS Heatmaps")

    @app.route("{0}/about".format(HOST_PREFIX))
    def about():
        return render_template("about.html", title="About | AHS Heatmaps")

    @app.route("{0}/ahs/<floor>".format(HOST_PREFIX))
    def load_svg(floor):
        try:
            floor_num = float(floor)
        except ValueError:
            abort(404)
            return None  # Stops the following code from executing

        if floor_num in levels:
            return render_template('svg_output_page.html', title='Andover HS Level {0}'.format(floor),
                                   file_filled_prefix="Andover-HS-level-{0}_filled_rooms_".format(floor), floor=floor)
        else:
            abort(404)

    @app.errorhandler(404)
    def error_404(e):
        return load_error_page(404, 'Page Not Found', 'The page you are looking for might have been removed, had its ' +
                               'name changed, or be temporarily unavailable.')

    @app.errorhandler(403)
    def error_403(e):
        return load_error_page(403, 'Forbidden', 'You don\'t have permission to access this page on this server')

    @app.errorhandler(500)
    def error_500(e):
        return load_error_page(500, 'Internal Server Error', Markup('The server encountered an internal error or ' +
                                                                    'misconfiguration and was unable to complete your request. <br><br>' +
                                                                    'Please contact Daniel Ivanovich (<a href="mailto:dan@ivanovi.ch">dan@ivanovi.ch</a>) ' +
                                                                    'to make this issue known.'))

    def load_error_page(code, tagline, details):
        return render_template('error.html', code=str(code), tagline=tagline, details=details), code

    app.register_error_handler(404, error_404)

    app.jinja_env.globals['host_prefix'] = HOST_PREFIX
    app.jinja_env.globals['floors'] = levels
    app.jinja_env.globals['date'] = datetime.datetime.now().strftime("%B %d, %Y")
    app.jinja_env.globals['blue_values'] = BLUE_VALUE
    app.jinja_env.globals['green_values'] = GREEN_VALUE
    app.jinja_env.globals['red_values'] = RED_VALUE
    app.static_url_path = '{0}/static'.format(HOST_PREFIX)

    # remove old static map
    url_map = app.url_map
    try:
        for rule in url_map.iter_rules('static'):
            url_map._rules.remove(rule)
    except ValueError:
        # no static view was created yet
        pass

    # register new; the same view function is used
    app.add_url_rule(
        app.static_url_path + '/<path:filename>',
        endpoint='static', view_func=app.send_static_file)


def get_time():
    return datetime_to_utc(datetime.datetime.now())


def get_year():
    return datetime.datetime.now().year


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

update_thread = threading.Thread(target=start_svg_auto_updater)
update_thread.start()

start_app()

if __name__ == '__main__':
    app.run()
