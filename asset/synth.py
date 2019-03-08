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
versions = ["v1beta1"]

excludes = ["setup.py", "nox*.py", "README.rst", "docs/conf.py", "docs/index.rst"]

# ----------------------------------------------------------------------------
# Generate asset GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        "asset",
        version,
        config_path=f"/google/cloud/asset/artman_cloudasset_{version}.yaml",
        artman_output_name=f"asset-{version}",
        include_protos=True,
    )

    s.move(library, excludes=excludes)

s.replace(
    "google/cloud/asset_v1beta1/proto/assets_pb2.py",
    "from google.iam.v1 import policy_pb2 as",
    "from google.iam.v1 import iam_policy_pb2_grpc as",
)

s.replace(
    "google/cloud/asset_v1beta1/proto/assets_pb2.py",
    "from google.iam.v1 import iam_policy_pb2_grpc "
    "as google_dot_iam_dot_v1_dot_policy__pb2",
    "from google.iam.v1 import iam_policy_pb2 "
    "as google_dot_iam_dot_v1_dot_policy__pb2",
)

s.replace(
    "google/cloud/asset_v1beta1/proto/assets_pb2.py",
    "_ASSET.fields_by_name\['iam_policy'\].message_type "
    "= google_dot_iam_dot_v1_dot_policy__pb2._POLICY",
    "_ASSET.fields_by_name['iam_policy'].message_type = google_dot_iam_dot"
    "_v1_dot_policy__pb2.google_dot_iam_dot_v1_dot_policy__pb2._POLICY",
)


_BORKED_ASSET_DOCSTRING = """\
          The full name of the asset. For example: ``//compute.googleapi
          s.com/projects/my_project_123/zones/zone1/instances/instance1`
          `. See `Resource Names <https://cloud.google.com/apis/design/r
          esource_names#full_resource_name>`__ for more information.
"""

_FIXED_ASSET_DOCSTRING = """
          The full name of the asset. For example:
          ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``.
          See https://cloud.google.com/apis/design/resource_names#full_resource_name
          for more information.
"""

s.replace(
    "google/cloud/asset_v1beta1/proto/assets_pb2.py",
    _BORKED_ASSET_DOCSTRING,
    _FIXED_ASSET_DOCSTRING,
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = gcp.CommonTemplates().py_library(unit_cov_level=79, cov_level=80)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
