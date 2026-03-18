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
import shutil

import nox

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

CLICK_VERSION = "click"
BLACK_VERSION = "black==23.7.0"
BLACK_PATHS = [
    "google",
    "tests",
    "tests_async",
    "noxfile.py",
    "setup.py",
    "docs/conf.py",
]

DEFAULT_PYTHON_VERSION = "3.14"
UNIT_TEST_PYTHON_VERSIONS = [
    "3.8",
    "3.9",
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
]
ALL_PYTHON = UNIT_TEST_PYTHON_VERSIONS.copy()
ALL_PYTHON.extend(["3.7"])

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

# pypy will be run as a github action instead of through Kokoro
nox.options.sessions = [
    "lint",
    "blacken",
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


@nox.session(python=ALL_PYTHON)
@nox.parametrize(["install_deprecated_extras"], (True, False))
def unit(session, install_deprecated_extras):
    # Install all test dependencies, then install this package in-place.

    if session.python in ("3.7",):
        session.skip("Python 3.7 is no longer supported")
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


@nox.session(python=DEFAULT_PYTHON_VERSION)
def prerelease_deps(session):
    """Run all tests with pre-release versions of dependencies installed
    rather than the standard non pre-release versions.
    Pre-release versions can be installed using
    `pip install --pre <package>`.
    """
    # TODO(https://github.com/googleapis/google-cloud-python/issues/16013):
    # Add prerelease tests
    session.skip("Prerelease tests are not yet supported")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def core_deps_from_source(session):
    """Run all tests with core dependencies installed from source
    rather than pulling the dependencies from PyPI.
    """
    # TODO(https://github.com/googleapis/google-cloud-python/issues/16013):
    # Add prerelease tests
    session.skip("Prerelease tests are not yet supported")
