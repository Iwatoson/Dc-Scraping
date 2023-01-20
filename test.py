import json

with open("TraditionalColors.json", "r") as file:
    categorys = set()
    data = json.load(file)
    for d in data:
        categorys.add(d["category"])
    print(categorys)
