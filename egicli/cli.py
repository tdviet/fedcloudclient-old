import logging

import click

from egicli.checkin import token
from egicli.endpoint import endpoint
from egicli.openstack import openstack


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    # level = logging.DEBUG if debug else logging.INFO
    # logging.basicConfig(level=level)
    pass


cli.add_command(token)
cli.add_command(endpoint)
cli.add_command(openstack)

if __name__ == "__main__":
    cli()
