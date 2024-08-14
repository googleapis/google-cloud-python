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


nox.options.sessions = [
    "unit",
    "blacken",
    "lint_setup_py",
]

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

BLACK_VERSION = "black==19.3b0"

CURRENT_DIRECTORY = Path(__file__).parent.absolute()

DEFAULT_PYTHON_VERSION = "3.8"

UNIT_TEST_PYTHON_VERSIONS = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]

# NOTE: Pin the version of grpcio-tools to 1.48.2 for compatibility with 
# Protobuf 3.19.5. Please ensure that the minimum required version of 
# protobuf in setup.py is compatible with the pb2 files generated
# by grpcio-tools before changing the pinned version below.
GRPCIO_TOOLS_VERSION = "grpcio-tools==1.48.2"


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black.
    Format code to uniform standard.
    """
    session.install(BLACK_VERSION, "click<8.1.0")
    session.run("black", "google", "setup.py")



@nox.session(python=DEFAULT_PYTHON_VERSION)
def generate_protos(session):
    """Generates the protos using protoc.
    Some notes on the `google` directory:
    1. The `_pb2.py` files are produced by protoc.
    2. The .proto files are non-functional but are left in the repository
       to make it easier to understand diffs.
    3. The `google` directory also has `__init__.py` files to create proper modules.
       If a new subdirectory is added, you will need to create more `__init__.py`
       files.
    NOTE: This should be migrated to use bazel in the future.
    """
    session.install(GRPCIO_TOOLS_VERSION)
    protos = [str(p) for p in (Path(".").glob("google/**/*.proto"))]

    session.run(
        "python",
        "-m",
        "grpc_tools.protoc",
        "--proto_path=.",
        "--python_out=.",
        *protos,
    )

@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid"""
    session.install("docutils", "pygments")
    session.run("python", "setup.py", "check", "--strict")


def default(session):
    # Install all test dependencies, then install this package in-place.
    session.install("mock", "pytest", "pytest-cov")

    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    session.install("-e", ".", "-c", constraints_path)

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        "--cov=google",
        "--cov=tests.unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        *session.posargs,
    )

@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run the unit test suite."""
    default(session)
