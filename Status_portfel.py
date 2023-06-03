from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import requests
import threading as th
import szczegoly_cjedn as sc

# from warnings import catch_warnings
# from currency_converter import CurrencyConverter
import json
import csv

root = Tk()
root.title("Status portfela")
root.iconbitmap("Dane\icona.ico")
core = Frame(root)

style = Style("flatly")
style.configure("primary.Treeview.Heading", font=("Helvetica", 12))
style.configure("core.TLabel", background="#009999", foreground="white")
style.configure("primary.TEntry", bordercolor="gray")
style.configure("primary.TButton", font=("Helvetica", 11))

core.configure(bg="#009999", padx=5, pady=5)
core.grid()

# region top
data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
top_data = ttk.Label(
    core, text=f"Status na dzień: {data}", style="core.TLabel", font=("Helvetica", 12)
)
top_data.grid(row=0, column=0, columnspan=3, pady=5)
frame_switch = Frame(core, bg="#009999")
frame_switch.grid(row=0, column=2)

# endregion

# region środek


def wybrane_z_portfel(event):
    global srodek_portfel_treeview, right_treev_wyniki

    a = srodek_portfel_treeview.focus()
    b = right_treev_wyniki.focus()

    a1 = srodek_portfel_treeview.get_children()
    b1 = right_treev_wyniki.get_children()

    a_index = a1.index(a)
    if b == "":
        b_index = a_index
        b_focus_selection = b1[a_index]
        right_treev_wyniki.selection_set(b_focus_selection)
        right_treev_wyniki.focus(b_focus_selection)
    else:
        b_index = b1.index(b)

    if a_index != b_index or a_index == 0:
        b_focus_selection = b1[a_index]
        right_treev_wyniki.selection_set(b_focus_selection)
        right_treev_wyniki.focus(b_focus_selection)


def wybrane_z_portfel2(event):
    global srodek_portfel_treeview, right_treev_wyniki

    a = srodek_portfel_treeview.focus()
    b = right_treev_wyniki.focus()

    a1 = srodek_portfel_treeview.get_children()
    b1 = right_treev_wyniki.get_children()

    b_index = b1.index(b)
    if a == "":
        a_index = b_index
        a_focus_selection = a1[b_index]
        srodek_portfel_treeview.selection_set(a_focus_selection)
        srodek_portfel_treeview.focus(a_focus_selection)
    else:
        a_index = a1.index(a)

    if b_index != a_index:
        a_focus_selection = a1[b_index]
        srodek_portfel_treeview.selection_set(a_focus_selection)
        srodek_portfel_treeview.focus(a_focus_selection)


frame_middle = Frame(core, bg="#009999", height=500)
frame_middle.grid(row=1, column=0)

srodek_portfel_treeview = ttk.Treeview(frame_middle, style="primary.Treeview")
srodek_portfel_treeview["columns"] = ("Nazwa", "Cena zl", "Cena $", "Ilość")
srodek_portfel_treeview.configure(show="headings", selectmode="browse")
srodek_portfel_treeview.bind("<<TreeviewSelect>>", wybrane_z_portfel)
srodek_portfel_treeview.grid(row=0, column=0)

srodek_portfel_treeview.column("Nazwa", width=80, anchor=CENTER)
srodek_portfel_treeview.column("Cena zl", width=80, anchor=CENTER)
srodek_portfel_treeview.column("Cena $", width=80, anchor=CENTER)
srodek_portfel_treeview.column("Ilość", width=95, anchor=CENTER)

srodek_portfel_treeview.heading("#0", text="\n")
srodek_portfel_treeview.heading("Nazwa", text="Nazwa\n waluty")
srodek_portfel_treeview.heading("Cena zl", text="Cena\n zakupu zł")
srodek_portfel_treeview.heading("Cena $", text="Cena\n zakupu $")
srodek_portfel_treeview.heading("Ilość", text="Ilość")

# Json File z ścieżkami
with open("App_file\zmienne.json", "r") as dane:
    zmienne_file = json.load(dane)

# region create messagebox do wyboru wartości dolara


