from pprint import pprint, pformat
import sys
from traceroute import run_traceroute
import click
from tracerouteparser import process
from aggregator import aggregator
from helpers import get_probe, get_list_probes_from_asn, get_list_probes_from_close_probe_different_asn
import random

import logging
import click_log

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.WARNING)
requests_log.propagate = True


@click.group()
@click.option('--verbose/--no-verbose', default=False)
def cli(verbose):
    if verbose:
        requests_log.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)


@cli.group()
def asn():
    pass


def run_traceroute_wrapper(src_probe, dst_probe, ip_version, dst_asn):
    dst_probe_ip = dst_probe["address_%s" % ip_version]
    traceroute_object = run_traceroute(str(src_probe['id']), dst_probe_ip)
    traceroute_parsed = process(traceroute_object)
    return aggregator(traceroute_parsed, dst_asn)


@asn.command('run')
@click_log.init()
@click.option('--src_asn', required=True)
@click.option('--another_probe_id', required=False)
@click.option('--dst_asn', required=True)
@click.option('-v6', default=False)
def asn_run(src_asn, another_probe_id, dst_asn, v6, ):
    ip_version = 'v6' if v6 else 'v4'
    asns = dict(src=src_asn, dst=dst_asn)
    probes = {}
    for x in asns.keys():
        probe_list = get_list_probes_from_asn(asns[x], ip_version)
        probes[x] = random.choice(list(probe_list))

    logger.debug('SRC ---> DST')
    forward, reverse = [], []
    forward.append(run_traceroute_wrapper(probes['src'], probes['dst'], ip_version, dst_asn))

    logger.debug('DST ---> SRC')
    reverse.append(run_traceroute_wrapper(probes['dst'], probes['src'], ip_version, src_asn))

    if another_probe_id:
        another_probe = get_probe(another_probe_id)
        forward.append(run_traceroute_wrapper(another_probe, probes['dst'], ip_version, dst_asn))
        reverse.append(run_traceroute_wrapper(probes['dst'], another_probe, ip_version,
                                              another_probe['asn_%s' % ip_version]))

    logging.debug(pformat(forward))
    logging.debug(pformat(reverse))


@cli.group()
def probe():
    pass


@probe.command('run')
@click_log.init()
@click.option('--src_probe_id', required=True)
@click.option('--dst_probe_id', required=True)
@click.option('-v6', default=False)
def probe_run(src_probe_id, dst_probe_id, v6):
    ip_version = 'v6' if v6 else 'v4'
    run_traceroute_wrapper(get_probe(src_probe_id), get_probe(dst_probe_id), ip_version, 'EMPTY')


if __name__ == "__main__":
    # try:
    cli()
    # except Exception as e:
    #     click.echo(e.message)
    #     sys.exit(1)
