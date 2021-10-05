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

extras = ["tqdm"]
templated_files = common.py_library(
    unit_test_python_versions=["3.7", "3.8", "3.9"],
    system_test_python_versions=["3.8", "3.9"],
    cov_level=86,
    unit_test_extras=extras,
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
    ["noxfile.py"], r"[\"']google[\"']", '"pandas_gbq"',
)

s.replace(
    ["noxfile.py"], "google/cloud", "pandas_gbq",
)

s.replace(
    [".github/header-checker-lint.yml"], '"Google LLC"', '"pandas-gbq Authors"',
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
