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

versions = ["v2beta1", "v2"]

for version in versions:
    library = gapic.py_library(
        "dialogflow",
        version,
        bazel_target=f"//google/cloud/dialogflow/{version}:dialogflow-{version}-py",
        include_protos=True,
    )

    s.move(library, excludes=["docs/index.rst", "setup.py"])

# # ----------------------------------------------------------------------------
# # Add templated files
# # ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# Don't treat warnings as errors
# Docstrings have unexpected idnentation and block quote formatting issues
s.replace(
    "noxfile.py",
    '''["']-W["'],  # warnings as errors''',
    "",
)
    
s.shell.run(["nox", "-s", "blacken"], hide_output=False)
