# Copyright 2020 Google LLC
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
import pathlib

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python


REPO_ROOT = pathlib.Path(__file__).parent.absolute()

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    s.replace(
        [
            library / "google/cloud/bigquery_reservation_v1/services/reservation_service/client.py",
            library / "google/cloud/bigquery_reservation_v1/services/reservation_service/async_client.py",
        ],
        "assignee=organizations/456``",
        "assignee=organizations/456``\n",
    )
    s.move(library, excludes=["nox.py", "setup.py", "README.rst", "docs/index.rst"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=100, microgenerator=True, samples=True,)
s.move(
    templated_files,
    excludes=[".coveragerc"],  # the microgenerator has a good coveragerc file
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()

# ----------------------------------------------------------------------------
# Final cleanup
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
for noxfile in REPO_ROOT.glob("samples/**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
