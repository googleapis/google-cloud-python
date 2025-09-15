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

import argparse
import multiprocessing
import os
import pathlib
import re
import shutil
import time
from typing import Dict, List

import nox
import nox.sessions

BLACK_VERSION = "black==22.3.0"
FLAKE8_VERSION = "flake8==7.1.2"
ISORT_VERSION = "isort==5.12.0"
MYPY_VERSION = "mypy==1.15.0"

# TODO: switch to 3.13 once remote functions / cloud run adds a runtime for it (internal issue 333742751)
LATEST_FULLY_SUPPORTED_PYTHON = "3.12"

# Notebook tests should match colab and BQ Studio.
# Check with import sys; sys.version_info
# on a fresh notebook runtime.
COLAB_AND_BQ_STUDIO_PYTHON_VERSIONS = [
    # BQ Studio
    "3.10",
    # colab.research.google.com
    "3.11",
]

# pytest-retry is not yet compatible with pytest 8.x.
# https://github.com/str0zzapreti/pytest-retry/issues/32
PYTEST_VERSION = "pytest<8.0.0dev"
SPHINX_VERSION = "sphinx==4.5.0"
LINT_PATHS = [
    "docs",
    "bigframes",
    "scripts",
    "tests",
    "third_party",
    "noxfile.py",
    "setup.py",
]

DEFAULT_PYTHON_VERSION = "3.10"

# Cloud Run Functions supports Python versions up to 3.12
# https://cloud.google.com/run/docs/runtimes/python
E2E_TEST_PYTHON_VERSION = "3.12"

UNIT_TEST_PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]
UNIT_TEST_STANDARD_DEPENDENCIES = [
    "mock",
    "asyncmock",
    PYTEST_VERSION,
    "pytest-asyncio",
    "pytest-cov",
    "pytest-mock",
    "pytest-timeout",
]
UNIT_TEST_LOCAL_DEPENDENCIES: List[str] = []
UNIT_TEST_DEPENDENCIES: List[str] = []
UNIT_TEST_EXTRAS: List[str] = ["tests"]
UNIT_TEST_EXTRAS_BY_PYTHON: Dict[str, List[str]] = {
    "3.10": ["tests", "scikit-learn", "anywidget"],
    "3.11": ["tests", "polars", "scikit-learn", "anywidget"],
    # Make sure we leave some versions without "extras" so we know those
    # dependencies are actually optional.
    "3.13": ["tests", "polars", "scikit-learn", "anywidget"],
}

# 3.11 is used by colab.
# 3.10 is needed for Windows tests as it is the only version installed in the
# bigframes-windows container image. For more information, search
# bigframes/windows-docker, internally.
SYSTEM_TEST_PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.13"]
SYSTEM_TEST_STANDARD_DEPENDENCIES = [
    "jinja2",
    "mock",
    "openpyxl",
    PYTEST_VERSION,
    "pytest-cov",
    "pytest-retry",
    "pytest-timeout",
    "pytest-xdist",
    "google-cloud-testutils",
    "tabulate",
    "xarray",
]
SYSTEM_TEST_EXTERNAL_DEPENDENCIES = [
    "google-cloud-bigquery",
]
SYSTEM_TEST_LOCAL_DEPENDENCIES: List[str] = []
SYSTEM_TEST_DEPENDENCIES: List[str] = []
SYSTEM_TEST_EXTRAS: List[str] = ["tests"]
SYSTEM_TEST_EXTRAS_BY_PYTHON: Dict[str, List[str]] = {
    # Make sure we leave some versions without "extras" so we know those
    # dependencies are actually optional.
    "3.10": ["tests", "scikit-learn", "anywidget"],
    "3.11": ["tests", "scikit-learn", "polars", "anywidget"],
    "3.13": ["tests", "polars", "anywidget"],
}

LOGGING_NAME_ENV_VAR = "BIGFRAMES_PERFORMANCE_LOG_NAME"

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

