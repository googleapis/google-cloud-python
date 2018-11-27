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

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()
versions = ["v1", "v1p1beta1", "v1p2beta1", "v1p3beta1"]


# ----------------------------------------------------------------------------
# Generate vision GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library("vision", version)

    s.move(library / f"google/cloud/vision_{version}/gapic")
    s.move(library / f"google/cloud/vision_{version}/__init__.py")
    s.move(library / f"google/cloud/vision_{version}/types.py")
    s.move(library / f"google/cloud/vision_{version}/proto")
    s.move(library / f"tests/unit/gapic/{version}")
    # don't publish docs for these versions
    if version not in ["v1p1beta1"]:
        s.move(library / f"docs/gapic/{version}")

    # Add vision helpers to each version
    s.replace(
        f"google/cloud/vision_{version}/__init__.py",
        f"from __future__ import absolute_import",
        f"\g<0>\n\n"
        f"from google.cloud.vision_helpers.decorators import "
        f"add_single_feature_methods\n"
        f"from google.cloud.vision_helpers import VisionHelpers",
    )

    s.replace(
        f"google/cloud/vision_{version}/__init__.py", f"image_annotator_client", f"iac"
    )

    s.replace(
        f"google/cloud/vision_{version}/__init__.py",
        f"from google.cloud.vision_{version}.gapic import iac",
        f"from google.cloud.vision_{version}.gapic import "
        f"image_annotator_client as iac",
    )

    s.replace(
        f"google/cloud/vision_{version}/__init__.py",
        f"class ImageAnnotatorClient\(iac.ImageAnnotatorClient\):",
        f"@add_single_feature_methods\n"
        f"class ImageAnnotatorClient(VisionHelpers, iac.ImageAnnotatorClient):",
    )

# Fix import of operations
targets = ["google/cloud/vision_*/**/*.py", "tests/system/gapic/*/**/*.py"]
s.replace(
    targets,
    "import google.api_core.operations_v1",
    "from google.api_core import operations_v1",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=36, cov_level=36)
s.move(templated_files)
