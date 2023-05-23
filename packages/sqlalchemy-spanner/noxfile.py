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
import nox
import os

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


BLACK_VERSION = "black==22.3.0"
BLACK_PATHS = ["google", "test", "noxfile.py", "setup.py", "samples"]
DEFAULT_PYTHON_VERSION = "3.8"


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
    session.run(
        "flake8",
        "google",
        "test",
        "--max-line-length=88",
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
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


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def compliance_test_13(session):
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
        "pytest-cov",
    )

    session.install("mock")
    session.install("-e", ".[tracing]")
    session.run("pip", "install", "sqlalchemy>=1.1.13,<=1.3.24", "--force-reinstall")
    session.run("pip", "install", "opentelemetry-api<=1.10", "--force-reinstall")
    session.run("pip", "install", "opentelemetry-sdk<=1.10", "--force-reinstall")
    session.run("python", "create_test_database.py")
    session.run("pip", "install", "pytest==6.2.2", "--force-reinstall")
    session.run(
        "pip", "install", "pytest-asyncio<0.21.0", "--force-reinstall", "--no-deps"
    )

    session.run(
        "py.test",
        "--cov=google.cloud.sqlalchemy_spanner",
        "--cov=test",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        "--asyncio-mode=auto",
        "test/test_suite_13.py",
        *session.posargs,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
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
    session.install("-e", ".[tracing]")
    session.run("pip", "install", "sqlalchemy>=1.4,<2.0", "--force-reinstall")
    session.run("python", "create_test_database.py")
    session.run(
        "py.test",
        "--cov=google.cloud.sqlalchemy_spanner",
        "--cov=test",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        "--asyncio-mode=auto",
        "test/test_suite_14.py",
        *session.posargs,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
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
    session.install("-e", ".[tracing]")
    session.run("pip", "install", "opentelemetry-api<=1.10", "--force-reinstall")
    session.run("python", "create_test_database.py")

    session.install("sqlalchemy>=2.0")

    session.run(
        "py.test",
        "--cov=google.cloud.sqlalchemy_spanner",
        "--cov=test",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        "--asyncio-mode=auto",
        "test/test_suite_20.py",
        *session.posargs,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def unit(session):
    """Run unit tests."""
    # Run SQLAlchemy dialect compliance test suite with OpenTelemetry.
    session.install("pytest")
    session.install("mock")
    session.install("-e", ".")
    session.install("opentelemetry-api==1.1.0")
    session.install("opentelemetry-sdk==1.1.0")
    session.install("opentelemetry-instrumentation==0.20b0")
    session.run("python", "create_test_config.py", "my-project", "my-instance")
    session.run("py.test", "--quiet", os.path.join("test/unit"), *session.posargs)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def migration_test(session):
    """Test migrations with SQLAlchemy v1.3.11+ and Alembic"""
    session.run("pip", "install", "sqlalchemy>=1.3.11,<2.0", "--force-reinstall")
    _migration_test(session)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def migration_test_1310(session):
    """Test migrations with SQLAlchemy 1.3.10 or lower and Alembic"""
    session.run("pip", "install", "sqlalchemy>=1.1.13,<=1.3.10", "--force-reinstall")
    _migration_test(session)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def _migration_test(session):
    """Migrate with SQLAlchemy and Alembic and check the result."""
    import glob
    import os
    import shutil

    try:
        import sqlalchemy
    except:
        session.run("pip", "install", "sqlalchemy>=1.3.11,<2.0", "--force-reinstall")

    session.install("pytest")
    session.install("-e", ".")
    session.install("alembic")

    session.run("python", "create_test_database.py")

    project = os.getenv(
        "GOOGLE_CLOUD_PROJECT",
        os.getenv("PROJECT_ID", "emulator-test-project"),
    )
    db_url = (
        f"spanner+spanner:///projects/{project}/instances/"
        "sqlalchemy-dialect-test/databases/compliance-test"
    )

    config = configparser.ConfigParser()
    if os.path.exists("test.cfg"):
        config.read("test.cfg")
    else:
        config.read("setup.cfg")
    db_url = config.get("db", "default", fallback=db_url)

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


@nox.session(python=DEFAULT_PYTHON_VERSION)
def snippets(session):
    """Run the documentation example snippets."""
    # Sanity check: Only run snippets system tests if the environment variable
    # is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""):
        session.skip("Credentials must be set via environment variable.")

    session.install("pytest")
    session.install("sqlalchemy>=1.4,<2.0")
    session.install(
        "git+https://github.com/googleapis/python-spanner.git#egg=google-cloud-spanner"
    )
    session.install("-e", ".")
    session.run("python", "create_test_database.py")
    session.run(
        "py.test",
        "--quiet",
        os.path.join("samples", "snippets_test.py"),
        *session.posargs,
    )
