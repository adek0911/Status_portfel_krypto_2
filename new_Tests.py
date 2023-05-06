
# from currency_converter import CurrencyConverter
# from datetime import date
# c = CurrencyConverter().convert(1,'USD','PLN')
# b=CurrencyConverter._get_rate('USD',date=date.today())

# print(c)
# print(b)

# from tkinter import *
# import sys

# class popupWindow(object):
#     def __init__(self,master):
#         top=self.top=Toplevel(master)
#         self.l=Label(top,text="Hello World")
#         self.l.pack()
#         self.e=Entry(top)
#         self.e.pack()
#         self.b=Button(top,text='Ok',command=self.cleanup)
#         self.b.pack()
#     def cleanup(self):
#         self.value=self.e.get()
#         self.top.destroy()

# class mainWindow(object):
#     def __init__(self,master):
#         self.master=master
#         self.b=Button(master,text="click me!",command=self.popup)
#         self.b.pack()
#         # self.b2=Button(master,text="print value",command=lambda: sys.stdout.write(self.entryValue()+'\n'))
#         self.b2=Button(master,text="print value",command=lambda: print(self.entryValue()))
#         self.b2.pack()

#     def popup(self):
#         self.w=popupWindow(self.master)
#         self.b["state"] = "disabled"
#         self.b2["state"] = "disabled" 
#         self.master.wait_window(self.w.top)
#         self.b["state"] = "normal"
#         self.b2["state"] = "normal"


#     def entryValue(self):
#         return self.w.value


# if __name__ == "__main__":
#     root=Tk()
#     m=mainWindow(root)
#     root.mainloop()

#Przykład connection ERROR 

# from requests.exceptions import ConnectionError
# try:
#    r = requests.get("http://example.com", timeout=0.001)
# except ConnectionError as e:    # This is the correct syntax
#    print e
#    r = "No response"

import json
  
zmienne_file=json.load(open('App_file\zmienne.json'))

# print(zmienne_file['connect_file'])
# print(zmienne_file['connect_file'])
# print(zmienne_file['connect_file'])
with(open('App_file\zmienne.json','r'))as dane:
    zmienne_file2=json.load(dane)

a=str(zmienne_file['Sciezka_portfel'])
i=5
a=a.replace('{i}',f'{i}')

print(a)
print(zmienne_file2['Sciezka_portfel'])