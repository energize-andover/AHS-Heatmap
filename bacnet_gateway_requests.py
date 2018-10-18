# Copyright 2018 BACnet Gateway.  All rights reserved.

import requests
import json


# Request present value and units for the supplied instance
def get_bacnet_value(facility, instance, gateway_hostname, gateway_port, live=False):
    value = None
    units = None

    if str(instance).isdigit() and int(instance) > 0:
        # Instance appears to be valid

        # Set up request arguments
        args = {
            'facility': facility,
            'instance': instance
        }

        if live:
            args['live'] = True

        # Issue request to HTTP service
        url = 'http://' + gateway_hostname + ':' + str(gateway_port)
        gateway_rsp = requests.post(url, data=args)

        # Convert JSON response to Python dictionary
        dc_rsp = json.loads(gateway_rsp.text)

        # Extract BACnet response from the dictionary
        dc_bn_rsp = dc_rsp['bacnet_response']

        # Extract result from BACnet response
        if (dc_bn_rsp['success']):

            dc_data = dc_bn_rsp['data']

            if dc_data['success']:
                value = dc_data['presentValue']
                units = dc_data['units']

    return value, units


# Request multiple values from BACnet Gateway
def get_bulk(bulk_request, gateway_hostname, gateway_port):
    bulk_rsp = []

    if isinstance(bulk_request, list) and len(bulk_request):
        # Set up request arguments
        args = {
            'bulk': json.dumps(bulk_request)
        }

        # Issue request to HTTP service
        url = 'http://' + gateway_hostname + ':' + str(gateway_port)
        gateway_rsp = requests.post(url, data=args)

        # Extract result
        bulk_rsp = json.loads(gateway_rsp.text)

    return bulk_rsp
