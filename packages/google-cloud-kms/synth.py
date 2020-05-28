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
import synthtool.gcp as gcp
from synthtool.languages import python
import logging

logging.basicConfig(level=logging.DEBUG)

client_library_version = "0.1.0"

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
version = "v1"

# ----------------------------------------------------------------------------
# Generate kms GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="kms",
    version=version,
    bazel_target="//google/cloud/kms/v1:kms-v1-py",
    include_protos=True,
)

s.move(library, excludes=["README.rst", "setup.py", "nox*.py", "docs/**/*"])

# Temporary fixup for 'grpc-google-iam-vi 0.12.4' (before generation).
s.replace(
    "google/cloud/kms_v1/gapic/transports/key_management_service_grpc_transport.py",
    "from google.iam.v1 import iam_policy_pb2",
    "from google.iam.v1 import iam_policy_pb2_grpc as iam_policy_pb2",
)
# re-insert `crypto_key_path_path` method as this was used in the published samples
# TODO: remove when this library is moved to the microgenerator and mention it in the relase
# notes
count = s.replace("google/cloud/kms_v1/gapic/key_management_service_client.py",
"""(@classmethod
\s+def crypto_key_version_path\(.*)""",
"""
    @classmethod	
    def crypto_key_path_path(cls, project, location, key_ring, crypto_key_path):	
        \"\"\"Return a fully-qualified crypto_key_path string.\"\"\"	
        return google.api_core.path_template.expand(	
            "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key_path=**}",	
            project=project,	
            location=location,	
            key_ring=key_ring,	
            crypto_key_path=crypto_key_path,	
        )

    \g<1>
""")

if count != 1:
    raise Exception("Required insertion of `crypto_key_path_path` not made.")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=70, samples=True)
s.move(templated_files)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
