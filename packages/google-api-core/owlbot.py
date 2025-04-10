# Copyright 2020 Google LLC
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

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
excludes = [
    "noxfile.py",  # pytype
    "setup.cfg",  # pytype
    ".coveragerc",  # layout
    "CONTRIBUTING.rst",  # no systests
    ".github/workflows/unittest.yml",  # exclude unittest gh action
    ".github/workflows/lint.yml",  # exclude lint gh action
    "README.rst",
]
templated_files = common.py_library(microgenerator=True, cov_level=100)
s.move(templated_files, excludes=excludes)

python.configure_previous_major_version_branches()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
