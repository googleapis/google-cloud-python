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
# Generate firestore GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    'firestore',
    'v1beta1',
    config_path='/google/firestore/artman_firestore.yaml',
    artman_output_name='firestore-v1beta1')

s.move(library / 'google/cloud/firestore_v1beta1/proto')
s.move(library / 'google/cloud/firestore_v1beta1/gapic')
s.move(library / 'tests/unit/gapic/v1beta1')

s.replace(
    'tests/unit/gapic/v1beta1/test_firestore_client_v1beta1.py',
    'from google.cloud import firestore_v1beta1',
    'from google.cloud.firestore_v1beta1.gapic import firestore_client',
)

s.replace(
    'tests/unit/gapic/v1beta1/test_firestore_client_v1beta1.py',
    'client = firestore_v1beta1.FirestoreClient',
    'client = firestore_client.FirestoreClient',
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    unit_cov_level=97, cov_level=100)
s.move(templated_files)
