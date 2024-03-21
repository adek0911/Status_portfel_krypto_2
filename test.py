from datetime import datetime
import requests
import json
import ttkbootstrap as ttk
from pprint import pprint
from datetime import timedelta

"""Dont REMOVE request for all users"""

"""Acounts"""
URL = "https://adix0911.eu.pythonanywhere.com/"

headers = {
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDc2NzQyMywianRpIjoiOTM3NWQzMTItZTA2ZS00N2Y2LWI4M2QtODUxMGVjNTNjYTY0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3MTA3Njc0MjMsImV4cCI6MTc0MTg3MTQyM30.xih_Q8-FwW9ocHpU8BsoCULMQwxqEaZrBEDbrgSEbMA"
    # "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDc3OTc2NiwianRpIjoiYjliZTI1MzYtY2E2Ni00MzgwLWFiODgtMWMzODU3MDBiY2IwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3MTA3Nzk3NjYsImV4cCI6MTc0MTg4Mzc2Nn0.i8tAMwxHgoAsh3VCQSMvmLBWpE0Em-z3HXIjPP-NcW4"
}


def req() -> dict:
    # [
    #     {"Account_ID": 1, "Login": "Adrian", "Password": "321321"},
    #     {"Account_ID": 2, "Login": "Admin", "Password": "321"},
    #     {"Account_ID": 3, "Login": "Test", "Password": "Tests"},
    # ]
    """for id 2"""
    # headers = {
    #     # "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDc2NzQyMywianRpIjoiOTM3NWQzMTItZTA2ZS00N2Y2LWI4M2QtODUxMGVjNTNjYTY0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3MTA3Njc0MjMsImV4cCI6MTc0MTg3MTQyM30.xih_Q8-FwW9ocHpU8BsoCULMQwxqEaZrBEDbrgSEbMA"
    #     # "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDc3OTc2NiwianRpIjoiYjliZTI1MzYtY2E2Ni00MzgwLWFiODgtMWMzODU3MDBiY2IwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3MTA3Nzk3NjYsImV4cCI6MTc0MTg4Mzc2Nn0.i8tAMwxHgoAsh3VCQSMvmLBWpE0Em-z3HXIjPP-NcW4"
    # }
    """For id 1 """
    headers = {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDc2NzYwMCwianRpIjoiYWNmOTc3MzEtOGZiZS00MzBmLTlkNGEtMGFiZjk4ZGM1ZGU0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3MTA3Njc2MDAsImV4cCI6MTc0MTg3MTYwMH0.LuSptTM5eeVZpf85FyW68Odm3WboWaMonucft5LB3iQ"
    }
    # result = requests.get(
    #     "https://adix0911.eu.pythonanywhere.com/authorization", headers=headers
    # )
    # result = requests.get("https://adix0911.eu.pythonanywhere.com/create_key/2")
    result = requests.get(
        "https://adix0911.eu.pythonanywhere.com/show_access_keys", headers=headers
    )
    # result = requests.get(
    #     "https://adix0911.eu.pythonanywhere.com/show_access_keys", headers=headers
    # )

    print(result.status_code, result.text)
    # return result


"""Wallets on id"""


def req2() -> None:
    result: list[dict] = requests.get(
        "https://adix0911.eu.pythonanywhere.com/wallets/2"
    ).json()
    print(result)


def req3():
    """GET"""
    # responce = requests.get(
    #     "https://adix0911.eu.pythonanywhere.com/trans_curr/1", headers=headers
    # )
    prep_data = {"date_purchase": "2024-03-05"}  # 2024-03-05
    responce = requests.patch(
        "https://adix0911.eu.pythonanywhere.com/trans_curr/49",
        headers=headers,
        json=prep_data,
    )

    try:
        result = responce.json()
    except:
        pass
    # Dont send a PLN value in request
    print(responce.status_code, result)


def req4():
    pass
    """all great"""
    # with open("Dane\Details_wallet_portfel_1.txt") as file:
    #     file_data = file.readlines()

    # for i in file_data:
    #     val = i.split(",")
    #     data_set = datetime.strptime(val[0], "%d.%m.%Y").strftime("%Y-%m-%d")
    #     status = val[2].replace("Kupno", "BUY").replace("Sprzedaz", "SALE")
    #     quantity = val[5].replace("\n", "")
    #     prep_data = {
    #         "date_purchase": data_set,
    #         "name_currency": val[1],
    #         "status_of_purchase": status,
    #         "price_PLN": val[3],
    #         "price_dollar": val[4],
    #         "quantity": quantity,
    #     }
    #     responce = requests.put(f"{URL}trans_curr/1", json=prep_data)
    #     print(responce.status_code)
    # responce = requests.put(f"{URL}trans_curr/1", json=prep_data).json()
    # print(responce)


def req5():
    # It should by work
    prep_data = {"Name": "Testowiec"}
    responce = requests.put(f"{URL}wallets/1", json=prep_data).json()
    print(responce)


def req6():

    pass


# sep = "-"

# print(f"[{sep: <10}]")
# print(f"[{sep: ^10}]")

req3()

# test = {"dupa": "123", "Tralalala": 1234, "Imie": None}

# for i in test:
#     if test[i] == None:
#         print(i)
