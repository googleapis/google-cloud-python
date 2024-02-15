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
import re
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

common_apis = [
    "google/api",
    "google/iam/v1",
    "google/longrunning",
    "google/rpc",
    "google/type",
]

# Create folders for dependencies of the protos that we want to compile
_ = [os.makedirs(dir, exist_ok=True) for dir in common_apis]

# Copy dependencies of the protos that we want to compile from googleapis
_ = [s.copy(f"googleapis/{dir}/*.proto", dir) for dir in common_apis]

# Copy the protos that we want to compile from googleapis
s.copy(
    "googleapis/google/identity/accesscontextmanager/v1/*.proto",
    "google/identity/accesscontextmanager/v1",
)
s.copy(
    "googleapis/google/identity/accesscontextmanager/type/*.proto",
    "google/identity/accesscontextmanager/type",
)

# Clean up googleapis
shutil.rmtree("googleapis")

# ----------------------------------------------------------------------------
#  Add templated files
# ----------------------------------------------------------------------------
common = gcp.CommonTemplates()
templated_files = common.py_library(microgenerator=True)

s.move(
    templated_files,
    excludes=[
        ".coveragerc",
        ".gitignore",
        ".github/workflows",
        "noxfile.py",
        "README.rst",
    ],
)

python.py_samples(skip_readmes=True)

# Generate _pb2.py files and format them
s.shell.run(["nox", "-s", "generate_protos"])

# Clean up the folders for dependencies which are shipped via `googleapis-common-protos`
# We should not ship them via this repository
_ = [shutil.rmtree(dir) for dir in common_apis]

# Also clean up "google/iam" directory
shutil.rmtree("google/iam")

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

# Add license headers
python.fix_pb2_headers()
