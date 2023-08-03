# # from currency_converter import CurrencyConverter
# # from datetime import date
# # c = CurrencyConverter().convert(1,'USD','PLN')
# # b=CurrencyConverter._get_rate('USD',date=date.today())

# # print(c)
# # print(b)

# # from tkinter import *
# # import sys

# # class popupWindow(object):
# #     def __init__(self,master):
# #         top=self.top=Toplevel(master)
# #         self.l=Label(top,text="Hello World")
# #         self.l.pack()
# #         self.e=Entry(top)
# #         self.e.pack()
# #         self.b=Button(top,text='Ok',command=self.cleanup)
# #         self.b.pack()
# #     def cleanup(self):
# #         self.value=self.e.get()
# #         self.top.destroy()

# # class mainWindow(object):
# #     def __init__(self,master):
# #         self.master=master
# #         self.b=Button(master,text="click me!",command=self.popup)
# #         self.b.pack()
# #         # self.b2=Button(master,text="print value",command=lambda: sys.stdout.write(self.entryValue()+'\n'))
# #         self.b2=Button(master,text="print value",command=lambda: print(self.entryValue()))
# #         self.b2.pack()

# #     def popup(self):
# #         self.w=popupWindow(self.master)
# #         self.b["state"] = "disabled"
# #         self.b2["state"] = "disabled"
# #         self.master.wait_window(self.w.top)
# #         self.b["state"] = "normal"
# #         self.b2["state"] = "normal"


# #     def entryValue(self):
# #         return self.w.value


# # if __name__ == "__main__":
# #     root=Tk()
# #     m=mainWindow(root)
# #     root.mainloop()

# # Przykład connection ERROR

# # from requests.exceptions import ConnectionError
# # try:
# #    r = requests.get("http://example.com", timeout=0.001)
# # except ConnectionError as e:    # This is the correct syntax
# #    print e
# #    r = "No response"


# # zmienne_file=json.load(open('App_file\zmienne.json'))

# # # print(zmienne_file['connect_file'])
# # # print(zmienne_file['connect_file'])
# # # print(zmienne_file['connect_file'])
# # with(open('App_file\zmienne.json','r'))as dane:
# #     zmienne_file2=json.load(dane)

# # a=str(zmienne_file['Sciezka_portfel'])
# # i=5
# # a=a.replace('{i}',f'{i}')

# # print(a)
# # print(zmienne_file2['Sciezka_portfel'])

# # import threading as th
# # import time
# # def dodanie(lista :list,poczatek:int,koniec:int):
# #     for i in range(poczatek,koniec,1):
# #         lista.append(i)

# # tm=[10,11,12,13,14,15,16,17,18,19]

# # def dod(lista:list):

# #     for i in lista:
# #         l1.append(i)

# #     time.sleep(1)

# # l1=[1,2,3,4,5,6,7,8,9,10] #source
# # # l1=[1,2,3,4,5,6,7,8,9,10,11] #source
# # # l1=[1,2,3,4,5,6,7,8,9] #source
# # l2=[]
# # l3=[]
# # l4=[]

# # len_l1=len(l1)
# # if (len_l1%3==0):
# #     len_l12=int((len_l1/3))
# #     len_l13=int((len_l1-len_l12))
# # if (len_l1%3==1):
# #     len_l12=int((len_l1/3)+1)
# #     len_l13=int((len_l1-len_l12)+1)
# # if (len_l1%3==2):
# #     len_l12=int((len_l1/3)+1)
# #     len_l13=int((len_l1-len_l12)+1)


# # print(len_l1)
# # print(len_l12)
# # print(len_l13)

# # temp_l1,temp_l2,temp_l3=[],[],[]

# # th.Thread(target=dodanie(temp_l1,0,len_l12))
# # th.Thread(target=dodanie(temp_l2,len_l12,len_l13))
# # th.Thread(target=dodanie(temp_l3,len_l13,len_l1))

# # print(temp_l1)
# # print(temp_l2)
# # print(temp_l3)

# # z=temp_l1+temp_l2+temp_l3
# # print(z)

# # th1.start()
# # th1.join()
# # th2.start()
# # th2.join()

# # th3=th.Thread(target=dodanie(l3,1,len_2_l1)).start()
# # th4=th.Thread(target=dodanie(l4,len_2_l1,len_l1)).start()

# # # th.Thread(target=dod(tm)).start()
# # z=l3+l4


# # # print(l2)
# # print(l3)
# # print(l4)
# # print(z)

# # with(open('App_file\zmienne.json','r', encoding='UTF-8'))as dane:
# #     zmienne_file=json.load(dane)

# # # print(zmienne_file)

# # a=zmienne_file['connect_file']['path_portfel']
# # print(a)


