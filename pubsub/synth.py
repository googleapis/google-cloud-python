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

import re

import synthtool as s
from synthtool import gcp

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()
version = 'v1'

# ----------------------------------------------------------------------------
# Generate pubsub GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    'pubsub', version, config_path='/google/pubsub/artman_pubsub.yaml')
s.move(
    library,
    excludes=[
        'docs/**/*', 'nox.py', 'README.rst', 'setup.py',
        'google/cloud/pubsub_v1/__init__.py', 'google/cloud/pubsub_v1/types.py'])

# Adjust tests to import the clients directly.
s.replace(
    'tests/unit/gapic/v1/test_publisher_client_v1.py',
    'from google.cloud import pubsub_v1',
    'from google.cloud.pubsub_v1.gapic import publisher_client')

s.replace(
    'tests/unit/gapic/v1/test_publisher_client_v1.py',
    ' pubsub_v1',
    ' publisher_client')

s.replace(
    'tests/unit/gapic/v1/test_subscriber_client_v1.py',
    'from google.cloud import pubsub_v1',
    'from google.cloud.pubsub_v1.gapic import subscriber_client')

s.replace(
    'tests/unit/gapic/v1/test_subscriber_client_v1.py',
    ' pubsub_v1',
    ' subscriber_client')

# DEFAULT SCOPES are being used. so let's force them in.
s.replace(
    'google/cloud/pubsub_v1/gapic/*er_client.py',
    '# The name of the interface for this client. This is the key used to',
    '''# The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/pubsub', )

    \g<0>'''
)

s.replace(
    'google/cloud/pubsub_v1/gapic/publisher_client.py',
    'import google.api_core.gapic_v1.method\n',
    '\g<0>import google.api_core.path_template\n'
)

# Doc strings are formatted poorly
s.replace(
    'google/cloud/pubsub_v1/proto/pubsub_pb2.py',
    'DESCRIPTOR = _MESSAGESTORAGEPOLICY,\n\s+__module__.*\n\s+,\n\s+__doc__ = """',
    '\g<0>A message storage policy.\n\n\n    '
)

s.replace(
    'google/cloud/pubsub_v1/gapic/subscriber_client.py',
    'subscription \(str\): The subscription whose backlog .*\n(.*\n)+?'
    '\s+Format is .*',
    '''subscription (str): The subscription whose backlog the snapshot retains.
                Specifically, the created snapshot is guaranteed to retain: \\
                 (a) The existing backlog on the subscription. More precisely, this is \\
                     defined as the messages in the subscription's backlog that are \\
                     unacknowledged upon the successful completion of the \\
                     `CreateSnapshot` request; as well as: \\
                 (b) Any messages published to the subscription's topic following the \\
                     successful completion of the CreateSnapshot request. \\

                Format is ``projects/{project}/subscriptions/{sub}``.'''
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = gcp.CommonTemplates().py_library(
    unit_cov_level=97, cov_level=61)
s.move(templated_files)