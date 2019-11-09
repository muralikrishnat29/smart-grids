import json
import os
import requests
import bottle

from bottle import route, run, request, abort
from datetime import datetime
from bottle import response

#from Demand Side import class
from DemandSide_latest import DemandSide

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
def index():
    return "use routes to get data"

@route('/demandSideInitialise', method='POST')
@enable_cors
def demandSideInitialise():
    demand = DemandSide()
    buildingId=0
    if "building" in request.forms:
        building = json.loads(request.forms.get('building'))
        buildingId = demand.addBuilding(building["name"])           
    else:
        buildingId = demand.addBuilding("defaultDevice")
    if "devices" in request.forms:
        deviceList = json.loads(request.forms.get('devices'))
        for i in range(0,len(deviceList)):
            demand.addDevice((int)(deviceList[i]["est"]),(int)(deviceList[i]["let"]),(float)(deviceList[i]["E"]),(int)(deviceList[i]["lot"]),deviceList[i]["name"],(int)(deviceList[i]["buildingId"]))
    
@route('/addDevice/<est:int>/<let:int>/<E:float>/<lot:int>/<name>/<startTime:int>/<endTime:int>/<buildingId:int>/', method='GET')
@enable_cors
def addDevice(est,let,E,lot,name,startTime,endTime,buildingId):
    data = DemandSide()
    deviceId = data.addDevice(est,let,E,lot,name,startTime,endTime,buildingId)
    if(deviceId>0):
        return json.dumps({
            "success":True
        })
    return json.dumps({
        "success":False
    })
    
@route('/addBuilding/<name>/', method='GET')
@enable_cors
def addBuilding(name):
    data = DemandSide()
    buildingId = data.addBuilding(name)
    if(buildingId>0):
        return json.dumps({
            "success":True
        })
    return json.dumps({
        "success":False
    })
    
@route('/buildings', method='GET')
@enable_cors
def get_building_list():
    data = DemandSide()
    req_data = data.getBuildingsBasedOnDemandSideId(data.DemandSideId)
    return json.dumps([dict(r) for r in req_data])

@route('/getAllDevices', method='GET')
@enable_cors
def get_devices_building_list():
    data = DemandSide()
    final_data={}
    building_data = data.getBuildingsBasedOnDemandSideId(data.DemandSideId)
    all_buildings = [dict(r) for r in building_data]
    for i in range(0,len(all_buildings)):
        final_data.update({all_buildings[i]['BuildingName']:{}})
        final_device_data = get_device_for_building(all_buildings[i]['Id'])
        final_data[all_buildings[i]['BuildingName']] = final_device_data
    return json.dumps(final_data)
        
def get_device_for_building(buildingId):
    data = DemandSide()
    final_device_data={}
    device_data = data.getCustomDevicesBasedOnBuildingId(buildingId)
    all_devices = [dict(r) for r in device_data]
    final_data={}
    for i in range(0,len(all_devices)):
        final_data.update({all_devices[i]['DeviceName']:{'Id':all_devices[i]['Id'],'EST':all_devices[i]['EST'],'LET':all_devices[i]['LET'],'LOT':all_devices[i]['LOT'],'E':all_devices[i]['Power']}})
    return final_data
        
@route('/devices/<buildingId:int>', method='GET')
@enable_cors
def get_devices_list(buildingId):
	data=DemandSide()
	req_data=data.getDevicesBasedOnBuildingId(buildingId)
	return json.dumps(req_data)


@route('/building/<buildingId:int>', method='GET')
@enable_cors
def get_building(buildingId):
	data=DemandSide()
	req_data=data.getBuildingBasedOnBuildingId(buildingId)
	return json.dumps([dict(r) for r in req_data])


@route('/updateStartStopTimeDevice/<StartTime:int>/<EndTime:int>/<deviceId:int>/', method='GET')
@enable_cors
def updateStartStopTimeDevice(StartTime, EndTime, deviceId):
    data=DemandSide()
    req_data = data.updateStartStopTimeDevice(StartTime,EndTime,deviceId)
    if(req_data is not None):
        return json.dumps({
            "success":True
        })
    return json.dumps({
            "success":False
        })
# Run Server
if __name__ == "__main__":
    run(host="0.0.0.0", port=5050, debug=True, reloader=True)    
