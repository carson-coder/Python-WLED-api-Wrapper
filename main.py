import requests
import json

endpoint = "http://carson-desk.local/json"

requests.post(endpoint+"/state", json={"seg": [{'id': 0, 'start': 0, 'stop': 1, 'len': 1, 'grp': 1, 'spc': 0, 'of': 0, 'on': True, 'frz': False, 'bri': 255, 'cct': 127, 'col': [[255, 255, 255], [0, 255, 0], [0, 0, 255]], 'fx': 0, 'sx': 128, 'ix': 128, 'pal': 5, 'sel': True, 'rev': False, 'mi': False}]})

# Move seg to the right
# Make seg white
reg = requests.get(endpoint)
start = reg.json()["state"]["seg"][0]["start"]
stop = reg.json()["state"]["seg"][0]["stop"]
start = int(start)
stop  = int(stop)
i = 0
inp = input("Can you see the white segment? (y/n)")
while inp != "n":
    start +=1
    stop += 1
    reg = requests.post(endpoint+"/state", json={"seg": [{'id': 0, 'start': start, 'stop': stop, 'len': 1, 'grp': 1, 'spc': 0, 'of': 0, 'on': True, 'frz': False, 'bri': 255, 'cct': 127, 'col': [[255, 255, 255], [0, 255, 0], [0, 0, 255]], 'fx': 0, 'sx': 128, 'ix': 128, 'pal': 5, 'sel': True, 'rev': False, 'mi': False}]})
    i += 1
    inp = input("Can you see the white segment? (y/n)")
print("The size of your led strip is ", i)