import requests
import pickle

def store_ixp_peering_lans():
    ## ccix contains country code with lists of IXP peering LANs
    ccix = {}

    ## contains useful info on peering lans, indexed by peeringdb ix_id
    ix2lans = {}

    r_ixlan = requests.get("https://beta.peeringdb.com/api/ixlan?depth=2")
    j_ixlan = r_ixlan.json()
    for ixlan in j_ixlan['data']:
        ix_id = ixlan['ix_id']
        #pfx_set = ixlan['prefix_set']
        pfx_set = ixlan['ixpfx_set']
        peeringlans = []
        if len( pfx_set ) == 0:
            continue
        for pe in pfx_set:
            if 'prefix' in pe:
                peeringlans.append( pe['prefix'] )
        if not ix_id in ix2lans:
            ix2lans[ ix_id ] = []
        ix2lans[ ix_id ].append({
            'name': ixlan['name'],
            'desc': ixlan['descr'],
            'peeringlans': peeringlans
        })

    r_ix = requests.get("https://beta.peeringdb.com/api/ix")
    j_ix = r_ix.json()
    for ix in j_ix['data']:
        ix_id = ix['id']
        if not ix_id in ix2lans:
            continue
        icountry = ix['country']
        icity = ix['city']
        iname = ix['name']
        if not icountry in ccix:
            ccix[ icountry ] = []
        # beware of name colisions @@TODO
        ixlan_name = iname
        for ixlan_info in ix2lans[ ix_id ]:
            if ixlan_info['name']:
                ixlan_name += "-%s" % ixlan_info['name']
            elif ixlan_info['desc']:
                ixlan_name += "-%s" % ixlan_info['name']
            ccix[ icountry ].append({
                'name': ixlan_name,
                'peeringlans': ixlan_info['peeringlans']
            })
    return ccix
#f = open('ixp_peering_lans','wb')
#pickle.dump(store_ixp_peering_lans(), f)
#f.close()
