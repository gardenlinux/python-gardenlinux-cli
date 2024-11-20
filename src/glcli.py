#!/bin/env python3

import click
import os
from registry import GlociRegistry
@click.group()
def cli():
    pass

@cli.command()
@click.option("--container", required=True, type=click.Path(), help="Container Name",)
@click.option("--version", required=True, type=click.Path(), help="Version of image",)
@click.option("--arch",required=True,type=click.Path(),help="Target Image CPU Architecture",)
@click.option("--cname", required=True, type=click.Path(), help="Canonical Name of Image")
@click.option("--dir", required=True, help="path to the build artifacts")
@click.option("--cosign_file", required=False, help="A file where the pushed manifests digests is written to. The content can be used by an external tool (e.g. cosign) to sign the manifests contents",)
def push_manifest(container, version, arch, cname, dir, cosign_file):
    """push artifacts from a dir to a registry"""
    container_name = f"{container}:{version}"
    registry = GlociRegistry(
        container_name=container_name,
        token=os.getenv("GLOCI_REGISTRY_TOKEN"),
    )
    digest = registry.push_from_dir(arch, version, cname, dir)
    if cosign_file:
        print(digest, file=open(cosign_file, "w"))

@cli.command()
@click.option("--container", "container",required=True, type=click.Path(), help="Container Name",)
@click.option("--version", "version" ,required=True, type=click.Path(), help="Version of image",)
def push_index(container, version):
    click.echo(f"Push index {container}, {version}")

if __name__ == '__main__':
    cli()
