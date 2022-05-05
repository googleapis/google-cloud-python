# -*- coding: utf-8 -*-
#
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


from __future__ import absolute_import
import os
import pathlib
import shutil

import nox

# 'update_lower_bounds' is excluded 
nox.options.sessions = [
    "lint",
    "blacken",
    "lint_setup_py",
    "mypy",
    "unit",
    "check_lower_bounds"
]


# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

BLACK_VERSION = "black==19.3b0"
BLACK_PATHS = ["test_utils", "setup.py"]
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()


@nox.session(python="3.8")
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION, "click<8.1.0")
    session.run(
        "black", "--check", *BLACK_PATHS,
    )
    session.run("flake8", *BLACK_PATHS)


@nox.session(python="3.8")
def blacken(session):
    """Run black.

    Format code to uniform standard.

    This currently uses Python 3.6 due to the automated Kokoro run of synthtool.
    That run uses an image that doesn't have 3.6 installed. Before updating this
    check the state of the `gcp_ubuntu_config` we use for that Kokoro run.
    """
    session.install(BLACK_VERSION, "click<8.1.0")
    session.run(
        "black", *BLACK_PATHS,
    )


@nox.session(python="3.8")
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python="3.8")
def mypy(session):
    """Verify type hints are mypy compatible."""
    session.install("-e", ".")
    session.install(
        "mypy",
        "types-mock",
        "types-setuptools",
    )
    session.run("mypy", "test_utils/", "tests/")


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10"])
def unit(session):
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Install two fake packages for the lower-bound-checker tests
    session.install("-e", "tests/unit/resources/good_package", "tests/unit/resources/bad_package")

    session.install("pytest", "pytest-cov")
    session.install("-e", ".", "-c", constraints_path)

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=test_utils",
        "--cov=tests/unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        *session.posargs,
    )

@nox.session(python="3.8")
def check_lower_bounds(session):
    """Check lower bounds in setup.py are reflected in constraints file"""
    session.install(".")
    session.run(
        "lower-bound-checker",
        "check",
        "--package-name",
        "google-cloud-testutils",
        "--constraints-file",
        "testing/constraints-3.6.txt",
    )


@nox.session(python="3.8")
def update_lower_bounds(session):
    """Update lower bounds in constraints.txt to match setup.py"""
    session.install(".")
    session.run(
        "lower-bound-checker",
        "update",
        "--package-name",
        "google-cloud-testutils",
        "--constraints-file",
        "testing/constraints-3.6.txt",
    )
