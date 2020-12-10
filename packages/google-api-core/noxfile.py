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
import shutil

# https://github.com/google/importlab/issues/25
import nox  # pytype: disable=import-error

_MINIMAL_ASYNCIO_SUPPORT_PYTHON_VERSION = [3, 6]


def _greater_or_equal_than_36(version_string):
    tokens = version_string.split(".")
    for i, token in enumerate(tokens):
        try:
            tokens[i] = int(token)
        except ValueError:
            pass
    return tokens >= [3, 6]


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

    pytest_args = [
        "python",
        "-m",
        "py.test",
        "--quiet",
        "--cov=google.api_core",
        "--cov=tests.unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
    ]
    pytest_args.extend(session.posargs)

    # Inject AsyncIO content, if version >= 3.6.
    if _greater_or_equal_than_36(session.python):
        session.install("asyncmock", "pytest-asyncio")

        pytest_args.append("--cov=tests.asyncio")
        pytest_args.append(os.path.join("tests", "asyncio"))
        session.run(*pytest_args)
    else:
        # Run py.test against the unit tests.
        session.run(*pytest_args)


@nox.session(python=["2.7", "3.5", "3.6", "3.7", "3.8", "3.9"])
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python=["2.7", "3.5", "3.6", "3.7", "3.8", "3.9"])
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


@nox.session(python="3.7")
def docs(session):
    """Build the docs for this library."""

    session.install(".", "grpcio >= 1.8.2", "grpcio-gcp >= 0.2.2")
    session.install("-e", ".")
    session.install("sphinx < 3.0", "alabaster", "recommonmark")

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


@nox.session(python="3.7")
def docfx(session):
    """Build the docfx yaml files for this library."""

    session.install("-e", ".")
    # sphinx-docfx-yaml supports up to sphinx version 1.5.5.
    # https://github.com/docascode/sphinx-docfx-yaml/issues/97
    session.install("sphinx==1.5.5", "alabaster", "recommonmark", "sphinx-docfx-yaml")

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
