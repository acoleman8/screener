def gui_details(filter):
    import sqlite3
    #from tkinter import Tk
    from tkinter import ttk,Tk,N,S,E,W
    #from yahoo_finance import Share

    sqlDBpath = "C:/sqlite/db/"
    sqlDBname = "test.db"

    sqlDB = sqlDBpath + sqlDBname

    # Connect to SQLite DB and open cursor
    con = sqlite3.connect(sqlDB)
    cur = con.cursor()

    root = Tk()
    root.title("Portfolio")

    #filter = 'OCLR'

    cur.execute('SELECT ISIN, Symbol, Exchange, Name, Market_Cap, Target_Price, PE, PB, PEG, MA50, MA200, AvgPrice, Current_Price FROM Details left join AvgPrice on Details.Symbol = AvgPrice.Ticker where Symbol = :filter',{'filter':filter})
    result = cur.fetchone()



    content = ttk.Frame(root, padding="3 3 12 12")
    content.grid(column=0, row=0, sticky=(N, W, E, S))

    content.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=1)



    ISIN = result[0]
    symbol = result[1]
    exchange = result[2]
    name = result[3]
    marketCap = result[4]
    targetPrice = result[5]
    pe = result[6]
    pb = result[7]
    peg = result[8]
    ma50 = result[9]
    ma200 = result[10]
    avgPrice = result[11]
    currentPrice = result[12]
    # if exchange == 'NA':
    #     stock = Share(symbol+'.AS')
    # else:
    #     stock = Share(symbol)
    # price = float(stock.get_price())
    avgChange = round(currentPrice - avgPrice,2)
    avgPercent = round(avgChange/currentPrice * 100,2)

    targetChange = round(targetPrice - currentPrice,2)
    targetPercent = round(targetChange/currentPrice * 100,2)

    targetAvgChange = round(targetPrice - avgPrice,2)
    targetAvgPercent = round(targetAvgChange/avgPrice * 100,2)

    ttk.Label(content, text=symbol).grid(column=0, row=0, sticky=E)
    ttk.Label(content, text=name).grid(column=1, row=0, sticky=W)
    ttk.Label(content, text=ISIN).grid(column=2, row=0, columnspan=2, sticky=E)

    ttk.Label(content, text="Current: ").grid(column=0, row=1, sticky=E)
    ttk.Label(content, text=currentPrice).grid(column=1, row=1, sticky=W)
    # ttk.Label(content, text="Change").grid(column=2, row=1, sticky=W)
    # ttk.Label(content, text="%").grid(column=3, row=1, sticky=W)

    ttk.Label(content, text='Bought: ').grid(column=0, row=2, sticky=E)
    ttk.Label(content, text=avgPrice).grid(column=1, row=2, sticky=W)
    ttk.Label(content, text=avgChange).grid(column=2, row=2, sticky=W)
    ttk.Label(content, text=str(avgPercent)+'%').grid(column=3, row=2, sticky=W)

    ttk.Label(content, text='Target: ').grid(column=0, row=3, sticky=E)
    ttk.Label(content, text=targetPrice).grid(column=1, row=3, sticky=W)
    ttk.Label(content, text=str(targetChange) + ' (' + str(targetAvgChange) + ')').grid(column=2, row=3, sticky=W)
    ttk.Label(content, text=str(targetPercent) + '% (' + str(targetAvgPercent) + '%)').grid(column=3, row=3, sticky=W)

    # ttk.Label(content, text=price).grid(column=2, row=x, sticky=W)
    # ttk.Label(content, text=change).grid(column=3, row=x, sticky=W)
    # ttk.Label(content, text=str(percentchange)+'%').grid(column=4, row=x, sticky=W)


    for child in content.winfo_children(): child.grid_configure(padx=5, pady=5)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=0)
    content.columnconfigure(0, weight=0)
    content.columnconfigure(1, weight=1)
    content.columnconfigure(2, weight=1)
    content.columnconfigure(3, weight=1)
    content.columnconfigure(4, weight=1)


    root.mainloop()
