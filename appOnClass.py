from datetime import datetime
import os
import json
import ttkbootstrap as ttk
import requests
import threading as th
import tkinter.messagebox as msgbox
from Classes import AreaFrame, ReadData, TopFrame, ReadFile
from details_wallet import purchers_area_ingredients

root = ttk.Window(themename="darkly")
# before
# root.style.configure(".", bordercolor="", borderwidth=0, font=("Helvetica", 9))

root.style.configure(".", bordercolor="", borderwidth=0, font=("Helvetica", 10))
root.style.configure(
    "11_label.TLabel", bordercolor="", borderwidth=0, font=("Helvetica", 11)
)
root.style.configure("primary.Treeview", rowheight=22, borderwidth=0)
root.style.configure("Treeview.Heading", font=("Helvetica", 11))

root.style.configure("primary.TEntry", font=("Helvetica", 12))
root.style.configure("primary.TButton", font=("Helvetica", 11), buttonuprelief="")
root.style.configure("12_label.TLabel", font=("Helvetica", 12))
core = ttk.Frame(root)
core.grid()
top_area = AreaFrame(onFrame=core, row=0, column=0, columnspan=4, sticky="ew", padx=5)
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
variable_json_File = ReadData()
# readFile.file_list[0] json zmienne
variable_json_File.read_from_file("App_file\zmienne.json", "json", "variable_json")
# readFile.file_list[0]["Sciezka_portfel"],"txt",

