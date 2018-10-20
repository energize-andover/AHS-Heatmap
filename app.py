from main import *
from data_tools import *
import os

rooms_and_sensors = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('data', 'csv', 'ahs_air.csv'))
current_facility = 'ahs'

init()
init_data_tools(rooms_and_sensors)
