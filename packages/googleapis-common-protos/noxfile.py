# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from pathlib import Path
import nox

BLACK_VERSION = "black==19.3b0"


@nox.session(python="3.6")
def blacken(session):
    """Run black.
    Format code to uniform standard.
    This currently uses Python 3.6 due to the automated Kokoro run of synthtool.
    That run uses an image that doesn't have 3.6 installed. Before updating this
    check the state of the `gcp_ubuntu_config` we use for that Kokoro run.
    """
    session.install(BLACK_VERSION)
    session.run("black", "google", "setup.py")


@nox.session(python="3.8")
def lint_setup_py(session):
    """Verify that setup.py is valid"""
    session.install("docutils", "pygments")
    session.run("python", "setup.py", "check", "--strict")


@nox.session(python="3.8")
def generate_protos(session):
    """Generates the protos using protoc.
    
    Some notes on the `google` directory:
    1. The `_pb2.py` files are produced by protoc. 
    2. The .proto files are non-functional but are left in the repository
       to make it easier to understand diffs.
    3. The `google` directory also has `__init__.py` files to create proper modules. 
       If a new subdirectory is added, you will need to create more `__init__.py`
       files.
    """
    session.install("grpcio-tools")
    protos = [str(p) for p in (Path(".").glob("google/**/*.proto"))]
    session.run(
        "python", "-m", "grpc_tools.protoc", "--proto_path=.", "--python_out=.", *protos
    )


def default(session):
    # Install all test dependencies, then install this package in-place.
    session.install("mock", "pytest", "pytest-cov")
    session.install("-e", ".")

    # Install googleapis-api-common-protos
    # This *must* be the last install command to get the package from source.
    session.install("..")

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        "--cov=google.cloud",
        "--cov=tests.unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        *session.posargs,
    )


def unit(session):
    """Run the unit test suite."""
    default(session)


def system(session):
    """Run the system test suite."""
    system_test_path = os.path.join("tests", "system.py")
    system_test_folder_path = os.path.join("tests", "system")
    # Sanity check: Only run tests if the environment variable is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""):
        session.skip("Credentials must be set via environment variable")

    system_test_exists = os.path.exists(system_test_path)
    system_test_folder_exists = os.path.exists(system_test_folder_path)
    # Sanity check: only run tests if found.
    if not system_test_exists and not system_test_folder_exists:
        session.skip("System tests were not found")

    # Use pre-release gRPC for system tests.
    session.install("--pre", "grpcio")

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    session.install("mock", "pytest", "google-cloud-testutils")

    session.install("-e", ".")

    # Install googleapis-api-common-protos
    # This *must* be the last install command to get the package from source.
    session.install("..")

    # Run py.test against the system tests.
    if system_test_exists:
        session.run("py.test", "--verbose", system_test_path, *session.posargs)
    if system_test_folder_exists:
        session.run("py.test", "--verbose", system_test_folder_path, *session.posargs)


@nox.session(python=["3.6", "3.7", "3.8"])
@nox.parametrize(
    "library",
    ["python-pubsub", "python-texttospeech"],
    ids=["pubsub", "texttospeech"],
)
def test(session, library):
    """Run tests from a downstream libraries.

    To verify that any changes we make here will not break downstream libraries, clone
    a few and run their unit and system tests.

    NOTE: The unit and system test functions above are copied from the templates. 
    They will need to be updated when the templates change.

    * Pub/Sub: GAPIC with handwritten layer.
    * Text-to-Speech: Full GAPIC.
    """
    try:
        session.run("git", "-C", library, "pull", external=True)
    except nox.command.CommandFailed:
        session.run(
            "git",
            "clone",
            "--single-branch",
            f"https://github.com/googleapis/{library}",
            external=True,
        )
    
    session.cd(library)

    unit(session)

    # system tests are run on 3.7 only
    if session.python == "3.7":
        if library == "python-pubsub":
            session.install("psutil")
        system(session)
