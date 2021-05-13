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

common = gcp.CommonTemplates()

# This library ships clients for two different APIs,
# BigTable and BigTable Admin
bigtable_default_version = "v2"
bigtable_admin_default_version = "v2"

for library in s.get_staging_dirs(bigtable_default_version):
    s.move(library / "google/cloud/bigtable_v*")
    s.move(library / "tests")
    s.move(library / "scripts")

s.remove_staging_dirs()

for library in s.get_staging_dirs(bigtable_admin_default_version):
    s.move(library / "google/cloud/bigtable_admin_v*")
    s.move(library / "tests")
    s.move(library / "scripts")

s.remove_staging_dirs()

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