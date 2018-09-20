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


#----------------------------------------------------------------------------
# Generate spanner client
#----------------------------------------------------------------------------
library = gapic.py_library(
    'spanner',
    'v1',
    config_path='/google/spanner/artman_spanner.yaml',
    artman_output_name='spanner-v1')

s.move(library / 'google/cloud/spanner_v1/proto')
s.move(library / 'google/cloud/spanner_v1/gapic')

# Add grpcio-gcp options
s.replace(
    "google/cloud/spanner_v1/gapic/transports/spanner_grpc_transport.py",
    '# limitations under the License.\n'
    '\n'
    'import google.api_core.grpc_helpers\n',
    '# limitations under the License.\n'
    '\n'
    'import pkg_resources\n'
    'import grpc_gcp\n'
    '\n'
    'import google.api_core.grpc_helpers\n',
)
s.replace(
    "google/cloud/spanner_v1/gapic/transports/spanner_grpc_transport.py",
    'from google.cloud.spanner_v1.proto import spanner_pb2_grpc\n',
    "\g<0>\n\n_SPANNER_GRPC_CONFIG = 'spanner.grpc.config'\n",
)

s.replace(
    "google/cloud/spanner_v1/gapic/transports/spanner_grpc_transport.py",
    '(\s+)return google.api_core.grpc_helpers.create_channel\(\n',
    '\g<1>grpc_gcp_config = grpc_gcp.api_config_from_text_pb('
    '\g<1>    pkg_resources.resource_string(__name__, _SPANNER_GRPC_CONFIG))'
    '\g<1>options = [(grpc_gcp.API_CONFIG_CHANNEL_ARG, grpc_gcp_config)]'
    '\g<0>',
)

#----------------------------------------------------------------------------
# Generate instance admin client
#----------------------------------------------------------------------------
library = gapic.py_library(
    'spanner_admin_instance',
    'v1',
    config_path='/google/spanner/admin/instance'
                '/artman_spanner_admin_instance.yaml',
    artman_output_name='spanner-admin-instance-v1')

s.move(library / 'google/cloud/spanner_admin_instance_v1/gapic')
s.move(library / 'google/cloud/spanner_admin_instance_v1/proto')
s.move(library / 'tests')

# Fix up the _GAPIC_LIBRARY_VERSION targets
s.replace(
    'google/cloud/spanner_admin_instance_v1/gapic/instance_admin_client.py',
    "'google-cloud-spanner-admin-instance'",
    "'google-cloud-spanner'",
)

# Fix up generated imports
s.replace(
    "google/**/*.py",
    'from google\.cloud\.spanner\.admin\.instance_v1.proto',
    'from google.cloud.spanner_admin_instance_v1.proto',
)

