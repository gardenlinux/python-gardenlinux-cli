from helper import call_command, spawn_background_process
import os
import tempfile
import sys
import shutil
import json
import pytest
from dotenv import load_dotenv


@pytest.fixture(autouse=False, scope="function")
def zot_session():
    load_dotenv()
    print("start zot session")
    zot_config = json.load(open("tests/zot/config.json"))

    print(f"Spawning zot registry with config {zot_config}")
    zot_process = spawn_background_process(
        f"zot serve {zot_config}",
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    yield zot_process
    print("clean up zot session")

    zot_process.terminate()

    if os.path.isdir("./output"):
        shutil.rmtree("./output")


def pytest_sessionstart(session):
    # call_command("./cert/gencert.sh")
    print(" pytest session started")
    call_command("./tests/data/build-test-data.sh --dummy")


def pytest_sessionfinish(session):
    print(" pytest session finished")
    # if os.path.isfile("./cert/oci-sign.crt"):
    #    os.remove("./cert/oci-sign.crt")
    # if os.path.isfile("./cert/oci-sign.key"):
    #    os.remove("./cert/oci-sign.key")
