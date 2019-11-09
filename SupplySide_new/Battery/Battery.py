import os, sys
import json
from datetime import datetime
import os.path

class Battery:
    def __init__(self, efficiency, time_interval, charge_specs, discharge_specs, energy_specs, initial_energy, self_discharge_rate):
        self.efficiency=efficiency            #Indicates Efficiency of battery
        self.time_interval = time_interval    #Indicates Time Interval along which the calculation of energy is done
        self.charge_specs=charge_specs        #Indicates Maximum charging capacity of battery
        self.discharge_specs=discharge_specs  #Indicates Maximum discharge capacity of battery
        self.energy_specs=energy_specs        #Indicates Capacity of Battery
        self.inital_energy=initial_energy     #Indicates Initial energy level for the battery to start with
        self.self_discharge_rate = self_discharge_rate
        self.power_level=0                    #Indicates Total Power 
        self.current_state= "idle"            #Indicates Current State 
        self.status=1                         #Indicates whether battery is ON or OFF

    def check_constraints(self, action, input_energy, total_energy): 
        if(action == "charging"):
            return True if input_energy<=self.charge_specs and total_energy<=self.energy_specs else False
        elif(action == "discharging"):
            return True if input_energy<=self.discharge_specs and total_energy - input_energy>=0 else False
        #returns true if constraints satisfies else false
        #Compare input energy and charge specs if charging
        #Compare input energy and discharge specs if discharging

    def calculate_energy(self, charge_rate, discharge_rate, status, current_energy):
        current_time = datetime.now()
        if(current_time.hour==1 or current_time.hour==0):
            return 0
        energy_charged = self.efficiency * charge_rate
        energy_discharged = discharge_rate/self.efficiency
        energy_self_discharged = status * self.self_discharge_rate
        total_energy = current_energy + energy_charged - energy_discharged - energy_self_discharged
        return total_energy

    def charge(self, input_energy, current_state_information):
        #self.current_state_information = self.get_current_state_information()
        total_energy = self.calculate_energy(input_energy, 0, current_state_information[0]["status"], float(current_state_information[0]["power_level"]))
        can_charge = self.check_constraints("charging", input_energy, total_energy)
        if(can_charge):
            return {
                "status":100, 
                "output":total_energy,
                "charging_state":"charging",
                "success":True
                }
        return {
            "status":101, 
            "output":0,
            "charging_state":"idle",
            "success":False
            }


    def discharge(self, input_energy, current_state_information):
        #self.current_state_information = self.get_current_state_information()
        total_energy = self.calculate_energy(0, input_energy, current_state_information[0]["status"], float(current_state_information[0]["power_level"]))
        can_discharge = self.check_constraints("discharging",input_energy, total_energy)
        if(can_discharge):
            return {
                "status":102, 
                "output":total_energy,
                "charging_state":"discharging" if input_energy>0 else "idle",
                "success":True
                }
        return {
            "status":103, 
            "output":0,
            "charging_state":"idle",
            "success":False
            }


    def update_energy(self, input_energy, current_state_information):
        if(input_energy>0):
            return(self.charge(input_energy, current_state_information))
        elif(input_energy==0):
            return(self.discharge(0))
        else:
            return(self.discharge(abs(input_energy), current_state_information))
