from datetime import datetime
import json
import ttkbootstrap as ttk
import requests
import threading as th
from Classes import AreaFrame, ReadData, TopFrame, ReadFile
import tkinter.messagebox as msgbox

root = ttk.Window(themename="darkly")
root.style.configure(".", bordercolor="", borderwidth=0, font=("Helvetica", 9))
root.style.configure("primary.Treeview", rowheight=22, borderwidth=0)
root.style.configure("primary.TEntry", font=("Helvetica", 12))
root.style.configure("primary.TButton", font=("Helvetica", 11), buttonuprelief="")
root.style.configure("Treeview.Heading", font=("Helvetica", 11))
root.style.configure("12_label.TLabel", font=("Helvetica", 12))
core = ttk.Frame(root)
core.grid()
top_area = AreaFrame(onFrame=core, row=0, column=0, columnspan=4, sticky="ew")
middle_area = AreaFrame(onFrame=core, row=1, column=0, columnspan=4)
bottom1_area = AreaFrame(onFrame=core, row=2, column=0, sticky="w")
bottom2_area = AreaFrame(onFrame=core, row=2, column=1, sticky="n")
bottom3_area = AreaFrame(onFrame=core, row=2, column=2, sticky="n")

# window for login
logins_window = TopFrame()

logins_area = AreaFrame(onFrame=logins_window.frame)
# purchase_details_window = TopFrame()
# purchase_details_area = AreaFrame(onFrame=purchase_details_window.frame)

# Trzeba to rozbić by każdy obiekt zawierał inne pobrane dane
readFile = ReadData()
# readFile.file_list[0] json zmienne
readFile.read_from_file("App_file\zmienne.json", "json")
# readFile.file_list[0]["Sciezka_portfel"],"txt",
readFile.read_from_file(readFile.file_list[0]["Sciezka_portfel"], "txt")


def time_now() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def price_wallet(wallet: list) -> list:
    """Prepare request, download krypto price, count value"""
    kryptoListFromWallet = []
    # 4 zmienne do wyliczenia i dodania do listy dane
    """Download dolar price and update every 24h"""
    with open("App_file\zmienneApiDolar.json", mode="r+", encoding="UTF-8") as file:
        last_time = datetime.now().strftime("%d-%m-%Y")
        read_file = json.load(file)
        if read_file["Stable_price"]["Dolar"][1] != last_time:
            response = requests.get(read_file["url"], headers=read_file["headers"])
            status_code = response.status_code
            if status_code == 200:
                result = json.loads(response.text)
                read_file["Stable_price"]["Dolar"] = (
                    result["quotes"]["USDPLN"],
                    last_time,
                )
                file.seek(0, 0)
                json.dump(read_file, file, ensure_ascii=False, indent=4)

    pre_url = '","'.join(
        [
            f"{i[0]}USDT"
            for i in wallet
            if i[0] not in readFile.file_list[0]["Charts_no_krypto_data"]
        ]
    )
    url = (
        requests.get(
            f'https://api.binance.com/api/v3/ticker/price?symbols=["{pre_url}"]'
        )
    ).json()

    prices = {i["symbol"]: float(i["price"]).__round__(4) for i in url}
    invest_val = 0
    val_of_wallet_pln = 0
    Profit_zl = 0
    Profit_dollar = 0
    # count price for each cryptocorrency
    for i in range(len(wallet)):
        try:
            download_price = prices[wallet[i][0] + "USDT"]
        except KeyError:
            if wallet[i][0] == "ARI10":
                download_price = readFile.file_list[0]["Cena_ARI10"]
            else:
                download_price = 0

        price_pln = (download_price * read_file["Stable_price"]["Dolar"][0]).__round__(
            3
        )
        value_pln = (float(wallet[i][3]) * price_pln).__round__(2)
        value_dollar = (float(wallet[i][3]) * download_price).__round__(2)
        profit_lost_zl = (value_pln - float(wallet[i][1])).__round__(2)
        profit_lost_dollar = (value_dollar - float(wallet[i][2])).__round__(2)
        # Value for frame result in app
        Profit_zl += profit_lost_zl
        Profit_dollar += profit_lost_dollar
        val_of_wallet_pln += value_pln
        invest_val += float(wallet[i][1])

        def count_percent():
            result = ((profit_lost_zl * 100) / abs(float(wallet[i][1]))).__round__(2)
            return f"{result} %"

        kryptoListFromWallet.append(
            [
                price_pln,
                download_price,
                value_pln,
                value_dollar,
                profit_lost_zl,
                profit_lost_dollar,
                count_percent(),
            ]
        )
    readFile.result_values["Profit_zl"] = Profit_zl.__round__(2)
    readFile.result_values["Profit_dollar"] = Profit_dollar.__round__(2)
    readFile.result_values["Profit_%"] = (
        (Profit_zl * 100) / val_of_wallet_pln.__round__(2)
    ).__round__(2)
    readFile.result_values["Value_of_wallet"] = val_of_wallet_pln.__round__(2)
    readFile.result_values["Invest_value"] = invest_val.__round__(2)
    return kryptoListFromWallet