def choice_dolar_price():
    window_price_dolar = Toplevel(root, bg="#009999")
    window_price_dolar.title("Wybierz wartość dolara")
    window_price_dolar.geometry("400x250")

    a = float(zmienne_file["Cena_Dolar"])
    # b = float(CurrencyConverter().convert(1, 'USD', 'PLN')).__round__(2)
    b = 1

    window_price_dolar_label1 = ttk.Label(
        window_price_dolar,
        text=f"Cena z pliku wynosi: {a}",
        style="core.TLabel",
        font=("Helvetica", 12),
        justify=LEFT,
    )
    window_price_dolar_label1.grid(row=0, column=0, columnspan=2, padx=5)
    window_price_dolar_button1 = ttk.Button(
        window_price_dolar,
        text="Wybierz",
        style="primary.TButton",
        command=lambda: przypisz(a, b, 0),
    )
    window_price_dolar_button1.grid(row=0, column=3, pady=5)

    window_price_dolar_label2 = ttk.Label(
        window_price_dolar,
        text=f"Cena pobrana wynosi: {b}",
        style="core.TLabel",
        font=("Helvetica", 12),
        justify=LEFT,
    )
    window_price_dolar_label2.grid(row=1, columnspan=2, column=0, padx=5)
    window_price_dolar_button2 = ttk.Button(
        window_price_dolar,
        text="Wybierz",
        style="primary.TButton",
        command=lambda: przypisz(a, b, 1),
    )
    window_price_dolar_button2.grid(row=1, column=3, pady=5)

    window_price_dolar_label3 = ttk.Label(
        window_price_dolar,
        text="Wprowadz własną cenę dolara: ",
        style="core.TLabel",
        font=("Helvetica", 12),
        justify=LEFT,
    )
    window_price_dolar_label3.grid(row=2, column=0, padx=5)
    window_price_dolar_entry = ttk.Entry(
        window_price_dolar, style="primary.TEntry", width=5
    )
    window_price_dolar_entry.grid(row=2, column=1, pady=5, padx=5)
    window_price_dolar_button3 = ttk.Button(
        window_price_dolar,
        text="Wybierz",
        style="primary.TButton",
        command=lambda: przypisz(a, b, 2),
    )
    window_price_dolar_button3.grid(row=2, column=3, pady=5)
    window_price_dolar.grid()

    def przypisz(a, b, x: int):
        # a=float(zmienne_file['Cena_Dolar'])
        # b=float(CurrencyConverter().convert(1,'USD','PLN')).__round__(2)
        global cena
        cena = 0
        if x == 0:
            cena = a
            window_price_dolar.destroy()

        if x == 1:
            cena = b
            window_price_dolar.destroy()

        if x == 2:
            cena = float((window_price_dolar_entry.get()).replace(",", "."))
            window_price_dolar.destroy()

        return cena

    # Zatrzymuje aplikację i czeka dopóki nie zostanie zamnięte okno
    window_price_dolar.wait_window()
    return cena


# endregion

# try:
#     c=CurrencyConverter()
#     # dolar=CurrencyRates().get_rate('USD','PLN',datetime(2023,4,2))
#     dolar=float(c.convert(1,'USD','PLN')).__round__(2)#,'PLN',datetime(2023,4,2))
#     #dolar=float(f'{dolar:.4f}')
#     # dolar=4.23
#     print(dolar)
# #problem z połączeniem
# except (requests.exceptions.ConnectionError ):#or CurrencyRates.get_rate.RatesNotAvailableError):
#     # message box z informacją że nie udał się pobrać wartości proszę podać własną albo zostanie wpisana stała 4,5
#     dolar=float(zmienne_file['Cena_Dolar'])

# dolar=float(zmienne_file['Cena_Dolar'])


