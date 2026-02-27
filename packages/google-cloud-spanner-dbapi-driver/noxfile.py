# Copyright 2026 Google LLC
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

import glob
import os
import shutil
from typing import List

import nox

DEFAULT_PYTHON_VERSION = "3.11"

TEST_PYTHON_VERSIONS: List[str] = [
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
]

FLAKE8_VERSION = "flake8>=6.1.0,<=7.3.0"
BLACK_VERSION = "black[jupyter]>=23.7.0,<25.11.0"
ISORT_VERSION = "isort>=5.11.0,<=7.0.0"

LINT_PATHS = ["google", "tests", "noxfile.py"]

# Add docs to the list of directories to format if the directory exists.
if os.path.isdir("docs"):
    LINT_PATHS.append("docs")

# Add samples to the list of directories to format if the directory exists.
if os.path.isdir("samples"):
    LINT_PATHS.append("samples")

nox.options.sessions = ["format", "lint", "unit", "system", "compliance"]

STANDARD_DEPENDENCIES = ["spannerlib-python"]

UNIT_TEST_STANDARD_DEPENDENCIES = [
    "pytest",
    "pytest-cov",
    "pytest-asyncio",
    "google-cloud-spanner",
]

SYSTEM_TEST_STANDARD_DEPENDENCIES = [
    "pytest",
]

COMPLIANCE_TEST_STANDARD_DEPENDENCIES = [
    "pytest",
]

VERBOSE = False
MODE = "--verbose" if VERBOSE else "--quiet"

DIST_DIR = "dist"

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

nox.options.sessions = ["format", "lint", "unit", "compliance", "system"]


@nox.session(python=DEFAULT_PYTHON_VERSION)
def format(session):
    """
    Run isort to sort imports. Then run black
    to format code to uniform standard.
    """
    session.install(BLACK_VERSION, ISORT_VERSION)
    session.run(
        "isort",
        "--fss",
        *LINT_PATHS,
    )
    session.run(
        "black",
        "--line-length=80",
        *LINT_PATHS,
    )


@nox.session
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install(FLAKE8_VERSION)
    session.run(
        "flake8",
        "--max-line-length=80",
        *LINT_PATHS,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "pygments", "setuptools")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=TEST_PYTHON_VERSIONS)
def unit(session):
    """Run unit tests."""

    session.install(*STANDARD_DEPENDENCIES, *UNIT_TEST_STANDARD_DEPENDENCIES)
    session.install("-e", ".")

    test_paths = (
        session.posargs if session.posargs else [os.path.join("tests", "unit")]
    )
    session.run(
        "py.test",
        MODE,
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=google",
        "--cov=tests/unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=80",
        *test_paths,
        env={},
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def compliance(session):
    """Run compliance tests."""

    # Sanity check: Only run tests if the environment variable is set.
    if not os.environ.get("SPANNER_EMULATOR_HOST", ""):
        session.skip(
            "Emulator host must be set via "
            "SPANNER_EMULATOR_HOST environment variable"
        )

    session.install(
        *STANDARD_DEPENDENCIES, *COMPLIANCE_TEST_STANDARD_DEPENDENCIES
    )
    session.install("-e", ".")

    test_paths = (
        session.posargs
        if session.posargs
        else [os.path.join("tests", "compliance")]
    )
    session.run(
        "py.test",
        MODE,
        f"--junitxml=compliance_{session.python}_sponge_log.xml",
        *test_paths,
        env={},
    )


@nox.session(python=TEST_PYTHON_VERSIONS)
def system(session):
    """Run system tests."""

    # Sanity check: Only run tests if the environment variable is set.
    if not os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS", ""
    ) and not os.environ.get("SPANNER_EMULATOR_HOST", ""):
        session.skip(
            "Credentials or emulator host must be set via environment variable"
        )

    session.install(*STANDARD_DEPENDENCIES, *SYSTEM_TEST_STANDARD_DEPENDENCIES)
    session.install("-e", ".")

    test_paths = (
        session.posargs
        if session.posargs
        else [os.path.join("tests", "system")]
    )
    session.run(
        "py.test",
        MODE,
        f"--junitxml=system_{session.python}_sponge_log.xml",
        *test_paths,
        env={},
    )


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
    session.install("-e", ".")
