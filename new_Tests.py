
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

  
# zmienne_file=json.load(open('App_file\zmienne.json'))

# # print(zmienne_file['connect_file'])
# # print(zmienne_file['connect_file'])
# # print(zmienne_file['connect_file'])
# with(open('App_file\zmienne.json','r'))as dane:
#     zmienne_file2=json.load(dane)

# a=str(zmienne_file['Sciezka_portfel'])
# i=5
# a=a.replace('{i}',f'{i}')

# print(a)
# print(zmienne_file2['Sciezka_portfel'])

# import threading as th
# import time
# def dodanie(lista :list,poczatek:int,koniec:int): 
#     for i in range(poczatek,koniec,1):
#         lista.append(i)

# tm=[10,11,12,13,14,15,16,17,18,19]

# def dod(lista:list):

#     for i in lista:
#         l1.append(i)

#     time.sleep(1)

# l1=[1,2,3,4,5,6,7,8,9,10] #source
# # l1=[1,2,3,4,5,6,7,8,9,10,11] #source
# # l1=[1,2,3,4,5,6,7,8,9] #source
# l2=[]
# l3=[]
# l4=[]

# len_l1=len(l1)
# if (len_l1%3==0):
#     len_l12=int((len_l1/3))
#     len_l13=int((len_l1-len_l12))
# if (len_l1%3==1):
#     len_l12=int((len_l1/3)+1)
#     len_l13=int((len_l1-len_l12)+1)
# if (len_l1%3==2):
#     len_l12=int((len_l1/3)+1)
#     len_l13=int((len_l1-len_l12)+1)

    
# print(len_l1)
# print(len_l12)
# print(len_l13)

# temp_l1,temp_l2,temp_l3=[],[],[]

# th.Thread(target=dodanie(temp_l1,0,len_l12))
# th.Thread(target=dodanie(temp_l2,len_l12,len_l13))
# th.Thread(target=dodanie(temp_l3,len_l13,len_l1))

# print(temp_l1)
# print(temp_l2)
# print(temp_l3)

# z=temp_l1+temp_l2+temp_l3
# print(z)

# th1.start()
# th1.join()
# th2.start()
# th2.join()

# th3=th.Thread(target=dodanie(l3,1,len_2_l1)).start()
# th4=th.Thread(target=dodanie(l4,len_2_l1,len_l1)).start()

# # th.Thread(target=dod(tm)).start()
# z=l3+l4


# # print(l2)
# print(l3)
# print(l4)
# print(z)

# with(open('App_file\zmienne.json','r', encoding='UTF-8'))as dane:
#     zmienne_file=json.load(dane)

# # print(zmienne_file)

# a=zmienne_file['connect_file']['path_portfel']
# print(a)


# url = f"https://api.apilayer.com/currency_data/live?source={source}¤cies= PLN"
# url = f"https://api.apilayer.com/currency_data/live?source=USD"
# url = "https://api.apilayer.com/currency_data/live?source=USD&currencies=PLN"
# headers= {"apikey": "o49OHWHzwbhE38MkfZZNDoOCV3bgOkBt"}
# response = requests.request("GET", url, headers=headers)
# status_code = response.status_code
# result = json.loads(response.text)
# print(result['quotes']['USDPLN'])

# działa i pobiera odpowiednią cenę zapisać
#  jeszcze datę żeby można było wykonać zapytanie
#  raz na dobę


'''
Działa tylko trzeba wrzucić do aplikacji oraz ustawić by zostało sprwdzane co 24 h do aktualizacji
import requests
import json

with open('App_file\zmienneTest.json',mode='r+',encoding='UTF-8') as file:
    url = "https://api.apilayer.com/currency_data/live?source=USD&currencies=PLN"
    headers= {"apikey": "o49OHWHzwbhE38MkfZZNDoOCV3bgOkBt"}
    response = requests.request("GET", url, headers=headers)
    status_code = response.status_code
    result = json.loads(response.text)

    file_str=file.read()
    a=json.loads(file_str)
    a['Stable_price']['Dolar']=result['quotes']['USDPLN']

    file.seek(0,0)
    json.dump(a,file,ensure_ascii=False,indent=4)
'''

