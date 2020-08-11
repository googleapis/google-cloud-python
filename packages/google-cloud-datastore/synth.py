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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate datastore GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="datastore",
    version="v1",
    bazel_target="//google/datastore/v1:datastore-v1-py",
    include_protos=True,
)

s.move(library / "google/cloud/datastore_v1/proto")
s.move(library / "google/cloud/datastore_v1/gapic")

# ----------------------------------------------------------------------------
# Generate datastore admin GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="datastore_admin",
    version="v1",
    bazel_target="//google/datastore/admin/v1:datastore-admin-v1-py",
    include_protos=True,
)

s.move(
    library / "datastore-admin-v1-py/google/cloud/datastore_admin_v1",
    "google/cloud/datastore_admin_v1"
)

s.move(library / "google/cloud/datastore_admin_v1/proto")

s.replace(
    "google/**/datastore_admin_client.py",
    "google-cloud-datastore-admin",
    "google-cloud-datstore"
)

# Remove spurious markup
s.replace(
    "google/**/datastore_admin_client.py",
    "-----------------------------------------------------------------------------",
    ""
)

# TODO(busunkim): Remove during the microgenerator transition.
# This re-orders the parameters to avoid breaking existing code.
num = s.replace(
"google/**/datastore_client.py",
"""def commit\(
\s+self,
\s+project_id,
\s+mode=None,
\s+transaction=None,
\s+mutations=None,
\s+retry=google\.api_core\.gapic_v1\.method\.DEFAULT,
\s+timeout=google\.api_core\.gapic_v1\.method\.DEFAULT,
\s+metadata=None\):""",
"""def commit(
        self,
        project_id,
        mode=None,
        mutations=None,
        transaction=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):"""
)

if num != 1:
    raise Exception("Required replacement not made.")
# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=99)
s.move(templated_files, excludes=["docs/conf.py", "docs/multiprocessing.rst"])

s.replace("noxfile.py", """["']sphinx['"]""", '''"sphinx<3.0.0"''')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
