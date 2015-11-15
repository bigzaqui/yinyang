from pprint import pprint
from ripe.atlas.cousteau import ProbeRequest
import sys
from traceroute import run_traceroute
import click
from tracerouteparser import process
from aggregator import aggregator
import logging
from helpers import resolve_as_to_probes, get_probe, get_list_probes_from_asn
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.group()
def asn():
    """
    Information about ip ranges.
    """
    pass


def run_traceroute_wrapper(src_probe, dst_probe, ip_version):
    dst_probe_ip = dst_probe["address_%s" % ip_version]
    traceroute_object = run_traceroute(str(src_probe['id']), dst_probe_ip)
    traceroute_parsed = process(traceroute_object)
    pprint(aggregator(traceroute_parsed))


@asn.command('run')
@click.option('--src_asn', required=True)
@click.option('--dst_asn', required=True)
@click.option('-v6', default=False)
def asn_run(src_asn, dst_asn, v6):
    ip_version = 'v6' if v6 else 'v4'
    asns = dict(src=src_asn, dst=dst_asn)
    probes = {}
    for x in asns.keys():
        probe_list = get_list_probes_from_asn(asns[x], ip_version)
        probes[x] = random.choice(list(probe_list))

    logger.warning('SRC ---> DST')
    run_traceroute_wrapper(probes['src'],probes['dst'],ip_version)

    logger.warning('DST ---> SRC')
    run_traceroute_wrapper(probes['dst'],probes['src'],ip_version)

@cli.group()
def probe():
    """
    Information about ip ranges.
    """
    pass


@probe.command('run')
@click.option('--src_probe_id', required=True)
@click.option('--dst_probe_id', required=True)
@click.option('-v6', default=False)
def probe_run(src_probe_id, dst_probe_id, v6):
    ip_version = 'v6' if v6 else 'v4'
    run_traceroute_wrapper(get_probe(src_probe_id), get_probe(dst_probe_id), ip_version)


if __name__ == "__main__":
    cli()
