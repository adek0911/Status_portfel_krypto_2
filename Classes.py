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
            event=''
    ):
        treeview = ttk.Treeview(self.frame, style='primary.Treeview')
        self.objList.append(treeview)

        treeview['columns'] = columns
        treeview.configure(show='headings', selectmode='browse')
        treeview.bind('<<TreeviewSelect>>',)
        treeview.grid(row=row, column=column, rowspan=rowspan,
                      columnspan=columnspan, padx=5, pady=5)

        for i in range(len(headings_text)):
            headings_text[i] = headings_text[i].replace(' ', '\n ', 1)

        treeview.heading('#0', text='\n')
        for i in range(len(columns)):
            treeview.column(columns[i], width=90, anchor='center')
            treeview.heading(columns[i], text=headings_text[i])

    def add_data_in_treeview(self, objkey: ttk.Treeview, dataObj):
        '''Clear treeview, insert data in treeview'''
        for i in objkey.get_children():
            objkey.delete(i)

        '''Check for empty value in file'''

        for i in range(len(dataObj.flatFile)):
            dataObj.flatFile[i] = dataObj.flatFile[i].split(',')
            for y in range(1, 4):
                # if dataObj.flatFile[i][2] == '':
                #     dataObj.flatFile[i][2] = (
                #         dataObj.flatFile[i][2] / float(dataObj.jsonFile['Cena_Dolar']))

                if (dataObj.flatFile[i][y] == ''):
                    dataObj.flatFile[i][y] = float('nan')
                dataObj.flatFile[i][y] = float(dataObj.flatFile[i][y])

        '''Insert data in treeview'''

        for i in range(len(dataObj.flatFile)):
            objkey.insert('', index=i, values=dataObj.flatFile[i])

    def add_data_in_treeview_v2(self, objkey: ttk.Treeview, data: list,):  # Nie używana
        for i in objkey.get_children():
            objkey.delete(i)

        for i in range(len(data)):
            objkey.insert('', index=i, values=data[i])

    def treeviewSelect(self, treeview1: ttk.Treeview, treeview2: ttk.Treeview, choice: int):
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
        self.button = ttk.Button(
            self.frame, text=text, style='primary.TButton', command=method)
        self.button.grid(row=row, column=column, rowspan=rowspan,
                         columnspan=columnspan, padx=5, pady=5)

        pass

        '''Błąd potrzebuje pozyskać odpowiedni index treeview'''

    # def __getitem__(self, key):
    #     return self.treeview[key]


class Read_data:
    '''Ehh trzeba przerobić by działało na różnych rodzajach plików'''

    def __init__(self) -> None:
        # with open((str(variables_file)), 'r') as file:
        #     self.walet_data = file.read().splitlines()
        # def isNan(num):
        #     return num != num
        # for i in range(len(self.walet_data)):
        #     if (isNan(self.walet_data[i][1]) == True) or (self.walet_data[i][1] == ''):
        #         self.walet_data[i][1] = float(
        #             self.walet_data[i][2]*variables_file['Cena_Dolar']).__round__(2)

        #     if (isNan(self.walet_data[i][2]) == True) or (self.walet_data[i][2] == ''):
        #         self.walet_data[i][2] = float(
        #             self.walet_data[i][1]/variables_file['Cena_Dolar']).__round__(2)
        pass

    def read_from_file(self, variableFilePath: str, typefile: str):
        '''Coś mi tu nie pasuje chyba każda klasa będzie trzymać osobne dane
            Sometching in missing maybe every object has only one read file
        '''
        if typefile == 'json':
            with (open(variableFilePath, 'r'))as file:
                self.jsonFile = json.load(file)
            # return self.jsonFile

        elif typefile == 'txt' or typefile == 'csv':
            with open(variableFilePath, 'r') as file:
                self.flatFile = file.read().splitlines()
            # return self.flatFile

    # def __getitem__(self, key):
    #     return self.walet_data[key]

    # def __len__(self):
    #     return len(self.walet_data)
