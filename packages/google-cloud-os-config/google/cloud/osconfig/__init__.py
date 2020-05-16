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
from google.cloud.osconfig_v1.types.patch_jobs import WindowsUpdateSettings
from google.cloud.osconfig_v1.types.patch_jobs import YumSettings
from google.cloud.osconfig_v1.types.patch_jobs import ZypperSettings

__all__ = (
    "AptSettings",
    "CancelPatchJobRequest",
    "CreatePatchDeploymentRequest",
    "DeletePatchDeploymentRequest",
    "ExecStep",
    "ExecStepConfig",
    "ExecutePatchJobRequest",
    "GcsObject",
    "GetPatchDeploymentRequest",
    "GetPatchJobRequest",
    "GooSettings",
    "Instance",
    "ListPatchDeploymentsRequest",
    "ListPatchDeploymentsResponse",
    "ListPatchJobInstanceDetailsRequest",
    "ListPatchJobInstanceDetailsResponse",
    "ListPatchJobsRequest",
    "ListPatchJobsResponse",
    "MonthlySchedule",
    "OneTimeSchedule",
    "OsConfigServiceClient",
    "PatchConfig",
    "PatchDeployment",
    "PatchInstanceFilter",
    "PatchJob",
    "PatchJobInstanceDetails",
    "RecurringSchedule",
    "WeekDayOfMonth",
    "WeeklySchedule",
    "WindowsUpdateSettings",
    "YumSettings",
    "ZypperSettings",
)