# Sessions are executed in the order so putting the smaller sessions
# ahead to fail fast at presubmit running.
nox.options.sessions = [
    "system-3.9",  # No extras.
    "system-3.11",
    "cover",
    # TODO(b/401609005): remove
    "cleanup",
]

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install(FLAKE8_VERSION, BLACK_VERSION, ISORT_VERSION)
    session.run(
        "isort",
        "--check",
        *LINT_PATHS,
    )
    session.run(
        "black",
        "--check",
        *LINT_PATHS,
    )
    session.run("flake8", *LINT_PATHS)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black. Format code to uniform standard."""
    session.install(BLACK_VERSION)
    session.run(
        "black",
        *LINT_PATHS,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def format(session):
    """
    Run isort to sort imports. Then run black
    to format code to uniform standard.
    """
    session.install(BLACK_VERSION, ISORT_VERSION)
    # Use the --fss option to sort imports using strict alphabetical order.
    # See https://pycqa.github.io/isort/docs/configuration/options.html#force-sort-within-sections
    session.run(
        "isort",
        *LINT_PATHS,
    )
    session.run(
        "black",
        *LINT_PATHS,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")

    session.install("twine", "wheel")
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    session.run("python", "setup.py", "sdist")
    session.run(
        "python", "-m", "twine", "check", *pathlib.Path("dist").glob("*.tar.gz")
    )


def install_unittest_dependencies(session, install_test_extra, *constraints):
    standard_deps = UNIT_TEST_STANDARD_DEPENDENCIES + UNIT_TEST_DEPENDENCIES
    session.install(*standard_deps, *constraints)

    if UNIT_TEST_LOCAL_DEPENDENCIES:
        session.install(*UNIT_TEST_LOCAL_DEPENDENCIES, *constraints)

    if install_test_extra:
        if session.python in UNIT_TEST_EXTRAS_BY_PYTHON:
            extras = UNIT_TEST_EXTRAS_BY_PYTHON[session.python]
        else:
            extras = UNIT_TEST_EXTRAS
        session.install("-e", f".[{','.join(extras)}]", *constraints)
    else:
        session.install("-e", ".", *constraints)


def run_unit(session, install_test_extra):
    """Run the unit test suite."""
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    install_unittest_dependencies(session, install_test_extra, "-c", constraints_path)

    # Run py.test against the unit tests.
    scripts_path = "scripts"
    tests_path = os.path.join("tests", "unit")
    third_party_tests_path = os.path.join("third_party", "bigframes_vendored")
    session.run(
        "py.test",
        "--quiet",
        # Any individual test taking longer than 1 mins will be terminated.
        "--timeout=60",
        # Log 20 slowest tests
        "--durations=20",
        f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=bigframes",
        f"--cov={tests_path}",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=term-missing",
        "--cov-fail-under=0",
        tests_path,
        third_party_tests_path,
        scripts_path,
        *session.posargs,
    )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    run_unit(session, install_test_extra=True)


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS[-1])
def unit_noextras(session):
    run_unit(session, install_test_extra=False)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Run type checks with mypy."""
    # Editable mode is not compatible with mypy when there are multiple
    # package directories. See:
    # https://github.com/python/mypy/issues/10564#issuecomment-851687749
    session.install(".")

    # Just install the dependencies' type info directly, since "mypy --install-types"
    # might require an additional pass.
    deps = (
        set(
            [
                MYPY_VERSION,
                # TODO: update to latest pandas-stubs once we resolve bigframes issues.
                "pandas-stubs<=2.2.3.241126",
                "types-protobuf",
                "types-python-dateutil",
                "types-requests",
                "types-setuptools",
                "types-tabulate",
                "types-PyYAML",
                "polars",
                "anywidget",
            ]
        )
        | set(SYSTEM_TEST_STANDARD_DEPENDENCIES)
        | set(UNIT_TEST_STANDARD_DEPENDENCIES)
    )

    session.install(*deps)
    shutil.rmtree(".mypy_cache", ignore_errors=True)
    session.run(
        "mypy",
        "bigframes",
        os.path.join("tests", "system"),
        os.path.join("tests", "unit"),
        "--check-untyped-defs",
        "--explicit-package-bases",
        '--exclude="^third_party"',
    )


