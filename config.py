import os

'''
    # Utilize the os package to form your paths:
    # The method os.path.join(part1, part2, ... lastPart) forms a properly-formatted path for your OS. 
    # The variable os.sep represents the proper path separator for your os (i.e. '/')
    # The method os.path.dirname(os.path.realpath(__file__) returns the path to the directory in which this file is 
      stored, named Nginx-Indexer by default. It may be useful os.path.join() it in your TEMP_UPDATE_PATH, 
      SVG_AND_CONVERSIONS_PATH, and ROOM_SENSOR_CSV
'''

'''
  # The prefix for the URL. For example, if equal to "/heatmap", the home page will be located at /heatmap/, the about page at
    /heatmap/about, the static files under /heatmap/static/. This is very useful for running the application on servers with
    many apps running on them with Nginx. 
'''
HOST_PREFIX = "" 

# The list of the levels of the floors that maps are provided for. Will be appended to the SVG_FILE_PREFIX
# e.g.: When equal to [2, 3, 4] and SVG_FILE_PREFIX = "Andover-HS-level-", files Andover-HS-level-2.svg, Andover-HS-level-3.svg
#     and Andover-HS-level-4.svg will be used as inputs and should be stored in the directory at SVG_AND_CONVERSIONS_PATH.
BUILDING_LEVELS = [2, 3, 4] 

# The path to the folder in which temporary SVG files will be stored during the updating process
TEMP_UPDATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('static', 'temp_update_svgs'))

# The prefix to the names of each SVG file you want to generate a map. Should be used in combination with BUILDING_LEVELS.
# See the comment above BUILDING_LEVELS for an example. 
SVG_FILE_PREFIX = "Andover-HS-level-"

# The path to the directory in which the svg files with the SVG_FILE_PREFIX prefix and BUILDING_LEVELS suffix lie
SVG_AND_CONVERSIONS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('static', 'svg_and_conversions'))

'''
  # The path to the CSV file with the data needed to access the sensors in the school. Will be read to request data.
  # It should have the following columns:
    # 'Label': Contains the number of the room in which the sensor lies. Dashes should be replaced with periods (e.g. '270.01')
    # 'Facility': The ID of the building that contains the room. The Heatmap will only read from rows with a facility of 'ahs'
    # 'Temperature': The ID number of the temperature sensor (e.g. '3011595')
    # 'CO2': The ID number of the CO2 sensor (e.g. '3011592') 
'''
ROOM_SENSOR_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('data', 'csv', 'ahs_air.csv'))

'''
  # Do NOT delete or rename any of these configuration constants. Doing so will stop the Heatmap from running.
  # BE SURE TO RUN 'git update-index --skip-worktree config.py' in the command line AFTER MAKING CHANGES TO THIS FILE FOR THE
    FIRST TIME! Doing so will keep your machine-specific configurations out of the repository, allowing the defaults to 
    remain untouched. 
'''
