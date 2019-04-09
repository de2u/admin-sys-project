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
links = re.findall(r'<link>(.*?)</link>',str(respData))

del titles[0]
del links[0]

for i in reversed(range(len(titles))):
    print(titles[i],'\n',links[i],'\n\n')
