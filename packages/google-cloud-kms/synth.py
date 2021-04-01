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
from synthtool.languages import python
import logging

logging.basicConfig(level=logging.DEBUG)

client_library_version = "0.1.0"

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
version = "v1"

# ----------------------------------------------------------------------------
# Generate kms GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="kms",
    version=version,
    bazel_target="//google/cloud/kms/v1:kms-v1-py",
    include_protos=True,
)

s.move(library, excludes=["README.rst", "setup.py", "nox*.py", "docs/index.rst"])

# Escape single '_' which RST treats as target names
s.replace("google/**/resources.py", '''"(.*?)_((SIGN)|(DECRYPT))_"''', '''"\g<1>_\g<2>\_"''')

# Docstrings of *_iam_policy() methods are formatted poorly and must be fixed
# in order to avoid docstring format warnings in docs.
s.replace(
    "google/**/*client.py",
    r"(\s+)Args:",
    "\n\g<1>Args:"
)
s.replace(
    "google/**/*client.py",
    r"(\s+)\*\*JSON Example\*\*\s+::",
    "\n\g<1>**JSON Example**::\n",
)
s.replace(
    "google/**/*client.py",
    r"(\s+)\*\*YAML Example\*\*\s+::",
    "\n\g<1>**YAML Example**::\n",
)
s.replace(
    "google/**/*client.py",
    r"(\s+)For a description of IAM and its features, see",
    "\n\g<0>",
)

# Rename `format_` to `format` to avoid breaking change
s.replace(
    "google/**/types/*.py",
    "format_",
    "format"
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=98,
    samples=True,
    microgenerator=True,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

sample_files = common.py_samples(unit_cov_level=97, cov_level=99, samples=True)
s.move(sample_files, excludes=['noxfile.py'])

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