def portfel_dane():
    global dane_portfel
    # with open((str(zmienne_file['Sciezka_portfel'])),'r') as odczyt:
    with open((str(zmienne_file["Sciezka_portfel_test"])), "r") as odczyt:
        dane_portfel = odczyt.read()

    dane_portfel = dane_portfel.splitlines()

    for i in range(len(dane_portfel)):
        dane_portfel[i] = dane_portfel[i].split(",")
        for y in range(1, 4):
            if dane_portfel[i][y] == "":
                dane_portfel[i][y] = float("nan")
            dane_portfel[i][y] = float(dane_portfel[i][y])
    global e4
    e4 = 0.0

    for i in srodek_portfel_treeview.get_children():
        srodek_portfel_treeview.delete(i)

    def isNan(num):
        return num != num

    for i in range(len(dane_portfel)):
        if (isNan(dane_portfel[i][1]) == True) or (dane_portfel[i][1] == ""):
            dane_portfel[i][1] = float(dane_portfel[i][2] * dolar).__round__(2)

        if (isNan(dane_portfel[i][2]) == True) or (dane_portfel[i][2] == ""):
            dane_portfel[i][2] = float(dane_portfel[i][1] / dolar).__round__(2)

        srodek_portfel_treeview.insert("", index=i, values=dane_portfel[i])
        e4 = e4 + float(dane_portfel[i][1])


# endregion


# region prawy

frame_right = Frame(core, height=500, width=100)
frame_right.grid(row=1, column=1, columnspan=2)

right_treev_wyniki = ttk.Treeview(frame_right, style="primary.Treeview")
right_treev_wyniki["columns"] = (
    "Cena zl",
    "Cena $",
    "Wartość zl",
    "Wartość $",
    "Zysk/Strata zl",
    "Zysk/Strata $",
    "Zysk/Strata %",
)
right_treev_wyniki.configure(show="headings", selectmode="browse")
right_treev_wyniki.bind("<<TreeviewSelect>>", wybrane_z_portfel2)
right_treev_wyniki.grid(row=0, column=0)

# right_treev_wyniki.column('#0',stretch=NO,minwidth=80)
right_treev_wyniki.column("Cena zl", width=95, stretch=NO, anchor=CENTER)
right_treev_wyniki.column("Cena $", width=95, stretch=NO, anchor=CENTER)
right_treev_wyniki.column("Wartość zl", width=87, stretch=NO, anchor=CENTER)
right_treev_wyniki.column("Wartość $", width=87, stretch=NO, anchor=CENTER)
right_treev_wyniki.column("Zysk/Strata zl", width=87, stretch=NO, anchor=CENTER)
right_treev_wyniki.column("Zysk/Strata $", width=87, stretch=NO, anchor=CENTER)
right_treev_wyniki.column("Zysk/Strata %", width=87, stretch=NO, anchor=CENTER)

right_treev_wyniki.heading("#0", text="\n")
right_treev_wyniki.heading("Cena zl", text="Cena\n aktualna zł")
right_treev_wyniki.heading("Cena $", text="Cena\n aktualna $")
right_treev_wyniki.heading("Wartość zl", text="Wartość\n zł")
right_treev_wyniki.heading("Wartość $", text="Wartość\n $")
right_treev_wyniki.heading("Zysk/Strata zl", text="Zysk/\n Strata zł")
right_treev_wyniki.heading("Zysk/Strata $", text="Zysk/\n Strata $")
right_treev_wyniki.heading("Zysk/Strata %", text="Zysk/\n Strata %")

# endregion

dolar = choice_dolar_price()

portfel_dane()
global dane_portfel

# download_krypto_price

# region podsumowania


