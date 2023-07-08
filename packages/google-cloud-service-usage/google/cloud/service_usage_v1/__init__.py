# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.service_usage_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.service_usage import ServiceUsageAsyncClient, ServiceUsageClient
from .types.resources import OperationMetadata, Service, ServiceConfig, State
from .types.serviceusage import (
    BatchEnableServicesRequest,
    BatchEnableServicesResponse,
    BatchGetServicesRequest,
    BatchGetServicesResponse,
    DisableServiceRequest,
    DisableServiceResponse,
    EnableServiceRequest,
    EnableServiceResponse,
    GetServiceRequest,
    ListServicesRequest,
    ListServicesResponse,
)

__all__ = (
    "ServiceUsageAsyncClient",
    "BatchEnableServicesRequest",
    "BatchEnableServicesResponse",
    "BatchGetServicesRequest",
    "BatchGetServicesResponse",
    "DisableServiceRequest",
    "DisableServiceResponse",
    "EnableServiceRequest",
    "EnableServiceResponse",
    "GetServiceRequest",
    "ListServicesRequest",
    "ListServicesResponse",
    "OperationMetadata",
    "Service",
    "ServiceConfig",
    "ServiceUsageClient",
    "State",
)
