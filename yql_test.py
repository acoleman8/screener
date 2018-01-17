import oauth2 as oauth
import requests
# import time
# import urllib2 as urllib

echo_base_url = 'https://api.login.yahoo.com/oauth2/get_token'

consumer = oauth.Consumer(key ='dj0yJmk9TW55a1FhNFdtdHJ6JmQ9WVdrOVdsUlVibGs0TldVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD02Zg--', secret='0403a53a94cbfe0614f28b2250b83009f0bb2dd8')
client = oauth.Client(consumer)

# r = requests.get('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20pm.finance%20where%20symbol%3D%22OCLR%22&format=json&diagnostics=true&callback=')
# r = r.json()
# print (r)

# params = ""
r = client.request(
            # echo_base_url + "/people/",
'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20pm.finance%20where%20symbol%3D%22OCLR%22&format=json&diagnostics=true&callback=',
            method = "GET",
            #body=params,
            #headers={'Content-type': 'application/xml'}
            #force_auth_header=True
            )
print (r)