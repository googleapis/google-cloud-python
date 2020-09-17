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

# ----------------------------------------------------------------------------
# Generate workflows and workflows executions GAPIC layer
# ----------------------------------------------------------------------------

library = gapic.py_library(
    service="workflows_executions",
    version="v1beta1",
    bazel_target="//google/cloud/workflows/executions/v1beta:workflows-executions-v1beta-py",
)

s.move(
    library,
    excludes=[
        "setup.py",
        "README.rst",
        "docs/index.rst",
        "scripts/fixup_executions_v1beta_keywords.py",
    ],
)

# move workflows after executions, since we want to use "workflows" for the name
library = gapic.py_library(
    service="workflows",
    version="v1beta",
    bazel_target="//google/cloud/workflows/v1beta:workflows-v1beta-py",
)

s.move(
    library,
    excludes=[
        "setup.py",
        "README.rst",
        "docs/index.rst",
        "scripts/fixup_workflows_v1beta_keywords.py",
    ],
)

# add empty line after list in docstring
s.replace(
    "google/**/*.py",
    """-  Must be unique within the customer project and
                   location.""",
    """-  Must be unique within the customer project and
                   location.\n""",
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
