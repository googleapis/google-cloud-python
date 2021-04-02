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

from synthtool.languages import python
import synthtool as s
import synthtool.gcp as gcp

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate trace GAPIC layer
# ----------------------------------------------------------------------------
for version in ["v1", "v2"]:
    library = gapic.py_library(
        service="trace",
        version=version,
        bazel_target=f"//google/devtools/cloudtrace/{version}:devtools-cloudtrace-{version}-py",
        proto_output_path=f"google/cloud/trace_{version}/proto",
        include_protos=True,
    )

    s.move(library, excludes=["docs/index.rst", "setup.py"])


# Rename field `type_` to `type` in v1 and v2 to avoid breaking change
s.replace(
    "google/**/types/*.py",
    "type_",
    "type"
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,  # set to True only if there are samples
    microgenerator=True,
    cov_level=98,
)

python.py_samples(skip_readmes=True)

s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file
s.shell.run(["nox", "-s", "blacken"], hide_output=False)
