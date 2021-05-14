# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from google.cloud.apigateway_v1.services.api_gateway_service.client import (
    ApiGatewayServiceClient,
)
from google.cloud.apigateway_v1.services.api_gateway_service.async_client import (
    ApiGatewayServiceAsyncClient,
)

from google.cloud.apigateway_v1.types.apigateway import Api
from google.cloud.apigateway_v1.types.apigateway import ApiConfig
from google.cloud.apigateway_v1.types.apigateway import CreateApiConfigRequest
from google.cloud.apigateway_v1.types.apigateway import CreateApiRequest
from google.cloud.apigateway_v1.types.apigateway import CreateGatewayRequest
from google.cloud.apigateway_v1.types.apigateway import DeleteApiConfigRequest
from google.cloud.apigateway_v1.types.apigateway import DeleteApiRequest
from google.cloud.apigateway_v1.types.apigateway import DeleteGatewayRequest
from google.cloud.apigateway_v1.types.apigateway import Gateway
from google.cloud.apigateway_v1.types.apigateway import GetApiConfigRequest
from google.cloud.apigateway_v1.types.apigateway import GetApiRequest
from google.cloud.apigateway_v1.types.apigateway import GetGatewayRequest
from google.cloud.apigateway_v1.types.apigateway import ListApiConfigsRequest
from google.cloud.apigateway_v1.types.apigateway import ListApiConfigsResponse
from google.cloud.apigateway_v1.types.apigateway import ListApisRequest
from google.cloud.apigateway_v1.types.apigateway import ListApisResponse
from google.cloud.apigateway_v1.types.apigateway import ListGatewaysRequest
from google.cloud.apigateway_v1.types.apigateway import ListGatewaysResponse
from google.cloud.apigateway_v1.types.apigateway import OperationMetadata
from google.cloud.apigateway_v1.types.apigateway import UpdateApiConfigRequest
from google.cloud.apigateway_v1.types.apigateway import UpdateApiRequest
from google.cloud.apigateway_v1.types.apigateway import UpdateGatewayRequest

__all__ = (
    "ApiGatewayServiceClient",
    "ApiGatewayServiceAsyncClient",
    "Api",
    "ApiConfig",
    "CreateApiConfigRequest",
    "CreateApiRequest",
    "CreateGatewayRequest",
    "DeleteApiConfigRequest",
    "DeleteApiRequest",
    "DeleteGatewayRequest",
    "Gateway",
    "GetApiConfigRequest",
    "GetApiRequest",
    "GetGatewayRequest",
    "ListApiConfigsRequest",
    "ListApiConfigsResponse",
    "ListApisRequest",
    "ListApisResponse",
    "ListGatewaysRequest",
    "ListGatewaysResponse",
    "OperationMetadata",
    "UpdateApiConfigRequest",
    "UpdateApiRequest",
    "UpdateGatewayRequest",
)
