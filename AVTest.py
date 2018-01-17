# https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols=MSFT,FB,AAPL&apikey=demo
import sqlite3
import requests


sqlDBpath = "C:/sqlite/db/"
sqlDBname = "test.db"

sqlDB = sqlDBpath + sqlDBname

# Connect to SQLite DB and open cursor
con = sqlite3.connect(sqlDB)
cur = con.cursor()

cur.execute(
        'Select AvgPrice.Ticker, AvgPrice, Exchange from AvgPrice left join Identifiers on AvgPrice.Ticker = Identifiers.Symbol where Exchange in ("UN","US") and Total <> 0 order by Ticker')
result = cur.fetchall()

tickerString = ''
count = 0

for i in result:
    if count > 0:
        tickerString += ','
    tickerString += i[0]
    count+=1

print(tickerString)

apiKey = 'ETR7MOFS0KMYTBG4'
requestURL = 'https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols=' + tickerString +'&apikey=' + apiKey

r = requests.get(requestURL)
r = r.json()

r = r['Stock Quotes']
quotes = {}
for i in r:
    print(i)
    quotes[i['1. symbol']]=i['2. price']

