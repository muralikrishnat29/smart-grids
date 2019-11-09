from Building.Device import Device
from Building.DemandProfile import DemandProfile
import numpy as np
class Building:
    def __init__(self):
        #Total energy need, including Uncontrollable Devices UD and Controllable Devices CED
        self.E = np.zeros(24)
        self.E_CED = np.zeros(24)
        self.E_UD = np.zeros(24)
        #Number of devices
        self.amount = 0
        #Device list
        self.device_list = {}
    
    #Add device into building object
    #INPUT:
    #Device name and the energy consumption in 24 hours
    #OUTPUT:
    #device_list: contains name and energy consumption array
    def device_add(self,name, array_data):
        self.device_list['%s'%(name)] = array_data
        self.amount += 1

    
    #Display device list
    def display(self):
        #print(self.device_list)
        return self.device_list
    
    #Total energy consumption of UD extracted from DemandProfile.py
    #OUTPUT
    #E_UD
    def energy_uncontrol(self):
        data = DemandProfile()
        self.E_UD = data.calculate_total_demand()
        print(self.E_UD)
        return self.E_UD
    
    #Total energy consumption of UD extracted from DemandProfile.py
    #OUTPUT
    #E_CED
    def energy_control(self):
        for i in range(self.amount):
            self.E_CED += list(self.device_list.values())[i] 
        #print("ced list")
        #print(self.E_CED)
        return self.E_CED
    
    #Total energy consumption of UD and CED
    #OUTPUT
    #E = E_CED + E_UD
    def total_energy_cal(self):
        self.energy_uncontrol()
        for i in range(self.amount):
            self.E_CED += list(self.device_list.values())[i] 
        #self.E = self.E_CED + self.E_UD
        #print("inside total energy")
        #print(self.E_UD)
        #print(self.E_CED)
        self.E = np.add(self.E_CED , self.E_UD)
        #print(self.E)
        return self.E
    
    
#test object
house = Building()
house.energy_uncontrol()
#washer = Device(9,18,1,2,"washer")
#washing_machine = Device(9,17,2,2,"washing_machine")
#house.energy_control()
#print("total energy building")
#house.total_energy_cal()
#print(house.total_energy_cal())

#dish_washer = Device(9,12,1.8,2)
#spin_dryer = Device(13,18,2.5,1)
#electrical_vehicle = Device(18,24,3.5,3,)
#vacuum_cleaner = Device(9,17,1.2,1)
