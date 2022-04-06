# Copyright 2022 Google LLC
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

import os
import subprocess
import shutil

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python
from synthtool.sources import git

GOOGLEAPIS_REPO = "googleapis/googleapis"

# Clone googleapis
googleapis_url = git.make_repo_clone_url(GOOGLEAPIS_REPO)
subprocess.run(["git", "clone", googleapis_url])

# This is required in order for s.copy() to work
s._tracked_paths.add("googleapis")

s.copy("googleapis/google/iam/v1/*.proto", "google/iam/v1")
s.copy("googleapis/google/iam/v1/logging/*.proto", "google/iam/v1/logging")

os.mkdir('google/type')
os.mkdir('google/api')
s.copy("googleapis/google/type/expr.proto", "google/type")
s.copy("googleapis/google/api/*.proto", "google/api")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library()
s.move(templated_files / ".kokoro", excludes=["docs/**/*", "publish-docs.sh"])
s.move(templated_files / "LICENSE")
s.move(templated_files / "*.rst")
s.move(templated_files / "*.md")
s.move(templated_files / ".github", excludes=["workflows"])

python.py_samples(skip_readmes=True)

# Generate _pb2.py files and format them
s.shell.run(["nox", "-s", "generate_protos"], hide_output=False)

# Clean up googleapis
shutil.rmtree('googleapis')

# Clean up google/api
shutil.rmtree('google/api')

# Clean up google/type
shutil.rmtree('google/type')

# ----------------------------------------------------------------------------
# Run blacken session
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)