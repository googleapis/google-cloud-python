# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pathlib
import re
import shutil

import nox

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

CLICK_VERSION = "click"
BLACK_VERSION = "black==23.7.0"
RUFF_VERSION = "ruff==0.14.14"
BLACK_PATHS = [
    "google",
    "tests",
    "tests_async",
    "noxfile.py",
    "setup.py",
    "docs/conf.py",
]

DEFAULT_PYTHON_VERSION = "3.14"

# TODO(https://github.com/googleapis/gapic-generator-python/issues/2450):
# Switch this to Python 3.15 alpha1
# https://peps.python.org/pep-0790/
PREVIEW_PYTHON_VERSION = "3.14"

UNIT_TEST_PYTHON_VERSIONS = [
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
]
ALL_PYTHON = UNIT_TEST_PYTHON_VERSIONS.copy()

UNIT_TEST_STANDARD_DEPENDENCIES = [
    "mock",
    "asyncmock",
    "pytest",
    "pytest-cov",
    "pytest-asyncio",
]
UNIT_TEST_EXTERNAL_DEPENDENCIES: list[str] = []

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

# pypy will be run as a github action instead of through Kokoro
nox.options.sessions = [
    "lint",
    "blacken",
    "format",
    "mypy",
    # cover must be last to avoid error `No data to report`
    "docs",
]


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    session.install(
        "flake8", "flake8-import-order", "docutils", CLICK_VERSION, BLACK_VERSION
    )
    session.install("-e", ".")
    session.run("black", "--check", *BLACK_PATHS)
    session.run(
        "flake8",
        "--import-order-style=google",
        "--application-import-names=google,tests,system_tests",
        "google",
        "tests",
        "tests_async",
    )
    session.run(
        "python", "setup.py", "check", "--metadata", "--restructuredtext", "--strict"
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("setuptools", "docutils", "pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black.
    Format code to uniform standard.
    The Python version should be consistent with what is
    supplied in the Python Owlbot postprocessor.

    https://github.com/googleapis/synthtool/blob/master/docker/owlbot/python/Dockerfile
    """
    session.install(CLICK_VERSION, BLACK_VERSION)
    session.run("black", *BLACK_PATHS)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def format(session):
    """
    Run ruff to sort imports and format code.
    """
    # 1. Install ruff (skipped automatically if you run with --no-venv)
    session.install(RUFF_VERSION)

    # 2. Run Ruff to fix imports
    session.run(
        "ruff",
        "check",
        "--select",
        "I",
        "--fix",
        f"--target-version=py{UNIT_TEST_PYTHON_VERSIONS[0].replace('.', '')}",
        "--line-length=88",
        *BLACK_PATHS,
    )

    # 3. Run Ruff to format code
    session.run(
        "ruff",
        "format",
        f"--target-version=py{ALL_PYTHON[0].replace('.', '')}",
        "--line-length=88",
        *BLACK_PATHS,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Verify type hints are mypy compatible."""
    session.install("-e", ".[aiohttp,rsa]")
    session.install(
        "mypy",
        "types-certifi",
        "types-freezegun",
        "types-pyOpenSSL",
        "types-requests",
        "types-setuptools",
        "types-mock",
        "pytest<8.0.0",
    )
    session.run("mypy", "-p", "google", "-p", "tests", "-p", "tests_async")


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
@nox.parametrize(["install_deprecated_extras"], (True, False))
def unit(session, install_deprecated_extras):
    # Install all test dependencies, then install this package in-place.

    min_py, max_py = UNIT_TEST_PYTHON_VERSIONS[0], UNIT_TEST_PYTHON_VERSIONS[-1]
    if not install_deprecated_extras and session.python not in (min_py, max_py):
        # only run double tests on first and last supported versions
        session.skip(
            f"Extended tests only run on boundary Python versions ({min_py}, {max_py}) to reduce CI load."
        )

    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    extras_str = "testing"
    if install_deprecated_extras:
        # rsa and oauth2client were both archived and support dropped,
        # but we still  test old code paths
        session.install("oauth2client")
        extras_str += ",rsa"
    session.install("-e", f".[{extras_str}]", "-c", constraints_path)
    session.run(
        "pytest",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov-append",
        "--cov=google.auth",
        "--cov=google.oauth2",
        "--cov=tests",
        "--cov-report=term-missing",
        "tests",
        "tests_async",
        *session.posargs,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")
    session.run("coverage", "erase")


@nox.session(python="3.10")
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".[aiohttp]")
    session.install("requests==2.31.0")
    session.install("sphinx", "alabaster", "recommonmark", "sphinx-docstring-typing")

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-T",  # show full traceback on exception
        "-W",  # warnings as errors
        "-N",  # no colors
        "-b",
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "html", ""),
    )


@nox.session(python="3.10")
def docfx(session):
    """Build the docfx yaml files for this library."""
    session.skip("This package does not have documentation in cloud.google.com")

