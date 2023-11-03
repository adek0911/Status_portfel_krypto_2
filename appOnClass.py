from datetime import datetime
import json
import ttkbootstrap as ttk
import requests
import threading as th
import tkinter.messagebox as msgbox
from Classes import AreaFrame, ReadData, TopFrame
from details_wallet import purchers_area_ingredients
from charts import chart_area_result
from style_config import style_conf

# from Invested_plan import invested_area_ingredients


def invested_area_ingredients(
    charts_area: AreaFrame,
    middle_area: AreaFrame,
    buttons_area: AreaFrame,
    variable_json_File: dict,
    dollar_price: dict,
    core: ttk.Frame,
):
    def button_change_color(button: ttk.Button):
        button.configure(style="Invest.TButton")  # "primary": "#375a7f",
        pass

    def count_predict():
        value = [invested_area.objList[1].get(), invested_area.objList[3].get()]
        dollar = dollar_price.file_dict["dollar_price"]["Stable_price"]["Dolar"][0]
        # zrobić ograniczenia tylko na liczby
        if value[0] == "":
            value[0] = float(value[1]) * dollar
            invested_area.objList[1].insert(0, str(value[0].__round__(2)))
        if value[1] == "":
            value[1] = float(value[0]) / dollar
            invested_area.objList[3].insert(0, str(value[1].__round__(2)))

        combo_index = crypto_from_wallet.index(
            invested_area.dict_combo["available_crypto"].get()
        )
        children_index = middle_area.objList[1].get_children()[combo_index]

        quantity = (
            float(value[0])
            / float(middle_area.objList[1].item(children_index)["values"][0])
        ).__round__(4)
        invested_area.objList[5]["state"] = "normal"
        invested_area.objList[5].insert(0, str(quantity))
        invested_area.objList[5]["state"] = "readonly"

    def clear_entry():
        invested_area.objList[1].delete(0, "end")
        invested_area.objList[3].delete(0, "end")
        invested_area.objList[5]["state"] = "normal"
        invested_area.objList[5].delete(0, "end")
        invested_area.objList[5]["state"] = "readonly"

    def add_to_wallet():
        entry = [
            invested_area.dict_combo["available_crypto"].get(),
            invested_area.objList[1].get(),
            invested_area.objList[3].get(),
            invested_area.objList[5].get(),
        ]
        if entry[1] != "" and entry[2] != "":
            clear_entry()
            invested_area.objList[8].insert("", "end", values=entry)
            for i in variable_json_File.file_dict["wallet_data"]:
                if i[0] == entry[0]:
                    i[1] = float(entry[1]) + i[1]
                    i[2] = float(entry[2]) + i[2]
                    i[3] = float(entry[3]) + i[3]
            middle_area.add_data_in_treeview(
                middle_area.objList[0],
                variable_json_File.file_dict["wallet_data"],
                "txt",
            )
            button_refresh_prices()
        else:
            msgbox.showwarning("Error", "Uzupełnij kolumnę z ceną")

    """Poniżej tabela z zaprezentowanymi zmianami, przycisk czyszczący predykcje oraz przycisk zapisujący w pliku"""

    charts_area.frame.grid_forget()
    button_change_color(buttons_area.objList[2])
    # buttons_area.objList[2].configure(bg="red")
    invested_area = AreaFrame(onFrame=core, row=2, column=0, sticky="n")
    crypto_from_wallet = [i[0] for i in variable_json_File.file_dict["wallet_data"]]
    invested_area.combobox_display(
        values=crypto_from_wallet,
        row=1,
        column=0,
        width=8,
        pady=5,
        name="available_crypto",
        justyfy="center",
    )
    invested_area.text_display("Cena PLN", row=0, column=1)
    invested_area.entry_display(row=1, column=1)
    invested_area.text_display("Cena USD", row=0, column=2)
    invested_area.entry_display(row=1, column=2)
    invested_area.text_display("Ilość", row=0, column=3)
    invested_area.entry_display(row=1, column=3, state="disable")

    invested_area.button_display(
        "Przelicz", row=2, column=0, columnspan=2, command=count_predict
    )
    invested_area.button_display(
        "Dodaj", row=2, column=2, columnspan=2, command=add_to_wallet
    )
    headings = ["Nazwa", "Cena_PLN", "Cena_USD", "Ilość"]
    invested_area.treeview_display(
        columns=tuple(headings), headings_text=headings, row=3, column=0, columnspan=4
    )
    invested_area.objList[8].configure(height=7)


