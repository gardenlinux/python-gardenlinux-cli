import os
import click
from registry import GlociRegistry

@click.group()
@click.option(
    "--insecure", default=True, is_flag=True, help="Allow insecure connections"
)
@click.pass_context
def oci(ctx, insecure):
    """Manage images"""
    ctx.ensure_object(dict)
    ctx.obj["insecure"] = insecure

@oci.command()
@click.option(
    "--container",
    "container_name",
    required=True,
    type=click.Path(),
    help="Container Name",
)
@click.option(
    "--architecture",
    required=True,
    type=click.Path(),
    help="Target Image CPU Architecture",
)
@click.option(
    "--cname", required=True, type=click.Path(), help="Canonical Name of Image"
)
@click.option("--version", required=True, type=click.Path(), help="Version of Image")
@click.option("--dir", required=True, help="path to the build artifacts")
@click.option(
    "--cosign_file",
    required=False,
    help="A file where the pushed manifests digests is written to. The content can be used by an external tool (e.g. cosign) to sign the manifests contents",
)
@click.pass_context
def push_from_dir(
    ctx,
    container_name,
    architecture,
    cname,
    version,
    dir,
    cosign_file,
):
    """push artifacts from a dir to a registry"""
    container_name = f"{container_name}:{version}"
    registry = GlociRegistry(
        container_name=container_name,
        insecure=ctx.obj["insecure"],
        token=os.getenv("GLOCI_REGISTRY_TOKEN"),
    )
    digest = registry.push_from_dir(architecture, version, cname, dir)
    if cosign_file:
        print(digest, file=open(cosign_file, "w"))