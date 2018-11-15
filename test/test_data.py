import numpy as np
import matplotlib.pyplot as plt
import time
import requests
x = np.arange(0,1000,1)

noise = np.random.normal(0,1,1000)

y = 10*np.sin(x*np.pi/100)+10 +noise

# plt.plot(x,y)
# plt.show()
# print(len(x))
for i in y:
    res = "http://127.0.0.1:5000/api/temps"
    data = {"value":str(i),"place":"pxl"}
    q = requests.post(res,json=data)
    if q.status_code==200:
        rs = q.json()
        print(rs)

    time.sleep(5)