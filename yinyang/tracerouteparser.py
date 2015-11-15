import requests
import logging
from Ixp_lan import Ixp_lan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def findAsn(ip):
    try:
        r = requests.get("https://stat.ripe.net/data/network-info/data.json?resource=%s" % ip)
        result = r.json()
        return result['data']['asns'][0]
    except:
        # failed to lookup as-number
        return False

def process(my_traceroute):
    result = {}
    result['result'] = []
    
    for hop in my_traceroute.hops:
        if hop.packets[0].origin:
            this_hop = {}
            this_hop['id'] = hop.index
            this_hop['rtt'] = hop.packets[0].rtt
            this_hop['origin'] = hop.packets[0].origin
            ixp_object = Ixp_lan()

            countrycode, name = ixp_object.check_for_ixp_ip(hop.packets[0].origin)

            if countrycode:
                this_hop['ixp'] = name

                try:
                    this_hop['asn'] = ixp_object.query_for_ip(hop.packets[0].origin)
                except:
                    #found a rouge AS on an IXP. What to do?
                    this_hop['asn'] = 101010101

            else:
                this_hop['ixp'] = False
                this_hop['asn'] = findAsn(hop.packets[0].origin)

            result['result'].append(this_hop)
        else:
            logger.error('skipped invalid hop')

    return result
