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
from google.cloud.backupdr_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.backup_dr import BackupDRClient
from .services.backup_dr import BackupDRAsyncClient

from .types.backupdr import CreateManagementServerRequest
from .types.backupdr import DeleteManagementServerRequest
from .types.backupdr import GetManagementServerRequest
from .types.backupdr import InitializeServiceRequest
from .types.backupdr import InitializeServiceResponse
from .types.backupdr import ListManagementServersRequest
from .types.backupdr import ListManagementServersResponse
from .types.backupdr import ManagementServer
from .types.backupdr import ManagementURI
from .types.backupdr import NetworkConfig
from .types.backupdr import OperationMetadata
from .types.backupdr import WorkforceIdentityBasedManagementURI
from .types.backupdr import WorkforceIdentityBasedOAuth2ClientID
from .types.backupplan import BackupPlan
from .types.backupplan import BackupPlanRevision
from .types.backupplan import BackupRule
from .types.backupplan import BackupWindow
from .types.backupplan import CreateBackupPlanRequest
from .types.backupplan import DeleteBackupPlanRequest
from .types.backupplan import GetBackupPlanRequest
from .types.backupplan import GetBackupPlanRevisionRequest
from .types.backupplan import ListBackupPlanRevisionsRequest
from .types.backupplan import ListBackupPlanRevisionsResponse
from .types.backupplan import ListBackupPlansRequest
from .types.backupplan import ListBackupPlansResponse
from .types.backupplan import StandardSchedule
from .types.backupplan import UpdateBackupPlanRequest
from .types.backupplan import WeekDayOfMonth
from .types.backupplanassociation import BackupPlanAssociation
from .types.backupplanassociation import CreateBackupPlanAssociationRequest
from .types.backupplanassociation import DeleteBackupPlanAssociationRequest
from .types.backupplanassociation import FetchBackupPlanAssociationsForResourceTypeRequest
from .types.backupplanassociation import FetchBackupPlanAssociationsForResourceTypeResponse
from .types.backupplanassociation import GetBackupPlanAssociationRequest
from .types.backupplanassociation import ListBackupPlanAssociationsRequest
from .types.backupplanassociation import ListBackupPlanAssociationsResponse
from .types.backupplanassociation import RuleConfigInfo
from .types.backupplanassociation import TriggerBackupRequest
from .types.backupplanassociation import UpdateBackupPlanAssociationRequest
from .types.backupvault import Backup
from .types.backupvault import BackupApplianceBackupConfig
from .types.backupvault import BackupApplianceLockInfo
from .types.backupvault import BackupConfigInfo
from .types.backupvault import BackupLock
from .types.backupvault import BackupVault
from .types.backupvault import CreateBackupVaultRequest
from .types.backupvault import DataSource
from .types.backupvault import DataSourceBackupApplianceApplication
from .types.backupvault import DataSourceGcpResource
from .types.backupvault import DeleteBackupRequest
from .types.backupvault import DeleteBackupVaultRequest
from .types.backupvault import FetchUsableBackupVaultsRequest
from .types.backupvault import FetchUsableBackupVaultsResponse
from .types.backupvault import GcpBackupConfig
from .types.backupvault import GcpResource
from .types.backupvault import GetBackupRequest
from .types.backupvault import GetBackupVaultRequest
from .types.backupvault import GetDataSourceRequest
from .types.backupvault import ListBackupsRequest
from .types.backupvault import ListBackupsResponse
from .types.backupvault import ListBackupVaultsRequest
from .types.backupvault import ListBackupVaultsResponse
from .types.backupvault import ListDataSourcesRequest
from .types.backupvault import ListDataSourcesResponse
from .types.backupvault import RestoreBackupRequest
from .types.backupvault import RestoreBackupResponse
from .types.backupvault import ServiceLockInfo
from .types.backupvault import TargetResource
from .types.backupvault import UpdateBackupRequest
from .types.backupvault import UpdateBackupVaultRequest
from .types.backupvault import UpdateDataSourceRequest
from .types.backupvault import BackupConfigState
from .types.backupvault import BackupVaultView
from .types.backupvault import BackupView
from .types.backupvault_ba import BackupApplianceBackupProperties
from .types.backupvault_cloudsql import CloudSqlInstanceBackupPlanAssociationProperties
from .types.backupvault_cloudsql import CloudSqlInstanceBackupProperties
from .types.backupvault_cloudsql import CloudSqlInstanceDataSourceProperties
from .types.backupvault_cloudsql import CloudSqlInstanceDataSourceReferenceProperties
from .types.backupvault_cloudsql import CloudSqlInstanceInitializationConfig
from .types.backupvault_disk import DiskBackupProperties
from .types.backupvault_disk import DiskDataSourceProperties
from .types.backupvault_disk import DiskRestoreProperties
from .types.backupvault_disk import DiskTargetEnvironment
from .types.backupvault_disk import RegionDiskTargetEnvironment
from .types.backupvault_gce import AcceleratorConfig
from .types.backupvault_gce import AccessConfig
from .types.backupvault_gce import AdvancedMachineFeatures
from .types.backupvault_gce import AliasIpRange
from .types.backupvault_gce import AllocationAffinity
from .types.backupvault_gce import AttachedDisk
from .types.backupvault_gce import ComputeInstanceBackupProperties
from .types.backupvault_gce import ComputeInstanceDataSourceProperties
from .types.backupvault_gce import ComputeInstanceRestoreProperties
from .types.backupvault_gce import ComputeInstanceTargetEnvironment
from .types.backupvault_gce import ConfidentialInstanceConfig
from .types.backupvault_gce import CustomerEncryptionKey
from .types.backupvault_gce import DisplayDevice
from .types.backupvault_gce import Entry
from .types.backupvault_gce import GuestOsFeature
from .types.backupvault_gce import InstanceParams
from .types.backupvault_gce import Metadata
from .types.backupvault_gce import NetworkInterface
from .types.backupvault_gce import NetworkPerformanceConfig
from .types.backupvault_gce import Scheduling
from .types.backupvault_gce import SchedulingDuration
from .types.backupvault_gce import ServiceAccount
from .types.backupvault_gce import Tags
from .types.backupvault_gce import KeyRevocationActionType
from .types.datasourcereference import DataSourceBackupConfigInfo
from .types.datasourcereference import DataSourceGcpResourceInfo
from .types.datasourcereference import DataSourceReference
from .types.datasourcereference import FetchDataSourceReferencesForResourceTypeRequest
from .types.datasourcereference import FetchDataSourceReferencesForResourceTypeResponse
from .types.datasourcereference import GetDataSourceReferenceRequest

