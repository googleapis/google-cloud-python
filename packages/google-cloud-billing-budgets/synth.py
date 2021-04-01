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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate billing budgets GAPIC layer
# ----------------------------------------------------------------------------
versions = ["v1beta1", "v1"]
for version in versions:
    library = gapic.py_library(
        service="billing_budgets",
        version=f"{version}",
        bazel_target=f"//google/cloud/billing/budgets/{version}:billing-budgets-{version}-py",
        include_protos=True,
        proto_output_path=f"google/cloud/billing/budgets_{version}/proto"
    )

    excludes = [
        "nox.py",
        "setup.py",
        "README.rst",
        library / "docs/index.rst",
    ]

    s.move(library, excludes=excludes)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
    cov_level=98,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# Update the namespace in noxfile.py
s.replace(
    "noxfile.py",
    "google.cloud.billingbudgets",
    "google.cloud.billing.budgets"
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
