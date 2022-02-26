# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.cloud.vmmigration_v1.services.vm_migration.client import VmMigrationClient
from google.cloud.vmmigration_v1.services.vm_migration.async_client import (
    VmMigrationAsyncClient,
)

from google.cloud.vmmigration_v1.types.vmmigration import AddGroupMigrationRequest
from google.cloud.vmmigration_v1.types.vmmigration import AddGroupMigrationResponse
from google.cloud.vmmigration_v1.types.vmmigration import AppliedLicense
from google.cloud.vmmigration_v1.types.vmmigration import CancelCloneJobRequest
from google.cloud.vmmigration_v1.types.vmmigration import CancelCloneJobResponse
from google.cloud.vmmigration_v1.types.vmmigration import CancelCutoverJobRequest
from google.cloud.vmmigration_v1.types.vmmigration import CancelCutoverJobResponse
from google.cloud.vmmigration_v1.types.vmmigration import CloneJob
from google.cloud.vmmigration_v1.types.vmmigration import ComputeEngineTargetDefaults
from google.cloud.vmmigration_v1.types.vmmigration import ComputeEngineTargetDetails
from google.cloud.vmmigration_v1.types.vmmigration import ComputeScheduling
from google.cloud.vmmigration_v1.types.vmmigration import CreateCloneJobRequest
from google.cloud.vmmigration_v1.types.vmmigration import CreateCutoverJobRequest
from google.cloud.vmmigration_v1.types.vmmigration import (
    CreateDatacenterConnectorRequest,
)
from google.cloud.vmmigration_v1.types.vmmigration import CreateGroupRequest
from google.cloud.vmmigration_v1.types.vmmigration import CreateMigratingVmRequest
from google.cloud.vmmigration_v1.types.vmmigration import CreateSourceRequest
from google.cloud.vmmigration_v1.types.vmmigration import CreateTargetProjectRequest
from google.cloud.vmmigration_v1.types.vmmigration import CreateUtilizationReportRequest
from google.cloud.vmmigration_v1.types.vmmigration import CutoverJob
from google.cloud.vmmigration_v1.types.vmmigration import DatacenterConnector
from google.cloud.vmmigration_v1.types.vmmigration import (
    DeleteDatacenterConnectorRequest,
)
from google.cloud.vmmigration_v1.types.vmmigration import DeleteGroupRequest
from google.cloud.vmmigration_v1.types.vmmigration import DeleteMigratingVmRequest
from google.cloud.vmmigration_v1.types.vmmigration import DeleteSourceRequest
from google.cloud.vmmigration_v1.types.vmmigration import DeleteTargetProjectRequest
from google.cloud.vmmigration_v1.types.vmmigration import DeleteUtilizationReportRequest
from google.cloud.vmmigration_v1.types.vmmigration import FetchInventoryRequest
from google.cloud.vmmigration_v1.types.vmmigration import FetchInventoryResponse
from google.cloud.vmmigration_v1.types.vmmigration import FinalizeMigrationRequest
from google.cloud.vmmigration_v1.types.vmmigration import FinalizeMigrationResponse
from google.cloud.vmmigration_v1.types.vmmigration import GetCloneJobRequest
from google.cloud.vmmigration_v1.types.vmmigration import GetCutoverJobRequest
from google.cloud.vmmigration_v1.types.vmmigration import GetDatacenterConnectorRequest
from google.cloud.vmmigration_v1.types.vmmigration import GetGroupRequest
from google.cloud.vmmigration_v1.types.vmmigration import GetMigratingVmRequest
from google.cloud.vmmigration_v1.types.vmmigration import GetSourceRequest
from google.cloud.vmmigration_v1.types.vmmigration import GetTargetProjectRequest
from google.cloud.vmmigration_v1.types.vmmigration import GetUtilizationReportRequest
from google.cloud.vmmigration_v1.types.vmmigration import Group
from google.cloud.vmmigration_v1.types.vmmigration import ListCloneJobsRequest
from google.cloud.vmmigration_v1.types.vmmigration import ListCloneJobsResponse
from google.cloud.vmmigration_v1.types.vmmigration import ListCutoverJobsRequest
from google.cloud.vmmigration_v1.types.vmmigration import ListCutoverJobsResponse
from google.cloud.vmmigration_v1.types.vmmigration import (
    ListDatacenterConnectorsRequest,
)
from google.cloud.vmmigration_v1.types.vmmigration import (
    ListDatacenterConnectorsResponse,
)
from google.cloud.vmmigration_v1.types.vmmigration import ListGroupsRequest
from google.cloud.vmmigration_v1.types.vmmigration import ListGroupsResponse
from google.cloud.vmmigration_v1.types.vmmigration import ListMigratingVmsRequest
from google.cloud.vmmigration_v1.types.vmmigration import ListMigratingVmsResponse
from google.cloud.vmmigration_v1.types.vmmigration import ListSourcesRequest
from google.cloud.vmmigration_v1.types.vmmigration import ListSourcesResponse
from google.cloud.vmmigration_v1.types.vmmigration import ListTargetProjectsRequest
from google.cloud.vmmigration_v1.types.vmmigration import ListTargetProjectsResponse
from google.cloud.vmmigration_v1.types.vmmigration import ListUtilizationReportsRequest
from google.cloud.vmmigration_v1.types.vmmigration import ListUtilizationReportsResponse
from google.cloud.vmmigration_v1.types.vmmigration import MigratingVm
from google.cloud.vmmigration_v1.types.vmmigration import MigrationError
from google.cloud.vmmigration_v1.types.vmmigration import NetworkInterface
from google.cloud.vmmigration_v1.types.vmmigration import OperationMetadata
from google.cloud.vmmigration_v1.types.vmmigration import PauseMigrationRequest
from google.cloud.vmmigration_v1.types.vmmigration import PauseMigrationResponse
from google.cloud.vmmigration_v1.types.vmmigration import RemoveGroupMigrationRequest
from google.cloud.vmmigration_v1.types.vmmigration import RemoveGroupMigrationResponse
from google.cloud.vmmigration_v1.types.vmmigration import ReplicationCycle
from google.cloud.vmmigration_v1.types.vmmigration import ReplicationSync
from google.cloud.vmmigration_v1.types.vmmigration import ResumeMigrationRequest
from google.cloud.vmmigration_v1.types.vmmigration import ResumeMigrationResponse
from google.cloud.vmmigration_v1.types.vmmigration import SchedulePolicy
from google.cloud.vmmigration_v1.types.vmmigration import SchedulingNodeAffinity
from google.cloud.vmmigration_v1.types.vmmigration import Source
from google.cloud.vmmigration_v1.types.vmmigration import StartMigrationRequest
from google.cloud.vmmigration_v1.types.vmmigration import StartMigrationResponse
from google.cloud.vmmigration_v1.types.vmmigration import TargetProject
from google.cloud.vmmigration_v1.types.vmmigration import UpdateGroupRequest
from google.cloud.vmmigration_v1.types.vmmigration import UpdateMigratingVmRequest
from google.cloud.vmmigration_v1.types.vmmigration import UpdateSourceRequest
from google.cloud.vmmigration_v1.types.vmmigration import UpdateTargetProjectRequest
from google.cloud.vmmigration_v1.types.vmmigration import UtilizationReport
from google.cloud.vmmigration_v1.types.vmmigration import VmUtilizationInfo
from google.cloud.vmmigration_v1.types.vmmigration import VmUtilizationMetrics
from google.cloud.vmmigration_v1.types.vmmigration import VmwareSourceDetails
from google.cloud.vmmigration_v1.types.vmmigration import VmwareVmDetails
from google.cloud.vmmigration_v1.types.vmmigration import VmwareVmsDetails
from google.cloud.vmmigration_v1.types.vmmigration import ComputeEngineBootOption
from google.cloud.vmmigration_v1.types.vmmigration import ComputeEngineDiskType
from google.cloud.vmmigration_v1.types.vmmigration import ComputeEngineLicenseType
from google.cloud.vmmigration_v1.types.vmmigration import UtilizationReportView

