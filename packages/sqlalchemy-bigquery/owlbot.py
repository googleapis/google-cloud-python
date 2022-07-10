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
    "3.8": ["tests", "alembic"],
    "3.10": ["tests", "geography"],
}
templated_files = common.py_library(
    system_test_python_versions=["3.8", "3.10"],
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

prerelease = r'''
@nox.session(python=DEFAULT_PYTHON_VERSION)
def prerelease(session):
    session.install(
        "--prefer-binary",
        "--pre",
        "--upgrade",
        "alembic",
        "geoalchemy2",
        "google-api-core",
        "google-cloud-bigquery",
        "google-cloud-bigquery-storage",
        "sqlalchemy",
        "shapely",
        # These are transitive dependencies, but we'd still like to know if a
        # change in a prerelease there breaks this connector.
        "google-cloud-core",
        "grpcio",
    )
    session.install(
        "freezegun",
        "google-cloud-testutils",
        "mock",
        "psutil",
        "pytest",
        "pytest-cov",
        "pytz",
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
            r"^\\s*(\\S+)(?===\\S+)", constraints_text, flags=re.MULTILINE
        )
    ]

    # We use --no-deps to ensure that pre-release versions aren't overwritten
    # by the version ranges in setup.py.
    session.install(*deps)
    session.install("--no-deps", "-e", ".")

    # Print out prerelease package versions.
    session.run("python", "-m", "pip", "freeze")

    # Run all tests, except a few samples tests which require extra dependencies.
    session.run(
        "py.test",
        "--quiet",
        f"--junitxml=prerelease_unit_{session.python}_sponge_log.xml",
        os.path.join("tests", "unit"),
    )
    session.run(
        "py.test",
        "--quiet",
        f"--junitxml=prerelease_system_{session.python}_sponge_log.xml",
        os.path.join("tests", "system"),
    )


'''

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

    session.install(
        "mock",
        # TODO: Allow latest version of pytest once SQLAlchemy 1.4.28+ is supported.
        # See: https://github.com/googleapis/python-bigquery-sqlalchemy/issues/413
        "pytest<=7.0.0dev",
        "pytest-rerunfailures",
        "google-cloud-testutils",
        "-c",
        constraints_path,
    )
    if session.python == "3.8":
        extras = "[tests,alembic]"
    elif session.python == "3.10":
        extras = "[tests,geography]"
    else:
        extras = "[tests]"
    session.install("-e", f".{extras}", "-c", constraints_path)

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
     prerelease + compliance,
     escape="()",
     )

s.replace(["noxfile.py"], '"alabaster"', '"alabaster", "geoalchemy2", "shapely"')



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

# ----------------------------------------------------------------------------
# Final cleanup
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
for noxfile in REPO_ROOT.glob("samples/**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
