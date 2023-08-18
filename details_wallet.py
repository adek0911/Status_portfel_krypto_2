import tkinter.messagebox as msgbox
from datetime import datetime
from Classes import AreaFrame, ReadFile

# from appOnClass import bottom2_area
import ttkbootstrap as ttk


def purchers_area_ingredients(choice_wallet: str, button_obj: ttk.Button) -> None:
    def button_change_state():
        button_obj.configure(state="normal")
        purchase_details_window.destroy()

    def upadate_data_filtr():
        result = ["Wszystko"]
        for i in range(len(purchase_details_data.file_data)):
            tmp = datetime.strptime(
                purchase_details_data.file_data[i][0][6:], "%Y"
            ).strftime("%Y")
            if tmp not in result:
                result.append(tmp)
        return result

    def update_filtr(value: int):
        result = []
        for i in range(len(purchase_details_data.file_data)):
            result.append(purchase_details_data.file_data[i][value])
        result = list(set(result))
        result.insert(0, "Wszystko")
        return result

    def sort_treeView(event) -> None:
        result = []
        data: str = purchase_details_area.dict_combo["Data_filtr"].get()
        name: str = purchase_details_area.dict_combo["Name_filtr"].get()
        status: str = purchase_details_area.dict_combo["Status_filtr"].get()

        status_combo = [data, name, status]
        count_stat = status_combo.count("Wszystko")

        if count_stat == 2:  # 1 filtr
            for i, value in enumerate(status_combo):
                if value != "Wszystko":
                    if i == 0:
                        for j in purchase_details_data.file_list:
                            if j[0][6:] == value:
                                result.append(j)
                    else:
                        for j in purchase_details_data.file_list:
                            if j[i] == value:
                                result.append(j)

        elif count_stat == 1:  # 2 filtry
            if status_combo[0] != "Wszystko" and status_combo[1] != "Wszystko":
                for i in purchase_details_data.file_list:
                    if i[0][6:] == data and i[1] == name:
                        result.append(i)
            if status_combo[1] != "Wszystko" and status_combo[2] != "Wszystko":
                for i in purchase_details_data.file_list:
                    if i[1] == name and i[2] == status:
                        result.append(i)
            if status_combo[0] != "Wszystko" and status_combo[2] != "Wszystko":
                for i in purchase_details_data.file_list:
                    if i[0][6:] == data and i[2] == status:
                        result.append(i)
        elif count_stat == 0:  # 3 filtry
            for i in purchase_details_data.file_list:
                if i[0][6:] == data and i[1] == name and i[2] == status:
                    result.append(i)
        else:
            result = purchase_details_data.file_list

        purchase_details_area.add_data_in_treeview(
            purchase_details_area.objList[3], result
        )

    def calculate_unit_price() -> list:
        # Zastanowić się czy nie lepiej żeby zwracał listę/tuple jako odpowiedź
        result_list = []
        unique_name = []

        quantity = 0  # ilość
        for crypto in purchase_details_data.file_data:
            if not crypto[1] in unique_name and crypto[2] == "Kupno":
                unique_name.append(crypto[1])
                result_list.append([])
                result_list[unique_name.index(crypto[1])].extend(
                    [crypto[3], crypto[4], crypto[5]]
                )
            elif crypto[2] == "Kupno":
                for i in range(3):
                    result_list[unique_name.index(crypto[1])][i] += crypto[
                        i + 3
                    ].__round__(5)
            elif crypto[2] == "Sprzedaz":
                for i in range(3):
                    result_list[unique_name.index(crypto[1])][i] -= crypto[
                        i + 3
                    ].__round__(5)

        for i in range(len(result_list)):
            if result_list[i][0] <= 0:
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
                        result_list[i][3],  # Cena jednostkowa pln
                        result_list[i][4],  # Cena jednostokowa $
                        result_list[i][2],  # Ilość
                    ]
                )
        return output_list
        # [95.04, 25.56, 0.0579, 1641.45, 441.45]
        # dane w pliku data, nazwa, kupno/sprzedaz, cena_z, cena_dolar,ilość
        # pobrać nazwy, cena_złotówki, cena_dolar, ilość,

    # all method for buttons
    def button_clear():
        for i in range(4, 10):
            if i != 6:
                purchase_details_area.objList[i].delete(0, "end")

    def button_selected():
        button_clear()
        selected = purchase_details_area.objList[3].item(
            purchase_details_area.objList[3].selection()
        )["values"]
        for i in range(4, 10):
            purchase_details_area.objList[i].insert(0, str(selected[i - 4]))

    def button_change():
        # Warning if wont change data
        change_data = []
        for i in range(4, 10):
            change_data.append(purchase_details_area.objList[i].get())

        purchase_details_area.objList[3].item(
            purchase_details_area.objList[3].selection(), values=change_data
        )
        pass

    def button_add():
        # create data control
        add_data = []
        for i in range(4, 10):
            add_data.append(purchase_details_area.objList[i].get())
        purchase_details_area.objList[3].insert("", "end", values=add_data)
        button_clear()

    def button_delete():
        purchase_details_area.objList[3].delete(
            purchase_details_area.objList[3].selection()
        )

        # add delete from file
        pass

    def button_update_wallet():
        pass

    # exist = False
    try:
        purchase_details_data = ReadFile(
            f"Dane\Details_wallet_{choice_wallet}.txt", "txt"
        )
        # exist = True

    except FileNotFoundError:
        msgbox.showinfo("Informacja", "Niestety nie ma szczegółów tego portfela.")
    else:
        button_obj.configure(state="disable")
        purchase_details_window = ttk.Toplevel()
        purchase_details_window.style.configure(
            "primary.Treeview", rowheight=22, borderwidth=0
        )
        purchase_details_window.protocol("WM_DELETE_WINDOW", button_change_state)
        purchase_details_area = AreaFrame(onFrame=purchase_details_window)
        status_transaction = ("Kupno", "Sprzedaz")
        purchase_details_area.text_display(text="Data", row=0, column=0, columnspan=2)
        purchase_details_area.text_display(text="Nazwa", row=0, column=2, columnspan=2)
        purchase_details_area.text_display(
            text="Sprzedaż/Kupno", row=0, column=4, columnspan=2
        )

        # name tmp only for tests
        filter_type = {"Crypto_name": 1, "Status_transaction": 2}

        purchase_details_area.combobox_display(
            values=upadate_data_filtr(),
            width=10,
            row=1,
            column=0,
            columnspan=2,
            name="Data_filtr",
        )
        purchase_details_area.combobox_display(
            values=update_filtr(filter_type["Crypto_name"]),
            width=10,
            row=1,
            column=2,
            columnspan=2,
            name="Name_filtr",
        )
        purchase_details_area.combobox_display(
            values=update_filtr(filter_type["Status_transaction"]),
            width=10,
            row=1,
            column=4,
            columnspan=2,
            name="Status_filtr",
        )
        purchase_details_area.dict_combo["Data_filtr"].bind(
            "<<ComboboxSelected>>", sort_treeView
        )
        purchase_details_area.dict_combo["Name_filtr"].bind(
            "<<ComboboxSelected>>", sort_treeView
        )
        purchase_details_area.dict_combo["Status_filtr"].bind(
            "<<ComboboxSelected>>", sort_treeView
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
        )
        # add data from file , create new instant and download data

        # 6 entry
        for i in range(6):
            if i != 2:
                purchase_details_area.entry_display(row=3, column=i)
            else:
                purchase_details_area.combobox_display(
                    values=status_transaction,
                    row=3,
                    column=i,
                    width=10,
                    name="combo_status_transaction",
                )

        # 6 button
        button_names = (
            "Wyczyść",
            "Wybierz",
            "Zamień",
            "Dodaj",
            "Usuń",
            "Aktualizuj",
        )

        purchase_details_area.button_display(
            text=button_names[0], row=4, column=0, command=button_clear
        )
        purchase_details_area.button_display(
            text=button_names[1], row=4, column=1, command=button_selected
        )
        purchase_details_area.button_display(
            text=button_names[2], row=4, column=2, command=button_change
        )
        purchase_details_area.button_display(
            text=button_names[3], row=4, column=3, command=button_add
        )
        purchase_details_area.button_display(
            text=button_names[4], row=4, column=4, command=button_delete
        )
        purchase_details_area.button_display(
            text=button_names[5], row=4, column=5, command=button_update_wallet
        )

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
            purchase_details_area.objList[3], purchase_details_data.file_list, "txt"
        )

        purchase_details_area.add_data_in_treeview(
            purchase_details_area.objList[15], calculate_unit_price()
        )

    # unit price column and data
