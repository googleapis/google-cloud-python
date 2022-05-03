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

import synthtool as s
from synthtool.gcp import CommonTemplates

templated_files = CommonTemplates().py_library()
s.move(
    templated_files / ".kokoro",
    excludes=["samples/**/*", "test-samples*", "publish-docs.sh"],
)

# remove docfx build
assert 1 == s.replace(
    ".kokoro/docs/docs-presubmit.cfg",
    'value: "docs docfx"',
    'value: "docs"',
)

# needed for docs build
s.move(templated_files / ".trampolinerc")

s.move(templated_files / "LICENSE")
s.move(templated_files / ".github", excludes=["workflows", "CODEOWNERS"])
