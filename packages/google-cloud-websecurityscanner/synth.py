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
# Generate websecurityscanner GAPIC layer
# ----------------------------------------------------------------------------
versions = ["v1alpha", "v1beta"]

for version in versions:
	library = gapic.py_library(
	    "websecurityscanner",
	    version,
	    config_path=f"/google/cloud/websecurityscanner"
	    f"/artman_websecurityscanner_{version}.yaml",
	    artman_output_name=f"websecurityscanner-{version}",
	    include_protos=True,
	)

	s.move(library / f"google/cloud/websecurityscanner_{version}/proto")
	s.move(library / f"google/cloud/websecurityscanner_{version}/gapic")
	s.move(library / f"google/cloud/websecurityscanner_{version}/*.py")
	s.move(library / f"docs/gapic/{version}")
	s.move(library / f"tests/unit/gapic/{version}")

s.move(library / "google/cloud/websecurityscanner.py")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=89)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
