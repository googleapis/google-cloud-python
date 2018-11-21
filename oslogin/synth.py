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

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate oslogin GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    'oslogin',
    'v1',
    config_path='/google/cloud/oslogin/artman_oslogin_v1.yaml',
    artman_output_name='os-login-v1')

s.move(library / 'google/cloud/oslogin_v1')
s.move(library / 'tests/unit/gapic/v1')

# Fix up imports
s.replace(
    'google/**/proto/*.py',
    'from google.cloud.oslogin.common import common_pb2',
    'from google.cloud.oslogin_v1.proto import common_pb2',
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    unit_cov_level=97, cov_level=100)
s.move(templated_files)
