import pickle
from netaddr import *


class Ixp_lan:
    ixp_lans = {}

    def __init__(self):
        f = open('ixp_peering_lans', 'r')
        # load the object from the file into var b
        self.ixp_lans = pickle.load(f)
        count_ixp = 0
        for country_code, ixps in self.ixp_lans.iteritems():
            for ixp in ixps:
                count_ixp = count_ixp + 1

        print 'Number of IXPS: %s' % count_ixp

    def check_for_ixp_ip(self, address):
        for country_code, ixps in self.ixp_lans.iteritems():
            for ixp in ixps:
                # print ixp['name'].decode('utf-8')
                # print ixp['peeringlans']
                for lan in ixp['peeringlans']:
                    ip = IPNetwork(lan)
                    if IPAddress(address) in ip:
                        return country_code, ixp['name']


# How to use:
#ixp_lans = Ixp_lan()
#print ixp_lans.check_for_ixp_ip('195.66.246.1')
