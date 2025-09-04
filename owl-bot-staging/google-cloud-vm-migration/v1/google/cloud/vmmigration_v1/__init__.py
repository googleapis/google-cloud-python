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
from google.cloud.vmmigration_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.vm_migration import VmMigrationClient
from .services.vm_migration import VmMigrationAsyncClient

from .types.vmmigration import AdaptingOSStep
from .types.vmmigration import AddGroupMigrationRequest
from .types.vmmigration import AddGroupMigrationResponse
from .types.vmmigration import ApplianceVersion
from .types.vmmigration import AppliedLicense
from .types.vmmigration import AvailableUpdates
from .types.vmmigration import AwsSecurityGroup
from .types.vmmigration import AwsSourceDetails
from .types.vmmigration import AwsSourceDiskDetails
from .types.vmmigration import AwsSourceVmDetails
from .types.vmmigration import AwsVmDetails
from .types.vmmigration import AwsVmsDetails
from .types.vmmigration import AzureSourceDetails
from .types.vmmigration import AzureSourceVmDetails
from .types.vmmigration import AzureVmDetails
from .types.vmmigration import AzureVmsDetails
from .types.vmmigration import BootDiskDefaults
from .types.vmmigration import CancelCloneJobRequest
from .types.vmmigration import CancelCloneJobResponse
from .types.vmmigration import CancelCutoverJobRequest
from .types.vmmigration import CancelCutoverJobResponse
from .types.vmmigration import CancelDiskMigrationJobRequest
from .types.vmmigration import CancelDiskMigrationJobResponse
from .types.vmmigration import CancelImageImportJobRequest
from .types.vmmigration import CancelImageImportJobResponse
from .types.vmmigration import CloneJob
from .types.vmmigration import CloneStep
from .types.vmmigration import ComputeEngineDisk
from .types.vmmigration import ComputeEngineDisksTargetDefaults
from .types.vmmigration import ComputeEngineDisksTargetDetails
from .types.vmmigration import ComputeEngineTargetDefaults
from .types.vmmigration import ComputeEngineTargetDetails
from .types.vmmigration import ComputeScheduling
from .types.vmmigration import CopyingSourceDiskSnapshotStep
from .types.vmmigration import CreateCloneJobRequest
from .types.vmmigration import CreateCutoverJobRequest
from .types.vmmigration import CreateDatacenterConnectorRequest
from .types.vmmigration import CreateDiskMigrationJobRequest
from .types.vmmigration import CreateGroupRequest
from .types.vmmigration import CreateImageImportRequest
from .types.vmmigration import CreateMigratingVmRequest
from .types.vmmigration import CreateSourceRequest
from .types.vmmigration import CreateTargetProjectRequest
from .types.vmmigration import CreateUtilizationReportRequest
from .types.vmmigration import CreatingImageStep
from .types.vmmigration import CreatingSourceDiskSnapshotStep
from .types.vmmigration import CutoverForecast
from .types.vmmigration import CutoverJob
from .types.vmmigration import CutoverStep
from .types.vmmigration import CycleStep
from .types.vmmigration import DatacenterConnector
from .types.vmmigration import DataDiskImageImport
from .types.vmmigration import DeleteDatacenterConnectorRequest
from .types.vmmigration import DeleteDiskMigrationJobRequest
from .types.vmmigration import DeleteGroupRequest
from .types.vmmigration import DeleteImageImportRequest
from .types.vmmigration import DeleteMigratingVmRequest
from .types.vmmigration import DeleteSourceRequest
from .types.vmmigration import DeleteTargetProjectRequest
from .types.vmmigration import DeleteUtilizationReportRequest
from .types.vmmigration import DiskImageTargetDetails
from .types.vmmigration import DiskMigrationJob
from .types.vmmigration import DiskMigrationJobTargetDetails
from .types.vmmigration import DiskMigrationStep
from .types.vmmigration import DisksMigrationDisksTargetDefaults
from .types.vmmigration import DisksMigrationDisksTargetDetails
from .types.vmmigration import DisksMigrationVmTargetDefaults
from .types.vmmigration import DisksMigrationVmTargetDetails
from .types.vmmigration import Encryption
from .types.vmmigration import ExtendMigrationRequest
from .types.vmmigration import ExtendMigrationResponse
from .types.vmmigration import FetchInventoryRequest
from .types.vmmigration import FetchInventoryResponse
from .types.vmmigration import FetchStorageInventoryRequest
from .types.vmmigration import FetchStorageInventoryResponse
from .types.vmmigration import FinalizeMigrationRequest
from .types.vmmigration import FinalizeMigrationResponse
from .types.vmmigration import GetCloneJobRequest
from .types.vmmigration import GetCutoverJobRequest
from .types.vmmigration import GetDatacenterConnectorRequest
from .types.vmmigration import GetDiskMigrationJobRequest
from .types.vmmigration import GetGroupRequest
from .types.vmmigration import GetImageImportJobRequest
from .types.vmmigration import GetImageImportRequest
from .types.vmmigration import GetMigratingVmRequest
from .types.vmmigration import GetReplicationCycleRequest
from .types.vmmigration import GetSourceRequest
from .types.vmmigration import GetTargetProjectRequest
from .types.vmmigration import GetUtilizationReportRequest
from .types.vmmigration import Group
from .types.vmmigration import ImageImport
from .types.vmmigration import ImageImportJob
from .types.vmmigration import ImageImportOsAdaptationParameters
from .types.vmmigration import ImageImportStep
from .types.vmmigration import InitializingImageImportStep
from .types.vmmigration import InitializingReplicationStep
from .types.vmmigration import InstantiatingMigratedVMStep
from .types.vmmigration import ListCloneJobsRequest
from .types.vmmigration import ListCloneJobsResponse
from .types.vmmigration import ListCutoverJobsRequest
from .types.vmmigration import ListCutoverJobsResponse
from .types.vmmigration import ListDatacenterConnectorsRequest
from .types.vmmigration import ListDatacenterConnectorsResponse
from .types.vmmigration import ListDiskMigrationJobsRequest
from .types.vmmigration import ListDiskMigrationJobsResponse
from .types.vmmigration import ListGroupsRequest
from .types.vmmigration import ListGroupsResponse
from .types.vmmigration import ListImageImportJobsRequest
from .types.vmmigration import ListImageImportJobsResponse
from .types.vmmigration import ListImageImportsRequest
from .types.vmmigration import ListImageImportsResponse
from .types.vmmigration import ListMigratingVmsRequest
from .types.vmmigration import ListMigratingVmsResponse
from .types.vmmigration import ListReplicationCyclesRequest
from .types.vmmigration import ListReplicationCyclesResponse
from .types.vmmigration import ListSourcesRequest
from .types.vmmigration import ListSourcesResponse
from .types.vmmigration import ListTargetProjectsRequest
from .types.vmmigration import ListTargetProjectsResponse
from .types.vmmigration import ListUtilizationReportsRequest
from .types.vmmigration import ListUtilizationReportsResponse
from .types.vmmigration import LoadingImageSourceFilesStep
from .types.vmmigration import MachineImageParametersOverrides
from .types.vmmigration import MachineImageTargetDetails
from .types.vmmigration import MigratingVm
from .types.vmmigration import MigrationError
from .types.vmmigration import MigrationWarning
from .types.vmmigration import NetworkInterface
from .types.vmmigration import OperationMetadata
from .types.vmmigration import PauseMigrationRequest
from .types.vmmigration import PauseMigrationResponse
from .types.vmmigration import PersistentDisk
from .types.vmmigration import PersistentDiskDefaults
from .types.vmmigration import PostProcessingStep
from .types.vmmigration import PreparingVMDisksStep
from .types.vmmigration import ProvisioningTargetDiskStep
from .types.vmmigration import RemoveGroupMigrationRequest
from .types.vmmigration import RemoveGroupMigrationResponse
from .types.vmmigration import ReplicatingStep
from .types.vmmigration import ReplicationCycle
from .types.vmmigration import ReplicationSync
from .types.vmmigration import ResumeMigrationRequest
from .types.vmmigration import ResumeMigrationResponse
from .types.vmmigration import RunDiskMigrationJobRequest
from .types.vmmigration import RunDiskMigrationJobResponse
from .types.vmmigration import SchedulePolicy
from .types.vmmigration import SchedulingNodeAffinity
from .types.vmmigration import ServiceAccount
from .types.vmmigration import ShieldedInstanceConfig
from .types.vmmigration import ShuttingDownSourceVMStep
from .types.vmmigration import SkipOsAdaptation
from .types.vmmigration import Source
from .types.vmmigration import SourceStorageResource
from .types.vmmigration import StartMigrationRequest
from .types.vmmigration import StartMigrationResponse
from .types.vmmigration import TargetProject
from .types.vmmigration import UpdateDiskMigrationJobRequest
from .types.vmmigration import UpdateGroupRequest
from .types.vmmigration import UpdateMigratingVmRequest
from .types.vmmigration import UpdateSourceRequest
from .types.vmmigration import UpdateTargetProjectRequest
from .types.vmmigration import UpgradeApplianceRequest
from .types.vmmigration import UpgradeApplianceResponse
from .types.vmmigration import UpgradeStatus
from .types.vmmigration import UtilizationReport
from .types.vmmigration import VmAttachmentDetails
from .types.vmmigration import VmCapabilities
from .types.vmmigration import VmUtilizationInfo
from .types.vmmigration import VmUtilizationMetrics
from .types.vmmigration import VmwareSourceDetails
from .types.vmmigration import VmwareSourceVmDetails
from .types.vmmigration import VmwareVmDetails
from .types.vmmigration import VmwareVmsDetails
from .types.vmmigration import BootConversion
from .types.vmmigration import ComputeEngineBootOption
from .types.vmmigration import ComputeEngineDiskType
from .types.vmmigration import ComputeEngineLicenseType
from .types.vmmigration import ComputeEngineNetworkTier
from .types.vmmigration import MigratingVmView
from .types.vmmigration import OsCapability
from .types.vmmigration import UtilizationReportView
from .types.vmmigration import VmArchitecture

