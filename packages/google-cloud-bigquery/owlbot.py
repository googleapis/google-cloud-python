# Copyright 2018 Google LLC
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
from pathlib import Path

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

REPO_ROOT = Path(__file__).parent.absolute()

default_version = "v2"

for library in s.get_staging_dirs(default_version):
    # Avoid breaking change due to change in field renames.
    # https://github.com/googleapis/python-bigquery/issues/319
    s.replace(
        library / f"google/cloud/bigquery_{library.name}/types/standard_sql.py",
        r"type_ ",
        "type ",
    )
    # Patch docs issue
    s.replace(
        library / f"google/cloud/bigquery_{library.name}/types/model.py",
        r"""\"predicted_\"""",
        """`predicted_`""",
    )
    s.move(library / f"google/cloud/bigquery_{library.name}/types")
s.remove_staging_dirs()

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=100,
    samples=True,
    microgenerator=True,
    split_system_tests=True,
    intersphinx_dependencies={
        "dateutil": "https://dateutil.readthedocs.io/en/latest/",
        "geopandas": "https://geopandas.org/",
        "pandas": "https://pandas.pydata.org/pandas-docs/stable/",
    },
    system_test_python_versions=["3.9", "3.13"],
    unit_test_python_versions=["3.9", "3.10", "3.11", "3.12", "3.13"],
    default_python_version="3.9",
)

# BigQuery has a custom multiprocessing note
s.move(
    templated_files,
    excludes=[
        "noxfile.py",
        "renovate.json",
        "docs/multiprocessing.rst",
        "docs/index.rst",
        ".coveragerc",
        ".github/CODEOWNERS",
        # Include custom SNIPPETS_TESTS job for performance.
        # https://github.com/googleapis/python-bigquery/issues/191
        ".kokoro/presubmit/presubmit.cfg",
        ".kokoro/presubmit/system-3.8.cfg",
        ".kokoro/continuous/prerelease-deps.cfg",
        ".kokoro/samples/python3.7/**",
        ".kokoro/samples/python3.8/**",
        ".github/workflows/**",  # exclude gh actions as credentials are needed for tests
        "README.rst",
    ],
)

python.configure_previous_major_version_branches()

s.replace(
    ".kokoro/test-samples-impl.sh",
    """# `virtualenv==20.26.6` is added for Python 3.7 compatibility
python3.9 -m pip install --upgrade --quiet nox virtualenv==20.26.6""",
    "python3.9 -m pip install --upgrade --quiet nox virtualenv",
)

s.replace(
    "CONTRIBUTING.rst",
    r"\$ nox -s py-3.8",
    r"$ nox -s py-3.9",
)

s.replace(
    "scripts/readme-gen/templates/install_deps.tmpl.rst",
    r"Samples are compatible with Python 3.7",
    r"Samples are compatible with Python 3.9",
)


# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()

s.replace(
    "samples/**/noxfile.py",
    'BLACK_VERSION = "black==22.3.0"',
    'BLACK_VERSION = "black==23.7.0"',
)
s.replace(
    "samples/**/noxfile.py",
    r'ALL_VERSIONS = \["3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13"\]',
    'ALL_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]',
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
for noxfile in REPO_ROOT.glob("samples/**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