def install_systemtest_dependencies(session, install_test_extra, *constraints):
    # Use pre-release gRPC for system tests.
    # Exclude version 1.49.0rc1 which has a known issue.
    # See https://github.com/grpc/grpc/pull/30642
    session.install("--pre", "grpcio!=1.49.0rc1")

    session.install(*SYSTEM_TEST_STANDARD_DEPENDENCIES, *constraints)

    if SYSTEM_TEST_EXTERNAL_DEPENDENCIES:
        session.install(*SYSTEM_TEST_EXTERNAL_DEPENDENCIES, *constraints)

    if SYSTEM_TEST_LOCAL_DEPENDENCIES:
        session.install("-e", *SYSTEM_TEST_LOCAL_DEPENDENCIES, *constraints)

    if SYSTEM_TEST_DEPENDENCIES:
        session.install("-e", *SYSTEM_TEST_DEPENDENCIES, *constraints)

    if install_test_extra and SYSTEM_TEST_EXTRAS_BY_PYTHON:
        extras = SYSTEM_TEST_EXTRAS_BY_PYTHON.get(session.python, [])
    elif install_test_extra and SYSTEM_TEST_EXTRAS:
        extras = SYSTEM_TEST_EXTRAS
    else:
        extras = []

    if extras:
        session.install("-e", f".[{','.join(extras)}]", *constraints)
    else:
        session.install("-e", ".", *constraints)


def run_system(
    session: nox.sessions.Session,
    prefix_name,
    test_folder,
    *,
    check_cov=False,
    install_test_extra=True,
    print_duration=False,
    extra_pytest_options=(),
    timeout_seconds=900,
    num_workers=20,
):
    """Run the system test suite."""
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Check the value of `RUN_SYSTEM_TESTS` env var. It defaults to true.
    if os.environ.get("RUN_SYSTEM_TESTS", "true") == "false":
        session.skip("RUN_SYSTEM_TESTS is set to false, skipping")
    # Install pyopenssl for mTLS testing.
    if os.environ.get("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false") == "true":
        session.install("pyopenssl")

    install_systemtest_dependencies(session, install_test_extra, "-c", constraints_path)

    # Print out package versions for debugging.
    session.run("python", "-m", "pip", "freeze")

    # Run py.test against the system tests.
    pytest_cmd = [
        "py.test",
        "-v",
        f"-n={num_workers}",
        # Any individual test taking longer than 15 mins will be terminated.
        f"--timeout={timeout_seconds}",
        # Log 20 slowest tests
        "--durations=20",
        f"--junitxml={prefix_name}_{session.python}_sponge_log.xml",
    ]
    if print_duration:
        pytest_cmd.extend(
            [
                "--durations=0",
            ]
        )
    if check_cov:
        pytest_cmd.extend(
            [
                "--cov=bigframes",
                f"--cov={test_folder}",
                "--cov-append",
                "--cov-config=.coveragerc",
                "--cov-report=term-missing",
                "--cov-fail-under=0",
            ]
        )

    pytest_cmd.extend(extra_pytest_options)
    session.run(
        *pytest_cmd,
        *session.posargs,
        test_folder,
    )


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def system(session: nox.sessions.Session):
    """Run the system test suite."""
    run_system(
        session=session,
        prefix_name="system",
        test_folder=os.path.join("tests", "system", "small"),
        check_cov=True,
    )


@nox.session(python=LATEST_FULLY_SUPPORTED_PYTHON)
def system_noextras(session: nox.sessions.Session):
    """Run the system test suite."""
    run_system(
        session=session,
        prefix_name="system_noextras",
        test_folder=os.path.join("tests", "system", "small"),
        install_test_extra=False,
    )


@nox.session(python=LATEST_FULLY_SUPPORTED_PYTHON)
def doctest(session: nox.sessions.Session):
    """Run the system test suite."""
    run_system(
        session=session,
        prefix_name="doctest",
        extra_pytest_options=(
            "--doctest-modules",
            "third_party",
            "--ignore",
            "third_party/bigframes_vendored/ibis",
            "--ignore",
            "bigframes/core/compile/polars",
            "--ignore",
            "bigframes/testing",
            "--ignore",
            "bigframes/display/anywidget.py",
        ),
        test_folder="bigframes",
        check_cov=True,
        num_workers=5,
    )


