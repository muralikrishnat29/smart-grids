import json
import bottle
import os
import numpy
import sqlite3
import random

from bottle import route, run, request, abort
from datetime import datetime

from Wind.wind import wind
from PV.pv import pv
from Battery.Battery import Battery

class SupplySide:
    def __init__(self):#, wind, pv, battery):
        self.db_path = "supply_side_data.db"
        self.schema_path = "supply_side_data.sql"
        self.SELECT_QUERY_WIND = "SELECT Id, Status, SupplySide, Ra, Location, CurrentEnergy, ForecastEnergy FROM WindModules"
        self.SELECT_QUERY_SOLAR = "SELECT Id, Status, SupplySide, Area, EMax, AngleOfModule, Location, CurrentEnergy, ForecastEnergy FROM PVModules"
        self.SELECT_QUERY_BATTERY = "SELECT Id, Status, SupplySide, State, Efficiency, TimeInterval, InitialEnergy, SelfDischargeRate, Charge, ChargeSpecs, DischargeSpecs, EnergySpecs FROM Battery"
        self.UPDATE_QUERY_BATTERY = "UPDATE Battery SET Status =?, Charge = ?, State = ? WHERE SupplySide =?"
        self.UPDATE_QUERY_BATTERY_COMPLETE = "UPDATE Battery SET Efficiency=?,TimeInterval=?,InitialEnergy=?,SelfDischargeRate=?, ChargeSpecs=?, DischargeSpecs=?, EnergySpecs=?  WHERE SupplySide =?"
        self.INSERT_QUERY_WIND = "INSERT INTO WindModules (Status, SupplySide, Ra, Location, CurrentEnergy, ForecastEnergy) VALUES ("
        self.INSERT_QUERY_SOLAR = "INSERT INTO PVModules (Status, SupplySide, Area, EMax, AngleOfModule, Location, CurrentEnergy, ForecastEnergy) VALUES("
        self.INSERT_QUERY_BATTERY = "INSERT INTO Battery (Status, SupplySide,State, Efficiency, TimeInterval, InitialEnergy, SelfDischargeRate, Charge, ChargeSpecs, DischargeSpecs, EnergySpecs) VALUES("
        self.INSERT_QUERY_HISTORY = "INSERT INTO History (Hour, WindEnergy, SolarEnergy, TotalEnergy) VALUES ("
        self.DELETE_QUERY_WIND = "DELETE FROM WindModules"
        self.DELETE_QUERY_SOLAR = "DELETE FROM PVModules"
        self.DELETE_QUERY_BATTERY = "DELETE FROM Battery"
        self.supplySideId = 0
        self.wind = []
        self.pvData = []
        self.battery = []
        #self.updateHistoricalEnergyGenerationData()
        #self.wind.append(wind)
        #self.pv.append(pv)
        #self.battery = battery
        # get forecast and add to db
        if(not self.check_db_existence()):
            self.create_db_schema()
            self.addSupplySide()
            self.update_last_update_time(initial=False)
        else:
            self.getExistingData()
        
    def getExistingData(self):
        cur=None
        con=None
        SELECT_SUPPLY_SIDE_QUERY = "SELECT Id FROM SupplySide"
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            res = cur.execute(SELECT_SUPPLY_SIDE_QUERY)
            for row in res:
                self.supplySideId = row[0]
            if(self.supplySideId != None):
                if(not self.is_data_latest()):
                    self.updateEnergyData()
            return self.supplySideId
        except sqlite3.Error as e:
            print("Exception Logged near update supply side: "+str(e))
            return 0
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def updateEnergyData(self):
        self.update_wind_energy_data(self.wind)
        self.update_solar_energy_data(self.pvData)
        self.update_last_update_time()

    @classmethod
    def customSupplySide(self, wind, pvSrc, battery):
        self.wind = wind
        self.pvData = pvSrc
        self.battery = battery
        # delete, get forecast and add to db

    def getSupplySide(self):
        cur=None
        con=None
        SELECT_SUPPLY_SIDE_QUERY = "SELECT Id FROM SupplySide"
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            result = cur.execute(SELECT_SUPPLY_SIDE_QUERY)
            for row in result:
                self.supplySideId = row[0]
                break
            con.commit()
            return self.supplySideId
        except sqlite3.Error as e:
            print("Exception Logged near update supply side: "+str(e))
            return 0
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def addSupplySide(self):
        cur=None
        con=None
        randomNumber = random.randint(1,1000)
        description = "SupplySide"+str(randomNumber)
        SELECT_SUPPLY_SIDE_QUERY = "SELECT Id FROM SupplySide WHERE Id = " +str(randomNumber)
        DELETE_SUPPLY_SIDE_QUERY = "DELETE FROM SupplySide"
        INSERT_SUPPLY_SIDE_QUERY = "INSERT INTO SupplySide (Id, Description) VALUES ("+str(randomNumber)+",'"+description+"')"
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            res = cur.execute(SELECT_SUPPLY_SIDE_QUERY)
            if(not res.rowcount ==-1):
                cur.execute(DELETE_SUPPLY_SIDE_QUERY)
            result = cur.execute(INSERT_SUPPLY_SIDE_QUERY)
            self.supplySideId = result.lastrowid
            con.commit()
            return self.supplySideId
        except sqlite3.Error as e:
            print("Exception Logged near update supply side: "+str(e))
            return 0
        finally:
            if cur:
                cur.close()
            if con:
                con.close()


    def update_solar_energy_data(self, pvData):
        cur = None
        con = None
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute(self.DELETE_QUERY_SOLAR+"WHERE SupplySide = "+str(self.supplySideId))
            for i in range(0,len(pvData)-1):
                pvComponent = pv(float(pvData[i]["Area"]),float(pvData[i]["EMax"]),float(pvData[i]["AngleOfModule"]),"Stuttgart")
                current_energy = pvComponent.energy_cal_cur()
                print("fd",current_energy)
                forecast_energy = self.convertArrayToString(pvComponent.energy_cal_for())
                FINAL_INSERT_QUERY = self.INSERT_QUERY_SOLAR + "1,"+str(self.supplySideId)+","+str(pvComponent.Area)+",'" \
                                    +str(pvComponent.Emax)+"',"+str(pvComponent.Angle_of_Module)+",'"+pvComponent.Location+"',"+str(current_energy)+",'"+forecast_energy+"')"
                cur.execute(FINAL_INSERT_QUERY)
                con.commit()
        except sqlite3.Error as e:
            print("Exception Logged near update solar energy data: "+str(e))
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def update_wind_energy_data(self, windData):
        cur = None
        con = None
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute(self.DELETE_QUERY_WIND+"WHERE SupplySide = "+str(self.supplySideId))
            for i in range(0,len(windData)-1):
                windComponent = wind(int(windData[i]["Ra"]),windData[i]["Location"])
                current_energy = windComponent.energy_cal_cur()
                forecast_energy = self.convertArrayToString(windComponent.energy_cal_for())
                print(type(forecast_energy))
                FINAL_INSERT_QUERY = self.INSERT_QUERY_WIND + "1,"+str(self.supplySideId)+","+str(windData[i]["Ra"])+",'" \
                                    +windData[i]["Location"]+"',"+str(current_energy)+",'"+forecast_energy+"')"
                cur.execute(FINAL_INSERT_QUERY)
                con.commit()
        except sqlite3.Error as e:
            print("Exception Logged near update wind energy data: "+str(e))
        finally:
            if cur:
                cur.close()
            if con:
                con.close()
        

    def check_db_existence(self):
        db_exists = os.path.exists(self.db_path)
        return db_exists

    def create_db_schema(self):
        with sqlite3.connect(self.db_path) as conn:
            with open(self.schema_path, 'rt') as file:
                schema = file.read()
            conn.executescript(schema)

    def get_last_update_time(self):
        con = None
        cur = None
        data = None
        SELECT_QUERY = "SELECT LastUpdate FROM LastUpdate LIMIT 1"
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            result = cur.execute(SELECT_QUERY)
            for row in result:
                print(row[0])
                return row[0]
        except sqlite3.Error as e:
            print("Exception Logged: Get "+str(e))
            return None
        finally:
            if con:
                con.close()

    def is_data_latest(self):
        current_hour = datetime.now().hour
        print(current_hour)
        last_update_time = self.get_last_update_time()
        print(last_update_time)
        if(not last_update_time is None):
            last_update_hour = datetime.strptime(last_update_time, '%b %d, %Y %H:%M:%S').hour
            if(current_hour == last_update_hour):
                return True
            return False
        return False

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

    def addWind(self, wind):
        self.wind.append(wind)
        current_energy = wind.energy_cal_cur()
        forecast_energy = self.convertArrayToString(wind.energy_cal_for())
        FINAL_INSERT_QUERY = self.INSERT_QUERY_WIND + "1,"+str(self.supplySideId)+","+str(wind.Ra)+",'" \
                                    +wind.location+"',"+str(current_energy)+",'"+forecast_energy+"')"
        print(FINAL_INSERT_QUERY)
        cur = None
        con = None
        data = None
        try:
            #current_time = datetime.strftime(datetime.now(), '%b %d, %Y %X')
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            result = cur.execute(FINAL_INSERT_QUERY)
            con.commit()
            data = 101
        except sqlite3.Error as e:
            print("Exception Logged: Add Wind "+str(e))
            data = 112
        finally:
            if con:
                con.close()
                return data
        # get forecast and add to db
    
    def addPV(self, pvSrc):
        current_energy = pvSrc.energy_cal_cur()
        forecast_energy = self.convertArrayToString(pvSrc.energy_cal_for())
        FINAL_INSERT_QUERY = self.INSERT_QUERY_SOLAR + "1,"+str(self.supplySideId)+","+str(pvSrc.Area)+",'" \
                                    +str(pvSrc.Emax)+"',"+str(pvSrc.Angle_of_Module)+",'"+pvSrc.Location+"',"+str(current_energy)+",'"+forecast_energy+"')"
        cur = None
        con = None
        data = None
        try:
            #current_time = datetime.strftime(datetime.now(), '%b %d, %Y %X')
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            result = cur.execute(FINAL_INSERT_QUERY)
            con.commit()
            data = 101
        except sqlite3.Error as e:
            print("Exception Logged: Add PV "+str(e))
            data = 112
        finally:
            if con:
                con.close()
                return data

    def addBattery(self, battery):
        #self.battery.append(battery)
        FINAL_INSERT_QUERY = self.INSERT_QUERY_BATTERY + "1,"+str(self.supplySideId)+",'"+battery.current_state+"',"+ \
            str(battery.efficiency)+","+str(battery.time_interval)+","+str(battery.inital_energy)+","+str(battery.self_discharge_rate)+","+ \
                str(battery.power_level)+","+str(battery.charge_specs)+","+str(battery.discharge_specs)+","+str(battery.energy_specs)+")"
        cur = None
        con = None
        data = None
        try:
            #current_time = datetime.strftime(datetime.now(), '%b %d, %Y %X')
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            result = cur.execute(FINAL_INSERT_QUERY)
            con.commit()
            data = 101
        except sqlite3.Error as e:
            print("Exception Logged: Add Battery "+str(e))
            data = 112
        finally:
            if con:
                con.close()
                return data
            
    def updateBatteryData(self, efficiency, time_interval, charge_specs, discharge_specs, energy_specs, initial_energy, self_discharge_rate):
        cur = None
        con = None
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute(self.UPDATE_QUERY_BATTERY_COMPLETE, [str(efficiency), str(time_interval),str(initial_energy),str(self_discharge_rate),str(charge_specs),str(discharge_specs),str(energy_specs),str(self.supplySideId)])
            con.commit()
            self.battery = self.getCurrentBatteryData()
        except sqlite3.Error as e:
            print("Exception Logged: Get "+str(e))
        except Exception as e:
            print("Exception is"+str(e))
        finally:
            if con:
                con.close()
        return self.battery   

    def updateBatteryCharge(self, input_charge):
        batteryInfo = self.getCurrentBatteryData()
        batteryModule = Battery(float(batteryInfo[0]["efficiency"]),float(batteryInfo[0]["time_interval"]),float(batteryInfo[0]["charge_specs"]),float(batteryInfo[0]["discharge_specs"]),float(batteryInfo[0]["energy_specs"]),float(batteryInfo[0]["initial_energy"]),float(batteryInfo[0]["self_discharge_rate"]))
        update_battery_status =  batteryModule.update_energy(input_charge, batteryInfo)
        cur = None
        con = None
        try:
            if(update_battery_status["success"]):
                con = sqlite3.connect(self.db_path)
                cur = con.cursor()
                cur.execute(self.UPDATE_QUERY_BATTERY, [update_battery_status["charging_state"], str(update_battery_status["output"]),"1",self.supplySideId])
                con.commit()
                self.battery = self.getCurrentBatteryData()
        except sqlite3.Error as e:
            print("Exception Logged: Get "+str(e))
        except Exception as e:
            print("Exception is"+str(e))
        finally:
            if con:
                con.close()
        return self.battery
    
    def updateBatteryStates(self, input_charge, state):
        cur = None
        con = None
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute(self.UPDATE_QUERY_BATTERY, ["1", str(input_charge),state,str(self.supplySideId)])
            con.commit()
            self.battery = self.getCurrentBatteryData()
        except sqlite3.Error as e:
            print("Exception Logged: Get "+str(e))
        except Exception as e:
            print("Exception is"+str(e))
        finally:
            if con:
                con.close()
        return self.battery

    def getCurrentBatteryStatus(self):
        return None

    def getCurrentBatteryData(self):
        con = None
        cur = None
        data = None
        try:            
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            result = cur.execute(self.SELECT_QUERY_BATTERY + " WHERE SupplySide = "+ str(self.supplySideId))
            for row in result:
                battery = {
                    "id": row[0],
                    "status":row[1],
                    "SupplySide":row[2],
                    "charging_state":row[3],
                    "efficiency":row[4],
                    "time_interval":row[5],
                    "initial_energy":row[6],
                    "self_discharge_rate": row[7],
                    "power_level": row[8],
                    "charge_specs":row[9],
                    "discharge_specs":row[10],
                    "energy_specs":row[11]
                }
                self.battery.append(battery)
        except sqlite3.Error as e:
            print("Exception Logged: Get "+str(e))
            self.battery=None
        except Exception as e:
            print("Exception is"+str(e))
            self.battery=None
        finally:
            if con:
                con.close()
            return self.battery
                
    def updateHistoricalEnergyGenerationData(self):
        wind_energy = self.getCurrentWindEnergyGenerationData()
        print(wind_energy)
        solar_energy = self.getCurrentSolarEnergyGenerationData()
        print(solar_energy)
        total_energy = wind_energy + solar_energy
        current_hour = datetime.now().hour
        SELECT_QUERY = "SELECT * FROM History WHERE Hour = "+str(current_hour)
        UPDATE_QUERY = "UPDATE History SET WindEnergy = "+str(wind_energy)+", SolarEnergy = "+str(solar_energy)+", TotalEnergy = "+str(total_energy)+" WHERE Hour ="+str(current_hour)
        FINAL_INSERT_QUERY = self.INSERT_QUERY_HISTORY + str(current_hour)+","+str(wind_energy) +"," + str(solar_energy) + "," +str(total_energy) +")"
        cur = None
        con = None
        data = None
        try:
            #current_time = datetime.strftime(datetime.now(), '%b %d, %Y %X')
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            if(self.is_zeroth_hour()):
                cur.execute("DELETE FROM History")
            cur.execute(SELECT_QUERY)
            get_existing = cur.fetchall()
            print(FINAL_INSERT_QUERY)
            print(UPDATE_QUERY, get_existing)
            if(len(get_existing)==0):
                result = cur.execute(FINAL_INSERT_QUERY)
            else:
                result = cur.execute(UPDATE_QUERY)
            con.commit()
            data = 101
        except sqlite3.Error as e:
            print("Exception Logged: Add Battery "+str(e))
            data = 112
        finally:
            if con:
                con.close()
                return data
        

    def getCurrentWindEnergyGenerationData(self):
        if(not self.is_data_latest()):
            self.updateEnergyData()
        wind = self.getAllWindEnergyData()
        total_energy = float(wind[len(wind)-1]["total"])
        print(total_energy)
        return total_energy

    def getCurrentSolarEnergyGenerationData(self):
        if(not self.is_data_latest()):
            self.updateEnergyData()
            print("Hello")
        pv = self.getAllSolarEnergyData()
        print(pv)
        total_energy = float(pv[len(pv)-1]["total"])
        return total_energy

    def getCurrentEnergyGenerationData(self):
        if(not self.is_data_latest()):
            self.updateEnergyData()
        wind = self.getAllWindEnergyData()
        pv = self.getAllSolarEnergyData()
        total_energy = float(wind[len(wind)-1]["total"]) + float(pv[len(pv)-1]["total"])
        return total_energy

    def addTwoForecastArrays(self, firstArray, secondArray):
        result = numpy.add(firstArray,secondArray)
        return result

    def getAllWindEnergyData(self):
        con = None
        cur = None
        data = None
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            result = cur.execute(self.SELECT_QUERY_WIND + " WHERE SupplySide = "+ str(self.supplySideId))
            data = []
            total_wind_energy = 0
            total_wind_forecast_energy = numpy.zeros(shape=24,dtype=float)
            for row in result:
                forecastEnergy = self.convertStringToArray(row[6])
                wind = {
                    "id":row[0],
                    "Status":row[1],
                    "SupplySide":row[2],
                    "Ra":row[3],
                    "Location":row[4],
                    "CurrentEnergy":row[5],
                    "ForecastEnergy":self.convertArrayToString(forecastEnergy)
                }
                total_wind_energy +=float(row[5])
                total_wind_forecast_energy = self.addTwoForecastArrays(total_wind_forecast_energy,forecastEnergy)
                data.append(wind)
            data.append({
                "total":total_wind_energy,
                "total_forecast":self.convertArrayToString(total_wind_forecast_energy)
            })
            self.wind = data
            print(self.wind)
        except sqlite3.Error as e:
            print("Exception Logged: Get "+str(e))
            data=None
        except Exception as e:
            print("Exception is"+str(e))
            data = None
        finally:
            if con:
                con.close()
            return data
        
    def is_zeroth_hour(self):
        if(datetime.now().hour ==0):
            return True
        return False
        
    def getHistoricalEnergyData(self):
        con = None
        cur = None
        data = None
        try:
            self.updateHistoricalEnergyGenerationData()
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            result = cur.execute("SELECT * FROM History WHERE Hour <="+str(datetime.now().hour))
            data = []
            for row in result:
                data.append({"Hour":row[0], "WindEnergy":row[1],"SolarEnergy":row[2],"TotalEnergy":row[3]})
        except sqlite3.Error as e:
            print("Exception Logged: Get "+str(e))
            data=None
        except Exception as e:
            print("Exception is"+str(e))
            data = None
        finally:
            if con:
                con.close()
            return data

    def getAllSolarEnergyData(self):
        con = None
        cur = None
        data = None
        try:            
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            result = cur.execute(self.SELECT_QUERY_SOLAR + " WHERE SupplySide = "+ str(self.supplySideId))
            data = []
            total_solar_energy = 0
            total_solar_forecast_energy = numpy.zeros(shape=24,dtype=float)
            for row in result:
                forecastEnergy = self.convertStringToArray(row[8])
                pv = {
                    "id":row[0],
                    "Status":row[1],
                    "SupplySide":row[2],
                    "Area":row[3],
                    "EMax":row[4],
                    "AngleOfModule":row[5],
                    "Location":row[6],
                    "CurrentEnergy":row[7],
                    "ForecastEnergy":self.convertArrayToString(forecastEnergy)
                }
                total_solar_energy +=float(row[7])
                total_solar_forecast_energy = self.addTwoForecastArrays(total_solar_forecast_energy,forecastEnergy)
                data.append(pv)
            data.append({
                "total":total_solar_energy,
                "total_forecast":self.convertArrayToString(total_solar_forecast_energy)
            })
            self.pvData = data
        except sqlite3.Error as e:
            print("Exception Logged: Get "+str(e))
            data=None
        except Exception as e:
            print("Exception is"+str(e))
            data = None
        finally:
            if con:
                con.close()
            return data

    def getForecastEnergyGenerationData(self):
        if(not self.is_data_latest()):
            self.updateEnergyData()
        wind = self.getAllWindEnergyData()
        pv = self.getAllSolarEnergyData()
        total_energy_generation_forecast = self.addTwoForecastArrays(wind[len(wind)-1]["total_forecast"],pv[len(pv)-1]["total_forecast"])
        return self.convertArrayToString(total_energy_generation_forecast)

    def getForecastWindEnergyGenerationData(self):
        if(not self.is_data_latest()):
            self.updateEnergyData()
        wind = self.getAllWindEnergyData()
        total_wind_energy_forecast = wind[len(wind)-1]["total_forecast"]
        return total_wind_energy_forecast

    def getForecastSolarEnergyGenerationData(self):
        if(not self.is_data_latest()):
            self.updateEnergyData()
        pv = self.getAllSolarEnergyData()
        total_pv_energy_forecast = pv[len(pv)-1]["total_forecast"]
        return total_pv_energy_forecast

    def convertArrayToString(self, strArray):
        stringData = json.dumps(numpy.around(strArray,decimals=2).tolist())
        return stringData

    def convertStringToArray(self, str):
        numpy.set_printoptions(suppress=True)
        arrayData = numpy.around(numpy.fromiter(json.loads(str), dtype=float, count=24),decimals=2)
        return arrayData

supply = SupplySide()
print(supply.getHistoricalEnergyData())
'''supply = SupplySide()
comp1 = wind(6, "Stuttgart")
supply.addWind(comp1)
comp2 = pv(20, 75, 60, "Stuttgart")
supply.addPV(comp2)
comp3 = Battery(0.55, 1, 5, 4, 12, 0, 2)
supply.addBattery(comp3)
print(supply.getForecastEnergyGenerationData())
print(supply.getCurrentBatteryData())'''
#print(supply.updateBatteryCharge(-4))
#print(supply.getCurrentEnergyGenerationData())
#print(supply.get_last_update_time())
#print(supply.is_data_latest())
#print(supply.addSupplySide())
#supply= SupplySide()
#print(supply.is_data_latest())