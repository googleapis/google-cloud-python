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
from synthtool.languages import python

common = gcp.CommonTemplates()

spanner_default_version = "v1"
spanner_admin_instance_default_version = "v1"
spanner_admin_database_default_version = "v1"

for library in s.get_staging_dirs(spanner_default_version):
    if library.parent.absolute() == "spanner":
        s.move(library, excludes=["google/cloud/spanner/**", "*.*", "docs/index.rst", "google/cloud/spanner_v1/__init__.py"])

s.remove_staging_dirs()

for library in s.get_staging_dirs(spanner_admin_instance_default_version):
    if library.parent.absolute() == "spanner_admin_instance":
        s.move(library, excludes=["google/cloud/spanner_admin_instance/**", "*.*", "docs/index.rst"])

s.remove_staging_dirs()

for library in s.get_staging_dirs(spanner_admin_database_default_version):
    if library.parent.absolute() == "spanner_admin_database":
        s.move(library, excludes=["google/cloud/spanner_admin_database/**", "*.*", "docs/index.rst"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(microgenerator=True, samples=True)
s.move(templated_files, excludes=[".coveragerc", "noxfile.py"])

# Ensure CI runs on a new instance each time
s.replace(
    ".kokoro/build.sh",
    "# Remove old nox",
    "# Set up creating a new instance for each system test run\n"
    "export GOOGLE_CLOUD_TESTS_CREATE_SPANNER_INSTANCE=true\n"
    "\n\g<0>",
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
