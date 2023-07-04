# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.cloud.beyondcorp_appconnections import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.beyondcorp_appconnections_v1.services.app_connections_service.client import AppConnectionsServiceClient
from google.cloud.beyondcorp_appconnections_v1.services.app_connections_service.async_client import AppConnectionsServiceAsyncClient

from google.cloud.beyondcorp_appconnections_v1.types.app_connections_service import AppConnection
from google.cloud.beyondcorp_appconnections_v1.types.app_connections_service import AppConnectionOperationMetadata
from google.cloud.beyondcorp_appconnections_v1.types.app_connections_service import CreateAppConnectionRequest
from google.cloud.beyondcorp_appconnections_v1.types.app_connections_service import DeleteAppConnectionRequest
from google.cloud.beyondcorp_appconnections_v1.types.app_connections_service import GetAppConnectionRequest
from google.cloud.beyondcorp_appconnections_v1.types.app_connections_service import ListAppConnectionsRequest
from google.cloud.beyondcorp_appconnections_v1.types.app_connections_service import ListAppConnectionsResponse
from google.cloud.beyondcorp_appconnections_v1.types.app_connections_service import ResolveAppConnectionsRequest
from google.cloud.beyondcorp_appconnections_v1.types.app_connections_service import ResolveAppConnectionsResponse
from google.cloud.beyondcorp_appconnections_v1.types.app_connections_service import UpdateAppConnectionRequest

__all__ = ('AppConnectionsServiceClient',
    'AppConnectionsServiceAsyncClient',
    'AppConnection',
    'AppConnectionOperationMetadata',
    'CreateAppConnectionRequest',
    'DeleteAppConnectionRequest',
    'GetAppConnectionRequest',
    'ListAppConnectionsRequest',
    'ListAppConnectionsResponse',
    'ResolveAppConnectionsRequest',
    'ResolveAppConnectionsResponse',
    'UpdateAppConnectionRequest',
)
