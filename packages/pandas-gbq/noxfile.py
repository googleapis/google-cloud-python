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


supported_pythons = ["3.7", "3.8"]
system_test_pythons = ["3.7", "3.8"]
latest_python = "3.8"

# Use a consistent version of black so CI is deterministic.
# Should match Stickler: https://stickler-ci.com/docs#black
black_package = "black==20.8b1"


@nox.session(python=latest_python)
def lint(session):
    session.install(black_package, "flake8")
    session.run("flake8", "pandas_gbq")
    session.run("flake8", "tests")
    session.run("black", "--check", ".")


@nox.session(python=latest_python)
def blacken(session):
    session.install(black_package)
    session.run("black", ".")


@nox.session(python=supported_pythons)
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
        *session.posargs
    )


@nox.session(python=latest_python)
def cover(session):
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=73")
    session.run("coverage", "erase")


@nox.session(python=latest_python)
def docs(session):
    """Build the docs."""

    session.install("-r", os.path.join("docs", "requirements-docs.txt"))
    session.install("-e", ".")

    shutil.rmtree(os.path.join("docs", "source", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-W",  # warnings as errors
        "-T",  # show full traceback on exception
        "-N",  # no colors
        "-b",
        "html",
        "-d",
        os.path.join("docs", "source", "_build", "doctrees", ""),
        os.path.join("docs", "source", ""),
        os.path.join("docs", "source", "_build", "html", ""),
    )


@nox.session(python=system_test_pythons)
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
        os.path.join(".", "samples", "tests"),
        "-v",
        *additional_args
    )
