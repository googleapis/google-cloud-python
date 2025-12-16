# -*- coding: utf-8 -*-
#
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

from __future__ import absolute_import
import os
import pathlib
import re
import shutil

import nox


BLACK_VERSION = "black==23.7.0"
BLACK_PATHS = ["docs", "google", "tests", "noxfile.py", "setup.py"]

DEFAULT_PYTHON_VERSION = "3.14"
SYSTEM_TEST_PYTHON_VERSIONS = ["3.9", "3.14"]
UNIT_TEST_PYTHON_VERSIONS = [
    "3.9",
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
]
CONFORMANCE_TEST_PYTHON_VERSIONS = ["3.12"]

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

nox.options.sessions = [
    "blacken",
    "conftest_retry",
    "docfx",
    "docs",
    "lint",
    "lint_setup_py",
    "system",
    # TODO(https://github.com/googleapis/python-storage/issues/1499):
    # Remove or restore testing for Python 3.7/3.8
    "unit-3.9",
    "unit-3.10",
    "unit-3.11",
    "unit-3.12",
    "unit-3.13",
    "unit-3.14",
    # cover must be last to avoid error `No data to report`
    "cover",
]


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    # Pin flake8 to 6.0.0
    # See https://github.com/googleapis/python-storage/issues/1102
    session.install("flake8", BLACK_VERSION)
    session.run(
        "black",
        "--check",
        *BLACK_PATHS,
    )
    session.run("flake8", "google", "tests")


@nox.session(python="3.14")
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
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "pygments", "setuptools>=79.0.1")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


def default(session, install_extras=True):
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    # Install all test dependencies, then install this package in-place.
    session.install(
        "mock",
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "brotli",
        "grpcio",
        "grpcio-status",
        "proto-plus",
        "grpc-google-iam-v1",
        "-c",
        constraints_path,
    )

    if install_extras:
        session.install("opentelemetry-api", "opentelemetry-sdk")

    session.install("-e", ".", "-c", constraints_path)

    session.run("python", "-m", "pip", "freeze")

    # This dependency is included in setup.py for backwards compatibility only
    # and the client library is expected to pass all tests without it. See
    # setup.py and README for details.
    session.run("pip", "uninstall", "-y", "google-resumable-media")

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=google.cloud.storage",
        "--cov=google.cloud",
        "--cov=tests.unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        os.path.join("tests", "resumable_media", "unit"),
        *session.posargs,
    )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def system(session):
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    """Run the system test suite."""
    rerun_count = 0

    # Check the value of `RUN_SYSTEM_TESTS` env var. It defaults to true.
    if os.environ.get("RUN_SYSTEM_TESTS", "true") == "false":
        session.skip("RUN_SYSTEM_TESTS is set to false, skipping")
    # Environment check: Only run tests if the environment variable is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""):
        session.skip(
            "Credentials must be set via environment variable GOOGLE_APPLICATION_CREDENTIALS"
        )
    # mTLS tests requires pyopenssl.
    if os.environ.get("GOOGLE_API_USE_CLIENT_CERTIFICATE", "") == "true":
        session.install("pyopenssl")
    # Check if endpoint is being overriden for rerun_count
    if (
        os.getenv("API_ENDPOINT_OVERRIDE", "https://storage.googleapis.com")
        != "https://storage.googleapis.com"
    ):
        rerun_count = 3

    # Use pre-release gRPC for system tests.
    # TODO: Remove ban of 1.52.0rc1 once grpc/grpc#31885 is resolved.
    session.install("--pre", "grpcio!=1.52.0rc1")

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    # 2021-05-06: defer installing 'google-cloud-*' to after this package,
    #             in order to work around Python 2.7 googolapis-common-protos
    #             issue.
    session.install("mock", "pytest", "pytest-rerunfailures", "-c", constraints_path)
    session.install("-e", ".", "-c", constraints_path)
    session.install(
        "google-cloud-testutils",
        "google-cloud-iam",
        "google-cloud-pubsub",
        "google-cloud-kms",
        "brotli",
        "-c",
        constraints_path,
    )

    # Run py.test against the system tests.
    session.run(
        "py.test",
        "--quiet",
        f"--junitxml=system_{session.python}_sponge_log.xml",
        "--reruns={}".format(rerun_count),
        os.path.join("tests", "system"),
        os.path.join("tests", "resumable_media", "system"),
        *session.posargs,
    )


@nox.session(python=CONFORMANCE_TEST_PYTHON_VERSIONS)
def conftest_retry(session):
    """Run the retry conformance test suite."""
    conformance_test_folder_path = os.path.join("tests", "conformance")
    conformance_test_folder_exists = os.path.exists(conformance_test_folder_path)
    # Environment check: only run tests if found.
    if not conformance_test_folder_exists:
        session.skip("Conformance tests were not found")

    # Install all test dependencies and pytest plugin to run tests in parallel.
    # Then install this package in-place.
    session.install("pytest", "pytest-xdist")
    session.install("-e", ".")

    # Run #CPU processes in parallel if no test session arguments are passed in.
    if session.posargs:
        test_cmd = [
            "py.test",
            "--quiet",
            conformance_test_folder_path,
            *session.posargs,
        ]
    else:
        test_cmd = ["py.test", "-n", "auto", "--quiet", conformance_test_folder_path]

    # Run py.test against the conformance tests.
    session.run(*test_cmd, env={"DOCKER_API_VERSION": "1.39"})


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=99")

    session.run("coverage", "erase")


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
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "html", ""),
    )


@nox.session(python="3.10")
def docfx(session):
    """Build the docfx yaml files for this library."""

    session.install("-e", ".")
    session.install("grpcio")
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


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS[-1])
@nox.parametrize(
    "protobuf_implementation",
    ["python", "upb"],
)
def prerelease_deps(session, protobuf_implementation):
    """Run all tests with prerelease versions of dependencies installed."""

    # Install all test dependencies
    session.install("mock", "pytest", "pytest-cov", "brotli")

    # Install dependencies needed for system tests
    session.install(
        "google-cloud-pubsub",
        "google-cloud-kms",
        "google-cloud-testutils",
        "google-cloud-iam",
    )

    # Install all dependencies
    session.install("-e", ".[protobuf, tracing]")

    prerel_deps = [
        "google-api-core",
        "google-auth",
        "google-cloud-core",
        "google-crc32c",
        "google-resumable-media",
        "opentelemetry-api",
        "protobuf",
    ]

    package_namespaces = {
        "google-api-core": "google.api_core",
        "google-auth": "google.auth",
        "google-cloud-core": "google.cloud.version",
        "opentelemetry-api": "opentelemetry.version",
        "protobuf": "google.protobuf",
    }

    for dep in prerel_deps:
        session.install("--pre", "--no-deps", "--upgrade", dep)
        print(f"Installed {dep}")

        version_namespace = package_namespaces.get(dep)

        if version_namespace:
            session.run(
                "python",
                "-c",
                f"import {version_namespace}; print({version_namespace}.__version__)",
            )
    # Remaining dependencies
    other_deps = [
        "requests",
    ]
    session.install(*other_deps)

    session.run(
        "py.test",
        "tests/unit",
        env={
            "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": protobuf_implementation,
        },
    )

    session.run(
        "py.test",
        "--verbose",
        f"--junitxml=system_{session.python}_sponge_log.xml",
        os.path.join("tests", "system"),
        *session.posargs,
        env={
            "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": protobuf_implementation,
        },
    )
