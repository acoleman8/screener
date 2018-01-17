import csv
import sqlite3
from datetime import datetime

printcheck = 0
incremental = 0

sqlDBpath = "C:/sqlite/db/"
sqlDBname = "test.db"

sqlDB = sqlDBpath + sqlDBname

filepath = 'U:/Documents/Dev/ExternalData/'
file = 'Account.csv'

file = filepath + file

# Connect to SQLite DB and open cursor
con = sqlite3.connect(sqlDB)
cur = con.cursor()

# Drop and recreate table
if incremental == 0:
    cur.execute('drop table if exists Account')
    cur.execute(
        "create table if not exists Account (Date DATETIME, Product VARCHAR, ISIN VARCHAR, Description VARCHAR, FX Decimal, Currency VARCHAR, Change DECIMAL, Balance DECIMAL);")

# Read data from .csv and insert to table; SKIP ROW 8
with open(file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    i = 0
    for row in reader:
        if i > 0:
            if row[0] != '':
                date = datetime.strptime(row[0] + row[1], '%d-%m-%Y%H:%M')
            else:
                date = ''
            cur.execute("insert into Account values (:v0,:v1,:v2,:v3,:v4,:v5,:v6,:v7)",
                        {'v0': date, 'v1': row[2], 'v2': row[3], 'v3': row[4], 'v4': row[5], 'v5': row[6], 'v6': row[7],
                         'v7': row[9]})

        i += 1

# Select and print all from table
if printcheck == 1:
    cur.execute("select * from Account")

    result = cur.fetchall()
    for i in result:
        print(i)

# Commit changes and close
con.commit()

cur.close()
con.close()
