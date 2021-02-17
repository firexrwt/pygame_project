import json

with open('Data/CustomSprites.json', 'r') as cs:
    d = json.load(cs)
    print(d)