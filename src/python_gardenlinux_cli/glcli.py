#!/bin/env python3

import click
from ocm import ocm
from apt import apt
from oci import oci


@click.group()
def glcli():
    """
    Garden Linux maintanance and development CLI
    """
    pass


glcli.add_command(oci)
glcli.add_command(ocm)
glcli.add_command(apt)


if __name__ == "__main__":
    glcli()
