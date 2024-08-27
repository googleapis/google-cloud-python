# Copyright 2023 Google LLC
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
from synthtool.languages import python

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    microgenerator=True,
)

# this is an http library, not grpc
s.move(
    templated_files,
    excludes=[
        ".github/workflows",
        ".gitignore",
        "CONTRIBUTING.rst",
        "docs/**/*",
        "MANIFEST.in",
        "noxfile.py",
        "README.rst",
        "scripts/**/*",
        "setup.py",
        "setup.cfg",
        "testing/**/*",
        ".kokoro/release.sh", # not needed
        ".kokoro/build.sh", # not needed
    ],
)

