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

# Helpful notes for local usage:
#   unset PYENV_VERSION
#   pyenv local 3.14.1 3.13.10 3.12.11 3.11.4 3.10.12 3.9.17
#   PIP_INDEX_URL=https://pypi.org/simple nox

from __future__ import absolute_import
import os
import pathlib
import re
import shutil
import unittest

# https://github.com/google/importlab/issues/25
import nox


BLACK_VERSION = "black==23.7.0"
BLACK_PATHS = ["docs", "google", "tests", "noxfile.py", "setup.py"]
# Black and flake8 clash on the syntax for ignoring flake8's F401 in this file.
BLACK_EXCLUDES = ["--exclude", "^/google/api_core/operations_v1/__init__.py"]

ALL_PYTHON = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]
SUPPORTED_PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]

DEFAULT_PYTHON_VERSION = "3.14"
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()


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
        if constraints_deps:
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
            "pyasn1",
            "cryptography",
            "cachetools",
        ]
        session.install(*other_deps)


def install_core_deps_dependencies(session, constraints_path):
    with open(constraints_path, encoding="utf-8") as constraints_file:
        constraints_text = constraints_file.read()
        # Ignore leading whitespace and comment lines.
        constraints_deps = [
            match.group(1)
            for match in re.finditer(
                r"^\s*(\S+)(?===\S+)", constraints_text, flags=re.MULTILINE
            )
        ]
        if constraints_deps:
            session.install(*constraints_deps)

        # Note: If a dependency is added to the `core_dependencies_from_source` list,
        # the `prerel_deps` list in the `install_prerelease_dependencies` method should also be updated.
        core_dependencies_from_source = [
            "googleapis-common-protos @ git+https://github.com/googleapis/google-cloud-python#egg=googleapis-common-protos&subdirectory=packages/googleapis-common-protos",
            "google-auth @ git+https://github.com/googleapis/google-auth-library-python.git",
            "grpc-google-iam-v1 @ git+https://github.com/googleapis/google-cloud-python#egg=grpc-google-iam-v1&subdirectory=packages/grpc-google-iam-v1",
            "proto-plus @ git+https://github.com/googleapis/proto-plus-python.git",
        ]

        for dep in core_dependencies_from_source:
            session.install(dep, "--no-deps", "--ignore-installed")
            print(f"Installed {dep}")

        # Remaining dependencies
        other_deps = [
            "requests",
            "pyasn1",
            "cryptography",
            "cachetools",
        ]
        session.install(*other_deps)


def default(
    session,
    install_grpc=True,
    prerelease=False,
    install_async_rest=False,
    install_deps_from_source=False,
):
    """Default unit test session.

    This is intended to be run **without** an interpreter set, so
    that the current ``python`` (on the ``PATH``) or the version of
    Python corresponding to the ``nox`` binary can run the tests.
    """
    if prerelease and not install_grpc:
        unittest.skip("The pre-release session cannot be run without grpc")

    session.install(
        "pytest",
        "pytest-cov",
        "pytest-mock",
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
            f"{constraints_dir}/constraints-{constraints_type}{SUPPORTED_PYTHON_VERSIONS[0]}.txt",
        )
        # This *must* be the last install command to get the package from source.
        session.install("-e", lib_with_extras, "--no-deps")
    elif install_deps_from_source:
        install_core_deps_dependencies(
            session,
            f"{constraints_dir}/constraints-{constraints_type}{SUPPORTED_PYTHON_VERSIONS[0]}.txt",
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


@nox.session(python=ALL_PYTHON)
@nox.parametrize(
    ["install_grpc", "install_async_rest", "python_versions", "legacy_proto"],
    [
        (True, False, None, None),  # Run unit tests with grpcio installed
        (False, False, None, None),  # Run unit tests without grpcio installed
        (
            True,
            True,
            None,
            None,
        ),  # Run unit tests with grpcio and async rest installed
        # TODO: Remove once we stop support for protobuf 4.x.
        (
            True,
            False,
            ["3.9", "3.10", "3.11"],
            4,
        ),  # Run proto4 tests with grpcio/grpcio-gcp installed
    ],
)
def unit(
    session, install_grpc, install_async_rest, python_versions=None, legacy_proto=None
):
    """Run the unit test suite with the given configuration parameters.

    If `python_versions` is provided, the test suite only runs when the Python version (xx.yy) is
    one of the values in `python_versions`.

    If `legacy_proto` is provided, this test suite will explicitly install the proto library at
    that major version. Only a few values are supported at any one time; the intent is to test
    deprecated but noyet abandoned versions.
    """
    if session.python in (
        "3.7",
        "3.8",
    ):
        session.skip("Python 3.7/3.8 is no longer supported")

    if python_versions and session.python not in python_versions:
        session.log(f"Skipping session for Python {session.python}")
        session.skip()

    # TODO: consider converting the following into a `match` statement once
    # we drop Python 3.9 support.
    if legacy_proto:
        if legacy_proto == 4:
            # Pin protobuf to a 4.x version to ensure coverage for the legacy code path.
            session.install("protobuf>=4.25.8,<5.0.0")
        else:
            assert False, f"Unknown legacy_proto: {legacy_proto}"

    default(
        session=session,
        install_grpc=install_grpc,
        install_async_rest=install_async_rest,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def prerelease_deps(session):
    """Run the test suite installing pre-release versions of dependencies."""
    default(session, prerelease=True)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def core_deps_from_source(session):
    """Run the test suite installing dependencies from source."""
    default(session, prerelease=True)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""

    session.install("docutils", "Pygments", "setuptools")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Run type-checking."""
    session.install(".[grpc,async_rest]", "mypy")
    session.install(
        "types-setuptools",
        "types-requests",
        "types-protobuf",
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
