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
from synthtool import _tracked_paths

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------
staging = Path("owl-bot-staging")

if staging.is_dir():
    _tracked_paths.add(staging)

    # Remove once this repository migrates to google-cloud-python
    s.replace(
        staging / "setup.py",
        """url = \"https://github.com/googleapis/python-common\"""",
        """url = \"https://github.com/googleapis/python-cloud-common\"""",
    )

    s.copy([staging], excludes=["**/gapic_version.py", "README.rst", "docs/index.rst"])

s.remove_staging_dirs()


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=100,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(templated_files, excludes=[".coveragerc", ".github/release-please.yml", "docs/index.rst", "README.rst"])

python.py_samples(skip_readmes=True)

# run format session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "format"], cwd=noxfile.parent, hide_output=False)

