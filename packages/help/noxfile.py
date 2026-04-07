# -*- coding: utf-8 -*-
#
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software/
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pathlib
import nox

DEFAULT_PYTHON_VERSION = "3.14"
ALL_PYTHON = ["3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
REPO_ROOT = CURRENT_DIRECTORY.parent.parent

# Hardcoded dictionary of documentation files.
# Format: {"Display Title": "filename.md" or absolute path}
DOCS_MAP = {
    "Getting started": str(REPO_ROOT / "README.rst"),
}

nox.options.sessions = [
    "lint",
    "lint_setup_py",
    "unit",
    "mypy",
    "prerelease_deps",
    "core_deps_from_source",
    "docfx",
    "docs",
]

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session: nox.Session) -> None:
    """Verify that setup.py is valid."""
    session.install("setuptools")
    session.run("python", "setup.py", "check", "--strict")

@nox.session(python=ALL_PYTHON)
def unit(session: nox.Session) -> None:
    """Run unit tests."""
    session.install("pytest", "pytest-cov")
    session.install("-e", ".")
    session.run("pytest", "tests")

@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session: nox.Session) -> None:
    """Run mypy."""
    session.install("mypy", "types-PyYAML")
    session.install("-e", ".")
    session.run("mypy", "help", "tests", "noxfile.py", "docfx_helper.py")

@nox.session(python=DEFAULT_PYTHON_VERSION)
def prerelease_deps(session: nox.Session) -> None:
    """Run unit tests with prerelease dependencies."""
    # Since we have no dependencies, this is just a normal unit test run
    # but with --pre enabled for any test tools.
    session.install("pytest", "pytest-cov")
    session.install("-e", ".")
    session.run("pytest", "tests")

@nox.session(python=DEFAULT_PYTHON_VERSION)
def core_deps_from_source(session: nox.Session) -> None:
    """Run unit tests with core dependencies installed from source."""
    # We don't depend on core, so we just run unit tests.
    session.install("pytest", "pytest-cov")
    session.install("-e", ".")
    session.run("pytest", "tests")

@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session: nox.Session) -> None:
    """Run linters."""
    session.install("ruff")
    session.run("ruff", "check", ".")

@nox.session(python="3.10")
def docfx(session: nox.Session) -> None:
    """Build the docfx yaml files for this library."""
    session.install("PyYAML", "pypandoc")
    
    # Construct arguments for the helper script
    args = [
        "--current-dir", str(CURRENT_DIRECTORY),
    ]
    for title, source in DOCS_MAP.items():
        args.extend(["--doc", title, str(source)])
    
    session.run("python", "docfx_helper.py", *args)

@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs(session: nox.Session) -> None:
    """No-op session for docs."""
    session.log("This package does not have Sphinx documentation.")
