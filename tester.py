import json

with open('Data/Misc/CustomSprites.json', 'r') as cs:
    d = json.load(cs)

d['-'][-1] = False

with open('Data/Misc/CustomSprites.json', 'w') as cs:
    json.dump(d, cs)
    print(d)