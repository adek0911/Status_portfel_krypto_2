import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import json

# app = ttk.Window(themename="darkly")


# scroll_frame = ScrolledFrame(app, autohide=True, width=400, height=400)  # , height=100)

# # sf.yview_moveto(1000)
# # sf.yview_scroll(0.2, "units")
# scroll_frame.grid()  # .pack(fill=BOTH, expand=YES)  # , padx=10, pady=10)

# # add a large number of checkbuttons into the scrolled frame
# canvas = ttk.Canvas(scroll_frame)
# test_frame = ttk.Frame(canvas)


# canvas.create_window((0, 0), window=test_frame, anchor="nw")
# canvas.pack(side="left")
# plt.style.use("seaborn-v0_8-darkgrid")
# for i in range(3):
#     wykres = plt.Figure(
#         figsize=(4.2, 1.9), dpi=100, facecolor=(0.18, 0.31, 0.31)
#     )  # facecolor=(0.18, 0.31, 0.31))
#     ax1 = wykres.add_subplot(111)
#     ax1.set_facecolor("darkgrey")
#     ax1.tick_params(labelcolor="White")
#     ax1.plot([0, 1, 2, 3, 4, 5], [2, 4, 6, 8, 10, 12])
#     ax1.set_title(f"Przejście pętli {i}", color="white")
#     line = FigureCanvasTkAgg(wykres, test_frame)
#     line.get_tk_widget().grid(row=i, ipady=45)
# test_frame.grid()
# app.mainloop()
# with open("App_file\zmienne.json", "r+") as file:
#     jsonFile = json.load(file)
#     if not "ARI10" in jsonFile["Charts_no_krypto_data"]:
#         jsonFile["Charts_no_krypto_data"].append("ARI10")
#     file.seek(0, 0)
#     json.dump(jsonFile, file, ensure_ascii=False, indent=4)
