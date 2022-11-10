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
import pathlib
import shutil

# https://github.com/google/importlab/issues/25
import nox  # pytype: disable=import-error


BLACK_VERSION = "black==22.3.0"
BLACK_PATHS = ["docs", "google", "tests", "noxfile.py", "setup.py"]
# Black and flake8 clash on the syntax for ignoring flake8's F401 in this file.
BLACK_EXCLUDES = ["--exclude", "^/google/api_core/operations_v1/__init__.py"]

DEFAULT_PYTHON_VERSION = "3.10"
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

# 'docfx' is excluded since it only needs to run in 'docs-presubmit'
nox.options.sessions = [
    "unit",
    "unit_grpc_gcp",
    "unit_wo_grpc",
    "cover",
    "pytype",
    "mypy",
    "lint",
    "lint_setup_py",
    "blacken",
    "docs",
]


def _greater_or_equal_than_37(version_string):
    tokens = version_string.split(".")
    for i, token in enumerate(tokens):
        try:
            tokens[i] = int(token)
        except ValueError:
            pass
    return tokens >= [3, 7]


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", "flake8-import-order", BLACK_VERSION)
    session.install(".")
    session.run(
        "black",
        "--check",
        *BLACK_EXCLUDES,
        *BLACK_PATHS,
    )
    session.run("flake8", "google", "tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black.

    Format code to uniform standard.
    """
    session.install(BLACK_VERSION)
    session.run("black", *BLACK_EXCLUDES, *BLACK_PATHS)


def default(session, install_grpc=True):
    """Default unit test session.

    This is intended to be run **without** an interpreter set, so
    that the current ``python`` (on the ``PATH``) or the version of
    Python corresponding to the ``nox`` binary the ``PATH`` can
    run the tests.
    """
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Install all test dependencies, then install this package in-place.
    session.install(
        "dataclasses",
        "mock",
        # Revert to just "pytest" once
        # https://github.com/pytest-dev/pytest/issues/10451 is fixed
        "pytest<7.2.0",
        "pytest-cov",
        "pytest-xdist",
    )

    if install_grpc:
        session.install("-e", ".[grpc]", "-c", constraints_path)
    else:
        session.install("-e", ".", "-c", constraints_path)

    pytest_args = [
        "python",
        "-m",
        "py.test",
        *(
            # Helpful for running a single test or testfile.
            session.posargs
            or [
                "--quiet",
                "--cov=google.api_core",
                "--cov=tests.unit",
                "--cov-append",
                "--cov-config=.coveragerc",
                "--cov-report=",
                "--cov-fail-under=0",
                # Running individual tests with parallelism enabled is usually not helpful.
                "-n=auto",
                os.path.join("tests", "unit"),
            ]
        ),
    ]

    # Inject AsyncIO content and proto-plus, if version >= 3.7.
    # proto-plus is needed for a field mask test in test_protobuf_helpers.py
    if _greater_or_equal_than_37(session.python):
        session.install("asyncmock", "pytest-asyncio", "proto-plus")

        # Having positional arguments means the user wants to run specific tests.
        # Best not to add additional tests to that list.
        if not session.posargs:
            pytest_args.append("--cov=tests.asyncio")
            pytest_args.append(os.path.join("tests", "asyncio"))

    session.run(*pytest_args)


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10"])
def unit_grpc_gcp(session):
    """Run the unit test suite with grpcio-gcp installed."""
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    # Install grpcio-gcp
    session.install("-e", ".[grpcgcp]", "-c", constraints_path)
    # Install protobuf < 4.0.0
    session.install("protobuf<4.0.0")

    default(session)


@nox.session(python=["3.8", "3.10"])
def unit_wo_grpc(session):
    """Run the unit test suite w/o grpcio installed"""
    default(session, install_grpc=False)


@nox.session(python="3.8")
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""

    session.install("docutils", "Pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python="3.8")
def pytype(session):
    """Run type-checking."""
    session.install(".[grpc]", "pytype >= 2019.3.21")
    session.run("pytype")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Run type-checking."""
    session.install(".[grpc]", "mypy")
    session.install(
        "types-setuptools",
        "types-requests",
        "types-protobuf",
        "types-mock",
        "types-dataclasses",
    )
    session.run("mypy", "google", "tests")


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
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".[grpc]")
    session.install("sphinx==4.2.0", "alabaster", "recommonmark")

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


@nox.session(python="3.8")
def docfx(session):
    """Build the docfx yaml files for this library."""

    session.install("-e", ".")
    session.install(
        "sphinx==4.0.1", "alabaster", "recommonmark", "gcp-sphinx-docfx-yaml"
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
