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

    # # Fix unindentation of bullet list second line
    # s.replace(
    #     f'google/cloud/tasks_{version}/gapic/cloud_tasks_client.py',
    #     '(        \* .*\n        )([^\s*])',
    #     '\g<1>  \g<2>')
    #
    # s.replace(
    #     f'google/cloud/tasks_{version}/gapic/cloud_tasks_client.py',
    #     '(Google IAM .*?_) ',
    #     '\g<1>_ ')
    #
    # # Issues with Anonymous ('__') links. Change to named.
    # s.replace(
    #     f"google/cloud/tasks_{version}/proto/*.py",
    #     ">`__",
    #     ">`_")


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
