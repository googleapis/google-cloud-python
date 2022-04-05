# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # Rename package to 'google-cloud-binary-authorization'
    s.replace(
        [library / "google/**/*.py", library / "tests/**/*.py"],
        "google-cloud-binaryauthorization",
        "google-cloud-binary-authorization",
    )

    if library.name == "v1":
        # Fix import of grafeas
        s.replace(
            [library / "google/**/*.py", library / "tests/**/*.py"],
            "from grafeas.v1",
            "from grafeas.grafeas_v1",
        )

        s.replace(
            [library / "google/**/*.py", library / "tests/**/*.py"],
            "from grafeas.grafeas_v1 import attestation_pb2",
            "from grafeas.grafeas_v1.types import attestation",
        )

        s.replace(
            [library / "google/**/*.py", library / "tests/**/*.py"],
            "from grafeas.grafeas_v1 import common_pb2",
            "from grafeas.grafeas_v1.types import common",
        )

        s.replace(
            [library / "google/**/*.py", library / "tests/**/*.py"],
            "message=attestation_pb2",
            "message=attestation",
        )

        s.replace(
            [library / "google/**/*.py", library / "tests/**/*.py"],
            "grafeas.v1.attestation_pb2.AttestationOccurrence",
            "grafeas.grafeas_v1.types.attestation.AttestationOccurrence",
        )

    s.move(library, excludes=["setup.py", "README.rst", "docs/index.rst"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = common.py_library(cov_level=100, microgenerator=True)
python.py_samples(skip_readmes=True)
s.move(
    templated_files,
    excludes=[".coveragerc"],  # the microgenerator has a good coveragerc file
)

python.configure_previous_major_version_branches()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
