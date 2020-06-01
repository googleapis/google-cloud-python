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
from synthtool.languages import python

gapic = gcp.GAPICMicrogenerator()
common = gcp.CommonTemplates()
versions = ["v1beta1", "v1"]

# ----------------------------------------------------------------------------
# Generate texttospeech GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(service="texttospeech", version=version,)
    s.move(library, excludes=["setup.py", "docs/index.rst"])

# Sphinx interprets `*` as emphasis
s.replace(
    ["google/cloud/**/client.py", "google/cloud/**/cloud_tts.py"],
    "((en)|(no)|(nb)(cmn)|(yue))-\*",
    "\g<1>-\*",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=100,
    samples=True,
    unit_test_python_versions=["3.6", "3.7", "3.8"],
    system_test_python_versions=["3.7"],
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples(skip_readmes=True)

# Extra lint ignores for microgenerator tests
# TODO: Remove when https://github.com/googleapis/gapic-generator-python/issues/425 is closed
s.replace(".flake8", "(ignore = .*)", "\g<1>, F401, F841")

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
