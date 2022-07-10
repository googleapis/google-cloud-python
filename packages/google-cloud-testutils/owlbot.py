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

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=78)
s.move(
    templated_files,
    excludes=[
        ".coveragerc",
        "MANIFEST.in",  # no 'google' package
        "noxfile.py",  # noxfile is non-standard
        "docs/**/*",  # no docs to publish
        ".kokoro/docs/",
        ".kokoro/publish-docs.sh",
        "CONTRIBUTING.rst",
        "renovate.json", # no bundle, ignore test resources
        ".github/workflows/docs.yml", # no docs to publish
	"README.rst",
    ],
)

# Work around bug in templates https://github.com/googleapis/synthtool/pull/1335
s.replace(".github/workflows/unittest.yml", "--fail-under=100", "--fail-under=78")

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
