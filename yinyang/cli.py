from pprint import pprint
from traceroute import run_traceroute
import click


@click.command()
@click.option('--probe_id')
@click.option('--dst_ip')
def cli(probe_id, dst_ip):
    a = run_traceroute(probe_id,dst_ip)
    pprint(a)
    print(a.af)


if __name__ == "__main__":
    cli()