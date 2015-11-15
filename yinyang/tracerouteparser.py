import urllib2
import json
import requests
import logging
from ripe.atlas.sagan import TracerouteResult
from Ixp_lan import Ixp_lan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def findAsn(ip):
    r = requests.get("https://stat.ripe.net/data/network-info/data.json?resource=%s" % ip)
    result = r.json()

    try:
        asn = result['data']['asns'][0]
    except:
        asn = "12345"

    return asn



result = {}
result['result'] = []

def process(my_traceroute):
    for hop in my_traceroute.hops:
        if hop.packets[0].origin:
            this_hop = {}
            this_hop['id'] = hop.index
            #this_hop['rtt'] = hop.packets[0].rtt
            this_hop['origin'] = hop.packets[0].origin
            ixp_object = Ixp_lan()

            countrycode, name = ixp_object.check_for_ixp_ip(hop.packets[0].origin)

            if countrycode:
                this_hop['ixp'] = name

                try:
                    this_hop['asn'] = ixp_object.query_for_ip(hop.packets[0].origin)
                except:
                    this_hop['asn'] = 12345

            else:
                this_hop['ixp'] = False
                this_hop['asn'] = findAsn(hop.packets[0].origin)

            result['result'].append(this_hop)
        else:
            logger.error('skipped invalid hop')

    return result
