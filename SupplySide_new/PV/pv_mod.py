import math
#import mysql.connector
import json
import os
import numpy
import requests
import sqlite3
from math import sin
from math import radians
#from DataAccessLayer.Weather_Data_Access import Weather_Data_Access


class pv:
    def __init__(self, Area, Emax, Angle_of_Module, Location):
        self.Area = Area
        self.Emax = Emax
        self.Angle_of_Module = Angle_of_Module
        self.Location = Location
        # get current parameters
        self.T_cur = 0  # DUMMY
        self.Lat_cur = 0
        self.Day_of_Year_cur = 0
        self.Shorizontal_cur = 0
        # get future parameters
        self.T_for = numpy.array([])
        self.Lat_for = numpy.array([])
        self.Day_of_Year_for = numpy.array([])
        self.Shorizontal_for = numpy.array([])
        fname = 'config.json'
        config=None
        with open(fname) as config_file:
            config = json.load(config_file)
        self.weather_service_url = (config)['config_data']['api_url']
        # constants

    # get data from database
    def get_current_parameters(self):
        req_data = (requests.get(self.weather_service_url +"PV")).json()
        # DUMMY req_data["Temperature"] + 273.15
        self.T_cur = req_data["Temperature"] + 273.15
        # print(self.T_cur)
        self.Lat_cur = req_data["Latitude"]
        self.Day_of_Year_cur = req_data["DayOfYear"]
        self.Shorizontal_cur = req_data["SolarIrradiance"]

    def get_forecast_parameters(self):
        req_data = (requests.get(self.weather_service_url+"PVforecast")).json()
        # print(req_data)
        # Generate data list
        # For loop to get 24-hour data
        for i in range(0, 24):
          # print(i)
            self.T_for = numpy.append(
                self.T_for, req_data[i]['%d' % (i+1)]["Temperature"]+273.15)
            self.Lat_for = numpy.append(
                self.Lat_for, req_data[i]['%d' % (i+1)]["Latitude"])
            self.Day_of_Year_for = numpy.append(
                self.Day_of_Year_for, req_data[i]['%d' % (i+1)]["DayOfYear"])
            self.Shorizontal_for = numpy.append(
                self.Shorizontal_for, req_data[i]['%d' % (i+1)]["SolarIrradiance"])
            # print(self.T_for,self.Lat_for,self.Day_of_Year_for,self.Shorizontal_for)
    # display

    def display_cus(self):
        print(self.Location, " ", self.Area, " ",
              self.Emax, " ", self.Angle_of_Module)

    # calculate current energy

    def energy_cal_cur(self):
        # Get data from get_current_parameters() function
        self.get_current_parameters()
        Emax = self.Emax
        Area = self.Area
        Angle_of_Module = self.Angle_of_Module
        T = self.T_cur
        Lat = self.Lat_cur
        Day_of_Year = self.Day_of_Year_cur
        Shorizontal = self.Shorizontal_cur
        p_alpha = 90-Lat+23.45 * \
            abs(sin(radians(360*(284+Day_of_Year)/365)))  # angle of sun=alpha
        p_beta = self.Angle_of_Module  # beta
        p_soalr_irradiance = (
            Shorizontal * abs(sin(radians(p_alpha + p_beta))))/sin(p_alpha)
        #p_PR=((((-1)**(T-25-273.15))* ((0.5)**abs(T-25-273.15)))* 100)+14
        p_PR = 100+((-0.5)*(T-25))-14
        # print(p_PR)
        print(Shorizontal)
        p_power_coeff = (Emax / Area)*100
        E = Area*p_power_coeff*p_PR*p_soalr_irradiance
        print("energy is:"+str(E))
        return E

    def energy_cal_for(self):
        # Get data from get_forecast_parameters() function
        self.get_forecast_parameters()
        Emax = self.Emax
        Area = self.Area
        Angle_of_Module = self.Angle_of_Module
        T = self.T_for  # numpy
        Lat = self.Lat_for  # numpy
        Day_of_Year = self.Day_of_Year_for  # numpy
        Shorizontal = self.Shorizontal_for  # numpy
        a1 = numpy.ones(24)
        arr90 = 90*a1
        arr284 = 284*a1
        arr3 = (366/365)*a1
        var1 = numpy.array([])
        var2 = numpy.array([])
        var1 = numpy.add((23.45*numpy.sin(numpy.radians(numpy.multiply(arr3,
                                                                       numpy.add(arr284, Day_of_Year.astype(int)))))), arr90)
        # p_alpha=90-Lat+23.45*sin(radians(360*(284+Day_of_Year)/365))#angle of sun=alpha
        p_alpha = numpy.subtract(var1, Lat)
        p_beta = self.Angle_of_Module  # beta
        p_beta_ar = p_beta*a1
        var2 = numpy.divide(numpy.absolute(numpy.sin(numpy.radians(
            p_alpha + p_beta_ar))), numpy.absolute(numpy.sin(numpy.radians(p_alpha))))
        p_soalr_irradiance = numpy.multiply(Shorizontal, var2)
        #p_PR=((((-1)**(T-25-273.15))* ((0.5)**abs(T-25-273.15)))* 100)+14
        p_PR = ((-0.5)*(T-273.15-25))+14
        p_power_coeff = (Emax / Area)
        E = Area*p_power_coeff*numpy.multiply(p_PR, p_soalr_irradiance)*.001
        E = numpy.around(E, 3)
        print("energy forecast in kilowatt is:"+str(E))
        return E


# test object
cus1 = pv(20, 75, 60, "Stuttgart")  # Area,Emax,Angle_of_Module,Location):
cus1.get_forecast_parameters()
cus1.energy_cal_for()
cus1.get_forecast_parameters()