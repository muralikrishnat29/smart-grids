import requests
import json
buildings = json.loads(requests.get("http://localhost:5050/buildings").content)
print(buildings)
data=[]
for i in range(0,len(buildings)):
    data.append(json.loads(buildings[i]['UDConsumption']))
print(data)
#print(json.loads(json.loads(requests.get("http://localhost:5050/buildings").content)[0]['UDConsumption']))