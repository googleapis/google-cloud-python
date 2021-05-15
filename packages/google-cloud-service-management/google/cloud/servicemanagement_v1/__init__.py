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

from .services.service_manager import ServiceManagerClient
from .services.service_manager import ServiceManagerAsyncClient

from .types.resources import ChangeReport
from .types.resources import ConfigFile
from .types.resources import ConfigRef
from .types.resources import ConfigSource
from .types.resources import Diagnostic
from .types.resources import ManagedService
from .types.resources import OperationMetadata
from .types.resources import Rollout
from .types.servicemanager import CreateServiceConfigRequest
from .types.servicemanager import CreateServiceRequest
from .types.servicemanager import CreateServiceRolloutRequest
from .types.servicemanager import DeleteServiceRequest
from .types.servicemanager import DisableServiceRequest
from .types.servicemanager import DisableServiceResponse
from .types.servicemanager import EnableServiceRequest
from .types.servicemanager import EnableServiceResponse
from .types.servicemanager import GenerateConfigReportRequest
from .types.servicemanager import GenerateConfigReportResponse
from .types.servicemanager import GetServiceConfigRequest
from .types.servicemanager import GetServiceRequest
from .types.servicemanager import GetServiceRolloutRequest
from .types.servicemanager import ListServiceConfigsRequest
from .types.servicemanager import ListServiceConfigsResponse
from .types.servicemanager import ListServiceRolloutsRequest
from .types.servicemanager import ListServiceRolloutsResponse
from .types.servicemanager import ListServicesRequest
from .types.servicemanager import ListServicesResponse
from .types.servicemanager import SubmitConfigSourceRequest
from .types.servicemanager import SubmitConfigSourceResponse
from .types.servicemanager import UndeleteServiceRequest
from .types.servicemanager import UndeleteServiceResponse

__all__ = (
    "ServiceManagerAsyncClient",
    "ChangeReport",
    "ConfigFile",
    "ConfigRef",
    "ConfigSource",
    "CreateServiceConfigRequest",
    "CreateServiceRequest",
    "CreateServiceRolloutRequest",
    "DeleteServiceRequest",
    "Diagnostic",
    "DisableServiceRequest",
    "DisableServiceResponse",
    "EnableServiceRequest",
    "EnableServiceResponse",
    "GenerateConfigReportRequest",
    "GenerateConfigReportResponse",
    "GetServiceConfigRequest",
    "GetServiceRequest",
    "GetServiceRolloutRequest",
    "ListServiceConfigsRequest",
    "ListServiceConfigsResponse",
    "ListServiceRolloutsRequest",
    "ListServiceRolloutsResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "ManagedService",
    "OperationMetadata",
    "Rollout",
    "ServiceManagerClient",
    "SubmitConfigSourceRequest",
    "SubmitConfigSourceResponse",
    "UndeleteServiceRequest",
    "UndeleteServiceResponse",
)