# # url = f"https://api.apilayer.com/currency_data/live?source={source}¤cies= PLN"
# # url = f"https://api.apilayer.com/currency_data/live?source=USD"
# # url = "https://api.apilayer.com/currency_data/live?source=USD&currencies=PLN"
# # headers= {"apikey": "o49OHWHzwbhE38MkfZZNDoOCV3bgOkBt"}
# # response = requests.request("GET", url, headers=headers)
# # status_code = response.status_code
# # result = json.loads(response.text)
# # print(result['quotes']['USDPLN'])

# # działa i pobiera odpowiednią cenę zapisać
# #  jeszcze datę żeby można było wykonać zapytanie
# #  raz na dobę


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
import requests
import json
import csv
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame

# """
# with open('App_file\zmienneApiDolar.json', mode='r+', encoding='UTF-8') as file:
#     last_time = datetime.now().strftime('%d-%m-%Y')
#     read_file = json.load(file)

#     if read_file['Stable_price']['Dolar'][1] != last_time:
#         print('Request')
#         response = requests.get(read_file['url'], headers=read_file['headers'])
#         status_code = response.status_code
#         if status_code == 200:
#             result = json.loads(response.text)
#             read_file['Stable_price']['Dolar'] = (
#                 result['quotes']['USDPLN'], last_time)
#             file.seek(0, 0)
#             json.dump(read_file, file, ensure_ascii=False, indent=4)
# """

# # a = 'https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_1h.csv'


# # Pobiera i przygotowuje dane do pliku
# # a = 'https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_d.csv'

# # Zrobić warunek by dane były pobierane tylko raz dziennie
# today = datetime.today().strftime("%Y-%m-%d")
# zm = ["ADA", "LTC", "DOGE", "XRP", "BCH", "BTC", "LRC", "ETH", "ARI10"]


# def update_charts_data():
#     with open("App_file\zmienne.json", "r+") as file:
#         jsonFile = json.load(file)
#         if jsonFile["Charts_data"] != today:
#             for i in zm:
#                 url = requests.get(
#                     f"https://www.cryptodatadownload.com/cdd/Binance_{i}USDT_d.csv"
#                 )
#                 if url.status_code == 200:
#                     result = url.text.split("\n", 100)
#                     # print(result[0:2])#'Unix,Date,Symbol,Open,High,Low,Close,Volume BTC,Volume USDT,tradecount'
#                     del result[:2]
#                     # result=result[:93]
#                     result = result[:100]
#                     for j in range(len(result)):
#                         result[j] = result[j].split(",")
#                         del result[j][0], result[j][2:5], result[j][3:]
#                         result[j][0:1] = result[j][0].split(" ")

#                     with open(
#                         f"Chart_file\\{i}_chartdata.csv",
#                         "w",
#                         encoding="UTF-8",
#                         newline="",
#                     ) as d_wykres:
#                         writer = csv.writer(d_wykres)
#                         # print(f'{data_wykres} wczytane dane')
#                         # writer.writerow([data_wykres]) #Wpisywana data pliku
#                         writer.writerows(result)
#                 if url.status_code != 200:
#                     zm.pop(zm.index(i))
#             jsonFile["Charts_data"] = today
#             file.seek(0, 0)
#             json.dump(jsonFile, file, ensure_ascii=False, indent=4)


# def selected_combobox(event):
#     choice = test_box.get()
#     try:
#         with open(f"Chart_file\\{choice}_chartdata.csv", "r", encoding="UTF-8") as file:
#             d_data = file.read().split("\n")
#             del d_data[-1]
#             for i in range((len(d_data))):
#                 d_data[i] = d_data[i].split(",")
#         # print(d_data)  # ['2023-05-07', 'BTCUSDT', '28430.1'], ['2023-05-06',
#         # canvas2 = tk.Canvas(core)
#         # canvas2.grid(row=1, column=0, columnspan=2)

#         chart_frame = tk.Frame(canvas)
#         # chart_frame.configure(bg="Black")
#         canvas.create_window((0, 0), window=chart_frame, anchor="nw")
#         canvas.pack(side="left")

#         def add_to_chart_lists():
#             tmp = i[0][5:]
#             tmp = tmp[3] + tmp[4] + tmp[2] + tmp[0] + tmp[1]

#             chart_list[0].append(tmp)
#             chart_list[1].append(float(i[2]))
#             pass

#         for j in range(3):
#             wykres = plt.Figure(
#                 figsize=(4.2, 1.5), dpi=100, facecolor=(0.18, 0.31, 0.31)
#             )
#             chart_list = [[], []]
#             for i in d_data:
#                 # if j == 0 and i[0] > data_range[0] and i[0] <= data_range[3]:
#                 if j == 0 and i[0] > data_range[0]:  # and i[0] <= data_range[3]:
#                     add_to_chart_lists()
#                 if j == 1 and i[0] > data_range[1]:
#                     add_to_chart_lists()

#                 if j == 2 and i[0] > data_range[2]:
#                     add_to_chart_lists()

#             chart_list[0].reverse()
#             chart_list[1].reverse()

