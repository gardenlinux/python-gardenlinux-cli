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
    ],
)
def test_push_manifest_and_index(version, arch, cname):
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
        ],
        catch_exceptions=False,
    )
    print(f"Output: {result.stdout_bytes}")
    if result.exit_code != 0:
        print(f"Exit Code: {result.exit_code}")
        if result.exception:
            print(result.exception)
        try:
            print(f"Output: {result.stderr}")
        except ValueError:
            print("No stderr captured.")
    assert result.exit_code == 0

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
            "--manifest_file",
            "manifest-entry.json",
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
