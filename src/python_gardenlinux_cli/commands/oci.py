# my_project/commands/image.py
import json

import click
import oras.client
import oras.container
from python_gardenlinux_lib.features import parse_features
from python_gardenlinux_lib.oras.registry import GlociRegistry


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
@click.option(
    "--gardenlinux_root",
    required=True,
    type=click.Path(),
    help="path to root directory of Garden Linux sources. Required for calculating all features based on cname",
)
@click.option(
    "--gardenlinux_root",
    required=True,
    type=click.Path(),
    help="path to root directory of Garden Linux sources. Required for calculating all features based on cname",
)
@click.option(
    "--build_output",
    required=False,
    type=click.Path(),
    help="path to .build directory of build targets.",
)
@click.option(
    "--cosign_file",
    required=False,
    help="A file where the pushed manifests digests is written to. The content can be used by an external tool (e.g. cosign) to sign the manifests contents",
)
@click.pass_context
def push(
    ctx,
    container_name,
    architecture,
    cname,
    version,
    gardenlinux_root,
    build_output,
    cosign_file,
):
    """push local build artifacts to a registry"""
    if not build_output:
        build_output = f"{gardenlinux_root}/.build"

    container_name = f"{container_name}:{version}"
    oci_metadata = parse_features.get_oci_metadata(
        cname, version, architecture, gardenlinux_root
    )

    features = parse_features.get_features(cname, gardenlinux_root)
    registry = GlociRegistry(
        container_name=container_name, insecure=ctx.obj["insecure"]
    )
    digest = registry.push_image_manifest(
        architecture, cname, version, build_output, oci_metadata, feature_set=features
    )
    if cosign_file:
        print(digest, file=open(cosign_file, 'w'))
    click.echo(f"Pushed {container_name}")


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
@click.option("--tar", required=True, help="path to the build-tarball")
@click.option(
    "--cosign_file",
    required=False,
    help="A file where the pushed manifests digests is written to. The content can be used by an external tool (e.g. cosign) to sign the manifests contents",
)
@click.pass_context
def push_from_tarball(
    ctx,
    container_name,
    architecture,
    cname,
    version,
    tar,
    cosign_file,
):
    """push artifacts from a tarball to a registry"""
    container_name = f"{container_name}:{version}"
    registry = GlociRegistry(
        container_name=container_name, insecure=ctx.obj["insecure"]
    )
    digest = registry.push_from_tar(architecture, version, cname, tar)
    if cosign_file:
        print(digest, file=open(cosign_file, 'w'))


@oci.command()
@click.option(
    "--container",
    "container_name",
    required=True,
    type=click.Path(),
    help="container string e.g. ghcr.io/gardenlinux/gardenlinux:1337",
)
@click.option("--cname", required=True, type=click.Path(), help="cname of target image")
@click.option("--version", required=True, type=click.Path(), help="Version of Image")
@click.option(
    "--architecture", required=True, type=click.Path(), help="architecture of image"
)
@click.option(
    "--file_path",
    required=True,
    type=click.Path(),
    help="file to attach to the manifest",
)
@click.option(
    "--media_type", required=True, type=click.Path(), help="mediatype of file"
)
@click.option(
    "--private_key",
    required=False,
    type=click.Path(),
    help="Path to private key to use for signing",
    default="cert/oci-sign.key",
    show_default=True,
)
@click.option(
    "--public_key",
    required=False,
    type=click.Path(),
    help="Path to public key to use for verification of signatures",
    default="cert/oci-sign.crt",
    show_default=True,
)
@click.pass_context
def attach(
    ctx,
    container_name,
    cname,
    version,
    architecture,
    file_path,
    media_type,
    private_key,
    public_key,
):
    """Attach data to an existing image manifest"""
    container_name = f"{container_name}:{version}"
    registry = setup_registry(
        container_name,
        insecure=ctx.obj["insecure"],
        private_key=private_key,
        public_key=public_key,
    )

    registry.attach_layer(cname, version, architecture, file_path, media_type)

    click.echo(f"Attached {file_path} to {container_name}")


@oci.command()
@click.option(
    "--container", "container_name", required=True, help="oci image reference"
)
@click.option("--version", required=True, type=click.Path(), help="Version of Image")
@click.pass_context
def status(ctx, container_name, version):
    """Get status of image"""
    container_name = f"{container_name}:{version}"
    registry = setup_registry(container_name, insecure=ctx.obj["insecure"])
    registry.status_all()


@oci.command()
@click.option(
    "--container", "container_name", required=True, help="oci image reference"
)
@click.option("--cname", required=True, help="cname of image")
@click.option("--version", required=True, type=click.Path(), help="Version of Image")
@click.option("--architecture", required=True, help="architecture of image")
@click.option(
    "--public_key",
    required=False,
    type=click.Path(),
    help="Path to public key to use for verification of signatures",
    default="cert/oci-sign.crt",
    show_default=True,
)
@click.pass_context
def inspect(ctx, container_name, cname, version, architecture, public_key):
    """inspect container"""
    container_name = f"{container_name}:{version}"
    container = oras.container.Container(container_name)
    registry = setup_registry(
        container_name, insecure=ctx.obj["insecure"], public_key=public_key
    )
    print(
        json.dumps(
            registry.get_manifest_by_cname(container, cname, version, architecture),
            indent=4,
        )
    )


@oci.command()
@click.option(
    "--container", "container_name", required=True, help="oci image reference"
)
@click.option("--version", required=True, type=click.Path(), help="Version of Image")
@click.option(
    "--public_key",
    required=False,
    type=click.Path(),
    help="Path to public key to use for verification of signatures",
    default="cert/oci-sign.crt",
    show_default=True,
)
@click.pass_context
def inspect_index(ctx, container_name, version, public_key):
    """inspects complete index"""
    container_name = f"{container_name}:{version}"
    registry = setup_registry(
        container_name, insecure=ctx.obj["insecure"], public_key=public_key
    )
    print(json.dumps(registry.get_index(), indent=4))
