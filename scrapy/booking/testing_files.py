import json

file = open('cities.json')
file = json.load(file)
print(file)