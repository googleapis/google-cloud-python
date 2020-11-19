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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
versions = ["v1beta1", "v1p1beta1", "v1p2beta1", "v1p4beta1", "v1p5beta1", "v1"]

excludes = ["setup.py", "nox*.py", "README.rst", "docs/conf.py", "docs/index.rst"]

# ----------------------------------------------------------------------------
# Generate asset GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="asset",
        version=version,
        bazel_target=f"//google/cloud/asset/{version}:asset-{version}-py",
    )

    s.move(library, excludes=excludes)

# Fix import of 'osconfig' type
s.replace(
    "google/cloud/asset_v1/types/assets.py",
    "from google\.cloud\.osconfig\.v1 import inventory_pb2 as inventory",
    "from google.cloud.osconfig_v1 import Inventory"
)

s.replace(
    "google/cloud/asset_v1/types/assets.py",
    "message=inventory\.Inventory,",
    "message=Inventory,"
)

# Remove broken `parse_asset_path` method
# The resource pattern is '*' which breaks the regex match
s.replace(
    "google/cloud/**/client.py",
    """@staticmethod
    def parse_asset_path.*?@staticmethod""",
    """@staticmethod""",
    flags=re.MULTILINE | re.DOTALL
)

s.replace(
    "google/cloud/**/async_client.py",
    """parse_asset_path = staticmethod\(AssetServiceClient\.parse_asset_path\)""",
    ""
)
s.replace(
    "tests/unit/**/test_asset_service.py",
    """def test_parse_asset_path.*?def""",
    """def""",
    flags=re.MULTILINE | re.DOTALL,
)
# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,  # set to True only if there are samples
    microgenerator=True,
    cov_level=99,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)

s.replace(
    "noxfile.py",
    "google\.cloud\.cloudasset",
    "google/cloud",
)

s.replace(
    "noxfile.py",
    '''["']--cov=google\.cloud["'],''',
    "",
)

s.replace(
    "noxfile.py",
    """"--cov=tests.unit",""",
    """"--cov=tests/unit",""",
)

# Temporarily disable warnings due to
# https://github.com/googleapis/gapic-generator-python/issues/525
s.replace("noxfile.py", '[\"\']-W[\"\']', '# "-W"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
