import tkinter.messagebox as msgbox
from datetime import datetime
from Classes import AreaFrame, TopFrame, ReadFile


def purchers_area_ingredients(choice_wallet: str) -> None:
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

    exist = False
    try:
        purchase_details_data = ReadFile(
            f"Dane\Details_wallet_{choice_wallet}.txt", "txt"
        )
        exist = True
    except FileNotFoundError:
        msgbox.showinfo("Informacja", "Niestety nie ma szczegółów tego portfela.")
    if exist:
        purchase_details_window = TopFrame()
        purchase_details_area = AreaFrame(onFrame=purchase_details_window.frame)
        purchase_details_area.text_display(text="Data", row=0, column=0, columnspan=2)
        purchase_details_area.text_display(text="Nazwa", row=0, column=2, columnspan=2)
        purchase_details_area.text_display(
            text="Sprzedaż/Kupno", row=0, column=4, columnspan=2
        )

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
            purchase_details_area.objList[6], purchase_details_data.file_list, "txt"
        )

        purchase_details_area.add_data_in_treeview(
            purchase_details_area.objList[19], calculate_unit_price()
        )

    # unit price column and data
