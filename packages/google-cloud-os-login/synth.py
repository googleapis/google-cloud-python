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
excludes = ["README.rst", "setup.py", "nox*.py", "docs/index.rst"]

# ----------------------------------------------------------------------------
# Generate oslogin GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="oslogin",
    version="v1",
    bazel_target="//google/cloud/oslogin/v1:oslogin-v1-py",
    include_protos=True,
)

s.move(library / "google/cloud/oslogin_v1")

s.move(library / "google/cloud/oslogin", excludes=[library / "google/cloud/oslogin/common/**/*"])
s.move(library / "google/cloud/oslogin/common", "google/cloud/oslogin_v1/common", excludes=[library / "google/cloud/oslogin/common/services"])

s.move(library / "tests/unit/gapic/oslogin_v1")

s.move(library / "scripts/fixup_oslogin_v1_keywords.py")

s.move(library / "docs", excludes=[library / "docs/index.rst", library / "docs/common"])
s.move(library / "docs/common", "docs/oslogin_v1/common", excludes=[library / "docs/common/services.rst"])
s.replace(
    "docs/oslogin_v1/common/types.rst",
    "google.cloud.oslogin.common.types",
    "google.cloud.oslogin_v1.common"
)

s.replace(
    "google/cloud/oslogin_v1/**/*.py",
    "google-cloud-oslogin",
    "google-cloud-os-login",
)

for file in ["google/cloud/**/*.py", "tests/**/*.py"]:
    s.replace(
        file,
        "from google.cloud.oslogin.common import common_pb2 as common",
        "from google.cloud.oslogin_v1 import common"
    )
s.replace(
    "google/cloud/oslogin_v1/**/*.py",
    "google.cloud.oslogin.common",
    "google.cloud.oslogin.v1"
)
s.replace(
    "google/cloud/oslogin_v1/**/*.py",
    "SshPublicKey.FromString",
    "SshPublicKey.deserialize"
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
