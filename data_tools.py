from bacnet_gateway_requests import get_bulk
import pandas as pd

cached_data = None
rooms_and_sensors = None


def init_data_tools(rooms_and_sensors_path):
    global rooms_and_sensors
    rooms_and_sensors = pd.read_csv(rooms_and_sensors_path)
