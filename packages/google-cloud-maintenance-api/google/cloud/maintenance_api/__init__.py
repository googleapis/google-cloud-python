# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.maintenance_api import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.maintenance_api_v1beta.services.maintenance.async_client import (
    MaintenanceAsyncClient,
)
from google.cloud.maintenance_api_v1beta.services.maintenance.client import (
    MaintenanceClient,
)
from google.cloud.maintenance_api_v1beta.types.maintenance_service import (
    GetResourceMaintenanceRequest,
    ListResourceMaintenancesRequest,
    ListResourceMaintenancesResponse,
    MaintenanceCategory,
    MaintenanceControl,
    MaintenanceSummary,
    ResourceMaintenance,
    SummarizeMaintenancesRequest,
    SummarizeMaintenancesResponse,
)

__all__ = (
    "MaintenanceClient",
    "MaintenanceAsyncClient",
    "GetResourceMaintenanceRequest",
    "ListResourceMaintenancesRequest",
    "ListResourceMaintenancesResponse",
    "MaintenanceControl",
    "MaintenanceSummary",
    "ResourceMaintenance",
    "SummarizeMaintenancesRequest",
    "SummarizeMaintenancesResponse",
    "MaintenanceCategory",
)
