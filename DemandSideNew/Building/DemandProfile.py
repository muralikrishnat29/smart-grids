import os, sys
import json
import os.path
import numpy

class DemandProfile:
    def __init__(self):
        cwd = os.getcwd()
        self.fname = cwd + '/demand-profile.json'
        
    def get_data(self):
        demand={}
        with open(self.fname) as demand_info:
            demand = json.load(demand_info)
        return demand

    def calculate_total_demand(self):
        data = self.get_data()
        total_energy_data=[]
        num=0
        total_demand = numpy.zeros(24)
        for i in data:
            value = i[str(1+num)]["Circulation Pump"]+i[str(1+num)]["Dish Washer"]+i[str(1+num)]["Freezer"]+i[str(1+num)]["Washing Machine"]
            total_demand[num] = value
            num+=1
        return total_demand

#sample object
#sample = DemandProfile()
#print(sample.calculate_total_demand())