__all__ = (
    "VmMigrationClient",
    "VmMigrationAsyncClient",
    "AddGroupMigrationRequest",
    "AddGroupMigrationResponse",
    "AppliedLicense",
    "CancelCloneJobRequest",
    "CancelCloneJobResponse",
    "CancelCutoverJobRequest",
    "CancelCutoverJobResponse",
    "CloneJob",
    "ComputeEngineTargetDefaults",
    "ComputeEngineTargetDetails",
    "ComputeScheduling",
    "CreateCloneJobRequest",
    "CreateCutoverJobRequest",
    "CreateDatacenterConnectorRequest",
    "CreateGroupRequest",
    "CreateMigratingVmRequest",
    "CreateSourceRequest",
    "CreateTargetProjectRequest",
    "CreateUtilizationReportRequest",
    "CutoverJob",
    "DatacenterConnector",
    "DeleteDatacenterConnectorRequest",
    "DeleteGroupRequest",
    "DeleteMigratingVmRequest",
    "DeleteSourceRequest",
    "DeleteTargetProjectRequest",
    "DeleteUtilizationReportRequest",
    "FetchInventoryRequest",
    "FetchInventoryResponse",
    "FinalizeMigrationRequest",
    "FinalizeMigrationResponse",
    "GetCloneJobRequest",
    "GetCutoverJobRequest",
    "GetDatacenterConnectorRequest",
    "GetGroupRequest",
    "GetMigratingVmRequest",
    "GetSourceRequest",
    "GetTargetProjectRequest",
    "GetUtilizationReportRequest",
    "Group",
    "ListCloneJobsRequest",
    "ListCloneJobsResponse",
    "ListCutoverJobsRequest",
    "ListCutoverJobsResponse",
    "ListDatacenterConnectorsRequest",
    "ListDatacenterConnectorsResponse",
    "ListGroupsRequest",
    "ListGroupsResponse",
    "ListMigratingVmsRequest",
    "ListMigratingVmsResponse",
    "ListSourcesRequest",
    "ListSourcesResponse",
    "ListTargetProjectsRequest",
    "ListTargetProjectsResponse",
    "ListUtilizationReportsRequest",
    "ListUtilizationReportsResponse",
    "MigratingVm",
    "MigrationError",
    "NetworkInterface",
    "OperationMetadata",
    "PauseMigrationRequest",
    "PauseMigrationResponse",
    "RemoveGroupMigrationRequest",
    "RemoveGroupMigrationResponse",
    "ReplicationCycle",
    "ReplicationSync",
    "ResumeMigrationRequest",
    "ResumeMigrationResponse",
    "SchedulePolicy",
    "SchedulingNodeAffinity",
    "Source",
    "StartMigrationRequest",
    "StartMigrationResponse",
    "TargetProject",
    "UpdateGroupRequest",
    "UpdateMigratingVmRequest",
    "UpdateSourceRequest",
    "UpdateTargetProjectRequest",
    "UtilizationReport",
    "VmUtilizationInfo",
    "VmUtilizationMetrics",
    "VmwareSourceDetails",
    "VmwareVmDetails",
    "VmwareVmsDetails",
    "ComputeEngineBootOption",
    "ComputeEngineDiskType",
    "ComputeEngineLicenseType",
    "UtilizationReportView",
)
