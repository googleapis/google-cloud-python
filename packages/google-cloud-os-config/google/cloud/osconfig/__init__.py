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

from google.cloud.osconfig_v1.services.os_config_service.client import (
    OsConfigServiceClient,
)
from google.cloud.osconfig_v1.services.os_config_service.async_client import (
    OsConfigServiceAsyncClient,
)
from google.cloud.osconfig_v1.services.os_config_zonal_service.client import (
    OsConfigZonalServiceClient,
)
from google.cloud.osconfig_v1.services.os_config_zonal_service.async_client import (
    OsConfigZonalServiceAsyncClient,
)

from google.cloud.osconfig_v1.types.inventory import GetInventoryRequest
from google.cloud.osconfig_v1.types.inventory import Inventory
from google.cloud.osconfig_v1.types.inventory import ListInventoriesRequest
from google.cloud.osconfig_v1.types.inventory import ListInventoriesResponse
from google.cloud.osconfig_v1.types.inventory import InventoryView
from google.cloud.osconfig_v1.types.osconfig_common import FixedOrPercent
from google.cloud.osconfig_v1.types.patch_deployments import (
    CreatePatchDeploymentRequest,
)
from google.cloud.osconfig_v1.types.patch_deployments import (
    DeletePatchDeploymentRequest,
)
from google.cloud.osconfig_v1.types.patch_deployments import GetPatchDeploymentRequest
from google.cloud.osconfig_v1.types.patch_deployments import ListPatchDeploymentsRequest
from google.cloud.osconfig_v1.types.patch_deployments import (
    ListPatchDeploymentsResponse,
)
from google.cloud.osconfig_v1.types.patch_deployments import MonthlySchedule
from google.cloud.osconfig_v1.types.patch_deployments import OneTimeSchedule
from google.cloud.osconfig_v1.types.patch_deployments import PatchDeployment
from google.cloud.osconfig_v1.types.patch_deployments import RecurringSchedule
from google.cloud.osconfig_v1.types.patch_deployments import WeekDayOfMonth
from google.cloud.osconfig_v1.types.patch_deployments import WeeklySchedule
from google.cloud.osconfig_v1.types.patch_jobs import AptSettings
from google.cloud.osconfig_v1.types.patch_jobs import CancelPatchJobRequest
from google.cloud.osconfig_v1.types.patch_jobs import ExecStep
from google.cloud.osconfig_v1.types.patch_jobs import ExecStepConfig
from google.cloud.osconfig_v1.types.patch_jobs import ExecutePatchJobRequest
from google.cloud.osconfig_v1.types.patch_jobs import GcsObject
from google.cloud.osconfig_v1.types.patch_jobs import GetPatchJobRequest
from google.cloud.osconfig_v1.types.patch_jobs import GooSettings
from google.cloud.osconfig_v1.types.patch_jobs import Instance
from google.cloud.osconfig_v1.types.patch_jobs import ListPatchJobInstanceDetailsRequest
from google.cloud.osconfig_v1.types.patch_jobs import (
    ListPatchJobInstanceDetailsResponse,
)
from google.cloud.osconfig_v1.types.patch_jobs import ListPatchJobsRequest
from google.cloud.osconfig_v1.types.patch_jobs import ListPatchJobsResponse
from google.cloud.osconfig_v1.types.patch_jobs import PatchConfig
from google.cloud.osconfig_v1.types.patch_jobs import PatchInstanceFilter
from google.cloud.osconfig_v1.types.patch_jobs import PatchJob
from google.cloud.osconfig_v1.types.patch_jobs import PatchJobInstanceDetails
from google.cloud.osconfig_v1.types.patch_jobs import PatchRollout
from google.cloud.osconfig_v1.types.patch_jobs import WindowsUpdateSettings
from google.cloud.osconfig_v1.types.patch_jobs import YumSettings
from google.cloud.osconfig_v1.types.patch_jobs import ZypperSettings
from google.cloud.osconfig_v1.types.vulnerability import CVSSv3
from google.cloud.osconfig_v1.types.vulnerability import GetVulnerabilityReportRequest
from google.cloud.osconfig_v1.types.vulnerability import ListVulnerabilityReportsRequest
from google.cloud.osconfig_v1.types.vulnerability import (
    ListVulnerabilityReportsResponse,
)
from google.cloud.osconfig_v1.types.vulnerability import VulnerabilityReport

__all__ = (
    "OsConfigServiceClient",
    "OsConfigServiceAsyncClient",
    "OsConfigZonalServiceClient",
    "OsConfigZonalServiceAsyncClient",
    "GetInventoryRequest",
    "Inventory",
    "ListInventoriesRequest",
    "ListInventoriesResponse",
    "InventoryView",
    "FixedOrPercent",
    "CreatePatchDeploymentRequest",
    "DeletePatchDeploymentRequest",
    "GetPatchDeploymentRequest",
    "ListPatchDeploymentsRequest",
    "ListPatchDeploymentsResponse",
    "MonthlySchedule",
    "OneTimeSchedule",
    "PatchDeployment",
    "RecurringSchedule",
    "WeekDayOfMonth",
    "WeeklySchedule",
    "AptSettings",
    "CancelPatchJobRequest",
    "ExecStep",
    "ExecStepConfig",
    "ExecutePatchJobRequest",
    "GcsObject",
    "GetPatchJobRequest",
    "GooSettings",
    "Instance",
    "ListPatchJobInstanceDetailsRequest",
    "ListPatchJobInstanceDetailsResponse",
    "ListPatchJobsRequest",
    "ListPatchJobsResponse",
    "PatchConfig",
    "PatchInstanceFilter",
    "PatchJob",
    "PatchJobInstanceDetails",
    "PatchRollout",
    "WindowsUpdateSettings",
    "YumSettings",
    "ZypperSettings",
    "CVSSv3",
    "GetVulnerabilityReportRequest",
    "ListVulnerabilityReportsRequest",
    "ListVulnerabilityReportsResponse",
    "VulnerabilityReport",
)
