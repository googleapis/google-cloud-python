# Copyright 2016 Google LLC
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

from __future__ import absolute_import
import os
import pathlib
import re
import shutil
import unittest

# https://github.com/google/importlab/issues/25
import nox  # pytype: disable=import-error


BLACK_VERSION = "black==22.3.0"
BLACK_PATHS = ["docs", "google", "tests", "noxfile.py", "setup.py"]
# Black and flake8 clash on the syntax for ignoring flake8's F401 in this file.
BLACK_EXCLUDES = ["--exclude", "^/google/api_core/operations_v1/__init__.py"]

PYTHON_VERSIONS = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]

DEFAULT_PYTHON_VERSION = "3.10"
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

# 'docfx' is excluded since it only needs to run in 'docs-presubmit'
nox.options.sessions = [
    "unit",
    "unit_grpc_gcp",
    "unit_wo_grpc",
    "unit_w_prerelease_deps",
    "unit_w_async_rest_extra",
    "cover",
    "pytype",
    "mypy",
    "lint",
    "lint_setup_py",
    "blacken",
    "docs",
]

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION)
    session.install(".")
    session.run(
        "black",
        "--check",
        *BLACK_EXCLUDES,
        *BLACK_PATHS,
    )
    session.run("flake8", "google", "tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black.

    Format code to uniform standard.
    """
    session.install(BLACK_VERSION)
    session.run("black", *BLACK_EXCLUDES, *BLACK_PATHS)


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
            "google-auth",
            "googleapis-common-protos",
            "grpcio",
            "grpcio-status",
            "proto-plus",
            "protobuf",
        ]

        for dep in prerel_deps:
            session.install("--pre", "--no-deps", "--upgrade", dep)

        # Remaining dependencies
        other_deps = [
            "requests",
        ]
        session.install(*other_deps)


def default(session, install_grpc=True, prerelease=False, install_async_rest=False):
    """Default unit test session.

    This is intended to be run **without** an interpreter set, so
    that the current ``python`` (on the ``PATH``) or the version of
    Python corresponding to the ``nox`` binary the ``PATH`` can
    run the tests.
    """
    if prerelease and not install_grpc:
        unittest.skip("The pre-release session cannot be run without grpc")

    session.install(
        "dataclasses",
        "mock; python_version=='3.7'",
        "pytest",
        "pytest-cov",
        "pytest-xdist",
    )

    install_extras = []
    if install_grpc:
        # Note: The extra is called `grpc` and not `grpcio`.
        install_extras.append("grpc")

    constraints_dir = str(CURRENT_DIRECTORY / "testing")
    if install_async_rest:
        install_extras.append("async_rest")
        constraints_type = "async-rest-"
    else:
        constraints_type = ""

    lib_with_extras = f".[{','.join(install_extras)}]" if len(install_extras) else "."
    if prerelease:
        install_prerelease_dependencies(
            session,
            f"{constraints_dir}/constraints-{constraints_type}{PYTHON_VERSIONS[0]}.txt",
        )
        # This *must* be the last install command to get the package from source.
        session.install("-e", lib_with_extras, "--no-deps")
    else:
        constraints_file = (
            f"{constraints_dir}/constraints-{constraints_type}{session.python}.txt"
        )
        # fall back to standard constraints file
        if not pathlib.Path(constraints_file).exists():
            constraints_file = f"{constraints_dir}/constraints-{session.python}.txt"

        session.install(
            "-e",
            lib_with_extras,
            "-c",
            constraints_file,
        )

    # Print out package versions of dependencies
    session.run(
        "python", "-c", "import google.protobuf; print(google.protobuf.__version__)"
    )
    # Support for proto.version was added in v1.23.0
    # https://github.com/googleapis/proto-plus-python/releases/tag/v1.23.0
    session.run(
        "python",
        "-c",
        """import proto; hasattr(proto, "version") and print(proto.version.__version__)""",
    )
    if install_grpc:
        session.run("python", "-c", "import grpc; print(grpc.__version__)")
    session.run("python", "-c", "import google.auth; print(google.auth.__version__)")

    pytest_args = [
        "python",
        "-m",
        "pytest",
        *(
            # Helpful for running a single test or testfile.
            session.posargs
            or [
                "--quiet",
                "--cov=google.api_core",
                "--cov=tests.unit",
                "--cov-append",
                "--cov-config=.coveragerc",
                "--cov-report=",
                "--cov-fail-under=0",
                # Running individual tests with parallelism enabled is usually not helpful.
                "-n=auto",
                os.path.join("tests", "unit"),
            ]
        ),
    ]

    session.install("asyncmock", "pytest-asyncio")

    # Having positional arguments means the user wants to run specific tests.
    # Best not to add additional tests to that list.
    if not session.posargs:
        pytest_args.append("--cov=tests.asyncio")
        pytest_args.append(os.path.join("tests", "asyncio"))

    session.run(*pytest_args)


@nox.session(python=PYTHON_VERSIONS)
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python=PYTHON_VERSIONS)
def unit_w_prerelease_deps(session):
    """Run the unit test suite."""
    default(session, prerelease=True)


@nox.session(python=PYTHON_VERSIONS)
def unit_grpc_gcp(session):
    """
    Run the unit test suite with grpcio-gcp installed.
    `grpcio-gcp` doesn't support protobuf 4+.
    Remove extra `grpcgcp` when protobuf 3.x is dropped.
    https://github.com/googleapis/python-api-core/issues/594
    """
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    # Install grpcio-gcp
    session.install("-e", ".[grpcgcp]", "-c", constraints_path)
    # Install protobuf < 4.0.0
    session.install("protobuf<4.0.0")

    default(session)


@nox.session(python=PYTHON_VERSIONS)
def unit_wo_grpc(session):
    """Run the unit test suite w/o grpcio installed"""
    default(session, install_grpc=False)


@nox.session(python=PYTHON_VERSIONS)
def unit_w_async_rest_extra(session):
    """Run the unit test suite with the `async_rest` extra"""
    default(session, install_async_rest=True)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""

    session.install("docutils", "Pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def pytype(session):
    """Run type-checking."""
    session.install(".[grpc]", "pytype")
    session.run("pytype")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Run type-checking."""
    # TODO(https://github.com/googleapis/python-api-core/issues/799):
    # Remove mypy constraint. We should use the latest version of mypy.
    session.install(".[grpc,async_rest]", "mypy<1.15.0")
    session.install(
        "types-setuptools",
        "types-requests",
        "types-protobuf",
        "types-dataclasses",
        "types-mock; python_version=='3.7'",
    )
    session.run("mypy", "google", "tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")
    session.run("coverage", "erase")


@nox.session(python="3.10")
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".[grpc]")
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
