from building_data_requests import get_value, get_bulk
from main import fill_from_data, add_overlay
import pandas as pd
import numbers
import requests

current_air_data = None
rooms_and_sensors = None


def init_data_tools(rooms_and_sensors_path):
    global rooms_and_sensors
    # Read spreadsheet into a DataFrame.
    # Each row contains the following:
    #   - Label
    #   - Facility
    #   - Instance ID of CO2 sensor
    #   - Instance ID of temperature sensor
    rooms_and_sensors = pd.read_csv(rooms_and_sensors_path, na_filter=False, comment='#')
    update_air_data()


def update_air_data():
    global current_air_data
    current_air_data = get_bulk_request_df()
    current_air_data['temperature'] = pd.to_numeric(current_air_data['temperature'], errors='coerce')
    current_air_data['co2'] = pd.to_numeric(current_air_data['co2'], errors='coerce')


def get_request_df(room):
    row = rooms_and_sensors[rooms_and_sensors['Label'] == str(room)]

    if not row.empty:
        try:
            temp_value, temp_units = get_value(row['Facility'].iloc[0], row['Temperature'].iloc[0], True)
            co2_value, co2_units = get_value(row['Facility'].iloc[0], row['CO2'].iloc[0], True)
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Unable to get data. Are you connected to the right WiFi network?")
        # Prepare to print
        temp_value = int(temp_value) if temp_value else ''
        temp_units = temp_units if temp_units else ''
        co2_value = int(co2_value) if co2_value else ''
        co2_units = co2_units if co2_units else ''

        df_dictionary = {
            'room': [room if temp_value and temp_units else ''],
            # If there's no data, leave the dictionary empty so the failsafe below catches it
            'temperature': [temp_value],
            'temperature units': [temp_units],
            'co2': [co2_value],
            'co2 units': [co2_units]
        }

        if not df_dictionary:
            return None

        return pd.DataFrame.from_dict(df_dictionary)
    else:
        return None


def get_bulk_request_df():
    bulk_rq = []

    # Iterate over the rows of the dataframe, adding elements to the bulk request
    for index, row in rooms_and_sensors.iterrows():

        # Append facility/instance pairs to bulk request
        if row['Temperature']:
            bulk_rq.append({'facility': row['Facility'], 'instance': row['Temperature']})
        if row['CO2']:
            bulk_rq.append({'facility': row['Facility'], 'instance': row['CO2']})

    # Issue get-bulk request
    try:
        bulk_rsp = get_bulk(bulk_rq)
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Unable to get data from. Are you connected to the right WiFi network?")

    # Extract map from get-bulk response
    map = bulk_rsp['rsp_map']

    df_dictionary = {
        'room': [],
        'temperature': [],
        'temperature units': [],
        'co2': [],
        'co2 units': []
    }

    # Iterate over the rows of the DataFrame, displaying temperature and CO2 values extracted from map
    for index, row in rooms_and_sensors.iterrows():

        # Initialize empty display values
        temp_value = ''
        temp_units = ''
        co2_value = ''
        co2_units = ''

        # Get facility of current row
        facility = row['Facility']

        # Try to extract current row's temperature and CO2 values from map
        if facility in map:

            instance = str(row['Temperature'])
            if instance and (instance in map[facility]):
                rsp = map[facility][instance]
                property = rsp['property']
                temp_value = int(rsp[property]) if isinstance(rsp[property], numbers.Number) else ''
                temp_units = rsp['units']

            instance = str(row['CO2'])
            if instance and (instance in map[facility]):
                rsp = map[facility][instance]
                property = rsp['property']
                co2_value = int(rsp[property]) if isinstance(rsp[property], numbers.Number) else ''
                co2_units = rsp['units']

        # Output CSV format
        df_dictionary['room'].append(row['Label'])
        df_dictionary['temperature'].append(temp_value)
        df_dictionary['temperature units'].append(temp_units)
        df_dictionary['co2'].append(co2_value)
        df_dictionary['co2 units'].append(co2_units)

    return pd.DataFrame.from_dict(df_dictionary)


def get_room_data(room):
    return current_air_data[current_air_data['room'] == room] if current_air_data is not None else None


def get_room_row_index(room):
    for indx, row in current_air_data.iterrows():
        if row['room'] == room or row['room'] == str(room):
            return indx

    return None


def get_new_room_data(room):
    global current_air_data
    # Pull some new data from the BACnet, and replace the old data in current_air_data with it
    room_data = get_request_df(room)

    if room_data is not None:
        current_data_room_index = get_room_row_index(room)

        if current_data_room_index is not None:
            current_air_data.at[current_data_room_index, 'temperature'] = room_data['temperature'].iloc[0]
            current_air_data.at[current_data_room_index, 'temperature units'] = room_data['temperature units'].iloc[0]
            current_air_data.at[current_data_room_index, 'co2'] = room_data['co2'].iloc[0]
            current_air_data.at[current_data_room_index, 'co2 units'] = room_data['co2 units'].iloc[0]

        return room_data
    else:
        return None


def fill_all_rooms(is_temperature_value):
    for indx, row in current_air_data.iterrows():
        fill_from_data(row, is_temperature_value)

    add_overlay(is_temperature_value)
