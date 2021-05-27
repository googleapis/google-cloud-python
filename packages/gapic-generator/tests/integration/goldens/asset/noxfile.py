# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import shutil
import subprocess
import sys


import nox  # type: ignore

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

LOWER_BOUND_CONSTRAINTS_FILE = CURRENT_DIRECTORY / "constraints.txt"
PACKAGE_NAME = subprocess.check_output([sys.executable, "setup.py", "--name"], encoding="utf-8")


nox.sessions = [
    "unit",
    "cover",
    "mypy",
    "check_lower_bounds"
    # exclude update_lower_bounds from default
    "docs",
]

@nox.session(python=['3.6', '3.7', '3.8', '3.9'])
def unit(session):
    """Run the unit test suite."""

    session.install('coverage', 'pytest', 'pytest-cov', 'asyncmock', 'pytest-asyncio')
    session.install('-e', '.')

    session.run(
        'py.test',
        '--quiet',
        '--cov=google/cloud/asset_v1/',
        '--cov-config=.coveragerc',
        '--cov-report=term',
        '--cov-report=html',
        os.path.join('tests', 'unit', ''.join(session.posargs))
    )


@nox.session(python='3.7')
def cover(session):
    """Run the final coverage report.
    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")

    session.run("coverage", "erase")


@nox.session(python=['3.6', '3.7'])
def mypy(session):
    """Run the type checker."""
    session.install('mypy')
    session.install('.')
    session.run(
        'mypy',
        '--explicit-package-bases',
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

@nox.session(python='3.6')
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".")
    session.install("sphinx<3.0.0", "alabaster", "recommonmark")

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