def frame_wyniki():
    global e1, e2, e5, e4
    e1 = e1.__round__(2)
    e2 = e2.__round__(2)
    e5 = e5.__round__(2)
    e3 = ((e1 * 100) / float(e4)).__round__(2)
    e4 = e4.__round__(2)

    frame_wyniki = Frame(core)
    frame_wyniki.configure(bg="#009999")
    frame_wyniki.grid(row=2, column=2, pady=5, padx=5, sticky=N)
    wyniki_opis = ttk.Label(
        frame_wyniki,
        text="Podsumowanie portfela",
        style="core.TLabel",
        font=("Helvetica", 12),
    )
    wyniki_opis.grid(row=0, column=0, columnspan=2, pady=5, padx=5)

    wyniki_o1 = ttk.Label(
        frame_wyniki,
        text="Ogólny Zysk/Strata zł wynosi: ",
        style="core.TLabel",
        font=("Helvetica", 12),
    )
    wyniki_o1.grid(row=1, column=0, pady=5, padx=5)

    wyniki_e1 = ttk.Entry(frame_wyniki, style="primary.TEntry", width=10)
    if e1 < 0:
        wyniki_e1.configure(foreground="Red")
    wyniki_e1.insert(0, e1)
    wyniki_e1["state"] = "readonly"
    wyniki_e1.grid(row=1, column=1, pady=5, padx=5)

    wyniki_o2 = ttk.Label(
        frame_wyniki,
        text="Ogólny Zysk/Strata $ wynosi: ",
        style="core.TLabel",
        font=("Helvetica", 12),
    )
    wyniki_o2.grid(row=2, column=0, pady=5, padx=5)

    wyniki_e2 = ttk.Entry(frame_wyniki, style="primary.TEntry", width=10)
    if e2 < 0:
        wyniki_e2.configure(foreground="Red")
    wyniki_e2.insert(0, e2)
    wyniki_e2["state"] = "readonly"
    wyniki_e2.grid(row=2, column=1, pady=5, padx=5)

    wyniki_o3 = ttk.Label(
        frame_wyniki,
        text="Ogólny Zysk/Strata % wynosi: ",
        style="core.TLabel",
        font=("Helvetica", 12),
    )
    wyniki_o3.grid(row=3, column=0, pady=5, padx=5)

    wyniki_e3 = ttk.Entry(frame_wyniki, style="primary.TEntry", width=10)
    if e3 < 0:
        wyniki_e3.configure(foreground="Red")
    e3 = str(e3) + " %"
    wyniki_e3.insert(0, e3)
    wyniki_e3["state"] = "readonly"
    wyniki_e3.grid(row=3, column=1, pady=5, padx=5)

    wyniki_e5 = ttk.Label(
        frame_wyniki,
        text="Wartość portfela w zł wynosi: ",
        style="core.TLabel",
        font=("Helvetica", 12),
    )
    wyniki_e5.grid(row=4, column=0, pady=5, padx=5)

    wyniki_e5 = ttk.Entry(frame_wyniki, style="primary.TEntry", width=10)
    if e5 < 0:
        wyniki_e5.configure(foreground="Red")
    wyniki_e5.insert(0, e5)
    wyniki_e5["state"] = "readonly"
    wyniki_e5.grid(row=4, column=1, pady=5, padx=5)

    wyniki_o5 = ttk.Label(
        frame_wyniki,
        text="Wartość zaiwestowana wynosi: ",
        style="core.TLabel",
        font=("Helvetica", 12),
    )
    wyniki_o5.grid(row=5, column=0, pady=5, padx=5)

    wyniki_e4 = ttk.Entry(frame_wyniki, style="primary.TEntry", width=10)
    wyniki_e4.insert(0, str(e4) + " zł")
    wyniki_e4["state"] = "readonly"
    wyniki_e4.grid(row=5, column=1, pady=5, padx=5)


def krypto_price():
    global lista_krypto, right_treev_wyniki
    global e1, e2, e5

    lista_krypto = []
    r_wyniki = []
    e1 = 0.0  # Zyski w złotówkach
    e2 = 0.0  # Zyski w dolarach
    e5 = 0.0  # Wartość zainwestowana
    j = 0

    for row in dane_portfel:
        lista_krypto.append(row[0] + "USDT")
        r_wyniki.append([])

    for a in lista_krypto:
        # url2=url+a
        url2 = str(zmienne_file["URL_krypto_price"]) + a
        cena = requests.get(url2)
        cena = cena.json()
        try:
            price = float(cena["price"]).__round__(3)
        except KeyError:
            if (
                a == "ARI10USDT"
            ):  # wartość wpisana z ręki dla ARI10 z dnia 10/12/2022 Dolar
                price = float(zmienne_file["Cena_ARI10"])
            else:
                price = 0

        r_wyniki[j].insert(0, ((price * dolar).__round__(3)))  # Cena zł
        r_wyniki[j].insert(1, price)  # Cena $
        r_wyniki[j].insert(
            2, float(dane_portfel[j][3] * r_wyniki[j][0]).__round__(2)
        )  # Wartość zł
        r_wyniki[j].insert(
            3, float(dane_portfel[j][3] * price).__round__(2)
        )  # Wartość $
        # Zysk_Strata zł
        r_wyniki[j].insert(4, (r_wyniki[j][2] - float(dane_portfel[j][1])).__round__(2))
        r_wyniki[j].insert(
            5, (r_wyniki[j][3] - float(dane_portfel[j][2])).__round__(2)
        )  # Zysk_Strata $

        if float(dane_portfel[j][1]) < 0:
            dane_tmp = float(dane_portfel[j][1]) * (-1)
            procent_z_zl = ((r_wyniki[j][4] * 100) / dane_tmp).__round__(2)
        else:
            dane_portfel[j][1] = float(dane_portfel[j][1])
            procent_z_zl = ((r_wyniki[j][4] * 100) / dane_portfel[j][1]).__round__(2)
        r_wyniki[j].insert(6, f"{procent_z_zl} %")  # Zysk_Strata %

        e1 += r_wyniki[j][4]
        e2 += r_wyniki[j][5]
        e5 += r_wyniki[j][2]
        right_treev_wyniki.insert("", index=j, values=r_wyniki[j])

        j = j + 1
    # print(r_wyniki)
    frame_wyniki()


