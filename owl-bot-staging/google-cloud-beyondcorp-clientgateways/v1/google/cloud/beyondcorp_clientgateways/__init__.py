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
from google.cloud.beyondcorp_clientgateways import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.beyondcorp_clientgateways_v1.services.client_gateways_service.client import ClientGatewaysServiceClient
from google.cloud.beyondcorp_clientgateways_v1.services.client_gateways_service.async_client import ClientGatewaysServiceAsyncClient

from google.cloud.beyondcorp_clientgateways_v1.types.client_gateways_service import ClientGateway
from google.cloud.beyondcorp_clientgateways_v1.types.client_gateways_service import ClientGatewayOperationMetadata
from google.cloud.beyondcorp_clientgateways_v1.types.client_gateways_service import CreateClientGatewayRequest
from google.cloud.beyondcorp_clientgateways_v1.types.client_gateways_service import DeleteClientGatewayRequest
from google.cloud.beyondcorp_clientgateways_v1.types.client_gateways_service import GetClientGatewayRequest
from google.cloud.beyondcorp_clientgateways_v1.types.client_gateways_service import ListClientGatewaysRequest
from google.cloud.beyondcorp_clientgateways_v1.types.client_gateways_service import ListClientGatewaysResponse

__all__ = ('ClientGatewaysServiceClient',
    'ClientGatewaysServiceAsyncClient',
    'ClientGateway',
    'ClientGatewayOperationMetadata',
    'CreateClientGatewayRequest',
    'DeleteClientGatewayRequest',
    'GetClientGatewayRequest',
    'ListClientGatewaysRequest',
    'ListClientGatewaysResponse',
)
