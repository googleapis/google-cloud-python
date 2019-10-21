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

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()
version = 'v1'

# ----------------------------------------------------------------------------
# Generate cloudbuild GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    'cloudbuild',
    version,
    config_path='/google/devtools/cloudbuild/artman_cloudbuild.yaml',
    generator_args=["--dev_samples"],
    include_protos=True
)

s.move(
    library,
    excludes=[
        'docs/conf.py',
        'docs/index.rst',
        # 'README.rst',
        'nox*.py',
        'setup.py',
        'setup.cfg',
    ],
)

# Move protos to the right directory
s.move("google/cloud/cloudbuild_v1/proto/", "google/cloud/devtools/cloudbuild_v1/")

# Fix up imports
s.replace(
    ["google/**/*.py", "tests/unit/**/*.py"],
    r"from google.devtools.cloudbuild_v1.proto import ",
    r"from google.cloud.devtools.cloudbuild_v1.proto import ",
)


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=74, cov_level=74)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
