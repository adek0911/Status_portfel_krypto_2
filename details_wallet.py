import tkinter.messagebox as msgbox
from datetime import datetime
from Classes import AreaFrame, ReadFile
import ttkbootstrap as ttk


def button_change_state(button: ttk.Button, window: ttk.Toplevel):
    button.configure(state="normal")
    window.destroy()


def update_filtr(value: int, data_list: list):
    result = []
    for i in range(len(data_list)):
        if value == 0:
            result.append(data_list[i][value][6:])
        else:
            result.append(data_list[i][value])
    result = list(set(result))
    result.insert(0, "Wszystko")
    return result


def button_clear(entry_obj_list: list):
    for i in range(4, 9):
        entry_obj_list[i].delete(0, "end")


def calculate_unit_price(file_data: list) -> list:
    # Zastanowić się czy nie lepiej żeby zwracał listę/tuple jako odpowiedź
    result_list = []
    unique_name = []

    for crypto in file_data:
        if not crypto[1] in unique_name and crypto[2] == "Kupno":
            unique_name.append(crypto[1])
            result_list.append([])
            result_list[unique_name.index(crypto[1])].extend(
                [crypto[3], crypto[4], crypto[5]]
            )
        elif crypto[2] == "Kupno":
            for i in range(3):
                result_list[unique_name.index(crypto[1])][i] += crypto[i + 3].__round__(
                    5
                )
        elif crypto[2] == "Sprzedaz":
            for i in range(3):
                result_list[unique_name.index(crypto[1])][i] -= crypto[i + 3].__round__(
                    5
                )

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


# create v2 beather
def sort_treeView(
    combobox_obj_dict: dict, treeview_data: list, area_frame: AreaFrame
) -> None:
    result = []
    data: str = combobox_obj_dict["Data_filtr"].get()
    name: str = combobox_obj_dict["Name_filtr"].get()
    status: str = combobox_obj_dict["Status_filtr"].get()

    status_combo = [data, name, status]
    count_stat = status_combo.count("Wszystko")

    if count_stat == 2:  # 1 filtr
        for i, value in enumerate(status_combo):
            if value != "Wszystko":
                if i == 0:
                    for j in treeview_data:
                        if j[0][6:] == value:
                            result.append(j)
                else:
                    for j in treeview_data:
                        if j[i] == value:
                            result.append(j)

    elif count_stat == 1:  # 2 filtry
        if status_combo[0] != "Wszystko" and status_combo[1] != "Wszystko":
            for i in treeview_data:
                if i[0][6:] == data and i[1] == name:
                    result.append(i)
        if status_combo[1] != "Wszystko" and status_combo[2] != "Wszystko":
            for i in treeview_data:
                if i[1] == name and i[2] == status:
                    result.append(i)
        if status_combo[0] != "Wszystko" and status_combo[2] != "Wszystko":
            for i in treeview_data:
                if i[0][6:] == data and i[2] == status:
                    result.append(i)
    elif count_stat == 0:  # 3 filtry
        for i in treeview_data:
            if i[0][6:] == data and i[1] == name and i[2] == status:
                result.append(i)
    else:
        result = treeview_data

    area_frame.add_data_in_treeview(area_frame.objList[3], result)


def button_selected(obj_list: list, dic_obj: ttk.Combobox):
    button_clear(obj_list)
    selected: list = obj_list[3].item(obj_list[3].selection())["values"]
    # pop status because its combobox obj and its set below
    status = selected.pop(2)

    # insert data to entry
    for i in range(4, 9):
        obj_list[i].insert(0, str(selected[i - 4]))
    dic_obj.set(status)


def purchers_area_ingredients(choice_wallet: str, button_obj: ttk.Button) -> None:
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

    try:
        purchase_details_data = ReadFile(
            f"Dane\Details_wallet_{choice_wallet}.txt", "txt"
        )

    except FileNotFoundError:
        msgbox.showinfo("Informacja", "Niestety nie ma szczegółów tego portfela.")
    else:
        button_obj.configure(state="disable")
        purchase_details_window = ttk.Toplevel()
        purchase_details_window.style.configure(
            "primary.Treeview", rowheight=22, borderwidth=0
        )
        purchase_details_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: button_change_state(button_obj, purchase_details_window),
        )
        purchase_details_area = AreaFrame(onFrame=purchase_details_window)
        status_transaction = ("Kupno", "Sprzedaz")
        purchase_details_area.text_display(
            text="Data", row=0, column=0, columnspan=2
        )  # obj_0
        purchase_details_area.text_display(
            text="Nazwa", row=0, column=2, columnspan=2
        )  # obj_1
        purchase_details_area.text_display(
            text="Sprzedaż/Kupno", row=0, column=4, columnspan=2
        )  # obj_2

        filter_type = {"Data_filtr": 0, "Name_filtr": 1, "Status_filtr": 2}
        column_change = 0
        for key in filter_type:
            purchase_details_area.combobox_display(
                values=update_filtr(filter_type[key], purchase_details_data.file_data),
                width=10,
                row=1,
                column=column_change,  # 0,2,4
                columnspan=2,
                name=key,
            )
            column_change += 2
            purchase_details_area.dict_combo[key].bind(
                "<<ComboboxSelected>>",
                lambda _: sort_treeView(
                    purchase_details_area.dict_combo,
                    purchase_details_data.file_list,
                    purchase_details_area,
                ),
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
        )  # obj_3
        # add data from file , create new instant and download data

        # 6 entry
        for i in range(6):  # obj_4-8
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
            text=button_names[0],
            row=4,
            column=0,
            command=lambda: button_clear(purchase_details_area.objList),
        )
        purchase_details_area.button_display(
            text=button_names[1],
            row=4,
            column=1,
            command=lambda: button_selected(
                purchase_details_area.objList,
                purchase_details_area.dict_combo["combo_status_transaction"],
            ),
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
        unit_price_column = ["Nazwa", "Cena jedn. zł", "Cena jedn. $", "Ilość"]
        purchase_details_area.treeview_display(
            columns=tuple(unit_price_column),
            headings_text=unit_price_column,
            row=5,
            column=0,
            columnspan=6,
        )

        purchase_details_area.add_data_in_treeview(
            purchase_details_area.objList[3], purchase_details_data.file_list, "txt"
        )

        purchase_details_area.add_data_in_treeview(
            purchase_details_area.objList[15],
            calculate_unit_price(purchase_details_data.file_data),
        )

    # unit price column and data
