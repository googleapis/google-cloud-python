# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
#
import os
import pathlib
import re
import shutil
import subprocess
import sys


import nox  # type: ignore

ALL_PYTHON = [
    "3.7",
    "3.8",
    "3.9",
    "3.10",
    "3.11",
    "3.12"
]

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

LOWER_BOUND_CONSTRAINTS_FILE = CURRENT_DIRECTORY / "constraints.txt"
PACKAGE_NAME = 'google-cloud-redis'

BLACK_VERSION = "black==22.3.0"
BLACK_PATHS = ["docs", "google", "tests", "samples", "noxfile.py", "setup.py"]
DEFAULT_PYTHON_VERSION = "3.12"

nox.sessions = [
    "unit",
    "cover",
    "mypy",
    "check_lower_bounds"
    # exclude update_lower_bounds from default
    "docs",
    "blacken",
    "lint",
    "prerelease_deps",
]

@nox.session(python=ALL_PYTHON)
def unit(session):
    """Run the unit test suite."""

    session.install('coverage', 'pytest', 'pytest-cov', 'pytest-asyncio', 'asyncmock; python_version < "3.8"')
    session.install('-e', '.')

    session.run(
        'py.test',
        '--quiet',
        '--cov=google/cloud/redis_v1/',
        '--cov=tests/',
        '--cov-config=.coveragerc',
        '--cov-report=term',
        '--cov-report=html',
        os.path.join('tests', 'unit', ''.join(session.posargs))
    )

@nox.session(python=ALL_PYTHON[-1])
def prerelease_deps(session):
    """Run the unit test suite against pre-release versions of dependencies."""

    # Install test environment dependencies
    session.install('coverage', 'pytest', 'pytest-cov', 'pytest-asyncio', 'asyncmock; python_version < "3.8"')

    # Install the package without dependencies
    session.install('-e', '.', '--no-deps')

    # We test the minimum dependency versions using the minimum Python
    # version so the lowest python runtime that we test has a corresponding constraints
    # file, located at `testing/constraints-<version>-.txt`,  which contains all of the
    # dependencies and extras.
    with open(
        CURRENT_DIRECTORY
        / "testing"
        / f"constraints-{ALL_PYTHON[0]}.txt",
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

    session.install(*constraints_deps)

    prerel_deps = [
        "googleapis-common-protos",
        "google-api-core",
        "google-auth",
        "grpcio",
        "grpcio-status",
        "protobuf",
        "proto-plus",
    ]

    for dep in prerel_deps:
        session.install("--pre", "--no-deps", "--upgrade", dep)

    # Remaining dependencies
    other_deps = [
        "requests",
    ]
    session.install(*other_deps)

    # Print out prerelease package versions

    session.run("python", "-c", "import google.api_core; print(google.api_core.__version__)")
    session.run("python", "-c", "import google.auth; print(google.auth.__version__)")
    session.run("python", "-c", "import grpc; print(grpc.__version__)")
    session.run(
        "python", "-c", "import google.protobuf; print(google.protobuf.__version__)"
    )
    session.run(
        "python", "-c", "import proto; print(proto.__version__)"
    )

    session.run(
        'py.test',
        '--quiet',
        '--cov=google/cloud/redis_v1/',
        '--cov=tests/',
        '--cov-config=.coveragerc',
        '--cov-report=term',
        '--cov-report=html',
        os.path.join('tests', 'unit', ''.join(session.posargs))
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


@nox.session(python=ALL_PYTHON)
def mypy(session):
    """Run the type checker."""
    session.install(
        'mypy',
        'types-requests',
        'types-protobuf'
    )
    session.install('.')
    session.run(
        'mypy',
        '-p',
        'google',
    )


@nox.session
def update_lower_bounds(session):
    """Update lower bounds in constraints.txt to match setup.py"""
    session.install('google-cloud-testutils')
    session.install('.')

    session.run(
        'lower-bound-checker',
        'update',
        '--package-name',
        PACKAGE_NAME,
        '--constraints-file',
        str(LOWER_BOUND_CONSTRAINTS_FILE),
    )


@nox.session
def check_lower_bounds(session):
    """Check lower bounds in setup.py are reflected in constraints file"""
    session.install('google-cloud-testutils')
    session.install('.')

    session.run(
        'lower-bound-checker',
        'check',
        '--package-name',
        PACKAGE_NAME,
        '--constraints-file',
        str(LOWER_BOUND_CONSTRAINTS_FILE),
    )

@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".")
    session.install("sphinx==7.0.1", "alabaster", "recommonmark")

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-W",  # warnings as errors
        "-T",  # show full traceback on exception
        "-N",  # no colors
        "-b",
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "html", ""),
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION)
    session.run(
        "black",
        "--check",
        *BLACK_PATHS,
    )
    session.run("flake8", "google", "tests", "samples")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black. Format code to uniform standard."""
    session.install(BLACK_VERSION)
    session.run(
        "black",
        *BLACK_PATHS,
    )
