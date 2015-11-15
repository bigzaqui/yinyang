from ripe.atlas.cousteau import ProbeRequest

def resolve_as_to_probes(asn, ip_version):
    filters = { "asn_%s" % ip_version: asn, "is_public": True, "status" : 1}
    return ProbeRequest(**filters)

