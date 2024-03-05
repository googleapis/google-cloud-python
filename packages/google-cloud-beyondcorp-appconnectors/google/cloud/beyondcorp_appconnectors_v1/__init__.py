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
from google.cloud.beyondcorp_appconnectors_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.app_connectors_service import (
    AppConnectorsServiceAsyncClient,
    AppConnectorsServiceClient,
)
from .types.app_connector_instance_config import (
    AppConnectorInstanceConfig,
    ImageConfig,
    NotificationConfig,
)
from .types.app_connectors_service import (
    AppConnector,
    AppConnectorOperationMetadata,
    CreateAppConnectorRequest,
    DeleteAppConnectorRequest,
    GetAppConnectorRequest,
    ListAppConnectorsRequest,
    ListAppConnectorsResponse,
    ReportStatusRequest,
    UpdateAppConnectorRequest,
)
from .types.resource_info import HealthStatus, ResourceInfo

__all__ = (
    "AppConnectorsServiceAsyncClient",
    "AppConnector",
    "AppConnectorInstanceConfig",
    "AppConnectorOperationMetadata",
    "AppConnectorsServiceClient",
    "CreateAppConnectorRequest",
    "DeleteAppConnectorRequest",
    "GetAppConnectorRequest",
    "HealthStatus",
    "ImageConfig",
    "ListAppConnectorsRequest",
    "ListAppConnectorsResponse",
    "NotificationConfig",
    "ReportStatusRequest",
    "ResourceInfo",
    "UpdateAppConnectorRequest",
)
