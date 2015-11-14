from ripe.atlas.sagan import TracerouteResult
import resolve_as
import urllib2
import json

# temporary data
response = urllib2.urlopen('https://atlas.ripe.net/api/v1/measurement/2929523/result/?format=txt')
data = json.load(response)  

my_traceroute = TracerouteResult(data).hops

# mock function awaiting sashas work
def isIxp(ip):
	return 1

result = {}
result['result'] = []

for hop in my_traceroute:
	this_hop = {}
	this_hop['id'] = hop.index
	this_hop['rtt'] = hop.packets[0].rtt
	this_hop['origin'] = hop.packets[0].origin

	if isIxp(hop.packets[0].origin):
		this_hop['ixp'] = "decix"
		this_hop['asnumber'] = "12345"
	else:
		this_hop['asnumber'] = resolve_as.findAsn(hop.packets[0].origin)

	result['result'].append(this_hop)

print result