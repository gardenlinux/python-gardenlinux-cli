import pytest
from click.testing import CliRunner
import sys

sys.path.append("src")

from glcli import cli


CONTAINER_NAME_ZOT_EXAMPLE = "localhost:5000/gardenlinux"
GARDENLINUX_ROOT_DIR_EXAMPLE = "tests/data/gardenlinux/.build"


@pytest.mark.usefixtures("zot_session")
@pytest.mark.parametrize(
    "version, cname, arch",
    [
        ("today", "aws-gardener_prod", "arm64"),
        ("today", "aws-gardener_prod", "amd64"),
        ("today", "gcp-gardener_prod", "arm64"),
        ("today", "gcp-gardener_prod", "amd64"),
        ("today", "azure-gardener_prod", "arm64"),
        ("today", "azure-gardener_prod", "amd64"),
        ("today", "openstack-gardener_prod", "arm64"),
        ("today", "openstack-gardener_prod", "amd64"),
        ("today", "openstackbaremetal-gardener_prod", "arm64"),
        ("today", "openstackbaremetal-gardener_prod", "amd64"),
        ("today", "metal-kvm_dev", "arm64"),
        ("today", "metal-kvm_dev", "amd64"),
    ],
)
def test_push_manifest(version, arch, cname):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "push-manifest",
            "--container",
            CONTAINER_NAME_ZOT_EXAMPLE,
            "--version",
            version,
            "--arch",
            arch,
            "--cname",
            cname,
            "--dir",
            GARDENLINUX_ROOT_DIR_EXAMPLE,
            "--insecure",
            "True",
            "--cosign_file",
            "digest"
        ],
        catch_exceptions=False,
    )
    if result.exit_code != 0:
        print(f"Exit Code: {result.exit_code}")
        print(f"Output: {result.output}")
        if result.exception:
            print(result.exception)
        try:
            print(f"Output: {result.stderr}")
        except ValueError:
            print("No stderr captured.")
    assert result.exit_code == 0
