from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap import Frame, Canvas
import tkinter.messagebox as msgbox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# now=datetime.now().strftime("%d/%m/%Y")

"""available coins from CoinGecko"""
# https://api.coingecko.com/api/v3/coins/list?include_platform=false


def load_from_api(currency: str) -> list:
    url = requests.get(
        f"https://adix0911.eu.pythonanywhere.com/chart_currency/{currency}"
    )
    if url.status_code == 200:
        result = url.json()
        for j in result:
            result[j] = [
                i.replace("/", "-").replace("\n", "").split(";") for i in result[j]
            ]
        return result[f"{currency}"]
    else:
        print("Coś nie działa " + str(url.status_code))


def chart_area_result(area_frame_obj):
    """prepare data for charts"""
    # load_chart_data(krypto_list)

    def selected_combobox(event):
        choice: str = area_frame_obj.dict_combo["available_crypto"].get()
        chart_frame = Frame(canvas)
        canvas.create_window((0, 0), window=chart_frame, anchor="nw")
        canvas.pack(side="left")
        # file_data = load_from_file(choice)
        file_data = load_from_api(choice)
        result_x = [i[0][:5] for i in file_data]
        result_y = [float(i[1]) for i in file_data]

        for i in range(3):
            if i == 0:
                x_val = result_x[:14]
                y_val = result_y[:14]

            elif i == 1:
                x_val = result_x[:30]
                y_val = result_y[:30]
            else:
                x_val = result_x
                y_val = result_y

            x_val.reverse()
            y_val.reverse()
            # chart on resolution of laptop ?check scaling %
            # wykres = plt.Figure(figsize=(3.2, 0.5), dpi=100, facecolor=(0.18, 0.31, 0.31))
            # chart on resolution of PC ? check scaling  form pix to %
            wykres = plt.Figure(
                figsize=(4.2, 1.6), dpi=100, facecolor=("#375a7f")
            )  # (0.18, 0.31, 0.31)

            def mean():
                return round(sum(y_val) / len(y_val), 3)

            ax1 = wykres.add_subplot(111)
            ax1.set_facecolor("grey")
            ax1.tick_params(labelcolor="White")
            ax1.grid(axis="both", color="darkgrey")
            ax1.plot(x_val, y_val)  # x, y

            def conf_plot(i, text):
                ax1.set_xticks(x_val[::i])
                # ax1.set_title(text, color="white", loc="left")

                # before laptop
                # ax1.set_title(
                #     text, color="white", loc="left", x=-0.13, fontsize=11
                # )
                ax1.set_title(text, color="white", loc="left", x=-0.13, fontsize=12)
                ax1.hlines(
                    mean(),
                    0,
                    len(x_val),
                    colors="r",
                    label=f"Średnia {str(mean())}$",
                )
                ax1.set_xlim(x_val[0], x_val[-1])

                ax1.plot(
                    y_val.index(max(y_val)),
                    max(y_val),
                    "o",
                    color="cyan",
                )
                ax1.plot(
                    y_val.index(min(y_val)),
                    min(y_val),
                    "o",
                )
                ax1.legend(labelcolor="white")

            if i == 0:
                conf_plot(
                    3,
                    f"Ostatnie 2 tyg. max: {max(y_val)}, min: {min(y_val)} ",
                )
            if i == 1:
                conf_plot(
                    7,
                    f"Ostatni miesiąc max: {max(y_val)}, min: {min(y_val)}",
                )
            if i == 2:
                conf_plot(
                    14,
                    f"Ost. 3 miesiące max: {max(y_val)}, min: {min(y_val)}",
                )
            line = FigureCanvasTkAgg(wykres, chart_frame)
            line.get_tk_widget().grid(row=i, ipady=45)  # , ipady=45)
        scroll_frame.yview_moveto(0)
        chart_frame.grid(row=0, column=0)

    plt.style.use("seaborn-v0_8-darkgrid")
    scroll_frame = ScrolledFrame(
        area_frame_obj.frame, autohide=True, width=410, height=260
    )  # 410
    scroll_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    frame_wykresy = Frame(area_frame_obj.frame)
    frame_wykresy.grid(row=1, column=0, columnspan=2, pady=10)
    canvas = Canvas(scroll_frame)

    area_frame_obj.dict_combo["available_crypto"].current(0)
    area_frame_obj.dict_combo["available_crypto"].bind(
        "<<ComboboxSelected>>", selected_combobox
    )
    selected_combobox(None)
