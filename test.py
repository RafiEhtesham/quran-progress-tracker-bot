import json

para = 4
quarter = 3
member = "1223"

with open('data.json', 'r+') as file:
    dic = json.load(file)
    dic[member] = [para, quarter]
    file.seek(0)
    json.dump(dic, file, indent= 4)
