import requests
import json
import time

from requests.exceptions import ConnectionError


# Request present value and units for the supplied instance
def get_value_and_units(facility, instance, gateway_hostname, gateway_port):
    value = None
    units = None

    if str(instance).isdigit() and int(instance) > 0:
        # Instance appears to be valid

        # Set up request arguments
        args = {
            'facility': facility,
            'instance': instance
        }
        while True:
            try:

                # Issue request to HTTP service
                url = 'http://' + str(gateway_hostname) + ':' + str(gateway_port)
                gateway_rsp = requests.post(url, data=args)

                # Convert JSON response to Python dictionary
                dc_rsp = json.loads(gateway_rsp.text)

                # Extract BACnet response from the dictionary
                dc_bn_rsp = dc_rsp['bacnet_response']

                # Extract result from BACnet response
                if dc_bn_rsp['success']:

                    dc_data = dc_bn_rsp['data']

                    if dc_data['success']:
                        value = dc_data['presentValue']
                        units = dc_data['units']

            except ConnectionError:
                time.sleep(5)
                continue

            break

    return value, units
