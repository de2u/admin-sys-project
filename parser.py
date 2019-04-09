import urllib.request
import urllib.parse
import re

url = 'http://www.cert.ssi.gouv.fr/site/cert-fr_alerte.rss'
values = {}
data = urllib.parse.urlencode(values)
data = data.encode('utf-8')
req = urllib.request.Request(url, data)
resp = urllib.request.urlopen(req)
respData = resp.read()

# print(respData)

titles = re.findall(r'<title>(.*?)</title>',str(respData))
links = re.findall(r'<guid ispermalink=\"true\">(.*)</guid>',str(respData))


for eachT in titles:
    print(eachT)

print(100*'#')

for eachL in links:
    print(eachL)
