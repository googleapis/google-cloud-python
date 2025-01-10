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

import os
import pathlib
from pathlib import Path
import re
import shutil
import tempfile

import nox


BLACK_VERSION = "black==22.3.0"
LINT_PATHS = ["docs", "google", "noxfile.py", "setup.py"]


CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
UNIT_TEST_PYTHON_VERSIONS = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]

nox.options.sessions = [
    "unit_local",
    "unit_remote",
    "blacken",
    "lint_setup_py",
    "docs",
    "docfx",
    "lint",
]

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True


@nox.session(python="3.8")
def blacken(session):
    """Run black.
    Format code to uniform standard.
    This currently uses Python 3.6 due to the automated Kokoro run of synthtool.
    That run uses an image that doesn't have 3.6 installed. Before updating this
    check the state of the `gcp_ubuntu_config` we use for that Kokoro run.
    """
    session.install(BLACK_VERSION)
    session.run("black", "google", "setup.py")


@nox.session(python="3.8")
def lint_setup_py(session):
    """Verify that setup.py is valid"""
    session.install("docutils", "pygments")
    session.run("python", "setup.py", "check", "--strict")


def unit(session, repository, package, prerelease, protobuf_implementation):
    """Run the unit test suite."""
    downstream_dir = repository
    if package:
        downstream_dir = f"{repository}/packages/{package}"

    # Install all test dependencies, then install this package in-place.
    session.install("asyncmock", "pytest-asyncio")

    # Pin mock due to https://github.com/googleapis/python-pubsub/issues/840
    session.install("mock==5.0.0", "pytest", "pytest-cov")

    install_command = ["-e", f"{CURRENT_DIRECTORY}/{downstream_dir}"]

    if prerelease:
        install_prerelease_dependencies(
            session,
            f"{CURRENT_DIRECTORY}/{downstream_dir}/testing/constraints-{UNIT_TEST_PYTHON_VERSIONS[0]}.txt",
        )
        # Use the `--no-deps` options to allow pre-release versions of dependencies to be installed
        install_command.extend(["--no-deps"])
    else:
        # Install the pinned dependencies in constraints file
        install_command.extend(
            [
                "-c",
                f"{CURRENT_DIRECTORY}/{downstream_dir}/testing/constraints-{session.python}.txt",
            ]
        )

    # These *must* be the last 3 install commands to get the packages from source.
    session.install(*install_command)

    # Remove the 'cpp' implementation once support for Protobuf 3.x is dropped.
    # The 'cpp' implementation requires Protobuf<4.
    if protobuf_implementation == "cpp":
        session.install("protobuf<4")

    # Install this library from source
    session.install(CURRENT_DIRECTORY, "--no-deps")

    # Print out package versions of dependencies
    session.run(
        "python", "-c", "import google.protobuf; print(google.protobuf.__version__)"
    )
    session.run("python", "-c", "import grpc; print(grpc.__version__)")
    session.run("python", "-c", "import google.auth; print(google.auth.__version__)")

    session.run(
        "python", "-c", "import google.api_core; print(google.api_core.__version__)"
    )

    # Run py.test against the unit tests in the downstream repository
    with session.chdir(downstream_dir):
        # Run py.test against the unit tests.
        session.run(
            "py.test",
            "--quiet",
            "--cov=google/cloud",
            "--cov=tests/unit",
            "--cov-append",
            "--cov-config=.coveragerc",
            "--cov-report=",
            "--cov-fail-under=0",
            os.path.join("tests", "unit"),
            *session.posargs,
            env={
                "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": protobuf_implementation,
            },
        )


