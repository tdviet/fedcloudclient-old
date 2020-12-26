import logging
import click
from fedcloudclient.sites import site

from fedcloudclient.checkin import token
from fedcloudclient.endpoint import endpoint
from fedcloudclient.openstack import openstack


@click.group()
@click.option(
    "--log-level",
    help="Debug level from 0:DEBUG to 4:CRITICAL",
    default=2
)
@click.option(
    "--log-file",
    help="Log filename",
    default=None
)
def cli(log_level, log_file):
    logging_level = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
    if log_file is not None:
        logging.basicConfig(filename=log_file, encoding='utf-8', level=logging_level[log_level])
    else:
        logging.basicConfig(level=logging_level[log_level])


cli.add_command(token)
cli.add_command(endpoint)
cli.add_command(openstack)
cli.add_command(site)

if __name__ == "__main__":
    cli()
