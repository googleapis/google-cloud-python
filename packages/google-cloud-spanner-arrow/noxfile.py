# Copyright 2026 Google LLC
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
import sys
import nox

HERE = os.path.dirname(__file__)

DEFAULT_PYTHON_VERSION = "3.12"
UNIT_TEST_PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13", "3.14"]
ALL_PYTHON = list(UNIT_TEST_PYTHON_VERSIONS)

FLAKE8_VERSION = "flake8==6.1.0"
BLACK_VERSION = "black[jupyter]==23.7.0"
RUFF_VERSION = "ruff==0.14.14"
ISORT_VERSION = "isort==5.11.0"
LINT_PATHS = ["src", "tests", "noxfile.py", "setup.py"]

nox.options.sessions = [
    "check",
    "lint",
    "blacken",
    "format",
    "lint_setup_py",
    "mypy",
    "unit",
]


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def check(session):
    """Run tests against built wheels."""
    session.install("pytest", "pyarrow>=14.0.0")
    session.install("--no-index", f"--find-links={HERE}/wheels", "google-cloud-spanner-arrow")
    session.run("pytest", "tests")
    session.run("python", f"{HERE}/scripts/check_spanner_arrow_extension.py", *session.posargs)


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run all unit tests."""
    session.install("pytest", "pyarrow>=14.0.0", "protobuf")
    session.install("-e", ".")
    session.run("pytest", "tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Verify type hints are mypy compatible."""
    session.install(
        "mypy",
        "types-mock",
        "types-setuptools",
        "pyarrow",
    )
    session.env["MYPYPATH"] = "src"
    session.run("mypy", "src/google_cloud_spanner_arrow/", "tests/")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters."""
    session.install(FLAKE8_VERSION, BLACK_VERSION)
    session.run(
        "black",
        "--check",
        *LINT_PATHS,
    )
    session.run("flake8", *LINT_PATHS)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black formatting."""
    session.install(BLACK_VERSION)
    session.run(
        "black",
        *LINT_PATHS,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def format(session):
    """Run ruff to sort imports and format code."""
    session.install(RUFF_VERSION)
    session.run(
        "ruff",
        "check",
        "--select",
        "I",
        "--fix",
        "--line-length=88",
        *LINT_PATHS,
    )
    session.run(
        "ruff",
        "format",
        "--line-length=88",
        *LINT_PATHS,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify setup.py validity."""
    session.install("docutils", "pygments", "setuptools")
    session.run("python", "setup.py", "check", "--strict")
