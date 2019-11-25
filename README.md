# smart-grids

This project is about ``Smart Energy Systems Lab: Electricity Demand-Response Management''. This gives us information on existing functionality of the microgrid, challenges involved, features that can be added on the existing architecture. Microgrid works as a local energy provider for domestic buildings to reduce energy expenses and gas emissions by utilizing distributed energy resources (DERs). The rapid advances in computing and communication capabilities enable the concept smart buildings become possible. Most energy-consuming household tasks do not need to be performed at specific times but rather within a preferred time. If these types of tasks can be coordinated among multiple homes so that they do not all occur at the same time yet still satisfy customers’ requirement, the energy cost and power peak demand could be reduced.

## Architecture of the system

The system consists of different REST API based web services with an User Interface to guide the user for a Smart Microgrid Demand Response Management system.

![Architecture of the system](https://github.com/muralikrishnat29/smart-grids/blob/master/pictures/architecture.png)

From the figure, the function and interaction of modules can be de-
duced: \
– Weather Service: uses data from Weatherbit.io API to provide the current
and forecast of 24 hours weather data. This service has the capability to get
latest data for the current hour through last update time check (both for
current data and forecast data) \
– Supply Service: when requested (either from optimisation service or UI),
this web service uses data from Weather Service and calculates energy gen-
erated from Simulated Wind Turbine and PV components, stores them in
the Database and gives data to the requested module. Apart from these,
it updates, stores and retrieves battery data. Not to forget, new Wind tur-
bine and solar panel can be added to the system through this service. Also,
battery specifications can be updated. \
– Demand Service: when requested, Demand Service which is an web service
gets information like building’s energy consumption [both total and con-
trolled devices energy consumption]. Also, new buildings and devices can
be added into the system through this service. Also, it has the capability
to update device information like Start Time, Stop Time which is used by
optimisation service to operate the devices towards the optimisation goal. \
– Pricing Unit: is also a web service that provides us with pricing data of energy \ 
• For current hour \
• For current day’s 24 hours \
• For next day’s 24 hours \
• Forecast for the next 24 hours \
– Optimisation: uses data from Supply Service, Demand Service and Pricing
Unit to optimise the system towards the goals. It uses Gurobi module to
optimise the operation of devices in building. Once optimum schedule is
obtained, the start and end time of devices are updated in the Demand Side
through the web service interface. Also, battery data is updated through
supply side Service.\
– User Interface UI: is created using NUXT JS (a framework based on Vue
JS) and Vuetify (Material design CSS Framework for VUE JS) [8]. This unit
has fluidic design, interactive charts and forms to obtain information from
user and also to display information from Supply Service, Demand Service,
Pricing Unit and Optimisation unit.\

## Get Started

To get started, requirements of respective web services are to be installed in a python virtual environment. Please follow the ReadMe guide of each web service and UI app to get started.

## User Interface Design:

### Home Page:

![Home Page](https://github.com/muralikrishnat29/smart-grids/blob/master/pictures/introduction.jpeg)

### Energy Generation Information:

![Energy Generation Information](https://github.com/muralikrishnat29/smart-grids/blob/master/pictures/energy%20generation%20information.jpeg)

### Others:

There are several other images to demonstrate the user interface in the link. \
[Images](https://github.com/muralikrishnat29/smart-grids/blob/master/pictures)

