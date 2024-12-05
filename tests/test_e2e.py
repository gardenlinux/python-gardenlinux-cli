import pytest
from click.testing import CliRunner
import sys
import logging

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
    ],
)
def test_push_manifest_and_index(version, arch, cname):
    logger = logging.getLogger(__name__)
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
            "digest",
            "--manifest_file",
            "manifests/manifest.json",
        ],
        catch_exceptions=False,
    )
    print(f"Output: {result.output}")
    if result.exit_code != 0:
        print(f"Exit Code: {result.exit_code}")
        if result.exception:
            print(result.exception)
        try:
            print(f"Output: {result.stderr}")
        except ValueError:
            print("No stderr captured.")
    assert result.exit_code == 0

    logger.info("Pushed manifests")

    result = runner.invoke(
        cli,
        [
            "update-index",
            "--container",
            CONTAINER_NAME_ZOT_EXAMPLE,
            "--version",
            version,
            "--insecure",
            "True",
            "--manifest_folder",
            "manifests",
        ],
        catch_exceptions=False,
    )
    print(f"Output: {result.output}")
    if result.exit_code != 0:
        print(f"Exit Code: {result.exit_code}")
        if result.exception:
            print(result.exception)
        try:
            print(f"Output: {result.stderr}")
        except ValueError:
            print("No stderr captured.")
    assert result.exit_code == 0
