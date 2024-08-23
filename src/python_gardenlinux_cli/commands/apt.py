from os import walk
from difflib import *
import sys
import click
from python_gardenlinux_lib.apt.package_repo_info import (
    compare_gardenlinux_repo_version,
    GardenLinuxRepo
)
import re

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

@apt.command()
@click.option(
    '--gardenlinux_version',
    required=True
)
def selected_sbom(gardenlinux_version):
    packages_of_relevance = re.compile('^linux-image-amd64$|^systemd$|^containerd$|^runc$|^curl$|^openssl$|^openssh-server$|^libc-bin$')
    repo = GardenLinuxRepo(gardenlinux_version)
    versions = repo.get_packages_versions()
    selected_versions = sorted([f'{p[0]} {p[1]}\n' for p in versions if packages_of_relevance.match(p[0])])
    sys.stdout.writelines(selected_versions)
