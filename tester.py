import json

with open('Data/Misc/CustomSprites.json', 'r') as cs:
    d = json.load(cs)
    print(d)