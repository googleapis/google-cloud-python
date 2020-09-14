# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd


from __future__ import absolute_import

import nox
import os
import shutil


BLACK_VERSION = "black==19.10b0"
BLACK_PATHS = [
    "django_spanner",
    "docs",
    "google",
    "tests",
    "noxfile.py",
    "setup.py",
]


@nox.session(python="3.8")
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION)
    session.run("black", "--check", *BLACK_PATHS)
    session.run("flake8", "django_spanner", "google", "tests")


@nox.session(python="3.8")
def blacken(session):
    """Run black.

    Format code to uniform standard.

    This currently uses Python 3.6 due to the automated Kokoro run of synthtool.
    That run uses an image that doesn't have 3.6 installed. Before updating this
    check the state of the `gcp_ubuntu_config` we use for that Kokoro run.
    """
    session.install(BLACK_VERSION)
    session.run("black", *BLACK_PATHS)


@nox.session(python="3.8")
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "pygments")
    session.run(
        "python", "setup.py", "check", "--restructuredtext", "--strict"
    )


def default(session):
    # Install all test dependencies, then install this package in-place.
    session.install("mock", "pytest", "pytest-cov")
    session.install("-e", ".")

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        "--cov=django_spanner",
        "--cov=google.cloud",
        "--cov=tests.spanner_dbapi",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "spanner_dbapi"),
        *session.posargs
    )


@nox.session(python=["3.5", "3.6", "3.7", "3.8"])
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python="3.8")
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

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    session.install("mock", "pytest", "google-cloud-testutils")
    session.install("-e", ".")

    # Run py.test against the system tests.
    if system_test_exists:
        session.run("py.test", "--quiet", system_test_path, *session.posargs)
    if system_test_folder_exists:
        session.run(
            "py.test", "--quiet", system_test_folder_path, *session.posargs
        )


@nox.session(python="3.8")
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=40")
    session.run("coverage", "erase")


@nox.session(python="3.8")
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
