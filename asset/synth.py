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

versions = ["v1beta1"]

excludes = [
    'setup.py',
    'README.rst',
    'docs/conf.py',
    'docs/index.rst',
]

for version in versions:
    library = gapic.py_library(
        "asset",
        version,
        config_path=f"/google/cloud/asset/artman_cloudasset_{version}.yaml",
        artman_output_name=f"asset-{version}",
    )

    s.move(library, excludes=excludes)

    s.replace(
        f"google/cloud/asset_{version}/gapic/asset_service_client.py",
        "'google-cloud-cloudasset', \).version",
        "'google-cloud-asset', ).version",
    )

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
