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

common = gcp.CommonTemplates()

default_version = "v3"

for library in s.get_staging_dirs(default_version):
    if library.name.startswith("v3"):
        # TODO(danoscarmike): remove once upstream protos have been fixed
        # Escape underscores in gs:\\ URLs
        s.replace(
            library / "google/cloud/translate_v3*/types/translation_service.py",
            "a_b_c_",
            "a_b_c\_"
        )

    excludes = [
        "setup.py",
        "nox*.py",
        "README.rst",
        "docs/conf.py",
        "docs/index.rst",
        "translation.py",
    ]

    s.replace(library / ".coveragerc",
        """google/cloud/translate/__init__.py""",
        """google/__init__.py
    google/cloud/__init__.py
    google/cloud/translate/__init__.py""",
    )
    s.move(library, excludes=excludes)

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,
    microgenerator=True,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()
python.configure_previous_major_version_branches()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
