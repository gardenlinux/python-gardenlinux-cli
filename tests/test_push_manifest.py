import pytest
from click.testing import CliRunner
import sys
sys.path.append("src")
from glcli import cli

CONTAINER_NAME_ZOT_EXAMPLE = "127.0.0.1:18081/gardenlinux-example"
#GARDENLINUX_ROOT_DIR_EXAMPLE = "test-data/build-metal-gardener_prod"
TEST_DATA_DIR = ""

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
            "1702.0",
            "--arch",
            "amd64",
            "--cname",
            "metal-gardener_prod",
            "--dir",
            #GARDENLINUX_ROOT_DIR_EXAMPLE
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