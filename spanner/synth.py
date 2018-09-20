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
