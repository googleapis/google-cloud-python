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
import os

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    excludes = ["README.rst", "setup.py", "nox*.py", "docs/index.rst"]
    s.move(library, excludes=excludes)

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,  # set to True only if there are samples
    microgenerator=True,
    cov_level=99,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# Fix type annotations for requests
# Not needed once generator version is >=0.51.1
# Generator version: https://github.com/googleapis/googleapis/blob/master/WORKSPACE#L227
# Fix in generator: https://github.com/googleapis/gapic-generator-python/commit/49205d99dd440690b838c8eb3f6a695f35b061c2

s.replace(
    "google/**/*client.py",
    "request: ([^U]*?) = None",
    "request: Union[\g<1>, dict] = None",
    
)
s.replace(
    "google/**/*client.py",
    "request \(:class:`(.*)`\):",
    "request (Union[\g<1>, dict]):"
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
