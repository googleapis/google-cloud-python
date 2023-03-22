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
from synthtool.languages import python

REPO_ROOT = pathlib.Path(__file__).parent.absolute()

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
extras = ["tests"]
extras_by_python = {
    "3.8": ["tests", "alembic", "bqstorage"],
    "3.11": ["tests", "geography", "bqstorage"],
}
templated_files = common.py_library(
    unit_test_python_versions=["3.7", "3.8", "3.9", "3.10", "3.11"],
    system_test_python_versions=["3.8", "3.11"],
    cov_level=100,
    unit_test_extras=extras,
    unit_test_extras_by_python=extras_by_python,
    system_test_extras=extras,
    system_test_extras_by_python=extras_by_python,
)
s.move(templated_files, excludes=[
    # sqlalchemy-bigquery was originally licensed MIT
    "LICENSE", 
    "docs/multiprocessing.rst",
    # exclude gh actions as credentials are needed for tests
    ".github/workflows",
    "README.rst",
])

# ----------------------------------------------------------------------------
# Fixup files
# ----------------------------------------------------------------------------

s.replace(
    [".coveragerc"],
    "google/cloud/__init__.py",
    "sqlalchemy_bigquery/requirements.py",
    )

s.replace(
    ["noxfile.py"],
    r"[\"']google[\"']",
    '"sqlalchemy_bigquery"',
)

s.replace(
    ["noxfile.py"],
    r"import shutil",
    "import re\nimport shutil",
)


s.replace(
    ["noxfile.py"], "--cov=google", "--cov=sqlalchemy_bigquery",
)


s.replace(
    ["noxfile.py"], 
    "\+ SYSTEM_TEST_EXTRAS",
    "",
)


s.replace(
    ["noxfile.py"],
    '''"protobuf",
        # dependency of grpc''',
    '''"protobuf",
        "sqlalchemy<2.0.0",
        # dependency of grpc''',
)


s.replace(
    ["noxfile.py"],
    r"def default\(session\)",
    "def default(session, install_extras=True)",    
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


install_logic = '''
    if install_extras and session.python == "3.11":
        install_target = ".[geography,alembic,tests,bqstorage]"
    elif install_extras:
        install_target = ".[all]"
    else:
        install_target = "."
    session.install("-e", install_target, "-c", constraints_path)
'''

place_before(
    "noxfile.py",
    "# Run py.test against the unit tests.",
    install_logic,
)


# Maybe we can get rid of this when we don't need pytest-rerunfailures,
# which we won't need when BQ retries itself:
# https://github.com/googleapis/python-bigquery/pull/837
compliance = '''
@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS[-1])
def compliance(session):
    """Run the SQLAlchemy dialect-compliance system tests"""
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    system_test_folder_path = os.path.join("tests", "sqlalchemy_dialect_compliance")

    if os.environ.get("RUN_COMPLIANCE_TESTS", "true") == "false":
        session.skip("RUN_COMPLIANCE_TESTS is set to false, skipping")
    if os.environ.get("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false") == "true":
        session.install("pyopenssl")
    if not os.path.exists(system_test_folder_path):
        session.skip("Compliance tests were not found")

    session.install("--pre", "grpcio")
    session.install("--pre", "--no-deps", "--upgrade", "sqlalchemy<2.0.0") 
    session.install(
        "mock",
        "pytest",
        "pytest-rerunfailures",
        "google-cloud-testutils",
        "-c",
        constraints_path,
    )
    if session.python == "3.8":
        extras = "[tests,alembic]"
    elif session.python == "3.11":
        extras = "[tests,geography]"
    else:
        extras = "[tests]"
    session.install("-e", f".{extras}", "-c", constraints_path)

    session.run("python", "-m", "pip", "freeze")

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
        # To suppress the "Deprecated API features detected!" warning when
        # features not compatible with 2.0 are detected, use a value of "1"
        env={
            "SQLALCHEMY_SILENCE_UBER_WARNING": "1",
        },
    )


'''

place_before(
     "noxfile.py",
     "@nox.session(python=DEFAULT_PYTHON_VERSION)\n"
     "def cover(session):",
     compliance,
     escape="()",
     )

s.replace(["noxfile.py"], '"alabaster"', '"alabaster", "geoalchemy2", "shapely"')


system_noextras = '''
@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def system_noextras(session):
    """Run the system test suite."""
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )
    system_test_path = os.path.join("tests", "system.py")
    system_test_folder_path = os.path.join("tests", "system")

    # Check the value of `RUN_SYSTEM_TESTS` env var. It defaults to true.
    if os.environ.get("RUN_SYSTEM_TESTS", "true") == "false":
        session.skip("RUN_SYSTEM_TESTS is set to false, skipping")
    # Install pyopenssl for mTLS testing.
    if os.environ.get("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false") == "true":
        session.install("pyopenssl")

    system_test_exists = os.path.exists(system_test_path)
    system_test_folder_exists = os.path.exists(system_test_folder_path)
    # Sanity check: only run tests if found.
    if not system_test_exists and not system_test_folder_exists:
        session.skip("System tests were not found")

    global SYSTEM_TEST_EXTRAS_BY_PYTHON
    SYSTEM_TEST_EXTRAS_BY_PYTHON = False
    install_systemtest_dependencies(session, "-c", constraints_path)

    # Run py.test against the system tests.
    if system_test_exists:
        session.run(
            "py.test",
            "--quiet",
            f"--junitxml=system_{session.python}_sponge_log.xml",
            system_test_path,
            *session.posargs,
        )
    if system_test_folder_exists:
        session.run(
            "py.test",
            "--quiet",
            f"--junitxml=system_{session.python}_sponge_log.xml",
            system_test_folder_path,
            *session.posargs,
        )

        
'''


place_before(
    "noxfile.py",
    "@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS[-1])\n"
    "def compliance(session):", 
    system_noextras,
    escape="()[]",
    )


# Add DB config for SQLAlchemy dialect test suite.
# https://github.com/googleapis/python-bigquery-sqlalchemy/issues/89
s.replace(
    ["setup.cfg"],
    "universal = 1\n",
    """universal = 1

[sqla_testing]
requirement_cls=sqlalchemy_bigquery.requirements:Requirements
profile_file=.sqlalchemy_dialect_compliance-profiles.txt

[tool:pytest]
addopts= --tb native -v -r fxX -p no:warnings
python_files=tests/*test_*.py
"""
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)

s.replace(
    ["./samples/snippets/noxfile.py"], 
    """session.install\("-e", _get_repo_root\(\)\)""",
    """session.install("-e", _get_repo_root())
    else:
        # ensure that sqlalchemy_bigquery gets installed
        # for tests that are not based on source
        session.install("sqlalchemy_bigquery")""",
)


# ----------------------------------------------------------------------------
# Final cleanup
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
for noxfile in REPO_ROOT.glob("samples/**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
