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

from .services.api_gateway_service import ApiGatewayServiceClient
from .services.api_gateway_service import ApiGatewayServiceAsyncClient

from .types.apigateway import Api
from .types.apigateway import ApiConfig
from .types.apigateway import CreateApiConfigRequest
from .types.apigateway import CreateApiRequest
from .types.apigateway import CreateGatewayRequest
from .types.apigateway import DeleteApiConfigRequest
from .types.apigateway import DeleteApiRequest
from .types.apigateway import DeleteGatewayRequest
from .types.apigateway import Gateway
from .types.apigateway import GetApiConfigRequest
from .types.apigateway import GetApiRequest
from .types.apigateway import GetGatewayRequest
from .types.apigateway import ListApiConfigsRequest
from .types.apigateway import ListApiConfigsResponse
from .types.apigateway import ListApisRequest
from .types.apigateway import ListApisResponse
from .types.apigateway import ListGatewaysRequest
from .types.apigateway import ListGatewaysResponse
from .types.apigateway import OperationMetadata
from .types.apigateway import UpdateApiConfigRequest
from .types.apigateway import UpdateApiRequest
from .types.apigateway import UpdateGatewayRequest

__all__ = (
    "ApiGatewayServiceAsyncClient",
    "Api",
    "ApiConfig",
    "ApiGatewayServiceClient",
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
