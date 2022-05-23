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

from __future__ import print_function

import glob
import os
from pathlib import Path
import sys
from typing import Callable, Dict, List, Optional

import nox


TEST_CONFIG = {
    # You can opt out from the test for specific Python versions.
    "ignored_versions": ["2.7"],
    # Old samples are opted out of enforcing Python type hints
    # All new samples should feature them
    "enforce_type_hints": False,
    # An envvar key for determining the project id to use. Change it
    # to 'BUILD_SPECIFIC_GCLOUD_PROJECT' if you want to opt in using a
    # build specific Cloud project. You can also use your own string
    # to use your own Cloud project.
    "gcloud_project_env": "GOOGLE_CLOUD_PROJECT",
    # 'gcloud_project_env': 'BUILD_SPECIFIC_GCLOUD_PROJECT',
    # A dictionary you want to inject into your test. Don't put any
    # secrets here. These values will override predefined values.
    "envs": {},
}

# Linting with flake8.


def _determine_local_import_names(start_dir: str) -> List[str]:
    """Determines all import names that should be considered "local".

    This is used when running the linter to insure that import order is
    properly checked.
    """
    file_ext_pairs = [os.path.splitext(path) for path in os.listdir(start_dir)]
    return [
        basename
        for basename, extension in file_ext_pairs
        if extension == ".py"
        or os.path.isdir(os.path.join(start_dir, basename))
        and basename not in ("__pycache__")
    ]


#
# We ignore the following rules:
#   E203: whitespace before ‘:’
#   E266: too many leading ‘#’ for block comment
#   E501: line too long
#   I202: Additional newline in a section of imports
#
# We also need to specify the rules which are ignored by default:
# ['E226', 'W504', 'E126', 'E123', 'W503', 'E24', 'E704', 'E121']

DEFAULT_PYTHON_VERSION = "3.9"
BLACK_PATHS = ["./deployable/python"]
BLACK_VERSION = "black==19.10b0"


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION)
    black_files = []
    for target in BLACK_PATHS:
        black_files += [
            f"{target}/{path}" for path in os.listdir(target) if path.endswith(".py")
        ]
    session.run(
        "black",
        "--check",
        *black_files,
    )
    session.run(
        "flake8",
        "--exclude=deployable/python/python-logging",
        *BLACK_PATHS,
    )


#
# Black
#


@nox.session
def blacken(session: nox.sessions.Session) -> None:

    session.install("black")
    black_files = []
    for target in BLACK_PATHS:
        black_files += [
            f"{target}/{path}" for path in os.listdir(target) if path.endswith(".py")
        ]

    session.run("black", *black_files)


# Environment Tests


@nox.session(python=DEFAULT_PYTHON_VERSION)
@nox.parametrize(
    "platform",
    [
        "compute",
        "appengine_standard",
        "appengine_flex_python",
        "appengine_flex_container",
        "appengine_flex",
        "kubernetes",
        "cloudrun",
        "functions",
    ],
)
@nox.parametrize("language", ["python", "go", "nodejs", "java"])
def tests(session, language, platform):
    """Run the e2e environment test suite."""
    if os.environ.get("RUN_ENV_TESTS", "true") == "false":
        session.skip("RUN_ENV_TESTS is set to false, skipping")
    # Sanity check: Only run tests if the environment variable is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""):
        session.skip("Credentials must be set via environment variable")

    # Use pre-release gRPC for system tests.
    session.install("--pre", "grpcio")

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    session.install(
        "mock",
        "pytest",
        "google-cloud-testutils",
        "google-cloud-bigquery",
        "google-cloud-pubsub",
        "google-cloud-storage",
        "google-cloud-testutils",
        "google-cloud-logging",
        "pandas",
    )

    test_path = f"./tests/{language}/test_{platform}.py"
    if os.path.exists(test_path):
        session.run("py.test", "-s", test_path, *session.posargs)
    else:
        print(f"not implemented: {test_path}")
        exit(1)
