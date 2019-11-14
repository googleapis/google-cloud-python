# Copyright 2019 Google LLC
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
import synthtool.gcp as gcp
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate billing budgets GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "billingbudgets",
    "v1beta1",
    config_path="/google/cloud/billing/budgets/artman_billingbudgets_v1beta1.yaml",
    include_protos=True,
)

excludes = [
    "nox.py",
    "setup.py",
    "README.rst",
    library / "docs/index.rst",
    library
    / "google/cloud/billingbudgets_v1beta1/proto",  # proto files are copied to the wrong place
]

s.move(library, excludes=excludes)
s.move(
    library / "google/cloud/billingbudgets_v1beta1/proto/*.proto",
    "google/cloud/billing_budgets_v1beta1/proto",
)

# Fix namespace
s.replace(
    "**/*.py",
    "from google\.cloud\.billing\.budgets_v1beta1",
    "from google.cloud.billing_budgets_v1beta1",
)

# Fix package name
s.replace(
    ["**/*.rst", "setup.py", "*/**/*.py"],
    "google-cloud-billingbudgets",
    "google-cloud-billing-budgets",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=72, cov_level=72)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
