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
import synthtool.gcp as gcp
from synthtool.languages import python
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
excludes = ["README.rst", "setup.py", "nox*.py", "docs/index.rst", "*.tar.gz"]

# ----------------------------------------------------------------------------
# Generate tasks GAPIC layer
# ----------------------------------------------------------------------------
for version in ["v2beta2", "v2beta3", "v2"]:
    library = gapic.py_library(
        service="tasks",
        version=version,
        bazel_target=f"//google/cloud/tasks/{version}:tasks-{version}-py",
        include_protos=True,
    )

    s.copy(library, excludes=excludes)

# Fix docstring.
s.replace("google/cloud/*/types/target.py", "X-Google-\*", "X-Google-\\*")
s.replace("google/cloud/*/types/target.py", "X-AppEngine-\*", "X-AppEngine-\\*")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
    cov_level=98,
)
s.move(
    templated_files, excludes=[".coveragerc"]
)  # microgenerator has a good .coveragerc file

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
