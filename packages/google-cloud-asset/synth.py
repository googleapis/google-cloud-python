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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
versions = ["v1beta1", "v1p1beta1", "v1p2beta1", "v1p4beta1", "v1"]

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

s.replace(
    "google/cloud/asset_v*/proto/assets_pb2.py",
    "from google.iam.v1 import policy_pb2 as",
    "from google.iam.v1 import iam_policy_pb2_grpc as",
)

s.replace(
    "google/cloud/asset_v*/proto/assets_pb2.py",
    "from google.iam.v1 import iam_policy_pb2_grpc "
    "as google_dot_iam_dot_v1_dot_policy__pb2",
    "from google.iam.v1 import iam_policy_pb2 "
    "as google_dot_iam_dot_v1_dot_policy__pb2",
)

s.replace(
    "google/cloud/asset_v*/proto/assets_pb2.py",
    "_ASSET\.fields_by_name\['iam_policy'\]\.message_type "
    "= google_dot_iam_dot_v1_dot_policy__pb2\._POLICY",
    "_ASSET.fields_by_name['iam_policy'].message_type = google_dot_iam_dot"
    "_v1_dot_policy__pb2.google_dot_iam_dot_v1_dot_policy__pb2._POLICY",
)

s.replace(
    "google/cloud/asset_v*/proto/assets_pb2.py",
    "_IAMPOLICYSEARCHRESULT\.fields_by_name\['policy'\]\.message_type "
    "= google_dot_iam_dot_v1_dot_policy__pb2\._POLICY",
    "_IAMPOLICYSEARCHRESULT.fields_by_name['policy'].message_type = google_dot_iam_dot"
    "_v1_dot_policy__pb2.google_dot_iam_dot_v1_dot_policy__pb2._POLICY",
)

s.replace(
    "google/cloud/asset_v*/proto/assets_pb2.py",
    "_IAMPOLICYANALYSISRESULT\.fields_by_name\['iam_binding'\]\.message_type "
    "= google_dot_iam_dot_v1_dot_policy__pb2\._BINDING",
    "_IAMPOLICYANALYSISRESULT.fields_by_name['iam_binding'].message_type = google_dot_iam_dot"
    "_v1_dot_policy__pb2.google_dot_iam_dot_v1_dot_policy__pb2._BINDING",
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
    "google/cloud/asset_v*/proto/assets_pb2.py",
    _BORKED_ASSET_DOCSTRING,
    _FIXED_ASSET_DOCSTRING,
)

s.replace(
    "google/cloud/**/asset_service_client.py",
    "google-cloud-cloudasset",
    "google-cloud-asset",
)
# Fix docstrings with no summary line
s.replace(
    "google/cloud/**/proto/*_pb2.py",
    r''''__doc__': """Attributes:''',
    ''''__doc__' : """
    Attributes:''',
)

# Fix accesscontextmanager and orgpolicy imports
s.replace(
    "google/cloud/asset_v1/types.py",
    "from google\.cloud\.asset_v1\.proto import ((access_level_pb2)|(service_perimeter_pb2)|(access_policy_pb2))",
    "from google.identity.accesscontextmanager.v1 import \g<1>",
)

s.replace(
    "google/cloud/asset_v1/types.py",
    "from google\.cloud\.asset_v1\.proto import orgpolicy_pb2",
    "from google.cloud.orgpolicy.v1 import orgpolicy_pb2",
)

# Glue in Project Path Method.
# TODO: Remove during microgenerator transition
count = s.replace(
    [
        "google/cloud/asset_v1/gapic/asset_service_client.py",
        "google/cloud/asset_v1beta1/gapic/asset_service_client.py",
    ],
    "(def __init__\()",
    '''@classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )
    \g<1>''',
)
if count != 2:
    raise Exception("``project_path`` method not added.")

# Keep same parameter order to avoid breaking existing calls
# Not re-ordering the docstring as that is more likely to break
# TODO: Remove during microgenerator transition
count = s.replace(
    [
        "google/cloud/asset_v1/gapic/asset_service_client.py",
        "google/cloud/asset_v1beta1/gapic/asset_service_client.py",
    ],
    """def batch_get_assets_history\(
            self,
            parent,
            asset_names=None,
            content_type=None,
            read_time_window=None,
            retry=google\.api_core\.gapic_v1\.method\.DEFAULT,
            timeout=google\.api_core\.gapic_v1\.method\.DEFAULT,
            metadata=None\):""",
    """def batch_get_assets_history(
            self,
            parent,
            content_type=None,
            read_time_window=None,
            asset_names=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):""",
)
if count != 2:
    raise Exception("Parameter order replace not made.")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = gcp.CommonTemplates().py_library(unit_cov_level=79, cov_level=80)
s.move(templated_files)

#s.shell.run(["nox", "-s", "blacken"], hide_output=False)
