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
versions = ["v1beta1", "v1"]
admin_versions = ["v1"]


# ----------------------------------------------------------------------------
# Generate firestore GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="firestore",
        version=version,
        bazel_target=f"//google/firestore/{version}:firestore-{version}-py",
        include_protos=True,
    )

    s.move(library / f"google/cloud/firestore_{version}/proto")
    s.move(library / f"google/cloud/firestore_{version}/gapic")
    s.move(library / f"tests/unit/gapic/{version}")

    s.replace(
        f"tests/unit/gapic/{version}/test_firestore_client_{version}.py",
        f"from google.cloud import firestore_{version}",
        f"from google.cloud.firestore_{version}.gapic import firestore_client",
    )

    s.replace(
        f"tests/unit/gapic/{version}/test_firestore_client_{version}.py",
        f"client = firestore_{version}.FirestoreClient",
        "client = firestore_client.FirestoreClient",
    )


# ----------------------------------------------------------------------------
# Generate firestore admin GAPIC layer
# ----------------------------------------------------------------------------
for version in admin_versions:
    library = gapic.py_library(
        service="firestore_admin",
        version=version,
        bazel_target=f"//google/firestore/admin/{version}:firestore-admin-{version}-py",
        include_protos=True,
    )
    s.move(library / f"google/cloud/firestore_admin_{version}")
    s.move(library / "tests")

    s.replace(
        f"google/cloud/firestore_admin_{version}/gapic/firestore_admin_client.py",
        "'google-cloud-firestore-admin'",
        "'google-cloud-firestore'",
    )

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=99)
s.move(templated_files)

s.replace(
    "noxfile.py",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "FIRESTORE_APPLICATION_CREDENTIALS",
)

s.replace(
    "noxfile.py",
    '"--quiet", system_test',
    '"--verbose", system_test',
)


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
