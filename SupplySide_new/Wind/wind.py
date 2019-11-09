import math
#from mysql.connector import Error
import json
import numpy
import requests
import sqlite3


class wind:

    def __init__(self, Ra, location):
        # User input parameters location and Ra - Radius of blade
        self.Ra = Ra
        self.location = location
        fname = 'config.json'
        config=None
        with open(fname) as config_file:
            config = json.load(config_file)
        self.weather_service_url = (config)['config_data']['api_url']
        # Current parameters
        self.T_cur = 0
        self.RH_cur = 0
        self.pda_cur = 0
        self.windspeed_cur = 0
        # Future parameters
        self.T_for = numpy.array([])
        self.RH_for = numpy.array([])
        self.pda_for = numpy.array([])
        self.windspeed_for = numpy.array([])
        # Constants
        # Power coefficient
        self.Cp = 0.4
        # Molar mass of dry air
        self.Mda = 0.029
        # Ideal gas constant
        self.R = 8.134
        # Result of functions
        self.area = 0
        self.p_cur = 0
        self.p_for = 0

    # Get current weather data from database
    # OUTPUT:
    # T - Temperature K
    # pda - Pressure of dry air Pa
    # RH - Humidity %
    #windspeed - m/s
    def get_current_parameters(self):
        req_data = (requests.get(self.weather_service_url+"wind")).json()
        self.T_cur = req_data["Temperature"] + 273.15
        self.pda_cur = req_data["Pressure"]
        self.RH_cur = req_data["Humidity"]/100
        print(req_data)
        self.windspeed_cur = req_data["Windspeed"]

    # Get forecast weather data from database
    # OUTPUT:
    # T_for - Temperature K
    # pda_for - Pressure of dry air
    # RH_for - Humidity %
    #windspeed_for - m/s
    def get_forecast_parameters(self):
        req_data = (requests.get(self.weather_service_url+"windforecast")).json()

        # Generate data list
        # For loop to get 24-hour data
        print(req_data)
        for i in range(0, 24):
            self.T_for = numpy.append(
                self.T_for, req_data[i]['%d' % (i+1)]["Temperature"]+273.15)
            self.pda_for = numpy.append(
                self.pda_for, req_data[i]['%d' % (i+1)]["Pressure"])
            self.RH_for = numpy.append(
                self.RH_for, req_data[i]['%d' % (i+1)]["Humidity"]/100)
            self.windspeed_for = numpy.append(
                self.windspeed_for, req_data[i]['%d' % (i+1)]["WindSpeed"])

    # Display user input parameters
    def display_cus(self):
        print(self.T_for)

    # Calculate the swept area of blade
    # INPUT:
    # Ra - Radius of blade
    # OUTPUT:
    # area - swept area = pi*Ra**2
    def area_cal(self):
        self.area = math.pi*self.Ra**2
        return self.area

    # Calculate the current power generated
    # INPUT:
    # T, pda, RH, windspeed called from .get_current_parameters()
    # OUTPUT:
    # P - Current power generated W
    def energy_cal_cur(self):
        # Get data from get_current_parameters() function
        self.get_current_parameters()
        # Calculate swept area
        self.area_cal()
        # Teten's constants
        c0 = 6.1087
        c1 = 7.5
        c2 = 237.3

        T = self.T_cur
        RH = self.RH_cur
        pda = self.pda_cur
        # partial density of dry air
        p_dry = (pda*self.Mda)/(self.R*T)
        # Saturated vapor pressure
        p_sat = c0*(10**((c1*(T-273.15))/(c2*(T-273.15))))
        # Partial density of water vapor
        p_vap = RH*p_sat
        self.p_cur = p_dry+p_vap
        P = 0.2*(self.area)*(self.p_cur)*((self.windspeed_cur)**3)
        return P

    # Calculate the forecast power generated
    # INPUT:
    # T_for, pda_for, RH_for, windspeed_for called from .get_forecast_parameters()
    # OUTPUT:
    # P - Forecast power generated W
    def energy_cal_for(self):
        # Get data from get_forecast_parameters() function
        self.get_forecast_parameters()
        # Calculate swept area
        self.area_cal()
        # Teten's constants
        c0 = 6.1087
        c1 = 7.5
        c2 = 237.3

        T = self.T_for
        RH = self.RH_for
        pda = self.pda_for
        # partial density of dry air
        p_dry = (self.Mda/self.R)*(pda/T)
        # Saturated vapor pressure
        p_sat = c0*(10**((c1*(T-273.15))/(c2*(T-273.15))))
        # Partial density of water vapor
        p_vap = numpy.multiply(RH, p_sat)
        self.p_for = p_dry+p_vap
        P = 0.2*(self.area) * \
            (numpy.multiply(self.p_for, ((self.windspeed_for)**3)))
        return P


# test object
#
#two = (cus1.energy_cal_for()).tostring()
#print(numpy.fromstring(two,dtype=float))
#cus1.display_cus()
