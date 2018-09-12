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

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

for version in ['v1beta1', 'v1']:
    library = gapic.py_library(
        'redis', version,
        config_path=f'artman_redis_{version}.yaml')

    s.copy(library, excludes=['docs/conf.py', 'docs/index.rst'])


# Set Release Status
release_status = 'Development Status :: 3 - Alpha'
s.replace('setup.py',
          '(release_status = )(.*)$',
          f"\\1'{release_status}'")

# Add Dependencies
s.replace('setup.py',
          'dependencies = \[\n*(^.*,\n)+',
          "\\g<0>    'grpc-google-iam-v1<0.12dev,>=0.11.4',\n")

# Fix the enable API link
s.replace(
    'README.rst',
    r'.. _Enable the Google Cloud Memorystore for Redis API.:  https://cloud.google.com/redis',
    '.. _Enable the Google Cloud Memorystore for Redis API.:  https://console.cloud.google.com/apis/'
    'library/redis.googleapis.com')

# Fix link to product page
s.replace(
    'README.rst',
    r'https://cloud.google.com/redis',
    'https://cloud.google.com/memorystore/')

# Fix link to Client Library Documentation
s.replace(
    'README.rst',
    r'https://googlecloudplatform.github.io/google-cloud-python/stable/redis/usage.html',
    'https://googlecloudplatform.github.io/google-cloud-python/latest/redis/index.html')

# Fix link to Auth instructions
s.replace(
    'README.rst',
    r'https://googlecloudplatform.github.io/google-cloud-python/stable/core/auth.html',
    'https://googlecloudplatform.github.io/google-cloud-python/latest/core/auth.html')
