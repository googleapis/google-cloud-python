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

    # Work around sphinx docs issue
    # Determine if this is a gapic-generator-python bug or docstring issue
    s.replace(library / f"google/cloud/devtools/cloudbuild_{library.name}/services/cloud_build/*client.py",
        "`WorkerPool`s.",
        r"`WorkerPool`\\s.",
    )

    # Remove replacement once repo has migrated to google-cloud-python
    assert 1 == s.replace(
        library / "setup.py",
        """url = \"https://github.com/googleapis/python-build\"""",
        """url = \"https://github.com/googleapis/python-cloudbuild\""""
    )

    # grpc-google-iam-v1 is required by cloud build v2 however setup.py does not reflect this.
    # The issue is that both v1 and v2 are generated which have different requirements for setup.py files.
    # The setup.py for v2 is clobbered by the setup.py for v1 which does not require grpc-google-iam-v1.
    assert 1 == s.replace(
        library / "setup.py",
        r"""\"protobuf>=3.19.5,<5.0.0dev,!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5\",\n""",
        """\"protobuf>=3.19.5,<5.0.0dev,!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5\",
    "grpc-google-iam-v1 >= 0.12.4, < 1.0.0dev",\n""",
    )

    s.move([library], excludes=["**/gapic_version.py"])
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=100,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(templated_files, excludes=[".coveragerc", ".github/release-please.yml"])

python.py_samples(skip_readmes=True)

# run format session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
