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

"""Build and test configuration file.

Assumes ``nox >= 2018.9.14`` is installed.
"""

import os
import pathlib
import shutil

import nox

LOCAL_DEPS = ("google-api-core", "google-cloud-core")
NOX_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_INTERPRETER = "3.8"
ALL_INTERPRETERS = ("2.7", "3.6", "3.7", "3.8", "3.9", "3.10")
PY3_INTERPRETERS = ("3.6", "3.7", "3.8", "3.9", "3.10")
MAJOR_INTERPRETERS = ("2.7", "3.8")
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

BLACK_VERSION = "black==20.8b1"


def get_path(*names):
    return os.path.join(NOX_DIR, *names)


@nox.session(py=ALL_INTERPRETERS)
def unit(session):
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    # Install all dependencies.
    session.install("pytest", "pytest-cov")
    session.install("mock")
    session.install("google-cloud-testutils", "-c", constraints_path)
    session.install("-e", ".", "-c", constraints_path)
    # This variable is used to skip coverage by Python version
    session.env["PY_VERSION"] = session.python[0]
    # Run py.test against the unit tests.
    run_args = ["pytest"]
    if session.posargs:
        run_args.extend(session.posargs)
    else:
        run_args.extend(
            [
                "--cov=google.cloud.ndb",
                "--cov=unit",
                "--cov-append",
                "--cov-config",
                get_path(".coveragerc"),
                "--cov-report=term-missing",
            ]
        )
    run_args.append(get_path("tests", "unit"))
    session.run(*run_args)

    # Do not run cover session for Python 2, or it will fail
    if not session.posargs and session.python[0] != "2":
        session.notify("cover")


@nox.session(py=DEFAULT_INTERPRETER)
def cover(session):
    # Install all dependencies.
    session.install("coverage")
    # Run coverage report.
    session.run("coverage", "report", "--fail-under=100", "--show-missing")
    # Erase cached coverage data.
    session.run("coverage", "erase")


def run_black(session, use_check=False):
    args = ["black"]
    if use_check:
        args.append("--check")

    args.extend(
        [
            get_path("docs"),
            get_path("noxfile.py"),
            get_path("google"),
            get_path("tests"),
        ]
    )

    session.run(*args)


@nox.session(py=DEFAULT_INTERPRETER)
def lint(session):
    """Run linters.
    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION, "click<8.1.0")
    run_black(session, use_check=True)
    session.run("flake8", "google", "tests")


@nox.session(py=DEFAULT_INTERPRETER)
def blacken(session):
    # Install all dependencies.
    session.install(BLACK_VERSION, "click<8.1.0")
    # Run ``black``.
    run_black(session)


@nox.session(py=DEFAULT_INTERPRETER)
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".")
    session.install(
        "Sphinx==4.0.1", "alabaster", "recommonmark", "sphinxcontrib.spelling"
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


@nox.session(py=DEFAULT_INTERPRETER)
def doctest(session):
    # Install all dependencies.
    session.install("Sphinx==4.0.1")
    session.install("sphinxcontrib.spelling")
    session.install(".")
    # Run the script for building docs and running doctests.
    run_args = [
        "sphinx-build",
        "-W",
        "-b",
        "doctest",
        "-d",
        get_path("docs", "_build", "doctrees"),
        get_path("docs"),
        get_path("docs", "_build", "doctest"),
    ]
    session.run(*run_args)


@nox.session(py=MAJOR_INTERPRETERS)
def system(session):
    """Run the system test suite."""
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    system_test_path = get_path("tests", "system.py")
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
    session.install("pytest")
    session.install("mock")
    session.install("google-cloud-testutils")
    for local_dep in LOCAL_DEPS:
        session.install(local_dep)
    session.install("-e", ".", "-c", constraints_path)

    # Run py.test against the system tests.
    if system_test_exists:
        session.run("py.test", "--quiet", system_test_path, *session.posargs)
    if system_test_folder_exists:
        session.run("py.test", "--quiet", system_test_folder_path, *session.posargs)
