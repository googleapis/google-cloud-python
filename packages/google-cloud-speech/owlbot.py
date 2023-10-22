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

    if "v1" in library.name:
        # Add the manually written SpeechHelpers to v1 and v1p1beta1
        # See google/cloud/speech_v1/helpers.py for details
        count = s.replace(library / f"google/cloud/speech_{library.name}/__init__.py",
                            """__all__ = \(""",
                            """from google.cloud.speech_v1.helpers import SpeechHelpers

class SpeechClient(SpeechHelpers, SpeechClient):
    __doc__ = SpeechClient.__doc__

__all__ = (
                        """,
                    )
        assert count == 1

    if library.name == "v1":
        # Import from speech_v1 to get the client with SpeechHelpers
        count = s.replace(library / "google/cloud/speech/__init__.py",
            """from google\.cloud\.speech_v1\.services\.speech\.client import SpeechClient""",
            """from google.cloud.speech_v1 import SpeechClient"""
            )
        assert count == 1

    s.replace(
        library / "google/cloud/speech_v*/__init__.py",
        "from google.cloud.speech import gapic_version as package_version",
        f"from google.cloud.speech_{library.name} import gapic_version as package_version",
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
