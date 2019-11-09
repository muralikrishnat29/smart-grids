from __future__ import print_function
import json
import bottle
import os
import requests
import sqlite3
from datetime import datetime
import numpy as np
from bottle import route, run, request, abort
from datetime import datetime
from bottle import response
from gurobipy import *




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

def convertArrayToString(strArray):
        #print("hello",strArray)
        stringData = json.dumps(np.around(strArray,decimals=2).tolist())
        return stringData
    

def convertArrayToString(strArray):
        #print("hello",strArray)
        stringData = json.dumps(np.around(strArray,decimals=2).tolist())
        return stringData

# Build optimization model
# INPUT:
# pv_out and wind_out from Supply_Side
# tariff from Pricing
# demand from Demand_Side
# OUTPUT:
# CED schedule
# Profit of stakeholder
# Bill of houses
# Battery status and energy_level
@route('/optimize', method='GET')
@enable_cors    
def set_model():
    fname = 'opti-config.json'
        #for Supply Side
    config=None
    with open(fname) as config_file:
        config = json.load(config_file)
    supply_side_url = (config)['config_data']['supply_url']
    tariff_url = (config)['config_data']['pricing_url']
    demand_url = (config)['config_data']['demand_url']  

    
    #Variables for optimization model
    users = ['User1','User2']
    
    demand = (requests.get(demand_url+"buildings")).json()
    data=[]
    for i in range(0,len(demand)):
        data.append(json.loads(demand[i]['UDConsumption']))    
    data_new = [i * 0.1 for i in data[0]]
    
    UD = {'User1':data_new,
         'User2':data_new}
    
    CED = (requests.get(demand_url+"getAllDevices")).json()
    
    
    
    devices1 = list(CED['User1'].keys())
    devices2 = list(CED['User2'].keys())
    

    '''SETS'''
    '''wind turbine and solar field'''
    plants = ['wind', 'pv']

    '''optimization horizon: 24 hours, 1 hour resolution'''
    time_steps = range(0,24)

    '''PARAMETERS'''
    '''the output of the solar field and wind turbine are known, assuming a perfect forecast kW'''
    wind_out = (requests.get(supply_side_url+"windforecastenergy")).json()
    pv_out = (requests.get(supply_side_url+"pvforecastenergy")).json()
    #convert W to kW
    wind_out = [i * 0.001 for i in wind_out]
    pv_out = [i * 0.001 for i in pv_out]

    '''technical characteristics and limits of power plants kW'''
    plants_char = { 'wind': {'p_min': min(wind_out), 'p_max': wind_out},
                'pv': {'p_min': 0, 'p_max': pv_out}}

    '''generation prce of power plants ct/kWh'''
    price = {'wind': 1, 'pv': 2}

    '''minimum and maximum exchangable power with the main grid. + means we import power from the main, - means we export power to the main grid'''
    grid = { 'p_min': -200, 'p_max': 200}

    '''Users tariff'''
    tariff = (requests.get(tariff_url+"forecast")).json()
    #change from MWh to KWh, and euro to cent
    tariff = [i * 0.1 for i in tariff]
 
    '''setup model'''
    model = Model('Optimal Scheduling')

    '''add variables'''
    p_gen = model.addVars(plants, time_steps, lb = 0, vtype=GRB.CONTINUOUS, name="pow_gen") # generated power from plants
    p_grid = model.addVars(time_steps, lb = -GRB.INFINITY, vtype=GRB.CONTINUOUS, name="exch_pow") # power exchanged with the main grid >0 if import <0 if export

    tot_d = model.addVars(users, time_steps, lb = 0, vtype=GRB.CONTINUOUS, name="total_demand") # total demand
    
    #need for loop for this
    status1 = model.addVars(devices1, time_steps, vtype=GRB.BINARY, name="Dev_status_user1") # status of devices of user1
    st_start1 = model.addVars(devices1, time_steps, vtype=GRB.BINARY, name="start_status_user1")
    st_end1 = model.addVars(devices1, time_steps, vtype=GRB.BINARY, name="end_status_user1")

    status2 = model.addVars(devices2, time_steps, vtype=GRB.BINARY, name="Dev_status_user2") # status of devices of user1
    st_start2 = model.addVars(devices2, time_steps, vtype=GRB.BINARY, name="start_status_user2")
    st_end2 = model.addVars(devices2, time_steps, vtype=GRB.BINARY, name="end_status_user2")

    '''add constraints'''
    '''balance'''
    model.addConstrs((quicksum(p_gen[pp,t] for pp in plants) - quicksum(tot_d[u,t] for u in users) + p_grid[t] == 0 for t in time_steps),name='balance')

    '''generation limit'''
    model.addConstrs((p_gen['wind',t] == plants_char['wind']['p_max'][t] for t in time_steps), name='P1output')
    model.addConstrs((p_gen['pv',t] == plants_char['pv']['p_max'][t] for t in time_steps), name='P2output')


    '''grid exchange'''
    model.addConstrs((p_grid[t] >= grid['p_min'] for t in time_steps), name='gridmin')
    model.addConstrs((p_grid[t] <= grid['p_max'] for t in time_steps), name='gridmax')

    '''DEMAND SIDE'''
  
    model.addConstrs((tot_d['User1',t] == UD['User1'][t] + quicksum(CED['User1'][d]['E']*status1[d,t] for d in devices1) for t in time_steps), name='U1totd')

    '''device start and end'''
    model.addConstrs((quicksum(st_start1[d,t] for t in time_steps if t >= CED['User1'][d]['EST'] or t <= CED['User1'][d]['LET']-CED['User1'][d]['LOT']) == 1 for d in devices1))
    model.addConstrs((quicksum(st_end1[d,t] for t in time_steps if t <= CED['User1'][d]['LET'] or t >= CED['User1'][d]['EST']+CED['User1'][d]['LOT']) == 1 for d in devices1))
    model.addConstrs((st_start1[d,t] ==0 for d in devices1 for t in time_steps if t < CED['User1'][d]['EST'] or t > CED['User1'][d]['LET']-CED['User1'][d]['LOT']))
    model.addConstrs((st_end1[d,t] ==0 for d in devices1 for t in time_steps if t < CED['User1'][d]['EST']+CED['User1'][d]['LOT'] or t > CED['User1'][d]['LET']))
    model.addConstrs((st_end1[d,t] == st_start1[d,t-CED['User1'][d]['LOT']] for d in devices1 for t in time_steps if t>= CED['User1'][d]['LOT']))

    '''device status'''
    model.addConstrs((quicksum(status1[d,t] for t in time_steps if t >= CED['User1'][d]['EST'] or t <= CED['User1'][d]['LET']) == CED['User1'][d]['LOT'] for d in devices1))
    model.addConstrs((status1[d,t] ==0 for d in devices1 for t in time_steps if t < CED['User1'][d]['EST'] or t > CED['User1'][d]['LET']))
    model.addConstrs((quicksum(status1[d,tau] for tau in range(t)) >= CED['User1'][d]['LOT']*st_end1[d,t] for d in devices1 for t in time_steps))
    model.addConstrs((quicksum(st_start1[d,tau] for tau in range(t+1)) >= status1[d,t] for d in devices1 for t in time_steps))

    '''DEMAND SIDE-User2'''
    '''total demand'''
    model.addConstrs((tot_d['User2',t] == UD['User2'][t] + quicksum(CED['User2'][d]['E']*status2[d,t] for d in devices2) for t in time_steps), name='U2totd')

    '''device start and end'''
    model.addConstrs((quicksum(st_start2[d,t] for t in time_steps if t >= CED['User2'][d]['EST'] or t <= CED['User2'][d]['LET']-CED['User2'][d]['LOT']) == 1 for d in devices2))
    model.addConstrs((quicksum(st_end2[d,t] for t in time_steps if t <= CED['User2'][d]['LET'] or t >= CED['User2'][d]['EST']+CED['User2'][d]['LOT']) == 1 for d in devices2))
    model.addConstrs((st_start2[d,t] ==0 for d in devices2 for t in time_steps if t < CED['User2'][d]['EST'] or t > CED['User2'][d]['LET']-CED['User2'][d]['LOT']))
    model.addConstrs((st_end2[d,t] ==0 for d in devices2 for t in time_steps if t < CED['User2'][d]['EST']+CED['User2'][d]['LOT'] or t > CED['User2'][d]['LET']))
    model.addConstrs((st_end2[d,t] == st_start2[d,t-CED['User2'][d]['LOT']] for d in devices2 for t in time_steps if t>= CED['User2'][d]['LOT']))

    '''device status'''
    model.addConstrs((quicksum(status2[d,t] for t in time_steps if t >= CED['User2'][d]['EST'] or t <= CED['User2'][d]['LET']) == CED['User2'][d]['LOT'] for d in devices2))
    model.addConstrs((status2[d,t] ==0 for d in devices2 for t in time_steps if t < CED['User2'][d]['EST'] or t > CED['User2'][d]['LET']))
    model.addConstrs((quicksum(status2[d,tau] for tau in range(t)) >= CED['User2'][d]['LOT']*st_end2[d,t] for d in devices2 for t in time_steps))
    model.addConstrs((quicksum(st_start2[d,tau] for tau in range(t+1)) >= status2[d,t] for d in devices2 for t in time_steps))

    '''OBJECTIVE'''
    #Minimize the users' bill
    #obj1 = quicksum(tariff[u][t]*tot_d[u,t]*1/100 for u in users for t in time_steps) #euro
    #model.setObjective(obj1, GRB.MINIMIZE)
    
    #Maximize stakeholer's profit
    obj2 = (quicksum(tariff[t]*tot_d[u,t]*1/100 for u in users for t in time_steps) - quicksum(price[pp]*p_gen[pp,t]*1/100 for pp in plants for t in time_steps))

    model.setObjective(obj2, GRB.MAXIMIZE)

    model.optimize()
    try:
        '''OUTPUT'''
        #Output data
        data = {'data':[{users[0]:{'schedule':[],'bill':0}},{users[1]:{'schedule':[],'bill':0}}],'profit': 0, 'battery_state':[],'battery_energy':[]}
     
        revenue1 = sum(price['wind']*p_gen['wind',t].X*1/100 for t in time_steps)
        revenue2 = sum(price['pv']*p_gen['pv',t].X*1/100 for t in time_steps)
    
    
        data['data'][0]['User1']['bill'] = sum(tariff[t]*tot_d['User1',t].X*1/100 for t in time_steps)
        for d in devices1:
            data['data'][0]['User1']['schedule'].append({d:[[t for t in time_steps if st_start1[d,t].X ==1][0],[t for t in time_steps if st_end1[d,t].X ==1][0]]}) 
            #Update start and end time for CED
            (requests.get(demand_url+'/updateStartStopTimeDevice/%d/%d/%d/'%(data['data'][0]['User1']['schedule'][0][u][0],data['data'][0]['User1']['schedule'][0][u][1],))).json()
            
        data['data'][1]['User2']['bill'] = sum(tariff[t]*tot_d['User2',t].X*1/100 for t in time_steps)
        for d in devices2:
            data['data'][1]['User2']['schedule'].append({d:[[t for t in time_steps if st_start2[d,t].X ==1][0],[t for t in time_steps if st_end2[d,t].X ==1][0]]}) 
            #Update start and end time for CED
            (requests.get(demand_url+'/updateStartStopTimeDevice/%d/%d/%d/'%(data['data'][0]['User2']['schedule'][0][u][0],data['data'][0]['User1']['schedule'][0][u][1],))).json()
   
        #get battery data
        battery_data = (requests.get(supply_side_url+"getBatteryData")).json()
        eff = battery_data[0]['efficiency']
        E_self = battery_data[0]['self_discharge_rate']
        E_ch = battery_data[0]['charge_specs']
        E_dch = battery_data[0]['discharge_specs']
        E_spec = battery_data[0]['energy_specs']
    
        exch_bat = []
        energy_level = []
        grid_bat = []
        bat_state = []
    
        for i in time_steps:
            if  E_ch >= p_grid[i].X >= -E_dch:
                exch_bat.append(p_grid[i].X)
            else:
                exch_bat.append(0)
        
        energy_level.append(0)
        for i in time_steps:
            if E_spec >= energy_level[i] - (eff)**np.sign(-exch_bat[i])*exch_bat[i] - E_self >= 0:
                energy_level.append(energy_level[i] - (eff)**np.sign(-exch_bat[i])*exch_bat[i] - E_self)
            else:
                if energy_level[i]- E_self >=0:
                    energy_level.append(energy_level[i]- E_self)
                    exch_bat[i]=0
                else:
                    energy_level.append(energy_level[i])
                    exch_bat[i]=0
        
            for i in time_steps:
                grid_bat.append(p_grid[i].X - exch_bat[i]) 
    
        energy_level.pop()
        exch_bat[-1] = abs(- (eff)**np.sign(-exch_bat[-2])*exch_bat[-2] - E_self)
    
        for i in time_steps:
            if exch_bat[i]>0:
                bat_state.append('discharge') 
            elif exch_bat[i]<0:
                bat_state.append('charge') 
            else:
                bat_state.append('idle')
   
    
        #get current hour
        key = datetime.now().hour
        #Update battery data
        #(requests.get(demand_url+'/updateBatteryData/%.02/%s/'%(energy_level[key],battery_state[key]))).json()
        data['battery_state'] = bat_state
        data['battery_energy'] = convertArrayToString(energy_level)
        #Re-calculate profit
    
        profit = sum((np.array(pv_out)+np.array(wind_out))*np.array(tariff)-revenue1-revenue2)*0.9
        data['profit'] = profit
    
        return json.dumps(data)
    except:
        data = None
        return json.dumps(data)

@route('/sample', method='GET')
@enable_cors
def sample_output():
    data = {
    "data": [
    {   
        "Building1": {
        "Schedule":[
            {"Washing Machine":[9,11]},
            {"Dish washer":[9,11]}
        ],
        "Profit": 4.2,
        "Bill":45.0
        }
    },
    {
        "Building2": {
        "Schedule":[
            {"Dryer":[9,11]},
            {"Device2":[9,11]}
        ],
        "Profit": 6.2,
        "Bill":55.0
        }
    }
]
}
    return json.dumps(data)
# Run Server
if __name__ == "__main__":
    run(host="0.0.0.0", port=4070, debug=True, reloader=True)