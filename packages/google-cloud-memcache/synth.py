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
import os

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

versions = ["v1beta2",
            "v1",
            ] # add new versions at the end of the list

# ----------------------------------------------------------------------------
# Generate memcache GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="memcache",
        version=version,
        bazel_target=f"//google/cloud/memcache/{version}:memcache-{version}-py")

    excludes = [
        "setup.py",
        "docs/index.rst",
        "README.rst"
    ]
    s.move(library, excludes=excludes)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=100, microgenerator=True)
s.move(
    templated_files, excludes=[".coveragerc"]
)  # the microgenerator has a good coveragerc file

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
