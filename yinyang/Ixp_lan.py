import pickle
from netaddr import *
import requests

class Ixp_lan:
    ixp_lans = {}

    def __init__(self):
        f = open('ixp_peering_lans','r')  
        # load the object from the file into var b
        self.ixp_lans = pickle.load(f)
        count_ixp = 0
        for country_code, ixps in self.ixp_lans.iteritems():
            for ixp in ixps:
                count_ixp = count_ixp + 1
        
    def check_for_ixp_ip(self, address):
        ip = IPAddress(address)
        for country_code, ixps in self.ixp_lans.iteritems():
            for ixp in ixps:
                for lan in ixp['peeringlans']:
                    network = IPNetwork(lan)
                    if network.version == ip.version:
                        if ip in network:
                            return country_code, ixp['name']
        return False,False

    def query_for_ip(self, address):
        ip = IPAddress(address)
        r = requests.get('https://beta.peeringdb.com/api/netixlan?ipaddr%s=%s'%(ip.version, address))
        j = r.json()
        return j['data'][0]['asn']


# How to use:
#ixp_lans = Ixp_lan()
#print ixp_lans.check_for_ixp_ip('195.66.246.1')
#print ixp_lans.query_for_ip('194.68.123.238')
#print ixp_lans.query_for_ip('2001:7f8::20d3:0:1')
