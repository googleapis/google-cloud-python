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

import synthtool as s
from synthtool.sources import git
import synthtool.gcp as gcp

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
#  Treat api-common-protos repo as source
# ----------------------------------------------------------------------------
url = git.make_repo_clone_url("googleapis/api-common-protos")
api_common_protos = git.clone(url) / "google"

# ----------------------------------------------------------------------------
#  Copy protos to this repo, excluding IAM which is published separately
# ----------------------------------------------------------------------------
s.copy(api_common_protos, excludes=["iam/**/*"])

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library()
s.move(templated_files / ".kokoro", excludes=["docs/**/*", "publish-docs.sh"])
s.move(templated_files / "setup.cfg")

# Generate _pb2.py files and format them
s.shell.run(["nox", "-s", "generate_protos"], hide_output=False)
s.shell.run(["nox", "-s", "blacken"], hide_output=False)
