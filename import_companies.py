import csv
import sqlite3

printcheck = 0
incremental = 0

sqlDBpath = "C:/sqlite/db/"
sqlDBname = "test.db"

sqlDB = sqlDBpath + sqlDBname

filepath = 'U:/Documents/Dev/ExternalData/'
filename = 'companylist.csv'

file = filepath + filename

# Connect to SQLite DB and open cursor
con = sqlite3.connect(sqlDB)
cur = con.cursor()

# Drop and recreate table
if incremental == 0:
    cur.execute('drop table if exists Companies')
    cur.execute(
        "create table if not exists Companies (Symbol VARCHAR, Name VARCHAR, Sector VARCHAR, Industry VARCHAR);")

# Read data from .csv and insert to table; SKIP COLUMN 8
with open(file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        if i > 0:
            cur.execute("insert into Companies values (:v0,:v1,:v2,:v3)",
                        {'v0': row[0], 'v1': row[1], 'v2': row[6], 'v3': row[7]})

        i += 1

# Select and print all from table
if printcheck == 1:
    cur.execute("select * from Companies")

    result = cur.fetchall()
    for i in result:
        print(i)

# Commit changes and close
con.commit()

cur.close()
con.close()
