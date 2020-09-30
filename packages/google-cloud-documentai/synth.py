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
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate document AI GAPIC layer
# ----------------------------------------------------------------------------

versions = ["v1beta2", "v1beta3"]

for version in versions:
    library = gapic.py_library(
        service="documentai",
        version=version,
        bazel_target=f"//google/cloud/documentai/{version}:documentai-{version}-py",
    )

    excludes = ["README.rst", "nox.py", "docs/index.rst", "setup.py"]
    s.move(library, excludes=excludes)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=100,
    microgenerator=True,
    samples=False,  # set to true if there are samples
)
s.move(
    templated_files,
    excludes=[".coveragerc"],  # microgenerator has a good .coveragerc file
) 

python.py_samples()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
