import requests
from ripe.atlas.cousteau import ProbeRequest


def get_probe(probe_id):
    filters = {"id": probe_id, "is_public": True, "status": 1}
    output = list(ProbeRequest(**filters))
    if output:
        return output[0]
    else:
        raise Exception('cannot find probe with ID: %s:' % probe_id)


def get_list_probes_from_asn(asn, ip_version):
    filters = {"asn_%s" % ip_version: asn, "is_public": True, "status": 1}
    output = list(ProbeRequest(**filters))
    if output:
        return output
    else:
        raise Exception('cannot find probe with that AS: %s' % asn)


def get_probe_from_close_probe_different_asn(asns, probe, ip_version):
    lon = probe['geometry']['coordinates'][0]
    lat = probe['geometry']['coordinates'][1]

    filters = {"center": "%s%s" % (lat, lon),
               "distance": 2,
               "is_public": True, "status": 1}

    url = 'https://atlas.ripe.net/api/v1/probe/'

    r = requests.get(url, params=filters)
    if r:
        v = r.json()
        return next(x for x in v['objects'] if x["asn_%s" % ip_version] not in asns)
    else:
        raise Exception('cannot find a close probe to the ASN: %s:' % probe['id'])