__all__ = (
    'VmMigrationAsyncClient',
'AdaptingOSStep',
'AddGroupMigrationRequest',
'AddGroupMigrationResponse',
'ApplianceVersion',
'AppliedLicense',
'AvailableUpdates',
'AwsSecurityGroup',
'AwsSourceDetails',
'AwsSourceDiskDetails',
'AwsSourceVmDetails',
'AwsVmDetails',
'AwsVmsDetails',
'AzureSourceDetails',
'AzureSourceVmDetails',
'AzureVmDetails',
'AzureVmsDetails',
'BootConversion',
'BootDiskDefaults',
'CancelCloneJobRequest',
'CancelCloneJobResponse',
'CancelCutoverJobRequest',
'CancelCutoverJobResponse',
'CancelDiskMigrationJobRequest',
'CancelDiskMigrationJobResponse',
'CancelImageImportJobRequest',
'CancelImageImportJobResponse',
'CloneJob',
'CloneStep',
'ComputeEngineBootOption',
'ComputeEngineDisk',
'ComputeEngineDiskType',
'ComputeEngineDisksTargetDefaults',
'ComputeEngineDisksTargetDetails',
'ComputeEngineLicenseType',
'ComputeEngineNetworkTier',
'ComputeEngineTargetDefaults',
'ComputeEngineTargetDetails',
'ComputeScheduling',
'CopyingSourceDiskSnapshotStep',
'CreateCloneJobRequest',
'CreateCutoverJobRequest',
'CreateDatacenterConnectorRequest',
'CreateDiskMigrationJobRequest',
'CreateGroupRequest',
'CreateImageImportRequest',
'CreateMigratingVmRequest',
'CreateSourceRequest',
'CreateTargetProjectRequest',
'CreateUtilizationReportRequest',
'CreatingImageStep',
'CreatingSourceDiskSnapshotStep',
'CutoverForecast',
'CutoverJob',
'CutoverStep',
'CycleStep',
'DataDiskImageImport',
'DatacenterConnector',
'DeleteDatacenterConnectorRequest',
'DeleteDiskMigrationJobRequest',
'DeleteGroupRequest',
'DeleteImageImportRequest',
'DeleteMigratingVmRequest',
'DeleteSourceRequest',
'DeleteTargetProjectRequest',
'DeleteUtilizationReportRequest',
'DiskImageTargetDetails',
'DiskMigrationJob',
'DiskMigrationJobTargetDetails',
'DiskMigrationStep',
'DisksMigrationDisksTargetDefaults',
'DisksMigrationDisksTargetDetails',
'DisksMigrationVmTargetDefaults',
'DisksMigrationVmTargetDetails',
'Encryption',
'ExtendMigrationRequest',
'ExtendMigrationResponse',
'FetchInventoryRequest',
'FetchInventoryResponse',
'FetchStorageInventoryRequest',
'FetchStorageInventoryResponse',
'FinalizeMigrationRequest',
'FinalizeMigrationResponse',
'GetCloneJobRequest',
'GetCutoverJobRequest',
'GetDatacenterConnectorRequest',
'GetDiskMigrationJobRequest',
'GetGroupRequest',
'GetImageImportJobRequest',
'GetImageImportRequest',
'GetMigratingVmRequest',
'GetReplicationCycleRequest',
'GetSourceRequest',
'GetTargetProjectRequest',
'GetUtilizationReportRequest',
'Group',
'ImageImport',
'ImageImportJob',
'ImageImportOsAdaptationParameters',
'ImageImportStep',
'InitializingImageImportStep',
'InitializingReplicationStep',
'InstantiatingMigratedVMStep',
'ListCloneJobsRequest',
'ListCloneJobsResponse',
'ListCutoverJobsRequest',
'ListCutoverJobsResponse',
'ListDatacenterConnectorsRequest',
'ListDatacenterConnectorsResponse',
'ListDiskMigrationJobsRequest',
'ListDiskMigrationJobsResponse',
'ListGroupsRequest',
'ListGroupsResponse',
'ListImageImportJobsRequest',
'ListImageImportJobsResponse',
'ListImageImportsRequest',
'ListImageImportsResponse',
'ListMigratingVmsRequest',
'ListMigratingVmsResponse',
'ListReplicationCyclesRequest',
'ListReplicationCyclesResponse',
'ListSourcesRequest',
'ListSourcesResponse',
'ListTargetProjectsRequest',
'ListTargetProjectsResponse',
'ListUtilizationReportsRequest',
'ListUtilizationReportsResponse',
'LoadingImageSourceFilesStep',
'MachineImageParametersOverrides',
'MachineImageTargetDetails',
'MigratingVm',
'MigratingVmView',
'MigrationError',
'MigrationWarning',
'NetworkInterface',
'OperationMetadata',
'OsCapability',
'PauseMigrationRequest',
'PauseMigrationResponse',
'PersistentDisk',
'PersistentDiskDefaults',
'PostProcessingStep',
'PreparingVMDisksStep',
'ProvisioningTargetDiskStep',
'RemoveGroupMigrationRequest',
'RemoveGroupMigrationResponse',
'ReplicatingStep',
'ReplicationCycle',
'ReplicationSync',
'ResumeMigrationRequest',
'ResumeMigrationResponse',
'RunDiskMigrationJobRequest',
'RunDiskMigrationJobResponse',
'SchedulePolicy',
'SchedulingNodeAffinity',
'ServiceAccount',
'ShieldedInstanceConfig',
'ShuttingDownSourceVMStep',
'SkipOsAdaptation',
'Source',
'SourceStorageResource',
'StartMigrationRequest',
'StartMigrationResponse',
'TargetProject',
'UpdateDiskMigrationJobRequest',
'UpdateGroupRequest',
'UpdateMigratingVmRequest',
'UpdateSourceRequest',
'UpdateTargetProjectRequest',
'UpgradeApplianceRequest',
'UpgradeApplianceResponse',
'UpgradeStatus',
'UtilizationReport',
'UtilizationReportView',
'VmArchitecture',
'VmAttachmentDetails',
'VmCapabilities',
'VmMigrationClient',
'VmUtilizationInfo',
'VmUtilizationMetrics',
'VmwareSourceDetails',
'VmwareSourceVmDetails',
'VmwareVmDetails',
'VmwareVmsDetails',
)
