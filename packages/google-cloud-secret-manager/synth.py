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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate secret manager GAPIC layer
# ----------------------------------------------------------------------------

versions = [
    # v1beta1 has a special config path so it must be passed explicitly
    ("v1beta1", "//google/cloud/secrets/v1beta1:secretmanager-v1beta1-py"),
    ("v1", "//google/cloud/secretmanager/v1:secretmanager-v1-py"),
]

for version, bazel_target in versions:
    library = gapic.py_library(
        service="secretmanager",
        version=version,
        bazel_target=bazel_target,
    )

    s.move(
        library,
        excludes=[
            f"google/cloud/secrets_{version}/proto",
            "nox.py",
            "setup.py",
            "README.rst",
            "docs/index.rst",
        ],
    )

    # protos are copied to the wrong location by default, so move separately
    s.move(
        library / f"google/cloud/secrets_{version}/proto",
        f"google/cloud/secretmanager_{version}/proto",
    )

    # correct proto import parth
    s.replace(
        "google/cloud/**/proto/*.py",
        rf"from google\.cloud\.secrets_{version}\.proto",
        f"from google.cloud.secretmanager_{version}.proto",
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

# Fix package name (v1beta1)
s.replace(
    ["docs/conf.py", "google/**/*.py", "README.rst", "setup.py"],
    "google-cloud-secretmanager",
    "google-cloud-secret-manager",
)

# Fix package name (v1)
s.replace(
    ["docs/conf.py", "google/**/*.py", "README.rst", "setup.py"],
    "google-cloud-secrets",
    "google-cloud-secret-manager",
)

# fix links in README
s.replace(
    "README.rst",
    "https://cloud\.google\.com/secrets",
    "https://cloud.google.com/secret-manager",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=75, samples=True)
s.move(templated_files)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples()

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
