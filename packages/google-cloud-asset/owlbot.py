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

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # Fix import of 'osconfig' type
    s.replace(
        library / f"google/cloud/asset_{library.name}/types/assets.py",
        f"from google\.cloud\.osconfig\.{library.name} import inventory_pb2",
        f"from google.cloud.osconfig_{library.name} import Inventory"
    )

    s.replace(
        library / f"google/cloud/asset_{library.name}/types/assets.py",
        "message=inventory_pb2\.Inventory,",
        "message=Inventory,"
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

    excludes = ["setup.py", "nox*.py", "README.rst", "docs/conf.py", "docs/index.rst"]
    s.move(library, excludes=excludes)

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,  # set to True only if there are samples
    microgenerator=True,
    cov_level=100,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file
python.configure_previous_major_version_branches()

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)

# Temporarily disable warnings due to
# https://github.com/googleapis/gapic-generator-python/issues/525
s.replace("noxfile.py", '[\"\']-W[\"\']', '# "-W"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