@nox.session(python=E2E_TEST_PYTHON_VERSION)
def e2e(session: nox.sessions.Session):
    """Run the large tests in system test suite."""
    run_system(
        session=session,
        prefix_name="e2e",
        test_folder=os.path.join("tests", "system", "large"),
        print_duration=True,
    )


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS[-1])
def load(session: nox.sessions.Session):
    """Run the very large tests in system test suite."""
    run_system(
        session=session,
        prefix_name="load",
        test_folder=os.path.join("tests", "system", "load"),
        print_duration=True,
        timeout_seconds=60 * 60 * 12,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the test runs
    (including system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")

    # Create a coverage report that includes only the product code.
    omitted_paths = [
        # non-prod, unit tested
        "bigframes/core/compile/polars/*",
        "bigframes/core/compile/sqlglot/*",
        # untested
        "bigframes/streaming/*",
        # utils
        "bigframes/testing/*",
    ]

    session.run(
        "coverage",
        "report",
        "--include=bigframes/*",
        # Only unit tested
        f"--omit={','.join(omitted_paths)}",
        "--show-missing",
        "--fail-under=84",
    )

    # Make sure there is no dead code in our system test directories.
    session.run(
        "coverage",
        "report",
        "--show-missing",
        "--include=tests/system/small/*",
        # TODO(b/353775058) resume coverage to 100 when the issue is fixed.
        "--fail-under=99",
    )

    session.run("coverage", "erase")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs(session):
    """Build the docs for this library."""
    session.install("-e", ".[scikit-learn]")
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
        SPHINX_VERSION,
        "alabaster",
        "recommonmark",
        "anywidget",
    )

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)

    session.run(
        "python",
        "scripts/publish_api_coverage.py",
        "docs",
    )
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


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docfx(session):
    """Build the docfx yaml files for this library."""

    session.install("-e", ".[scikit-learn]")
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
        SPHINX_VERSION,
        "alabaster",
        "recommonmark",
        "gcp-sphinx-docfx-yaml==3.0.1",
        "anywidget",
    )

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)

    session.run(
        "python",
        "scripts/publish_api_coverage.py",
        "docs",
    )
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


def prerelease(session: nox.sessions.Session, tests_path, extra_pytest_options=()):
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

    # Ignore officially released versions of certain packages specified in
    # testing/constraints-*.txt and install a more recent, pre-release versions
    # directly
    already_installed = set()

    # PyArrow prerelease packages are published to an alternative PyPI host.
    # https://arrow.apache.org/docs/python/install.html#installing-nightly-packages
    session.install(
        "--extra-index-url",
        "https://pypi.fury.io/arrow-nightlies/",
        "--prefer-binary",
        "--pre",
        "--upgrade",
        "pyarrow",
    )
    already_installed.add("pyarrow")

    session.install(
        "--prefer-binary",
        "--pre",
        "--upgrade",
        # We exclude each version individually so that we can continue to test
        # some prerelease packages. See:
        # https://github.com/googleapis/python-bigquery-dataframes/pull/268#discussion_r1423205172
        # "pandas!=2.1.4, !=2.2.0rc0, !=2.2.0, !=2.2.1",
        "pandas",
    )
    already_installed.add("pandas")

    # Try to avoid a cap on our SQLGlot so that bigframes
    # can be integrated with SQLMesh. See:
    # https://github.com/googleapis/python-bigquery-dataframes/issues/942
    # If SQLGlot introduces something that breaks us, lets file an issue
    # upstream and/or make sure we fix bigframes to work with it.
    session.install(
        "--upgrade",
        "git+https://github.com/tobymao/sqlglot.git#egg=sqlglot",
    )
    already_installed.add("sqlglot")

    # Workaround https://github.com/googleapis/python-db-dtypes-pandas/issues/178
    session.install("--no-deps", "db-dtypes")
    already_installed.add("db-dtypes")

    # Ensure we catch breaking changes in the client libraries early.
    session.install(
        "--upgrade",
        "git+https://github.com/googleapis/python-bigquery.git#egg=google-cloud-bigquery",
    )
    already_installed.add("google-cloud-bigquery")
    session.install(
        "--upgrade",
        "-e",
        "git+https://github.com/googleapis/google-cloud-python.git#egg=google-cloud-bigquery-storage&subdirectory=packages/google-cloud-bigquery-storage",
    )
    already_installed.add("google-cloud-bigquery-storage")
    session.install(
        "--upgrade",
        "git+https://github.com/googleapis/python-bigquery-pandas.git#egg=pandas-gbq",
    )
    already_installed.add("pandas-gbq")

    session.install(
        *set(UNIT_TEST_STANDARD_DEPENDENCIES + SYSTEM_TEST_STANDARD_DEPENDENCIES),
        "-c",
        constraints_path,
    )

    # Because we test minimum dependency versions on the minimum Python
    # version, the first version we test with in the unit tests sessions has a
    # constraints file containing all dependencies and extras.
    with open(
        CURRENT_DIRECTORY
        / "testing"
        / f"constraints-{UNIT_TEST_PYTHON_VERSIONS[0]}.txt",
        encoding="utf-8",
    ) as constraints_file:
        constraints_text = constraints_file.read()

    # Ignore leading whitespace and comment lines.
    deps = [
        match.group(1)
        for match in re.finditer(
            r"^\s*(\S+)(?===\S+)", constraints_text, flags=re.MULTILINE
        )
        if match.group(1) not in already_installed
    ]

    print(already_installed)

    # We use --no-deps to ensure that pre-release versions aren't overwritten
    # by the version ranges in setup.py.
    session.install(*deps)
    session.install("--no-deps", "-e", ".")

    # Print out prerelease package versions.
    session.run("python", "-m", "pip", "freeze")

    # Run py.test against the tests.
    session.run(
        "py.test",
        "--quiet",
        "-n=20",
        # Any individual test taking longer than 10 mins will be terminated.
        "--timeout=600",
        f"--junitxml={os.path.split(tests_path)[-1]}_prerelease_{session.python}_sponge_log.xml",
        "--cov=bigframes",
        f"--cov={tests_path}",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=term-missing",
        "--cov-fail-under=0",
        tests_path,
        *extra_pytest_options,
        *session.posargs,
    )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS[-1])