def install_prerelease_dependencies(session, constraints_path):
    with open(constraints_path, encoding="utf-8") as constraints_file:
        constraints_text = constraints_file.read()
        # Ignore leading whitespace and comment lines.
        constraints_deps = [
            match.group(1)
            for match in re.finditer(
                r"^\s*(\S+)(?===\S+)", constraints_text, flags=re.MULTILINE
            )
        ]
        session.install(*constraints_deps)
        prerel_deps = [
            "googleapis-common-protos",
            "protobuf",
            "six",
            "grpcio",
            "grpcio-status",
            "google-api-core",
            "google-auth",
            "proto-plus",
            "google-cloud-testutils",
            # dependencies of google-cloud-testutils"
            "click",
        ]

        for dep in prerel_deps:
            session.install("--pre", "--no-deps", "--upgrade", dep)

        # Remaining dependencies
        other_deps = [
            "requests",
        ]
        session.install(*other_deps)


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
@nox.parametrize(
    "library,prerelease,protobuf_implementation",
    [
        (("google-cloud-python", "google-cloud-asset"), False, "python"),
        (("google-cloud-python", "google-cloud-asset"), False, "upb"),
        (("google-cloud-python", "google-cloud-asset"), False, "cpp"),
        (("google-cloud-python", "google-cloud-asset"), True, "python"),
        (("google-cloud-python", "google-cloud-asset"), True, "upb"),
        (("google-cloud-python", "google-cloud-asset"), True, "cpp"),
    ],
)
def unit_remote(session, library, prerelease, protobuf_implementation):
    """Run tests from a downstream libraries.

    To verify that any changes we make here will not break downstream libraries, clone
    a few and run their unit and system tests.

    NOTE: The unit and system test functions above are copied from the templates.
    They will need to be updated when the templates change.

    * Asset: GAPIC which uses `google-cloud-access-context-manager`
    """

    if protobuf_implementation == "cpp" and session.python in ("3.11", "3.12"):
        session.skip("cpp implementation is not supported in python 3.11+")

    repository, package = library
    with tempfile.TemporaryDirectory() as working_dir:
        session.run(
            "git",
            "clone",
            "--single-branch",
            f"https://github.com/googleapis/{repository}",
            f"{working_dir}/{repository}",
            external=True,
        )

        downstream_dir = repository
        if package:
            downstream_dir = f"{working_dir}/{repository}/packages/{package}"

        # Install all test dependencies, then install this package in-place.
        session.install("asyncmock", "pytest-asyncio")

        session.install("mock", "pytest", "pytest-cov")

        install_command = ["-e", downstream_dir]

        if prerelease:
            install_prerelease_dependencies(
                session,
                f"{downstream_dir}/testing/constraints-{UNIT_TEST_PYTHON_VERSIONS[0]}.txt",
            )
            # Use the `--no-deps` options to allow pre-release versions of dependencies to be installed
            install_command.extend(["--no-deps"])
        else:
            # Install the pinned dependencies in constraints file
            install_command.extend(
                [
                    "-c",
                    f"{downstream_dir}/testing/constraints-{session.python}.txt",
                ]
            )

        # These *must* be the last 3 install commands to get the packages from source.
        session.install(*install_command)

        # Remove the 'cpp' implementation once support for Protobuf 3.x is dropped.
        # The 'cpp' implementation requires Protobuf<4.
        if protobuf_implementation == "cpp":
            session.install("protobuf<4")

        # Install this library from source
        session.install(CURRENT_DIRECTORY, "--no-deps")

        # Print out package versions of dependencies
        session.run(
            "python", "-c", "import google.protobuf; print(google.protobuf.__version__)"
        )
        session.run("python", "-c", "import grpc; print(grpc.__version__)")
        session.run(
            "python", "-c", "import google.auth; print(google.auth.__version__)"
        )

        session.run(
            "python", "-c", "import google.api_core; print(google.api_core.__version__)"
        )

        # Run py.test against the unit tests in the downstream repository
        with session.chdir(downstream_dir):
            # Run py.test against the unit tests.
            session.run(
                "py.test",
                "--quiet",
                "--cov=google/cloud",
                "--cov=tests/unit",
                "--cov-append",
                "--cov-config=.coveragerc",
                "--cov-report=",
                "--cov-fail-under=0",
                os.path.join("tests", "unit"),
                *session.posargs,
                env={
                    "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": protobuf_implementation,
                },
            )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
@nox.parametrize("protobuf_implementation", ["python", "upb", "cpp"])
def unit_local(session, protobuf_implementation):
    """Run tests in this local repo."""
    # Install all test dependencies, then install this package in-place.

    # TODO(https://github.com/googleapis/proto-plus-python/issues/389):
    # Remove the 'cpp' implementation once support for Protobuf 3.x is dropped.
    # The 'cpp' implementation requires Protobuf == 3.x however version 3.x
    # does not support Python 3.11 and newer. The 'cpp' implementation
    # must be excluded from the test matrix for these runtimes.
    if protobuf_implementation == "cpp" and session.python in ("3.11", "3.12"):
        session.skip("cpp implementation is not supported in python 3.11+")

    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    session.install(
        "mock",
        "asyncmock",
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "-c",
        constraints_path,
    )

    session.install("-e", ".", "-c", constraints_path)

    # Remove the 'cpp' implementation once support for Protobuf 3.x is dropped.
    # The 'cpp' implementation requires Protobuf<4.
    if protobuf_implementation == "cpp":
        session.install("protobuf<4")

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=google",
        "--cov=tests/unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        *session.posargs,
        env={
            "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": protobuf_implementation,
        },
    )


@nox.session(python="3.9")
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


@nox.session(python="3.8")
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION)
    session.run(
        "black",
        "--check",
        *LINT_PATHS,
    )
