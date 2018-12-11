from file_conversion_tools import *
from pdf_tools import *
from coordinate_tools import *
from bs4 import BeautifulSoup
from colour import Color
import os
import shutil
import svgwrite
import svgutils.transform as st
import math


class HeatmapMain:
    def __init__(self, path, r, g, b):
        self.svg_path = path

        self.pdf_path = self.svg_path[0:-4] + ".pdf"
        self.png_path = self.svg_path[0:-4] + ".png"

        temp_path = self.svg_path[0:-4] + '_filled_rooms_temperature.svg'
        co2_path = self.svg_path[0:-4] + '_filled_rooms_co2.svg'

        if os.path.exists(temp_path):
            os.remove(temp_path)

        if os.path.exists(co2_path):
            os.remove(co2_path)

        svg_to_pdf(self.svg_path, self.pdf_path)
        self.text_and_coords = get_text_and_coordinates(self.pdf_path)

        svg_to_png(self.svg_path, self.png_path, 72)
        initialize_cv(self.png_path)

        # Extract the viewBox from the SVG using BeautifulSoup and convert it into a tuple of integers
        soup = BeautifulSoup(open(self.svg_path), "html.parser")
        self.view_box = tuple(map(int, soup.find("svg")["viewbox"].split(" ")))
        self.media_box = get_media_box(self.pdf_path)

        self.red_value = r
        self.green_value = g
        self.blue_value = b

        self.red = Color('#ff0000')
        self.green = Color('#00ff00')
        self.blue = Color('#00ffff')

        self.generate_color_arrays()

    def fill_room(self, room, color_hex_code, opacity, value, units, is_temperature):
        temp_path = self.svg_path[0:-4] + '_temp_rect.svg'
        output_path = self.svg_path[0:-4] + '_filled_rooms_{0}.svg'.format('temperature' if is_temperature else 'co2')

        if not os.path.exists(output_path):
            shutil.copy(self.svg_path, output_path)

        room_rect_info = get_room_rect_info(room, self.media_box, self.text_and_coords)

        if room_rect_info is not None:
            room_corner = (room_rect_info[0], room_rect_info[1])
            room_width = room_rect_info[2]
            room_height = room_rect_info[3]

            room_rect_svg_coords = get_svg_coords(room_corner, self.view_box, self.media_box)
            room_svg_width = get_svg_measure(room_width, self.view_box[2], self.media_box[2])
            room_svg_height = get_svg_measure(room_height, self.view_box[3], self.media_box[3])

            dwg = svgwrite.Drawing(temp_path)
            dwg.add(dwg.path(
                d="M{0} {1} L{2} {3} L{4} {5} L{6} {7} Z".format(room_rect_svg_coords[0], room_rect_svg_coords[1],
                                                                 room_rect_svg_coords[0],
                                                                 room_rect_svg_coords[1] + room_svg_height,
                                                                 room_rect_svg_coords[0] + room_svg_width,
                                                                 room_rect_svg_coords[1] + room_svg_height,
                                                                 room_rect_svg_coords[0] + room_svg_width,
                                                                 room_rect_svg_coords[1]), fill=color_hex_code,
                opacity=opacity, id="room-rect-{0}".format(room),
                onmouseover="showRoomData(this, {0}, '{1}')".format(value, units),
                onmouseout="hideRoomData(this)"))
            dwg.save()  # Save the path to a temporary file

            # Merge the files
            floor_plan = st.fromfile(output_path)
            second_svg = st.fromfile(temp_path)
            floor_plan.append(second_svg)
            floor_plan.save(output_path)
            os.remove(temp_path)

    def generate_color_arrays(self):
        global temperature_colors, co2_colors
        temperature_colors = self.generate_color_array(self.red_value[0], self.green_value[0], self.blue_value[0])
        co2_colors = self.generate_color_array(self.red_value[1], self.green_value[1], self.blue_value[1])

    def generate_color_array(self, red_val, green_val, blue_val):
        blue_to_green = list(self.blue.range_to(self.green, green_val - blue_val + 1))
        green_to_red = list(self.green.range_to(self.red, red_val - green_val))
        green_to_red.pop(0)  # Remove the repeat of green
        return blue_to_green + green_to_red

    def get_value_color(self, value, is_temperature_value):
        value_index = 0 if is_temperature_value else 1
        global array_index
        array_index = 0

        last_element_index = self.red_value[value_index] - self.blue_value[value_index] - 1

        if value <= self.blue_value[value_index]:
            array_index = 0
        elif value < self.red_value[value_index]:
            array_index = int(last_element_index - (self.red_value[value_index] - value) + 1)
        else:
            array_index = last_element_index  # The index of the last element in the color array

        return temperature_colors[array_index].hex_l if is_temperature_value else co2_colors[array_index].hex_l

    def fill_from_data(self, data, is_temperature_value):
        value = data['temperature'] if is_temperature_value else data['co2']
        units = data['temperature units'] if is_temperature_value else data['co2 units']
        if not math.isnan(value) and units is not None and units != '':
            color = self.get_value_color(value, is_temperature_value)
            self.fill_room(data['room'], color, 0.6, value, units, is_temperature_value)

    def add_overlay(self, is_temperature):
        temp_path = self.svg_path[0:-4] + '_temp_rect.svg'
        output_path = self.svg_path[0:-4] + '_filled_rooms_{0}.svg'.format('temperature' if is_temperature else 'co2')

        dwg = svgwrite.Drawing(temp_path)
        dwg.add(dwg.path(d="M0 0 L0 {0} L{1} {2} L{3} 0 Z".format(self.view_box[3], self.view_box[2], self.view_box[3],
                                                                  self.view_box[2]),
                         fill='#ffffff', opacity=0, id="floor-plan-overlay", visibility="hidden"))
        dwg.add(dwg.rect(insert=(0, 0), size=(0, 0), fill="white", stroke="black", id="value-box", visibility="hidden"))
        dwg.add(dwg.text(text="", insert=(0, 0), fill="black", id="room-title-text", visibility="hidden",
                         style="font-weight: bold; font-size: 80px; font-family: 'Roboto Mono', monospace;"))
        dwg.add(dwg.text(text="", insert=(0, 0), fill="black", id="room-value-text", visibility="hidden",
                         style="font-size: 60px; font-family: 'Roboto Mono', monospace;"))
        dwg.save()  # Save the path to a temporary file
        floor_plan = st.fromfile(
            self.svg_path[0:-4] + '_filled_rooms_{0}.svg'.format('temperature' if is_temperature else 'co2'))
        second_svg = st.fromfile(temp_path)
        floor_plan.append(second_svg)
        floor_plan.save(output_path)
        os.remove(temp_path)

    def delete_temp_file(self, is_temperature):
        os.remove(self.svg_path[0:-4] + '_filled_rooms_{0}.svg'.format('temperature' if is_temperature else 'co2'))
