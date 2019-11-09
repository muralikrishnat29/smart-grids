import os, sys
import json
import sqlite3
from datetime import datetime, timedelta
import time
import os.path
import random

class load_data:
    def __init__(self):
        cwd = os.getcwd()
        self.fname = cwd + '/demand-profile.json'
        self.dbname = cwd + '/household_data.sqlite'
        
        
    def check_db_file_existence(self):
        if(os.path.exists(self.fname) and os.path.exists(self.dbname)):
            return True
        return False

    def get_random_date_range(self):
        start = "2015-04-16"
        end = "2016-01-11"
        format = "%Y-%m-%d"
        return_format1 = "%Y-%m-%dT00:00:00+0200"
        return_format2 = "%Y-%m-%dT00:00:00+0100"
        stime = time.mktime(time.strptime(start, format))
        etime = time.mktime(time.strptime(end, format))
        props = random.random()
        ptime = stime + props * (etime - stime)
        endtime = datetime.strptime(time.strftime(format, time.localtime(ptime)), format) + timedelta(days=1)
        random_date = time.strftime(return_format1, time.localtime(ptime))
        return {
            "startNDST":time.strftime(return_format1, time.localtime(ptime)),
            "endNDST": datetime.strftime(endtime,return_format1),
            "startDST": time.strftime(return_format2, time.localtime(ptime)),
            "endDST": datetime.strftime(endtime,return_format2),
        }

    def get_data(self):
        date_range = self.get_random_date_range()
        SELECT_QUERY = "SELECT DE_KN_residential2_circulation_pump,DE_KN_residential2_dishwasher, DE_KN_residential2_freezer, DE_KN_residential2_washing_machine FROM household_data_60min_singleindex"
        con = None
        cur = None
        data = []
        try:
            con = sqlite3.connect(self.dbname)
            cur = con.cursor()
            CONDITION_1 = " cet_cest_timestamp BETWEEN '" + date_range["startDST"] + "' AND '"+ date_range["endDST"]+"'"
            CONDITION_2 = " cet_cest_timestamp BETWEEN '" + date_range["startNDST"] + "' AND '"+ date_range["endNDST"]+"'"
            FINAL_QUERY = SELECT_QUERY + " WHERE " + CONDITION_1 + " OR " + CONDITION_2
            result = cur.execute(FINAL_QUERY)
            num = 1
            for row in result:
                data.append({num:{"Circulation Pump":row[0],"Dish Washer":row[1],"Freezer":row[2],"Washing Machine":row[3]}})
                num +=1
                if(num==25):
                    break
        except sqlite3.Error as e:
            print("Exception Logged near Get Data: "+str(e))
        finally:
            if cur:
                cur.close()
            if con:
                con.close()
            return data

    def put_data(self):
        data = self.get_data()
        try:
            with open(self.fname,'w') as outfile:
                json.dump(data,outfile)
            return True
        except Exception as e:
            print("Error: ", str(e)) 
            return False


p = load_data()
print(p.put_data())


    
