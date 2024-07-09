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
import pathlib
from pathlib import Path
import re
import tempfile

import nox

BLACK_VERSION = "black==22.3.0"

# `grpcio-tools` 1.59.0 or newer is required for protobuf 5.x compatibility.
GRPCIO_TOOLS_VERSION = "grpcio-tools==1.59.0"

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
UNIT_TEST_PYTHON_VERSIONS = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True


@nox.session(python="3.8")
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


def unit(session, repository, package, prerelease, protobuf_implementation, working_dir):
    """Run the unit test suite."""

    downstream_dir = repository
    if package:
        downstream_dir = f"{repository}/packages/{package}"

    # Install all test dependencies, then install this package in-place.
    session.install("asyncmock", "pytest-asyncio")

    # Pin mock due to https://github.com/googleapis/python-pubsub/issues/840
    session.install("mock==5.0.0", "pytest", "pytest-cov")

    install_command = ["-e", f"{working_dir}/{downstream_dir}"]
    if prerelease:
        install_prerelease_dependencies(
            session,
            f"{working_dir}/{downstream_dir}/testing/constraints-{UNIT_TEST_PYTHON_VERSIONS[0]}.txt",
        )
        # Use the `--no-deps` options to allow pre-release versions of dependencies to be installed
        install_command.extend(["--no-deps"])
    else:
        contraints_file = f"{CURRENT_DIRECTORY}/testing/constraints-{session.python}-{repository}.txt"
        if not Path(contraints_file).exists():
            contraints_file = f"{CURRENT_DIRECTORY}/testing/constraints-{session.python}.txt"

        install_command.extend(["-c", contraints_file])

    # These *must* be the last 3 install commands to get the packages from source.
    session.install(*install_command)

    # Remove the 'cpp' implementation once support for Protobuf 3.x is dropped.
    # The 'cpp' implementation requires Protobuf<4.
    if protobuf_implementation == "cpp":
        session.install("protobuf<4")

    # Install this library from source
    session.install(".", "--no-deps", "--ignore-installed")

    # Print out package versions of dependencies
    session.run(
        "python", "-c", "import google.protobuf; print(google.protobuf.__version__)"
    )
    session.run("python", "-c", "import grpc; print(grpc.__version__)")
    session.run("python", "-c", "import google.auth; print(google.auth.__version__)")

    session.run(
        "python", "-c", "import google.api_core; print(google.api_core.__version__)"
    )

    # Run py.test against the unit tests in the downstream repository
    with session.chdir(f"{working_dir}/{downstream_dir}"):
        session.run(
            "py.test",
            "--quiet",
            "--cov=google/cloud",
            "--cov=tests/unit",
            "--cov-append",
            "--cov-config=.coveragerc",
            "--cov-report=",
            "--cov-fail-under=0",
            os.path.join("tests", "unit"),
            *session.posargs,
            env={
                "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": protobuf_implementation,
            },
        )


def install_prerelease_dependencies(session, constraints_path):
    with open(constraints_path, encoding="utf-8") as constraints_file:
        constraints_text = constraints_file.read()
        # Ignore leading whitespace and comment lines.
        constraints_deps = [
            match.group(1)
            for match in re.finditer(
                r"^\s*(\S+)(?===\S+)", constraints_text, flags=re.MULTILINE
            )
        ]
        session.install(*constraints_deps)
        prerel_deps = [
            "protobuf",
            "six",
            "grpcio",
            "grpcio-status",
            "google-api-core",
            "google-auth",
            "proto-plus",
            "google-cloud-testutils",
            # dependencies of google-cloud-testutils"
            "click",
        ]

        for dep in prerel_deps:
            session.install("--pre", "--no-deps", "--upgrade", dep)

        # Remaining dependencies
        other_deps = [
            "requests",
        ]
        session.install(*other_deps)


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
@nox.parametrize(
    "library,prerelease,protobuf_implementation",
    [
        (("python-pubsub", None), False, "python"),
        (("python-pubsub", None), False, "upb"),
        (("python-pubsub", None), False, "cpp"),
        (("python-pubsub", None), True, "python"),
        (("python-pubsub", None), True, "upb"),
        (("python-pubsub", None), True, "cpp"),
        (("google-cloud-python", "google-cloud-speech"), False, "python"),
        (("google-cloud-python", "google-cloud-speech"), False, "upb"),
        (("google-cloud-python", "google-cloud-speech"), False, "cpp"),
        (("google-cloud-python", "google-cloud-speech"), True, "python"),
        (("google-cloud-python", "google-cloud-speech"), True, "upb"),
        (("google-cloud-python", "google-cloud-speech"), True, "cpp"),
    ],
)
def test(session, library, prerelease, protobuf_implementation):
    """Run tests from a downstream libraries.

    To verify that any changes we make here will not break downstream libraries, clone
    a few and run their unit tests.

    NOTE: The unit test functions above are copied from the templates.
    They will need to be updated when the templates change.

    * Pub/Sub: GAPIC with handwritten layer.
    * Speech: Full GAPIC, has long running operations.
    """
    if prerelease and session.python != UNIT_TEST_PYTHON_VERSIONS[-1]:
        session.skip("Prerelease test is only run using the latest python runtime")

    if protobuf_implementation == "cpp" and session.python in ("3.11", "3.12"):
        session.skip("cpp implementation is not supported in python 3.11+")

    repository, package = library
    with tempfile.TemporaryDirectory() as working_dir:
        session.run(
            "git",
            "clone",
            "--single-branch",
            f"https://github.com/googleapis/{repository}",
            f"{working_dir}/{repository}",
            external=True,
        )

        unit(
            session=session,
            repository=repository,
            package=package,
            prerelease=prerelease,
            protobuf_implementation=protobuf_implementation,
            working_dir=working_dir
        )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
