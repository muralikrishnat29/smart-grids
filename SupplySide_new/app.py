import json
import bottle
import os

from bottle import route, run, request, abort
from datetime import datetime

from Wind.wind import wind
from PV.pv import pv
from Battery.Battery import Battery
from supplySide import SupplySide
from bottle import response

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

@route('/supplySideInitialise', method='POST')
@enable_cors
def supplySideInitialise():
    supply = SupplySide()
    if "wind" in request.forms:
        windData = json.loads(request.forms.get('wind'))
        for i in range(0,len(windData)):
            wind_energy = wind((int)(windData[i]["ra"]),windData[i]["city"])
            supply.addWind(wind_energy)
    else:
        wind_energy = wind(6,"Stuttgart")
        supply.addWind(wind_energy)
    if "pv" in request.forms:
        pvData = json.loads(request.forms.get('pv',None))
        for i in range(0,len(pvData)):
            solar_energy = pv((int)(pvData[i]["area"]),(int)(pvData[i]["emax"]),(int)(pvData[i]["angle"]),pvData[i]["location"])
            supply.addPV(solar_energy)
    else:
        solar_energy = pv(20,75,60,"Stuttgart")
        supply.addPV(solar_energy)
    if "battery" in request.forms:
        batteryData = json.loads(request.forms.get('battery',None))
        for i in range(0,len(batteryData)):
            battery = Battery((float)(batteryData[i]["efficiency"]),(int)(batteryData[i]["timeInterval"]),(int)(batteryData[i]["chargeSpecs"]), (int)(batteryData[i]["dischargeSpecs"]),(int)(batteryData[i]["energySpecs"]), (int)(batteryData[i]["initialEnergy"]),(float)(batteryData[i]["selfDischargeRate"]))
            supply.addBattery(battery)
    else:
        battery = Battery(0.55,1,10,5,400,0,0.2)
        supply.addBattery(battery)

@route('/windcurrentenergy', method='GET')
@enable_cors
def get_wind_current_energy():
    supply = SupplySide()
    data = supply.getCurrentWindEnergyGenerationData()
    return str(data)


@route('/pvcurrentenergy', method='GET')
@enable_cors
def get_pv_current_energy():
    supply = SupplySide()
    data = supply.getCurrentSolarEnergyGenerationData()
    return str(data)

@route('/addWind/<ra:int>/<location>/', method='GET')
@enable_cors
def addWind(ra,location):
    supply = SupplySide()
    wind_energy = wind((int)(ra),location)
    data = supply.addWind(wind_energy)
    if(data==101):
        return {"success":True}
    return {"success": False}

@route('/getWindEnergyData', method='GET')
@enable_cors
def getWindEnergyData():
    supply = SupplySide()
    wind_data = list(supply.getAllWindEnergyData())
    return json.dumps(wind_data[0:len(wind_data)-1])

@route('/getSolarEnergyData', method='GET')
@enable_cors
def getSolarEnergyData():
    supply = SupplySide()
    pv_data = list(supply.getAllSolarEnergyData())
    return json.dumps(pv_data[0:len(pv_data)-1])

@route('/addPV/<area:int>/<emax:int>/<angle:int>/<location>/', method='GET')
@enable_cors
def addPV(area,emax,angle,location):
    supply = SupplySide()
    solar_energy = pv((int)(area),(int)(emax),(int)(angle),location)
    data=supply.addPV(solar_energy)
    if(data==101):
        return {"success":True}
    return {"success": False}

@route('/addBattery/<efficiency:float>/<timeInterval:int>/<chargeSpecs:int>/<dischargeSpecs:int>/<energySpecs:int>/<initialEnergy:int>/<selfDischargeRate:float>/', method='GET')
@enable_cors
def addBattery(efficiency,timeInterval,chargeSpecs,dischargeSpecs,energySpecs,initialEnergy,selfDischargeRate):
    supply = SupplySide()
    battery = Battery((float)(efficiency),(int)(timeInterval),(int)(chargeSpecs), (int)(dischargeSpecs),(int)(energySpecs), (int)(initialEnergy),(float)(selfDischargeRate))
    data = supply.addBattery(battery)
    if(data==101):
        return {"success":True}
    return {"success": False}

@route('/totalcurrentenergy', method='GET')
@enable_cors
def get_total_current_energy():
    supply = SupplySide()
    data = supply.getCurrentEnergyGenerationData()
    return str(data)

@route('/windforecastenergy', method='GET')
@enable_cors
def get_wind_forecast_energy():
    supply = SupplySide()
    data = supply.getForecastWindEnergyGenerationData()
    return data

@route('/pvforecastenergy', method='GET')
@enable_cors
def get_pv_forecast_energy():
    supply = SupplySide()
    data = supply.getForecastSolarEnergyGenerationData()
    return data

@route('/totalforecastenergy', method='GET')
@enable_cors
def get_total_forecast_energy():
    supply = SupplySide()
    data = supply.getForecastEnergyGenerationData()
    return data

@route('/getBatteryData', method='GET')
@enable_cors
def get_battery_data():
    supply = SupplySide()
    data = supply.getCurrentBatteryData()
    return json.dumps(data)

@route('/updateBatteryData/<charge:float>/', method='GET')
@enable_cors
def update_battery_data(charge):
    supply = SupplySide()
    data = supply.updateBatteryCharge(charge)
    return json.dumps(data)

@route('/updateBatteryStates/<charge:float>/<state>/',method='GET')
@enable_cors
def update_battery_states(charge,state):
    supply = SupplySide()
    data = supply.updateBatteryStates(charge,state)
    return json.dumps(data)

@route('/updateBatteryDetails/<efficiency:float>/<timeInterval:int>/<chargeSpecs:int>/<dischargeSpecs:int>/<energySpecs:int>/<initialEnergy:int>/<selfDischargeRate:float>/', method='GET')
@enable_cors
def update_battery_data(efficiency,timeInterval, chargeSpecs, dischargeSpecs, energySpecs, initialEnergy, selfDischargeRate):
    supply = SupplySide()
    data = supply.updateBatteryData(efficiency,timeInterval,chargeSpecs,dischargeSpecs,energySpecs,initialEnergy,selfDischargeRate)
    return json.dumps(data)

@route('/history', method='GET')
@enable_cors
def get_history():
    supply = SupplySide()
    data = supply.getHistoricalEnergyData()
    return json.dumps(data)

# Run Server
if __name__ == "__main__":
    run(host="0.0.0.0", port=4000, debug=True, reloader=True)
