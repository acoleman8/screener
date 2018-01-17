import csv
import sqlite3

# Connect to SQLite DB and open cursor
con = sqlite3.connect("C:/sqlite/db/test.db")
cur = con.cursor()

# Drop and recreate table
cur.execute('drop table Portfolio')
cur.execute("create table if not exists Portfolio (Product VARCHAR, ISIN VARCHAR, Amount INTEGER, Closing DECIMAL, Currency VARCHAR, Local_Value DECIMAL, Value_ in_EUR DECIMAL);")


# Read data from .csv and insert to table
with open('U:/Documents/Dev/ExternalData/Portfolio.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    i = 0
    for row in reader:
        if i > 2:
            cur.execute("insert into Portfolio values (:v0,:v1,:v2,:v3,:v4,:v5,:v6)", {'v0':row[0], 'v1':row[1],'v2':row[2], 'v3':row[3], 'v4':row[4], 'v5':row[5], 'v6':row[6]})

        i += 1

#Select and print all from table
cur.execute("select * from Portfolio")

result = cur.fetchall()
for i in result:
    print(i)

#Commit changes and close    
con.commit()

cur.close()
con.close()
