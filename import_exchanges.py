import csv
import sqlite3

printcheck = 0
incremental = 0

sqlDBpath = "C:/sqlite/db/"
sqlDBname = "test.db"

sqlDB = sqlDBpath + sqlDBname

filepath= 'C:/Users/acoleman/Downloads/'
filename = 'Exchanges.csv'

file = filepath + filename

# Connect to SQLite DB and open cursor
con = sqlite3.connect(sqlDB)
cur = con.cursor()

# Drop and recreate table
if incremental == 0:
    cur.execute('drop table if exists Exchanges')
    cur.execute("create table if not exists Exchanges (MIC VARCHAR, Operating MIC VARCHAR, Name VARCHAR, Corp Exchange VARCHAR, Exch Code VARCHAR, Country VARCHAR);")


# Read data from .csv and insert to table; SKIP ROW 8
with open(file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        if i > 0:
            cur.execute("insert into Exchanges values (:v0,:v1,:v2,:v3,:v4,:v5)", {'v0':row[0], 'v1':row[1],'v2':row[2], 'v3':row[3], 'v4':row[4], 'v5':row[7]})

        i += 1

#Select and print all from table
if printcheck == 1:
    cur.execute("select * from Exchanges")

    result = cur.fetchall()
    for i in result:
        print(i)

#Commit changes and close    
con.commit()

cur.close()
con.close()
