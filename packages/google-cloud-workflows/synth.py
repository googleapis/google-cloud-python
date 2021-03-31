# Copyright 2020 Google LLC
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
import os

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# This library ships clients for two different APIs,
# Workflows and Workflows Executions
workflows_versions = ["v1beta", "v1"]
workflows_executions_versions = ["v1beta", "v1"]

# ----------------------------------------------------------------------------
# Generate workflows and workflows executions GAPIC layer
# ----------------------------------------------------------------------------

for version in workflows_executions_versions:
    library = gapic.py_library(
        service="workflows_executions",
        version=version,
        bazel_target=f"//google/cloud/workflows/executions/{version}:workflows-executions-{version}-py",
    )

    s.move(
        library,
        excludes=[
            "setup.py",
            "README.rst",
            "docs/index.rst",
            f"scripts/fixup_executions_{version}_keywords.py",
        ],
    )

for version in workflows_versions:
    # move workflows after executions, since we want to use "workflows" for the name
    library = gapic.py_library(
        service="workflows",
        version=version,
        bazel_target=f"//google/cloud/workflows/{version}:workflows-{version}-py",
    )

    s.move(
        library,
        excludes=[
            "setup.py",
            "README.rst",
            "docs/index.rst",
            f"scripts/fixup_workflows_{version}_keywords.py",
        ],
    )


# Make sure this library is named 'google-cloud-workflows' everywhere
s.replace(
    "google/**/*.py", "google-cloud-workflows-executions", "google-cloud-workflow"
)
# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=98, microgenerator=True)
s.move(
    templated_files, excludes=[".coveragerc"]
)  # the microgenerator has a good coveragerc file


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
