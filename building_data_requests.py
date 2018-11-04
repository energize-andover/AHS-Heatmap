# Copyright 2018 BACnet Gateway.  All rights reserved.

import requests
import json

PUBLIC_HOSTNAME = 'energize.andoverma.us'
INTERNAL_PORT = '8000'


# Request present value and units for the supplied instance
def get_value( facility, instance, gateway_hostname=None, gateway_port=None, live=False ):

    value = None
    units = None

    if str( instance ).isdigit() and int( instance ) > 0:
        # Instance appears to be valid

        # Set up request arguments
        args = {
            'facility': facility,
            'instance': instance
        }

        if live:
            args['live'] = True

        # Issue request to web service
        gateway_rsp = post_request( gateway_hostname, gateway_port, args )

        # Convert JSON response to Python dictionary
        dc_rsp = json.loads( gateway_rsp.text )

        # Extract instance response from the dictionary
        dc_inst_rsp = dc_rsp['instance_response']

        # Extract result from instance response
        if ( dc_inst_rsp['success'] ):

            dc_data = dc_inst_rsp['data']

            if dc_data['success']:
                value = dc_data['presentValue']
                units = dc_data['units']

    return value, units


# Request multiple values from BACnet Gateway
def get_bulk( bulk_request, gateway_hostname=None, gateway_port=None ):

    bulk_rsp = []

    if isinstance( bulk_request, list ) and len( bulk_request ):

        # Set up request arguments
        args = {
            'bulk': json.dumps( bulk_request )
        }

        # Issue request to web service
        gateway_rsp = post_request( gateway_hostname, gateway_port, args )

        # Extract result
        bulk_rsp = json.loads( gateway_rsp.text )

    return bulk_rsp


# Post request to web service
def post_request( gateway_hostname, gateway_port, args ):

    # Normalize hostname
    if not gateway_hostname:
        gateway_hostname = PUBLIC_HOSTNAME

    # Normalize port
    gateway_port = str( gateway_port ) if gateway_port else ''

    # Set SSL and port fragments
    if gateway_hostname == PUBLIC_HOSTNAME:

        if gateway_port:
            s = ''
            port = ':' + gateway_port
        else:
            s = 's'
            port = ''

    else:

        s = ''

        if gateway_port:
            port = ':' + gateway_port
        else:
            port = ':' + INTERNAL_PORT

    # Format URL
    url = 'http' + s + '://' + gateway_hostname + port

    # Post request
    gateway_rsp = requests.post( url, data=args )

    return gateway_rsp
