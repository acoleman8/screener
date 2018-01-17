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
root.resizable(False, False)


def loadPortfolioTable():
    # Drop and recreate table
    cur.execute('drop table if exists gPortfolio')
    cur.execute(
        "create table if not exists gPortfolio (Symbol VARCHAR, AvgPrice FLOAT, Price FLOAT, Change FLOAT, PercentChange FLOAT);")

    cur.execute(
        'Select AvgPrice.Ticker, AvgPrice, Exchange from AvgPrice left join Identifiers on AvgPrice.Ticker = Identifiers.Symbol where Exchange in ("UN","US") and Total <> 0 order by Ticker')
    result = cur.fetchall()

    tickerString = ''
    count = 0

    for i in result:
        if count > 0:
            tickerString += ','
        tickerString += i[0]
        count += 1

    apiKey = 'ETR7MOFS0KMYTBG4'
    requestURL = 'https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols=' + tickerString + '&apikey=' + apiKey

    r = requests.get(requestURL)
    r = r.json()

    r = r['Stock Quotes']
    quotes = {}
    for i in r:
        quotes[i['1. symbol']] = i['2. price']

    x = 1

    for row in result:
        symbol = row[0]
        avgprice = row[1]
        exchange = row[2]

        price = float(quotes[symbol])
        change = round(price - avgprice, 2)
        percentchange = round(change / avgprice * 100, 2)

        cur.execute("insert into gPortfolio values (:v0,:v1,:v2,:v3,:v4)",
                    {'v0': symbol, 'v1': avgprice, 'v2': price, 'v3': change, 'v4': percentchange})
        x += 1

        # Commit changes
        con.commit()


def readPortfolioTable():
    cur.execute('Select * from gPortfolio')
    result = cur.fetchall()

    content = ttk.Frame(root, padding="3 3 12 12")
    content.grid(column=0, row=0, sticky=(N, W, E, S))

    content.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=1)

    # ttk.Label(content, text="Symbol").grid(column=1, row=1, sticky=E)
    ttk.Label(content, text="Bought").grid(column=1, row=0, sticky=W)
    ttk.Label(content, text="Current").grid(column=2, row=0, sticky=W)
    ttk.Label(content, text="Change").grid(column=3, row=0, sticky=W)
    ttk.Label(content, text=str("%")).grid(column=4, row=0, sticky=W)

    x = 1

    for row in result:
        symbol = row[0]
        avgprice = row[1]
        price = row[2]
        change = row[3]
        percentchange = row[4]

        ttk.Label(content, text=symbol).grid(column=0, row=x, sticky=E)
        ttk.Label(content, text=avgprice).grid(column=1, row=x, sticky=W)
        ttk.Label(content, text=price).grid(column=2, row=x, sticky=W)
        ttk.Label(content, text=change).grid(column=3, row=x, sticky=W)
        ttk.Label(content, text=str(percentchange) + '%').grid(column=4, row=x, sticky=W)

        x += 1

    for child in content.winfo_children(): child.grid_configure(padx=5, pady=5)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=0)
    content.columnconfigure(0, weight=0)
    content.columnconfigure(1, weight=1)
    content.columnconfigure(2, weight=1)
    content.columnconfigure(3, weight=1)
    content.columnconfigure(4, weight=1)

    # print('refresh')


def portfolio():
    loadPortfolioTable()
    readPortfolioTable()
    # root.after(5000, portfolio)


portfolio()

root.mainloop()
