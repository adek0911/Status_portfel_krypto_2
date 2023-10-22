from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap import Frame, Canvas
from dateutil.relativedelta import relativedelta

from datetime import datetime
import tkinter.messagebox as msgbox
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv


def chart_area_result(area_frame_obj, krypto_list: list, variable_json: object):
    today = datetime.today().strftime("%Y-%m-%d")

    def load_chart_data(krypto_list: list):  # , crypto_date: str
        # stworzyć metodę sprawdzającą

        if variable_json.file_dict["variable_json"]["Charts_data"] != today:
            for i in krypto_list:
                url = requests.get(
                    f"https://www.cryptodatadownload.com/cdd/Binance_{i}USDT_d.csv"
                )
                if url.status_code == 200:
                    result = url.text.split("\n", 100)
                    del result[:2]
                    result = result[:100]
                    for index, _ in enumerate(result):
                        result[index] = result[index].split(",")
                        del result[index][0], result[index][2:5], result[index][3:]
                        result[index][0:1] = result[index][0].split(" ")

                    with open(
                        f"Chart_file\\{i}_chartdata.csv",
                        "w",
                        encoding="UTF-8",
                        newline="",
                    ) as d_wykres:
                        writer = csv.writer(d_wykres)
                        writer.writerows(result)
                if url.status_code != 200:
                    # make some tests
                    msgbox.showerror(
                        title="Brak danych",
                        message=f"Niestety nie udało się pobrać danych dla {i}",
                    )
            with open("App_file\zmienne.json", "r+") as file:
                read_json = json.load(file)
                read_json["Charts_data"] = today
                variable_json.file_dict["variable_json"]["Charts_data"] = today
                file.seek(0, 0)
                json.dump(read_json, file, ensure_ascii=False, indent=4)

    plt.style.use("seaborn-v0_8-darkgrid")
    scroll_frame = ScrolledFrame(
        area_frame_obj.frame, autohide=True, width=410, height=260
    )  # 410
    scroll_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    frame_wykresy = Frame(area_frame_obj.frame)
    frame_wykresy.grid(row=1, column=0, columnspan=2, pady=10)
    canvas = Canvas(scroll_frame)

    now = datetime.today() + relativedelta(days=-1)  # from datetime to str
    data_range = (
        (now + relativedelta(weeks=-2)).strftime("%Y-%m-%d"),
        (now + relativedelta(months=-1)).strftime("%Y-%m-%d"),
        (now + relativedelta(months=-3)).strftime("%Y-%m-%d"),
        now.strftime("%Y-%m-%d"),
    )

    def selected_combobox(event):
        load_chart_data(krypto_list)
        choice = area_frame_obj.dict_combo["available_crypto"].get()
        try:
            with open(
                f"Chart_file\\{choice}_chartdata.csv", "r", encoding="UTF-8"
            ) as file:
                d_data = file.read().split("\n")
                del d_data[-1]  # data
                for i in range((len(d_data))):
                    d_data[i] = d_data[i].split(",")
            chart_frame = Frame(canvas)
            canvas.create_window((0, 0), window=chart_frame, anchor="nw")
            canvas.pack(side="left")

            def add_to_chart_lists():
                tmp = i[0][5:]
                tmp = tmp[3] + tmp[4] + tmp[2] + tmp[0] + tmp[1]
                chart_list[0].append(tmp)
                chart_list[1].append(float(i[2]))

            for j in range(3):
                # chart on resolution of laptop ?check scaling %
                # wykres = plt.Figure(
                #     figsize=(3.2, 0.5), dpi=100, facecolor=(0.18, 0.31, 0.31)
                # )
                # chart on resolution of PC ? check scaling  form pix to %
                wykres = plt.Figure(
                    figsize=(4.2, 1.6),
                    dpi=100,
                    facecolor=("#375a7f"),  # (0.18, 0.31, 0.31)
                )
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

                    # before laptop
                    # ax1.set_title(
                    #     text, color="white", loc="left", x=-0.13, fontsize=11
                    # )
                    ax1.set_title(text, color="white", loc="left", x=-0.13, fontsize=12)
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
            scroll_frame.yview_moveto(0)
        # Nie było jeszcze sprawdzane
        except FileNotFoundError:
            msgbox.INFO("Nie ma pliku o takiej nazwie")
            # print("Nie ma pliku o takiej nazwie")

        chart_frame.grid(row=0, column=0)

    area_frame_obj.dict_combo["available_crypto"].current(0)
    area_frame_obj.dict_combo["available_crypto"].bind(
        "<<ComboboxSelected>>", selected_combobox
    )
    selected_combobox(None)
