from config import *
from main import HeatmapMain
from data_tools import fill_all_rooms
import os
import shutil


def update_map(svg_name, svg_path, red, green, blue):
    # Build the absolute path of the temporary output file (where what will be the updated SVG is stored)
    TEMP_UPDATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    os.path.join('static', 'temp_update_svgs', svg_name))

    shutil.copy(svg_path, TEMP_UPDATE_PATH)  # Copy the empty SVG to the other folder

    heatmap = HeatmapMain(TEMP_UPDATE_PATH, red, green, blue)

    is_temperature = True

    for iteration in range(2):
        fill_all_rooms(heatmap, is_temperature)
        outputted_svg_path = TEMP_UPDATE_PATH[0:-4] + '_filled_rooms_{0}.svg'.format(
            'temperature' if is_temperature else 'co2')

        svg_to_be_replaced = svg_path[0:-4] + '_filled_rooms_{0}.svg'.format(
            'temperature' if is_temperature else 'co2')  # The currently existing, outdated, filled SVG file

        if os.path.exists(svg_to_be_replaced):
            os.remove(svg_to_be_replaced)

        shutil.copy(outputted_svg_path, svg_to_be_replaced)

        is_temperature = not is_temperature  # Toggle is_temperature
