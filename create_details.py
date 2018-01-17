import requests
import sqlite3

from lxml import html

printCheck = 0
incremental = 1

sqlDBPath = "C:/sqlite/db/"
sqlDBName = "test.db"

sqlDB = sqlDBPath + sqlDBName

# Connect to SQLite DB and open cursor
con = sqlite3.connect(sqlDB)
cur = con.cursor()

# Drop and recreate table
if incremental == 0:
    cur.execute('drop table if exists Details')
cur.execute(
    "create table if not exists Details (Symbol VARCHAR, Name VARCHAR, Price DECIMAL, MarketCap Decimal, TargetPrice DECIMAL, PE DECIMAL, PB DECIMAL, PEG DECIMAL, MA50 DECIMAL, MA200 DECIMAL)")

cur.execute(
    "Select Symbol from Companies where Industry = 'Semiconductors'")
result = cur.fetchall()

for row in result:
    symbol = row[0]
    print(symbol)

    cur.execute("INSERT into Details (Symbol) VALUES (:v0) EXCEPT SELECT Symbol FROM Details WHERE Symbol = :v0",
                {'v0': symbol})

    statsURL = 'https://api.iextrading.com/1.0/stock/' + symbol + '/stats'
    # requestURL = 'https://api.iextrading.com/1.0/ref-data/symbols'

    r = requests.get(statsURL)
    r = r.json()

    name = r['companyName']
    marketCap = r['marketcap']
    pb = r['priceToBook']
    ma50 = r['day50MovingAvg']
    ma200 = r['day200MovingAvg']

    quoteURL = 'https://api.iextrading.com/1.0/stock/' + symbol + '/quote'

    r = requests.get(quoteURL)
    r = r.json()

    price = r['latestPrice']
    pe = r['peRatio']

    page = requests.get('https://finance.yahoo.com/quote/' + symbol)
    tree = html.fromstring(page.content)

    target = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[8]/td[2]/span/text()')
    if len(target) > 0:
        target = target[0]
    else:
        target = 'N/A'

    cur.execute(
        'UPDATE Details SET Name = :name, Price = :price, MarketCap = :marketCap, TargetPrice = :target, PE = :pe, PB = :pb, MA50 = :ma50, MA200 = :ma200 WHERE Symbol = :symbol;',
        {'name': name, 'price': price, 'marketCap': marketCap, 'target': target, 'pe': pe, 'pb': pb, 'ma50': ma50,
         'ma200': ma200, 'symbol': symbol})

# for row in r:
# print(row)
# print(row + ',' + str(r[row]))


# Commit changes and close
con.commit()

cur.close()
con.close()