def krypto_price_2_0():
    global right_treev_wyniki
    global e1, e2, e5

    lista_krypto, lista_krypto2, lista_krypto3 = [], [], []
    r_wyniki, r_wyniki2, r_wyniki3 = [], [], []
    e1 = 0.0  # Zyski w złotówkach
    e2 = 0.0  # Zyski w dolarach
    e5 = 0.0  # Wartość zainwestowana

    # Dla 3 wątków
    l_dane_portfel = len(dane_portfel)
    if l_dane_portfel % 3 == 0:
        len_l12 = int((l_dane_portfel / 3))
        len_l13 = int((l_dane_portfel - len_l12))
    if l_dane_portfel % 3 == 1 or l_dane_portfel % 3 == 2:
        len_l12 = int((l_dane_portfel / 3) + 1)
        len_l13 = int((l_dane_portfel - len_l12) + 1)

    def watki(lista: list, poczatek: int, koniec: int, nazwy: list, wyniki: list):
        for i in range(poczatek, koniec, 1):
            lista.append(nazwy[i][0] + "USDT")
            wyniki.append([])

    watki(lista_krypto, 0, len_l12, dane_portfel, r_wyniki)
    watki(lista_krypto2, len_l12, len_l13, dane_portfel, r_wyniki2)
    watki(lista_krypto3, len_l13, l_dane_portfel, dane_portfel, r_wyniki3)

    def wartosci(krypto: list, wynik: list, numer_zadania: int):
        j = 0
        global e1, e2, e5
        for a in krypto:
            # url2=url+a
            url2 = str(zmienne_file["URL_krypto_price"]) + a
            cena = requests.get(url2)
            cena = cena.json()
            try:
                price = float(cena["price"]).__round__(3)
            except KeyError:
                if a == "ARI10USDT":
                    price = float(zmienne_file["Cena_ARI10"])
                else:
                    price = 0

            wynik[j].insert(0, ((price * dolar).__round__(3)))  # Cena zł
            wynik[j].insert(1, price)  # Cena $

            def portf(numer_zadania: int, j: int):
                tmp = j
                if numer_zadania == 2:
                    tmp = tmp + 3
                if numer_zadania == 3:
                    tmp = tmp + 6
                wynik[j].insert(
                    2, float(dane_portfel[tmp][3] * wynik[j][0]).__round__(2)
                )  # Wartość zł
                wynik[j].insert(
                    3, float(dane_portfel[tmp][3] * price).__round__(2)
                )  # Wartość $
                # Zysk_Strata zł
                wynik[j].insert(
                    4, (wynik[j][2] - float(dane_portfel[tmp][1])).__round__(2)
                )
                # Zysk_Strata $
                wynik[j].insert(
                    5, (wynik[j][3] - float(dane_portfel[tmp][2])).__round__(2)
                )
                if float(dane_portfel[tmp][1]) < 0:
                    dane_tmp = float(dane_portfel[tmp][1]) * (-1)
                    procent_z_zl = ((wynik[j][4] * 100) / dane_tmp).__round__(2)
                else:
                    dane_portfel[tmp][1] = float(dane_portfel[tmp][1])
                    procent_z_zl = (
                        (wynik[j][4] * 100) / dane_portfel[tmp][1]
                    ).__round__(2)
                wynik[j].insert(6, f"{procent_z_zl} %")  # Zysk_Strata %

            portf(numer_zadania, j)

            e1 += wynik[j][4]
            e2 += wynik[j][5]
            e5 += wynik[j][2]
            j = j + 1

    th_1 = th.Thread(target=wartosci(lista_krypto, r_wyniki, 1))

    th_2 = th.Thread(target=wartosci(lista_krypto2, r_wyniki2, 2))

    th_3 = th.Thread(target=wartosci(lista_krypto3, r_wyniki3, 3))

    th_1.start()
    th_2.start()
    th_3.start()

    # if (th_1.is_alive()==False or th_2.is_alive()==False or th_3.is_alive()==False):
    r_wyniki = r_wyniki + r_wyniki2 + r_wyniki3

    old_value = []
    for i in range(len(r_wyniki)):
        right_treev_wyniki.insert("", index=i, values=r_wyniki[i])
        old_value.append(str(r_wyniki[i][4]))
        # dla wartości:
        # Tutaj zrobić zapis wartości do pliku z ostatniego dnia
        # Zmiana tych wartości dopiero jeżeli data jest różna (tydzień , dzień ostatnie uruchomienie??)
    # dzisiaj warunek jeżeli dane są inne od dzisiaj
    # data_wykres=datetime.now().strftime('%d/%m/%Y')
    data = datetime.now()
    # zapis
    with open(
        zmienne_file["Sciezka_Dane_old"], "w", encoding="UTF-8", newline=""
    ) as old_dane:
        writer = csv.writer(old_dane)
        print(f"{data} Dane zostały wczytane")
        writer.writerow([data])
        writer.writerows([old_value])

    # print(old_value)

    frame_wyniki()


