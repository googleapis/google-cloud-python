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
        include_protos=True,
    )
    s.move(library, excludes=["README.rst", "docs/index.rst", "setup.py"])



# fix bad indentation
s.replace(
    "google/**/*service.py",
    """(\s+)settings resource.
\s+If empty all mutable fields will be updated.""",
    """\g<1>settings resource.
\g<1>If empty all mutable fields will be updated.""",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,
    microgenerator=True,  # set to True only if there are samples
    cov_level=99,
)
s.move(
    templated_files, excludes=[".coveragerc"]
)  # microgenerator has a good .coveragerc file

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
