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
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate bigtable and bigtable_admin GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="bigtable",
    version="v2",
    bazel_target="//google/bigtable/v2:bigtable-v2-py",
    include_protos=True,
)

s.move(library / "google/cloud/bigtable_v2")
s.move(library / "tests")
s.move(library / "scripts")

# Generate admin client
library = gapic.py_library(
    service="bigtable_admin",
    version="v2",
    bazel_target="//google/bigtable/admin/v2:bigtable-admin-v2-py",
    include_protos=True,
)

s.move(library / "google/cloud/bigtable_admin_v2")
s.move(library / "tests")
s.move(library / "scripts")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,  # set to True only if there are samples
    microgenerator=True,
    cov_level=99
)
s.move(templated_files, excludes=[".coveragerc", "noxfile.py"])

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

sample_files = common.py_samples(samples=True)
for path in sample_files:
    s.move(path, excludes=['noxfile.py'])


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
