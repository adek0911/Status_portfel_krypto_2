import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import json

app = ttk.Window(themename="darkly")

app.style.configure(
    ".",
    font=("Helvetica", 12),
    highlightbackground=0,
    buttonuprelief="",
)
# Login window for choice wallet

core = ttk.Frame(app, height=100, width=100)
core.grid()
credentials = {"Admin": "123"}
wallet_path = {}


def test_value():
    login = entry.get()
    if login in credentials:
        password = entry1.get()
        if password == credentials[login]:
            print("Brawo udało się zalogować")
        else:
            print("Błędne hasło")
    else:
        print("Nie udało się zalogować")
    entry1.delete(0, END)


label = ttk.Label(
    core, text="Podaj login i hasło do portfela", style="Label", font=("Helvetica", 12)
)
label.grid(row=0, column=0, columnspan=2, padx=15, pady=5)

label1 = ttk.Label(core, text="Login: ", font=("Helvetica", 12))
label1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry = ttk.Entry(core, style="primary", width=15, justify="center")
entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
label2 = ttk.Label(core, text="Hasło: ", font=("Helvetica", 12))
label2.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry1 = ttk.Entry(core, style="primary", width=15, justify="center", show="*")

entry.insert(0, "Admin")  # Only for tests
entry1.insert(0, "123")  # Only for tests
# entry1.configure(show="") If i wont to see password
entry1.grid(row=2, column=1, padx=5, pady=5, sticky="w")
button = ttk.Button(
    core, text="Zatwierdź", bootstyle="primary", width=10, command=test_value
)
button.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
core.wait_window()


app.mainloop()