czas = int(zmienne_file["czas_refresh"])
# th.Thread(target=krypto_price).start()

th.Thread(target=krypto_price_2_0).start()


def refresh_date():
    global is_on
    refresh_status = th.Timer(czas, refresh_date)
    # top_data.configure(text=text+f' {str(dolar)}')
    if is_on == False:
        for i in right_treev_wyniki.get_children():
            right_treev_wyniki.delete(i)
        th.Thread(target=krypto_price).start()
        refresh_status.start()


global is_on
is_on = True


def refresh():
    global is_on
    if is_on:
        top_switch_button.configure(text="ON")
        is_on = False
        refresh_date()
    else:
        top_switch_button.configure(text="OFF")

        is_on = True


# endregion
top_switch_label = ttk.Label(
    frame_switch,
    text=f"Włącz odświeżanie danych co {czas}s ",
    style="core.TLabel",
    font=("Helvetica", 12),
)
top_switch_label.grid(row=0, column=0)
top_switch_button = ttk.Button(
    frame_switch, text="OFF", style="primary.TButton", command=refresh
)
top_switch_button.grid(row=0, column=1)

global button_on
button_on = True


# region button_glowny
def szczeg():
    global button_on
    if len(Toplevel.winfo_children(root)) < 2:
        sc.szczegoly_zakupow()


frame_button = Frame(core, height=150)
frame_button.configure(bg="#009999", padx=5, pady=5)
frame_button.grid(row=2, column=1, sticky=N, pady=10)

frame_button_szczegoly_zamowienia = ttk.Button(
    frame_button, text="Szczegóły zakupów", style="primary.TButton", command=szczeg
)
frame_button_szczegoly_zamowienia.grid(row=0, column=0, pady=10)


frame_button_edycja_portfel = ttk.Button(
    frame_button, text="Odśwież portfel", style="primary.TButton", command=portfel_dane
)
frame_button_edycja_portfel.grid(row=1, column=0, pady=10)

frame_button_bot_trading = ttk.Button(
    frame_button, text="Bot trading", style="primary.TButton"
)
frame_button_bot_trading.grid(row=2, column=0, pady=10)

frame_button_exit = ttk.Button(
    frame_button, text="Exit", style="primary.TButton", command=root.destroy
)
frame_button_exit.grid(row=3, column=0, pady=10)
# endregion


# pobranie danych
frame_wykresy = Frame(core)
frame_wykresy.grid(row=2, column=0, pady=10)

