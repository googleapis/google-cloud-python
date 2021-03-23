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
    system_test_python_versions=["3.8"],
    cov_level=50
)
s.move(templated_files, excludes=[
    # pybigquery was originally licensed MIT
    "LICENSE"
])

# ----------------------------------------------------------------------------
# Fixup files
# ----------------------------------------------------------------------------

s.replace(
    ["noxfile.py"],
    r"[\"']google[\"']",
    '"pybigquery"',
)

s.replace(
    ["noxfile.py"], "google/cloud", "pybigquery",
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
profile_file=.profiles.txt

[db]
default=bigquery://
bigquery=bigquery://
"""
)

# ----------------------------------------------------------------------------
# Final cleanup
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
for noxfile in REPO_ROOT.glob("samples/**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
