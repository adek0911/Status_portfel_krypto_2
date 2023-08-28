import requests
import csv
from datetime import datetime
import json

today = datetime.today().strftime("%Y-%m-%d")
status_change = False

with open("Chart_file\\Chart_files\\.status.json", "r") as file:
    load_file: json = json.load(file)
    krypto_list: list = load_file["available_charts_data"]
    status_date: str = load_file["Status_data"]

    # status_date = json.load(file)

print(krypto_list)
print(status_date)
"""Zmienić api na https://www.coingecko.com/en/api/documentation"""
for i in krypto_list:
    req = requests.get(f"https://www.cryptodatadownload.com/cdd/Binance_{i}USDT_d.csv")
    if req.status_code == 200:
        status_change = True
        result = req.text.split("\n", 100)
        del result[:2]
        result = result[:100]
        for index in range(len(result)):
            result[index] = result[index].split(",")
            del result[index][0], result[index][2:5], result[index][3:]
            result[index][0:1] = result[index][0].split(" ")
        with open(
            f"Chart_file\\Chart_files\\{i}_chartdata.csv",
            "w+",
            encoding="UTF-8",
            newline="",
        ) as data_charts:
            write = csv.writer(data_charts)
            write.writerows(result)
if status_change == True:
    with open("Chart_file\\Chart_files\\.status.json", "r+") as status:
        read_json = json.load(status)
        read_json["Status_data"] = today

        status.seek(0, 0)
        json.dump(read_json, status, ensure_ascii=False, indent=4)