def unit_prerelease(session: nox.sessions.Session):
    """Run the unit test suite with prerelease dependencies."""
    prerelease(session, os.path.join("tests", "unit"))


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS[-1])
def system_prerelease(session: nox.sessions.Session):
    """Run the system test suite with prerelease dependencies."""
    small_tests_dir = os.path.join("tests", "system", "small")

    # Let's exclude remote function tests from the prerelease tests, since the
    # some of the package dependencies propagate to the cloud run functions'
    # requirements.txt, and the prerelease package versions may not be available
    # in the standard pip install.
    # This would mean that we will only rely on the standard remote function
    # tests.
    small_remote_function_tests = os.path.join(
        small_tests_dir, "functions", "test_remote_function.py"
    )
    assert os.path.exists(small_remote_function_tests)

    prerelease(
        session,
        os.path.join("tests", "system", "small"),
        (f"--ignore={small_remote_function_tests}",),
    )


@nox.session(python=COLAB_AND_BQ_STUDIO_PYTHON_VERSIONS)
def notebook(session: nox.Session):
    google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not google_cloud_project:
        session.error(
            "Set GOOGLE_CLOUD_PROJECT environment variable to run notebook session."
        )

    session.install("-e", ".[all]")
    session.install(
        "pytest",
        "pytest-xdist",
        "pytest-retry",
        "nbmake",
        "google-cloud-aiplatform",
        "matplotlib",
        "seaborn",
        "anywidget",
    )

    notebooks_list = list(pathlib.Path("notebooks/").glob("*/*.ipynb"))

    denylist = [
        # Regionalized testing is manually added later.
        "notebooks/location/regionalized.ipynb",
        # These notebooks contain special colab `param {type:"string"}`
        # comments, which make it easy for customers to fill in their
        # own information.
        #
        # With the notebooks_fill_params.py script, we are able to find and
        # replace the PROJECT_ID parameter, but not the others.
        #
        # TODO(b/357904266): Test these notebooks by replacing parameters with
        # appropriate values and omitting cleanup logic that may break
        # our test infrastructure.
        "notebooks/getting_started/ml_fundamentals_bq_dataframes.ipynb",  # Needs DATASET.
        "notebooks/ml/bq_dataframes_ml_linear_regression.ipynb",  # Needs DATASET_ID.
        "notebooks/ml/bq_dataframes_ml_linear_regression_big.ipynb",  # Needs DATASET_ID.
        "notebooks/generative_ai/bq_dataframes_ml_drug_name_generation.ipynb",  # Needs CONNECTION.
        # TODO(b/332737009): investigate why we get 404 errors, even though
        # bq_dataframes_llm_code_generation creates a bucket in the sample.
        "notebooks/generative_ai/bq_dataframes_llm_code_generation.ipynb",  # Needs BUCKET_URI.
        "notebooks/generative_ai/sentiment_analysis.ipynb",  # Too slow
        "notebooks/generative_ai/bq_dataframes_llm_gemini_2.ipynb",  # Gemini 2.0 backend hasn't ready in prod.
        "notebooks/generative_ai/bq_dataframes_llm_vector_search.ipynb",  # Needs DATASET_ID.
        "notebooks/generative_ai/bq_dataframes_ml_drug_name_generation.ipynb",  # Needs CONNECTION.
        # TODO(b/366290533): to protect BQML quota
        "notebooks/generative_ai/bq_dataframes_llm_claude3_museum_art.ipynb",
        "notebooks/vertex_sdk/sdk2_bigframes_pytorch.ipynb",  # Needs BUCKET_URI.
        "notebooks/vertex_sdk/sdk2_bigframes_sklearn.ipynb",  # Needs BUCKET_URI.
        "notebooks/vertex_sdk/sdk2_bigframes_tensorflow.ipynb",  # Needs BUCKET_URI.
        # The experimental notebooks imagine features that don't yet
        # exist or only exist as temporary prototypes.
        "notebooks/experimental/ai_operators.ipynb",
        "notebooks/experimental/semantic_operators.ipynb",
        # The notebooks that are added for more use cases, such as backing a
        # blog post, which may take longer to execute and need not be
        # continuously tested.
        "notebooks/apps/synthetic_data_generation.ipynb",
        "notebooks/multimodal/multimodal_dataframe.ipynb",  # too slow
        # This anywidget notebook uses deferred execution, so it won't
        # produce metrics for the performance benchmark script.
        "notebooks/dataframes/anywidget_mode.ipynb",
    ]

    # TODO: remove exception for Python 3.13 cloud run adds a runtime for it (internal issue 333742751)
    # TODO: remove exception for Python 3.13 if nbmake adds support for
    # sys.exit(0) or pytest.skip(...).
    # See: https://github.com/treebeardtech/nbmake/issues/134
    if session.python == "3.13":
        denylist.extend(
            [
                "notebooks/getting_started/getting_started_bq_dataframes.ipynb",
                "notebooks/remote_functions/remote_function_usecases.ipynb",
                "notebooks/remote_functions/remote_function_vertex_claude_model.ipynb",
                "notebooks/remote_functions/remote_function.ipynb",
            ]
        )

    # Convert each Path notebook object to a string using a list comprehension,
    # and remove tests that we choose not to test.
    notebooks = [str(nb) for nb in notebooks_list]
    notebooks = [nb for nb in notebooks if nb not in denylist and "/kaggle/" not in nb]

    # Regionalized notebooks
    notebooks_reg = {
        "regionalized.ipynb": [
            "asia-southeast1",
            "eu",
            "europe-west4",
            "southamerica-west1",
            "us",
            "us-central1",
        ]
    }
    notebooks_reg = {
        os.path.join("notebooks/location", nb): regions
        for nb, regions in notebooks_reg.items()
    }

    # The pytest --nbmake exits silently with "no tests ran" message if
    # one of the notebook paths supplied does not exist. Let's make sure that
    # each path exists.
    for nb in notebooks + list(notebooks_reg):
        assert os.path.exists(nb), nb

    # Determine whether to enable multi-process mode based on the environment
    # variable. If BENCHMARK_AND_PUBLISH is "true", it indicates we're running
    # a benchmark, so we disable multi-process mode. If BENCHMARK_AND_PUBLISH
    # is "false", we enable multi-process mode for faster execution.
    multi_process_mode = os.getenv("BENCHMARK_AND_PUBLISH", "false") == "false"

    try:
        # Populate notebook parameters and make a backup so that the notebooks
        # are runnable.
        session.run(
            "python",
            CURRENT_DIRECTORY / "scripts" / "notebooks_fill_params.py",
            *notebooks,
        )

        processes = []
        for notebook in notebooks:
            args = (
                "python",
                "scripts/run_and_publish_benchmark.py",
                "--notebook",
                f"--benchmark-path={notebook}",
            )
            if multi_process_mode:
                process = multiprocessing.Process(
                    target=session.run,
                    args=args,
                )
                process.start()
                processes.append(process)
                # Adding a small delay between starting each
                # process to avoid potential race conditions。
                time.sleep(1)
            else:
                session.run(*args)

        for notebook, regions in notebooks_reg.items():
            for region in regions:
                region_args = (
                    "python",
                    "scripts/run_and_publish_benchmark.py",
                    "--notebook",
                    f"--benchmark-path={notebook}",
                    f"--region={region}",
                )
                if multi_process_mode:
                    process = multiprocessing.Process(
                        target=session.run,
                        args=region_args,
                    )
                    process.start()
                    processes.append(process)
                    # Adding a small delay between starting each
                    # process to avoid potential race conditions。
                    time.sleep(1)
                else:
                    session.run(*region_args)

        for process in processes:
            process.join()
    finally:
        # Prevent our notebook changes from getting checked in to git
        # accidentally.
        session.run(
            "python",
            CURRENT_DIRECTORY / "scripts" / "notebooks_restore_from_backup.py",
            *notebooks,
        )
        session.run(
            "python",
            "scripts/run_and_publish_benchmark.py",
            "--notebook",
            "--publish-benchmarks=notebooks/",
        )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def benchmark(session: nox.Session):
    session.install("-e", ".[all]")
    base_path = os.path.join("tests", "benchmark")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=1,
        help="Number of iterations to run each benchmark.",
    )
    parser.add_argument(
        "-o",
        "--output-csv",
        nargs="?",
        const=True,
        default=False,
        help=(
            "Determines whether to output results to a CSV file. If no location is provided, "
            "a temporary location is automatically generated."
        ),
    )
    parser.add_argument(
        "-b",
        "--benchmark-filter",
        nargs="+",
        help=(
            "List of file or directory names to include in the benchmarks. If not provided, "
            "all benchmarks are run."
        ),
    )

    args = parser.parse_args(session.posargs)

    benchmark_script_list: List[pathlib.Path] = []
    if args.benchmark_filter:
        for filter_item in args.benchmark_filter:
            full_path = os.path.join(base_path, filter_item)
            if os.path.isdir(full_path):
                benchmark_script_list.extend(pathlib.Path(full_path).rglob("*.py"))
            elif os.path.isfile(full_path) and full_path.endswith(".py"):
                benchmark_script_list.append(pathlib.Path(full_path))
            else:
                raise ValueError(
                    f"Item {filter_item} does not match any valid file or directory"
                )
    else:
        benchmark_script_list = list(pathlib.Path(base_path).rglob("*.py"))

    try:
        for benchmark in benchmark_script_list:
            if benchmark.name in ("__init__.py", "utils.py"):
                continue
            session.run(
                "python",
                "scripts/run_and_publish_benchmark.py",
                f"--benchmark-path={benchmark}",
                f"--iterations={args.iterations}",
            )
    finally:
        session.run(
            "python",
            "scripts/run_and_publish_benchmark.py",
            f"--publish-benchmarks={base_path}",
            f"--iterations={args.iterations}",
            f"--output-csv={args.output_csv}",
        )


