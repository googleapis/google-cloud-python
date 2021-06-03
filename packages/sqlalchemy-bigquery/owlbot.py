# Copyright 2021 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import pathlib

import synthtool as s
from synthtool import gcp


REPO_ROOT = pathlib.Path(__file__).parent.absolute()

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    unit_test_python_versions=["3.6", "3.7", "3.8", "3.9"],
    system_test_python_versions=["3.8", "3.9"],
    cov_level=100
)
s.move(templated_files, excludes=[
    # pybigquery was originally licensed MIT
    "LICENSE"
])

# ----------------------------------------------------------------------------
# Fixup files
# ----------------------------------------------------------------------------

s.replace(
    [".coveragerc"],
    "google/cloud/__init__.py",
    "pybigquery/requirements.py",
    )

s.replace(
    ["noxfile.py"],
    r"[\"']google[\"']",
    '"pybigquery"',
)

s.replace(
    ["noxfile.py"], "google/cloud", "pybigquery",
)

def place_before(path, text, *before_text, escape=None):
    replacement = "\n".join(before_text) + "\n" + text
    if escape:
        for c in escape:
            text = text.replace(c, '\\' + c)
    s.replace([path], text, replacement)

place_before(
    "noxfile.py",
    "SYSTEM_TEST_PYTHON_VERSIONS=",
    "",
    "# We're using two Python versions to test with sqlalchemy 1.3 and 1.4.",
)

place_before(
    "noxfile.py",
    "nox.options.error_on_missing_interpreters = True",
    "nox.options.stop_on_first_error = True",
)

install_alembic_for_python_38 = '''
def install_alembic_for_python_38(session, constraints_path):
    """
    install alembic for Python 3.8 unit and system tests

    We do not require alembic and most tests should run without it, however

    - We run some unit tests (Python 3.8) to cover the alembic
      registration that happens when alembic is installed.

    - We have a system test that demonstrates working with alembic and
      proves that the things we think should work do work. :)
    """
    if session.python == "3.8":
        session.install("alembic", "-c", constraints_path)


'''

place_before(
    "noxfile.py",
    "def default",
    install_alembic_for_python_38,
    )

place_before(
    "noxfile.py",
    '    session.install("-e", ".", ',
    "    install_alembic_for_python_38(session, constraints_path)",
    escape='(')

old_sessions = '''
    "unit",
    "system",
    "cover",
    "lint",
'''

new_sessions = '''
    "lint",
    "unit",
    "cover",
    "system",
    "compliance",
'''

s.replace( ["noxfile.py"], old_sessions, new_sessions)

compliance = '''
@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def compliance(session):
    """Run the SQLAlchemy dialect-compliance system tests"""
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    system_test_folder_path = os.path.join("tests", "sqlalchemy_dialect_compliance")

    if os.environ.get("RUN_COMPLIANCE_TESTS", "true") == "false":
        session.skip("RUN_COMPLIANCE_TESTS is set to false, skipping")
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""):
        session.skip("Credentials must be set via environment variable")
    if os.environ.get("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false") == "true":
        session.install("pyopenssl")
    if not os.path.exists(system_test_folder_path):
        session.skip("Compliance tests were not found")

    session.install("--pre", "grpcio")

    session.install(
        "mock",
        "pytest",
        "pytest-rerunfailures",
        "google-cloud-testutils",
        "-c",
        constraints_path,
    )
    session.install("-e", ".", "-c", constraints_path)

    session.run(
        "py.test",
        "-vv",
        f"--junitxml=compliance_{session.python}_sponge_log.xml",
        "--reruns=3",
        "--reruns-delay=60",
        "--only-rerun=403 Exceeded rate limits",
        "--only-rerun=409 Already Exists",
        "--only-rerun=404 Not found",
        "--only-rerun=400 Cannot execute DML over a non-existent table",
        system_test_folder_path,
        *session.posargs,
    )


'''

place_before(
     "noxfile.py",
     "@nox.session(python=DEFAULT_PYTHON_VERSION)\n"
     "def cover(session):",
     compliance,
     escape="()",
     )




# Add DB config for SQLAlchemy dialect test suite.
# https://github.com/sqlalchemy/sqlalchemy/blob/master/README.dialects.rst
# https://github.com/googleapis/python-bigquery-sqlalchemy/issues/89
s.replace(
    ["setup.cfg"],
    "universal = 1\n",
    """universal = 1

[sqla_testing]
requirement_cls=pybigquery.requirements:Requirements
profile_file=.sqlalchemy_dialect_compliance-profiles.txt

[tool:pytest]
addopts= --tb native -v -r fxX -p no:warnings
python_files=tests/*test_*.py
"""
)

# ----------------------------------------------------------------------------
# Final cleanup
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
for noxfile in REPO_ROOT.glob("samples/**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