#             def mean():
#                 result = sum(chart_list[1]) / len(chart_list[1])
#                 return result.__round__(3)

#             ax1 = wykres.add_subplot(111)
#             ax1.set_facecolor("darkgrey")
#             ax1.tick_params(labelcolor="White")
#             ax1.grid(axis="both", color="grey")
#             ax1.plot(chart_list[0], chart_list[1])  # x, y

#             def conf_plot(j, text):
#                 ax1.set_xticks(chart_list[0][::j])
#                 ax1.set_title(text, color="white", loc="left")
#                 ax1.hlines(
#                     mean(),
#                     0,
#                     len(chart_list[0]),
#                     colors="r",
#                     label=f"Średnia {str(mean())}$",
#                 )
#                 ax1.set_xlim(chart_list[0][0], chart_list[0][-1])

#                 ax1.plot(
#                     chart_list[1].index(max(chart_list[1])),
#                     max(chart_list[1]),
#                     "o",
#                     color="cyan",
#                 )
#                 ax1.plot(
#                     chart_list[1].index(min(chart_list[1])),
#                     min(chart_list[1]),
#                     "o",
#                 )
#                 ax1.legend()  # labelcolor="white"

#             if j == 0:
#                 conf_plot(
#                     3,
#                     f"Ostatnie 2 tyg. max: {max(chart_list[1])}, min: {min(chart_list[1])} ",
#                 )
#             if j == 1:
#                 conf_plot(
#                     7,
#                     f"Ostatni miesiąc max: {max(chart_list[1])}, min: {min(chart_list[1])}",
#                 )
#             if j == 2:
#                 conf_plot(
#                     14,
#                     f"Ostatnie 3 miesiące max: {max(chart_list[1])}, min: {min(chart_list[1])}",
#                 )
#             line = FigureCanvasTkAgg(wykres, chart_frame)
#             line.get_tk_widget().grid(row=j, ipady=45, ipadx=0)  # , ipadx=20)
#     except FileNotFoundError:
#         print("Nie ma pliku o takiej nazwie")
#     chart_frame.grid(row=0, column=0)
#     # charts_scrollbar.config(command=canvas.yview)
#     # canvas.configure(scrollregion=canvas.bbox("all"))


# root = ttk.Window(themename="darkly")
# core = tk.Frame(root)
# core.grid()
# scroll_frame = ScrolledFrame(core, autohide=True, width=410, height=400)
# scroll_frame.grid(row=1, column=0, columnspan=2)
# print(scroll_frame.vscroll.get())
# frame_wykresy = ttk.Frame(core)
# frame_wykresy.grid(row=1, column=0, columnspan=2, pady=10)
# plt.style.use("seaborn-v0_8-darkgrid")

# test_box = ttk.Combobox(core, values=zm, style="primary", state="readonly")
# test_box.grid(row=0, column=1)  # .pack(anchor="ne")  #
# label = ttk.Label(core, text="Wybierz krypto do wyświetlania wykresu:")
# label.grid(row=0, column=0)  # .pack(anchor="nw")  #
# canvas = ttk.Canvas(scroll_frame)  # , width=430, height=300)

# now = datetime.today() + relativedelta(days=-1)  # from datetime to str
# data_range = (
#     (now + relativedelta(weeks=-2)).strftime("%Y-%m-%d"),
#     (now + relativedelta(months=-1)).strftime("%Y-%m-%d"),
#     (now + relativedelta(months=-3)).strftime("%Y-%m-%d"),
#     now.strftime("%Y-%m-%d"),
# )

# test_box.current(0)
# test_box.bind("<<ComboboxSelected>>", selected_combobox)

# selected_combobox(None)
# # scroll_frame.yview_scroll(50000, "units") ni działa

# root.resizable(False, False)
# root.mainloop()


# """
# now = datetime.today().strftime('%Y-%m-%d') #from datetime to str
# now2=datetime.strptime(now, '%Y-%m-%d') # from str to datetime
# for num in range(N, -1, -1) : # reverse loop
# """


# # before3m = now-relativedelta(month=3)
# # before1m = now-relativedelta(month=1)
# # before2week = now-relativedelta(weeks=2)

# # print(before3m)
# # print(before1m)
# # print(before2week)


# # for i in range(len(d_data)):
# #      d_data[i][0]=d_data[i][0]

# url = requests.get(f"https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_d.csv")
# tmp = url.text.split("\n", 100)[:10]
# print(tmp)

# Test_group = ["Test1", "Test2", "Test3"]

# # filter(function, list)
# a = sorted(Test_group)
# print(a)


req = requests.get(
    "https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_d.csv"
).text.split("\n", 150)
req = req[:150]
del req[:2]
for i, _ in enumerate(req):
    req[i] = req[i].split(",")
    del req[i][0], req[i][2:5], req[i][3:]
    req[i][0:1] = req[i][0].split(" ")

data = [i[0] for i in req]
print(data[:5])
