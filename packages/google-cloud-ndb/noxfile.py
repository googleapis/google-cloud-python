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

import nox

LOCAL_DEPS = ("google-cloud-core", "google-api-core")
NOX_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_INTERPRETER = "3.7"
PYPY = "pypy3"
ALL_INTERPRETERS = ("3.6", "3.7", PYPY)


def get_path(*names):
    return os.path.join(NOX_DIR, *names)


@nox.session(py=ALL_INTERPRETERS)
def unit(session):
    # Install all dependencies.
    session.install("pytest", "pytest-cov")
    session.install(".")
    # Run py.test against the unit tests.
    run_args = ["pytest"]
    if session.posargs:
        run_args.extend(session.posargs)
    else:
        run_args.extend(
            [
                "--cov=google.cloud.ndb",
                "--cov=tests.unit",
                "--cov-config",
                get_path(".coveragerc"),
                "--cov-report=",
            ]
        )
    run_args.append(get_path("tests", "unit"))
    session.run(*run_args)

    if not session.posargs:
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
            "--line-length=79",
            get_path("docs"),
            get_path("noxfile.py"),
            get_path("src"),
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
    session.install("flake8", "black")
    run_black(session, use_check=True)
    session.run("flake8", "google", "tests")


@nox.session(py=DEFAULT_INTERPRETER)
def blacken(session):
    # Install all dependencies.
    session.install("black")
    # Run ``black``.
    run_black(session)


@nox.session(py=DEFAULT_INTERPRETER)
def docs(session):
    # Install all dependencies.
    session.install("Sphinx < 2.0dev")
    session.install(".")
    # Building the docs.
    run_args = [
        "sphinx-build",
        "-W",
        "-b",
        "html",
        "-d",
        get_path("docs", "_build", "doctrees"),
        "docs",
        get_path("docs", "_build", "html"),
    ]
    session.run(*run_args)


@nox.session(py=DEFAULT_INTERPRETER)
def doctest(session):
    # Install all dependencies.
    session.install("Sphinx < 2.0dev")
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


@nox.session(py=DEFAULT_INTERPRETER)
def system(session):
    """Run the system test suite."""
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
    for local_dep in LOCAL_DEPS:
        session.install(local_dep)
    session.install("-e", get_path("test_utils", "test_utils"))
    session.install("-e", ".")

    # Run py.test against the system tests.
    if system_test_exists:
        session.run("py.test", "--quiet", system_test_path, *session.posargs)
    if system_test_folder_exists:
        session.run(
            "py.test", "--quiet", system_test_folder_path, *session.posargs
        )
