# Copyright 2017 Google Inc.
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
import shutil

import nox

SYSTEM_TEST_ENV_VARS = ("GOOGLE_APPLICATION_CREDENTIALS",)
BLACK_VERSION = "black==20.8b1"
GOOGLE_AUTH = "google-auth >= 1.22.0, < 2.0dev"

DEFAULT_PYTHON_VERSION = "3.8"
SYSTEM_TEST_PYTHON_VERSIONS = ["2.7", "3.8"]
UNIT_TEST_PYTHON_VERSIONS = ["3.6", "3.7", "3.8"]
UNIT_TEST_SYNC_PYTHON_VERSIONS = ["2.7", "3.5"]


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run the unit test suite."""

    # Install all test dependencies, then install this package in-place.
    session.install("mock", "pytest", "pytest-cov", "pytest-asyncio", GOOGLE_AUTH)
    session.install("-e", ".[requests]")

    # Run py.test against the unit tests.
    # NOTE: We don't require 100% line coverage for unit test runs since
    #       some have branches that are Py2/Py3 specific.
    line_coverage = "--cov-fail-under=0"
    session.run(
        "py.test",
        "--cov=google.resumable_media",
        "--cov=google._async_resumable_media",
        "--cov=tests.unit",
        "--cov=tests_async.unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        line_coverage,
        os.path.join("tests", "unit"),
        os.path.join("tests_async", "unit"),
        *session.posargs
    )


@nox.session(python=UNIT_TEST_SYNC_PYTHON_VERSIONS)
def unit_2(session):
    """Run the unit test suite."""

    # Install all test dependencies, then install this package in-place.
    session.install("mock", "pytest", "pytest-cov")
    session.install("-e", ".[requests]")

    # Run py.test against the unit tests.
    # NOTE: We don't require 100% line coverage for unit test runs since
    #       some have branches that are Py2/Py3 specific.
    line_coverage = "--cov-fail-under=0"
    session.run(
        "py.test",
        "--cov=google.resumable_media",
        "--cov=tests.unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        line_coverage,
        os.path.join("tests", "unit"),
        *session.posargs
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".")
    session.install("sphinx", "alabaster", "recommonmark")

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
def docfx(session):
    """Build the docfx yaml files for this library."""

    session.install("-e", ".")
    session.install("sphinx", "alabaster", "recommonmark", "sphinx-docfx-yaml")

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-T",  # show full traceback on exception
        "-N",  # no colors
        "-D",
        (
            "extensions=sphinx.ext.autodoc,"
            "sphinx.ext.autosummary,"
            "docfx_yaml.extension,"
            "sphinx.ext.intersphinx,"
            "sphinx.ext.coverage,"
            "sphinx.ext.napoleon,"
            "sphinx.ext.todo,"
            "sphinx.ext.viewcode,"
            "recommonmark"
        ),
        "-b",
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "html", ""),
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def doctest(session):
    """Run the doctests."""
    session.install("-e", ".[requests]")
    session.install("sphinx", "alabaster", "recommonmark")
    session.install(
        "sphinx",
        "sphinx_rtd_theme",
        "sphinx-docstring-typing >= 0.0.3",
        "mock",
        GOOGLE_AUTH,
    )

    # Run the doctests with Sphinx.
    session.run(
        "sphinx-build",
        "-W",
        "-b",
        "doctest",
        "-d",
        os.path.join("docs", "_build", "doctrees"),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "doctest"),
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run flake8.

    Returns a failure if flake8 finds linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION)
    session.install("-e", ".")
    session.run(
        "flake8",
        os.path.join("google", "resumable_media"),
        "tests",
        os.path.join("google", "_async_resumable_media"),
        "tests_async",
    )
    session.run(
        "black",
        "--check",
        os.path.join("google", "resumable_media"),
        "tests",
        os.path.join("google", "_async_resumable_media"),
        "tests_async",
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "Pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    session.install(BLACK_VERSION)
    session.run(
        "black",
        os.path.join("google", "resumable_media"),
        "tests",
        os.path.join("google", "_async_resumable_media"),
        "tests_async",
    )


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def system(session):
    """Run the system test suite."""

    # Sanity check: environment variables are set.
    missing = []
    for env_var in SYSTEM_TEST_ENV_VARS:
        if env_var not in os.environ:
            missing.append(env_var)

    # Only run system tests if the environment variables are set.
    if missing:
        all_vars = ", ".join(missing)
        msg = "Environment variable(s) unset: {}".format(all_vars)
        session.skip(msg)

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    session.install("mock", "pytest", GOOGLE_AUTH, "google-cloud-testutils")
    session.install("-e", ".[requests]")

    # Run py.test against the async system tests.
    if session.python.startswith("3"):
        session.install("pytest-asyncio")
        session.run(
            "py.test", "-s", os.path.join("tests_async", "system"), *session.posargs
        )

    # Run py.test against the system tests.
    session.run("py.test", "-s", os.path.join("tests", "system"), *session.posargs)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")
    session.run("coverage", "erase")
