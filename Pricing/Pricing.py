import sqlite3
from datetime import datetime
from datetime import timedelta
import time
from entsoe import EntsoePandasClient
import pandas as pd
import os

class Pricing_data:
    def __init__(self):
        self.__db_name = 'Pricing_data.db'
        self.schema_path = "pricing_schema.sql"
        self.__cursor = None
        self.__connection = None
        self.__client = EntsoePandasClient(api_key='db59dcca-7ec4-4484-956e-86152f39e8be')
        self.__country_code = 'BE'  # Belgium
        self.__timezone = 'Europe/Brussels'
        self.today_start = None
        self.today_end = None
        self.tomorrow_start = None
        self.tomorrow_end = None
        self.updated = False
        self.create_db()

    def check_db_existence(self):
        db_exists = os.path.exists(self.__db_name)
        return db_exists

    def create_db_schema(self):
        with sqlite3.connect(self.__db_name) as conn:
            with open(self.schema_path, 'rt') as file:
                schema = file.read()
            conn.executescript(schema)
        self.update_last_update_time_today_price(True)
        self.update_last_update_time_tomorrow_price(True)
        
    def create_db(self):
        if(not self.check_db_existence()):
            self.create_db_schema()
        self.__connection = sqlite3.connect(self.__db_name)
        self.__cursor = self.__connection.cursor()
        #create empty tables
        #self.__cursor.execute('CREATE TABLE today(hour INTEGER PRIMARY KEY, price FLOAT)')
        #self.__cursor.execute('CREATE TABLE tomorrow(hour INTEGER PRIMARY KEY, price FLOAT)')

        

    def get_today_data(self):
        #get today time
        today = datetime.now().date()
        self.today_start = today.strftime('%Y%m%d')
        self.today_end = (today + timedelta(days=1)).strftime('%Y%m%d')
            
        #set today time
        self.today_start = pd.Timestamp(self.today_start,tz = self.__timezone)
        self.today_end = pd.Timestamp(self.today_end, tz = self.__timezone)
            
        #get today data
        today_data = self.__client.query_day_ahead_prices(self.__country_code,start = self.today_start,end = self.today_end)
        
        return today_data
    
    def upload_today_data(self):
        today_data = self.get_today_data()
        #delete the yesterday table
        self.__cursor.execute('DROP TABLE today')
        self.__cursor.execute('CREATE TABLE today(hour INTEGER PRIMARY KEY, price FLOAT)')
        for i in range(0,24):
            self.__cursor.execute('INSERT INTO today VALUES(?,?)',(i,today_data[i]))
            self.__connection.commit()
        self.update_last_update_time_today_price()
    # No need
    def check_time(self):
        #check if correct date for updating tomorrow data
        #should have changed the tomorrow data, first need to check datetime, if in range, continuously update til latest one, 
        #otherwise use the today data
        update = False
        now = datetime.now()
        update_start = now.replace(hour=10, minute=30, second=0, microsecond=0)
        #update_end = now.replace(hour=13, minute=30, second=0, microsecond=0)
        if (update_start < now):
            update = True
        
        return update
        
    
    def get_tomorrow_data(self):
        #loop = True
        #get today time
        tomorrow = datetime.now().date() + timedelta(days = 1)
        self.tomorrow_start = tomorrow.strftime('%Y%m%d')
        self.tomorrow_end = (tomorrow + timedelta(days=1)).strftime('%Y%m%d')
        
        #set tomorrow time
        self.tomorrow_start = pd.Timestamp(self.tomorrow_start,tz = self.__timezone)
        self.tomorrow_end = pd.Timestamp(self.tomorrow_end, tz = self.__timezone)
        
        #while(self.check_time() & loop):
            #get tomorrow data
        #    try:
        #        tomorrow_data = self.__client.query_day_ahead_prices(self.__country_code,start = self.tomorrow_start,end = self.tomorrow_end)
        #        loop = False
        #        self.updated = True
        #    except:
        #        loop = True
        is_latest = False
        try:
            tomorrow_data = self.__client.query_day_ahead_prices(self.__country_code,start = self.tomorrow_start,end = self.tomorrow_end)
            is_latest = True
        except Exception as e:
            # in case the value is not yet available
            tomorrow_data = self.get_today_data()
            is_latest = False
        return { "data" : tomorrow_data, "is_latest": is_latest }

    def is_data_latest_for_today_price(self):
        current_date = datetime.now().date
        last_update_time = self.get_last_update_time()
        if(not last_update_time is None):
            last_update_date = datetime.strptime(last_update_time["today"], '%b %d, %Y %H:%M:%S').date
            if(current_date == last_update_date):
                return True
            return False
        return False
    
    def is_data_latest_for_tomorrow_price(self):
        current_date = datetime.now().date
        last_update_time = self.get_last_update_time()
        if(not last_update_time is None):
            last_update_date = datetime.strptime(last_update_time["tomorrow"], '%b %d, %Y %H:%M:%S').date
            if(current_date == last_update_date):
                return True
            return False
        return False
    
    def upload_tomorrow_data(self):
        #if(self.updated == False):
        #    tomorrow_data = self.get_today_data()
        #else:
        #    tomorrow_data = self.get_tomorrow_data()
        #delete the today table
        raw_data = self.get_tomorrow_data()
        self.__cursor.execute('DROP TABLE tomorrow')
        self.__cursor.execute('CREATE TABLE tomorrow(hour INTEGER PRIMARY KEY, price FLOAT)')
        for i in range(0,24):
            self.__cursor.execute('INSERT INTO tomorrow VALUES(?,?)',(i,raw_data["data"][i]))
            self.__connection.commit()
        if(raw_data["is_latest"]):
            self.update_last_update_time_tomorrow_price()

    def get_forecast_pricing(self):
        print(self.is_data_latest_for_tomorrow_price())
        if(not self.is_data_latest_for_tomorrow_price()):
            self.upload_tomorrow_data()
        current_hour = datetime.now().hour
        con = None
        cur = None
        data = None
        SELECT_QUERY = "SELECT price FROM today WHERE hour>="+str(current_hour)+" UNION ALL SELECT price from tomorrow WHERE hour<="+str(current_hour-1)
        try:
            con = sqlite3.connect(self.__db_name)
            cur = con.cursor()
            result = cur.execute(SELECT_QUERY)
            forecast_pricing = []
            for row in result:
                forecast_pricing.append(row[0])
        except sqlite3.Error as e:
            print("Exception Logged: Get "+str(e))
            return None
        finally:
            if con:
                con.close()
            return forecast_pricing


    def get_current_pricing(self):
        print(self.is_data_latest_for_today_price())
        if(not self.is_data_latest_for_today_price()):
            self.upload_today_data()
        current_hour = datetime.now().hour
        con = None
        cur = None
        data = None
        SELECT_QUERY = "SELECT price FROM today WHERE hour = "+str(current_hour)
        try:
            con = sqlite3.connect(self.__db_name)
            cur = con.cursor()
            result = cur.execute(SELECT_QUERY)
            for row in result:
                return row[0]
        except sqlite3.Error as e:
            print("Exception Logged: Get "+str(e))
            return None
        finally:
            if con:
                con.close()

    def can_update(self):
        current_hour = datetime.now().hour
        if(current_hour>=10 and current_hour<=13):
            return True
        return False

    def get_last_update_time(self):
        con = None
        cur = None
        data = None
        SELECT_QUERY = "SELECT LastUpdateTodayPrice, LastUpdateTomorrowPrice FROM LastUpdate LIMIT 1"
        try:
            con = sqlite3.connect(self.__db_name)
            cur = con.cursor()
            result = cur.execute(SELECT_QUERY)
            for row in result:
                print(row[0])
                return {"today": row[0],"tomorrow": row[1]}
        except sqlite3.Error as e:
            print("Exception Logged: Get "+str(e))
            return None
        finally:
            if con:
                con.close()
   
    def update_last_update_time_today_price(self, initial=False):
        cur = None
        con = None
        data = None
        try:
            if(initial):
                yesterday = datetime.now() - timedelta(days=1)
                current_time = datetime.strftime(yesterday, '%b %d, %Y %X')
            else:
                current_time = datetime.strftime(datetime.now(), '%b %d, %Y %X')
            con = sqlite3.connect(self.__db_name)
            cur = con.cursor()
            INSERT_QUERY = "INSERT INTO LastUpdate (Id,LastUpdateTodayPrice) VALUES (1,'"+current_time+"')"
            UPDATE_QUERY = "UPDATE LastUpdate SET LastUpdateTodayPrice='"+current_time+"' WHERE Id=1"
            if(self.get_last_update_time()["Today"] is None):
                print("None")
                result = cur.execute(INSERT_QUERY)
                con.commit()
                data = 100
            else:
                print("Time" + self.get_last_update_time()["Today"])
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

    def update_last_update_time_tomorrow_price(self, initial=False):
        cur = None
        con = None
        data = None
        try:
            if(initial):
                yesterday = datetime.now() - timedelta(days=1)
                current_time = datetime.strftime(yesterday, '%b %d, %Y %X')
            else:
                current_time = datetime.strftime(datetime.now(), '%b %d, %Y %X')
            con = sqlite3.connect(self.__db_name)
            cur = con.cursor()
            INSERT_QUERY = "INSERT INTO LastUpdate (Id,LastUpdateTomorrowPrice) VALUES (1,'"+current_time+"')"
            UPDATE_QUERY = "UPDATE LastUpdate SET LastUpdateTomorrowPrice='"+current_time+"' WHERE Id=1"
            if(self.get_last_update_time()["Tomorrow"] is None):
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
              

test = Pricing_data()
#test.create_db()
#test.upload_today_data()
#test.upload_tomorrow_data()
print(test.get_current_pricing())
print(test.get_forecast_pricing())
#print(test.get_tomorrow_data()["data"])