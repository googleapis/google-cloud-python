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
from .inventory import (
    GetInventoryRequest,
    Inventory,
    ListInventoriesRequest,
    ListInventoriesResponse,
    InventoryView,
)
from .osconfig_common import FixedOrPercent
from .patch_deployments import (
    CreatePatchDeploymentRequest,
    DeletePatchDeploymentRequest,
    GetPatchDeploymentRequest,
    ListPatchDeploymentsRequest,
    ListPatchDeploymentsResponse,
    MonthlySchedule,
    OneTimeSchedule,
    PatchDeployment,
    RecurringSchedule,
    WeekDayOfMonth,
    WeeklySchedule,
)
from .patch_jobs import (
    AptSettings,
    CancelPatchJobRequest,
    ExecStep,
    ExecStepConfig,
    ExecutePatchJobRequest,
    GcsObject,
    GetPatchJobRequest,
    GooSettings,
    Instance,
    ListPatchJobInstanceDetailsRequest,
    ListPatchJobInstanceDetailsResponse,
    ListPatchJobsRequest,
    ListPatchJobsResponse,
    PatchConfig,
    PatchInstanceFilter,
    PatchJob,
    PatchJobInstanceDetails,
    PatchRollout,
    WindowsUpdateSettings,
    YumSettings,
    ZypperSettings,
)
from .vulnerability import (
    CVSSv3,
    GetVulnerabilityReportRequest,
    ListVulnerabilityReportsRequest,
    ListVulnerabilityReportsResponse,
    VulnerabilityReport,
)

__all__ = (
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
