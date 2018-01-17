import sqlite3

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
    cur.execute('drop table if exists AvgPrice')
cur.execute("create table if not exists AvgPrice (Ticker VARCHAR, AvgPrice DECIMAL, Value DECIMAL, Total INTEGER)")

# Read ISINs
cur.execute("Select distinct ISIN from Transactions")

ISINlist = cur.fetchall()

# Read Transaction data for each ISIN
for ISIN in ISINlist:
            
    cur.execute("Select Symbol, Number, Price, Value from Transactions left join Identifiers on Transactions.ISIN = Identifiers.ISIN where Transactions.ISIN =:ISIN order by date(Date) asc",{'ISIN':ISIN[0]})

    result = cur.fetchall()

# Calculate Average Price
    symbol = result[0][0]
    total = 0
    totalValue = 0
    avgPrice = 0

    for row in result:
        # print(row)
        number = row[1]
        price = row[2]
        value = row[3]

        total += number
        totalValue += value

        if total != 0:
            avgPrice = totalValue/total*-1

        print (symbol + ", " + str(total) + ", " + str(avgPrice))

    avgPrice = round(avgPrice, 2)
    cur.execute("Insert into AvgPrice values (:v1, :v2, :v3, :v4)", {'v1': symbol, 'v2': avgPrice, 'v3': totalValue, 'v4': total})

# Select and print all from table
if printCheck == 1:
    cur.execute("select * from AvgPrice")

    result = cur.fetchall()
    for i in result:
        print(i)

# Commit changes and close
con.commit()

cur.close()
con.close()
