# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
"""Noxfile for spanner-mockserver-python package."""

import glob
import os
import pathlib
import re
import shutil
import tempfile
import warnings
from typing import Dict, List

import nox

RUFF_VERSION = "ruff==0.14.14"

LINT_PATHS = [
    "spannermockserver",
    "tests",
    "noxfile.py",
]
SKIP_PATHS = ["spannermockserver/generated"]

# Add samples to the list of directories to format if the directory exists.
if os.path.isdir("samples"):
    LINT_PATHS.append("samples")

ALL_PYTHON = [
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
]

VERBOSE = False
MODE = "--verbose" if VERBOSE else "--quiet"

DEFAULT_PYTHON_VERSION = "3.11"

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

PACKAGE_NAME = "google-cloud-spanner-mockserver"

GRPC_GENERATED_VERSION = "1.67.0"
DIST_DIR = "dist"

UNIT_TEST_STANDARD_DEPENDENCIES = [
    "mock",
    "asyncmock",
    "pytest",
    "pytest-cov",
    "pytest-asyncio",
]
UNIT_TEST_EXTERNAL_DEPENDENCIES: List[str] = []
UNIT_TEST_LOCAL_DEPENDENCIES: List[str] = []
UNIT_TEST_DEPENDENCIES: List[str] = []
UNIT_TEST_EXTRAS: List[str] = []
UNIT_TEST_EXTRAS_BY_PYTHON: Dict[str, List[str]] = {}

INTEGRATION_TEST_PYTHON_VERSIONS: List[str] = ALL_PYTHON
INTEGRATION_TEST_STANDARD_DEPENDENCIES = [
    "pytest",
    "pytest-asyncio",
    "mock",
]
INTEGRATION_TEST_EXTERNAL_DEPENDENCIES: List[str] = []
INTEGRATION_TEST_LOCAL_DEPENDENCIES: List[str] = []
INTEGRATION_TEST_DEPENDENCIES: List[str] = []
INTEGRATION_TEST_EXTRAS: List[str] = []
INTEGRATION_TEST_EXTRAS_BY_PYTHON: Dict[str, List[str]] = {}

nox.options.sessions = [
    "format",
    "lint",
    "lint_setup_py",
    "unit",
    "integration",
    "cover",
    "docs",
]

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True


