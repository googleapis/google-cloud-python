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
versions = ["v1beta1", "v1"]

# ----------------------------------------------------------------------------
# Generate texttospeech GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library("texttospeech", version)
    s.move(library / f"google/cloud/texttospeech_{version}")
    s.move(library / f"tests/unit/gapic/{version}")
    s.move(library / f"docs/gapic/{version}")

# Use the highest version library to generate import alias.
s.move(library / "google/cloud/texttospeech.py")

# Fix bad docstrings.
s.replace("**/gapic/*_client.py", r'\\"(.+?)-\*\\"', r'"\1-\\*"')

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files)
