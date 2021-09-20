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
    unit_test_python_versions=["3.6", "3.7", "3.8", "3.9"],
    system_test_python_versions=["3.8"],
    cov_level=100,
)
s.move(templated_files, excludes=["docs/multiprocessing.rst"])

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
    ["noxfile.py"], "google/cloud", "db_dtypes",
)


def place_before(path, text, *before_text, escape=None):
    replacement = "\n".join(before_text) + "\n" + text
    if escape:
        for c in escape:
            text = text.replace(c, "\\" + c)
    s.replace([path], text, replacement)


place_before(
    "noxfile.py",
    "nox.options.error_on_missing_interpreters = True",
    "nox.options.stop_on_first_error = True",
)

old_sessions = """
    "unit",
    "system",
    "cover",
    "lint",
"""

new_sessions = """
    "lint",
    "unit",
    "cover",
    "system",
    "compliance",
"""

s.replace(["noxfile.py"], old_sessions, new_sessions)

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
