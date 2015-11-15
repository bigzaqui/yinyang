from ripe.atlas.cousteau import ProbeRequest


def get_probe(probe_id):
    filters = {"id": probe_id, "is_public": True, "status": 1}
    output = list(ProbeRequest(**filters))
    if output:
        return output[0]
    else:
        raise Exception('cannot find probe with ID: %s:' % probe_id)


def get_list_probes_from_asn(asn,ip_version):
    filters = {"asn_%s" % ip_version: asn, "is_public": True, "status": 1}
    output = list(ProbeRequest(**filters))
    if output:
        return output
    else:
        raise Exception('cannot find probe with that AS: %s' % asn)

