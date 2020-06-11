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

gapic = gcp.GAPICMicrogenerator()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate Service Directory GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "servicedirectory", "v1beta1"
)

s.move(library, excludes=["setup.py", "README.rst", "docs/index.rst"])

# rename library to google-cloud-service-directory
s.replace(["google/**/*.py", "tests/**/*.py"], "google-cloud-servicedirectory", "google-cloud-service-directory")

# surround path with * with ``
s.replace("google/**/*.py", '''["'](projects/\*/.*)["']\.''', "``\g<1>``" )

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=100,
    samples=False,
    unit_test_python_versions=["3.6", "3.7", "3.8"],
    system_test_python_versions=["3.7"],
)

s.move(templated_files, excludes=[".coveragerc"])  # the microgenerator has a good coveragerc file

# Extra lint ignores for microgenerator tests
# TODO: Remove when https://github.com/googleapis/gapic-generator-python/issues/425 is closed
s.replace(".flake8", "(ignore = .*)", "\g<1>, F401, F841")

s.shell.run(["nox", "-s", "blacken"], hide_output=False)