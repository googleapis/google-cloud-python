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
import re
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
    # Fix import of 'osconfig' type
    s.replace(
        library / f"google/cloud/asset_{library.name}/types/assets.py",
        f"from google\.cloud\.osconfig\.{library.name} import inventory_pb2",
        f"from google.cloud.osconfig_{library.name} import Inventory"
    )

    s.replace(
        library / f"google/cloud/asset_{library.name}/types/assets.py",
        "inventory_pb2\.Inventory",
        "Inventory"
    )

    s.replace(
        library / f"google/cloud/asset_{library.name}/types/assets.py",
        "google\.cloud\.osconfig\.v1\.inventory_pb2\.Inventory",
        "google.cloud.osconfig_v1.Inventory"
    )

    # Remove broken `parse_asset_path` method
    # The resource pattern is '*' which breaks the regex match
    s.replace(
        library / "google/cloud/**/client.py",
        """@staticmethod
    def parse_asset_path.*?@staticmethod""",
        """@staticmethod""",
        flags=re.MULTILINE | re.DOTALL
    )

    s.replace(
        library / "google/cloud/**/async_client.py",
        """parse_asset_path = staticmethod\(AssetServiceClient\.parse_asset_path\)""",
        ""
    )

    s.replace(
        library / "tests/unit/**/test_asset_service.py",
        """def test_parse_asset_path.*?def""",
        """def""",
        flags=re.MULTILINE | re.DOTALL,
    )

    s.replace(
        library / "google/cloud/asset_v*/__init__.py",
        "from google.cloud.asset import gapic_version as package_version",
        f"from google.cloud.asset_{library.name} import gapic_version as package_version",
    )

    s.move([library], excludes=["**/gapic_version.py", "docs/index.rst", "setup.py", "testing/constraints-3.7.txt"])
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=99,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(templated_files, excludes=[".coveragerc", ".github/release-please.yml", "docs/index.rst"])

python.py_samples(skip_readmes=True)

# run format session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
