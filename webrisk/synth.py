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

import re

import synthtool as s
from synthtool import gcp

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()
versions = ["v1beta1"]

# ----------------------------------------------------------------------------
# Generate webrisk GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library("webrisk", version, include_protos=True)
    s.copy(library, excludes=["docs/index.rst", "nox.py", "README.rst", "setup.py"])


# Fix docstring issue for classes with no summary line
s.replace(
    "google/cloud/**/proto/webrisk_pb2.py",
    '''__doc__ = """Attributes:''',
    '''__doc__ = """
    Attributes:''',
)


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files, excludes=["noxfile.py"])

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
