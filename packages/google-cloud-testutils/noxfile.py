# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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


from __future__ import absolute_import
import os
import pathlib
import re
import shutil

import nox

# 'update_lower_bounds' is excluded
nox.options.sessions = [
    "check_lower_bounds",
    "format",
]


# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

ALL_PYTHON = ["3.10", "3.11", "3.12", "3.13", "3.14"]
DEFAULT_PYTHON_VERSION = "3.14"
BLACK_VERSION = "black==23.7.0"
RUFF_VERSION = "ruff==0.14.14"
BLACK_PATHS = ["test_utils", "setup.py"]
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION)
    session.run(
        "black",
        "--check",
        *BLACK_PATHS,
    )
    session.run("flake8", *BLACK_PATHS)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black.

    Format code to uniform standard.
    """
    session.install(BLACK_VERSION)
    session.run(
        "black",
        *BLACK_PATHS,
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
        f"--target-version=py{ALL_PYTHON[0].replace('.', '')}",
        "--line-length=88",
        *BLACK_PATHS,
    )

    # 3. Run Ruff to format code
    session.run(
        "ruff", "format",
        f"--target-version=py{ALL_PYTHON[0].replace('.', '')}",
        "--line-length=88",
        *BLACK_PATHS,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "pygments", "setuptools")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Verify type hints are mypy compatible."""
    session.install("-e", ".")
    session.install(
        "mypy",
        "types-mock",
        "types-setuptools",
    )
    session.run("mypy", "test_utils/", "tests/")


@nox.session(python=ALL_PYTHON)
def unit(session):
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Install two fake packages for the lower-bound-checker tests
    session.install(
        "-e", "tests/unit/resources/good_package", "tests/unit/resources/bad_package"
    )

    session.install("pytest", "pytest-cov")
    session.install("-e", ".", "-c", constraints_path)

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=test_utils",
        "--cov=tests/unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        *session.posargs,
    )


