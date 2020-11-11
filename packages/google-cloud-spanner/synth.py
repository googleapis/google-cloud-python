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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate spanner GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="spanner",
    version="v1",
    bazel_target="//google/spanner/v1:spanner-v1-py",
    include_protos=True,
)

s.move(library, excludes=["google/cloud/spanner/**", "*.*", "docs/index.rst", "google/cloud/spanner_v1/__init__.py"])

# ----------------------------------------------------------------------------
# Generate instance admin client
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="spanner_admin_instance",
    version="v1",
    bazel_target="//google/spanner/admin/instance/v1:admin-instance-v1-py",
    include_protos=True,
)

s.move(library, excludes=["google/cloud/spanner_admin_instance/**", "*.*", "docs/index.rst"])

# ----------------------------------------------------------------------------
# Generate database admin client
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="spanner_admin_database",
    version="v1",
    bazel_target="//google/spanner/admin/database/v1:admin-database-v1-py",
    include_protos=True,
)

s.move(library, excludes=["google/cloud/spanner_admin_database/**", "*.*", "docs/index.rst"])

# Fix formatting for bullet lists.
# See: https://github.com/googleapis/gapic-generator-python/issues/604
s.replace(
    "google/cloud/spanner_admin_database_v1/services/database_admin/*.py",
    "``backup.expire_time``.",
    "``backup.expire_time``.\n"
)

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
