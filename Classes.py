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
        self.height = height
        self.width = width
        self.frame = ttk.Frame(onFrame, width=self.width, height=self.height)
        # self.frame.configure(bg=color)
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
        **kwargs,
    ):
        label = ttk.Label(
            self.frame, text=text, style=style
        )  # , font=("Helvetica", 12)
        label.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            pady=5,
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
        treeview = ttk.Treeview(self.frame, bootstyle="primary")

        treeview["columns"] = columns
        treeview.configure(show="headings", selectmode="browse")

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
        treeview.heading("#0", text="\n")

        self.objList.append(treeview)

    def add_data_in_treeview(self, objkey: ttk.Treeview, dataObj, type: str = ""):
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
        index_1 = get_children1.index(objkey.focus())
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

    # def __getitem__(self, key):
    #     return self.treeview[key]
    def combobox_display(
        self, values: list, width: int, row: int, column: int, **kwargs
    ):
        combobox = ttk.Combobox(
            self.frame,
            values=values,
            bootstyle="primary",
            state="readonly",
            width=width,
        )
        combobox.grid(row=row, column=column, **kwargs)
        combobox.current(0)
        self.objList.append(combobox)

    # Przerobić na statyczną metode
    def chart(self, krypto_list: list):
        def update_charts_data(krypto_list):
            with open("App_file\zmienne.json", "r+") as file:
                jsonFile = json.load(file)
                if jsonFile["Charts_data"] != today:
                    for i in krypto_list:
                        # krypto_list = ["ADA", "LTC", "DOGE", "XRP", "BCH", "BTC", "LRC", "ETH", "ARI10"]
                        url = requests.get(
                            f"https://www.cryptodatadownload.com/cdd/Binance_{i}USDT_d.csv"
                        )
                        if url.status_code == 200:
                            result = url.text.split("\n", 100)
                            # print(result[0:2])#'Unix,Date,Symbol,Open,High,Low,Close,Volume BTC,Volume USDT,tradecount'
                            del result[:2]
                            result = result[:100]
                            for j in range(len(result)):
                                result[j] = result[j].split(",")
                                del result[j][0], result[j][2:5], result[j][3:]
                                result[j][0:1] = result[j][0].split(" ")

                            with open(
                                f"Chart_file\\{i}_chartdata.csv",
                                "w",
                                encoding="UTF-8",
                                newline="",
                            ) as d_wykres:
                                writer = csv.writer(d_wykres)
                                writer.writerows(result)
                        if url.status_code != 200:
                            if not i in jsonFile["Charts_no_krypto_data"]:
                                jsonFile["Charts_no_krypto_data"].append(i)
                    jsonFile["Charts_data"] = today
                    file.seek(0, 0)
                    json.dump(jsonFile, file, ensure_ascii=False, indent=4)

        plt.style.use("seaborn-v0_8-darkgrid")
        scroll_frame = ScrolledFrame(
            self.frame, autohide=True, width=410, height=260
        )  # 410
        scroll_frame.grid(row=1, column=0, columnspan=2)

        frame_wykresy = ttk.Frame(self.frame)
        frame_wykresy.grid(row=1, column=0, columnspan=2, pady=10)
        canvas = ttk.Canvas(scroll_frame)

        today = datetime.today().strftime("%Y-%m-%d")
        now = datetime.today() + relativedelta(days=-1)  # from datetime to str
        data_range = (
            (now + relativedelta(weeks=-2)).strftime("%Y-%m-%d"),
            (now + relativedelta(months=-1)).strftime("%Y-%m-%d"),
            (now + relativedelta(months=-3)).strftime("%Y-%m-%d"),
            now.strftime("%Y-%m-%d"),
        )

        def selected_combobox(event):
            update_charts_data(krypto_list)
            choice = self.objList[1].get()
            try:
                with open(
                    f"Chart_file\\{choice}_chartdata.csv", "r", encoding="UTF-8"
                ) as file:
                    d_data = file.read().split("\n")
                    del d_data[-1]  # data
                    for i in range((len(d_data))):
                        d_data[i] = d_data[i].split(",")
                chart_frame = ttk.Frame(canvas)
                canvas.create_window((0, 0), window=chart_frame, anchor="nw")
                canvas.pack(side="left")

                def add_to_chart_lists():
                    tmp = i[0][5:]
                    tmp = tmp[3] + tmp[4] + tmp[2] + tmp[0] + tmp[1]

                    chart_list[0].append(tmp)
                    chart_list[1].append(float(i[2]))
                    pass

                for j in range(3):
                    wykres = plt.Figure(
                        figsize=(3.2, 0.5), dpi=100, facecolor=(0.18, 0.31, 0.31)
                    )  # figsize=(4.2, 1.6),
                    chart_list = [[], []]
                    for i in d_data:
                        if j == 0 and i[0] > data_range[0]:
                            add_to_chart_lists()
                        if j == 1 and i[0] > data_range[1]:
                            add_to_chart_lists()
                        if j == 2 and i[0] > data_range[2]:
                            add_to_chart_lists()

                    chart_list[0].reverse()
                    chart_list[1].reverse()

                    def mean():
                        result = sum(chart_list[1]) / len(chart_list[1])
                        return result.__round__(3)

                    ax1 = wykres.add_subplot(111)
                    ax1.set_facecolor("grey")
                    ax1.tick_params(labelcolor="White")
                    ax1.grid(axis="both", color="darkgrey")
                    ax1.plot(chart_list[0], chart_list[1])  # x, y

                    def conf_plot(j, text):
                        ax1.set_xticks(chart_list[0][::j])
                        # ax1.set_title(text, color="white", loc="left")
                        ax1.set_title(
                            text, color="white", loc="left", x=-0.13, fontsize=11
                        )
                        ax1.hlines(
                            mean(),
                            0,
                            len(chart_list[0]),
                            colors="r",
                            label=f"Średnia {str(mean())}$",
                        )
                        ax1.set_xlim(chart_list[0][0], chart_list[0][-1])

                        ax1.plot(
                            chart_list[1].index(max(chart_list[1])),
                            max(chart_list[1]),
                            "o",
                            color="cyan",
                        )
                        ax1.plot(
                            chart_list[1].index(min(chart_list[1])),
                            min(chart_list[1]),
                            "o",
                        )
                        ax1.legend(labelcolor="white")

                    if j == 0:
                        conf_plot(
                            3,
                            f"Ostatnie 2 tyg. max: {max(chart_list[1])}, min: {min(chart_list[1])} ",
                        )
                    if j == 1:
                        conf_plot(
                            7,
                            f"Ostatni miesiąc max: {max(chart_list[1])}, min: {min(chart_list[1])}",
                        )
                    if j == 2:
                        conf_plot(
                            14,
                            f"Ost. 3 miesiące max: {max(chart_list[1])}, min: {min(chart_list[1])}",
                        )
                    line = FigureCanvasTkAgg(wykres, chart_frame)
                    line.get_tk_widget().grid(row=j, ipady=45)  # , ipady=45)
            # Nie było jeszcze sprawdzane
            except FileNotFoundError:
                msgbox.INFO("Nie ma pliku o takiej nazwie")
                print("Nie ma pliku o takiej nazwie")

            chart_frame.grid(row=0, column=0)

        self.objList[1].current(0)
        self.objList[1].bind("<<ComboboxSelected>>", selected_combobox)

        selected_combobox(None)

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

    def __init__(self) -> None:
        self.file_list = []
        self.result_values = {
            "Profit_zl": 0,
            "Profit_dollar": 0,
            "Profit_%": "",
            "Value_of_wallet": 0,
            "Invest_value": 0,
        }

    def read_from_file(self, variableFilePath: str, typefile: str):
        """Give path to file and file extension"""
        if typefile == "json":
            with open(variableFilePath, "r") as file:
                jsonFile = json.load(file)
                self.file_list.append(jsonFile)

        elif typefile == "txt" or typefile == "csv":
            with open(variableFilePath, "r") as file:
                flatFile = file.read().splitlines()
            for i in range(len(flatFile)):
                flatFile[i] = flatFile[i].split(",")
            self.file_list.append(flatFile)
            # return self.flatFile

    # def __getitem__(self, key):
    #     return self.walet_data[key]

    # def __len__(self):
    #     return len(self.walet_data)


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
        def file_data(self) -> list:
            return self.file_data