@nox.parametrize("protobuf_implementation", ["python", "upb", "cpp"])
def tests_local(session, protobuf_implementation):
    """Run tests in this local repo."""
    # Install all test dependencies, then install this package in-place.

    # TODO(https://github.com/googleapis/proto-plus-python/issues/389):
    # Remove the 'cpp' implementation once support for Protobuf 3.x is dropped.
    # The 'cpp' implementation requires Protobuf == 3.x however version 3.x
    # does not support Python 3.11 and newer. The 'cpp' implementation
    # must be excluded from the test matrix for these runtimes.
    if protobuf_implementation == "cpp" and session.python in ("3.11", "3.12"):
        session.skip("cpp implementation is not supported in python 3.11+")

    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    session.install(
        "mock",
        "asyncmock",
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "-c",
        constraints_path,
    )

    session.install("-e", ".", "-c", constraints_path)

    # Remove the 'cpp' implementation once support for Protobuf 3.x is dropped.
    # The 'cpp' implementation requires Protobuf<4.
    if protobuf_implementation == "cpp":
        session.install("protobuf<4")

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=google",
        "--cov=tests/unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        *session.posargs,
        env={
            "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": protobuf_implementation,
        },
    )


@nox.session(python="3.8")
def generate_protos(session):
    """Generates the protos using protoc.

    This session but be last to avoid overwriting the protos used in CI runs.

    Some notes on the `google` directory:
    1. The `_pb2.py` files are produced by protoc.
    2. The .proto files are non-functional but are left in the repository
       to make it easier to understand diffs.
    3. The `google` directory also has `__init__.py` files to create proper modules.
       If a new subdirectory is added, you will need to create more `__init__.py`
       files.
    """
    # longrunning operations directory is non-standard for backwards compatibility
    # see comments in directory for details
    # Temporarily rename the operations_pb2.py to keep it from getting overwritten
    os.replace(
        "google/longrunning/operations_pb2.py",
        "google/longrunning/operations_pb2-COPY.py",
    )

    session.install(GRPCIO_TOOLS_VERSION)
    protos = [str(p) for p in (Path(".").glob("google/**/*.proto"))]
    session.run(
        "python", "-m", "grpc_tools.protoc", "--proto_path=.", "--python_out=.", *protos
    )

    # Some files contain service definitions for which `_pb2_grpc.py` files must be generated.
    service_protos = ["google/longrunning/operations.proto"]
    session.run(
        "python",
        "-m",
        "grpc_tools.protoc",
        "--proto_path=.",
        "--grpc_python_out=.",
        *service_protos,
    )

    # More LRO non-standard fixes: rename the file and fix the import statement
    operations_grpc_py = Path("google/longrunning/operations_pb2_grpc.py")
    file_contents = operations_grpc_py.read_text()
    file_contents = file_contents.replace("operations_pb2", "operations_proto_pb2")
    operations_grpc_py.write_text(file_contents)

    # Clean up LRO directory
    os.replace(
        "google/longrunning/operations_pb2.py",
        "google/longrunning/operations_proto_pb2.py",
    )
    os.replace(
        "google/longrunning/operations_pb2-COPY.py",
        "google/longrunning/operations_pb2.py",
    )
