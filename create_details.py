import sqlite3
from yahoo_finance import Share

printCheck = 0
incremental = 0

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
    "create table if not exists Details (ISIN VARCHAR, Symbol VARCHAR, Exchange VARCHAR, Name VARCHAR, Market_Cap VARCHAR, Target_Price FLOAT, Current_Price FLOAT, PE FLOAT, PB FLOAT, PEG FLOAT, MA50 FLOAT, MA200 FLOAT)")

# Read ISINs from Transactions table
cur.execute("Select Symbol, ISIN, Exchange from Identifiers")

result = cur.fetchall()

for row in result:
    symbol = row[0]
    ISIN = row[1]
    exchange = row[2]
    if exchange == 'NA':
        stock = Share(symbol + '.AS')
    else:
        stock = Share(symbol)
    name = stock.get_name()
    marketCap = stock.get_market_cap()
    targetPrice = stock.get_one_yr_target_price()
    currentPrice = stock.get_price()
    pe = stock.get_price_earnings_ratio()
    pb = stock.get_price_book()
    peg = stock.get_price_earnings_growth_ratio()
    ma50 = stock.get_50day_moving_avg()
    ma200 = stock.get_200day_moving_avg()

    cur.execute('Insert into Details values (:v0,:v1,:v2,:v3,:v4,:v5,:v6,:v7,:v8,:v9,:v10,:v11)',
                {'v0': ISIN, 'v1': symbol, 'v2': exchange, 'v3': name, 'v4': marketCap, 'v5': targetPrice,
                 'v6': currentPrice, 'v7': pe, 'v8': pb, 'v9': peg, 'v10': ma50, 'v11': ma200})

# Commit changes and close
con.commit()

cur.close()
con.close()
