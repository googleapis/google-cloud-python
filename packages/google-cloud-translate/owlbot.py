# Copyright 2022 Google LLC
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

import json
from pathlib import Path
import shutil

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

clean_up_generated_samples = True

# Load the default version defined in .repo-metadata.json.
default_version = json.load(open(".repo-metadata.json", "rt")).get(
    "default_version"
)

for library in s.get_staging_dirs(default_version):
    if clean_up_generated_samples:
        shutil.rmtree("samples/generated_samples", ignore_errors=True)
        clean_up_generated_samples = False

    if library.name.startswith("v3"):
        # TODO(danoscarmike): remove once upstream protos have been fixed
        # Escape underscores in gs:\\ URLs
        s.replace(
            library / "google/cloud/translate_v3*/types/translation_service.py",
            "a_b_c_",
            "a_b_c\_"
        )

    s.replace(library / ".coveragerc",
        """google/cloud/translate/__init__.py""",
        """google/__init__.py
    google/cloud/__init__.py
    google/cloud/translate/__init__.py""",
    )
    s.move([library], excludes=["**/gapic_version.py", "docs/index.rst", "setup.py", "testing/constraints-3.7.txt"])
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=100,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(templated_files, excludes=[".coveragerc", ".github/release-please.yml", "docs/index.rst"])

python.py_samples(skip_readmes=True)

# run format session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
