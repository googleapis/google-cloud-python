# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import subprocess

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python
from synthtool.sources import git

GOOGLEAPIS_REPO = "googleapis/googleapis"

# Clean up googleapis
shutil.rmtree("googleapis", ignore_errors=True)

# Clone googleapis
googleapis_url = git.make_repo_clone_url(GOOGLEAPIS_REPO)
subprocess.run(["git", "clone", googleapis_url])

# This is required in order for s.copy() to work
s._tracked_paths.add("googleapis")

# Create folders for dependencies of the protos that we want to compile
common_apis = [
    "google/api",
    "google/iam/v1",
    "google/rpc",
    "google/rpc/context",
    "google/type",
]
_ = [os.makedirs(dir, exist_ok=True) for dir in common_apis]

# Copy dependencies of the protos that we want to compile from googleapis
s.copy("googleapis/google/api/*.proto", "google/api")
s.copy("googleapis/google/iam/v1/*.proto", "google/iam/v1")
s.copy("googleapis/google/rpc/context/attribute_context.proto", "google/rpc/context")
s.copy("googleapis/google/rpc/status.proto", "google/rpc")
s.copy("googleapis/google/type/*.proto", "google/type")

# Copy the protos that we want to compile from googleapis
s.copy("googleapis/google/cloud/audit/*.proto", "google/cloud/audit")

# Clean up googleapis
shutil.rmtree("googleapis")

# ----------------------------------------------------------------------------
#  Add templated files
# ----------------------------------------------------------------------------

# TODO: generate via Bazel

common = gcp.CommonTemplates()
templated_files = common.py_library()
# TODO: use protoc-docs-plugin to add docstrings to protos
s.move(templated_files / ".kokoro", excludes=["docs/**/*", "publish-docs.sh"])
s.move(templated_files / "setup.cfg")
s.move(templated_files / "LICENSE")
s.move(templated_files / "CODE_OF_CONDUCT.md")
s.move(templated_files / ".github", excludes=["workflows"])
s.move(templated_files / ".gitignore")
s.move(templated_files / "renovate.json")

# Generate _pb2.py files and format them
s.shell.run(["nox", "-s", "generate_protos"], hide_output=False)

# Clean up the folders for dependencies which are shipped via `googleapis-common-protos`
# We should not ship them via this repository
_ = [shutil.rmtree(dir, ignore_errors=True) for dir in common_apis]

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

# Add license headers
python.fix_pb2_headers()
