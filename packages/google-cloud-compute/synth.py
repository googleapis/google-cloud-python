# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
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
# Generate Compute Engine GAPIC layer
# ----------------------------------------------------------------------------
versions = ["v1"]
for version in versions:
    library = gapic.py_library(
        service="compute",
        version="v1",
        bazel_target="//google/cloud/compute/v1:compute-v1-py",
        diregapic=True,
    )
    s.move(library, excludes=["setup.py", "README.rst", "docs/index.rst", "docs/multiprocessing.rst", f"scripts/fixup_compute_{version}_keywords.py"])

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = common.py_library(cov_level=96, microgenerator=True)
s.move(
  templated_files, excludes=[".coveragerc"] # the microgenerator has a good coveragerc file
)

# --------------------------------------------------------------------------
# Samples templates
# --------------------------------------------------------------------------
python.py_samples()

# Don't treat docs warnings as errors
# A few errors like:
# docstring of google.cloud.compute_v1.types.compute.InterconnectOutageNotification:31: WARNING: Unknown target name: "it".
s.replace(
    "noxfile.py",
    '''['"]-W['"].*''',
    "",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
