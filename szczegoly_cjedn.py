import tkinter as tk
from ttkbootstrap import Style
from tkinter import *
from tkinter import ttk
from datetime import datetime
import json


def szczegoly_zakupow():
    szczegoly_zakupow_window = tk.Toplevel(bg="#009999")
    szczegoly_zakupow_window.iconbitmap("Dane\icona.ico")
    szczegoly_zakupow_window.configure(padx=10, pady=5)
    szczegoly_zakupow_window.title("Szczegóły zakupów")
    style = Style("flatly")
    style.configure("primary.Treeview.Heading", font=("Helvetica", 12))
    style.configure("core.TLabel", background="#009999", foreground="white")
    # style.configure('primary.TEntry')

    # region szczegoly_zakupow_treeview
    szczegoly_zakupow_treeview = ttk.Treeview(
        szczegoly_zakupow_window,
        style="primary.Treeview",
        show="headings",
        selectmode="browse",
    )
    szczegoly_zakupow_treeview["columns"] = (
        "Data",
        "Krypto",
        "Kupno/Sprzedaż",
        "Cena zl",
        "Cena $",
        "Ilość",
    )
    szczegoly_zakupow_treeview.grid(row=1, column=0, padx=5, pady=5)

    szczegoly_zakupow_treeview.column("Data", width=80, anchor=CENTER)
    szczegoly_zakupow_treeview.column("Krypto", width=95, anchor=CENTER)
    szczegoly_zakupow_treeview.column("Kupno/Sprzedaż", width=95, anchor=CENTER)
    szczegoly_zakupow_treeview.column("Cena zl", width=95, anchor=CENTER)
    szczegoly_zakupow_treeview.column("Cena $", width=80, anchor=CENTER)
    szczegoly_zakupow_treeview.column("Ilość", width=95, anchor=CENTER)

    szczegoly_zakupow_treeview.heading("#0", text="\n")
    szczegoly_zakupow_treeview.heading("Data", text="Data")
    szczegoly_zakupow_treeview.heading("Krypto", text="Nazwa\n Krypto")
    szczegoly_zakupow_treeview.heading("Kupno/Sprzedaż", text="Kupno/\nSprzedaż")
    szczegoly_zakupow_treeview.heading("Cena zl", text="Cena zł")
    szczegoly_zakupow_treeview.heading("Cena $", text="Cena $")
    szczegoly_zakupow_treeview.heading("Ilość", text="Ilość")

    # endregion

    # region Dane szczegoly_zakupow_treeview
    global szczegoly_zakupow_dane
    szczegoly_zakupow_dane = []
    szczegoly_zakupow_filtr_data = []
    szczegoly_zakupow_filtr_krypto = []
    szczegoly_zakupow_filtr_k_s = []

    szczegoly_zakupow_filtr_data.append("Wszystko")
    szczegoly_zakupow_filtr_krypto.append("Wszystko")
    szczegoly_zakupow_filtr_k_s.append("Wszystko")

    def search(list: list, object):
        for i in range(len(list)):
            if list[i] == object:
                return TRUE
        return FALSE

    def clear_treeview(treeview: ttk.Treeview):
        for i in treeview.get_children():
            treeview.delete(i)

    with open("App_file\zmienne.json", "r") as dane:
        zmienne_file = json.load(dane)

    def dane_szczegoly_zakupow_treeview():  # Zwykłe pobranie z pliku z uzupełnienem date
        odczyt = open(str(zmienne_file["Sciezka_Szczegoly_zakupow"]), "r")

        i = 0
        for a in odczyt:
            a = a.splitlines()
            szczegoly_zakupow_dane.append(a)
            szczegoly_zakupow_dane[i] = str(szczegoly_zakupow_dane[i][0]).split(",")
            szczegoly_zakupow_treeview.insert(
                "", "end", values=szczegoly_zakupow_dane[i]
            )
            data = datetime.strptime((szczegoly_zakupow_dane[i][0])[6:], "%Y").strftime(
                "%Y"
            )
            if i == 0:
                szczegoly_zakupow_filtr_data.append(data)
                szczegoly_zakupow_filtr_krypto.append(szczegoly_zakupow_dane[i][1])
                szczegoly_zakupow_filtr_k_s.append(szczegoly_zakupow_dane[i][2])

            if i >= 1:
                if search(szczegoly_zakupow_filtr_data, data) == False:
                    szczegoly_zakupow_filtr_data.append(data)
                if (
                    search(szczegoly_zakupow_filtr_krypto, szczegoly_zakupow_dane[i][1])
                    == False
                ):
                    szczegoly_zakupow_filtr_krypto.append(szczegoly_zakupow_dane[i][1])
                if (
                    search(szczegoly_zakupow_filtr_k_s, szczegoly_zakupow_dane[i][2])
                    == False
                ):
                    szczegoly_zakupow_filtr_k_s.append(szczegoly_zakupow_dane[i][2])

            i += 1

    dane_szczegoly_zakupow_treeview()

    # endregion

    # szczegoly_treeview_cjednostkowa

    # region tabela ceny jednostkowej

    szczegoly_treeview_cjednostkowa = ttk.Treeview(
        szczegoly_zakupow_window,
        style="primary.Treeview",
        show="headings",
        selectmode="browse",
    )
    szczegoly_treeview_cjednostkowa["columns"] = (
        "Krypto",
        "Cena jend. zł",
        "Cena jend. $",
        "Ilosc",
    )
    szczegoly_treeview_cjednostkowa.grid(row=3, column=0, padx=5, pady=5)

    szczegoly_treeview_cjednostkowa.column("Krypto", width=95, anchor=CENTER)
    szczegoly_treeview_cjednostkowa.column("Cena jend. zł", width=95, anchor=CENTER)
    szczegoly_treeview_cjednostkowa.column("Cena jend. $", width=95, anchor=CENTER)
    szczegoly_treeview_cjednostkowa.column("Ilosc", width=95, anchor=CENTER)

    szczegoly_treeview_cjednostkowa.heading("#0", text="\n")
    szczegoly_treeview_cjednostkowa.heading("Krypto", text="Nazwa\n krypto")
    szczegoly_treeview_cjednostkowa.heading("Cena jend. zł", text="Cena jend.\n    zł")
    szczegoly_treeview_cjednostkowa.heading("Cena jend. $", text="Cena jend.\n    $")
    szczegoly_treeview_cjednostkowa.heading("Ilosc", text="Ilość")

    # endregion

    # region dane ceny jendostkowej

    global szczegoly_treeview_cjednostkowa_dane
    szczegoly_treeview_cjednostkowa_dane = []

    def tab_cjednostkowa_dane():
        unique_krypto = []
        global szczegoly_treeview_cjednostkowa_dane
        global szczegoly_zakupow_dane
        szczegoly_treeview_cjednostkowa_dane.clear()
        for i in szczegoly_zakupow_dane:
            if search(unique_krypto, i[1]) == False:
                unique_krypto.append(i[1])

        # print(szczegoly_zakupow_dane)

        for krypto in unique_krypto:
            tab1 = []
            for j in szczegoly_zakupow_dane:
                if j[1] == krypto:
                    tab1.append(j)
            cena_z = 0  # cena złotówki wspólna dla każdej krypto
            cena_d = 0  # cena dolar wspólna dla każdej krypto
            ilosc = 0  # ilość wspólna dla każdej krypto
            for j in range(len(tab1)):
                if tab1[j][2] == "Kupno":
                    cena_z += float(tab1[j][3])
                    cena_d += float(tab1[j][4])
                    ilosc = (ilosc + float(tab1[j][5])).__round__(8)

                if tab1[j][2] == "Sprzedaz":
                    cena_z -= float(tab1[j][3])
                    cena_d -= float(tab1[j][4])
                    ilosc = (ilosc - float(tab1[j][5])).__round__(8)

            if ilosc != 0:
                if cena_z < 0:
                    cena_jedn_zl = 0
                    cena_jedn_d = 0
                else:
                    cena_jedn_zl = (cena_z / ilosc).__round__(2)
                    cena_jedn_d = (cena_d / ilosc).__round__(2)
                cena_z = cena_z.__round__(2)
                cena_d = cena_d.__round__(2)
                szczegoly_treeview_cjednostkowa_dane.append(
                    [krypto, cena_jedn_zl, cena_jedn_d, ilosc, cena_z, cena_d]
                )

        clear_treeview(szczegoly_treeview_cjednostkowa)

        for row in szczegoly_treeview_cjednostkowa_dane:
            # wycięcie rekordów gdzie nie zostały sprzedane wszystkie krypto
            if row[3] != 0:
                szczegoly_treeview_cjednostkowa.insert("", "end", values=row[:4])

    tab_cjednostkowa_dane()

    # endregion

    def update_portfel():
        # region Porównanie wartości w portfelu

        with open(str(zmienne_file["Sciezka_portfel"]), "r") as odczyt:
            dane_portfel = odczyt.read()

        dane_portfel = dane_portfel.splitlines()
        for i in range(len(dane_portfel)):
            dane_portfel[i] = dane_portfel[i].split(",")

        def search2(list, j, object):
            for i in range(len(list)):
                if list[i][j] == object:
                    return TRUE
            return FALSE

        # print(szczegoly_treeview_cjednostkowa_dane) #['BCH', 1641.37, 441.43, 0.05790292, 95.04, 25.56],

        delete_date = []

        # wyszukanie krypto z portfela których nie ma w cenach jednostkowych
        for j in range(len(dane_portfel)):
            if (
                search2(szczegoly_treeview_cjednostkowa_dane, 0, dane_portfel[j][0])
                == False
            ):
                delete_date.append(dane_portfel[j])

        # Usunięcie wierszy nie będących w cenach jednostkowych
        for i in delete_date:
            dane_portfel.remove(i)

        for i in range(len(szczegoly_treeview_cjednostkowa_dane)):
            for j in range(len(dane_portfel)):
                if (
                    search2(dane_portfel, 0, szczegoly_treeview_cjednostkowa_dane[i][0])
                    == False
                    and szczegoly_treeview_cjednostkowa_dane[i][3] > 0
                ):
                    append_date = [
                        str(szczegoly_treeview_cjednostkowa_dane[i][0]),
                        str(szczegoly_treeview_cjednostkowa_dane[i][4]),
                        str(szczegoly_treeview_cjednostkowa_dane[i][5]),
                        str(szczegoly_treeview_cjednostkowa_dane[i][3]),
                    ]
                    dane_portfel.append(append_date)

                if (
                    dane_portfel[j][0] == szczegoly_treeview_cjednostkowa_dane[i][0]
                    and dane_portfel[j][3] != szczegoly_treeview_cjednostkowa_dane[i][3]
                ):
                    # warunek 0 lub mniej
                    dane_portfel[j][1] = str(
                        (szczegoly_treeview_cjednostkowa_dane[i][4]).__round__(2)
                    )  # zł
                    dane_portfel[j][2] = str(
                        (szczegoly_treeview_cjednostkowa_dane[i][5]).__round__(2)
                    )  # dolar
                    dane_portfel[j][3] = str(
                        szczegoly_treeview_cjednostkowa_dane[i][3]
                    )  # ilosc

        with open(str(zmienne_file["Sciezka_portfel"]), "w") as zapis:
            for i in range(len(dane_portfel)):
                a = ",".join(dane_portfel[i])
                zapis.write(a)
                if i < len(dane_portfel) - 1:
                    zapis.write("\n")

    # endregion

    tabela_wybrana = []

    def filtr_szczegoly_zakupow(event):
        wybrana_data = szczegoly_zakupow_combobox_data.get()
        wybrana_krypto = szczegoly_zakupow_combobox_krypto.get()
        wybrana_b_s = szczegoly_zakupow_combobox_b_s.get()
        clear_treeview(szczegoly_zakupow_treeview)

        szczegoly_zakupow_filtr_data2 = []
        szczegoly_zakupow_filtr_krypto2 = []
        szczegoly_zakupow_filtr_k_s2 = []
        szczegoly_zakupow_filtr_data2.append("Wszystko")
        szczegoly_zakupow_filtr_krypto2.append("Wszystko")
        szczegoly_zakupow_filtr_k_s2.append("Wszystko")

        if wybrana_data != "Wszystko":
            if wybrana_krypto != "Wszystko" and len(tabela_wybrana) > 0:
                wynik_tab = []
                for i in range(len(tabela_wybrana)):
                    data = datetime.strptime((tabela_wybrana[i][0])[6:], "%Y").strftime(
                        "%Y"
                    )

                    if tabela_wybrana[i][1] == wybrana_krypto:
                        if search(szczegoly_zakupow_filtr_data2, data) == False:
                            szczegoly_zakupow_filtr_data2.append(data)
                        if (
                            search(
                                szczegoly_zakupow_filtr_krypto2, tabela_wybrana[i][1]
                            )
                            == False
                        ):
                            szczegoly_zakupow_filtr_krypto2.append(tabela_wybrana[i][1])
                        elif (
                            search(szczegoly_zakupow_filtr_k_s2, tabela_wybrana[i][2])
                            == False
                        ):
                            szczegoly_zakupow_filtr_k_s2.append(tabela_wybrana[i][2])

                        wynik_tab.append(tabela_wybrana[i])

                szczegoly_zakupow_combobox_data[
                    "values"
                ] = szczegoly_zakupow_filtr_data2
                szczegoly_zakupow_combobox_krypto[
                    "values"
                ] = szczegoly_zakupow_filtr_krypto2
                szczegoly_zakupow_combobox_b_s["values"] = szczegoly_zakupow_filtr_k_s2

                tabela_wybrana.clear()
                for row in wynik_tab:
                    szczegoly_zakupow_treeview.insert("", "end", values=row)
                    tabela_wybrana.append(row)

                if wybrana_b_s != "Wszystko" and len(tabela_wybrana) > 0:
                    wynik_tab = []

                    del szczegoly_zakupow_filtr_data2[1:]
                    del szczegoly_zakupow_filtr_krypto2[1:]
                    del szczegoly_zakupow_filtr_k_s2[1:]

                    for i in range(len(tabela_wybrana)):
                        data = datetime.strptime(
                            (tabela_wybrana[i][0])[6:], "%Y"
                        ).strftime("%Y")

                        if tabela_wybrana[i][2] == wybrana_b_s:
                            if search(szczegoly_zakupow_filtr_data2, data) == False:
                                szczegoly_zakupow_filtr_data2.append(data)
                            if (
                                search(
                                    szczegoly_zakupow_filtr_krypto2,
                                    tabela_wybrana[i][1],
                                )
                                == False
                            ):
                                szczegoly_zakupow_filtr_krypto2.append(
                                    tabela_wybrana[i][1]
                                )
                            elif (
                                search(
                                    szczegoly_zakupow_filtr_k_s2, tabela_wybrana[i][2]
                                )
                                == False
                            ):
                                szczegoly_zakupow_filtr_k_s2.append(
                                    tabela_wybrana[i][2]
                                )

                            wynik_tab.append(tabela_wybrana[i])

                    szczegoly_zakupow_combobox_data[
                        "values"
                    ] = szczegoly_zakupow_filtr_data2
                    szczegoly_zakupow_combobox_krypto[
                        "values"
                    ] = szczegoly_zakupow_filtr_krypto2
                    szczegoly_zakupow_combobox_b_s[
                        "values"
                    ] = szczegoly_zakupow_filtr_k_s2
                    clear_treeview(szczegoly_zakupow_treeview)
                    for row in wynik_tab:
                        szczegoly_zakupow_treeview.insert("", "end", values=row)

            elif wybrana_b_s != "Wszystko" and len(tabela_wybrana) > 0:
                wynik_tab = []
                for i in range(len(tabela_wybrana)):
                    data = datetime.strptime((tabela_wybrana[i][0])[6:], "%Y").strftime(
                        "%Y"
                    )

                    if tabela_wybrana[i][2] == wybrana_b_s:
                        if search(szczegoly_zakupow_filtr_data2, data) == False:
                            szczegoly_zakupow_filtr_data2.append(data)
                        if (
                            search(
                                szczegoly_zakupow_filtr_krypto2, tabela_wybrana[i][1]
                            )
                            == False
                        ):
                            szczegoly_zakupow_filtr_krypto2.append(tabela_wybrana[i][1])
                        elif (
                            search(szczegoly_zakupow_filtr_k_s2, tabela_wybrana[i][2])
                            == False
                        ):
                            szczegoly_zakupow_filtr_k_s2.append(tabela_wybrana[i][2])

                        wynik_tab.append(tabela_wybrana[i])

                szczegoly_zakupow_combobox_data[
                    "values"
                ] = szczegoly_zakupow_filtr_data2
                szczegoly_zakupow_combobox_krypto[
                    "values"
                ] = szczegoly_zakupow_filtr_krypto2
                szczegoly_zakupow_combobox_b_s["values"] = szczegoly_zakupow_filtr_k_s2
                tabela_wybrana.clear()

                for row in wynik_tab:
                    szczegoly_zakupow_treeview.insert("", "end", values=row)
                    tabela_wybrana.append(row)

                if wybrana_krypto != "Wszystko" and len(tabela_wybrana) > 0:
                    wynik_tab = []
                    for i in range(len(tabela_wybrana)):
                        data = datetime.strptime(
                            (tabela_wybrana[i][0])[6:], "%Y"
                        ).strftime("%Y")

                        if tabela_wybrana[i][1] == wybrana_b_s:
                            if search(szczegoly_zakupow_filtr_data2, data) == False:
                                szczegoly_zakupow_filtr_data2.append(data)
                            if (
                                search(
                                    szczegoly_zakupow_filtr_krypto2,
                                    tabela_wybrana[i][1],
                                )
                                == False
                            ):
                                szczegoly_zakupow_filtr_krypto2.append(
                                    tabela_wybrana[i][1]
                                )
                            elif (
                                search(
                                    szczegoly_zakupow_filtr_k_s2, tabela_wybrana[i][2]
                                )
                                == False
                            ):
                                szczegoly_zakupow_filtr_k_s2.append(
                                    tabela_wybrana[i][2]
                                )

                            wynik_tab.append(tabela_wybrana[i])

                    szczegoly_zakupow_combobox_data[
                        "values"
                    ] = szczegoly_zakupow_filtr_data2
                    szczegoly_zakupow_combobox_krypto[
                        "values"
                    ] = szczegoly_zakupow_filtr_krypto2
                    szczegoly_zakupow_combobox_b_s[
                        "values"
                    ] = szczegoly_zakupow_filtr_k_s2
                    clear_treeview(szczegoly_zakupow_treeview)
                    for row in wynik_tab:
                        szczegoly_zakupow_treeview.insert("", "end", values=row)

            else:
                tabela_wybrana.clear()
                for i in range(len(szczegoly_zakupow_dane)):
                    data = datetime.strptime(
                        (szczegoly_zakupow_dane[i][0])[6:], "%Y"
                    ).strftime("%Y")

                    if ((szczegoly_zakupow_dane[i][0])[6:]) == wybrana_data:
                        if search(szczegoly_zakupow_filtr_data2, data) == False:
                            szczegoly_zakupow_filtr_data2.append(data)
                        elif (
                            search(
                                szczegoly_zakupow_filtr_krypto2,
                                szczegoly_zakupow_dane[i][1],
                            )
                            == False
                        ):
                            szczegoly_zakupow_filtr_krypto2.append(
                                szczegoly_zakupow_dane[i][1]
                            )
                        elif (
                            search(
                                szczegoly_zakupow_filtr_k_s2,
                                szczegoly_zakupow_dane[i][2],
                            )
                            == False
                        ):
                            szczegoly_zakupow_filtr_k_s2.append(
                                szczegoly_zakupow_dane[i][2]
                            )

                        tabela_wybrana.append(szczegoly_zakupow_dane[i])

                szczegoly_zakupow_combobox_data[
                    "values"
                ] = szczegoly_zakupow_filtr_data2
                szczegoly_zakupow_combobox_krypto[
                    "values"
                ] = szczegoly_zakupow_filtr_krypto2
                szczegoly_zakupow_combobox_b_s["values"] = szczegoly_zakupow_filtr_k_s2

                for row in tabela_wybrana:
                    szczegoly_zakupow_treeview.insert("", "end", values=row)

        elif wybrana_krypto != "Wszystko":
            if wybrana_b_s != "Wszystko" and len(tabela_wybrana) > 0:
                wynik_tab = []
                for i in range(len(tabela_wybrana)):
                    data = datetime.strptime(
                        (szczegoly_zakupow_dane[i][0])[6:], "%Y"
                    ).strftime("%Y")

                    if tabela_wybrana[i][2] == wybrana_b_s:
                        if search(szczegoly_zakupow_filtr_data2, data) == False:
                            szczegoly_zakupow_filtr_data2.append(data)
                        if (
                            search(
                                szczegoly_zakupow_filtr_krypto2, tabela_wybrana[i][1]
                            )
                            == False
                        ):
                            szczegoly_zakupow_filtr_krypto2.append(tabela_wybrana[i][1])
                        elif (
                            search(szczegoly_zakupow_filtr_k_s2, tabela_wybrana[i][2])
                            == False
                        ):
                            szczegoly_zakupow_filtr_k_s2.append(tabela_wybrana[i][2])

                        wynik_tab.append(tabela_wybrana[i])

                szczegoly_zakupow_combobox_data[
                    "values"
                ] = szczegoly_zakupow_filtr_data2
                szczegoly_zakupow_combobox_krypto[
                    "values"
                ] = szczegoly_zakupow_filtr_krypto2
                szczegoly_zakupow_combobox_b_s["values"] = szczegoly_zakupow_filtr_k_s2

                # tabela_wybrana.clear()
                for row in wynik_tab:
                    szczegoly_zakupow_treeview.insert("", "end", values=row)

            else:
                tabela_wybrana.clear()
                for i in range(len(szczegoly_zakupow_dane)):
                    data = datetime.strptime(
                        (szczegoly_zakupow_dane[i][0])[6:], "%Y"
                    ).strftime("%Y")

                    if szczegoly_zakupow_dane[i][1] == wybrana_krypto:
                        if search(szczegoly_zakupow_filtr_data2, data) == False:
                            szczegoly_zakupow_filtr_data2.append(data)
                        elif (
                            search(
                                szczegoly_zakupow_filtr_krypto2,
                                szczegoly_zakupow_dane[i][1],
                            )
                            == False
                        ):
                            szczegoly_zakupow_filtr_krypto2.append(
                                szczegoly_zakupow_dane[i][1]
                            )
                        elif (
                            search(
                                szczegoly_zakupow_filtr_k_s2,
                                szczegoly_zakupow_dane[i][2],
                            )
                            == False
                        ):
                            szczegoly_zakupow_filtr_k_s2.append(
                                szczegoly_zakupow_dane[i][2]
                            )

                        tabela_wybrana.append(szczegoly_zakupow_dane[i])

                szczegoly_zakupow_combobox_data[
                    "values"
                ] = szczegoly_zakupow_filtr_data2
                szczegoly_zakupow_combobox_krypto[
                    "values"
                ] = szczegoly_zakupow_filtr_krypto2
                szczegoly_zakupow_combobox_b_s["values"] = szczegoly_zakupow_filtr_k_s2

                for row in tabela_wybrana:
                    szczegoly_zakupow_treeview.insert("", "end", values=row)

        elif wybrana_b_s != "Wszystko":
            tabela_wybrana.clear()
            for i in range(len(szczegoly_zakupow_dane)):
                data = datetime.strptime(
                    (szczegoly_zakupow_dane[i][0])[6:], "%Y"
                ).strftime("%Y")

                if szczegoly_zakupow_dane[i][2] == wybrana_b_s:
                    if search(szczegoly_zakupow_filtr_data2, data) == False:
                        szczegoly_zakupow_filtr_data2.append(data)
                    elif (
                        search(
                            szczegoly_zakupow_filtr_krypto2,
                            szczegoly_zakupow_dane[i][1],
                        )
                        == False
                    ):
                        szczegoly_zakupow_filtr_krypto2.append(
                            szczegoly_zakupow_dane[i][1]
                        )
                    elif (
                        search(
                            szczegoly_zakupow_filtr_k_s2, szczegoly_zakupow_dane[i][2]
                        )
                        == False
                    ):
                        szczegoly_zakupow_filtr_k_s2.append(
                            szczegoly_zakupow_dane[i][2]
                        )

                    tabela_wybrana.append(szczegoly_zakupow_dane[i])

            szczegoly_zakupow_combobox_data["values"] = szczegoly_zakupow_filtr_data2
            szczegoly_zakupow_combobox_krypto[
                "values"
            ] = szczegoly_zakupow_filtr_krypto2
            szczegoly_zakupow_combobox_b_s["values"] = szczegoly_zakupow_filtr_k_s2

            for row in tabela_wybrana:
                szczegoly_zakupow_treeview.insert("", "end", values=row)

        elif (
            wybrana_data == "Wszystko"
            and wybrana_krypto == "Wszystko"
            and wybrana_b_s == "Wszystko"
        ):
            for row in szczegoly_zakupow_dane:
                szczegoly_zakupow_treeview.insert("", "end", values=row)
            szczegoly_zakupow_combobox_data["values"] = szczegoly_zakupow_filtr_data
            szczegoly_zakupow_combobox_krypto["values"] = szczegoly_zakupow_filtr_krypto
            szczegoly_zakupow_combobox_b_s["values"] = szczegoly_zakupow_filtr_k_s

    # edit_method

    def clear_entry():
        szczegoly_zakupow_entry_data.delete(0, END)
        szczegoly_zakupow_entry_krypto.delete(0, END)
        szczegoly_zakupow_entry_k_s.delete(0, END)
        szczegoly_zakupow_entry_cena_zl.delete(0, END)
        szczegoly_zakupow_entry_cena_d.delete(0, END)
        szczegoly_zakupow_entry_ilosc.delete(0, END)

    def edit_wybierz():
        selected_date = szczegoly_zakupow_treeview.item(
            szczegoly_zakupow_treeview.selection()
        )[
            "values"
        ]  # ['02.04.2021', 'ETH', 'Sprzedaz', '15785.59', '4047.59', 2]

        clear_entry()

        szczegoly_zakupow_entry_data.insert(0, str(selected_date[0]))
        szczegoly_zakupow_entry_krypto.insert(0, str(selected_date[1]))
        szczegoly_zakupow_entry_k_s.insert(0, selected_date[2])
        szczegoly_zakupow_entry_cena_zl.insert(0, selected_date[3])
        szczegoly_zakupow_entry_cena_d.insert(0, selected_date[4])
        szczegoly_zakupow_entry_ilosc.insert(0, selected_date[5])

    def edit_dodaj():
        add_date = []
        add_date.insert(0, szczegoly_zakupow_entry_data.get())
        add_date.insert(1, szczegoly_zakupow_entry_krypto.get())
        add_date.insert(2, szczegoly_zakupow_entry_k_s.get())
        add_date.insert(3, szczegoly_zakupow_entry_cena_zl.get())
        add_date.insert(4, szczegoly_zakupow_entry_cena_d.get())
        add_date.insert(5, szczegoly_zakupow_entry_ilosc.get())

        szczegoly_zakupow_treeview.insert("", "end", values=add_date)
        clear_entry()

        # dodawnie do pliku
        s_add_date = ",".join(add_date)

        with open(str(zmienne_file["Sciezka_Szczegoly_zakupow"]), "a") as sz_z:
            sz_z.write("\n")
            sz_z.write(s_add_date)

        tab_cjednostkowa_dane()

    def edit_usun():
        selected_date = szczegoly_zakupow_treeview.selection()
        szczegoly_zakupow_treeview.delete(selected_date)

        con_line = []
        for line in range(len(szczegoly_zakupow_treeview.get_children())):
            con_line_1 = []
            for value in szczegoly_zakupow_treeview.item(
                szczegoly_zakupow_treeview.get_children()[line]
            )["values"]:
                v = str(value)
                con_line_1.append(v)
            con_line.append(con_line_1)

        with open(str(zmienne_file["Sciezka_Szczegoly_zakupow"]), "w") as usun:
            for i in range(len(con_line)):
                a = ",".join(con_line[i])
                usun.write(a)
                if i < len(con_line) - 1:  # ostatnia linia bez nowej linii
                    usun.write("\n")

    def edit_zamien():
        add_date = []
        add_date.insert(0, szczegoly_zakupow_entry_data.get())
        add_date.insert(1, szczegoly_zakupow_entry_krypto.get())
        add_date.insert(2, szczegoly_zakupow_entry_k_s.get())
        add_date.insert(3, szczegoly_zakupow_entry_cena_zl.get())
        add_date.insert(4, szczegoly_zakupow_entry_cena_d.get())
        add_date.insert(5, szczegoly_zakupow_entry_ilosc.get())

        szczegoly_zakupow_treeview.item(
            szczegoly_zakupow_treeview.selection(), values=add_date
        )

        con_line = []
        for line in range(len(szczegoly_zakupow_treeview.get_children())):
            con_line_1 = []
            for value in szczegoly_zakupow_treeview.item(
                szczegoly_zakupow_treeview.get_children()[line]
            )["values"]:
                v = str(value)
                con_line_1.append(v)
            con_line.append(con_line_1)

        with open(str(zmienne_file["Sciezka_Szczegoly_zakupow"]), "w") as zmien:
            for i in range(len(con_line)):
                a = ",".join(con_line[i])
                zmien.write(a)
                if i < len(con_line) - 1:  # ostatnia linia bez nowej linii
                    zmien.write("\n")
        clear_entry()

    # region Frame_filtry

    szczegoly_zakupow_frame_filtry = Frame(szczegoly_zakupow_window, bg="#009999")
    szczegoly_zakupow_frame_filtry.grid(row=0, column=0)

    szczegoly_zakupow_label_data = ttk.Label(
        szczegoly_zakupow_frame_filtry,
        text="Data:",
        style="core.TLabel",
        font=("Helvetica", 12),
    )
    szczegoly_zakupow_label_data.grid(row=0, column=0)
    szczegoly_zakupow_combobox_data = ttk.Combobox(
        szczegoly_zakupow_frame_filtry, text="Data"
    )  # Ustawić opcje bez edycji
    szczegoly_zakupow_combobox_data.configure(
        state="readonly", values=szczegoly_zakupow_filtr_data
    )  # działa
    szczegoly_zakupow_combobox_data.current(0)
    szczegoly_zakupow_combobox_data.bind(
        "<<ComboboxSelected>>", filtr_szczegoly_zakupow
    )  # on choice
    szczegoly_zakupow_combobox_data.grid(row=1, column=0)

    szczegoly_zakupow_label_krypto = ttk.Label(
        szczegoly_zakupow_frame_filtry,
        text="Krypto:",
        style="core.TLabel",
        font=("Helvetica", 12),
    )
    szczegoly_zakupow_label_krypto.grid(row=0, column=1)
    szczegoly_zakupow_combobox_krypto = ttk.Combobox(
        szczegoly_zakupow_frame_filtry, text="krypto"
    )
    szczegoly_zakupow_combobox_krypto.configure(
        state="readonly", values=szczegoly_zakupow_filtr_krypto
    )
    szczegoly_zakupow_combobox_krypto.current(0)
    szczegoly_zakupow_combobox_krypto.bind(
        "<<ComboboxSelected>>", filtr_szczegoly_zakupow
    )
    szczegoly_zakupow_combobox_krypto.grid(row=1, column=1)

    szczegoly_zakupow_label_b_s = ttk.Label(
        szczegoly_zakupow_frame_filtry,
        text="Kupno/Sprzedaż:",
        style="core.TLabel",
        font=("Helvetica", 12),
    )
    szczegoly_zakupow_label_b_s.grid(row=0, column=2)
    szczegoly_zakupow_combobox_b_s = ttk.Combobox(
        szczegoly_zakupow_frame_filtry, text="kupno/Sprzedaż"
    )
    szczegoly_zakupow_combobox_b_s.configure(
        state="readonly", values=szczegoly_zakupow_filtr_k_s
    )
    szczegoly_zakupow_combobox_b_s.current(0)
    szczegoly_zakupow_combobox_b_s.bind("<<ComboboxSelected>>", filtr_szczegoly_zakupow)
    szczegoly_zakupow_combobox_b_s.grid(row=1, column=2)

    # endregion

    # region edycji danych szczególy zakupu

    szczegoly_zakupow_frame_edit = Frame(szczegoly_zakupow_window, bg="#009999")
    szczegoly_zakupow_frame_edit.grid(row=2, column=0)

    szczegoly_zakupow_entry_data = ttk.Entry(
        szczegoly_zakupow_frame_edit, style="primary.TEntry", width=11
    )
    szczegoly_zakupow_entry_data.grid(row=0, column=0)

    szczegoly_zakupow_entry_krypto = ttk.Entry(
        szczegoly_zakupow_frame_edit, style="primary.TEntry", width=11
    )
    szczegoly_zakupow_entry_krypto.grid(row=0, column=1)

    szczegoly_zakupow_entry_k_s = ttk.Entry(
        szczegoly_zakupow_frame_edit, style="primary.TEntry", width=11
    )
    szczegoly_zakupow_entry_k_s.grid(row=0, column=2)

    szczegoly_zakupow_entry_cena_zl = ttk.Entry(
        szczegoly_zakupow_frame_edit, style="primary.TEntry", width=11
    )
    szczegoly_zakupow_entry_cena_zl.grid(row=0, column=3)

    szczegoly_zakupow_entry_cena_d = ttk.Entry(
        szczegoly_zakupow_frame_edit, style="primary.TEntry", width=11
    )
    szczegoly_zakupow_entry_cena_d.grid(row=0, column=4)

    szczegoly_zakupow_entry_ilosc = ttk.Entry(
        szczegoly_zakupow_frame_edit, style="primary.TEntry", width=11
    )
    szczegoly_zakupow_entry_ilosc.grid(row=0, column=5)

    szczegoly_zakupow_frame_edit_button = Frame(
        szczegoly_zakupow_frame_edit, bg="#009999"
    )
    szczegoly_zakupow_frame_edit_button.grid(row=1, column=0, columnspan=6)

    szczegoly_zakupow_button_wyczysc = ttk.Button(
        szczegoly_zakupow_frame_edit_button,
        text="Wyczyść",
        style="primary.TButton",
        command=clear_entry,
    )
    szczegoly_zakupow_button_wyczysc.grid(row=0, column=0, padx=5, pady=5)

    szczegoly_zakupow_button_wybierz = ttk.Button(
        szczegoly_zakupow_frame_edit_button,
        text="Wybierz",
        style="primary.TButton",
        command=edit_wybierz,
    )
    szczegoly_zakupow_button_wybierz.grid(row=0, column=1, padx=5, pady=5)

    szczegoly_zakupow_button_zamien = ttk.Button(
        szczegoly_zakupow_frame_edit_button,
        text="Zamień",
        style="primary.TButton",
        command=edit_zamien,
    )
    szczegoly_zakupow_button_zamien.grid(row=0, column=2, padx=5, pady=5)

    szczegoly_zakupow_button_dodaj = ttk.Button(
        szczegoly_zakupow_frame_edit_button,
        text="Dodaj",
        style="primary.TButton",
        command=edit_dodaj,
    )
    szczegoly_zakupow_button_dodaj.grid(row=0, column=3, padx=5, pady=5)

    szczegoly_zakupow_button_usun = ttk.Button(
        szczegoly_zakupow_frame_edit_button,
        text="Usuń",
        style="primary.TButton",
        command=edit_usun,
    )
    szczegoly_zakupow_button_usun.grid(row=0, column=4, padx=5, pady=5)

    szczegoly_zakupow_button_update_portfel = ttk.Button(
        szczegoly_zakupow_frame_edit_button,
        text="Aktualizacja\n Portfela",
        command=update_portfel,
    )
    szczegoly_zakupow_button_update_portfel.grid(row=0, column=5, padx=5, pady=5)

    # endregion

    szczegoly_zakupow_window.resizable(False, False)

    # for test only
    # szczegoly_zakupow_window.mainloop()


# for test only
# szczegoly_zakupow()
