#!/bin/env python3

import click

from python_gardenlinux_cli.commands import oci, ocm, apt


@click.group()
def cli():
    """
    Garden Linux maintanance and development CLI
    """
    pass


cli.add_command(oci.oci)
cli.add_command(ocm.ocm)
cli.add_command(apt.apt)


if __name__ == "__main__":
    cli()
