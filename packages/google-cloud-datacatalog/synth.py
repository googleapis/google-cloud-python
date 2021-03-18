# Copyright 2019 Google LLC
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


# ----------------------------------------------------------------------------
# Generate datacatalog GAPIC layer
# ----------------------------------------------------------------------------
versions = ['v1', 'v1beta1']
for version in versions:
    library = gapic.py_library(
        service='datacatalog',
        version=version,
        bazel_target=f"//google/cloud/datacatalog/{version}:datacatalog-{version}-py",
        include_protos=True,
    )

    s.move(
        library,
        excludes=[
            'docs/conf.py',
            'docs/index.rst',
            'README.rst',
            'nox*.py',
            'setup.py',
            'setup.cfg',
        ],
    )

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,
    microgenerator=True,
)
s.move(templated_files, excludes=[".coveragerc"]) # microgenerator has a good .coveragerc file

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
