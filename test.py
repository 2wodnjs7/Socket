import json

path = './server/user.json'

with open(path, "r") as json_file:
    json_data = json.load(json_file)

json_data['user'].append({
    "id" : 2,
    "name" : "qwer1",
    "age" : 1
})

with open(path, 'w') as outfile:
    json.dump(json_data, outfile, indent=4)



print(json_data)