def button_change_time() -> None:
    top_area.objList[2].configure(text=f"Status na dzień: {time_now()}")
    th.Thread(
        target=middle_area.add_data_in_treeview(
            middle_area.objList[1], price_wallet(readFile.file_list[1])
        )
    ).start()


# Top area in main app
def top_area_ingredients() -> None:
    """List of wallets, current data and button with refresh corrent value of invest"""
    # wallet_lists = ["Portfel1"]
    with open("App_file\Wallets.json", "r") as file:
        tmp = json.load(file)
        wallet_lists = tmp["Admin"]  # temporary
    top_area.text_display(f"Wybierz portfel:", row=0, column=0, padx=5)
    top_area.combobox_display(
        values=wallet_lists, width=12, row=0, column=1, padx=15, pady=10
    )
    top_area.text_display(
        f"Status na dzień: {time_now()}",
        row=0,
        column=2,
        padx=30,
        style="12_label.TLabel",
    )  # was padx=95
    top_area.text_display(
        f"Odśwież wyliczenia portfela: ",
        row=0,
        column=3,
        sticky="e",
        padx=5,
    )
    top_area.button_display(
        "Odśwież",
        row=0,
        column=4,
        command=button_change_time,
        padx=5,
        pady=5,
    )


def check_logins(login, password) -> None:
    with open("App_file\credentials.json", "r") as file:
        logins_dict = json.load(file)
    if login in logins_dict and password == logins_dict[login]:
        root.deiconify()
        logins_window.frame.destroy()
    else:
        logins_area.objList[4].delete(0, "end")


def warning_mess() -> None:
    mes = msgbox.askokcancel(
        "Czy wyłączyć aplikację",
        "Jeżeli wybierzesz ok aplikacja zostanie zamknięta.",
    )
    if mes:
        root.destroy()


def logins_area_ingredients() -> None:
    """Place with entry login and passowrd for verification"""
    logins_area.text_display(
        text="Podaj login i hasło do portfela: ",
        row=0,
        column=0,
        columnspan=2,
        padx=15,
    )
    logins_area.text_display(text="Login: ", row=1, column=0)
    logins_area.entry_display(justify="center", row=1, column=1, state="normal")
    logins_area.text_display(text="Hasło: ", row=2, column=0)
    logins_area.entry_display(justify="center", row=2, column=1, state="normal")
    logins_area.button_display(
        text="Zatwiedź",
        width=10,
        row=3,
        column=0,
        columnspan=2,
        padx=5,
        pady=5,
        command=lambda: check_logins(
            logins_area.objList[2].get(), logins_area.objList[4].get()
        ),
    )
    logins_window.frame.protocol("WM_DELETE_WINDOW", warning_mess)
    logins_window.frame.bind(
        "<Return>", lambda event=None: logins_area.objList[5].invoke()
    )
    # only for tests
    logins_area.objList[2].insert(0, "Admin")
    logins_area.objList[4].insert(0, "123")
    # check_logins(logins_area.objList[2].get(), logins_area.objList[4].get())
    root.withdraw()
    # hide window
    # show window
    # win.deiconify()
    # działa tylko trzeba ustawić
    logins_area.frame.wait_window()


# Middle area in main app
def middle_area_ingrednients() -> None:
    """Wallet data in treeView and calculation of wallet"""
    column_tuple_walet = ("Nazwa", "Cena zl", "Cena $", "Ilość")
    headings_list_walet = ["Nazwa waluty", "Cena zakupu zł", "Cena zakupu $", "Ilość"]
    middle_area.treeview_display(
        columns=column_tuple_walet, headings_text=headings_list_walet, row=1, column=0
    )

    middle_area.add_data_in_treeview(
        middle_area.objList[0], readFile.file_list[1], "txt"
    )

    column_tuple_price = (
        "Cena zl",
        "Cena $",
        "Wartość zl",
        "Wartość $",
        "Zysk/Strata zl",
        "Zysk/Strata $",
        "Zysk/Strata %",
    )
    headings_list_price = [
        "Cena akt. zł",
        "Cena akt. $",
        "Wartość zł",
        "Wartość $",
        "Zysk/ Strata zł",
        "Zysk/ Strata $",
        "Zysk/ Strata %",
    ]
    middle_area.treeview_display(
        columns=column_tuple_price, headings_text=headings_list_price, row=1, column=1
    )
    th.Thread(
        target=middle_area.add_data_in_treeview(
            middle_area.objList[1], price_wallet(readFile.file_list[1])
        )
    ).start()

    def selected_choice(val: int):
        if val == 0:
            AreaFrame.choice_portfel(
                middle_area.objList[val], middle_area.objList[val + 1]
            )
        else:
            AreaFrame.choice_portfel(middle_area.objList[1], middle_area.objList[0])

    middle_area.objList[0].bind("<<TreeviewSelect>>", lambda _: selected_choice(0))
    middle_area.objList[1].bind("<<TreeviewSelect>>", lambda _: selected_choice(1))


