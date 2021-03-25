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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()


# ----------------------------------------------------------------------------
# Generate websecurityscanner GAPIC layer
# ----------------------------------------------------------------------------
versions = ["v1alpha", "v1beta"]

for version in versions:
    library = gapic.py_library(
        service="websecurityscanner",
        version=version,
        bazel_target=f"//google/cloud/websecurityscanner/{version}:websecurityscanner-{version}-py",
        include_protos=True,
    )
    s.move(library / f"google/cloud/websecurityscanner_{version}")
    s.move(library / "tests")
    s.move(library / "scripts")
    s.move(library / "docs", excludes=[library / "docs/index.rst"])


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=98,
    samples=False,  # set to True only if there are samples
    microgenerator=True,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
