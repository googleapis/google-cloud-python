# Copyright 2016 Google LLC
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
import os

# https://github.com/google/importlab/issues/25
import nox  # pytype: disable=import-error


def default(session):
    """Default unit test session.

    This is intended to be run **without** an interpreter set, so
    that the current ``python`` (on the ``PATH``) or the version of
    Python corresponding to the ``nox`` binary the ``PATH`` can
    run the tests.
    """
    # Install all test dependencies, then install this package in-place.
    session.install("mock", "pytest", "pytest-cov", "grpcio >= 1.0.2")
    session.install("-e", ".")

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        "--cov=google.api_core",
        "--cov=tests.unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=97",
        os.path.join("tests", "unit"),
        *session.posargs
    )


@nox.session(python=["2.7", "3.5", "3.6", "3.7"])
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python=["2.7", "3.5", "3.6", "3.7"])
def unit_grpc_gcp(session):
    """Run the unit test suite with grpcio-gcp installed."""

    # Install grpcio-gcp
    session.install("grpcio-gcp")

    default(session)


@nox.session(python="3.6")
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", "flake8-import-order")
    session.install(".")
    session.run("flake8", "google", "tests")


@nox.session(python="3.6")
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""

    session.install("docutils", "Pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


# No 2.7 due to https://github.com/google/importlab/issues/26.
# No 3.7 because pytype supports up to 3.6 only.
@nox.session(python="3.6")
def pytype(session):
    """Run type-checking."""
    session.install(
        ".", "grpcio >= 1.8.2", "grpcio-gcp >= 0.2.2", "pytype >= 2019.3.21"
    )
    session.run("pytype")


@nox.session(python="3.6")
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")
    session.run("coverage", "erase")
