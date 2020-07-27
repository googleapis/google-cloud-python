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

# ----------------------------------------------------------------------------
#  Add templated files
# ----------------------------------------------------------------------------

# TODO: fetch protos from their source of truth (googleapis/googleapis) and
# generate via Bazel

common = gcp.CommonTemplates()
templated_files = common.py_library()
# TODO: use protoc-docs-plugin to add docstrings to protos
s.move(templated_files / ".kokoro", excludes=["docs/**/*", "publish-docs.sh"])
s.move(templated_files / "setup.cfg")
s.move(templated_files / "LICENSE")
s.move(templated_files / "CODE_OF_CONDUCT.md")
s.move(templated_files / ".github")
s.move(templated_files / ".gitignore")


# Add license headers
python.fix_pb2_headers()