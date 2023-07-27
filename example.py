"""
Wykonanie pobrania dosępnych plików z danymi do wykresów

"""


import os
import json

data = os.listdir(".\\Chart_file")

for index, i in enumerate(data):
    a = i.split("_")
    data[index] = a[0]


with open("App_file\\zmienne.json", "r+", encoding="utf-8") as file:
    read_file = json.load(file)
    read_file["available_charts_data"] = data
    file.seek(0, 0)
    json.dump(read_file, file, ensure_ascii=False, indent=4)
