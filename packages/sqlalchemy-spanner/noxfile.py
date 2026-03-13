# -*- coding: utf-8 -*-
#
# Copyright 2021 Google LLC
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

import configparser
import os
import shutil

import nox

ALEMBIC_CONF = """
[alembic]
script_location = test_migration
prepend_sys_path = .
sqlalchemy.url = {}
[post_write_hooks]
[loggers]
keys = root,sqlalchemy,alembic
[handlers]
keys = console
[formatters]
keys = generic
[logger_root]
level = WARN
handlers = console
qualname =
[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine
[logger_alembic]
level = INFO
handlers =
qualname = alembic
[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic
[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""

UPGRADE_CODE = """def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )
    op.alter_column(
        'account',
        'name',
        existing_type=sa.String(70),
    )
    op.alter_column(
        'account',
        'description',
        existing_type=sa.Unicode(200),
        nullable=False,
    )
    """


BLACK_VERSION = "black==23.7.0"
ISORT_VERSION = "isort==5.11.0"
BLACK_PATHS = ["google", "tests", "noxfile.py", "setup.py", "samples"]
UNIT_TEST_PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]
ALL_PYTHON = list(UNIT_TEST_PYTHON_VERSIONS)
ALL_PYTHON.extend(["3.7"])
SYSTEM_TEST_PYTHON_VERSIONS = ["3.12"]
SYSTEM_COMPLIANCE_MIGRATION_TEST_PYTHON_VERSIONS = ["3.8", "3.12", "3.14"]
DEFAULT_PYTHON_VERSION = "3.14"
DEFAULT_PYTHON_VERSION_FOR_SQLALCHEMY_20 = "3.14"


nox.options.sessions = [
    "system",
    "compliance_test_14",
    "compliance_test_20",
    "migration_test",
    "_migration_test",
    "mockserver",
]

@nox.session(python=DEFAULT_PYTHON_VERSION_FOR_SQLALCHEMY_20)
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
    session.run(
        "flake8",
        "google",
        "tests",
        "--max-line-length=88",
    )


@nox.session(python=DEFAULT_PYTHON_VERSION_FOR_SQLALCHEMY_20)
def blacken(session):
    """Run black.

    Format code to uniform standard.

    This currently uses Python 3.6 due to the automated Kokoro run of synthtool.
    That run uses an image that doesn't have 3.6 installed. Before updating this
    check the state of the `gcp_ubuntu_config` we use for that Kokoro run.
    """
    session.install(BLACK_VERSION)
    session.run(
        "black",
        *BLACK_PATHS,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION_FOR_SQLALCHEMY_20)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "pygments", "setuptools")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS[0])
def compliance_test_14(session):
    """Run SQLAlchemy dialect compliance test suite."""

    # Check the value of `RUN_COMPLIANCE_TESTS` env var. It defaults to true.
    if os.environ.get("RUN_COMPLIANCE_TESTS", "true") == "false":
        session.skip("RUN_COMPLIANCE_TESTS is set to false, skipping")
    # Sanity check: Only run tests if the environment variable is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "") and not os.environ.get(
        "SPANNER_EMULATOR_HOST", ""
    ):
        session.skip(
            "Credentials or emulator host must be set via environment variable"
        )

    session.install(
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
    )

    session.install("mock")
    session.install(".[tracing]")
    session.run("pip", "install", "sqlalchemy>=1.4,<2.0", "--force-reinstall")
    session.run("python", "create_test_database.py")
    session.run(
        "py.test",
        "--cov=google.cloud.sqlalchemy_spanner",
        "--cov=tests",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        "--asyncio-mode=auto",
        "tests/test_suite_14.py",
        *session.posargs,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION_FOR_SQLALCHEMY_20)
def compliance_test_20(session):
    """Run SQLAlchemy dialect compliance test suite."""

    # Check the value of `RUN_COMPLIANCE_TESTS` env var. It defaults to true.
    if os.environ.get("RUN_COMPLIANCE_TESTS", "true") == "false":
        session.skip("RUN_COMPLIANCE_TESTS is set to false, skipping")

    # Sanity check: Only run tests if the environment variable is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "") and not os.environ.get(
        "SPANNER_EMULATOR_HOST", ""
    ):
        session.skip(
            "Credentials or emulator host must be set via environment variable"
        )

    session.install(
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
    )

    session.install("mock")
    session.install("-e", ".", "--force-reinstall")
    session.run("python", "create_test_database.py")

    session.install("sqlalchemy>=2.0")

    session.run(
        "py.test",
        "--cov=google.cloud.sqlalchemy_spanner",
        "--cov=tests",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        "--asyncio-mode=auto",
        "tests/test_suite_20.py",
        *session.posargs,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION_FOR_SQLALCHEMY_20)
def mockserver(session):
    """Run mockserver tests."""
    # Run SQLAlchemy dialect tests using an in-mem mocked Spanner server.
    session.install("setuptools")
    session.install("pytest")
    session.install("mock")
    session.install(".")
    session.install("sqlalchemy>=2.0")
    session.run(
        "python",
        "create_test_config.py",
        "my-project",
        "my-instance",
        "my-database",
        "none",
        "AnonymousCredentials",
        "localhost",
        "9999",
    )
    session.run(
        "py.test", "--quiet", os.path.join("tests", "mockserver_tests"), *session.posargs
    )


@nox.session(python=SYSTEM_COMPLIANCE_MIGRATION_TEST_PYTHON_VERSIONS[0])
def migration_test(session):
    """Test migrations with SQLAlchemy v1.4 and Alembic"""
    session.run("pip", "install", "sqlalchemy>=1.4,<2.0", "--force-reinstall")
    _migration_test(session)


@nox.session(python=SYSTEM_COMPLIANCE_MIGRATION_TEST_PYTHON_VERSIONS[-1])
def _migration_test(session):
    """Migrate with SQLAlchemy and Alembic and check the result."""
    import glob
    import os
    import shutil

    session.install("pytest")
    session.install(".")
    session.install("alembic")

    session.run("python", "create_test_database.py")

    config = configparser.ConfigParser()
    if os.path.exists("test.cfg"):
        config.read("test.cfg")
    else:
        config.read("setup.cfg")
    db_url = config.get("db", "default")

    session.run("alembic", "init", "test_migration")

    # setting testing configurations
    os.remove("alembic.ini")
    with open("alembic.ini", "w") as f:
        f.write(ALEMBIC_CONF.format(db_url))

    session.run("alembic", "revision", "-m", "migration_for_test")
    files = glob.glob("test_migration/versions/*.py")

    # updating the upgrade-script code
    with open(files[0], "rb") as f:
        script_code = f.read().decode()

    script_code = script_code.replace(
        """def upgrade() -> None:\n    pass""", UPGRADE_CODE
    )
    with open(files[0], "wb") as f:
        f.write(script_code.encode())

    os.remove("test_migration/env.py")
    shutil.copyfile("test_migration_env.py", "test_migration/env.py")

    # running the test migration
    session.run("alembic", "upgrade", "head")

    # clearing the migration data
    os.remove("alembic.ini")
    shutil.rmtree("test_migration")
    session.run("python", "migration_test_cleanup.py", db_url)
    if os.path.exists("test.cfg"):
        os.remove("test.cfg")


@nox.session(python=ALL_PYTHON)
@nox.parametrize("test_type", ["unit", "mockserver"])
def unit(session, test_type):
    """Run unit tests."""
    if session.python in ("3.7",):
        session.skip("Python 3.7 is no longer supported")

    if (
        test_type == "mockserver"
        and session.python != DEFAULT_PYTHON_VERSION_FOR_SQLALCHEMY_20
    ):
        session.skip("mockserver tests only run on python 3.14")

    if test_type == "mockserver":
        mockserver(session)
        return

    if test_type == "unit":
        # Run SQLAlchemy dialect compliance test suite with OpenTelemetry.
        session.install("setuptools")
        session.install("pytest")
        session.install("mock")
        session.install(".")
        session.install("opentelemetry-api")
        session.install("opentelemetry-sdk")
        session.install("opentelemetry-instrumentation")
        session.run("py.test", "--quiet", os.path.join("tests/unit"), *session.posargs)
        return


@nox.session(python=SYSTEM_COMPLIANCE_MIGRATION_TEST_PYTHON_VERSIONS)
@nox.parametrize(
    "test_type",
    ["system", "compliance_14", "compliance_20", "migration_14", "migration_20"],
)
def system(session, test_type):
    """Run SQLAlchemy dialect system test suite."""

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "") and not os.environ.get(
        "SPANNER_EMULATOR_HOST", ""
    ):
        session.skip(
            "Credentials or emulator host must be set via environment variable"
        )

    if os.environ.get("RUN_COMPLIANCE_TESTS", "true") == "false" and not os.environ.get(
        "SPANNER_EMULATOR_HOST", ""
    ):
        session.skip("RUN_COMPLIANCE_TESTS is set to false, skipping")

    if test_type == "system" and session.python not in SYSTEM_TEST_PYTHON_VERSIONS:
        session.skip("Standard system tests configured to run exclusively on 3.12")
    if (
        test_type in ["compliance_14", "migration_14"]
        and session.python != SYSTEM_COMPLIANCE_MIGRATION_TEST_PYTHON_VERSIONS[0]
    ):
        session.skip(
            f"SQLAlchemy 1.4-based tests configured to run exclusively on {SYSTEM_COMPLIANCE_MIGRATION_TEST_PYTHON_VERSIONS[0]}"
        )
    if (
        test_type in ["compliance_20", "migration_20"]
        and session.python != DEFAULT_PYTHON_VERSION_FOR_SQLALCHEMY_20
    ):
        session.skip(
            f"SQLAlchemy 2.0-based tests configured to run exclusively on {DEFAULT_PYTHON_VERSION_FOR_SQLALCHEMY_20}"
        )

    if test_type == "system":
        session.install("pytest", "pytest-cov", "pytest-asyncio")
        session.install("mock")
        session.install(".[tracing]")
        session.install("opentelemetry-api")
        session.install("opentelemetry-sdk")
        session.install("opentelemetry-instrumentation")
        session.run("python", "create_test_database.py")
        session.install("sqlalchemy>=2.0")
        session.run(
            "py.test", "--quiet", os.path.join("tests", "system"), *session.posargs
        )
        session.run("python", "drop_test_database.py")
    elif test_type == "compliance_14":
        compliance_test_14(session)
    elif test_type == "compliance_20":
        compliance_test_20(session)
    elif test_type == "migration_14":
        migration_test(session)
    elif test_type == "migration_20":
        _migration_test(session)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Run the type checker."""
    session.skip("mypy tests are not yet supported")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def core_deps_from_source(session):
    """Run all tests with core dependencies installed from source"""
    session.skip("Core deps from source tests are not yet supported")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def prerelease_deps(session):
    """Run all tests with prerelease versions of dependencies installed."""
    session.skip("prerelease deps tests are not yet supported")


@nox.session(python="3.10")
def docs(session):
    """Build the docs for this library."""
    session.skip("docs builds are not yet supported")


@nox.session(python="3.10")
def docfx(session):
    """Build the docfx yaml files for this library."""
    session.skip("docfx builds are not yet supported")


@nox.session
def format(session: nox.sessions.Session) -> None:
    session.install(BLACK_VERSION, ISORT_VERSION)
    import os

    python_files = [path for path in os.listdir(".") if path.endswith(".py")]
    session.run("isort", "--fss", *python_files)
    session.run("black", *python_files)