# Fix docstrings
s.replace(
    'google/cloud/spanner_admin_instance_v1/gapic/instance_admin_client.py',
    r"""
        \* The instance is readable via the API, with all requested attributes
        but no allocated resources. Its state is `CREATING`.""",
    r"""
        * The instance is readable via the API, with all requested attributes
          but no allocated resources. Its state is `CREATING`.""",
)
s.replace(
    'google/cloud/spanner_admin_instance_v1/gapic/instance_admin_client.py',
    r"""
        \* Cancelling the operation renders the instance immediately unreadable
        via the API.""",
    r"""
        * Cancelling the operation renders the instance immediately unreadable
          via the API.""",
)
s.replace(
    'google/cloud/spanner_admin_instance_v1/gapic/instance_admin_client.py',
    r"""
        \* Billing for all successfully-allocated resources begins \(some types
        may have lower than the requested levels\).""",
    r"""
        * Billing for all successfully-allocated resources begins (some types
          may have lower than the requested levels).""",
)
s.replace(
    'google/cloud/spanner_admin_instance_v1/gapic/instance_admin_client.py',
    r"""
        \* The instance and \*all of its databases\* immediately and
        irrevocably disappear from the API. All data in the databases
        is permanently deleted.""",
    r"""
        * The instance and *all of its databases* immediately and
          irrevocably disappear from the API. All data in the databases
          is permanently deleted.""",
)
s.replace(
    'google/cloud/spanner_admin_instance_v1/gapic/instance_admin_client.py',
    r"""
                  \* ``labels.env:dev`` --> The instance has the label \\"env\\" and the value of
                ::

                                       the label contains the string \\"dev\\".""",
    r"""
                  * ``labels.env:dev`` --> The instance has the label \\"env\\"
                    and the value of the label contains the string \\"dev\\".""",
)
s.replace(
    'google/cloud/spanner_admin_instance_v1/gapic/instance_admin_client.py',
    r"""
                  \* ``name:howl labels.env:dev`` --> The instance's name contains \\"howl\\" and
                ::

                                                 it has the label \\"env\\" with its value
                                                 containing \\"dev\\".""",
    r"""
                  * ``name:howl labels.env:dev`` --> The instance's name
                    contains \\"howl\\" and it has the label \\"env\\" with
                    its value containing \\"dev\\".""",
)
s.replace(
    'google/cloud/spanner_admin_instance_v1/gapic/instance_admin_client.py',
    r"""
        \* For resource types for which a decrease in the instance's allocation
        has been requested, billing is based on the newly-requested level.""",
    r"""
        * For resource types for which a decrease in the instance's allocation
          has been requested, billing is based on the newly-requested level.""",
)
s.replace(
    'google/cloud/spanner_admin_instance_v1/gapic/instance_admin_client.py',
    r"""
        \* Cancelling the operation sets its metadata's
        \[cancel_time\]\[google.spanner.admin.instance.v1.UpdateInstanceMetadata.cancel_time\], and begins
        restoring resources to their pre-request values. The operation
        is guaranteed to succeed at undoing all resource changes,
        after which point it terminates with a `CANCELLED` status.""",
    r"""
        * Cancelling the operation sets its metadata's
          [cancel_time][google.spanner.admin.instance.v1.UpdateInstanceMetadata.cancel_time],
          and begins restoring resources to their pre-request values.
          The operation is guaranteed to succeed at undoing all resource
          changes, after which point it terminates with a `CANCELLED` status.""",
)
s.replace(
    'google/cloud/spanner_admin_instance_v1/gapic/instance_admin_client.py',
    r"""
        \* Reading the instance via the API continues to give the pre-request
        resource levels.""",
    r"""
        * Reading the instance via the API continues to give the pre-request
          resource levels.""",
)
s.replace(
    'google/cloud/spanner_admin_instance_v1/gapic/instance_admin_client.py',
    r"""
        \* Billing begins for all successfully-allocated resources \(some types
        may have lower than the requested levels\).
        \* All newly-reserved resources are available for serving the instance's
        tables.""",
    r"""
        * Billing begins for all successfully-allocated resources (some types
          may have lower than the requested levels).
        * All newly-reserved resources are available for serving the instance's
          tables.""",
)
s.replace(
    'google/cloud/spanner_v1/proto/transaction_pb2.py',
    r"""====*""",
    r"",
)
s.replace(
    'google/cloud/spanner_v1/proto/transaction_pb2.py',
    r"""----*""",
    r"",
)
s.replace(
    'google/cloud/spanner_v1/proto/transaction_pb2.py',
    r"""~~~~*""",
    r"",
)

#----------------------------------------------------------------------------
# Generate database admin client
#----------------------------------------------------------------------------
library = gapic.py_library(
    'spanner_admin_database',
    'v1',
    config_path='/google/spanner/admin/database'
                '/artman_spanner_admin_database.yaml',
    artman_output_name='spanner-admin-database-v1')

s.move(library / 'google/cloud/spanner_admin_database_v1/gapic')
s.move(library / 'google/cloud/spanner_admin_database_v1/proto')
s.move(library / 'tests')

# Fix up the _GAPIC_LIBRARY_VERSION targets
s.replace(
    'google/cloud/spanner_admin_database_v1/gapic/database_admin_client.py',
    "'google-cloud-spanner-admin-database'",
    "'google-cloud-spanner'",
)

# Fix up the _GAPIC_LIBRARY_VERSION targets
s.replace(
    "google/**/*.py",
    'from google\.cloud\.spanner\.admin\.database_v1.proto',
    'from google.cloud.spanner_admin_database_v1.proto',
)

# Fix docstrings
s.replace(
    'google/cloud/spanner_admin_database_v1/gapic/database_admin_client.py',
    r'database ID must be enclosed in backticks \(`` `` ``\).',
    r'database ID must be enclosed in backticks.',
)
