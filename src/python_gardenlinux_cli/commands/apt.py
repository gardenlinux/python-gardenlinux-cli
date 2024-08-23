from os import walk
from difflib import *
import sys
import click
from python_gardenlinux_lib.apt.package_repo_info import (
    compare_gardenlinux_repo_version,
)


@click.group()
def apt():
    """Manage apt"""
    pass


@apt.command()
@click.option(
    "--version_a",
    required=True,
)
@click.option(
    "--version_b",
    required=True,
)
def compare(version_a, version_b):
    result = compare_gardenlinux_repo_version(version_a, version_b)

    a = sorted([f"{r[0]} {r[1]}\n" for r in result if r[1] is not None])
    b = sorted([f"{r[0]} {r[2]}\n" for r in result if r[2] is not None])

    sys.stdout.writelines(unified_diff(a, b, fromfile=version_a, tofile=version_b))
