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
import synthtool.gcp as gcp
import logging

logging.basicConfig(level=logging.DEBUG)

client_library_version = '0.1.0'

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

version = 'v1beta1'
library = gapic.py_library(
    'kms', version, config_path='artman_cloudkms.yaml',
    artman_output_name='kms-v1')

s.copy(library)

# Set Release Status
release_status = 'Development Status :: 3 - Alpha'
s.replace('setup.py',
          '(release_status = )(.*)$',
          f"\\1'{release_status}'")
s.replace('setup.py', 'version = .*', f"version = '{client_library_version}'")

# Wrong import name. Drop _grpc
# https://github.com/googleapis/gapic-generator/issues/2160
s.replace("**/*.py", "iam_policy_pb2_grpc", "iam_policy_pb2")
