from helper import call_command, spawn_background_process
import os
import sys
import shutil
import pytest


@pytest.fixture(autouse=False, scope="function")
def zot_session():
    print("Starting zot session")
    zot_config = "tests/zot/config.json"
    print(f"Spawning zot registry with config {zot_config}")
    zot_process = spawn_background_process(
        f"zot serve {zot_config}",
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    yield zot_process
    print("Clean up zot session")

    zot_process.terminate()

    if os.path.isdir("./output"):
        shutil.rmtree("./output")


def pytest_sessionstart(session):
    call_command("./tests/cert/gencert.sh")
    print("pytest session started")
    call_command("./tests/data/build-test-data.sh --dummy")


def pytest_sessionfinish(session):
    print(" pytest session finished")
    if os.path.isfile("./tests/cert/oci-sign.crt"):
        os.remove("./tests/cert/oci-sign.crt")
    if os.path.isfile("./tests/cert/oci-sign.key"):
        os.remove("./tests/cert/oci-sign.key")
