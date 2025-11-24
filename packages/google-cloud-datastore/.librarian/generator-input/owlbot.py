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
from pathlib import Path
from typing import List, Optional

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

# This library ships clients for two different APIs,
# Datastore and Datastore Admin
datastore_default_version = "v1"
datastore_admin_default_version = "v1"

for library in s.get_staging_dirs(datastore_default_version):
    s.move(library / f"google/cloud/datastore_{library.name}")
    s.move(library / "tests/")
    s.move(library / "scripts")

for library in s.get_staging_dirs(datastore_admin_default_version):

    s.move(library / f"google/cloud/datastore_admin")
    s.move(library / f"google/cloud/datastore_admin_{library.name}")
    s.move(library / "tests")
    s.move(library / "scripts")

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    microgenerator=True,
    split_system_tests=True,
    # six required by (but not installed by) google-cloud-core < v2.0.0
    unit_test_external_dependencies=["six"],
    system_test_external_dependencies=["six"],
    cov_level=100,
    unit_test_python_versions=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"],
    default_python_version="3.14",
    system_test_python_versions=["3.14"],
)
s.move(
    templated_files,
    excludes=["docs/multiprocessing.rst", ".coveragerc", ".github/**", ".kokoro/**"],
)

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
