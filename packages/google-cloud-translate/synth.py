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
from synthtool import gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
versions = ["v3beta1", "v3"]

excludes = [
    "setup.py",
    "nox*.py",
    "README.rst",
    "docs/conf.py",
    "docs/index.rst",
    "translation.py",
]

# ----------------------------------------------------------------------------
# Generate asset GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="translate",
        version=version,
        bazel_target=f"//google/cloud/translate/{version}:translation-{version}-py",
    )
    s.move(library, excludes=excludes)

# TODO(danoscarmike): remove once upstream protos have been fixed
# Escape underscores in gs:\\ URLs
s.replace(
    "google/cloud/translate_v3*/types/translation_service.py",
    r"""a_b_c_""",
    """a_b_c\_"""
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,
    microgenerator=True,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# Correct namespace in noxfile
s.replace("noxfile.py", "google.cloud.translation", "google.cloud.translate")

# Exclude the v2 from coverage targets
s.replace(".coveragerc",
"    google/cloud/translate/__init__.py",
"""    google/cloud/translate/__init__.py
    google/cloud/translate_v2/__init__.py
    google/cloud/__init__.py"""
)
# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
