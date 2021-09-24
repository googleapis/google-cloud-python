# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Nox test automation configuration.

See: https://nox.readthedocs.io/en/latest/
"""

import os
import os.path
import shutil

import nox


BLACK_VERSION = "black==19.10b0"
BLACK_PATHS = ["docs", "pandas_gbq", "tests", "noxfile.py", "setup.py"]

DEFAULT_PYTHON_VERSION = "3.8"
SYSTEM_TEST_PYTHON_VERSIONS = ["3.8"]
UNIT_TEST_PYTHON_VERSIONS = ["3.7", "3.8", "3.9"]


# Error if a python version is missing
nox.options.error_on_missing_interpreters = True


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.
    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION)
    session.run(
        "black", "--check", *BLACK_PATHS,
    )
    session.run("flake8", "pandas_gbq", "tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black. Format code to uniform standard."""
    session.install(BLACK_VERSION)
    session.run(
        "black", *BLACK_PATHS,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    session.install("pytest", "pytest-cov")
    session.install(
        "-e",
        ".",
        # Use dependencies versions from constraints file. This enables testing
        # across a more full range of versions of the dependencies.
        "-c",
        os.path.join(".", "ci", "constraints-{}.pip".format(session.python)),
    )
    session.run(
        "pytest",
        os.path.join(".", "tests", "unit"),
        "-v",
        "--cov=pandas_gbq",
        "--cov=tests.unit",
        "--cov-report",
        "xml:/tmp/pytest-cov.xml",
        *session.posargs,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cover(session):
    """Run the final coverage report.
    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=73")

    session.run("coverage", "erase")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".")
    session.install("sphinx==4.0.1", "alabaster", "recommonmark")

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


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def system(session):
    session.install("pytest", "pytest-cov")
    session.install(
        "-e",
        ".",
        # Use dependencies versions from constraints file. This enables testing
        # across a more full range of versions of the dependencies.
        "-c",
        os.path.join(".", "ci", "constraints-{}.pip".format(session.python)),
    )

    # Skip local auth tests on CI.
    additional_args = list(session.posargs)
    if "CIRCLECI" in os.environ:
        additional_args = additional_args + ["-m", "not local_auth"]

    session.run(
        "pytest",
        os.path.join(".", "tests", "system"),
        os.path.join(".", "samples", "snippets"),
        "-v",
        *additional_args,
    )
