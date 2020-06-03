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


import synthtool as s
import synthtool.gcp as gcp
from synthtool import tmp
from synthtool.languages import python
from synthtool.sources import git

API_COMMON_PROTOS_REPO = "googleapis/api-common-protos"
# ----------------------------------------------------------------------------
#  Get api-common-protos
# ----------------------------------------------------------------------------

# Use api-common-protos as a proper synthtool git source
api_common_protos_url = git.make_repo_clone_url(API_COMMON_PROTOS_REPO)
api_common_protos = git.clone(api_common_protos_url) / "google"


excludes = [
    # Exclude iam protos (they are released in a separate package)
    "iam/**/*",
    "**/BUILD.bazel",
]
s.copy(api_common_protos, excludes=excludes)

# ----------------------------------------------------------------------------
#  Add templated files
# ----------------------------------------------------------------------------
common = gcp.CommonTemplates()
templated_files = common.py_library()
# TODO: use protoc-docs-plugin to add docstrings to protos
s.move(templated_files / ".kokoro", excludes=["docs/**/*", "publish-docs.sh"])
s.move(templated_files / "setup.cfg")
s.move(templated_files / "LICENSE")
s.move(templated_files / ".github")

# longrunning operations directory is non-standard for backwards compatibility
# see comments in directory for details
# Temporarily rename the operations_pb2.py to keep it from getting overwritten
os.replace("google/longrunning/operations_pb2.py", "google/longrunning/operations_pb2-COPY.py")

# Generate _pb2.py files and format them
s.shell.run(["nox", "-s", "generate_protos"], hide_output=False)

# Clean up LRO directory
os.replace(
    "google/longrunning/operations_pb2.py", "google/longrunning/operations_proto_pb2.py.py"
)
os.replace(
    "google/longrunning/operations_pb2-COPY.py", "google/longrunning/operations_pb2.py"
)


s.shell.run(["nox", "-s", "blacken"], hide_output=False)

# Add license headers
python.fix_pb2_headers()