analiza_scrollbar = Scrollbar(frame_wykresy, orient="vertical")
analiza_scrollbar.pack(side=RIGHT, fill=BOTH)
canvas = Canvas(frame_wykresy, width=430, height=300)
canvas.pack(side=LEFT)
canvas.config(yscrollcommand=analiza_scrollbar.set)


def wykresy():
    # Zrobić zapis danych by ich nie pobierać za każdym razem
    frame_wykresy2 = Frame(canvas)
    frame_wykresy2.configure(bg="#009999")
    canvas.create_window((0, 0), window=frame_wykresy2, anchor="nw")

    label_wykresy = ttk.Label(
        frame_wykresy2,
        text="Wykresy z ostatnich 24h",
        style="core.TLabel",
        font=("Helvetica", 12),
        background="#2c3e50",
        border=5,
    )
    label_wykresy.grid(row=0, column=0, pady=5)

    # Warunek do odczytywania zmiennych

    data_wykres = datetime.now().strftime("%d/%m/%Y")

    data_file = open(zmienne_file["Sciezka_Dane_wykres"], "r", newline="").readline()
    data_file = data_file.strip("\n\r")

    global dane_portfel
    t_lista = []
    for i in dane_portfel:
        t_lista.append(str(i[0]) + "USDT")
    t_lista2 = []
    lista_final = []

    if data_wykres == data_file:
        with open(zmienne_file["Sciezka_Dane_wykres"], "r", newline="") as od_dane:
            lista_final = od_dane.read().splitlines()
            lista_final.pop(0)
            for i in range(len(lista_final)):
                lista_final[i] = lista_final[i].split(",")

    else:
        for i in t_lista:
            filepath = str(zmienne_file["URL_wykres_data"]).replace("{i}", f"{i}")
            responce = requests.get(filepath).text

            lista = responce.split("\n", 27)

            del lista[0:3]
            lista = lista[:24]

            for a in range(len(lista)):
                lista[a] = lista[a].split(",")
                del lista[a][0], lista[a][2:5], lista[a][3:]
                lista[a][0:1] = lista[a][0].split(" ")
                del lista[a][0]
            lista_final += lista

        # Zapis do pliku csv
        with open(
            zmienne_file["Sciezka_Dane_wykres"], "w", encoding="UTF-8", newline=""
        ) as d_wykres:
            writer = csv.writer(d_wykres)
            # print(f'{data_wykres} wczytane dane')
            writer.writerow([data_wykres])
            writer.writerows(lista_final)

    for i in lista_final:
        if i[1] not in t_lista2:
            t_lista2.append(i[1])

    # region wykresu

    plt.style.use("ggplot")
    for j in range(len(dane_portfel)):
        wykres = plt.Figure(figsize=(4.2, 1), dpi=100)
        ax1 = wykres.add_subplot(111)
        lista_wybrana = [[], []]

        for i in lista_final:
            if len(t_lista2) > j:
                if i[1] == t_lista2[j]:
                    lista_wybrana[0].append(i[0])
                    lista_wybrana[1].append(float(i[2]).__round__(4))

        lista_wybrana[0].reverse()
        lista_wybrana[1].reverse()
        if len(lista_wybrana[1]) != 0:
            tendencja_24 = str(
                (
                    (
                        (
                            lista_wybrana[1][(len(lista_wybrana[1]) - 1)]
                            / lista_wybrana[1][0]
                        )
                        - 1
                    )
                    * 100
                ).__round__(2)
            )

            l_label = lista_wybrana[0][::6]
            for i in range(len(l_label)):
                l_label[i] = l_label[i][:5]

            ax1.plot(lista_wybrana[0], lista_wybrana[1])
            # ax1.get_xaxis().set_visible(False)
            ax1.set_xticks(lista_wybrana[0][::6], l_label)
            ax1.set_title(
                f"{str(t_lista2[j])[:-4]}\n{tendencja_24} %",
                fontsize=10,
                y=1,
                pad=-30,
                x=1.04,
            )
            line1 = FigureCanvasTkAgg(wykres, frame_wykresy2)
            line1.get_tk_widget().grid(row=j + 1, column=0, padx=10, ipady=45)

    analiza_scrollbar.config(command=canvas.yview)
    canvas.configure(scrollregion=canvas.bbox("all"))


# endregion
th.Thread(target=wykresy).start()


root.resizable(False, False)
root.mainloop()
