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
versions = ["v1beta1", "v1"]

# ----------------------------------------------------------------------------
# Generate webrisk GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="webrisk",
        version=version,
        bazel_target=f"//google/cloud/webrisk/{version}:webrisk-{version}-py",
        include_protos=True,
    )
    s.copy(library, excludes=["docs/index.rst", "nox.py", "README.rst", "setup.py"])


# Fix docstring issue for classes with no summary line
s.replace(
    "google/cloud/**/proto/webrisk_pb2.py",
    ''''__doc__': """Attributes:''',
    ''''__doc__': """
    Attributes:''',
)


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
    cov_level=99,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
