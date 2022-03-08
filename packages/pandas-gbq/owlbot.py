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
import re

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

REPO_ROOT = pathlib.Path(__file__).parent.absolute()

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

extras_by_python = {
    # Use a middle version of Python to test when no extras are installed.
    "3.9": []
}
extras = ["tqdm"]
templated_files = common.py_library(
    unit_test_python_versions=["3.7", "3.8", "3.9", "3.10"],
    system_test_python_versions=["3.7", "3.8", "3.9", "3.10"],
    cov_level=96,
    unit_test_external_dependencies=["freezegun"],
    unit_test_extras=extras,
    unit_test_extras_by_python=extras_by_python,
    system_test_extras=extras,
    intersphinx_dependencies={
        "pandas": "https://pandas.pydata.org/pandas-docs/stable/",
        "pydata-google-auth": "https://pydata-google-auth.readthedocs.io/en/latest/",
    },
)
s.move(
    templated_files,
    excludes=[
        # pandas-gbq was originally licensed BSD-3-Clause License
        "LICENSE",
        # Mulit-processing note isn't relevant, as pandas_gbq is responsible for
        # creating clients, not the end user.
        "docs/multiprocessing.rst",
    ],
)

# ----------------------------------------------------------------------------
# Fixup files
# ----------------------------------------------------------------------------

s.replace(
    ["noxfile.py"],
    r"import pathlib\s+import shutil",
    "import pathlib\nimport re\nimport shutil",
)

s.replace(
    ["noxfile.py"], r"[\"']google[\"']", '"pandas_gbq"',
)


s.replace(
    ["noxfile.py"], "--cov=google", "--cov=pandas_gbq",
)

# Workaround for https://github.com/googleapis/synthtool/issues/1317
s.replace(
    ["noxfile.py"], r'extras = "\[\]"', 'extras = ""',
)

s.replace(
    ["noxfile.py"],
    r"@nox.session\(python=DEFAULT_PYTHON_VERSION\)\s+def cover\(session\):",
    r"""@nox.session(python=DEFAULT_PYTHON_VERSION)
def prerelease(session):
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
        "--prefer-binary",
        "--pre",
        "--upgrade",
        "google-api-core",
        "google-cloud-bigquery",
        "google-cloud-bigquery-storage",
        "google-cloud-core",
        "google-resumable-media",
        "grpcio",
    )
    session.install(
        "freezegun",
        "google-cloud-datacatalog",
        "google-cloud-storage",
        "google-cloud-testutils",
        "IPython",
        "mock",
        "psutil",
        "pytest",
        "pytest-cov",
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
    session.install("--no-deps", "-e", ".[all]")

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


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cover(session):""",
    re.MULTILINE,
)

s.replace(
    [".github/header-checker-lint.yml"], '"Google LLC"', '"pandas-gbq Authors"',
)

# Work around bug in templates https://github.com/googleapis/synthtool/pull/1335
s.replace(".github/workflows/unittest.yml", "--fail-under=100", "--fail-under=96")

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