# bottom 1/3 area in main app
def chart_area_ingredients() -> None:
    """Charts with data"""
    bottom1_area.text_display(
        "Wybierz krypto do wyświetlania wykresu:", row=0, column=0
    )
    krypto_wallet_list = [
        i[0]
        for i in readFile.file_list[1]
        if i[0] not in readFile.file_list[0]["Charts_no_krypto_data"]
    ]
    bottom1_area.combobox_display(
        values=krypto_wallet_list,
        row=0,
        column=1,
        width=10,
        pady=5,
    )
    bottom1_area.chart(krypto_wallet_list)


def purchers_area_ingredients() -> None:
    def upadate_data_filtr():
        result = []
        for i in range(len(purchase_details_data.file_data)):
            tmp = datetime.strptime(
                purchase_details_data.file_data[i][0][6:], "%Y"
            ).strftime("%Y")
            if tmp not in result:
                result.append(tmp)

        return result

    def update_filtr(value):
        result = []
        for i in range(len(purchase_details_data.file_data)):
            result.append(purchase_details_data.file_data[i][value])
        return list(set(result))

    purchase_details_window = TopFrame()
    purchase_details_area = AreaFrame(onFrame=purchase_details_window.frame)
    purchase_details_area.text_display(text="Data", row=0, column=0, columnspan=2)
    purchase_details_area.text_display(text="Nazwa", row=0, column=2, columnspan=2)
    purchase_details_area.text_display(
        text="Sprzedaż/Kupno", row=0, column=4, columnspan=2
    )
    purchase_details_data = ReadFile("Dane\Szczegoly_zakupow_org.txt", "txt")

    # purchase_details_data_filtr = {"Wszystko"}
    purchase_details_data_filtr = upadate_data_filtr()
    # name tmp only for tests
    purchase_details_nazwa_filtr = update_filtr(1)
    purchase_details_zakup_filtr = update_filtr(2)

    purchase_details_area.combobox_display(
        values=purchase_details_data_filtr, width=10, row=1, column=0, columnspan=2
    )
    purchase_details_area.combobox_display(
        values=purchase_details_nazwa_filtr, width=10, row=1, column=2, columnspan=2
    )
    purchase_details_area.combobox_display(
        values=purchase_details_zakup_filtr, width=10, row=1, column=4, columnspan=2
    )
    tree_view_headers = [
        "Data",
        "Nazwa",
        "Sprzedaż/ Kupno",
        "Cena zł",
        "Cena $",
        "Ilość",
    ]
    purchase_details_area.treeview_display(
        columns=tuple(tree_view_headers),
        headings_text=tree_view_headers,
        row=2,
        column=0,
        columnspan=6,
        width=100,
    )
    # purchase_details_area.objList[6].heading("#0", text="\n")
    # add data from file , create new instant and download data

    # 6 entry
    for i in range(6):
        purchase_details_area.entry_display(row=3, column=i)

    # 6 button
    button_names = ("Wyczyść", "Wybierz", "Zamień", "Dodaj", "Usuń", "Aktualizuj")
    for i in range(6):
        purchase_details_area.button_display(text=button_names[i], row=4, column=i)

    # treeview with unit price
    unit_price_column = ("Nazwa", "Cena jedn. zł", "Cena jedn. $", "Ilość")
    unit_price_column2 = ["Nazwa", "Cena jedn. zł", "Cena jedn. $", "Ilość"]

    purchase_details_area.treeview_display(
        columns=unit_price_column,
        headings_text=unit_price_column2,
        row=5,
        column=0,
        columnspan=6,
    )

    purchase_details_area.add_data_in_treeview(
        purchase_details_area.objList[6], purchase_details_data.file_data, "txt"
    )

    def calculate_unit_price() -> list:
        # Zastanowić się czy nie lepiej żeby zwracał listę/tuple jako odpowiedź
        result_list = []
        unique_name = []

        quantity = 0  # ilość
        for name in purchase_details_data.file_data:
            if not name[1] in unique_name and name[2] == "Kupno":
                unique_name.append(name[1])
                result_list.append([])
                result_list[unique_name.index(name[1])].extend(
                    [name[3], name[4], name[5]]
                )
            elif name[2] == "Kupno":
                for i in range(3):
                    result_list[unique_name.index(name[1])][i] += name[i + 3].__round__(
                        5
                    )
            elif name[2] == "Sprzedaz":
                for i in range(3):
                    result_list[unique_name.index(name[1])][i] -= name[i + 3].__round__(
                        5
                    )

        for i in range(len(result_list)):
            if result_list[i][0] < 0:
                result_list[i][0] = 0
                result_list[i][1] = 0
            if result_list[i][2] != 0:
                pln = (result_list[i][0] / result_list[i][2]).__round__(2)
                dollar = (result_list[i][1] / result_list[i][2]).__round__(2)
                result_list[i].extend([pln, dollar])

        output_list = []
        for i in range(len(result_list)):
            if result_list[i][2] != 0:
                output_list.append(
                    [
                        unique_name[i],
                        result_list[i][3],
                        result_list[i][4],
                        result_list[i][2],
                    ]
                )
        return output_list
        # [95.04, 25.56, 0.0579, 1641.45, 441.45]
        # dane w pliku data, nazwa, kupno/sprzedaz, cena_z, cena_dolar,ilość
        # pobrać nazwy, cena_złotówki, cena_dolar, ilość,

    purchase_details_area.add_data_in_treeview(
        purchase_details_area.objList[19], calculate_unit_price()
    )

    # unit price column and data


