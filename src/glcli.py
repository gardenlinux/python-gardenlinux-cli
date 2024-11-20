#!/bin/env python3

import click
from oci import oci


@click.group()
def glcli():
    """
    Garden Linux maintanance and development CLI
    """
    pass


glcli.add_command(oci)

if __name__ == "__main__":
    glcli()
