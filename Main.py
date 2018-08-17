import os
import argparse
import pandas as pd
import datetime
import time
from bacnet_gateway_requests import get_value_and_units
from PyPDF2 import PdfFileReader
from FileHelpers import *

pdf_path = None
svg_path = None
png_path = None
coords_df = None
media_box = None
svg_width = None
svg_height = None
HOSTNAME = None
PORT = None
DATA_PATH = None
data = None


def init(width, height, hostname, port, data_path):
    global svg_width, svg_height, media_box, pdf_path, svg_path, png_path, coords_df, HOSTNAME, PORT, DATA_PATH

    pdf_path = os.path.join('static', 'pdf', 'Andover HS level 3.pdf')
    svg_path = os.path.join('static', 'svg', 'Andover HS level 3.svg')
    png_path = os.path.join('static', 'png', 'Andover HS level 3.png')

    coords_df = get_text_and_coordinates(pdf_path)

    svg_to_pdf(svg_path, pdf_path)

    # Gets PDF size in pts (1pt = 1/72 in) [0, 0, width, height]
    media_box = PdfFileReader(open(pdf_path, 'rb')).getPage(0).mediaBox

    svg_width = width
    svg_height = height

    svg_to_png(svg_path, png_path, svg_width, svg_height)

    HOSTNAME = hostname
    PORT = port

    DATA_PATH = data_path if data_path != 'AHS' else os.path.join('data', 'csv', 'ahs_air.csv')

    return 'Ok!'


def get_air_value_df(hostname, port, selected_room):
    df_dictionary = {
        'Date / Time': [],
        'Room': [],
        'Temperature': [],
        'Temperature Units': [],
        'CO2 Level': [],
        'CO2 Units': []
    }

    # Read spreadsheet into a DataFrame.
    # Each row contains the following:
    #   - Location
    #   - Instance ID of CO2 sensor
    #   - Instance ID of temperature sensor
    df = pd.read_csv(DATA_PATH, na_filter=False, comment='#')

    chosen_room = df['Label'] == selected_room
    filtered_room = df[chosen_room]

    for row_index, row in filtered_room.iterrows():
        # Retrieve data
        temp_value, temp_units = get_value_and_units(row['Facility'], row['Temperature'], hostname,
                                                     port)
        co2_value, co2_units = get_value_and_units(row['Facility'], row['CO2'], hostname, port)

        # Prepare to print
        temp_value = round(int(temp_value)) if temp_value else ''
        temp_units = temp_units.replace('deg ', '°') if temp_units else ''
        co2_value = round(int(co2_value)) if co2_value else ''
        co2_units = co2_units if co2_units else ''

        # Update dictionary
        df_dictionary['Date / Time'].append(datetime.datetime.now().strftime("%m/%d/%Y %H:%M"))
        df_dictionary['Room'].append(row['Label'])
        df_dictionary['Temperature'].append(temp_value)
        df_dictionary['Temperature Units'].append(temp_units)
        df_dictionary['CO2 Level'].append(co2_value)
        df_dictionary['CO2 Units'].append(co2_units)

        break

    return pd.DataFrame.from_dict(df_dictionary)


def get_all_room_data(selected_rooms, floor):
    room_data = None

    for row_index, row in selected_rooms.iterrows():
        if row['Label'] in coords_df['text'].unique() or row['Label'] in [str(floor) + text for text in
                                                                          coords_df['text'].unique()]:
            if room_data is None:
                room_data = get_air_value_df(HOSTNAME, PORT, row['Label'])
            else:
                room_data = room_data.append(get_air_value_df(HOSTNAME, PORT, row['Label']), ignore_index=True)

    return room_data


def update_with_data(temp_data):
    global data
    data = temp_data

    return 'Ok!' if data is not None else 'Error!'


def get_room_coordinates(room):

    while DATA_PATH is None:
        time.sleep(1)
        continue

    selected_row = coords_df.loc[coords_df['text'] == str(room)]

    if not selected_row.empty:
        pdf_width_pt = media_box[2]
        pdf_height_pt = media_box[3]

        width_percent = selected_row['x0'] / pdf_width_pt
        height_percent = selected_row['y0'] / pdf_height_pt

        coords = get_room_coords(png_path, [width_percent, height_percent])

        return [coords[0][0], coords[0][1], coords[1][0], coords[1][1], coords[2][0], coords[2][1], coords[3][0],
                coords[3][1]]

    return []
