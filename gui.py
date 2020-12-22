import tkinter as tk
from tkcalendar import Calendar, DateEntry
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt

today = datetime.now().strftime('%Y-%m-%d')

mydb = mysql.connector.connect(
    host="localhost",
    user="username,
    password="password",
    database="mtgPrices"
)

cursor = mydb.cursor()

query = '''SELECT name, price FROM DECKS ORDER BY price DESC'''
cursor.execute(query)
result = cursor.fetchall()
Texts = []
Price = []
for i in result:
    Texts.append(i[0])
    Price.append(i[1])

datequery = '''SELECT date FROM PHISTORY'''
cursor.execute(datequery)
result = cursor.fetchall()
date = [i[0] for i in result]
date = list(dict.fromkeys(date))

def getUid(s):
    cursor.execute('''SELECT uid FROM DECKS where name=%s''', (s,))
    r = cursor.fetchall()
    if r:
        return(r[0][0]) 


def queryList(s, d):
    listq = '''SELECT list FROM DECKLIST where uid=%s and date=%s'''
    cursor.execute(listq, (getUid(s), d))
    r = cursor.fetchall()
    if r:
        return r[0][0]



root = tk.Tk()

def fetchCard(s):
    cursor.execute('''SELECT price, date FROM CHISTORY where name=%s''', (s,))
    r=cursor.fetchall()
    prices = []
    dates = []
    if r:
        for i in r:
            prices.append(i[0])
            dates.append(i[1])
        plt.plot(dates, prices)
        plt.ylabel('price over time')
        plt.show()
    

def searchCard():
    s = e3.get()
    input3.set('')
    fetchCard(s)

def deckPhistory(s):
    cursor.execute('''SELECT price, date FROM PHISTORY where uid=%s''', (getUid(s), ))
    r = cursor.fetchall()
    if(r):
        prices = []
        dates = []
        for i in r:
            prices.append(i[0])
            dates.append(i[1])
        plt.plot(dates, prices)
        plt.ylabel('price over time')
        plt.show()

def deckSelected(s):
    deckT = tk.Tk()
    deckq = '''SELECT date FROM PHISTORY as k JOIN (SELECT uid FROM DECKS where name=%s) as t ON k.uid=t.uid'''
    cursor.execute(deckq, (s, ))
    r = cursor.fetchall()
    if r:
        deckDates = [i[0] for i in r]
    c = 0
    r = 1
    deck = queryList(s, today)
    for i in deck.splitlines():
        if not i.isspace() and i != '':
            butt = tk.Button(deckT, text=i, command= lambda temp=i : fetchCard(temp[temp.find(" ")+1:]))
            butt.grid(row=r,column=c)
            c += 1
            if c > 5:
                c = 0
                r += 1

    butt = tk.Button(deckT, text="Show Price History", command= lambda temp=s : deckPhistory(temp))
    butt.grid(row=r+2, column=0)
    
    
    deckT.mainloop()

def lessthan():
    lprice = int(e1.get())
    input.set('')
    new = tk.Tk()
    pricequery1 = '''SELECT name, price FROM DECKS WHERE price<%s ORDER BY price DESC'''
    cursor.execute(pricequery1, (lprice,))
    r = cursor.fetchall()
    if(r):
        names = [i[0] for i in r]
        p = [i[1] for i in r]
        r = 1
        c = 0
        for i, z in enumerate(names):
            butt = tk.Button(new, text=z+"\n$"+str(p[i]), command= lambda ztemp=z : deckSelected(ztemp))
            butt.grid(row=r,column=c)
            c += 1
            if c > 5:
                c = 0
                r += 1
    new.title("Price < " + str(lprice))
    new.mainloop()

def greaterthan():
    hprice = int(e2.get())
    input2.set('')
    new2 = tk.Tk()
    pricequery2 = '''SELECT name, price FROM DECKS WHERE price>%s ORDER BY price DESC'''
    cursor.execute(pricequery2, (hprice,))
    r = cursor.fetchall()
    if(r):
        names = [i[0] for i in r]
        p = [i[1] for i in r]
        r = 1
        c = 0
        for i, z in enumerate(names):
            butt = tk.Button(new2, text=z+"\n$"+str(p[i]), command= lambda ztemp=z : deckSelected(ztemp))
            butt.grid(row=r,column=c)
            c += 1
            if c > 5:
                c = 0
                r += 1
    new2.title("Price > " + str(hprice))
    new2.mainloop()

def dateselect(d):
    dateT = tk.Tk()
    dquery = '''SELECT name, dateprice FROM DECKS as k JOIN (SELECT uid, price as dateprice FROM PHISTORY where date=%s) as t ON k.uid=t.uid'''
    cursor.execute(dquery, (d, ))
    r = cursor.fetchall()
    if(r):
        names = [i[0] for i in r]
        p = [i[1] for i in r]
        r = 1
        c = 0
        for i, z in enumerate(names):
            butt = tk.Button(dateT, text=z+"\n$"+str(p[i]), command= lambda ztemp=z : deckSelected(ztemp))
            butt.grid(row=r,column=c)
            c += 1
            if c > 5:
                c = 0
                r += 1
    dateT.title(d)
    dateT.mainloop()


Buttons=[]

r = 1
c = 0
input=tk.StringVar()
input2=tk.StringVar()
input3=tk.StringVar()
for i, z in enumerate(Texts):
    Buttons.append(tk.Button(root, text=z+"\n$"+str(Price[i]), command= lambda ztemp=z : deckSelected(ztemp)))
    Buttons[i].grid(row=r,column=c)
    c += 1
    if c > 5:
        c = 0
        r += 1

label = tk.Label(root, text="Price less than:")
label.grid(row = 10, column=0)
e1 = tk.Entry(root, textvariable=input)
e1.grid(row=10, column=1)
enter = tk.Button(root, text="enter", command=lessthan)
enter.grid(row=10, column=2)

label2 = tk.Label(root, text="Price greater than:")
label2.grid(row = 11, column=0)
e2 = tk.Entry(root, textvariable=input2)
e2.grid(row=11, column=1)
enter2 = tk.Button(root, text="enter", command=greaterthan)
enter2.grid(row=11, column=2)

label3 = tk.Label(root, text="Search Card:")
label3.grid(row = 12, column=0)
e3 = tk.Entry(root, textvariable=input3)
e3.grid(row=12, column=1)
enter3 = tk.Button(root, text="enter", command=searchCard)
enter3.grid(row=12, column=2)

r += 2
c = 0
label3 = tk.Label(root, text="Select Day: ")
label3.grid(row=r, column=c)
c += 1
for i in date:
    butt = tk.Button(root, text=i.strftime('%Y-%m-%d'), command = lambda d=i : dateselect(d))
    butt.grid(row=r, column=c)
    c += 1
    


root.title("Deck Data")

root.mainloop()