def time_now() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def price_wallet(wallet: list, variable_json_File: dict) -> list:
    """Prepare request, download krypto price, count value"""
    krypto_list_from_wallet = []
    # 4 zmienne do wyliczenia i dodania do listy dane
    """Download dolar price and update every 24h"""
    with open("App_file\zmienneApiDolar.json", mode="r+", encoding="UTF-8") as file:
        last_time = datetime.now().strftime("%d-%m-%Y")
        read_file = json.load(file)
        if read_file["Stable_price"]["Dolar"][1] != last_time:
            response = requests.get(read_file["url"], headers=read_file["headers"])
            if response.status_code == 200:
                result = json.loads(response.text)
                read_file["Stable_price"]["Dolar"] = (
                    result["quotes"]["USDPLN"],
                    last_time,
                )
                file.seek(0, 0)
                file.truncate()
                json.dump(read_file, file, ensure_ascii=False, indent=4)
    """Check if data charts is anavable"""
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

        krypto_list_from_wallet.append(
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
    return krypto_list_from_wallet


def refresh_result_data(result_area: AreaFrame, variable_json_File: dict):
    for i in range(2, 11, 2):
        result_area.objList[i]["state"] = "normal"
        result_area.objList[i].delete(0, "end")
        if i == 2:
            result_area.objList[i].insert(
                0, variable_json_File.result_values["Profit_zl"]
            )
        if i == 4:
            result_area.objList[i].insert(
                0, variable_json_File.result_values["Profit_dollar"]
            )
        if i == 6:
            result_area.objList[i].insert(
                0, f'{variable_json_File.result_values["Profit_%"]} %'
            )
        if i == 8:
            result_area.objList[i].insert(
                0, variable_json_File.result_values["Value_of_wallet"]
            )
        if i == 10:
            result_area.objList[i].insert(
                0, variable_json_File.result_values["Invest_value"]
            )

        result_area.objList[i]["state"] = "readonly"


def button_refresh_prices(
    top_area: AreaFrame,
    middle_area: AreaFrame,
    result_area: AreaFrame,
    variable_json_File: dict,
) -> None:
    top_area.objList[1].configure(text=f"Status na dzień: {time_now()}")
    middle_area.add_data_in_treeview(
        middle_area.objList[1],
        price_wallet(variable_json_File.file_dict["wallet_data"], variable_json_File),
    )

    refresh_result_data(result_area, variable_json_File)


def refresh_charts_data(charts_area: AreaFrame, variable_json_File: dict):
    for widgets in charts_area.frame.winfo_children():
        widgets.destroy()

    chart_area_ingredients(charts_area, variable_json_File)
    pass


def log_out():
    # logins_window = TopFrame()
    # logins_area = AreaFrame(onFrame=logins_window.frame)
    # logins_area_ingredients(logins_area, logins_window)
    main()


def downlad_wallet_values_from_database(
    current_wallet: str, ac_id: int, variable_json_File: dict
):
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
    response: list[dict] = requests.get(
        url_credentials + f"wallet_detail/{wallet_id}"
    ).json()
    for i in range(len(response)):
        response[i] = list(response[i].values())

    variable_json_File.file_dict["wallet_data"] = response


# funkcja będzie czyścić tabele portfel oraz ustawiać ją
# zależnie od wybranej warotści
def refresh_wallet(
    top_area: AreaFrame,
    middle_area: AreaFrame,
    result_area: AreaFrame,
    charts_area: AreaFrame,
    variable_json_File: dict,
    session_user: dict,
):
    # czyszczenie tabeli portfel
    downlad_wallet_values_from_database(
        top_area.dict_combo["wallet_list"].get(),
        session_user["Account_ID"],
        variable_json_File,
    )

    middle_area.add_data_in_treeview(
        middle_area.objList[0], variable_json_File.file_dict["wallet_data"], "txt"
    )
    th.Thread(
        target=middle_area.add_data_in_treeview(
            middle_area.objList[1],
            price_wallet(
                variable_json_File.file_dict["wallet_data"], variable_json_File
            ),
        )
    ).start()

    # calculate and refresh area
    refresh_result_data(result_area, variable_json_File)
    # refresh charts
    # th.Thread(target=refresh_charts_data).start()
    refresh_charts_data(charts_area, variable_json_File)


# Top area in main app
def top_area_ingredients(
    top_area: AreaFrame,
    middle_area: AreaFrame,
    result_area: AreaFrame,
    charts_area: AreaFrame,
    variable_json_File: dict,
    session_user: dict,
) -> None:
    """List of wallets, current data and button with refresh corrent value of invest"""

    url_credentials: str = variable_json_File.file_dict["variable_json"][
        "URL_Credentials"
    ]
    responde = requests.get(
        url_credentials + f"wallets/{session_user['Account_ID']}"
    ).json()

    wallet_lists = [i["Name"] for i in responde]
    # print(wallet_lists) #Testsd
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
    top_area.dict_combo["wallet_list"].bind(
        "<<ComboboxSelected>>",
        lambda _: refresh_wallet(
            top_area,
            middle_area,
            result_area,
            charts_area,
            variable_json_File,
            session_user,
        ),
    )
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
        command=lambda: button_refresh_prices(
            top_area, middle_area, result_area, variable_json_File
        ),
        padx=5,
        pady=5,
    )


