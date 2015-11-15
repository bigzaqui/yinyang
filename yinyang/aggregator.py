
#fake source as data
source_as = 1299

def getnode(this_hop):
	if this_hop['ixp']:
		return {"nodetype": "ixp", "descriptor": this_hop['ixp'], "rtt": 0}
	else:
		#return {"nodetype": "asn", "descriptor": this_hop['asn'], "rtt": this_hop['rtt']}
		return {"nodetype": "asn", "descriptor": this_hop['asn'], "rtt": 0}		

def aggregator(traceroute_parsed):
	aggregated_path = [{"nodetype": "source", "descriptor": source_as, "rtt": 0}]

	for hop in traceroute_parsed['result']:
		if len(aggregated_path) == 1:
			aggregated_path.append(getnode(hop))
		else:
			if aggregated_path[-1]['descriptor'] == hop['asn']:
				#aggregated_path[-1]['rtt'] == hop['rtt']
				aggregated_path[-1]['rtt'] == 0
			else:
				aggregated_path.append(getnode(hop))

	aggregated_path[-1]['nodetype'] = "destination"

	return aggregated_path