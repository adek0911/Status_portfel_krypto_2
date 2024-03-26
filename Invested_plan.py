# import tkinter.messagebox as msgbox
from Classes import AreaFrame
import ttkbootstrap as ttk
import tkinter.messagebox as msgbox


# wallet values price in pln and dollar save in to file maybe in wallet


def invested_area_ingredients(
    area_dict: dict[AreaFrame],
    variable_json_File: dict,
    dollar_price: dict,
    core: ttk.Frame,
    button_status: dict,
):
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
        children_index = area_dict["charts_area"].objList[1].get_children()[combo_index]

        quantity = (
            float(value[0])
            / float(
                area_dict["charts_area"].objList[1].item(children_index)["values"][0]
            )
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
            area_dict["middle_area"].add_data_in_treeview(
                area_dict["middle_area"].objList[0],
                variable_json_File.file_dict["wallet_data"],
                "txt",
            )
            super.button_refresh_prices(area_dict, variable_json_File)
        else:
            msgbox.showwarning("Error", "Uzupełnij kolumnę z ceną")

    """Poniżej tabela z zaprezentowanymi zmianami, przycisk czyszczący predykcje oraz przycisk zapisujący w pliku"""
    if button_status["button_pred_state"] == 0:
        area_dict["buttons_area"].objList[2].configure(
            style="Invest.TButton"
        )  # RED button
        button_status["button_pred_state"] = 1

        button_status["chart_grid"] = area_dict["charts_area"].frame.grid_size()
        area_dict["charts_area"].frame.grid_forget()
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
            columns=tuple(headings),
            headings_text=headings,
            row=3,
            column=0,
            columnspan=4,
        )
        invested_area.objList[8].configure(height=7)
        button_status["invest_area"] = invested_area

    else:
        area_dict["buttons_area"].objList[2].configure(style="primary.TButton")
        button_status["button_pred_state"] = 0
        button_status["invest_area"].frame.grid_forget()
        area_dict["charts_area"].frame.grid(
            column=0,
            row=button_status["chart_grid"][1],
        )
