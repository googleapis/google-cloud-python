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

s.move(library / "google/cloud/iam_credentials_v1/proto")
s.move(library / "google/iam/credentials/", "google/cloud/iam_credentials")
s.move(library / "google/iam/credentials_v1", "google/cloud/iam_credentials_v1")
s.move(library / "tests")
s.move(library / "scripts")
s.move(library / "docs", excludes=[library / "docs/index.rst"])

# Fix namespace
s.replace(
    "google/cloud/**/*.py",
    "google.iam.credentials_v1",
    "google.cloud.iam_credentials_v1",
)
s.replace(
    "tests/unit/gapic/**/*.py",
    "google.iam.credentials_v1",
    "google.cloud.iam_credentials_v1",
)
s.replace(
    "docs/**/*.rst",
    "google.iam.credentials_v1",
    "google.cloud.iam_credentials_v1",
)

# Rename package to `google-cloud-build`
s.replace(
    ["**/*.rst", "*/**/*.py", "**/*.md"],
    "google-iam-credentials",
    "google-cloud-iam"
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
    cov_level=99,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

s.replace(
    "noxfile.py",
    "google.cloud.iam",
    "google.cloud.iam_credentials_v1",
)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
