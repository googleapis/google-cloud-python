# Copyright 2019 Google LLC
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
import os

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate secret manager GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "secretmanager", "v1beta1", config_path="/google/cloud/secrets/artman_secretmanager_v1beta1.yaml"
)

s.move(library, excludes=["google/cloud/secrets_v1beta1/proto", "nox.py", "setup.py", "README.rst", "docs/index.rst"])

# protos are copied to the wrong location by default, so move separately
s.move(
    library / "google/cloud/secrets_v1beta1/proto",
    "google/cloud/secretmanager_v1beta1/proto",
)

# correct proto import parth
s.replace(
    "google/cloud/**/proto/*.py",
    r"from google\.cloud\.secrets_v1beta1\.proto",
    "from google.cloud.secretmanager_v1beta1.proto",
)

# fix import path for iam
s.replace(
    "google/**/gapic/transports/*_grpc_transport.py",
    "from google.iam.v1 import iam_policy_pb2 ",
    "from google.iam.v1 import iam_policy_pb2_grpc as iam_policy_pb2",
)

# correct license headers
python.fix_pb2_headers()
python.fix_pb2_grpc_headers()

# Fix package name
s.replace(
    ["docs/conf.py", "google/**/*.py", "README.rst", "setup.py"],
    "google-cloud-secretmanager",
    "google-cloud-secret-manager",
)

# fix links in README
s.replace("README.rst", "https://cloud\.google\.com/secrets", "https://cloud.google.com/secret-manager")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=75)
s.move(templated_files)

# No local dependencies in a split repo
# Manually remove from noxfile until the template is updated
s.replace("noxfile.py", "LOCAL_DEPS = .*", "LOCAL_DEPS = []")


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
