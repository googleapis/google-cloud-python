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

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    s.move(library / f"google/cloud/oslogin_{library.name}")
    s.move(library / "google/cloud/oslogin", excludes=[ "common/**/*"])
    s.move(library / "google/cloud/oslogin/common", f"google/cloud/oslogin_{library.name}/common", excludes=["services"])
    s.move(library / f"tests/unit/gapic/oslogin_{library.name}")
    s.move(library / f"scripts/fixup_oslogin_{library.name}_keywords.py")
    s.move(library / "docs", excludes=["index.rst", "common"])
    s.move(library / f"docs/common", f"docs/oslogin_{library.name}/common", excludes=["services.rst"])
    s.move(library / "samples")

s.remove_staging_dirs()

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

s.replace(
    ["google/cloud/**/*.py", "tests/**/*.py"],
    "from google.cloud.oslogin.common import common_pb2",
    "from google.cloud.oslogin_v1 import common"
)
s.replace(
    ["google/cloud/**/*.py", "tests/**/*.py"],
    "common_pb2\.",
    "common."
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
    cov_level=100,
)

s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

python.py_samples(skip_readmes=True)

python.configure_previous_major_version_branches()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
