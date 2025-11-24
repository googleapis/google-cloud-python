# Copyright 2017, Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import nox
import pathlib


CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()


PYTHON_VERSIONS = [
    "3.7",
    "3.8",
    "3.9",
    "3.10",
    "pypy3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
]

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize("implementation", ["cpp", "upb", "python"])
def unit(session, implementation):
    """Run the unit test suite."""

    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    session.env["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = implementation
    session.install("coverage", "pytest", "pytest-cov", "pytz")
    session.install("-e", ".[testing]", "-c", constraints_path)
    # TODO(https://github.com/googleapis/proto-plus-python/issues/389):
    # Remove the 'cpp' implementation once support for Protobuf 3.x is dropped.
    # The 'cpp' implementation requires Protobuf<4.
    if implementation == "cpp":
        session.install("protobuf<4")

    # TODO(https://github.com/googleapis/proto-plus-python/issues/403): re-enable `-W=error`
    # The warnings-as-errors flag `-W=error` was removed in
    # https://github.com/googleapis/proto-plus-python/pull/400.
    # It should be re-added once issue
    # https://github.com/protocolbuffers/protobuf/issues/15077 is fixed.
    session.run(
        "pytest",
        "--quiet",
        *(
            session.posargs  # Coverage info when running individual tests is annoying.
            or [
                "--cov=proto",
                "--cov-config=.coveragerc",
                "--cov-report=term",
                "--cov-report=html",
                "tests",
            ]
        ),
    )


# Only test upb and python implementation backends.
# As of protobuf 4.x, the "ccp" implementation is not available in the PyPI package as per
# https://github.com/protocolbuffers/protobuf/tree/main/python#implementation-backends
@nox.session(python=PYTHON_VERSIONS[-1])
@nox.parametrize("implementation", ["python", "upb"])
def prerelease_deps(session, implementation):
    """Run the unit test suite against pre-release versions of dependencies."""

    session.env["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = implementation

    # Install test environment dependencies
    session.install("coverage", "pytest", "pytest-cov", "pytz")

    # Install the package without dependencies
    session.install("-e", ".", "--no-deps")

    prerel_deps = [
        "google-api-core",
        # dependency of google-api-core
        "googleapis-common-protos",
    ]

    for dep in prerel_deps:
        session.install("--pre", "--no-deps", "--upgrade", dep)

    session.install("--pre", "--upgrade", "protobuf")
    # Print out prerelease package versions
    session.run(
        "python", "-c", "import google.protobuf; print(google.protobuf.__version__)"
    )
    session.run(
        "python", "-c", "import google.api_core; print(google.api_core.__version__)"
    )

    # TODO(https://github.com/googleapis/proto-plus-python/issues/403): re-enable `-W=error`
    # The warnings-as-errors flag `-W=error` was removed in
    # https://github.com/googleapis/proto-plus-python/pull/400.
    # It should be re-added once issue
    # https://github.com/protocolbuffers/protobuf/issues/15077 is fixed.
    session.run(
        "pytest",
        "--quiet",
        *(
            session.posargs  # Coverage info when running individual tests is annoying.
            or [
                "--cov=proto",
                "--cov-config=.coveragerc",
                "--cov-report=term",
                "--cov-report=html",
                "tests",
            ]
        ),
    )


@nox.session(python="3.10")
def docs(session):
    """Build the docs."""

    session.install(
        # We need to pin to specific versions of the `sphinxcontrib-*` packages
        # which still support sphinx 4.x.
        # See https://github.com/googleapis/sphinx-docfx-yaml/issues/344
        # and https://github.com/googleapis/sphinx-docfx-yaml/issues/345.
        "sphinxcontrib-applehelp==1.0.4",
        "sphinxcontrib-devhelp==1.0.2",
        "sphinxcontrib-htmlhelp==2.0.1",
        "sphinxcontrib-qthelp==1.0.3",
        "sphinxcontrib-serializinghtml==1.1.5",
        "sphinx==4.5.0",
        "sphinx_rtd_theme",
    )
    session.install(".")

    # Build the docs!
    session.run("rm", "-rf", "docs/_build/")
    session.run(
        "sphinx-build",
        "-W",
        "-b",
        "html",
        "-d",
        "docs/_build/doctrees",
        "docs/",
        "docs/_build/html/",
    )


@nox.session(python="3.10")
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""

    session.install("docutils", "Pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")
