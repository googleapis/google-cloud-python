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

version = 'v1'


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

# iam_policy_pb2_grpc doesn't exist.
s.replace(
    ['google/cloud/pubsub_v1/gapic/publisher_client.py',
     'google/cloud/pubsub_v1/gapic/subscriber_client.py'],
    'from google.iam.v1 import iam_policy_pb2_grpc\n',
    '')
s.replace(
    ['google/cloud/pubsub_v1/gapic/transports/publisher_grpc_transport.py',
     'google/cloud/pubsub_v1/gapic/transports/subscriber_grpc_transport.py'],
    'from google.iam.v1 import iam_policy_pb2_grpc\n',
    'from google.iam.v1 import iam_policy_pb2\n')
s.replace(
    'google/cloud/pubsub_v1/gapic/transports/publisher_grpc_transport.py',
    'iam_policy_pb2_grpc',
    'iam_policy_pb2')
s.replace(
    'google/cloud/pubsub_v1/gapic/transports/subscriber_grpc_transport.py',
    'iam_policy_pb2_grpc',
    'iam_policy_pb2')

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


# Stubs are missing
s.replace(
    'google/cloud/pubsub_v1/gapic/subscriber_client.py',
    '^(\s+)if client_info is None:\n',
    '\g<1>self.iam_policy_stub = (iam_policy_pb2.IAMPolicyStub(channel))'
    '\g<1>self.subscriber_stub = (pubsub_pb2_grpc.SubscriberStub(channel))\n'
    '\g<0>'
)

s.replace(
    'google/cloud/pubsub_v1/gapic/publisher_client.py',
    '^(\s+)if client_info is None:\n',
    '\g<1>self.iam_policy_stub = (iam_policy_pb2.IAMPolicyStub(channel))'
    '\g<1>self.publisher_stub = (pubsub_pb2_grpc.PublisherStub(channel))\n'
    '\g<0>'
)

s.replace(
    'google/cloud/pubsub_v1/gapic/publisher_client.py',
    'import google.api_core.gapic_v1.method\n',
    '\g<0>import google.api_core.path_template\n'
)
