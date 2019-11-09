import os, sys
import json
import requests
import sqlite3
from datetime import datetime
import os.path

class Weather_Data_Access:
    def __init__(self):
        cwd = os.getcwd()
        fname = cwd+'/DataAccessLayer/config.json'
        with open(fname) as config_file:
            config = json.load(config_file)
        self.__current_weather_api_url=''
        self.__forecast_weather_api_url=''
        self.__db_connection=''
        self.__BASE_DIR=''
        self.__db_path=''
        self.__schema_file_path=''
        self.__db_schema_filename = 'Weather_Service_DB_Schema.sql'
        self.form_connections(config)
        print("Does DB Exists "+str(self.check_db_existence()))

    def check_db_existence(self):
        db_exists = os.path.exists(self.__db_path)
        return db_exists

    def form_connections(self, config):
        self.__current_weather_api_url = (config)['config_data']['api_url'] + '/current' + \
            '?key=' + (config)['config_data']['api_key'] + '&postal_code='+(config)['required_data']['city_code']+ \
                '&country='+(config)['required_data']['country']
        self.__forecast_weather_api_url = (config)['config_data']['api_url'] + '/forecast/hourly' + \
            '?key=' + (config)['config_data']['api_key'] + '&postal_code='+(config)['required_data']['city_code']+ \
                '&country='+(config)['required_data']['country']+'&hours=48' 
        self.__db_connection = (config)['config_data']['db_url']
        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__db_path = os.path.join(self.__BASE_DIR, self.__db_connection)
        self.__schema_file_path = os.path.join(self.__BASE_DIR, self.__db_schema_filename)
        #Check If DB exists in the path
        if(not self.check_db_existence()):
            self.create_db_schema()

    def create_db_schema(self):
        with sqlite3.connect(self.__db_path) as conn:
            with open(self.__schema_file_path, 'rt') as file:
                schema = file.read()
            conn.executescript(schema)
            self.update_forecast_data()

    def get_last_update_time(self):
        con = None
        cur = None
        data = None
        SELECT_QUERY = "SELECT LastUpdate FROM LastUpdate LIMIT 1"
        try:
            con = sqlite3.connect(self.__db_path)
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
        last_update_time = self.get_last_update_time()
        last_update_hour = datetime.strptime(last_update_time, '%b %d, %Y %H:%M:%S').hour
        if(current_hour == last_update_hour):
            return True
        return False

    def update_last_update_time(self):
        cur = None
        con = None
        data = None
        try:
            current_time = datetime.strftime(datetime.now(), '%b %d, %Y %X')
            con = sqlite3.connect(self.__db_path)
            cur = con.cursor()
            INSERT_QUERY = "INSERT INTO LastUpdate (Id,LastUpdate) VALUES (1,'"+current_time+"')"
            UPDATE_QUERY = "UPDATE LastUpdate SET LastUpdate='"+current_time+"' WHERE Id=1"
            if(self.get_last_update_time() is None):
                print("None")
                result = cur.execute(INSERT_QUERY)
                con.commit()
                data = 100
            else:
                print("Time" + self.get_last_update_time())
                result = cur.execute(UPDATE_QUERY)
                con.commit()
                data = 101
        except sqlite3.Error as e:
            print("Exception Logged: Update"+str(e))
            data = 112
        finally:
            if con:
                con.close()
                return data
        
    def get_current_data(self):
        return (requests.get(self.__current_weather_api_url)).json()
    
    def get_wind_parameters(self):
        data = self.get_current_data()
        return {
            #edit params names into capital
            "Temperature": data["data"][0]["temp"],
            "Pressure": data["data"][0]["pres"],
            "Humidity": data["data"][0]["rh"],
            "Windspeed": data["data"][0]["wind_spd"],
        }

    def get_PV_Parameters(self):
        data = self.get_current_data()
        last_day_rec = datetime.strptime(data["data"][0]["datetime"],'%Y-%m-%d:%H')
        return {
            "Temperature": data["data"][0]["temp"],
            "Latitude": data["data"][0]["lat"],
            "DayOfYear": (last_day_rec - datetime(last_day_rec.year,1,1)).days+1,
            "SolarIrradiance": data["data"][0]["solar_rad"],
        }

    def get_forecast_values(self):
        return (requests.get(self.__forecast_weather_api_url)).json()

    def update_wind_energy_data(self, forecast_data):
        cur = None
        con = None
        try:
            con = sqlite3.connect(self.__db_path)
            cur = con.cursor()
            DELETE_QUERY = "DELETE FROM WindParameters"
            cur.execute(DELETE_QUERY)
            con.commit()
            INSERT_QUERY = "INSERT INTO WindParameters (Temperature,Pressure,Humidity,WindSpeed) VALUES ("
            for i in forecast_data["data"]:
                cur.execute(INSERT_QUERY+str(i["temp"])+","+str(i["pres"])+","+str(i["rh"])+","+str(i["wind_spd"])+")")
                con.commit()
        except sqlite3.Error as e:
            print("Exception Logged near update wind: "+str(e))
        finally:
            if cur:
                cur.close()
            if con:
                con.close()
            #self.__wind_energy_forecast_data.append({"temperature":i["temp"],"pressure":i["pres"],"humidity":i["rh"]})

    def update_forecast_data(self):
        data = self.get_forecast_values()
        self.update_wind_energy_data(data)
        self.update_solar_energy_data(data)
        self.update_last_update_time()

    def update_solar_energy_data(self, forecast_data):
        cur = None
        con = None
        try:
            con = sqlite3.connect(self.__db_path)
            cur = con.cursor()
            DELETE_QUERY = "DELETE FROM PVParameters"
            cur.execute(DELETE_QUERY)
            INSERT_QUERY = "INSERT INTO PVParameters (Temperature, SolarIrradiance,LastMeasure,Latitude) VALUES ("
            lat = forecast_data["lat"]
            for i in forecast_data["data"]:
                last_day_rec = datetime.strptime(i["datetime"], '%Y-%m-%d:%H')
                cur.execute(INSERT_QUERY+str(i["temp"])+","+str(i["solar_rad"])+","+str((last_day_rec - datetime(last_day_rec.year,1,1)).days+1)+","+str(lat)+")")
                con.commit()
        except sqlite3.Error as e:
            print("Exception Logged near update solar: "+str(e))
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    
    def get_wind_forecast(self):
        cur = None
        con = None
        data = []
        try:
            print(self.is_data_latest())
            if(self.is_data_latest()==False):
                self.update_forecast_data()
            SELECT_QUERY = "SELECT Hour,Temperature,Pressure,Humidity,WindSpeed FROM WindParameters"
            con = sqlite3.connect(self.__db_path)
            cur = con.cursor()
            result = cur.execute(SELECT_QUERY)
            for row in result:
                #add Humidity row at 3rd column
                data.append({row[0]:{"Temperature":row[1],"Pressure":row[2],"Humidity":row[3],"WindSpeed":row[4]}})
        except sqlite3.Error as e:
            print("Exception Logged near get wind forecast: "+str(e))
        finally:
            if cur:
                cur.close()
            if con:
                con.close()
            return data

    def get_PV_forecast(self):
        cur = None
        con = None
        data = []
        try:
            if(self.is_data_latest()==False):
                self.update_forecast_data()
            SELECT_QUERY = "SELECT Hour,Temperature,SolarIrradiance,LastMeasure,Latitude FROM PVParameters"
            con = sqlite3.connect(self.__db_path)
            cur = con.cursor()
            result = cur.execute(SELECT_QUERY)
            for row in result:
                data.append({row[0]:{"Temperature":row[1],"SolarIrradiance":row[2],"DayOfYear":row[3],"Latitude":row[4]}})
        except sqlite3.Error as e:
            print("Exception Logged near PV forecast: "+str(e))
        finally:
            if cur:
                cur.close()
            if con:
                con.close()
            return data
        