__all__ = (
    'BackupDRAsyncClient',
'AcceleratorConfig',
'AccessConfig',
'AdvancedMachineFeatures',
'AliasIpRange',
'AllocationAffinity',
'AttachedDisk',
'Backup',
'BackupApplianceBackupConfig',
'BackupApplianceBackupProperties',
'BackupApplianceLockInfo',
'BackupConfigInfo',
'BackupConfigState',
'BackupDRClient',
'BackupLock',
'BackupPlan',
'BackupPlanAssociation',
'BackupPlanRevision',
'BackupRule',
'BackupVault',
'BackupVaultView',
'BackupView',
'BackupWindow',
'CloudSqlInstanceBackupPlanAssociationProperties',
'CloudSqlInstanceBackupProperties',
'CloudSqlInstanceDataSourceProperties',
'CloudSqlInstanceDataSourceReferenceProperties',
'CloudSqlInstanceInitializationConfig',
'ComputeInstanceBackupProperties',
'ComputeInstanceDataSourceProperties',
'ComputeInstanceRestoreProperties',
'ComputeInstanceTargetEnvironment',
'ConfidentialInstanceConfig',
'CreateBackupPlanAssociationRequest',
'CreateBackupPlanRequest',
'CreateBackupVaultRequest',
'CreateManagementServerRequest',
'CustomerEncryptionKey',
'DataSource',
'DataSourceBackupApplianceApplication',
'DataSourceBackupConfigInfo',
'DataSourceGcpResource',
'DataSourceGcpResourceInfo',
'DataSourceReference',
'DeleteBackupPlanAssociationRequest',
'DeleteBackupPlanRequest',
'DeleteBackupRequest',
'DeleteBackupVaultRequest',
'DeleteManagementServerRequest',
'DiskBackupProperties',
'DiskDataSourceProperties',
'DiskRestoreProperties',
'DiskTargetEnvironment',
'DisplayDevice',
'Entry',
'FetchBackupPlanAssociationsForResourceTypeRequest',
'FetchBackupPlanAssociationsForResourceTypeResponse',
'FetchDataSourceReferencesForResourceTypeRequest',
'FetchDataSourceReferencesForResourceTypeResponse',
'FetchUsableBackupVaultsRequest',
'FetchUsableBackupVaultsResponse',
'GcpBackupConfig',
'GcpResource',
'GetBackupPlanAssociationRequest',
'GetBackupPlanRequest',
'GetBackupPlanRevisionRequest',
'GetBackupRequest',
'GetBackupVaultRequest',
'GetDataSourceReferenceRequest',
'GetDataSourceRequest',
'GetManagementServerRequest',
'GuestOsFeature',
'InitializeServiceRequest',
'InitializeServiceResponse',
'InstanceParams',
'KeyRevocationActionType',
'ListBackupPlanAssociationsRequest',
'ListBackupPlanAssociationsResponse',
'ListBackupPlanRevisionsRequest',
'ListBackupPlanRevisionsResponse',
'ListBackupPlansRequest',
'ListBackupPlansResponse',
'ListBackupVaultsRequest',
'ListBackupVaultsResponse',
'ListBackupsRequest',
'ListBackupsResponse',
'ListDataSourcesRequest',
'ListDataSourcesResponse',
'ListManagementServersRequest',
'ListManagementServersResponse',
'ManagementServer',
'ManagementURI',
'Metadata',
'NetworkConfig',
'NetworkInterface',
'NetworkPerformanceConfig',
'OperationMetadata',
'RegionDiskTargetEnvironment',
'RestoreBackupRequest',
'RestoreBackupResponse',
'RuleConfigInfo',
'Scheduling',
'SchedulingDuration',
'ServiceAccount',
'ServiceLockInfo',
'StandardSchedule',
'Tags',
'TargetResource',
'TriggerBackupRequest',
'UpdateBackupPlanAssociationRequest',
'UpdateBackupPlanRequest',
'UpdateBackupRequest',
'UpdateBackupVaultRequest',
'UpdateDataSourceRequest',
'WeekDayOfMonth',
'WorkforceIdentityBasedManagementURI',
'WorkforceIdentityBasedOAuth2ClientID',
)
