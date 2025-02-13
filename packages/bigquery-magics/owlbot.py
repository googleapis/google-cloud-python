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

extras_storage = ["bqstorage"]
extras_bf = ["bqstorage", "bigframes", "geopandas"]
extras_by_python = {
    "3.7": extras_storage,
    "3.8": extras_storage,
    "3.9": extras_bf,
    "3.10": extras_bf,
    # Use a middle version of Python to test when no extras are installed.
    "3.11": [],
    "3.12": [],
    "3.13": extras_bf,
}
templated_files = common.py_library(
    unit_test_python_versions=["3.7", "3.8", "3.9", "3.11", "3.12", "3.13"],
    system_test_python_versions=["3.8", "3.11", "3.12", "3.13"],
    cov_level=100,
    unit_test_extras_by_python=extras_by_python,
    unit_test_external_dependencies=["google-cloud-testutils"],
    system_test_extras_by_python=extras_by_python,
    intersphinx_dependencies={
        "pandas": "https://pandas.pydata.org/pandas-docs/stable/",
        "pydata-google-auth": "https://pydata-google-auth.readthedocs.io/en/latest/",
    },
)
s.move(
    templated_files,
    excludes=[
        # Multi-processing note isn't relevant, as bigquery-magics is responsible for
        # creating clients, not the end user.
        "docs/multiprocessing.rst",
        "README.rst",
        ".github/workflows/unittest.yml",
    ],
)

# ----------------------------------------------------------------------------
# Fixup files
# ----------------------------------------------------------------------------

s.replace(
    ["noxfile.py"],
    r"[\"']google[\"']",
    '"bigquery_magics"',
)


s.replace(
    ["noxfile.py"],
    "--cov=google",
    "--cov=bigquery_magics",
)


# Workaround for https://github.com/googleapis/synthtool/issues/1317
s.replace(
    ["noxfile.py"],
    r'extras = "\[\]"',
    'extras = ""',
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)

# ----------------------------------------------------------------------------
# Final cleanup
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "format"], hide_output=False)
for noxfile in REPO_ROOT.glob("samples/**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