@nox.session(python="3.10")
def release_dry_run(session):
    env = {}

    # If the project root is not set, then take current directory as the project
    # root. See the release script for how the project root is set/used. This is
    # specially useful when the developer runs the nox session on local machine.
    if not os.environ.get("PROJECT_ROOT") and not os.environ.get(
        "KOKORO_ARTIFACTS_DIR"
    ):
        env["PROJECT_ROOT"] = "."
    session.run(".kokoro/release-nightly.sh", "--dry-run", env=env)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cleanup(session):
    """Clean up stale and/or temporary resources in the test project."""
    google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
    cleanup_options = []
    if google_cloud_project:
        cleanup_options.append(f"--project-id={google_cloud_project}")

    # Cleanup a few stale (more than 12 hours old) temporary cloud run
    # functions created by bigframems. This will help keeping the test GCP
    # project within the "Number of functions" quota
    # https://cloud.google.com/functions/quotas#resource_limits
    recency_cutoff_hours = 12
    cleanup_count_per_location = 40
    cleanup_options.extend(
        [
            f"--recency-cutoff={recency_cutoff_hours}",
            "cleanup",
            f"--number={cleanup_count_per_location}",
        ]
    )

    session.install("-e", ".")

    session.run("python", "scripts/manage_cloud_functions.py", *cleanup_options)
