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
import pathlib
import shutil

import nox

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

SYSTEM_TEST_ENV_VARS = ("GOOGLE_APPLICATION_CREDENTIALS",)
RUFF_VERSION = "ruff==0.14.14"

DEFAULT_PYTHON_VERSION = "3.14"
UNIT_TEST_PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]
SYSTEM_TEST_PYTHON_VERSIONS = UNIT_TEST_PYTHON_VERSIONS

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

nox.options.sessions = [
    "system",
    "blacken",
    "mypy",
    "doctest",
    "format",
]


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run the unit test suite."""

    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Install all test dependencies, then install this package in-place.
    session.install("mock", "pytest", "pytest-cov", "pytest-asyncio<=0.14.0", "brotli")
    session.install("-e", ".[requests,aiohttp]", "-c", constraints_path)

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


@nox.session(python="3.10")
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".")
    session.install(
        # We need to pin to specific versions of the `sphinxcontrib-*` packages
        # which still support sphinx 4.x.
        # See https://github.com/googleapis/sphinx-docfx-yaml/issues/344
        # and https://github.com/googleapis/sphinx-docfx-yaml/issues/345.
        "sphinxcontrib-applehelp==1.0.4",
        "sphinxcontrib-devhelp==1.0.2",
        "sphinxcontrib-htmlhelp==2.0.1",
        "sphinxcontrib-qthelp==1.0.3",
        "sphinxcontrib-serializinghtml==1.1.5",
        "sphinx==4.5.0",
        "alabaster",
        "recommonmark",
    )

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

@nox.session(python="3.10")
def docfx(session):
    """Build the docfx yaml files for this library."""

    session.install("-e", ".")
    session.install(
        # We need to pin to specific versions of the `sphinxcontrib-*` packages
        # which still support sphinx 4.x.
        # See https://github.com/googleapis/sphinx-docfx-yaml/issues/344
        # and https://github.com/googleapis/sphinx-docfx-yaml/issues/345.
        "sphinxcontrib-applehelp==1.0.4",
        "sphinxcontrib-devhelp==1.0.2",
        "sphinxcontrib-htmlhelp==2.0.1",
        "sphinxcontrib-qthelp==1.0.3",
        "sphinxcontrib-serializinghtml==1.1.5",
        "gcp-sphinx-docfx-yaml",
        "alabaster",
        "recommonmark",
    )

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
    session.install("-e", ".[requests,aiohttp]")
    session.install("sphinx==4.0.1", "alabaster", "recommonmark")
    session.install(
        "sphinxcontrib-applehelp==1.0.4",
        "sphinxcontrib-devhelp==1.0.2",
        "sphinxcontrib-htmlhelp==2.0.1",
        "sphinxcontrib-qthelp==1.0.3",
        "sphinxcontrib-serializinghtml==1.1.5",
        "sphinx==4.5.0",
        "sphinx_rtd_theme",
        "sphinx-docstring-typing >= 0.0.3",
        "mock",
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
    session.install("flake8", RUFF_VERSION)
    session.install("-e", ".")
    session.run(
        "flake8",
        os.path.join("google", "resumable_media"),
        "tests",
        os.path.join("google", "_async_resumable_media"),
        "tests_async",
    )

    # 2. Check formatting
    session.run(
        "ruff",
        "format",
        "--check",
        f"--target-version=py{UNIT_TEST_PYTHON_VERSIONS[0].replace('.', '')}",
        "--line-length=88",
        os.path.join("google", "resumable_media"),
        "tests",
        os.path.join("google", "_async_resumable_media"),
        "tests_async",
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("setuptools", "docutils", "Pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """(Deprecated) Legacy session. Please use 'nox -s format'."""
    session.log(
        "WARNING: The 'blacken' session is deprecated and will be removed in a future release. Please use 'nox -s format' in the future."
    )

    # Just run the ruff formatter (keeping legacy behavior of only formatting, not sorting imports)
    session.install(RUFF_VERSION)
    session.run(
        "ruff",
        "format",
        f"--target-version=py{UNIT_TEST_PYTHON_VERSIONS[0].replace('.', '')}",
        "--line-length=88",
        os.path.join("google", "resumable_media"),
        "tests",
        os.path.join("google", "_async_resumable_media"),
        "tests_async",
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def format(session):
    """
    Run ruff to sort imports and format code.
    """
    # 1. Install ruff (skipped automatically if you run with --no-venv)
    session.install(RUFF_VERSION)

    # 2. Run Ruff to fix imports
    session.run(
        "ruff", "check",
        "--select", "I",
        "--fix",
        f"--target-version=py{UNIT_TEST_PYTHON_VERSIONS[0].replace('.', '')}",
        "--line-length=88",
        os.path.join("google", "resumable_media"),
        "tests",
        os.path.join("google", "_async_resumable_media"),
        "tests_async",
        "noxfile.py",
        "setup.py",
    )

    # 3. Run Ruff to format code
    session.run(
        "ruff", "format",
        f"--target-version=py{UNIT_TEST_PYTHON_VERSIONS[0].replace('.', '')}",
        "--line-length=88",
        os.path.join("google", "resumable_media"),
        "tests",
        os.path.join("google", "_async_resumable_media"),
        "tests_async",
        "noxfile.py",
        "setup.py",
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Verify type hints are mypy compatible."""
    session.install("-e", ".")
    session.install(
        "mypy",
        "types-setuptools",
        "types-requests",
        "types-mock",
    )
    session.run("mypy", "-p", "google", "-p", "tests", "-p", "tests_async")


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def system(session):
    """Run the system test suite."""

    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Environment check: environment variables are set.
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
    session.install("mock", "pytest", "google-cloud-testutils", "brotli")
    session.install("-e", ".[requests,aiohttp]", "-c", constraints_path)

    # Run py.test against the async system tests.
    if session.python.startswith("3"):
        session.install("pytest-asyncio<=0.14.0")
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


@nox.session(python=DEFAULT_PYTHON_VERSION)
def prerelease_deps(session):
    # TODO(https://github.com/googleapis/google-cloud-python/issues/16014):
    # Resolve the linked bug once prerelease_deps and core_deps_from_source
    # are implemented for this package.
    if session.python == DEFAULT_PYTHON_VERSION:
        session.skip(f"Skipping prerelease_deps for {DEFAULT_PYTHON_VERSION} until a future release.")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def core_deps_from_source(session):
    ## TODO(https://github.com/googleapis/google-cloud-python/issues/16014):
    # Resolve the linked bug once prerelease_deps and core_deps_from_source
    # are implemented for this package.
    if session.python == DEFAULT_PYTHON_VERSION:
        session.skip(f"Skipping core_deps_from_source for {DEFAULT_PYTHON_VERSION} until a future release.")
