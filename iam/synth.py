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

import synthtool as s
from synthtool import gcp

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate automl GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "iam",
    "v1",
    config_path="/google/iam/credentials/artman_iamcredentials_v1.yaml",
    artman_output_name="iamcredentials-v1"
)

excludes = [
    "README.rst",
    "setup.py",
    "docs/index.rst",
]
s.copy(library, excludes=excludes)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=82, cov_level=83)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
