#!/bin/env python3

import click

from python_gardenlinux_cli.commands import oci, ocm, apt


@click.group()
def glcli():
    """
    Garden Linux maintanance and development CLI
    """
    pass


glcli.add_command(oci.oci)
glcli.add_command(ocm.ocm)
glcli.add_command(apt.apt)


if __name__ == "__main__":
    glcli()
