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
excludes = [
    'README.rst',
    'setup.py',
    'nox*.py',
    'docs/conf.py',
    'docs/index.rst',
]

# ----------------------------------------------------------------------------
# Generate tasks GAPIC layer
# ----------------------------------------------------------------------------
for version in ['v2beta2', 'v2beta3']:
    library = gapic.py_library(
        'tasks', version,
        config_path=f'artman_cloudtasks_{version}.yaml')

    s.copy(library, excludes=excludes)

    # Fix unindentation of bullet list second line
    s.replace(
        f'google/cloud/tasks_{version}/gapic/cloud_tasks_client.py',
        '(        \* .*\n        )([^\s*])',
        '\g<1>  \g<2>')

    s.replace(
        f'google/cloud/tasks_{version}/gapic/cloud_tasks_client.py',
        '(Google IAM .*?_) ',
        '\g<1>_ ')

    # Issues with Anonymous ('__') links. Change to named.
    s.replace(
        f"google/cloud/tasks_{version}/proto/*.py",
        ">`__",
        ">`_")

# Issue in v2beta2
s.replace(
    f'google/cloud/tasks_v2beta2/gapic/cloud_tasks_client.py',
    r'(Sample filter \\"app_engine_http_target: )\*\\".',
    '\g<1>\\*\\".')

# Wrapped link fails due to space in link (v2beta2)
s.replace(
    f"google/cloud/tasks_v2beta2/proto/queue_pb2.py",
    '(uests in queue.yaml/xml) <\n\s+',
    '\g<1>\n          <')

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    unit_cov_level=85, cov_level=85)
s.move(templated_files)
