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
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate document AI GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="documentai",
    version="v1beta2",
    bazel_target="//google/cloud/documentai/v1beta2:documentai-v1beta2-py",
)

library = gapic.py_library("documentai", "v1beta2")

excludes = ["README.rst", "nox.py", "docs/index.rst", "setup.py"]
s.move(library, excludes=excludes)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=73)
s.move(templated_files)

# Remove 2.7 and 3.5 tests from noxfile.py
s.replace("noxfile.py", '''\["2\.7", ''', '[')
s.replace("noxfile.py", '''"3.5", ''', '')

# Expand flake errors permitted to accomodate the Microgenerator
# TODO: remove extra error codes once issues below are resolved
# F401: https://github.com/googleapis/gapic-generator-python/issues/324
# F841: local variable 'client'/'response' is assigned to but never use
s.replace(".flake8", "ignore = .*", "ignore = E203, E266, E501, W503, F401, F841")

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
