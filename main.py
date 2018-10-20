from file_conversion_tools import *
from pdf_tools import *
from coordinate_tools import *
from bs4 import BeautifulSoup
import os
import shutil
import svgwrite
import svgutils.transform as st

# Define variables
svg_path = None
svg_output_path = None
pdf_path = None
png_path = None
text_and_coords = None
soup = None
view_box = None
media_box = None


def init():
    global svg_path, svg_output_path, pdf_path, png_path, text_and_coords, soup, view_box, media_box
    svg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Andover HS level 3.svg")
    svg_output_path = svg_path[0:-4] + "_filled_rooms.svg"
    pdf_path = svg_path[0:-4] + ".pdf"
    png_path = svg_path[0:-4] + ".png"

    if os.path.exists(svg_output_path):
        os.remove(svg_output_path)

    shutil.copy(svg_path, svg_output_path)

    svg_to_pdf(svg_path, pdf_path)
    text_and_coords = get_text_and_coordinates(pdf_path)

    svg_to_png(svg_path, png_path, 72)
    initialize_cv(png_path)

    # Extract the viewBox from the SVG using BeautifulSoup and convert it into a tuple of integers
    soup = BeautifulSoup(open(svg_path), "html.parser")
    view_box = tuple(map(int, soup.find("svg")["viewbox"].split(" ")))
    media_box = get_media_box(pdf_path)


def fill_room(room, color_hex_code, opacity):
    room_rect_info = get_room_rect_info(room, media_box, text_and_coords, png_path)

    if room_rect_info is not None:
        room_corner = (room_rect_info[0], room_rect_info[1])
        room_width = room_rect_info[2]
        room_height = room_rect_info[3]

        room_rect_svg_coords = get_svg_coords(room_corner, view_box, media_box)
        room_svg_width = get_svg_measure(room_width, view_box[2], media_box[2])
        room_svg_height = get_svg_measure(room_height, view_box[3], media_box[3])

        temp_path = svg_path[0:-4] + '_temp_rect.svg'
        dwg = svgwrite.Drawing(temp_path)
        dwg.add(dwg.rect(insert=room_rect_svg_coords, size=(room_svg_width, room_svg_height), fill=color_hex_code,
                         opacity=opacity))
        dwg.save()  # Save the path to a temporary file

        # Merge the files
        floor_plan = st.fromfile(svg_output_path)
        second_svg = st.fromfile(svg_path[0:-4] + '_temp_rect.svg')
        floor_plan.append(second_svg)
        floor_plan.save(svg_output_path)
        os.remove(temp_path)
