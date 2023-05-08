import json
import tkinter as tk
from tkinter import ttk
from tkinter import ttk
from ttkbootstrap import Style


class AreaFrame:

    def __init__(self, height=0, width=0, onFrame=tk.Frame, color='#009999') -> None:
        style = Style('flatly')
        style.configure('primary.Treeview.Heading', font=('Helvetica', 12))
        style.configure('core.TLabel', background='#009999',
                        foreground='white')
        style.configure('primary.TEntry', bordercolor='gray')
        style.configure('primary.TButton', font=('Helvetica', 11))

        self.objList = []
        self.height = height
        self.width = width
        self.frame = tk.Frame(onFrame, width=self.width, height=self.height)
        self.frame.configure(bg=color)
        self.frame.grid()

    def __str__(self) -> str:
        return 'Aktualnie jesteś w ramce głownej'

    def text_display(self, text: str, row: int, column: int, rowspan=None, columnspan=None):
        label = ttk.Label(self.frame, text=text,
                          style='core.TLabel', font=('Helvetica', 12))
        label.grid(row=row, column=column, rowspan=rowspan,
                   columnspan=columnspan, padx=5, pady=5)
        self.objList.append(label)

    def treeview_display(
            self,
            columns: tuple,
            row: int,
            column: int,
            rowspan: int = None,
            columnspan: int = None,
            headings_text: list = [],
            # method: function = ''
    ):
        treeview = ttk.Treeview(self.frame, style='primary.Treeview')
        self.objList.append(treeview)

        treeview['columns'] = columns
        treeview.configure(show='headings', selectmode='browse')
        # treeview.bind('<<TreeviewSelect>>', method)
        treeview.grid(row=row, column=column, rowspan=rowspan,
                      columnspan=columnspan, padx=5, pady=5)

        for i in range(len(headings_text)):
            headings_text[i] = headings_text[i].replace(' ', '\n ', 1)

        treeview.heading('#0', text='\n')
        for i in range(len(columns)):
            treeview.column(columns[i], width=90, anchor='center')
            treeview.heading(columns[i], text=headings_text[i])

    def add_data_in_treeview(self, objkey: ttk.Treeview, dataObj, type: str = ''):
        '''Clear treeview, insert data in treeview'''
        for i in objkey.get_children():
            objkey.delete(i)

        '''Check for empty value in file'''
        if type == 'txt':
            for i in range(len(dataObj)):
                dataObj[i] = dataObj[i].split(',')
        '''Insert data in treeview'''

        for i in range(len(dataObj)):
            objkey.insert('', index=i, values=dataObj[i])

    def treeview_Select(self, treeview1: ttk.Treeview, treeview2: ttk.Treeview, choice: int):
        focus1 = treeview1.focus()
        focus2 = treeview2.focus()

        getSelected1 = treeview1.get_children()
        getSelected2 = treeview2.get_children()

        if choice == 1:
            index1 = getSelected1.index(focus1)

            if focus2 == '':
                index2 = index1
                index2Selection = getSelected2[index1]
                treeview1.selection_set(index2Selection)
                treeview2.focus(index2Selection)
            else:
                index2 = getSelected2.index(focus2)

        pass

    def button_display(self, text: str, row: int, column: int, rowspan=None, columnspan=None, method=None):
        button = ttk.Button(
            self.frame, text=text, style='primary.TButton', command=method)
        button.grid(row=row, column=column, rowspan=rowspan,
                    columnspan=columnspan, padx=5, pady=5)
        self.objList.append(button)

    @staticmethod
    def choice_portfel(objkey: ttk.Treeview, objkey2: ttk.Treeview):
        get_children1 = objkey.get_children()
        index_1 = get_children1.index(objkey.focus())
        if objkey2.focus() == '':
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


class ReadData:
    '''Create list with file objects'''

    def __init__(self) -> None:
        self.file_list = []

    def read_from_file(self, variableFilePath: str, typefile: str):
        '''Give path to file and file extension'''
        if typefile == 'json':
            with (open(variableFilePath, 'r'))as file:
                jsonFile = json.load(file)
                self.file_list.append(jsonFile)

        elif typefile == 'txt' or typefile == 'csv':
            with open(variableFilePath, 'r') as file:
                flatFile = file.read().splitlines()
                self.file_list.append(flatFile)
            # return self.flatFile

    # def __getitem__(self, key):
    #     return self.walet_data[key]

    # def __len__(self):
    #     return len(self.walet_data)
