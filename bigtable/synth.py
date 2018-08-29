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


# Generate client
library = gapic.py_library(
    'bigtable',
    'v2',
    config_path='/google/bigtable/artman_bigtable.yaml',
    artman_output_name='bigtable-v2')

s.move(library / 'google/cloud/bigtable_v2')

# Generate admin client
library = gapic.py_library(
    'bigtable_admin',
    'v2',
    config_path='/google/bigtable/admin/artman_bigtableadmin.yaml',
    artman_output_name='bigtable-admin-v2')

s.move(library / 'google/cloud/bigtable_admin_v2')