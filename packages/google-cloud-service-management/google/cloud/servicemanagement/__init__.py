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

from google.cloud.servicemanagement_v1.services.service_manager.client import (
    ServiceManagerClient,
)
from google.cloud.servicemanagement_v1.services.service_manager.async_client import (
    ServiceManagerAsyncClient,
)

from google.cloud.servicemanagement_v1.types.resources import ChangeReport
from google.cloud.servicemanagement_v1.types.resources import ConfigFile
from google.cloud.servicemanagement_v1.types.resources import ConfigRef
from google.cloud.servicemanagement_v1.types.resources import ConfigSource
from google.cloud.servicemanagement_v1.types.resources import Diagnostic
from google.cloud.servicemanagement_v1.types.resources import ManagedService
from google.cloud.servicemanagement_v1.types.resources import OperationMetadata
from google.cloud.servicemanagement_v1.types.resources import Rollout
from google.cloud.servicemanagement_v1.types.servicemanager import (
    CreateServiceConfigRequest,
)
from google.cloud.servicemanagement_v1.types.servicemanager import CreateServiceRequest
from google.cloud.servicemanagement_v1.types.servicemanager import (
    CreateServiceRolloutRequest,
)
from google.cloud.servicemanagement_v1.types.servicemanager import DeleteServiceRequest
from google.cloud.servicemanagement_v1.types.servicemanager import DisableServiceRequest
from google.cloud.servicemanagement_v1.types.servicemanager import (
    DisableServiceResponse,
)
from google.cloud.servicemanagement_v1.types.servicemanager import EnableServiceRequest
from google.cloud.servicemanagement_v1.types.servicemanager import EnableServiceResponse
from google.cloud.servicemanagement_v1.types.servicemanager import (
    GenerateConfigReportRequest,
)
from google.cloud.servicemanagement_v1.types.servicemanager import (
    GenerateConfigReportResponse,
)
from google.cloud.servicemanagement_v1.types.servicemanager import (
    GetServiceConfigRequest,
)
from google.cloud.servicemanagement_v1.types.servicemanager import GetServiceRequest
from google.cloud.servicemanagement_v1.types.servicemanager import (
    GetServiceRolloutRequest,
)
from google.cloud.servicemanagement_v1.types.servicemanager import (
    ListServiceConfigsRequest,
)
from google.cloud.servicemanagement_v1.types.servicemanager import (
    ListServiceConfigsResponse,
)
from google.cloud.servicemanagement_v1.types.servicemanager import (
    ListServiceRolloutsRequest,
)
from google.cloud.servicemanagement_v1.types.servicemanager import (
    ListServiceRolloutsResponse,
)
from google.cloud.servicemanagement_v1.types.servicemanager import ListServicesRequest
from google.cloud.servicemanagement_v1.types.servicemanager import ListServicesResponse
from google.cloud.servicemanagement_v1.types.servicemanager import (
    SubmitConfigSourceRequest,
)
from google.cloud.servicemanagement_v1.types.servicemanager import (
    SubmitConfigSourceResponse,
)
from google.cloud.servicemanagement_v1.types.servicemanager import (
    UndeleteServiceRequest,
)
from google.cloud.servicemanagement_v1.types.servicemanager import (
    UndeleteServiceResponse,
)

__all__ = (
    "ServiceManagerClient",
    "ServiceManagerAsyncClient",
    "ChangeReport",
    "ConfigFile",
    "ConfigRef",
    "ConfigSource",
    "Diagnostic",
    "ManagedService",
    "OperationMetadata",
    "Rollout",
    "CreateServiceConfigRequest",
    "CreateServiceRequest",
    "CreateServiceRolloutRequest",
    "DeleteServiceRequest",
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
    "SubmitConfigSourceRequest",
    "SubmitConfigSourceResponse",
    "UndeleteServiceRequest",
    "UndeleteServiceResponse",
)
