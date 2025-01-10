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
import synthtool.gcp as gcp
from synthtool.languages import python


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

for library in s.get_staging_dirs():
    s.move([library / "**/*.py*"])
s.remove_staging_dirs()

templated_files = gcp.CommonTemplates().py_library()
s.move(templated_files / ".kokoro")
s.replace(
    ".kokoro/docs/common.cfg",
    """# Push non-cloud library docs to `docs-staging-v2-staging` instead of the
    # Cloud RAD bucket `docs-staging-v2`
    value: \"docs-staging-v2-staging\"""",
    """# Allow publishing docs for this library.
    value: \"docs-staging-v2\"""",
)

s.move(templated_files / "docs", excludes=["multiprocessing.rst"])
s.move(templated_files / "LICENSE")
s.move(templated_files / "CONTRIBUTING.rst")
s.move(templated_files / "*.md")
s.move(templated_files / "renovate.json")
s.move(templated_files / ".github", excludes=["workflows/unittest.yml"])
s.move(templated_files / ".trampolinerc")

python.py_samples(skip_readmes=True)

# Add license headers
python.fix_pb2_headers()

# ----------------------------------------------------------------------------
# Run blacken session
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
