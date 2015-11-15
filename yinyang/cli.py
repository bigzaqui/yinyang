from pprint import pprint
from traceroute import run_traceroute
import click
from tracerouteparser import process
from aggregator import aggregator
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--probe_id')
@click.option('--dst_ip')
def cli(probe_id, dst_ip):
    traceroute_object = run_traceroute(probe_id,dst_ip)
    logger.error('Returned traceroute')
    traceroute_parsed = process(traceroute_object)
    pprint(aggregator(traceroute_parsed))

if __name__ == "__main__":
    cli()