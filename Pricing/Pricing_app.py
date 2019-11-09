import json
import bottle
import os

from bottle import route, run, request, abort
from datetime import datetime
from bottle import response

#from Pricing_data import Pricing_data
from Pricing import Pricing_data

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

app = bottle.default_app()

@route('/', method='GET')
@enable_cors
def index():
    return "use routes to get data"

@route('/today', method='GET')
@enable_cors
def get_today_price():
    data = Pricing_data()
    req_data = data.get_today_data()
    return json.dumps(req_data.values.tolist())
    #return json.dumps(req_data.to_json())

@route('/tomorrow', method='GET')
@enable_cors
def get_tomorrow_price():
    data = Pricing_data()
    req_data= data.get_tomorrow_data()
    return json.dumps(req_data['data'].tolist())

@route('/current', method='GET')
@enable_cors
def get_current_price():
    data = Pricing_data()
    req_data = data.get_current_pricing()
    return json.dumps(req_data)

@route('/forecast', method='GET')
@enable_cors
def get_forecast_price():
    data = Pricing_data()
    req_data= data.get_forecast_pricing()
    #return json.dumps(req_data.values.tolist())
    return json.dumps(req_data)

# Run Server
run(host='localhost', port=4050)