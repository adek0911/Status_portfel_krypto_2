from datetime import datetime
import json
import tkinter as tk
import requests
from Classes import *

root = tk.Tk()
core = tk.Frame(root)
core.configure(bg='#009999', padx=5, pady=5)
core.grid()

top_area = AreaFrame(onFrame=core, height=300, width=350)
middle_area = AreaFrame(onFrame=core, height=100, width=100)
# bottom_area = Area_Frame(onFrame=core, height=100, width=100)
readFile = Read_data()
readFile.read_from_file('App_file\zmienne.json', 'json')
readFile.read_from_file(readFile.jsonFile['Sciezka_portfel_test'], 'txt')


def top_area_ingredients():
    time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    cooldown = ''
    top_area.text_display(f'Status na dzień: {time}', row=0, column=1)
    top_area.text_display(
        f'Włącz odświeżanie danych co {cooldown}', row=0, column=2)
    top_area.button_display(f'Off', row=0, column=3, method='')

    # print(top_area.objList)


top_area_ingredients()


def middle_area_ingrednients():

    def price_wallet(wallet: list):
        kryptoListFromWallet = []

        for i in range(len(wallet)):
            wallet[i][0] += 'USDT'
            price = (requests.get(
                readFile.jsonFile['URL_krypto_price']+wallet[i][0])).json()

            try:
                downloadPrice = float(price['price']).__round__(3)
            except KeyError:
                if wallet[i][0] == 'ARI10USDT':
                    downloadPrice = float(readFile.jsonFile['Cena_ARI10'])
                else:
                    downloadPrice = 0

            pricePln = (downloadPrice *
                        readFile.jsonFile['Cena_Dolar']).__round__(3)
            valuePln = float(wallet[i][3]*pricePln).__round__(2)
            valueDollar = float(wallet[i][3]*downloadPrice).__round__(2)

            def count_percent():

                result = ((profitLost*100)/abs(wallet[i][1])).__round__(2)
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
            pass

        return kryptoListFromWallet

    column_list_walet = ('Nazwa', 'Cena zl', 'Cena $', 'Ilość')
    headings_list_walet = ["Nazwa waluty",
                           "Cena zakupu zł", "Cena zakupu $", "Ilość"]
    middle_area.treeview_display(
        columns=column_list_walet, headings_text=headings_list_walet, row=1, column=0)

    middle_area.add_data_in_treeview(middle_area.objList[0], readFile)

    column_list_price = ('Cena zl', 'Cena $', 'Wartość zl', 'Wartość $',
                         'Zysk/Strata zl', 'Zysk/Strata $', 'Zysk/Strata %')
    headings_list_price = ["Cena aktualna zł", "Cena aktualna $", "Wartość zł",
                           "Wartość $", "Zysk/ Strata zł", "Zysk/ Strata $", "Zysk/ Strata %"]
    middle_area.treeview_display(
        columns=column_list_price, headings_text=headings_list_price, row=1, column=1)

    middle_area.add_data_in_treeview_v2(
        middle_area.objList[1], price_wallet(readFile.flatFile))
    # print(price_wallet(readFile.flatFile))


middle_area_ingrednients()


root.mainloop()
