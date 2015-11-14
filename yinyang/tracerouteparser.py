import urllib2
import json
import requests

from ripe.atlas.sagan import TracerouteResult

def findAsn(ip):
    r = requests.get("https://stat.ripe.net/data/network-info/data.json?resource=%s" % ip)
    result = r.json()

    try:
        asn = result['data']['asns'][0]
    except:
        asn = "12345"

    return asn


# temporary data
response = urllib2.urlopen('https://atlas.ripe.net/api/v1/measurement/2929523/result/?format=txt')
data = json.load(response)

my_traceroute = TracerouteResult(data).hops


# mock function awaiting sashas work
def isIxp(ip):
    return 1


def getMemberByIXPIP(ip):
    return 15170


result = {}
result['result'] = []

for hop in my_traceroute:
    this_hop = {}
    this_hop['id'] = hop.index
    this_hop['rtt'] = hop.packets[0].rtt
    this_hop['origin'] = hop.packets[0].origin

    if isIxp(hop.packets[0].origin):
        this_hop['ixp'] = "decix"

        try:
            this_hop['asnumber'] = getMemberByIXPIP(hop.packets[0].origin)
        except:
            this_hop['asnumber'] = 12345

    else:
        this_hop['asnumber'] = findAsn(hop.packets[0].origin)

    result['result'].append(this_hop)

print result
