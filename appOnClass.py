from datetime import datetime
import json
import tkinter as tk
import ttkbootstrap as ttk
import requests
import threading as th
from Classes import AreaFrame, ReadData

# from ttkbootstrap import Style

root = ttk.Window(themename="darkly")
root.style.configure('.', font=('Helvetica', 11))
root.style.configure('Treeview.Heading', font=('Helvetica', 12))
core = ttk.Frame(root)
core.grid()


top_area = AreaFrame(onFrame=core, height=300, width=350)
middle_area = AreaFrame(onFrame=core, height=100, width=100)
bottom_area = AreaFrame(onFrame=core, height=100, width=100)
readFile = ReadData()
readFile.read_from_file('App_file\zmienne.json', 'json')
readFile.read_from_file(readFile.file_list[0]['Sciezka_portfel_test'], 'txt')


def time_now():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


def price_wallet(wallet: list):
    '''Prepare request, download krypto price, count value, return data[]'''
    kryptoListFromWallet = []

    '''Download dolar price'''
    with open('App_file\zmienneApiDolar.json', mode='r+', encoding='UTF-8') as file:
        last_time = datetime.now().strftime('%d-%m-%Y')
        read_file = json.load(file)
        if read_file['Stable_price']['Dolar'][1] != last_time:
            response = requests.get(
                read_file['url'], headers=read_file['headers'])
            status_code = response.status_code
            if status_code == 200:
                result = json.loads(response.text)
                read_file['Stable_price']['Dolar'] = (
                    result['quotes']['USDPLN'], last_time)
                file.seek(0, 0)
                json.dump(read_file, file, ensure_ascii=False, indent=4)

    pre_url = '","'.join(
        [f"{i[0]}USDT" for i in wallet if i[0] != 'ARI10'])
    url = (requests.get(
        f'https://api.binance.com/api/v3/ticker/price?symbols=["{pre_url}"]')).json()

    prices = {i['symbol']: float(i['price']).__round__(4) for i in url}

    for i in range(len(wallet)):
        try:
            downloadPrice = prices[wallet[i][0]+'USDT']
        except KeyError:
            if wallet[i][0] == 'ARI10':
                downloadPrice = float(readFile.file_list[0]['Cena_ARI10'])
            else:
                downloadPrice = 0

        pricePln = (downloadPrice *
                    read_file['Stable_price']['Dolar'][0]).__round__(3)
        valuePln = (float(wallet[i][3])*pricePln).__round__(2)
        valueDollar = (float(wallet[i][3])*downloadPrice).__round__(2)

        def count_percent():

            result = ((profitLost*100) /
                      abs(float(wallet[i][1]))).__round__(2)
            return f'{result} %'

        profitLost = (valuePln-float(wallet[i][1])).__round__(2)
        kryptoListFromWallet.append([
            pricePln,
            downloadPrice,
            valuePln,
            valueDollar,
            profitLost,
            (valueDollar-float(wallet[i][2])).__round__(2),
            count_percent()
        ])

    return kryptoListFromWallet


switch_button = False


def button_change_time():
    global switch_button
    if switch_button == False:
        top_area.objList[0].configure(text=f'Status na dzień: {time_now()}')
        top_area.objList[2].configure(text='ON')
        th.Thread(target=middle_area.add_data_in_treeview(
            middle_area.objList[1], price_wallet(readFile.file_list[1]))).start()

        switch_button = True
    elif switch_button == True:
        top_area.objList[2].configure(text='OFF')
        switch_button = False


def top_area_ingredients():

    top_area.text_display(f'Status na dzień: {time_now()}', row=0, column=1)
    top_area.text_display(
        f'Włącz odświeżanie danych co {readFile.file_list[0]["czas_refresh"]}s', row=0, column=2)
    top_area.button_display(f'OFF', row=0, column=3,
                            method=button_change_time)
    # print(top_area.objList[2].pressed)


top_area_ingredients()


def middle_area_ingrednients():

    column_list_walet = ('Nazwa', 'Cena zl', 'Cena $', 'Ilość')
    headings_list_walet = ["Nazwa waluty",
                           "Cena zakupu zł", "Cena zakupu $", "Ilość"]
    middle_area.treeview_display(
        columns=column_list_walet, headings_text=headings_list_walet, row=1, column=0)

    middle_area.add_data_in_treeview(
        middle_area.objList[0], readFile.file_list[1], 'txt')

    column_list_price = ('Cena zl', 'Cena $', 'Wartość zl', 'Wartość $',
                         'Zysk/Strata zl', 'Zysk/Strata $', 'Zysk/Strata %')
    headings_list_price = ["Cena aktualna zł", "Cena aktualna $", "Wartość zł",
                           "Wartość $", "Zysk/ Strata zł", "Zysk/ Strata $", "Zysk/ Strata %"]
    middle_area.treeview_display(
        columns=column_list_price, headings_text=headings_list_price, row=1, column=1)
    # print(readFile.file_list[1])
    middle_area.add_data_in_treeview(
        middle_area.objList[1], price_wallet(readFile.file_list[1]))
    # Config table

    def pomocnicza(val: int):
        if val == 0:
            AreaFrame.choice_portfel(
                middle_area.objList[val], middle_area.objList[val+1])
        else:
            AreaFrame.choice_portfel(
                middle_area.objList[1], middle_area.objList[0])
    middle_area.objList[0].bind('<<TreeviewSelect>>', lambda _: pomocnicza(0))
    middle_area.objList[1].bind('<<TreeviewSelect>>', lambda _: pomocnicza(1))


middle_area_ingrednients()


def bottom_area_ingredients():

    pass


bottom_area_ingredients()


root.mainloop()
