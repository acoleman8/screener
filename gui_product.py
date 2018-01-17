import sqlite3
from tkinter import *
from tkinter import ttk
import requests

sqlDBpath = "C:/sqlite/db/"
sqlDBname = "test.db"

sqlDB = sqlDBpath + sqlDBname

# Connect to SQLite DB and open cursor
con = sqlite3.connect(sqlDB)
cur = con.cursor()

root = Tk()
root.title("Portfolio")

cur.execute('Select AvgPrice.Ticker, AvgPrice, Portfolio.Closing from AvgPrice left join Identifiers on AvgPrice.Ticker = Identifiers.Symbol left join Portfolio on Identifiers.ISIN = Portfolio.ISIN ')
result = cur.fetchall()


    
content = ttk.Frame(root, padding="3 3 12 12")
content.grid(column=0, row=0, sticky=(N, W, E, S))

content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=1)


#ttk.Label(content, text="Symbol").grid(column=1, row=1, sticky=E)
ttk.Label(content, text="Bought").grid(column=1, row=0, sticky=W)
ttk.Label(content, text="Closing").grid(column=2, row=0, sticky=W)
ttk.Label(content, text="Change").grid(column=3, row=0, sticky=W)
ttk.Label(content, text=str("%")).grid(column=4, row=0, sticky=W)

x = 1

for row in result:
    symbol = row[0]
    avgprice = row[1]
    closingprice = row[2]
    change = round(closingprice - avgprice,2)
    percentchange = round(change/closingprice * 100,2)
    #r = requests.get("https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20pm.finance%20where%20symbol%3D%22OCLR%22&format=json&diagnostics=true&callback=")
    #r = r.json()
    # print (r)
    ttk.Label(content, text=symbol).grid(column=0, row=x, sticky=E)
    ttk.Label(content, text=avgprice).grid(column=1, row=x, sticky=W)
    ttk.Label(content, text=closingprice).grid(column=2, row=x, sticky=W)
    ttk.Label(content, text=change).grid(column=3, row=x, sticky=W)
    ttk.Label(content, text=str(percentchange)+'%').grid(column=4, row=x, sticky=W)

    x+=1

for child in content.winfo_children(): child.grid_configure(padx=5, pady=5)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=0)
content.columnconfigure(1, weight=1)
content.columnconfigure(2, weight=1)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)

root.after(5000,ch)

root.mainloop()
