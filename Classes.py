import json
import ttkbootstrap as ttk
from datetime import datetime
from dateutil.relativedelta import relativedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import requests
from ttkbootstrap.scrolled import ScrolledFrame
import csv
import tkinter.messagebox as msgbox

# import tkinter as tk
# from ttkbootstrap import Style


class AreaFrame:
    def __init__(self, height=100, width=100, onFrame=ttk.Frame, **kwargs) -> None:
        self.objList = []
        self.dict_combo = {}
        self.height = height
        self.width = width
        self.frame = ttk.Frame(onFrame, width=self.width, height=self.height)
        self.frame.grid(**kwargs)

    def __str__(self) -> str:
        return "Aktualnie jesteś w ramce głownej"

    def text_display(
        self,
        text: str,
        row: int,
        column: int,
        rowspan=None,
        columnspan=None,
        style="TLabel",
        pady=5,
        **kwargs,
    ):
        label = ttk.Label(self.frame, text=text, style=style)
        label.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            pady=pady,
            **kwargs,
        )
        self.objList.append(label)

    def treeview_display(
        self,
        columns: tuple,
        row: int,
        column: int,
        headings_text: list,
        rowspan: int = None,
        columnspan: int = None,
        width: int = 90,
    ):
        # treeview = ttk.Treeview(self.frame, bootstyle="primary")
        treeview = ttk.Treeview(self.frame, style="primary")
        treeview.heading("#0", text="\n")
        treeview["columns"] = columns
        treeview.configure(show="headings", selectmode="browse")
        # treeview.configure("Treeview.Heading", rowheight=20)
        treeview.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            padx=5,
            pady=5,
        )

        for i in range(len(headings_text)):
            headings_text[i] = headings_text[i].replace(" ", "\n ", 1)

        for i in range(len(columns)):
            treeview.column(columns[i], width=width, anchor="center")
            treeview.heading(columns[i], text=headings_text[i])
        # treeview.configure(hea)
        self.objList.append(treeview)

    def add_data_in_treeview(self, objkey: ttk.Treeview, dataObj: list, type: str = ""):
        """Clear treeview, insert data in treeview"""
        for i in objkey.get_children():
            objkey.delete(i)

        """Check for empty value in file"""
        if type == "txt":
            for i in range(len(dataObj)):
                for j in range(1, len(dataObj[i])):
                    try:
                        dataObj[i][j] = float(dataObj[i][j]).__round__(4)
                    except ValueError:
                        dataObj[i][j] = str(dataObj[i][j])
        """Insert data in treeview"""

        for i in range(len(dataObj)):
            objkey.insert("", index=i, values=dataObj[i])

    def treeview_Select(
        self, treeview1: ttk.Treeview, treeview2: ttk.Treeview, choice: int
    ):
        focus1 = treeview1.focus()
        focus2 = treeview2.focus()

        getSelected1 = treeview1.get_children()
        getSelected2 = treeview2.get_children()

        if choice == 1:
            index1 = getSelected1.index(focus1)

            if focus2 == "":
                index2 = index1
                index2Selection = getSelected2[index1]
                treeview1.selection_set(index2Selection)
                treeview2.focus(index2Selection)
            else:
                index2 = getSelected2.index(focus2)

        pass

    def button_display(
        self,
        text: str,
        row: int,
        column: int,
        rowspan=None,
        columnspan=None,
        command=None,
        width=8,
        **kwargs,
    ):
        button = ttk.Button(
            self.frame, text=text, bootstyle="primary", command=command, width=width
        )
        button.grid(
            row=row, column=column, rowspan=rowspan, columnspan=columnspan, **kwargs
        )
        self.objList.append(button)

    @staticmethod
    def choice_portfel(objkey: ttk.Treeview, objkey2: ttk.Treeview):
        get_children1 = objkey.get_children()
        status = True
        try:
            index_1 = get_children1.index(objkey.focus())
        except ValueError:
            status = False
        if status:
            if objkey2.focus() == "":
                index_2 = index_1
                focus_selection = objkey2.get_children()[index_1]
                objkey2.selection_set(focus_selection)
                objkey2.focus(focus_selection)
            else:
                index_2 = objkey2.get_children().index(objkey2.focus())

            if index_1 != index_2:
                focus_selection = objkey2.get_children()[index_1]
                objkey2.selection_set(focus_selection)
                objkey2.focus(focus_selection)

    def combobox_display(
        self,
        values: list,
        width: int,
        row: int,
        column: int,
        name: str,
        justyfy="left",
        **kwargs,
    ):
        combobox = ttk.Combobox(
            self.frame,
            values=values,
            bootstyle="primary",
            state="readonly",
            width=width,
            justify=justyfy,
        )
        combobox.grid(row=row, column=column, **kwargs)
        combobox.current(0)

        self.dict_combo[f"{name}"] = combobox

    def entry_display(
        self,
        row,
        column,
        state="normal",
        result_value: float = 0,
        justify="left",
        width=10,
        index: int = 0,
        text: str = "",
        insert: bool = False,
    ):
        entry = ttk.Entry(self.frame, style="primary", width=width, justify=justify)
        # if result_value < 0:
        #     entry.configure(style="negative.primary.TEntry")
        #     pass
        if insert == True:
            entry.insert(index, f"{str(result_value)} {text}")
        entry["state"] = state
        entry.grid(row=row, column=column, padx=5, pady=5)
        self.objList.append(entry)


class TopFrame:
    def __init__(self, **kwargs) -> None:
        self.frame = ttk.Toplevel(resizable=(False, False))
        self.frame.grid(**kwargs)


class ReadData:
    """Create list with file objects"""

    # brak potrzeby tworzenia specialnie słownika z plikami lepiej tworzyć osobne obiekty dla każdego osobnego pliku
    def __init__(self) -> None:
        self.file_dict = {}
        self.result_values = {
            "Profit_zl": 0,
            "Profit_dollar": 0,
            "Profit_%": "",
            "Value_of_wallet": 0,
            "Invest_value": 0,
        }

    def read_from_file(self, variableFilePath: str, typefile: str, data_name: str):
        """Give path to file and file extension"""
        if typefile == "json":
            with open(variableFilePath, "r") as file:
                jsonFile = json.load(file)
                self.file_dict[f"{data_name}"] = jsonFile

        if typefile == "txt" or typefile == "csv":
            with open(variableFilePath, "r") as file:
                flatFile = file.read().splitlines()
            for i in range(len(flatFile)):
                flatFile[i] = flatFile[i].split(",")
            self.file_dict[f"{data_name}"] = flatFile


class ReadFile:
    def __init__(self, path, type_file):
        if type_file == "txt":
            with open(path, "r", encoding="utf-8", newline="") as File:
                data = File.read().splitlines()
            for i in range(len(data)):
                data[i] = data[i].split(",")
        else:
            print("Nie posiadam takiego typu")

        self.file_data = data

    @property
    def file_list(self) -> list:
        return self.file_data
