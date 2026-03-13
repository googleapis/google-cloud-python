# Copyright 2021 Google LLC
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
import nox

DEFAULT_PYTHON_VERSION = "3.14"
UNIT_TEST_PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]

ALL_PYTHON = list(UNIT_TEST_PYTHON_VERSIONS)
# ALL_PYTHON.extend(["3.7"]) # User said NOT to include 3.7

nox.options.sessions = [
    "format",
    "lint",
    "lint_setup_py",
    "mypy",
    "unit",
    "docs",
    "prerelease_deps",
    "core_deps_from_source",
]

def _skip_if_37(session):
    if session.python in ("3.7",):
        session.skip("Python 3.7 is no longer supported")

@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Run the type checker."""
    # TODO(https://github.com/googleapis/google-cloud-python/issues/16014):
    # Add mypy tests
    session.skip("mypy tests are not yet supported")

@nox.session(python=DEFAULT_PYTHON_VERSION)
def core_deps_from_source(session):
    """Run all tests with core dependencies installed from source
    rather than pulling the dependencies from PyPI.
    """
    # TODO(https://github.com/googleapis/google-cloud-python/issues/16014):
    # Add core deps from source tests
    session.skip("Core deps from source tests are not yet supported")

@nox.session(python=DEFAULT_PYTHON_VERSION)
def prerelease_deps(session):
    """Run all tests with prerelease versions of dependencies installed.
    """
    # TODO(https://github.com/googleapis/google-cloud-python/issues/16014):
    # Add prerelease deps tests
    session.skip("prerelease deps tests are not yet supported")

@nox.session
def format(session: nox.sessions.Session) -> None:
    """
    Run isort to sort imports. Then run black
    to format code to uniform standard.
    """
    _skip_if_37(session)
    session.install("black", "isort")
    python_files = [path for path in os.listdir(".") if path.endswith(".py")]
    if not python_files:
        pass
    
    # Use the --fss option to sort imports using strict alphabetical order.
    # See https://pycqa.github.io/isort/docs/configuration/options.html#force-sort-within-sections
    session.run("isort", "--fss", *python_files)
    session.run("black", *python_files)

@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linter."""
    _skip_if_37(session)
    session.install("flake8")
    session.run("flake8", ".")

@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Lint setup.py."""
    _skip_if_37(session)
    session.install("setuptools", "flake8")
    session.run("flake8", "setup.py")

@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run unit tests."""
    _skip_if_37(session)
    session.install("-r", "requirements.txt")
    session.install("pytest")
    session.run("pytest", "tests")

@nox.session(python="3.10")
def docs(session):
    """Build documentation."""
    _skip_if_37(session)
    session.install("-r", "requirements.txt")
    session.install("sphinx", "sphinx-docfx-yaml")
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")
