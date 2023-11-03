"""
Wykonanie pobrania dosępnych plików z danymi do wykresów

"""

##Jeszcze nie wprowadzone zmiany do aplikacji
# import os
# import json

# data = os.listdir(".\\Chart_file\\Chart_files")
# del data[0:2]
# for index, i in enumerate(data):
#     data[index] = i.split("_")[0]
# data = tuple(data)
# print(data)

# with open("App_file\\zmienne.json", "r+", encoding="utf-8") as file:
#     read_file = json.load(file)
#     read_file["available_charts_data"] = data
#     file.seek(0, 0)
#     json.dump(read_file, file, ensure_ascii=False, indent=4)

"""Testy działania api"""

# https://www.coingecko.com/api/documentation
from datetime import datetime
import requests

a = datetime.today().strftime("%d/%m/%Y").split("/")
b = datetime(day=int(a[0]), month=int(a[1]), year=int(a[2]))
c = datetime(day=int(a[0]) - 7, month=int(a[1]), year=int(a[2]))
today = int(datetime.today().timestamp())
time_from = datetime(2023, 10, 24).timestamp()
time_to = datetime(2023, 10, 25).timestamp()
d = datetime.fromtimestamp(1697673600000 / 1000)  # from json
f = datetime.fromtimestamp(1698261795000 / 1000)
# e = datetime.today().utctimetuple()
# print(d, f)
ans = requests.get(
    "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7&interval=daily&precision=4"
).json()

for i in ans["prices"]:
    i[0] = datetime.fromtimestamp(i[0] // 1000).strftime("%d/%m/%Y %H:%M")
print(ans["prices"][-1])

# ans = requests.get(
#     "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from=1697580000&to=1698184800&precision=4"
# ).json()
# print(ans)
# ans = {
#     "prices": [
#         [1697580016791, 28497.7987],
#         [1697583601077, 28400.424],
#         [1697587249566, 28417.7218],
#         [1697590836977, 28378.2193],
#         [1697594433940, 28368.3667],
#         [1697598064555, 28471.0746],
#         [1697601624813, 28524.0213],
#         [1697605223617, 28767.3005],
#         [1697608829160, 28671.336],
#         [1697612435827, 28698.2923],
#     ]
# }


# for i in ans["prices"]:
#     i[0] = datetime.fromtimestamp(i[0] // 1000).strftime("%d/%m/%Y %H:%M")

# if i[0][-5:] != "00:00":
#     ans["prices"].remove(i)

# print(ans)
