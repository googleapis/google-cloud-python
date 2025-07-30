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
extras = ["tests"]
extras_by_python = {
    "3.9": ["tests", "alembic", "bqstorage"],
    "3.11": ["tests", "geography", "bqstorage"],
    "3.12": ["tests", "geography", "bqstorage"],
    "3.13": ["tests", "geography", "bqstorage"],
}
templated_files = common.py_library(
    unit_test_python_versions=["3.9", "3.10", "3.11", "3.12", "3.13"],
    system_test_python_versions=["3.9", "3.12", "3.13"],
    cov_level=100,
    unit_test_extras=extras,
    unit_test_extras_by_python=extras_by_python,
    system_test_extras=extras,
    system_test_extras_by_python=extras_by_python,
)
s.move(
    templated_files,
    excludes=[
        # sqlalchemy-bigquery was originally licensed MIT
        "LICENSE",
        "docs/multiprocessing.rst",
        # exclude gh actions as credentials are needed for tests
        ".github/workflows",
        "README.rst",
        "renovate.json",
    ],
)

# ----------------------------------------------------------------------------
# Fixup files
# ----------------------------------------------------------------------------

s.replace(
    [".coveragerc"],
    "google/cloud/__init__.py",
    "sqlalchemy_bigquery/requirements.py",
)


# Add DB config for SQLAlchemy dialect test suite.
# https://github.com/googleapis/python-bigquery-sqlalchemy/issues/89
s.replace(
    ["setup.cfg"],
    "universal = 1\n",
    """universal = 1
""",
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
