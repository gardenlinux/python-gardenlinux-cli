from os import walk
import click
from python_gardenlinux_lib.package_repo_info import compare_gardenlinux_repo_version


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
    print(result)
