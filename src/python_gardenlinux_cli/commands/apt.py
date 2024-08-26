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

@apt.command()
@click.option(
    '--package_name',
    required=True
)
@click.option(
    '--gardenlinux_version',
    required=True
)
def package_version(package_name, gardenlinux_version):
    repo = GardenLinuxRepo(gardenlinux_version)
    res = repo.get_package_version_by_name(package_name)
    # fixme: Is this a fair assumption? We're not doing a substring matching here, so we will only get exactly 0 or one match, right?
    assert len(res) == 1, f"Expected only one package with name {package_name} in version {gardenlinux_version}, but got {len(res)} results."
    (name, version) = res[0]
    print(f"{name} {version}")

@apt.command()
@click.option(
    '--package_name',
    required=True
)
def package_version_in_all_recent(package_name):
    # similar to 'all suites' in the debian package tracker https://packages.debian.org/search?suite=all&searchon=names&keywords=wget
    # todo: get most recent versions from api
    recent_versions = ['1592.1', '1592.0', '1443.10', '1443.9']
    for gardenlinux_version in recent_versions:
        repo = GardenLinuxRepo(gardenlinux_version)
        res = repo.get_package_version_by_name(package_name)
        # fixme: Is this a fair assumption? We're not doing a substring matching here, so we will only get exactly 0 or one match, right?
        assert len(res) == 1, f"Expected only one package with name {package_name} in version {gardenlinux_version}, but got {len(res)} results."
        (name, version) = res[0]
        print(gardenlinux_version)
        print(f"  {name} {version}")