# bottom 2/3 area in main app
def buttons_area_ingredients() -> None:
    """Buttons with program options"""
    bottom2_area.button_display(
        text="Szczegóły zakupów",
        row=0,
        column=0,
        padx=5,
        pady=15,
        width=18,
        command=purchers_area_ingredients,
    )
    bottom2_area.button_display(
        text="Odśwież portfel", row=1, column=0, padx=5, pady=15, width=15
    )
    bottom2_area.button_display(
        text="Bot trading", row=2, column=0, padx=5, pady=15, width=12
    )
    bottom2_area.button_display(text="Wyloguj", row=3, column=0, pady=15, width=10)
    bottom2_area.button_display(
        text="Exit", row=4, column=0, command=root.destroy, padx=5, pady=15
    )


# bottom 3/3 area in main app
def result_area_ingredients() -> None:
    """Result in one table about of wallet"""

    bottom3_area.text_display(
        text="Podsumowanie portfela",
        row=0,
        column=0,
        columnspan=2,
        style="12_label.TLabel",
    )
    bottom3_area.text_display(text="Ogólny Zysk/Strata zł wynosi: ", row=1, column=0)
    bottom3_area.entry_display(
        result_value=readFile.result_values["Profit_zl"],
        state="readonly",
        row=1,
        column=1,
        insert=True,
    )
    bottom3_area.text_display(text="Ogólny Zysk/Strata $ wynosi: ", row=2, column=0)
    bottom3_area.entry_display(
        result_value=readFile.result_values["Profit_dollar"],
        state="readonly",
        row=2,
        column=1,
        insert=True,
    )
    bottom3_area.text_display(text="Ogólny Zysk/Strata % wynosi: ", row=3, column=0)
    bottom3_area.entry_display(
        result_value=readFile.result_values["Profit_%"],
        state="readonly",
        text="%",
        row=3,
        column=1,
        insert=True,
    )
    bottom3_area.text_display(text="Wartość portfela w zł wynosi: ", row=4, column=0)
    bottom3_area.entry_display(
        result_value=readFile.result_values["Value_of_wallet"],
        state="readonly",
        row=4,
        column=1,
        insert=True,
    )
    bottom3_area.text_display(text="Wartość zaiwestowana wynosi: ", row=5, column=0)
    bottom3_area.entry_display(
        width=10,
        result_value=readFile.result_values["Invest_value"],
        state="readonly",
        row=5,
        column=1,
        insert=True,
    )


def main() -> None:
    # For test only
    logins_area_ingredients()
    top_area_ingredients()
    th.Thread(target=middle_area_ingrednients()).start()
    # Wywala mi szerkość treeview headers
    th.Thread(target=chart_area_ingredients()).start()
    # for test only
    # purchers_area_ingredients()
    buttons_area_ingredients()
    result_area_ingredients()

    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