global user_login


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
                file.truncate()
                json.dump(read_file, file, ensure_ascii=False, indent=4)

    pre_url = '","'.join(
        [
            f"{i[0]}USDT"
            for i in wallet
            if i[0]
            in variable_json_File.file_dict["variable_json"]["available_charts_data"]
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

    def count_percent_value(profit_pln: float, amount: float):
        result = ((profit_pln * 100) / abs(float(amount))).__round__(2)
        return f"{result} %"

    for index, _ in enumerate(wallet):
        try:
            download_price = prices[wallet[index][0] + "USDT"]
        except KeyError:
            if wallet[index][0] == "ARI10":
                download_price = variable_json_File.file_dict["variable_json"][
                    "Cena_ARI10"
                ]
            else:
                download_price = 0

        price_pln = (download_price * read_file["Stable_price"]["Dolar"][0]).__round__(
            3
        )
        value_pln = (float(wallet[index][3]) * price_pln).__round__(2)
        value_dollar = (float(wallet[index][3]) * download_price).__round__(2)
        profit_lost_zl = (value_pln - float(wallet[index][1])).__round__(2)
        profit_lost_dollar = (value_dollar - float(wallet[index][2])).__round__(2)
        # Value for frame result in app
        Profit_zl += profit_lost_zl
        Profit_dollar += profit_lost_dollar
        val_of_wallet_pln += value_pln
        invest_val += float(wallet[index][1])

        kryptoListFromWallet.append(
            [
                price_pln,
                download_price,
                value_pln,
                value_dollar,
                profit_lost_zl,
                profit_lost_dollar,
                count_percent_value(profit_lost_zl, wallet[index][1]),
            ]
        )

    variable_json_File.result_values["Profit_zl"] = Profit_zl.__round__(2)
    variable_json_File.result_values["Profit_dollar"] = Profit_dollar.__round__(2)
    variable_json_File.result_values["Profit_%"] = (
        (Profit_zl * 100) / val_of_wallet_pln.__round__(2)
    ).__round__(2)
    variable_json_File.result_values["Value_of_wallet"] = val_of_wallet_pln.__round__(2)
    variable_json_File.result_values["Invest_value"] = invest_val.__round__(2)
    return kryptoListFromWallet


def refresh_result_data():
    for i in range(2, 11, 2):
        bottom3_area.objList[i]["state"] = "normal"
        bottom3_area.objList[i].delete(0, "end")
        if i == 2:
            bottom3_area.objList[i].insert(
                0, variable_json_File.result_values["Profit_zl"]
            )
        if i == 4:
            bottom3_area.objList[i].insert(
                0, variable_json_File.result_values["Profit_dollar"]
            )
        if i == 6:
            bottom3_area.objList[i].insert(
                0, f'{variable_json_File.result_values["Profit_%"]} %'
            )
        if i == 8:
            bottom3_area.objList[i].insert(
                0, variable_json_File.result_values["Value_of_wallet"]
            )
        if i == 10:
            bottom3_area.objList[i].insert(
                0, variable_json_File.result_values["Invest_value"]
            )

        bottom3_area.objList[i]["state"] = "readonly"


def button_refresh_prices() -> None:
    top_area.objList[1].configure(text=f"Status na dzień: {time_now()}")
    th.Thread(
        target=middle_area.add_data_in_treeview(
            middle_area.objList[1],
            price_wallet(variable_json_File.file_dict["wallet_data"]),
        )
    ).start()

    refresh_result_data()


def refresh_charts_data():
    for widgets in bottom1_area.frame.winfo_children():
        widgets.destroy()

    chart_area_ingredients()
    pass


# funkcja będzie czyścić tabele portfel oraz ustawiać ją
# zależnie od wybranej warotści
def refresh_wallet(event):
    # czyszczenie tabeli portfel

    # wprowadzenie wartości do tabeli portfel
    with open(f"Dane\{top_area.dict_combo['wallet_list'].get()}.txt", "r") as file:
        data = file.read().splitlines()
    for i in range(len(data)):
        data[i] = data[i].split(",")
    variable_json_File.read_from_file(
        f"Dane\{top_area.dict_combo['wallet_list'].get()}.txt", "txt", "wallet_data"
    )

    middle_area.add_data_in_treeview(middle_area.objList[0], data, "txt")
    th.Thread(
        target=middle_area.add_data_in_treeview(
            middle_area.objList[1], price_wallet(data)
        )
    ).start()

    # aktywowanie wyliczeń wartości na nowych danych
    refresh_result_data()
    # aktualizacja wykresów
    # th.Thread(target=refresh_charts_data).start()
    refresh_charts_data()


# Top area in main app
def top_area_ingredients() -> None:
    """List of wallets, current data and button with refresh corrent value of invest"""
    # wallet_lists = ["Portfel1"]
    global user_login
    with open("App_file\Wallets.json", "r") as file:
        tmp = json.load(file)
        wallet_lists = tmp[f"{user_login}"]  # temporary
    top_area.text_display(
        f"Wybierz portfel:", row=0, column=0, padx=5, style="11_label.TLabel"
    )

    top_area.combobox_display(
        values=wallet_lists,
        width=12,
        row=0,
        column=1,
        padx=15,
        pady=10,
        name="wallet_list",
    )
    top_area.dict_combo["wallet_list"].bind("<<ComboboxSelected>>", refresh_wallet)
    top_area.text_display(
        f"Status na dzień: {time_now()}",
        row=0,
        column=2,
        # was padx=95
        # padx=30, before
        padx=95,
        style="12_label.TLabel",
    )
    top_area.text_display(
        f"Odśwież wyliczenia portfela: ",
        row=0,
        column=3,
        sticky="e",
        padx=5,
        style="11_label.TLabel",
    )
    top_area.button_display(
        "Odśwież",
        row=0,
        column=4,
        command=button_refresh_prices,
        padx=5,
        pady=5,
    )


def check_logins(login, password) -> None:
    global user_login
    with open("App_file\credentials.json", "r") as file:
        logins_dict = json.load(file)
    if login in logins_dict and password == logins_dict[login]:
        user_login = login
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
        style="11_label.TLabel",
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

    variable_json_File.read_from_file(
        f"Dane\{top_area.dict_combo['wallet_list'].get()}.txt", "txt", "wallet_data"
    )

    middle_area.add_data_in_treeview(
        middle_area.objList[0], variable_json_File.file_dict["wallet_data"], "txt"
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
            middle_area.objList[1],
            price_wallet(variable_json_File.file_dict["wallet_data"]),
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
        "Wybierz krypto do wyświetlania wykresu:",
        row=0,
        column=0,
        style="11_label.TLabel",
    )
    krypto_wallet_list = [
        i[0]
        for i in variable_json_File.file_dict["wallet_data"]
        if i[0]
        in variable_json_File.file_dict["variable_json"]["available_charts_data"]
    ]
    bottom1_area.combobox_display(
        values=krypto_wallet_list,
        row=0,
        column=1,
        width=10,
        pady=5,
        name="available_crypto",
    )
    # old version
    # bottom1_area.chart(krypto_wallet_list)

    bottom1_area.chart_v2(krypto_wallet_list, variable_json_File)


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
        command=lambda: purchers_area_ingredients(
            top_area.dict_combo["wallet_list"].get()
        ),
        # command=lambda: purchers_area_ingredients(top_area.objList[1].get()),
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
    bottom3_area.text_display(
        text="Ogólny Zysk/Strata zł wynosi: ",
        row=1,
        column=0,
        pady=15,
        style="11_label.TLabel",
    )
    bottom3_area.entry_display(
        result_value=variable_json_File.result_values["Profit_zl"],
        state="readonly",
        row=1,
        column=1,
        insert=True,
    )
    bottom3_area.text_display(
        text="Ogólny Zysk/Strata $ wynosi: ",
        row=2,
        column=0,
        pady=15,
        style="11_label.TLabel",
    )
    bottom3_area.entry_display(
        result_value=variable_json_File.result_values["Profit_dollar"],
        state="readonly",
        row=2,
        column=1,
        insert=True,
    )
    bottom3_area.text_display(
        text="Ogólny Zysk/Strata % wynosi: ",
        row=3,
        column=0,
        pady=15,
        style="11_label.TLabel",
    )
    bottom3_area.entry_display(
        result_value=variable_json_File.result_values["Profit_%"],
        state="readonly",
        text="%",
        row=3,
        column=1,
        insert=True,
    )
    bottom3_area.text_display(
        text="Wartość portfela w zł wynosi: ",
        row=4,
        column=0,
        pady=15,
        style="11_label.TLabel",
    )
    bottom3_area.entry_display(
        result_value=variable_json_File.result_values["Value_of_wallet"],
        state="readonly",
        row=4,
        column=1,
        insert=True,
    )
    bottom3_area.text_display(
        text="Wartość zaiwestowana wynosi: ",
        row=5,
        column=0,
        pady=15,
        style="11_label.TLabel",
    )
    bottom3_area.entry_display(
        width=10,
        result_value=variable_json_File.result_values["Invest_value"],
        state="readonly",
        row=5,
        column=1,
        insert=True,
    )


def main() -> None:
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
