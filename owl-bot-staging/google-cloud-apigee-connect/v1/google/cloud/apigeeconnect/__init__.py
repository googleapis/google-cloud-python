# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
#
from google.cloud.apigeeconnect import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.apigeeconnect_v1.services.connection_service.client import ConnectionServiceClient
from google.cloud.apigeeconnect_v1.services.connection_service.async_client import ConnectionServiceAsyncClient
from google.cloud.apigeeconnect_v1.services.tether.client import TetherClient
from google.cloud.apigeeconnect_v1.services.tether.async_client import TetherAsyncClient

from google.cloud.apigeeconnect_v1.types.connection import Cluster
from google.cloud.apigeeconnect_v1.types.connection import Connection
from google.cloud.apigeeconnect_v1.types.connection import ListConnectionsRequest
from google.cloud.apigeeconnect_v1.types.connection import ListConnectionsResponse
from google.cloud.apigeeconnect_v1.types.tether import EgressRequest
from google.cloud.apigeeconnect_v1.types.tether import EgressResponse
from google.cloud.apigeeconnect_v1.types.tether import Header
from google.cloud.apigeeconnect_v1.types.tether import HttpRequest
from google.cloud.apigeeconnect_v1.types.tether import HttpResponse
from google.cloud.apigeeconnect_v1.types.tether import Payload
from google.cloud.apigeeconnect_v1.types.tether import StreamInfo
from google.cloud.apigeeconnect_v1.types.tether import Url
from google.cloud.apigeeconnect_v1.types.tether import Action
from google.cloud.apigeeconnect_v1.types.tether import Scheme
from google.cloud.apigeeconnect_v1.types.tether import TetherEndpoint

__all__ = ('ConnectionServiceClient',
    'ConnectionServiceAsyncClient',
    'TetherClient',
    'TetherAsyncClient',
    'Cluster',
    'Connection',
    'ListConnectionsRequest',
    'ListConnectionsResponse',
    'EgressRequest',
    'EgressResponse',
    'Header',
    'HttpRequest',
    'HttpResponse',
    'Payload',
    'StreamInfo',
    'Url',
    'Action',
    'Scheme',
    'TetherEndpoint',
)
