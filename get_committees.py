import requests
import json

GET_COM_URL = "http://localhost:5052/beacon/committees?epoch="

START_EPOCH=9957
END_EPOCH=10101

d = dict()

for i in range(START_EPOCH, END_EPOCH+1):
    print(i)
    r = requests.get(GET_COM_URL + str(i)).json()
    for data in r:
        slot = data['slot']
        com = data['committee']
        index = data['index']
        try:
            d[slot].append(com)
        except:
            d[slot] = list()
            d[slot].append(com)
    
with open('com.json', 'w') as f:
    json.dump(d, f)
