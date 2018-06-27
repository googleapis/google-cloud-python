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

# tasks has two product names, and a poorly named artman yaml
v2beta2_library = gapic.py_library(
    'tasks', 'v2beta2',
    config_path='artman_cloudtasks.yaml')

s.copy(v2beta2_library)

# Set Release Status
release_status = 'Development Status :: 3 - Alpha'
s.replace('setup.py',
          '(release_status = )(.*)$',
          f"\\1'{release_status}'")

# Add Dependencies
s.replace('setup.py',
          'dependencies = \[\n*(^.*,\n)+',
          "\\g<0>    'grpc-google-iam-v1<0.12dev,>=0.11.4',\n")

# Correct Naming of package
s.replace('**/*.rst',
          'google-cloud-cloud-tasks',
          'google-cloud-tasks')
s.replace('**/*.py',
          'google-cloud-cloud-tasks',
          'google-cloud-tasks')
s.replace('README.rst',
          '/cloud-tasks',
          '/tasks')

# Correct calls to routing_header
# https://github.com/googleapis/gapic-generator/issues/2016
s.replace(
    "google/cloud/*/gapic/*_client.py",
    "routing_header\(",
    "routing_header.to_grpc_metadata(")

# metadata in tests in none but should be empty list.
# https://github.com/googleapis/gapic-generator/issues/2014
s.replace(
    "google/cloud/*/gapic/*_client.py",
    'def .*\(([^\)]+)\n.*metadata=None\):\n\s+"""(.*\n)*?\s+"""\n',
    '\g<0>'
    '        if metadata is None:\n'
    '            metadata = []\n'
    '        metadata = list(metadata)\n')


# empty objects trying to get attrs
# https://github.com/googleapis/gapic-generator/issues/2015
s.replace(
    "google/cloud/*/gapic/*_client.py",
    "(^        )(routing_header = google.api_core.gapic_v1.routing_header"
    ".to_grpc_metadata\(\n)"
    "(\s+)(\[\('[a-z\_]*?\.name', )([a-z\_]*?)(.name\)\], \)\n)"
    "(\s+metadata.append\(routing_header\)\n)",
    "\g<1>if hasattr(\g<5>, 'name'):\n"
    "\g<1>    \g<2>\g<3>    \g<4>\g<5>\g<6>    \g<7>"
)


# fix the combined shared/local modules. 
# https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5364
# https://github.com/googleapis/gapic-generator/issues/2058
s.replace(
    "google/cloud/*/types.py",
    "for module in \(\n(.*\n)*?\):\n(    .*\n)+",
    """_shared_modules = [
    http_pb2,
    iam_policy_pb2,
    policy_pb2,
    any_pb2,
    descriptor_pb2,
    duration_pb2,
    empty_pb2,
    field_mask_pb2,
    timestamp_pb2,
    status_pb2,
]

_local_modules = [
    cloudtasks_pb2,
    queue_pb2,
    target_pb2,
    task_pb2,
]

for module in _shared_modules:
    for name, message in get_messages(module).items():
        setattr(sys.modules[__name__], name, message)
        names.append(name)

for module in _local_modules:
    for name, message in get_messages(module).items():
        message.__module__ = 'google.cloud.tasks_v2beta2.types'
        setattr(sys.modules[__name__], name, message)
        names.append(name)
""")
