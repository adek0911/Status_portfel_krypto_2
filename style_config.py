import ttkbootstrap as ttk


def style_conf(root: ttk.Window):
    """Set configuration for all elements in app"""
    # before
    # root.style.configure(".", bordercolor="", borderwidth=0, font=("Helvetica", 9))

    root.style.configure(".", bordercolor="", borderwidth=0, font=("Helvetica", 10))
    root.style.configure(
        "11_label.TLabel", bordercolor="", borderwidth=0, font=("Helvetica", 11)
    )
    root.style.configure("primary.Treeview", rowheight=22, borderwidth=0)
    root.style.configure("Treeview.Heading", font=("Helvetica", 11))

    root.style.configure("primary.TEntry", font=("Helvetica", 12))
    root.style.configure("primary.TButton", font=("Helvetica", 11), buttonuprelief="")
    # work but need to configure prop
    root.style.configure("Invest.TButton", font=("Helvetica", 11), background="Red")
    root.style.configure("12_label.TLabel", font=("Helvetica", 12))
