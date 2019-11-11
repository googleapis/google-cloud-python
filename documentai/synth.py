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

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate document AI GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library("documentai", "v1beta1", include_protos=True)

excludes = ["README.rst", "nox.py", "setup.py", "docs/index.rst"]
s.move(library, excludes=excludes)

# Fix bad docstring with stray pipe characters
s.replace(
    "google/cloud/**/document_understanding_pb2.py",
    """\| Specifies a known document type for deeper structure
          detection\. Valid   values are currently "general" and
          "invoice"\. If not provided,   "general" \| is used as default.
          If any other value is given, the request is   rejected\.""",
    """Specifies a known document type for deeper structure
          detection. Valid   values are currently "general" and
          "invoice". If not provided,   "general" is used as default.
          If any other value is given, the request is   rejected.""",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
