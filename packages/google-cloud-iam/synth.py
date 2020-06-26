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

# ----------------------------------------------------------------------------
# Generate automl GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="iam_credentials",
    version="v1",
    bazel_target="//google/iam/credentials/v1:iam-credentials-v1-py",
    include_protos=True,
)

excludes = [
    "README.rst",
    "setup.py",
    "docs/index.rst",
    "nox.py",
]
s.copy(library, excludes=excludes)

s.replace(
    "google/**/*.py",
    "google-cloud-iam-credentials",
    "google-cloud-iam"
)
s.replace(
    "docs/**/*.py",
    "google-cloud-iam-credentials",
    "google-cloud-iam"
)

s.replace(
    "**/*.py",
    "from google\.iam\.credentials\.v1 import common_pb2",
    "from google.cloud.iam_credentials_v1.proto import common_pb2"
)
s.replace(
    "**/*.py",
    "from google\.iam\.credentials\.v1 import iamcredentials_pb2_grpc",
    "from google.cloud.iam_credentials_v1.proto import iamcredentials_pb2_grpc"
)

s.replace(
    "google/cloud/iam_credentials_v1/proto/common_pb2.py",
    "\"\"\"Attributes:\n",
    "\"\"\"\nAttributes:\n"
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=76)
s.move(templated_files)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
