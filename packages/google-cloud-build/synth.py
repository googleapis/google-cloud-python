# Copyright 2019 Google LLC
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
version = 'v1'

# ----------------------------------------------------------------------------
# Generate cloudbuild GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service='cloudbuild',
    version=version,
    bazel_target=f"//google/devtools/cloudbuild/{version}:devtools-cloudbuild-{version}-py",
    include_protos=True,
    proto_output_path=f"google/devtools/cloudbuild_{version}/proto",
)

s.move(library / "google/devtools/cloudbuild", "google/cloud/devtools/cloudbuild")
s.move(
    library / f"google/devtools/cloudbuild_{version}",
    f"google/cloud/devtools/cloudbuild_{version}"
)
s.move(library / "tests")
s.move(library / "scripts")
s.move(library / "docs", excludes=[library / "docs/index.rst"])

# Fix namespace
s.replace(
    f"google/cloud/**/*.py",
    f"google.devtools.cloudbuild_{version}",
    f"google.cloud.devtools.cloudbuild_{version}",
)
s.replace(
    f"tests/unit/gapic/**/*.py",
    f"google.devtools.cloudbuild_{version}",
    f"google.cloud.devtools.cloudbuild_{version}",
)
s.replace(
    f"google/cloud/**/*.py",
    f"google.devtools.cloudbuild_{version}",
    f"google.cloud.devtools.cloudbuild_{version}",
)
s.replace(
    f"docs/**/*.rst",
    f"google.devtools.cloudbuild_{version}",
    f"google.cloud.devtools.cloudbuild_{version}",
)

# Rename package to `google-cloud-build`
s.replace(
    ["**/*.rst", "*/**/*.py", "**/*.md"],
    "google-cloud-devtools-cloudbuild",
    "google-cloud-build"
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
    cov_level=99,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

s.replace(
    "noxfile.py",
    "google.cloud.cloudbuild",
    "google.cloud.devtools.cloudbuild",
)


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
