import requests
import json

myip = "8.8.8.8"

def findAsn(ip):
	r = requests.get("https://stat.ripe.net/data/network-info/data.json?resource=%s" % ip)
	result = r.json()
	asn = result['data']['asns'][0]
	return asn

print findAsn(myip)