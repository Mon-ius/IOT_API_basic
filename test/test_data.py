import numpy as np
import matplotlib.pyplot as plt
import time
import requests

User = [("password","admin")]
Sensor = ["SensorTest_1","SensorTest_2"]

x = np.arange(0,1000,1)
noise = np.random.normal(0,1,1000)
y = 10*np.sin(x*np.pi/100)+10 +noise

# plt.plot(x,y)
# plt.show()
# print(len(x))
for i in User:
    reg = "http://127.0.0.1:5000/api/users"
    ses = "http://127.0.0.1:5000/api/sensors"
    data = "http://127.0.0.1:5000/api/dataset"

    u = {"name":i[0],"password":i[1],"email":"ts@ts.com"}
    regQ1 = requests.post(reg,json=u)
    for j in Sensor:
        sesQ1 = requests.post(ses,json={"stype":j},auth=i)
        print(sesQ1.json())
        uuid = sesQ1.json()['sensor']['uuid']
        x = np.arange(0,1000,1)
        noise = np.random.normal(0,1,1000)
        y = 10*np.sin(x*np.pi/100)+10 +noise
        for d in y[:60]:
            dataQ1  = requests.post(data,json={"value":d},headers={"uuid":uuid})
            rs  = dataQ1.json()
            print(rs)
            time.sleep(5)