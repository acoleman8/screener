import sqlite3
import requests

printcheck = 0
incremental = 0

sqlDBpath = "C:/sqlite/db/"
sqlDBname = "test.db"

sqlDB = sqlDBpath + sqlDBname

# Connect to SQLite DB and open cursor
con = sqlite3.connect(sqlDB)
cur = con.cursor()

# Drop and recreate table
if incremental == 0:
    cur.execute('drop table if exists Identifiers')
cur.execute("create table if not exists Identifiers (ISIN VARCHAR, Symbol VARCHAR, Exchange VARCHAR)")

# Read ISINs from Transactions table
cur.execute("Select distinct ISIN, Exchange from Transactions where Exchange <> 'DEGIRO'")

ISINlist = cur.fetchall()

for ISIN in ISINlist:

    exchange = ISIN[1]
    ticker = ''
    
    if exchange == 'NDQ':
        exchange = 'US'
    elif exchange == 'EAM' or exchange == 'DEGIRO':
        exchange = 'NA'
    elif exchange == 'NSY':
        exchange = 'UN'


    data = [{"idType":"ID_ISIN","idValue":ISIN[0],'exchCode':exchange}]
    r = requests.post('https://api.openfigi.com/v1/mapping',
                    headers={"Content-Type": "text/json",'X-OPENFIGI-APIKEY': '3fee7d1a-0429-43b1-a9ca-db07551b2db9'},
                    json=data)

    r = r.json()
    ticker = (r[0]['data'][0]['ticker'])
    cur.execute('Insert into Identifiers values (:v0,:v1,:v2)',{'v0':ISIN[0],'v1':ticker,'v2':exchange})
            


#Select and print all from table
if printcheck == 1:
    cur.execute("select * from Identifiers")

    result = cur.fetchall()
    for i in result:
        print(i)

#Commit changes and close    
con.commit()

cur.close()
con.close()

