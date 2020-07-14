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
versions = ["v1p1beta1", "v1beta1", "v1"]

# ----------------------------------------------------------------------------
# Generate securitycenter GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="securitycenter",
        version=version,
        bazel_target=f"//google/cloud/securitycenter/{version}:securitycenter-{version}-py",
        include_protos=True
    )
    s.move(library / f"google/cloud/securitycenter_{version}")
    s.move(library / f"tests/unit/gapic/{version}")
    s.move(library / f"docs/gapic/{version}")

# Use the highest version library to generate import alias.
s.move(library / "google/cloud/securitycenter.py")

# Fix bad line wrapping in docstring
s.replace("google/**/security_marks_pb2.py",
"""“organizations/\{organization_id\}/assets/\{asset_
\s+id\}/securityMarks” “organizations/\{organization_id\}/sources/\{s
\s+ource_id\}/findings/\{finding_id\}/securityMarks”\.""",
"""``organizations/{organization_id}/assets/{asset_id}/securityMarks``
          ``organizations/{organization_id}/sources/{source_id}/findings/{finding_id}/securityMarks``.""")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=88, samples=True)
s.move(templated_files)

python.py_samples(root="samples", skip_readmes=True)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
