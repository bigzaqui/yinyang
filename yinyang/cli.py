from pprint import pprint
from traceroute import run_traceroute
import click
from tracerouteparser import process
from aggregator import aggregator
import logging
from probe_stuff import resolve_as_to_probes
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--src_asn')
@click.option('--dst_asn')
@click.option('-v6', default=False)
def cli(src_asn, dst_asn, v6):
    ip_version = 'v6' if v6 else 'v4'
    asns = dict(src=src_asn,dst=dst_asn)
    probes = {}
    for x in asns.keys():
        tmp = resolve_as_to_probes(asns[x], ip_version)
        if tmp:
            probe_object = random.choice(list(tmp))
            probes[x] = str(probe_object['id']), probe_object["address_%s" % ip_version]

        else:
            raise Exception('no probes found for the src_asn.')

    #SRC -> DST
    pprint(probes)
    traceroute_object = run_traceroute(probes['src'][0], probes['dst'][1])
    pprint(traceroute_object.raw_data)

    logger.error('Returned traceroute')
    traceroute_parsed = process(traceroute_object)
    pprint(aggregator(traceroute_parsed))

if __name__ == "__main__":
    cli()