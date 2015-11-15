from pprint import pprint, pformat
import sys
from traceroute import run_traceroute
import click
from tracerouteparser import process
from aggregator import aggregator
from helpers import get_probe, get_list_probes_from_asn, get_probe_from_close_probe_different_asn
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
@click.option('--another/--no-another', default=False)
@click.option('--dst_asn', required=True)
@click.option('--v6/--no-v6', default=False)
@click.option('--draw/--no-draw', default=False)
def asn_run(src_asn, another, dst_asn, v6, draw):
    ip_version = 'v6' if v6 else 'v4'
    asns = dict(src=src_asn, dst=dst_asn)
    probes = {}
    for x in asns.keys():
        probe_list = get_list_probes_from_asn(asns[x], ip_version)
        probes[x] = random.choice(list(probe_list))

    results = []

    src_dst = {}
    logger.debug('SRC ---> DST')
    src_dst['forward'], src_dst['forward_rtt'] = run_traceroute_wrapper(probes['src'], probes['dst'], ip_version,
                                                                        dst_asn)
    src_dst['forward'][0]['descriptor'] = 'S1'
    src_dst['forward'][-1]['descriptor'] = 'D'
    src_dst['reverse'], src_dst['reverse_rtt'] = run_traceroute_wrapper(probes['dst'], probes['src'], ip_version,
                                                                        src_asn)
    src_dst['reverse'][0]['descriptor'] = 'D'
    src_dst['reverse'][-1]['descriptor'] = 'S1'

    results.append(src_dst)
    if another:
        another_probe = get_probe_from_close_probe_different_asn([src_asn, dst_asn], probes['src'], ip_version)

        src2_dst = {}
        logger.debug('another probe ID %s' % another_probe['id'])
        logger.debug('SRC2 ---> DST')
        src2_dst['forward'], src2_dst['forward_rtt'] = run_traceroute_wrapper(another_probe, probes['dst'], ip_version,
                                                                              dst_asn)
        src2_dst['forward'][0]['descriptor'] = 'S2'
        src2_dst['forward'][-1]['descriptor'] = 'D'
        logger.debug('DST ---> SRC2')
        src2_dst['reverse'], src2_dst['reverse_rtt'] = run_traceroute_wrapper(probes['dst'], another_probe, ip_version,
                                                                              src_asn)
        src2_dst['reverse'][0]['descriptor'] = 'D'
        src2_dst['reverse'][-1]['descriptor'] = 'S2'
        results.append(src2_dst)

    if draw:
        from drawing import draw_results
        draw_results(results)
    else:
        pprint(results)


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
