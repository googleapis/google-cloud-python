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


NOX_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_INTERPRETER = "3.7"
PYPY = "pypy3"
ALL_INTERPRETERS = ("3.5", "3.6", "3.7", PYPY)


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
                "--cov=tests",
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


@nox.session(py=DEFAULT_INTERPRETER)
def lint(session):
    """Run linters.
    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", "black")
    session.run(
        "black",
        "--check",
        "--line-length=79",
        get_path("docs"),
        get_path("noxfile.py"),
        get_path("src"),
        get_path("tests"),
    )
    session.run("flake8", "google", "tests")


@nox.session(py=DEFAULT_INTERPRETER)
def blacken(session):
    # Install all dependencies.
    session.install("black")
    # Run ``black``.
    session.run(
        "black",
        "--line-length=79",
        get_path("docs"),
        get_path("noxfile.py"),
        get_path("src"),
        get_path("tests"),
    )


@nox.session(py=DEFAULT_INTERPRETER)
def docs(session):
    # Install all dependencies.
    session.install("Sphinx")
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
    session.install("Sphinx")
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
