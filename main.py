from file_conversion_tools import *
from pdf_tools import *
from openCV_tools import *
from bs4 import BeautifulSoup
import pandas as pd
import os

svg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Andover HS level 3.svg")
pdf_path = svg_path[0:-4] + ".pdf"
png_path = svg_path[0:-4] + ".png"

svg_to_pdf(svg_path, pdf_path)
text_and_coords = get_text_and_coordinates(pdf_path)

svg_to_png(svg_path, png_path, 72)
initialize_cv(png_path)

# Extract the viewBox from the SVG using BeautifulSoup and convert it into a tuple of integers
soup = BeautifulSoup(open(svg_path), "html.parser")
view_box = tuple(map(int, soup.find("svg")['viewbox'].split(" ")))
media_box = get_media_box(pdf_path)


def get_svg_coords(pdf_coords, svg_view_box, pdf_media_box):
    x_coord = pdf_coords[0] * svg_view_box[2] / pdf_media_box[2]
    y_coord = svg_view_box[3] - pdf_coords[1] * svg_view_box[3] / pdf_media_box[3]
    coords = [x_coord, y_coord]
    return tuple(coords)


def get_room_pdf_coords(room):
    text = text_and_coords['text']
    global roomIndex
    roomIndex = None

    for indx, col_room in text.iteritems():
        if col_room == room or col_room.startswith(room) or col_room.endswith(room):
            roomIndex = indx

    if roomIndex is None:
        return None
    room_row = text_and_coords.iloc[roomIndex]
    return [room_row['x0'], room_row['y0'], room_row['x1'], room_row['y1']]


room_coords = [int(coord) for coord in get_room_pdf_coords('217')[:2]]
room_coords[1] = media_box[3] - room_coords[1]

get_room_corner_coords(tuple(room_coords), png_path)