def check_logins(
    login: str,
    password: str,
    area: AreaFrame,
    window: TopFrame,
    variable_json_File: dict,
    session_user: dict,
    root: ttk.Window,
) -> None:
    """Check if login and password is correct with data in database"""

    url_credentials: str = variable_json_File.file_dict["variable_json"][
        "URL_Credentials"
    ]
    responde = requests.get(url_credentials + f"authorization/{login}")

    if len(login) > 0 and len(password) > 0 and responde.status_code == 200:
        responde = responde.json()
        if responde["Password"] == password:
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


def warning_mess(root: ttk.Window) -> None:
    mes = msgbox.askokcancel(
        "Czy wyłączyć aplikację",
        "Jeżeli wybierzesz ok aplikacja zostanie zamknięta.",
    )
    if mes:
        root.destroy()


def logins_area_ingredients(
    area: AreaFrame,
    window: TopFrame,
    root: ttk.Window,
    variable_json_File: dict,
    session_user: dict,
) -> None:
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
            area.objList[2].get(),
            area.objList[4].get(),
            area,
            window,
            variable_json_File,
            session_user,
            root,
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
def middle_area_ingrednients(
    middle_area: AreaFrame,
    top_area: AreaFrame,
    session_user: dict,
    variable_json_File: dict,
) -> None:
    """Wallet data in treeView and calculation of wallet"""
    column_tuple_wallet = ("Nazwa", "Cena zl", "Cena $", "Ilość")
    headings_list_wallet = ["Nazwa waluty", "Cena zakupu zł", "Cena zakupu $", "Ilość"]
    middle_area.treeview_display(
        columns=column_tuple_wallet, headings_text=headings_list_wallet, row=1, column=0
    )
    downlad_wallet_values_from_database(
        top_area.dict_combo["wallet_list"].get(),
        session_user["Account_ID"],
        variable_json_File,
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
            price_wallet(
                variable_json_File.file_dict["wallet_data"], variable_json_File
            ),
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
def chart_area_ingredients(charts_area: AreaFrame, variable_json_File: dict) -> None:
    """Charts with data"""
    charts_area.text_display(
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
    charts_area.combobox_display(
        values=krypto_wallet_list,
        row=0,
        column=1,
        width=10,
        pady=5,
        name="available_crypto",
    )
    chart_area_result(charts_area, krypto_wallet_list, variable_json_File)


# bottom 2/3 area in main app
def buttons_area_ingredients(
    buttons_area: AreaFrame, top_area: AreaFrame, root: ttk.Window
) -> None:
    """Buttons with program options"""
    buttons_area.button_display(
        text="Szczegóły zakupów",
        row=0,
        column=0,
        padx=5,
        pady=15,
        width=18,
        command=lambda: purchers_area_ingredients(
            top_area.dict_combo["wallet_list"].get(),
            buttons_area.objList[0],  # wallet_name, button obj
        ),
    )
    """Do nothing in future update wallet data if some was added in detail wallet"""
    buttons_area.button_display(
        text="Odśwież portfel", row=1, column=0, padx=5, pady=15, width=15
    )
    """command=lambda: invested_area_ingredients(variable_json_File.file_dict["wallet_data"]),"""
    # print(price_wallet(variable_json_File.file_dict["wallet_data"]))
    buttons_area.button_display(
        text="Plany inwestycyjne",
        command=invested_area_ingredients,
        row=2,
        column=0,
        padx=5,
        pady=15,
        width=16,
    )

    buttons_area.button_display(
        text="Wyloguj", command=log_out, row=3, column=0, pady=15, width=10
    )
    buttons_area.button_display(
        text="Exit", row=4, column=0, command=root.destroy, padx=5, pady=15
    )


# bottom 3/3 area in main app
def result_area_ingredients(result_area: AreaFrame, variable_json_File: dict) -> None:
    """Result in one table about of wallet"""

    result_area.text_display(
        text="Podsumowanie portfela",
        row=0,
        column=0,
        columnspan=2,
        style="12_label.TLabel",
    )
    result_area.text_display(
        text="Ogólny Zysk/Strata zł wynosi: ",
        row=1,
        column=0,
        pady=15,
        style="11_label.TLabel",
    )
    result_area.entry_display(
        result_value=variable_json_File.result_values["Profit_zl"],
        state="readonly",
        row=1,
        column=1,
        insert=True,
    )
    result_area.text_display(
        text="Ogólny Zysk/Strata $ wynosi: ",
        row=2,
        column=0,
        pady=15,
        style="11_label.TLabel",
    )
    result_area.entry_display(
        result_value=variable_json_File.result_values["Profit_dollar"],
        state="readonly",
        row=2,
        column=1,
        insert=True,
    )
    result_area.text_display(
        text="Ogólny Zysk/Strata % wynosi: ",
        row=3,
        column=0,
        pady=15,
        style="11_label.TLabel",
    )
    result_area.entry_display(
        result_value=variable_json_File.result_values["Profit_%"],
        state="readonly",
        text="%",
        row=3,
        column=1,
        insert=True,
    )
    result_area.text_display(
        text="Wartość portfela w zł wynosi: ",
        row=4,
        column=0,
        pady=15,
        style="11_label.TLabel",
    )
    result_area.entry_display(
        result_value=variable_json_File.result_values["Value_of_wallet"],
        state="readonly",
        row=4,
        column=1,
        insert=True,
    )
    result_area.text_display(
        text="Wartość zaiwestowana wynosi: ",
        row=5,
        column=0,
        pady=15,
        style="11_label.TLabel",
    )
    result_area.entry_display(
        width=10,
        result_value=variable_json_File.result_values["Invest_value"],
        state="readonly",
        row=5,
        column=1,
        insert=True,
    )


# Not use
def threed_middle_result_ingrednients(
    middle_area: AreaFrame,
    top_area: AreaFrame,
    session_user: dict,
    result_area: AreaFrame,
    variable_json_File: dict,
):
    middle_area_ingrednients(middle_area, top_area, session_user, variable_json_File)
    result_area_ingredients(result_area, variable_json_File)


def main() -> None:
    # window for login
    root = ttk.Window(themename="darkly")
    logins_window = TopFrame()
    logins_area = AreaFrame(onFrame=logins_window.frame)
    style_conf(root)

    core = ttk.Frame(root)
    core.grid()
    top_area = AreaFrame(
        onFrame=core, row=0, column=0, columnspan=4, sticky="ew", padx=5
    )
    middle_area = AreaFrame(onFrame=core, row=1, column=0, columnspan=4)
    charts_area = AreaFrame(onFrame=core, row=2, column=0, sticky="w")
    buttons_area = AreaFrame(onFrame=core, row=2, column=1, sticky="n")
    result_area = AreaFrame(onFrame=core, row=2, column=2, sticky="n")

    variable_json_File = ReadData()
    variable_json_File.read_from_file("App_file\zmienne.json", "json", "variable_json")

    dollar_price = ReadData()
    dollar_price.read_from_file("App_file\zmienneApiDolar.json", "json", "dollar_price")
    # print(variable_json_File.file_dict["wallet_data"])
    session_user = {}

    logins_area_ingredients(
        logins_area, logins_window, root, variable_json_File, session_user
    )
    top_area_ingredients(
        top_area,
        middle_area,
        result_area,
        charts_area,
        variable_json_File,
        session_user,
    )
    th.Thread(
        target=threed_middle_result_ingrednients(
            middle_area, top_area, session_user, result_area, variable_json_File
        )
    ).start()

    # Wywala mi szerkość treeview headers
    th.Thread(target=chart_area_ingredients(charts_area, variable_json_File)).start()

    buttons_area_ingredients(buttons_area, top_area, root)
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
