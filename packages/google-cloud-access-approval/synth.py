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
# Generate access approva lGAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library("accessapproval", "v1")

s.move(library, excludes=["nox.py", "setup.py", "README.rst", "docs/index.rst"])

# correct license headers
python.fix_pb2_headers()
python.fix_pb2_grpc_headers()

# Rename package to `google-cloud-access-approval` instead of `google-cloud-accessapproval`
s.replace(
    ["google/**/*.py", "tests/**/*.py"],
    "google-cloud-accessapproval",
    "google-cloud-access-approval",
)

# fix bad docs insertion for protobuf
s.replace("google/**/accessapproval_pb2.py", "__doc__ = ", "'__doc__' : ")

#
s.replace('google/**/accessapproval_pb2.py', '''"""Attributes:''', '''"""\nAttributes:''')

# fix bad quotes
s.replace('google/**/accessapproval_pb2.py', "“", '"')
s.replace('google/**/accessapproval_pb2.py', "”", '"')

# fix unescaped curly braces
s.replace('google/**/accessapproval_pb2.py', """\{projects|folders
          |organizations\}/\{id\}/approvalRequests/\{approval_request_id\}""",
          """``{projects|folders
          |organizations}/{id}/approvalRequests/{approval_request_id}``""")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=70)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
