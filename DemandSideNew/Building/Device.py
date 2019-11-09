import numpy as np
class Device: 
    #should be used for controllable devices
    def __init__(self,est,let,E,lot, name):
        #User input parameters
        #est - 
        #let - 
        #E
        self.name = name
        self.est = est
        self.let = let
        self.E = E
        self.lot = lot
        #Get from user
        self.t_start = -1.0
        self.t_end = -1.0
        #Status results
        self.s = np.zeros(24)
        self.P = np.zeros(24)
        self.totalE=0
    #Display all user input parameters    
    def display(self):
        print(self.est," ", self.let," ",self.E," ",self.lot)
    
    #the time should be automatically controlled by system? according to the price?
    def get_time(self):
        self.t_start = float(input("input starting time: "))
        self.t_end = float(input("input ending time: "))
    
    #Check if the device is turned on or not
    #Return -1 if the device is not properly turned on
    def start_check(self):
        count = 0
        #check if machine is turned on out of bound => inactivate
        if (self.t_start < self.est):
            self.t_start = -1
        else:
            for i in range(self.est,self.let-self.lot+1):
                if (i==self.t_start):
                    count+=1
        #throws warning if count > 1 ??
    
    #Check if the device is turned off or not
    #Return -1 if the device is not properly turned off
    def end_check(self):
        count = 0
        if (self.t_start == -1):
            self.t_end = -1
        elif (self.t_end>(self.t_start+self.lot)):
            self.t_end = self.t_start+self.lot
        elif (self.t_end < (self.t_start+self.lot)):
            self.t_end = self.t_start+self.lot
        else:
            for i in range(self.est+self.lot,self.let+1):
                if(i==self.t_end):
                    self.s_end = i
                    count+=1
        #throw warning when count < 1 ??
    
    #Return the status array of device in 24 hours
    #OUTPUT:
    #Array of 24 values: 1 for activation and 0 for inactivation
    def state(self):
        #Working state of machine in 24 hours
        #Analyse the turn on/off time
        #if user forget to turn machine off, it is off after lot
        for i in range(0,24):
             if (self.t_start-1<= i < self.t_end-1):
                    self.s[i] = 1    
        return self.s
    
    #Calculate the energy consumption in 24 hours
    #OUTPUT:
    #P - energy consumption
    def energy_cal(self, start_time=0, end_time=0):
        #Call other previous functions, except for setting time
        #self.t_start = start_time
        #self.t_end = end_time
        if(start_time==0 and end_time==0):
            self.get_time()
        else:
            self.t_start=start_time
            self.t_end=end_time
        self.start_check()
        self.end_check()
        self.state()
        self.P = self.E*self.s
        #print(self.P)
        return self.P
    #shai add
    def energy_total(self):
        self.totalE=sum(self.P)
        #print(self.totalE)
        return self.totalE

#test object
'''washer = Device(9,18,1,6,"washer")
washer.display()   
washer.energy_cal()
washer.energy_total()'''
