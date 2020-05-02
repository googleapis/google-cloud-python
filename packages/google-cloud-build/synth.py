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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
version = 'v1'

# ----------------------------------------------------------------------------
# Generate cloudbuild GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service='cloudbuild',
    version=version,
    bazel_target=f"//google/devtools/cloudbuild/{version}:devtools-cloudbuild-{version}-py",
    include_protos=True,
    proto_output_path=f"google/cloud/devtools/cloudbuild_{version}/proto",
)

s.move(
    library,
    excludes=[
        'docs/index.rst',
        'nox*.py',
        'setup.py',
        'setup.cfg',
        'README.rst',
        'google/cloud/devtools/__init__.py',  # declare this as a namespace package
    ],
)

# Rename package to `google-cloud-build`
s.replace(
    ["**/*.rst", "*/**/*.py", "**/*.md"],
    "google-cloud-devtools-cloudbuild",
    "google-cloud-build"
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

# coverage level is low because of missing coverage for __init__.py files
templated_files = common.py_library(unit_cov_level=65, cov_level=65)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)