@nox.session(python=PREVIEW_PYTHON_VERSION)
@nox.parametrize(
    "protobuf_implementation",
    ["python", "upb"],
)
def prerelease_deps(session, protobuf_implementation):
    """
    Run all tests with pre-release versions of dependencies installed
    rather than the standard non pre-release versions.
    Pre-release versions can be installed using
    `pip install --pre <package>`.
    """

    # Install all dependencies
    session.install("-e", ".[testing,rsa]")
    session.install("oauth2client")

    # Install dependencies for the unit test environment
    unit_deps_all = UNIT_TEST_STANDARD_DEPENDENCIES + UNIT_TEST_EXTERNAL_DEPENDENCIES
    session.install(*unit_deps_all)

    # Because we test minimum dependency versions on the minimum Python
    # version, the first version we test with in the unit tests sessions has a
    # constraints file containing all dependencies and extras.
    with open(
        CURRENT_DIRECTORY / "testing" / f"constraints-{ALL_PYTHON[0]}.txt",
        encoding="utf-8",
    ) as constraints_file:
        constraints_text = constraints_file.read()

    # Ignore leading whitespace and comment lines.
    constraints_deps = [
        match.group(1)
        for match in re.finditer(
            r"^\s*(\S+)(?===\S+)", constraints_text, flags=re.MULTILINE
        )
    ]

    # Install dependencies specified in `testing/constraints-X.txt`.
    session.install(*constraints_deps)

    # Note: If a dependency is added to the `prerel_deps` list,
    # the `core_dependencies_from_source` list in the `core_deps_from_source`
    # nox session should also be updated.
    prerel_deps = [
        "cryptography>=38.0.3",
        "pyasn1-modules>=0.2.1",
        "requests>=2.20.0,<3.0.0",
        "aiohttp>=3.8.0,<3.10.0", 
        "urllib3",
        "pyjwt>=2.0",
        "pyopenssl<24.3.0",
        "rsa>=3.1.4,<5",
        "grpcio>=1.75.1" if session.python >= "3.12" else "grpcio<=1.62.2",
    ]

    for dep in prerel_deps:
        session.install("--pre", "--no-deps", "--ignore-installed", dep)
        print(f"Installed {dep}")

    session.run(
        "py.test",
        "tests",
        "tests_async",
        env={
            "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": protobuf_implementation,
        },
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
@nox.parametrize(
    "protobuf_implementation",
    ["python", "upb"],
)
def core_deps_from_source(session, protobuf_implementation):
    """Run all tests with core dependencies installed from source
    rather than pulling the dependencies from PyPI.
    """

    # Install all dependencies
    session.install("-e", ".[testing,rsa]")
    session.install("oauth2client")

    # Install dependencies for the unit test environment
    unit_deps_all = UNIT_TEST_STANDARD_DEPENDENCIES + UNIT_TEST_EXTERNAL_DEPENDENCIES
    session.install(*unit_deps_all)

    # Because we test minimum dependency versions on the minimum Python
    # version, the first version we test with in the unit tests sessions has a
    # constraints file containing all dependencies and extras.
    with open(
        CURRENT_DIRECTORY
        / "testing"
        / f"constraints-{UNIT_TEST_PYTHON_VERSIONS[0]}.txt",
        encoding="utf-8",
    ) as constraints_file:
        constraints_text = constraints_file.read()

    # Ignore leading whitespace and comment lines.
    constraints_deps = [
        match.group(1)
        for match in re.finditer(
            r"^\s*(\S+)(?===\S+)", constraints_text, flags=re.MULTILINE
        )
    ]

    # Install dependencies specified in `testing/constraints-X.txt`.
    session.install(*constraints_deps)

    # TODO(https://github.com/googleapis/gapic-generator-python/issues/2358): `grpcio` and
    # `grpcio-status` should be added to the list below so that they are installed from source,
    # rather than PyPI.
    # TODO(https://github.com/googleapis/gapic-generator-python/issues/2357): `protobuf` should be
    # added to the list below so that it is installed from source, rather than PyPI
    # Note: If a dependency is added to the `core_dependencies_from_source` list,
    # the `prerel_deps` list in the `prerelease_deps` nox session should also be updated.
    core_dependencies_from_source = [
        "googleapis-common-protos @ git+https://github.com/googleapis/google-cloud-python#egg=googleapis-common-protos&subdirectory=packages/googleapis-common-protos",
        "google-api-core @ git+https://github.com/googleapis/google-cloud-python#egg=google-api-core&subdirectory=packages/google-api-core",
        "grpc-google-iam-v1 @ git+https://github.com/googleapis/google-cloud-python#egg=grpc-google-iam-v1&subdirectory=packages/grpc-google-iam-v1",
        "proto-plus @ git+https://github.com/googleapis/google-cloud-python#egg=proto-plus&subdirectory=packages/proto-plus",
    ]

    for dep in core_dependencies_from_source:
        session.install(dep, "--no-deps", "--ignore-installed")
        print(f"Installed {dep}")

    session.run(
        "py.test",
        "tests",
        "tests_async",
        env={
            "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": protobuf_implementation,
        },
    )
