import json
import bottle
import os
import numpy
import sqlite3
import random
import sqlalchemy as db
from sqlalchemy.orm import load_only

from bottle import route, run, request, abort
from datetime import datetime

from Building.DemandProfile import DemandProfile
from Building.Device import Device
from Building.Building import Building

class DemandSide:
    def __init__(self):
        self.db_path = "demand_side_data.db"
        self.schema_path = "demand_side_data.sql"
        #self.SELECT_QUERY_DEVICE = "SELECT Id, Building, DemandSide, DeviceName, EST, LET, LOT, Power(kW), StartTime(h), EndTime(h), DeviceStatus, Power_total(kW) FROM DeviceModules"
        #self.SELECT_QUERY_BUILDING = "SELECT Id, DemandSide, CED_Count, CED_List, CEDConsumption, UDConsumption, TotalDemand FROM Building"
        #self.INSERT_QUERY_DEVICE = "INSERT INTO DeviceModules (Id, Building, DemandSide, DeviceName, EST, LET, LOT, Power(kW), StartTime(h), EndTime(h), DeviceStatus, Power_total(kW)) VALUES ("
        #self.INSERT_QUERY_BUILDING = "INSERT INTO Building (Id, DemandSide, CED_Count, CED_List, CEDConsumption, UDConsumption, TotalDemand) VALUES ("
        #self.DELETE_QUERY_DEVICE = "DELETE FROM DeviceModules"
        #self.DELETE_QUERY_BUILDING = "DELETE FROM Building"
        self.DemandSideId = 0
        self.devices = []
        self.buildings = []
        self.uncontrolled = []
        if(not self.check_db_existence()):
            self.create_db_schema()
            self.addDemandSide()
            self.update_last_update_time(initial=True)
        else:
            demandSide = self.get_all_data_from_table('DemandSide')
            if(len(demandSide)>0):
                self.DemandSideId = demandSide[0][0]
                print(self.DemandSideId)
            else:
                self.DemandSideId = self.addDemandSide()
    
    def check_db_existence(self):
        db_exists = os.path.exists(self.db_path)
        return db_exists

    def create_db_schema(self):
        with sqlite3.connect(self.db_path) as conn:
            with open(self.schema_path, 'rt') as file:
                schema = file.read()
            conn.executescript(schema)

    def get_last_update_time(self):
        engine = db.create_engine('sqlite:///'+self.db_path)
        connection = engine.connect()
        metadata = db.MetaData()
        last_update = db.Table('LastUpdate', metadata, autoload=True, autoload_with=engine)
        query = db.select([last_update])
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        return ResultSet[0][1]

    def get_all_data_from_table(self, table):
        engine = db.create_engine('sqlite:///'+self.db_path)
        connection = engine.connect()
        metadata = db.MetaData()
        object = db.Table(table, metadata, autoload=True, autoload_with=engine)
        query = db.select([object])
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        return ResultSet

    def insert_given_data(self, table, values):
        engine = db.create_engine('sqlite:///'+self.db_path)
        connection = engine.connect()
        metadata = db.MetaData()
        object = db.Table(table, metadata, autoload=True, autoload_with=engine)
        insert_query = db.insert(object)
        insert_result = connection.execute(insert_query, values)
        inserted_id = insert_result.inserted_primary_key[0]
        return inserted_id
    
    def delete_all_data(self, table):
        engine = db.create_engine('sqlite:///'+self.db_path)
        connection = engine.connect()
        metadata = db.MetaData()
        object = db.Table(table, metadata, autoload=True, autoload_with=engine)
        delete_query = db.delete(object)
        delete_result = connection.execute(delete_query)

    '''def execute_query_select(self, table, query_type, values= None):
        engine = db.create_engine('sqlite:///'+self.db_path)
        connection = engine.connect()
        metadata = db.MetaData()
        object = db.Table(table, metadata, autoload=True, autoload_with=engine)
        if(query_type=='SELECT'):
            query = db.select([object])'''

    def is_data_latest(self):
        current_hour = datetime.now().hour
        last_update_time = self.get_last_update_time()
        print("last update time:"+str(last_update_time))
        if(not last_update_time is None):
            last_update_hour = datetime.strptime(last_update_time, '%b %d, %Y %H:%M:%S').hour
            if(current_hour == last_update_hour):
                return True
            return False
        return False

    def addDemandSide(self):
        #Create and Add devices to db [Using addDevice method] and add those devices to building using building class
        randomNumber = random.randint(1,1000)
        description = "DemandSide"+str(randomNumber)
        if(len(self.get_all_data_from_table('DemandSide'))>0):
            #delete_existing_query = delete_existing_query.where(emp.columns.salary < 100000)
            self.delete_all_data('DeviceModules')
            self.delete_all_data('Building')
            self.delete_all_data('DemandSide')
        values = [{'Id':str(randomNumber), 'Description':description}]
        #insert_query = db.insert(DemandSide).values(Id=str(randomNumber),Description=description)
        #insert_result = connection.execute(insert_query)
        self.DemandSideId = self.insert_given_data('DemandSide',values)
        return self.DemandSideId

    def getDevicesBasedOnBuildingId(self,buildingId):
        engine = db.create_engine('sqlite:///'+self.db_path)
        connection = engine.connect()
        metadata = db.MetaData()
        deviceModules = db.Table('DeviceModules', metadata, autoload=True, autoload_with=engine)
        query = db.select([deviceModules]).where(deviceModules.columns.Building == buildingId)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        result = []
        for row in ResultSet:
            device = {
                'Id':str(row[0]),
                'Building':str(int(row[1])),
                'DemandSide':str(int(row[2])),
                'DeviceName':str(row[3]),
                'EST':str(row[4]),
                'LET':str(row[5]),
                'LOT':str(row[6]),
                'Power':str(row[7]),
                'StartTime':str(row[8]),
                'EndTime':str(row[9]),
                'DeviceStatus':str(row[10]),
                'Power_total':row[11],
                'Power_sum':row[12]
                }
            result.append(device)
            #append building name write function getbuildingname based on building id
        #print(type(ResultSet[0][0]))
        return result
    
    def getCustomDevicesBasedOnBuildingId(self,buildingId):
        engine = db.create_engine('sqlite:///'+self.db_path)
        connection = engine.connect()
        metadata = db.MetaData()
        deviceModules = db.Table('DeviceModules', metadata, autoload=True, autoload_with=engine)
        query = db.select([deviceModules]).where(deviceModules.columns.Building == buildingId)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        result = []
        for row in ResultSet:
            device = {
                'Id':str(row[0]),
                'Building':str(int(row[1])),
                'DemandSide':str(int(row[2])),
                'DeviceName':str(row[3]),
                'EST':row[4],
                'LET':row[5],
                'LOT':row[6],
                'Power':row[7],
                'StartTime':str(row[8]),
                'EndTime':str(row[9]),
                'DeviceStatus':str(row[10]),
                'Power_total':row[11],
                'Power_sum':row[12]
                }
            result.append(device)
            #append building name write function getbuildingname based on building id
        #print(type(ResultSet[0][0]))
        return result
    
    def getDevicesBasedOnDeviceId(self,deviceId):
        engine = db.create_engine('sqlite:///'+self.db_path)
        connection = engine.connect()
        metadata = db.MetaData()
        deviceModules = db.Table('DeviceModules', metadata, autoload=True, autoload_with=engine)
        query = db.select([deviceModules]).where(deviceModules.columns.Id == deviceId)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        result = []
        for row in ResultSet:
            device = {
                'Id':str(row[0]),
                'Building':str(int(row[1])),
                'DemandSide':str(int(row[2])),
                'DeviceName':str(row[3]),
                'EST':str(row[4]),
                'LET':str(row[5]),
                'LOT':str(row[6]),
                'Power':str(row[7]),
                'StartTime':str(row[8]),
                'EndTime':str(row[9]),
                'DeviceStatus':str(row[10]),
                'Power_total':row[11],
                'Power_sum':row[12]
                }
            result.append(device)
            #append building name write function getbuildingname based on building id
        #print(type(ResultSet[0][0]))
        return result

    def getBuildingBasedOnBuildingId(self,buildingId):
        engine = db.create_engine('sqlite:///'+self.db_path)
        connection = engine.connect()
        metadata = db.MetaData()
        buildings = db.Table('Building', metadata, autoload=True, autoload_with=engine)
        query = db.select([buildings]).where(buildings.columns.Id == buildingId)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        #print("based on building id")
        #print(ResultSet)
        return ResultSet
    
    def getBuildingsBasedOnDemandSideId(self,demandSideId):
        engine = db.create_engine('sqlite:///'+self.db_path)
        connection = engine.connect()
        metadata = db.MetaData()
        buildings = db.Table('Building', metadata, autoload=True, autoload_with=engine)
        query = db.select([buildings]).where(buildings.columns.DemandSide == demandSideId)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        return ResultSet

    def updateBuildingData(self, buildingId):
        building = Building()
        building_in_db = self.getBuildingBasedOnBuildingId(buildingId)
        devices_in_db = self.getDevicesBasedOnBuildingId(buildingId)
        for device in devices_in_db:
            unlinked_device = Device(int(device[4]),int(device[5]), int(device[7]), int(device[6]),device[3])
            building.device_add(unlinked_device.name,unlinked_device.energy_cal())
        total_energy = building.total_energy_cal()
        engine = db.create_engine('sqlite:///'+self.db_path)
        connection = engine.connect()
        metadata = db.MetaData()
        buildings = db.Table('Building', metadata, autoload=True, autoload_with=engine)
        query = db.update(buildings).values(TotalDemand=self.convertArrayToString(total_energy))
        query = query.where(buildings.columns.Id == 1)
        ResultProxy = connection.execute(query)
        return ResultProxy
    
    def addBuilding(self, name):
        building = Building()
        e_ud=building.energy_uncontrol()
        ced_energy=numpy.zeros(24)
        device_energy=numpy.zeros(24)
        ced_list=[]
        values = [{'DemandSide':str(self.DemandSideId), 'BuildingName':str(name),'CED_Count':0, 'CED_List':str('[]'),'CEDConsumption':self.convertArrayToString([]) , 'UDConsumption': self.convertArrayToString(e_ud), 'TotalDemand': self.convertArrayToString([])}]
        buildingId = self.insert_given_data('Building',values)
        return buildingId

    def addBuildingWithDevices(self, name, devices):
        building = Building()
        e_ud=building.energy_uncontrol()
        ced_energy=numpy.zeros(24)
        device_energy=numpy.zeros(24)
        ced_list=[]
        DeviceList={"Device1":[9,18,1.3,2],"Device2":[9,18,1.3,2]}
        values = [{'Name':name,'DemandSide':str(self.DemandSideId), 'BuildingName':str(name),'CED_Count':str(len(DeviceList)), 'CED_List':str(ced_list),'CEDConsumption':self.convertArrayToString([]) , 'UDConsumption': self.convertArrayToString(e_ud), 'TotalDemand': self.convertArrayToString([])}]
        buildingId = self.insert_given_data('Building',values)
        for the_key, the_value in DeviceList.items():
            device_energy=self.addDevicetoBuilding(the_key,the_value,buildingId)
            building.device_add(the_key, device_energy)
            ced_energy=numpy.add(device_energy,ced_energy)
            ced_list.append(str(the_key))
        #print(ced_list)
        total_energy = building.total_energy_cal()
        values = {'CEDConsumption': self.convertArrayToString(total_energy), 'UDConsumption': self.convertArrayToString(e_ud), 'TotalDemand':self.convertArrayToString(total_energy), 'CED_Count':len(DeviceList),'CED_List':str(ced_list)}
        update_result = self.updateBuildingEnergyData(0, buildingId)#update  returniing none
        if(update_result is None):
            #print(update_result)
            return -22
        return buildingId

    def updateBuildingEnergyData(self, deviceId=0,buildingId=0):
        try:
            building = Building()
            e_ud=building.energy_uncontrol()
            ced_energy=numpy.zeros(24)
            device_energy=numpy.zeros(24)
            if(buildingId ==0):
                deviceToGetBuildingId = [dict(r) for r in self.getDevicesBasedOnDeviceId(deviceId)]
                buildingId=deviceToGetBuildingId[0]['Building']
            deviceResultSet = self.getDevicesBasedOnBuildingId(buildingId)
            deviceDict = [dict(r) for r in deviceResultSet]
            ced_list=[]
            for i in deviceDict:
                print("qFF",int(i['StartTime']), int(i['EndTime']))
                deviceTemp = Device(int(i['EST']),int(i['LET']),float(i['Power']),int(i['LOT']),i['DeviceName'])
                device_energy = deviceTemp.energy_cal(int(i['StartTime']), int(i['EndTime']))
                print("qq",device_energy)
                device_total = deviceTemp.energy_total()
                print("qy",device_energy)
                building.device_add(i['DeviceName'], device_energy)
                deviceValuesToUpdate = {'Power_total(kW)':self.convertArrayToString(device_energy),'Power_sum(kW)':str(device_total)}
                deviceUpdateResult = self.updateDeviceEnergyData(deviceValuesToUpdate, i['Id'])
                ced_energy=numpy.add(device_energy,ced_energy)
                ced_list.append(i['DeviceName'])
            total_energy = building.total_energy_cal()
            print("11",total_energy)
            values = {'DemandSide':str(self.DemandSideId), 'CED_Count':str(len(ced_list)), 'CED_List':str(ced_list),'CEDConsumption':self.convertArrayToString(ced_energy) , 'UDConsumption': self.convertArrayToString(e_ud), 'TotalDemand': self.convertArrayToString(total_energy)}
            engine = db.create_engine('sqlite:///'+self.db_path)
            connection = engine.connect()
            metadata = db.MetaData()
            object = db.Table('Building', metadata, autoload=True, autoload_with=engine)
            query = db.update(object).values(values)
            query = query.where(object.columns.Id == buildingId)
            results = connection.execute(query)
            return results
        except Exception as e:
            print(e.args)
            return None
        
    def updateDeviceEnergyData(self, values, deviceId):
        try:
            engine = db.create_engine('sqlite:///'+self.db_path)
            connection = engine.connect()
            metadata = db.MetaData()
            object = db.Table('DeviceModules', metadata, autoload=True, autoload_with=engine)
            query = db.update(object).values(values)
            query = query.where(object.columns.Id == deviceId)
            results = connection.execute(query)
            return results
        except Exception as e:
            print("Hello yy")
            print(e.args)
            return None
        
    def updateStartStopTimeDevice(self, StartTime, EndTime, deviceId):
        try:
            print(StartTime, EndTime, deviceId)
            engine = db.create_engine('sqlite:///'+self.db_path)
            connection = engine.connect()
            metadata = db.MetaData()
            object = db.Table('DeviceModules', metadata, autoload=True, autoload_with=engine)
            values = {'StartTime(h)':str(StartTime),'EndTime(h)': str(EndTime)}
            query = db.update(object).values(values)
            query = query.where(object.columns.Id == deviceId)
            results = connection.execute(query)
            self.updateBuildingEnergyData(deviceId,0)
            return results
        except Exception as e:
            print(e.args)
            return None
    
        
    def addDevicetoBuilding(self,the_key,the_value,buildingId):
        device=Device(est=the_value[0],let=the_value[1],E=the_value[2],lot=the_value[3],name=the_key)
        device_energy=device.energy_cal()
        total=device.energy_total()
        values = [{'Building':str(int(buildingId)), 'DemandSide':str(int(self.DemandSideId)), 'DeviceName':str(the_key), 'EST(h)': str(the_value[0]), 'LET(h)':str(the_value[1]), 'LOT(h)':str(the_value[3]),'Power(kW)':str(the_value[2]), 'StartTime(h)':str(device.t_start),'EndTime(h)':str(device.t_end), 'DeviceStatus':1,'Power_total(kW)':self.convertArrayToString(device_energy),'Power_sum(kW)':str(total)}]
        deviceId = self.insert_given_data('DeviceModules',values)
        return device_energy
        

    def addDevice(self, est, let, E, lot, name,startTime, endTime, buildingId):
        device = Device(est = est, let = let, E=E, lot=lot,name=name)
        consumption = device.energy_cal(startTime,endTime)
        total=device.energy_total()
        values = [{'Building':str(int(buildingId)), 'DemandSide':str(int(self.DemandSideId)), 'DeviceName':device.name, 'EST(h)': str(device.est), 'LET(h)':str(device.let), 'LOT(h)':str(device.lot),'Power(kW)':str(device.E), 'StartTime(h)':str(device.t_start),'EndTime(h)':str(device.t_end), 'DeviceStatus':1,'Power_total(kW)':self.convertArrayToString(consumption),'Power_sum(kW)':str(total)}]
        deviceId = self.insert_given_data('DeviceModules',values)
        print("kk",deviceId)
        self.updateBuildingEnergyData(deviceId,0)
        return deviceId
        

    def update_last_update_time(self, initial = False):
        cur = None
        con = None
        data = None
        try:
            current_time = datetime.strftime(datetime.now(), '%b %d, %Y %X')
            INSERT_INITIAL_QUERY = "INSERT INTO LastUpdate (Id,LastUpdate) VALUES (1,NULL)"
            INSERT_QUERY = "INSERT INTO LastUpdate (Id,LastUpdate) VALUES (1,'"+current_time+"')"
            UPDATE_QUERY = "UPDATE LastUpdate SET LastUpdate='"+current_time+"' WHERE Id=1"
            print(INSERT_INITIAL_QUERY, INSERT_QUERY, UPDATE_QUERY)
            if(not initial):
                con = sqlite3.connect(self.db_path)
                cur = con.cursor()
                if(self.get_last_update_time() is None):
                    cur.execute(INSERT_QUERY)
                    con.commit()
                    data = 100
                else:
                    cur.execute(UPDATE_QUERY)
                    con.commit()
                    data = 101
            else:
                con = sqlite3.connect(self.db_path)
                cur = con.cursor()
                cur.execute("DELETE FROM LastUpdate")
                cur.execute(INSERT_INITIAL_QUERY)
                con.commit()
                data = 100
        except sqlite3.Error as e:
            print("Exception Logged: Update"+str(e))
            data = 112
        finally:
            if con:
                con.close()
            return data

    def convertArrayToString(self, strArray):
        #print("hello",strArray)
        stringData = json.dumps(numpy.around(strArray,decimals=2).tolist())
        return stringData

    def convertStringToArray(self, str):
        numpy.set_printoptions(suppress=True)
        arrayData = numpy.around(numpy.fromiter(json.loads(str), dtype=float, count=24),decimals=2)
        return arrayData

test = DemandSide()
#demandid=test.addDemandSide()
#test.getBuildingsBasedOnDemandSideId(demandid)
#print(test.is_data_latest())
#print(test.addDemandSide())
#test.addDemandSide()
#build = test.addBuilding()
print("1",test.updateStartStopTimeDevice(14,16,3))
#print(test.addDevice(9,18,1,2,"washer",1))
#print("2",test.getDevicesBasedOnBuildingId(build))
#print(test.updateBuildingData(build))
