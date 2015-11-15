from ripe.atlas.cousteau import ProbeRequest


def resolve_as_to_probes(asn, ip_version):
    filters = {"asn_%s" % ip_version: asn, "is_public": True, "status": 1}
    return ProbeRequest(**filters)


def get_probe(probe_id):
    filters = {"id": probe_id, "is_public": True, "status": 1}
    output = list(ProbeRequest(**filters))
    if output:
        return output[0]
    else:
        raise Exception('cannot find probe with that id.')


def get_list_probes_from_asn(asn,ip_version):
    tmp = resolve_as_to_probes(asn, ip_version)
    if tmp:
        return list(tmp)
    else:
        raise Exception('no probes found for the src_asn.')

