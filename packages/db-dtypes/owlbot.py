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
templated_files = common.py_library(
    system_test_python_versions=["3.8"],
    cov_level=100,
    intersphinx_dependencies={
        "pandas": "https://pandas.pydata.org/pandas-docs/stable/"
    },
)
s.move(templated_files, excludes=["docs/multiprocessing.rst", "README.rst"])

# ----------------------------------------------------------------------------
# Fixup files
# ----------------------------------------------------------------------------

s.replace(
    [".coveragerc"], "google/cloud/__init__.py", "db_dtypes/requirements.py",
)

s.replace(
    ["noxfile.py"], r"[\"']google[\"']", '"db_dtypes"',
)

s.replace(
    ["noxfile.py"], r"import shutil", "import re\nimport shutil",
)

s.replace(
    ["noxfile.py"], "--cov=google", "--cov=db_dtypes",
)

# There are no system tests for this package.
old_sessions = """
    "unit",
    "system",
    "cover",
    "lint",
"""

new_sessions = """
    "lint",
    "unit",
    "unit_prerelease",
    "compliance",
    "compliance_prerelease",
    "cover",
"""

s.replace(["noxfile.py"], old_sessions, new_sessions)

# Add compliance tests.
s.replace(
    ["noxfile.py"], r"def default\(session\):", "def default(session, tests_path):"
)
s.replace(["noxfile.py"], r'os.path.join\("tests", "unit"\),', "tests_path,")
s.replace(
    ["noxfile.py"],
    r'f"--junitxml=unit_{session.python}_sponge_log.xml",',
    r'f"--junitxml={os.path.split(tests_path)[-1]}_{session.python}_sponge_log.xml",',
)
s.replace(
    ["noxfile.py"],
    r'''
@nox.session\(python=UNIT_TEST_PYTHON_VERSIONS\)
def unit\(session\):
    """Run the unit test suite."""
    default\(session\)
''',
    r'''
def prerelease(session, tests_path):
    constraints_path = str(
        CURRENT_DIRECTORY / "testing" / f"constraints-{session.python}.txt"
    )

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
    session.install(
        "--extra-index-url",
        "https://pypi.anaconda.org/scipy-wheels-nightly/simple",
        "--prefer-binary",
        "--pre",
        "--upgrade",
        "pandas",
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

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        f"--junitxml={os.path.split(tests_path)[-1]}_prerelease_{session.python}_sponge_log.xml",
        "--cov=db_dtypes",
        "--cov=tests/unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        tests_path,
        *session.posargs,
    )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS[-1])
def compliance(session):
    """Run the compliance test suite."""
    default(session, os.path.join("tests", "compliance"))


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS[-1])
def compliance_prerelease(session):
    """Run the compliance test suite with prerelease dependencies."""
    prerelease(session, os.path.join("tests", "compliance"))


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run the unit test suite."""
    default(session, os.path.join("tests", "unit"))


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS[-1])
def unit_prerelease(session):
    """Run the unit test suite with prerelease dependencies."""
    prerelease(session, os.path.join("tests", "unit"))
''',
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
