import json
import bottle
import os

from bottle import route, run, request, abort, response
from datetime import datetime

from DataAccessLayer.Weather_Data_Access import Weather_Data_Access

def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

@route('/', method='GET')
@enable_cors
def index():
    return "use routes to get data"

@route('/wind', method='GET')
@enable_cors
def get_wind_parameters():
    data = Weather_Data_Access()
    req_data = data.get_wind_parameters()
    return json.dumps(req_data)


@route('/windforecast', method='GET')
@enable_cors
def get_wind_forecast_values():
    data = Weather_Data_Access()
    req_data= data.get_wind_forecast()
    return json.dumps(req_data)

@route('/PV', method='GET')
@enable_cors
def get_pv_parameters():
    data = Weather_Data_Access()
    req_data = data.get_PV_Parameters()
    return json.dumps(req_data)

@route('/PVforecast', method='GET')
@enable_cors
def get_PV_forecast_values():
    data = Weather_Data_Access()
    req_data= data.get_PV_forecast()
    return json.dumps(req_data)

# Run Server
run(host='localhost', port=5000)