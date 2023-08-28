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

# Trzeba to rozbić by każdy obiekt zawierał inne pobrane dane
variable_json_File = ReadData()
# readFile.file_list[0] json zmienne
variable_json_File.read_from_file("App_file\zmienne.json", "json", "variable_json")
# readFile.file_list[0]["Sciezka_portfel"],"txt",

session_user = {}


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


def log_out():
    root.withdraw()
    logins_window = TopFrame()
    logins_area = AreaFrame(onFrame=logins_window.frame)
    logins_area_ingredients(logins_area, logins_window)


def downlad_wallet_values_from_database(current_wallet: str, ac_id: int):
    url_credentials: str = variable_json_File.file_dict["variable_json"][
        "URL_Credentials"
    ]

    # get all wallet on this account
    response = requests.get(url_credentials + f"wallets/{ac_id}").json()
    for i in response:
        if i["Name"] == current_wallet:
            wallet_id = i["Id"]  # take only current
            break

    # get wallet values and format data
    response = requests.get(url_credentials + f"wallet_detail/{wallet_id}").json()
    for i, val in enumerate(response):
        response[i] = [
            str(val["Name"]),
            str(val["Price_PLN"]),
            str(val["Price_USD"]),
            str(val["Quantity"]),
        ]

    variable_json_File.file_dict["wallet_data"] = response


# funkcja będzie czyścić tabele portfel oraz ustawiać ją
# zależnie od wybranej warotści
def refresh_wallet(event):
    # czyszczenie tabeli portfel
    downlad_wallet_values_from_database(
        top_area.dict_combo["wallet_list"].get(), session_user["Account_ID"]
    )

    middle_area.add_data_in_treeview(
        middle_area.objList[0], variable_json_File.file_dict["wallet_data"], "txt"
    )
    th.Thread(
        target=middle_area.add_data_in_treeview(
            middle_area.objList[1],
            price_wallet(variable_json_File.file_dict["wallet_data"]),
        )
    ).start()

    # calculate and refresh area
    refresh_result_data()
    # refresh charts
    # th.Thread(target=refresh_charts_data).start()
    refresh_charts_data()


# Top area in main app
def top_area_ingredients() -> None:
    """List of wallets, current data and button with refresh corrent value of invest"""

    url_credentials: str = variable_json_File.file_dict["variable_json"][
        "URL_Credentials"
    ]
    responde = requests.get(
        url_credentials + f"wallets/{session_user['Account_ID']}"
    ).json()
    wallet_lists = [i["Name"] for i in responde]

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


def check_logins(login: str, password: str, area: AreaFrame, window: TopFrame) -> None:
    """Check if login and password is correct with data in database"""

    url_credentials: str = variable_json_File.file_dict["variable_json"][
        "URL_Credentials"
    ]
    responde = requests.get(url_credentials + f"authorization/{login}")

    if len(login) > 0 and len(password) > 0 and responde.status_code == 200:
        responde = responde.json()
        if responde["Password"] == password:
            # Temp
            session_user["login"] = login
            session_user["Account_ID"] = responde["Account_ID"]
            root.deiconify()
            window.frame.destroy()
        else:
            msgbox.showwarning("Error", "Podane hasło jest błędne.")
            area.objList[4].delete(0, "end")
    else:
        msgbox.showwarning("Error", "Nie został podany login lub hasło.")
        area.objList[2].delete(0, "end")
        area.objList[4].delete(0, "end")


def warning_mess() -> None:
    mes = msgbox.askokcancel(
        "Czy wyłączyć aplikację",
        "Jeżeli wybierzesz ok aplikacja zostanie zamknięta.",
    )
    if mes:
        root.destroy()


def logins_area_ingredients(area: AreaFrame, window: TopFrame) -> None:
    """Place with entry login and passoword for verification"""
    area.text_display(
        text="Podaj login i hasło do portfela: ",
        row=0,
        column=0,
        columnspan=2,
        style="11_label.TLabel",
        padx=15,
    )
    area.text_display(text="Login: ", row=1, column=0)
    area.entry_display(justify="center", row=1, column=1, state="normal")
    area.text_display(text="Hasło: ", row=2, column=0)
    area.entry_display(justify="center", row=2, column=1, state="normal")
    area.button_display(
        text="Zatwiedź",
        width=10,
        row=3,
        column=0,
        columnspan=2,
        padx=5,
        pady=5,
        command=lambda: check_logins(
            area.objList[2].get(), area.objList[4].get(), area, window
        ),
    )
    window.frame.protocol("WM_DELETE_WINDOW", warning_mess)
    window.frame.bind("<Return>", lambda event=None: area.objList[5].invoke())
    # only for tests
    area.objList[2].insert(0, "Admin")
    area.objList[4].insert(0, "321")  # correct 321
    # check_logins(logins_area.objList[2].get(), logins_area.objList[4].get())
    root.withdraw()
    # hide window
    # show window
    # win.deiconify()
    # działa tylko trzeba ustawić
    area.frame.wait_window()


# Middle area in main app
def middle_area_ingrednients() -> None:
    """Wallet data in treeView and calculation of wallet"""
    column_tuple_wallet = ("Nazwa", "Cena zl", "Cena $", "Ilość")
    headings_list_wallet = ["Nazwa waluty", "Cena zakupu zł", "Cena zakupu $", "Ilość"]
    middle_area.treeview_display(
        columns=column_tuple_wallet, headings_text=headings_list_wallet, row=1, column=0
    )
    downlad_wallet_values_from_database(
        top_area.dict_combo["wallet_list"].get(), session_user["Account_ID"]
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
            top_area.dict_combo["wallet_list"].get(),
            bottom2_area.objList[0],  # wallet_name, button obj
        ),
    )
    """Do nothing in future update wallet data if some was added in detail wallet"""
    bottom2_area.button_display(
        text="Odśwież portfel", row=1, column=0, padx=5, pady=15, width=15
    )
    """"""
    bottom2_area.button_display(
        text="Plany inwestycyjne", row=2, column=0, padx=5, pady=15, width=12
    )
    bottom2_area.button_display(
        text="Wyloguj", command=log_out, row=3, column=0, pady=15, width=10
    )
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
    logins_area_ingredients(logins_area, logins_window)
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