@nox.session(python=ALL_PYTHON)
def system(session):
    """Run system test.
    Check lower bounds in setup.py are reflected in constraints file"""
    session.install(".")
    session.run(
        "lower-bound-checker",
        "check",
        "--package-name",
        "google-cloud-testutils",
        "--constraints-file",
        "testing/constraints-3.10.txt",
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def update_lower_bounds(session):
    """Update lower bounds in constraints.txt to match setup.py"""
    session.install(".")
    session.run(
        "lower-bound-checker",
        "update",
        "--package-name",
        "google-cloud-testutils",
        "--constraints-file",
        "testing/constraints-3.10.txt",
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
        "html",  # builder
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),  # cache directory
        # paths to build:
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
def prerelease_deps(session):
    """
    Run all tests with pre-release versions of dependencies installed
    rather than the standard non pre-release versions.
    Pre-release versions can be installed using
    `pip install --pre <package>`.
    """

    # Install all dependencies
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Install two fake packages for the lower-bound-checker tests
    session.install(
        "-e", "tests/unit/resources/good_package", "tests/unit/resources/bad_package"
    )

    session.install("pytest", "pytest-cov")
    session.install("-e", ".", "-c", constraints_path)

    # Because we test minimum dependency versions on the minimum Python
    # version, the first version we test with in the unit tests sessions has a
    # constraints file containing all dependencies and extras.
    with open(
        CURRENT_DIRECTORY / "testing" / f"constraints-{ALL_PYTHON[0]}.txt",
        encoding="utf-8",
    ) as constraints_file:
        constraints_text = constraints_file.read()

    # Ignore leading whitespace and comment lines.
    constraints_deps = [
        match.group(1)
        for match in re.finditer(
            r"^\s*(\S+)(?===\S+)", constraints_text, flags=re.MULTILINE
        )
    ]

    # Install dependencies specified in `testing/constraints-X.txt`.
    session.install(*constraints_deps)

    # Note: If a dependency is added to the `prerel_deps` list,
    # the `core_dependencies_from_source` list in the `core_deps_from_source`
    # nox session should also be updated.
    prerel_deps = [
        "googleapis-common-protos",
        "google-api-core",
        "google-auth",
        "grpc-google-iam-v1",
        "grpcio>=1.75.1" if session.python >= "3.12" else "grpcio<=1.62.2",
        "grpcio-status",
        "protobuf",
        "proto-plus",
    ]

    deps_dir = CURRENT_DIRECTORY.parent
    while deps_dir.name != "packages" and deps_dir.parent != deps_dir:
        deps_dir = deps_dir.parent

    # Extract the base package name, safely ignoring version bounds and spaces
    # (e.g., "grpcio>=1.75.1" becomes "grpcio")
    parsed_deps = {
        dep: re.match(r"^([a-zA-Z0-9_-]+)", dep).group(1) 
        for dep in prerel_deps
    }

    # Dynamically sort local packages vs PyPI dependencies
    local_paths = []
    pypi_deps = []
    
    for dep, pkg_name in parsed_deps.items():
        if (deps_dir / pkg_name).exists():
            local_paths.append(str(deps_dir / pkg_name))
        else:
            pypi_deps.append(dep)

    # Batch pip installations for maximum speed
    if local_paths:
        session.install(*local_paths, "--no-deps", "--ignore-installed")
    if pypi_deps:
        session.install(*pypi_deps, "--pre", "--no-deps", "--ignore-installed")

    # TODO(https://github.com/grpc/grpc/issues/38965): Add `grpcio-status`
    # to the dictionary below once this bug is fixed.
    # TODO(https://github.com/googleapis/google-cloud-python/issues/13643): Add
    # `googleapis-common-protos` and `grpc-google-iam-v1` to the dictionary below
    # once this bug is fixed.
    package_namespaces = {
        "google-api-core": "google.api_core",
        "google-auth": "google.auth",
        "grpcio": "grpc",
        "protobuf": "google.protobuf",
        "proto-plus": "proto",
    }

    # Reuse the parsed names for logging and version verification
    for dep, pkg_name in parsed_deps.items():
        print(f"Installed {dep}")
        version_namespace = package_namespaces.get(pkg_name)

        if version_namespace:
            session.run(
                "python",
                "-c",
                f"import {version_namespace}; print({version_namespace}.__version__)",
            )

    session.run(
        "py.test",
        "tests/unit",
    )



@nox.session(python=DEFAULT_PYTHON_VERSION)
def core_deps_from_source(session):
    """Run all tests with core dependencies installed from source
    rather than pulling the dependencies from PyPI.
    """


    # Install all dependencies
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Install two fake packages for the lower-bound-checker tests
    session.install(
        "-e", "tests/unit/resources/good_package", "tests/unit/resources/bad_package"
    )

    session.install("pytest", "pytest-cov")
    session.install("-e", ".", "-c", constraints_path)

    # Because we test minimum dependency versions on the minimum Python
    # version, the first version we test with in the unit tests sessions has a
    # constraints file containing all dependencies and extras.
    with open(
        CURRENT_DIRECTORY / "testing" / f"constraints-{ALL_PYTHON[0]}.txt",
        encoding="utf-8",
    ) as constraints_file:
        constraints_text = constraints_file.read()

    # Ignore leading whitespace and comment lines.
    constraints_deps = [
        match.group(1)
        for match in re.finditer(
            r"^\s*(\S+)(?===\S+)", constraints_text, flags=re.MULTILINE
        )
    ]

    # Install dependencies specified in `testing/constraints-X.txt`.
    session.install(*constraints_deps)

    # Note: If a dependency is added to the `core_dependencies_from_source` list,
    # the `prerel_deps` list in the `prerelease_deps` nox session should also be updated.
    core_dependencies_from_source = [
        "googleapis-common-protos",
        "google-api-core",
        "google-auth",
        "grpc-google-iam-v1",
        "proto-plus",
    ]

    deps_dir = CURRENT_DIRECTORY.parent
    while deps_dir.name != "packages" and deps_dir.parent != deps_dir:
        deps_dir = deps_dir.parent

    # Batch the pip installation to avoid sequential overhead
    dep_paths = [str(deps_dir / dep) for dep in core_dependencies_from_source]
    session.install(*dep_paths, "--no-deps", "--ignore-installed")

    for dep in core_dependencies_from_source:
        dep_path = str(deps_dir / dep)
        print(f"Installed {dep} locally from {dep_path}")

    session.run(
        "py.test",
        "tests/unit",
    )
