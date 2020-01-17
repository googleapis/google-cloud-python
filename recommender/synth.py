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
import re

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
versions = ["v1beta1", "v1"]
common = gcp.CommonTemplates()


# ----------------------------------------------------------------------------
# Generate Cloud Recommender
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library("recommender", version)
    s.move(library, excludes=["nox.py", "docs/index.rst", "README.rst", "setup.py"])

# Fix docstring with regex pattern that breaks docgen
s.replace("google/**/recommender_client.py", "(/\^.*\$/)", "``\g<1>``")

# Fix more regex in docstrings
s.replace("google/**/*_pb2.py", ":math:`(/)", "\g<1>")
s.replace("google/**/*_pb2.py", "`/\.", "/.")
s.replace("google/**/*_pb2.py", "(regex\s+)(/.*?/)\.", "\g<1>``\g<2>``.", flags=re.MULTILINE | re.DOTALL,)

# Fix docstring with JSON example by wrapping with backticks
s.replace(
    "google/**/recommendation_pb2.py",
    "( -  Example: )(\{.*?\})",
    "\g<1>``\g<2>``",
    flags=re.MULTILINE | re.DOTALL,
)

python.fix_pb2_headers()
python.fix_pb2_grpc_headers()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=92)
s.move(templated_files)

# don't run 2.7 tests
s.replace("noxfile.py", """\["2\.7", """, "[")

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
