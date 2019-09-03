import os

HOST_PREFIX = ""
BUILDING_LEVELS = [2, 3, 4]
TEMP_UPDATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('static', 'temp_update_svgs'))
SVG_FILE_PREFIX = "Andover-HS-level-"
SVG_AND_CONVERSIONS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('static', 'svg_and_conversions'))
ROOM_SENSOR_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('data', 'csv', 'ahs_air.csv'))
