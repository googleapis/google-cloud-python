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
versions = ["v1beta2", "v1"]


# ----------------------------------------------------------------------------
# Generate language GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        "language",
        version,
        config_path=f"/google/cloud/language/artman_language_{version}.yaml",
        artman_output_name=f"language-{version}",
        include_protos=True,
        include_samples=True
    )

    s.move(library / f"google/cloud/language_{version}/proto")
    s.move(library / f"google/cloud/language_{version}/gapic")
    s.move(library / f"tests/unit/gapic/{version}")
    s.move(library / f"tests/system/gapic/{version}")
    s.move(library / f"samples")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files, excludes=['noxfile.py'])

s.replace(
    f"google/cloud/**/gapic/language_service_client.py",
    r"types\.EncodingType",
    "enums.EncodingType",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
