# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
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
import shutil

import nox


LOCAL_DEPS = (os.path.join("..", "api_core"), os.path.join("..", "core"))

@nox.session(python="3.7")
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", "black", *LOCAL_DEPS)
    session.run(
        "black",
        "--check",
        "google",
        "tests",
        "docs",
    )
    session.run("flake8", "google", "tests")


@nox.session(python="3.6")
def blacken(session):
    """Run black.

    Format code to uniform standard.
    
    This currently uses Python 3.6 due to the automated Kokoro run of synthtool.
    That run uses an image that doesn't have 3.6 installed. Before updating this
    check the state of the `gcp_ubuntu_config` we use for that Kokoro run.
    """
    session.install("black")
    session.run(
        "black",
        "google",
        "tests",
        "docs",
    )


@nox.session(python="3.7")
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


def default(session):
    # Install all test dependencies, then install this package in-place.
    session.install("mock", "pytest", "pytest-cov")
    for local_dep in LOCAL_DEPS:
        session.install("-e", local_dep)
    session.install("-e", ".")

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        "--cov=google.cloud",
        "--cov=tests.unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=97",
        os.path.join("tests", "unit"),
        *session.posargs,
    )


@nox.session(python=["2.7", "3.5", "3.6", "3.7"])
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python=["2.7", "3.7"])
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
    session.install("mock", "pytest")
    for local_dep in LOCAL_DEPS:
        session.install("-e", local_dep)
    session.install("-e", "../test_utils/")
    session.install("-e", ".")

    # Additional setup for VPCSC system tests
    if os.environ.get("GOOGLE_CLOUD_TESTS_IN_VPCSC") != "true":
        # Unset PROJECT_ID, since VPCSC system tests expect this to be a project
        # within the VPCSC perimeter.
        env = {
            "PROJECT_ID": "",
            "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT": os.environ.get("PROJECT_ID"),
        }

    # Run py.test against the system tests.
    if system_test_exists:
        session.run("py.test", "--quiet", system_test_path, env=env, *session.posargs)
    if system_test_folder_exists:
        session.run("py.test", "--quiet", system_test_folder_path, env=env, *session.posargs)


@nox.session(python="3.7")
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=97")

    session.run("coverage", "erase")

@nox.session(python="3.7")
def docs(session):
    """Build the docs for this library."""

    session.install('-e', '.')
    session.install('sphinx', 'alabaster', 'recommonmark')

    shutil.rmtree(os.path.join('docs', '_build'), ignore_errors=True)
    session.run(
        'sphinx-build',
        '-W',  # warnings as errors
        '-T',  # show full traceback on exception
        '-N',  # no colors
        '-b', 'html',
        '-d', os.path.join('docs', '_build', 'doctrees', ''),
        os.path.join('docs', ''),
        os.path.join('docs', '_build', 'html', ''),
    )
