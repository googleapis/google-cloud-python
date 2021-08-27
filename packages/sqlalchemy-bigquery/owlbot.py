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
    "3.9": ["tests", "geography"],
}
templated_files = common.py_library(
    unit_test_python_versions=["3.6", "3.7", "3.8", "3.9"],
    system_test_python_versions=["3.8", "3.9"],
    cov_level=100,
    unit_test_extras=extras,
    unit_test_extras_by_python=extras_by_python,
    system_test_extras=extras,
    system_test_extras_by_python=extras_by_python,
)
s.move(templated_files, excludes=[
    # sqlalchemy-bigquery was originally licensed MIT
    "LICENSE", "docs/multiprocessing.rst"
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
    ["noxfile.py"], "google/cloud", "sqlalchemy_bigquery",
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

# Maybe we can get rid of this when we don't need pytest-rerunfailures,
# which we won't need when BQ retries itself:
# https://github.com/googleapis/python-bigquery/pull/837
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
    if session.python == "3.8":
        extras = "[tests,alembic]"
    elif session.python == "3.9":
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
     compliance,
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
# Remove the replacements below once https://github.com/googleapis/synthtool/pull/1188 is merged

# Update googleapis/repo-automation-bots repo to main in .kokoro/*.sh files
s.replace(".kokoro/*.sh", "repo-automation-bots/tree/master", "repo-automation-bots/tree/main")

# Customize CONTRIBUTING.rst to replace master with main
s.replace(
    "CONTRIBUTING.rst",
    "fetch and merge changes from upstream into master",
    "fetch and merge changes from upstream into main",
)

s.replace(
    "CONTRIBUTING.rst",
    "git merge upstream/master",
    "git merge upstream/main",
)

s.replace(
    "CONTRIBUTING.rst",
    """export GOOGLE_CLOUD_TESTING_BRANCH=\"master\"""",
    """export GOOGLE_CLOUD_TESTING_BRANCH=\"main\"""",
)

s.replace(
    "CONTRIBUTING.rst",
    "remote \(``master``\)",
    "remote (``main``)",
)

s.replace(
    "CONTRIBUTING.rst",
    "blob/master/CONTRIBUTING.rst",
    "blob/main/CONTRIBUTING.rst",
)

s.replace(
    "CONTRIBUTING.rst",
    "blob/master/noxfile.py",
    "blob/main/noxfile.py",
)

s.replace("docs/conf.py", "master", "root")

# ----------------------------------------------------------------------------
# Final cleanup
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
for noxfile in REPO_ROOT.glob("samples/**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
