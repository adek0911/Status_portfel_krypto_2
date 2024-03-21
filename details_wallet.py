import tkinter.messagebox as msgbox
from datetime import datetime
from Classes import AreaFrame, ReadFile, TopFrame
import ttkbootstrap as ttk
import requests


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


def cal_unit_prices(history_trans_data: list) -> list:
    result = [[]]
    for val in history_trans_data:
        if val[1] not in result[0]:
            result[0].append(val[1])
            result.append([val[1], 0, 0, 0])  # nazwa, cena jed. zł, cena jed. $, ilosc
        if val[2] == "BUY":
            result[result[0].index(val[1]) + 1][1] += val[3]
            result[result[0].index(val[1]) + 1][2] += val[4]
            result[result[0].index(val[1]) + 1][3] += val[5]
        if val[2] == "SALE":
            result[result[0].index(val[1]) + 1][1] -= val[3]
            result[result[0].index(val[1]) + 1][2] -= val[4]
            result[result[0].index(val[1]) + 1][3] -= val[5]
    result.pop(0)
    for i in result:
        i[3] = i[3].__round__(4)
        if i[3] != 0:
            i[1] = round(i[1] / i[3], 4)
            i[2] = round(i[2] / i[3], 4)
            i[3] = round(i[3], 4)
        else:
            result.pop(result.index(i))
    return result


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


def prep_data_from_db(data_db: list[dict]):
    result = []
    for val in data_db:
        temp = []
        temp.append(
            datetime.strptime(val["date_purchase"], "%Y-%m-%d").strftime("%d.%m.%Y")
        )
        temp.append(val["name_currency"])
        temp.append(
            val["status_of_purchase"].replace("}", "").replace("{", "").replace("'", "")
        )
        temp.append(f"{val['price_PLN']}")
        temp.append(f"{val['price_dollar']}")
        temp.append(f"{val['quantity']}")
        temp.append({"Id": val["Id"]})
        result.append(temp)

    return result


"""TEMP"""


def save_in_file(path: str, detail_wallet: list):
    prep_data = []
    for i, val in enumerate(detail_wallet):
        if i == len(detail_wallet) - 1:
            prep_data.append(",".join(val))
        else:
            prep_data.append(",".join(val) + "\n")
    with open(path, "w", encoding="UTF-8") as file:
        file.writelines(prep_data)


def button_update_wallet(treeview_values: list, db_data: list, url: str):
    # result = []
    # for i in purchase_details_area.objList[3].get_children():
    #     result.append(purchase_details_area.objList[3].item(i)["values"])

    # save_in_file(f"Dane\Details_wallet_{choice_wallet}.txt", result)
    """Add popup button for confirm"""

    """Check if in treeview is some changes:
    maybe check button press or just check for change"""
    treeview_values = [
        treeview_values.item(values)["values"]
        for values in treeview_values.get_children()
    ]  # [['04.01.2021', 'BCH', 'BUY', '10.0', '2.7', '0.00600648'], ['1...
    # print(db_data) [['04.01.2021', 'BCH', 'BUY', '10.0', '2.7', '0.00600648', {'Id': 1}], ['...
    # TODO 1 all below
    """If something is diffrent change this data add if is need to to database"""
    """Count if something is change value for wallet"""
    """Change wallet data in database """
    # in test file
    """Active refresh method on main window app to update data for this wallet"""
    pass


def purchers_area_ingredients(
    choice_wallet: str, button_obj: ttk.Button, url: str, selected_wallet_id: int
) -> None:

    def button_change():
        # Warning if wont change data
        change_data = []
        for i in range(4, 9):
            change_data.append(purchase_details_area.objList[i].get())
        change_data.insert(
            2, purchase_details_area.dict_combo["combo_status_transaction"].get()
        )
        purchase_details_area.objList[3].item(
            purchase_details_area.objList[3].selection(), values=change_data
        )

    def button_add():
        # create data control
        add_data = [purchase_details_area.objList[val].get() for val in range(4, 9)]
        add_data.insert(
            2, purchase_details_area.dict_combo["combo_status_transaction"].get()
        )
        # add_data ==['11.02.2021', 'BUY', 'Kupno', '10000.0', '2702.7', '1.4811']
        purchase_details_area.objList[3].insert("", "end", values=add_data)
        """Add data to file rebild for api and add in database"""
        # refresh treeview
        purchase_details_area.add_data_in_treeview(
            purchase_details_area.objList[15],
            cal_unit_prices(purchase_details_data.file_data),
        )

    def button_delete():
        """Add a popup window to confirm this delete"""
        # TODO popup window
        purchase_details_area.objList[3].delete(
            purchase_details_area.objList[3].selection()
        )

    """Local variables"""
    try:
        purchase_details_data = ReadFile(
            f"Dane\Details_wallet_{choice_wallet}.txt", "txt"
        )
        """Change to database data"""
        responce = requests.get(f"{url}trans_curr/{selected_wallet_id}").json()
        purchase_details_from_db_core = prep_data_from_db(responce)
        purchase_details_from_db = [val[:6] for val in purchase_details_from_db_core]
    except FileNotFoundError:
        msgbox.showinfo("Informacja", "Niestety nie ma szczegółów tego portfela.")

    button_obj.configure(state="disable")
    purchase_details_window = TopFrame()
    purchase_details_window.frame.style.configure(
        "primary.Treeview", rowheight=22, borderwidth=0
    )
    purchase_details_window.frame.protocol(
        "WM_DELETE_WINDOW",
        lambda: button_change_state(button_obj, purchase_details_window.frame),
    )
    purchase_details_area = AreaFrame(onFrame=purchase_details_window.frame)
    status_transaction = ("BUY", "SALE")
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
            values=update_filtr(filter_type[key], purchase_details_from_db),
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
                purchase_details_from_db[:6],
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

    # 5 entry
    for i in range(6):  # obj_4-8
        if i != 2:
            purchase_details_area.entry_display(row=3, column=i)
        else:
            """on index 2 is combobox"""
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
        text=button_names[5],
        row=4,
        column=5,
        command=lambda: button_update_wallet(
            treeview_values=purchase_details_area.objList[3],
            db_data=purchase_details_from_db_core,
            url=url,
        ),
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
        purchase_details_area.objList[3], purchase_details_from_db, "txt", 10
    )

    purchase_details_area.add_data_in_treeview(
        purchase_details_area.objList[15],
        cal_unit_prices(purchase_details_from_db),
    )

    # unit price column and data
