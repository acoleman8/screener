import json
import os
import datetime
import requests
import urllib.request

conf_path = 'C:/Users/acoleman/Documents/Dev/config.json'

conf = json.load(open(conf_path))
sess = requests.Session()

# Login
url = 'https://trader.degiro.nl/login/secure/login'
payload = {'username': conf['username'],
           'password': conf['password'],
           'isPassCodeReset': False,
           'isRedirectToMobile': False}
header = {'content-type': 'application/json'}

r = sess.post(url, data=json.dumps(payload))
print('Login')
print('\tStatus code: {}'.format(r.status_code))

# Get session id
sessid = r.headers['Set-Cookie']
sessid = sessid.split(';')[0]
sessid = sessid.split('=')[1]


print('\tSession id: {}'.format(sessid))

filepath= 'U:/Documents/Dev/ExternalData/'
filename = 'Transactions.csv'
filename_old = 'Transactions_old.csv'

file = filepath + filename
file_old = filepath +filename_old

if os.path.isfile(file_old):
    os.remove(file_old)
if os.path.isfile(file):
    os.rename(file,file_old)

now = datetime.datetime.now()

toDate = now.strftime("%d") + '%2F' + now.strftime("%m") + '%2F' + now.strftime("%Y")

transactionsURL = 'https://trader.degiro.nl/reporting/secure/v3/transactionReport/csv?intAccount=165000183&sessionId=' + sessid + '&country=IE&langTransactionsByOrder=true=en&fromDate=01%2F08%2F2016&toDate=' + toDate + '&group'
response = urllib.request.urlretrieve(transactionsURL,file)