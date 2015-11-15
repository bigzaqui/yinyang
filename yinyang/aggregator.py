def getnode(this_hop):
    if this_hop['ixp']:
        return {"nodetype": "ixp", "descriptor": this_hop['ixp'], "rtt": 0}
    else:
        # return {"nodetype": "asn", "descriptor": this_hop['asn'], "rtt": this_hop['rtt']}
        return {"nodetype": "asn", "descriptor": this_hop['asn'], "rtt": 0}


def aggregator(traceroute_parsed, dst_asn):
    aggregated_path = [{"nodetype": "source", "descriptor": 0, "rtt": 0}]

    for hop in traceroute_parsed['result']:
        if hop['asn'] and (len(aggregated_path) == 1):
            aggregated_path.append(getnode(hop))

        elif hop['asn']:
                if aggregated_path[-1]['descriptor'] == hop['asn']:
                    # we already have this asnumber in our path
                    #aggregated_path[-1]['rtt'] == hop['rtt']
                    continue
                elif hop['asn'] == dst_asn:
                    # we are now in the destination as number for this traceroute. 
                    # this means we have all we need to plot our data
                    # adding the new hop and then we're inserting our destination object
                    aggregated_path.append(getnode(hop))
                    aggregated_path.append({"nodetype": "destination", "descriptor": 0, "rtt": 0})
                    break
                else:
                    # this is the first occurence of this asnumber. add it
                    aggregated_path.append(getnode(hop))

    return aggregated_path