@nox.session(python=ALL_PYTHON)
def mypy(session):
    """Run the type checker."""
    session.install(
        # TODO(https://github.com/googleapis/gapic-generator-python/issues/2410): Use the latest version of mypy
        "mypy<1.16.0",
        "types-requests",
        "types-protobuf",
    )
    session.install(".")
    session.run(
        "mypy",
        "-p",
        "spannermockserver",
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", RUFF_VERSION)

    # 2. Check formatting
    session.run(
        "ruff",
        "format",
        "--check",
        f"--target-version=py{ALL_PYTHON[0].replace('.', '')}",
        "--line-length=88",
        f"--exclude={','.join(SKIP_PATHS)}",
        *LINT_PATHS,
    )

    session.run("flake8", "--max-line-length=88", "spannermockserver", "tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def format(session):
    """
    Run ruff to sort imports and format code.
    """
    # 1. Install ruff (skipped automatically if you run with --no-venv)
    session.install(RUFF_VERSION)

    # 2. Run Ruff to fix imports
    # check --select I: Enables strict import sorting
    # --fix: Applies the changes automatically
    session.run(
        "ruff",
        "check",
        "--select",
        "I",
        "--fix",
        f"--target-version=py{ALL_PYTHON[0].replace('.', '')}",
        "--line-length=88",  # Standard Black line length
        f"--exclude={','.join(SKIP_PATHS)}",
        *LINT_PATHS,
    )

    # 3. Run Ruff to format code
    session.run(
        "ruff",
        "format",
        f"--target-version=py{ALL_PYTHON[0].replace('.', '')}",
        "--line-length=88",  # Standard Black line length
        f"--exclude={','.join(SKIP_PATHS)}",
        *LINT_PATHS,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("setuptools", "docutils", "pygments")
    session.run("python", "setup.py", "check", "--strict")


def install_unittest_dependencies(session, *constraints):
    standard_deps = UNIT_TEST_STANDARD_DEPENDENCIES + UNIT_TEST_DEPENDENCIES
    session.install(*standard_deps, *constraints)

    if UNIT_TEST_EXTERNAL_DEPENDENCIES:
        warnings.warn(
            "'unit_test_external_dependencies' is deprecated. Instead, please "
            "use 'unit_test_dependencies' or 'unit_test_local_dependencies'.",
            DeprecationWarning,
        )
        session.install(*UNIT_TEST_EXTERNAL_DEPENDENCIES, *constraints)

    if UNIT_TEST_LOCAL_DEPENDENCIES:
        session.install(*UNIT_TEST_LOCAL_DEPENDENCIES, *constraints)

    if UNIT_TEST_EXTRAS_BY_PYTHON:
        extras = UNIT_TEST_EXTRAS_BY_PYTHON.get(session.python, [])
    elif UNIT_TEST_EXTRAS:
        extras = UNIT_TEST_EXTRAS
    else:
        extras = []

    if extras:
        session.install("-e", f".[{','.join(extras)}]", *constraints)
    else:
        session.install("-e", ".", *constraints)


@nox.session(python=ALL_PYTHON)
def unit(session):
    # Install all test dependencies, then install this package in-place.

    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    if os.path.exists(constraints_path):
        install_unittest_dependencies(session, "-c", constraints_path)
    else:
        install_unittest_dependencies(session)

    # Run py.test against the unit tests.
    test_paths = session.posargs if session.posargs else [os.path.join("tests", "unit")]

    session.run(
        "py.test",
        MODE,
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=spannermockserver",
        "--cov=tests/unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        *test_paths,
        env={},
    )


def install_integration_test_dependencies(session, *constraints):
    session.install("--pre", "grpcio")

    session.install(*INTEGRATION_TEST_STANDARD_DEPENDENCIES, *constraints)

    if INTEGRATION_TEST_EXTERNAL_DEPENDENCIES:
        session.install(*INTEGRATION_TEST_EXTERNAL_DEPENDENCIES, *constraints)

    if INTEGRATION_TEST_LOCAL_DEPENDENCIES:
        session.install("-e", *INTEGRATION_TEST_LOCAL_DEPENDENCIES, *constraints)

    if INTEGRATION_TEST_DEPENDENCIES:
        session.install("-e", *INTEGRATION_TEST_DEPENDENCIES, *constraints)

    if INTEGRATION_TEST_EXTRAS_BY_PYTHON:
        extras = INTEGRATION_TEST_EXTRAS_BY_PYTHON.get(session.python, [])
    elif INTEGRATION_TEST_EXTRAS:
        extras = INTEGRATION_TEST_EXTRAS
    else:
        extras = []

    if extras:
        session.install("-e", f".[{','.join(extras)}]", *constraints)
    else:
        session.install("-e", ".", *constraints)


@nox.session(python=INTEGRATION_TEST_PYTHON_VERSIONS)
def integration(session):
    """Run the integration test suite."""
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    integration_test_path = os.path.join("tests", "integration.py")
    integration_test_folder_path = os.path.join("tests", "integration")

    # Check the value of `RUN_SYSTEM_TESTS` env var. It defaults to true.
    if os.environ.get("RUN_SYSTEM_TESTS", "true") == "false":
        session.skip("RUN_SYSTEM_TESTS is set to false, skipping")

    integration_test_exists = os.path.exists(integration_test_path)
    integration_test_folder_exists = os.path.exists(integration_test_folder_path)
    # Sanity check: only run tests if found.
    if not integration_test_exists and not integration_test_folder_exists:
        session.skip("Integration tests were not found")

    if os.path.exists(constraints_path):
        install_integration_test_dependencies(session, "-c", constraints_path)
    else:
        install_integration_test_dependencies(session)

    test_paths = session.posargs

    # Run py.test against the integration tests.
    if integration_test_exists and not test_paths:
        session.run(
            "py.test",
            MODE,
            f"--junitxml=integration_{session.python}_sponge_log.xml",
            integration_test_path,
        )
    if integration_test_folder_exists and not test_paths:
        session.run(
            "py.test",
            MODE,
            f"--junitxml=integration_{session.python}_sponge_log.xml",
            integration_test_folder_path,
        )
    if test_paths:
        session.run(
            "py.test",
            MODE,
            f"--junitxml=integration_{session.python}_sponge_log.xml",
            *test_paths,
        )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not integration test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")

    session.run("coverage", "erase")


@nox.session(python=DEFAULT_PYTHON_VERSION)
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


@nox.session(python=DEFAULT_PYTHON_VERSION)
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


def post_process_generated_files(target_dir):
    """
    Post-process generated gRPC files to use google-cloud-spanner types.
    """
    for file_name in os.listdir(target_dir):
        if not file_name.endswith("_grpc.py"):
            continue

        file_path = os.path.join(target_dir, file_name)
        with open(file_path, "r") as f:
            content = f.read()

        # Replace imports
        # Spanner v1
        content = re.sub(
            r"from google\.spanner\.v1 import (\w+)_pb2 as "
            r"google_dot_spanner_dot_v1_dot_(\w+)__pb2",
            r"from google.cloud.spanner_v1.types import \1 as "
            r"google_dot_spanner_dot_v1_dot_\2__pb2",
            content,
        )

        # Database Admin v1
        content = re.sub(
            r"from google\.spanner\.admin\.database\.v1 import (\w+)_pb2 as "
            r"google_dot_spanner_dot_admin_dot_database_dot_v1_dot_(\w+)__pb2",
            r"from google.cloud.spanner_admin_database_v1.types import \1 as "
            r"google_dot_spanner_dot_admin_dot_database_dot_v1_dot_\2__pb2",
            content,
        )

        # Replace serialization methods for Spanner types
        content = re.sub(
            r"(google_dot_spanner_dot_[a-zA-Z0-9_]+__pb2\.[a-zA-Z0-9_]+)"
            r"\.SerializeToString",
            r"\1.serialize",
            content,
        )
        content = re.sub(
            r"(google_dot_spanner_dot_[a-zA-Z0-9_]+__pb2\.[a-zA-Z0-9_]+)"
            r"\.FromString",
            r"\1.deserialize",
            content,
        )

        with open(file_path, "w") as f:
            f.write(content)


@nox.session
def generate_grpc(session):
    """
    Generate gRPC code from googleapis.
    """
    session.install(f"grpcio-tools=={GRPC_GENERATED_VERSION}")

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Clone googleapis
        session.log("Cloning googleapis...")
        session.run(
            "git",
            "clone",
            "--depth",
            "1",
            "https://github.com/googleapis/googleapis.git",
            f"{tmp_dir}/googleapis",
            external=True,
        )

        googleapis_dir = os.path.join(tmp_dir, "googleapis")
        proto_files = glob.glob(
            os.path.join(googleapis_dir, "google/spanner/v1/*.proto")
        ) + glob.glob(
            os.path.join(googleapis_dir, "google/spanner/admin/database/v1/*.proto")
        )
        proto_files_rel = [os.path.relpath(p, googleapis_dir) for p in proto_files]

        # Run protoc
        session.log("Generating code...")
        with session.chdir(googleapis_dir):
            session.run(
                "python",
                "-m",
                "grpc_tools.protoc",
                "-I",
                ".",
                "--python_out=.",
                "--pyi_out=.",
                "--grpc_python_out=.",
                *proto_files_rel,
            )

        target_dir = os.path.join(os.getcwd(), "spannermockserver", "generated")

        files_to_copy = {
            "spanner_pb2_grpc.py": os.path.join(
                googleapis_dir, "google", "spanner", "v1"
            ),
            "spanner_database_admin_pb2_grpc.py": os.path.join(
                googleapis_dir, "google", "spanner", "admin", "database", "v1"
            ),
        }

        for file_name, source_dir in files_to_copy.items():
            src = os.path.join(source_dir, file_name)
            dst = os.path.join(target_dir, file_name)
            shutil.copy(src, dst)
            session.log(f"Copied {file_name} to {target_dir}")

        post_process_generated_files(target_dir)
        session.log("Post-processed generated files.")


@nox.session
def build(session):
    """
    Prepares the platform-specific artifacts and builds the wheel.
    """
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)

    # Install build dependencies
    session.install("build", "twine")

    # Build the wheel
    session.log("Building...")
    session.run("python", "-m", "build")

    # Check the built artifacts with twine
    session.log("Checking artifacts with twine...")
    artifacts = glob.glob("dist/*")
    if not artifacts:
        session.error("No built artifacts found in dist/ to check.")

    session.run("twine", "check", *artifacts)


@nox.session
def install(session):
    """
    Install locally
    """
    build(session)
    session.install("-e", ".")
