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
from google.cloud.backupdr import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.backupdr_v1.services.backup_dr.client import BackupDRClient
from google.cloud.backupdr_v1.services.backup_dr.async_client import BackupDRAsyncClient

from google.cloud.backupdr_v1.types.backupdr import CreateManagementServerRequest
from google.cloud.backupdr_v1.types.backupdr import DeleteManagementServerRequest
from google.cloud.backupdr_v1.types.backupdr import GetManagementServerRequest
from google.cloud.backupdr_v1.types.backupdr import InitializeServiceRequest
from google.cloud.backupdr_v1.types.backupdr import InitializeServiceResponse
from google.cloud.backupdr_v1.types.backupdr import ListManagementServersRequest
from google.cloud.backupdr_v1.types.backupdr import ListManagementServersResponse
from google.cloud.backupdr_v1.types.backupdr import ManagementServer
from google.cloud.backupdr_v1.types.backupdr import ManagementURI
from google.cloud.backupdr_v1.types.backupdr import NetworkConfig
from google.cloud.backupdr_v1.types.backupdr import OperationMetadata
from google.cloud.backupdr_v1.types.backupdr import WorkforceIdentityBasedManagementURI
from google.cloud.backupdr_v1.types.backupdr import WorkforceIdentityBasedOAuth2ClientID
from google.cloud.backupdr_v1.types.backupplan import BackupPlan
from google.cloud.backupdr_v1.types.backupplan import BackupPlanRevision
from google.cloud.backupdr_v1.types.backupplan import BackupRule
from google.cloud.backupdr_v1.types.backupplan import BackupWindow
from google.cloud.backupdr_v1.types.backupplan import CreateBackupPlanRequest
from google.cloud.backupdr_v1.types.backupplan import DeleteBackupPlanRequest
from google.cloud.backupdr_v1.types.backupplan import GetBackupPlanRequest
from google.cloud.backupdr_v1.types.backupplan import GetBackupPlanRevisionRequest
from google.cloud.backupdr_v1.types.backupplan import ListBackupPlanRevisionsRequest
from google.cloud.backupdr_v1.types.backupplan import ListBackupPlanRevisionsResponse
from google.cloud.backupdr_v1.types.backupplan import ListBackupPlansRequest
from google.cloud.backupdr_v1.types.backupplan import ListBackupPlansResponse
from google.cloud.backupdr_v1.types.backupplan import StandardSchedule
from google.cloud.backupdr_v1.types.backupplan import UpdateBackupPlanRequest
from google.cloud.backupdr_v1.types.backupplan import WeekDayOfMonth
from google.cloud.backupdr_v1.types.backupplanassociation import BackupPlanAssociation
from google.cloud.backupdr_v1.types.backupplanassociation import CreateBackupPlanAssociationRequest
from google.cloud.backupdr_v1.types.backupplanassociation import DeleteBackupPlanAssociationRequest
from google.cloud.backupdr_v1.types.backupplanassociation import FetchBackupPlanAssociationsForResourceTypeRequest
from google.cloud.backupdr_v1.types.backupplanassociation import FetchBackupPlanAssociationsForResourceTypeResponse
from google.cloud.backupdr_v1.types.backupplanassociation import GetBackupPlanAssociationRequest
from google.cloud.backupdr_v1.types.backupplanassociation import ListBackupPlanAssociationsRequest
from google.cloud.backupdr_v1.types.backupplanassociation import ListBackupPlanAssociationsResponse
from google.cloud.backupdr_v1.types.backupplanassociation import RuleConfigInfo
from google.cloud.backupdr_v1.types.backupplanassociation import TriggerBackupRequest
from google.cloud.backupdr_v1.types.backupplanassociation import UpdateBackupPlanAssociationRequest
from google.cloud.backupdr_v1.types.backupvault import Backup
from google.cloud.backupdr_v1.types.backupvault import BackupApplianceBackupConfig
from google.cloud.backupdr_v1.types.backupvault import BackupApplianceLockInfo
from google.cloud.backupdr_v1.types.backupvault import BackupConfigInfo
from google.cloud.backupdr_v1.types.backupvault import BackupLock
from google.cloud.backupdr_v1.types.backupvault import BackupVault
from google.cloud.backupdr_v1.types.backupvault import CreateBackupVaultRequest
from google.cloud.backupdr_v1.types.backupvault import DataSource
from google.cloud.backupdr_v1.types.backupvault import DataSourceBackupApplianceApplication
from google.cloud.backupdr_v1.types.backupvault import DataSourceGcpResource
from google.cloud.backupdr_v1.types.backupvault import DeleteBackupRequest
from google.cloud.backupdr_v1.types.backupvault import DeleteBackupVaultRequest
from google.cloud.backupdr_v1.types.backupvault import FetchUsableBackupVaultsRequest
from google.cloud.backupdr_v1.types.backupvault import FetchUsableBackupVaultsResponse
from google.cloud.backupdr_v1.types.backupvault import GcpBackupConfig
from google.cloud.backupdr_v1.types.backupvault import GcpResource
from google.cloud.backupdr_v1.types.backupvault import GetBackupRequest
from google.cloud.backupdr_v1.types.backupvault import GetBackupVaultRequest
from google.cloud.backupdr_v1.types.backupvault import GetDataSourceRequest
from google.cloud.backupdr_v1.types.backupvault import ListBackupsRequest
from google.cloud.backupdr_v1.types.backupvault import ListBackupsResponse
from google.cloud.backupdr_v1.types.backupvault import ListBackupVaultsRequest
from google.cloud.backupdr_v1.types.backupvault import ListBackupVaultsResponse
from google.cloud.backupdr_v1.types.backupvault import ListDataSourcesRequest
from google.cloud.backupdr_v1.types.backupvault import ListDataSourcesResponse
from google.cloud.backupdr_v1.types.backupvault import RestoreBackupRequest
from google.cloud.backupdr_v1.types.backupvault import RestoreBackupResponse
from google.cloud.backupdr_v1.types.backupvault import ServiceLockInfo
from google.cloud.backupdr_v1.types.backupvault import TargetResource
from google.cloud.backupdr_v1.types.backupvault import UpdateBackupRequest
from google.cloud.backupdr_v1.types.backupvault import UpdateBackupVaultRequest
from google.cloud.backupdr_v1.types.backupvault import UpdateDataSourceRequest
from google.cloud.backupdr_v1.types.backupvault import BackupConfigState
from google.cloud.backupdr_v1.types.backupvault import BackupVaultView
from google.cloud.backupdr_v1.types.backupvault import BackupView
from google.cloud.backupdr_v1.types.backupvault_ba import BackupApplianceBackupProperties
from google.cloud.backupdr_v1.types.backupvault_cloudsql import CloudSqlInstanceBackupPlanAssociationProperties
from google.cloud.backupdr_v1.types.backupvault_cloudsql import CloudSqlInstanceBackupProperties
from google.cloud.backupdr_v1.types.backupvault_cloudsql import CloudSqlInstanceDataSourceProperties
from google.cloud.backupdr_v1.types.backupvault_cloudsql import CloudSqlInstanceDataSourceReferenceProperties
from google.cloud.backupdr_v1.types.backupvault_cloudsql import CloudSqlInstanceInitializationConfig
from google.cloud.backupdr_v1.types.backupvault_disk import DiskBackupProperties
from google.cloud.backupdr_v1.types.backupvault_disk import DiskDataSourceProperties
from google.cloud.backupdr_v1.types.backupvault_disk import DiskRestoreProperties
from google.cloud.backupdr_v1.types.backupvault_disk import DiskTargetEnvironment
from google.cloud.backupdr_v1.types.backupvault_disk import RegionDiskTargetEnvironment
from google.cloud.backupdr_v1.types.backupvault_gce import AcceleratorConfig
from google.cloud.backupdr_v1.types.backupvault_gce import AccessConfig
from google.cloud.backupdr_v1.types.backupvault_gce import AdvancedMachineFeatures
from google.cloud.backupdr_v1.types.backupvault_gce import AliasIpRange
from google.cloud.backupdr_v1.types.backupvault_gce import AllocationAffinity
from google.cloud.backupdr_v1.types.backupvault_gce import AttachedDisk
from google.cloud.backupdr_v1.types.backupvault_gce import ComputeInstanceBackupProperties
from google.cloud.backupdr_v1.types.backupvault_gce import ComputeInstanceDataSourceProperties
from google.cloud.backupdr_v1.types.backupvault_gce import ComputeInstanceRestoreProperties
from google.cloud.backupdr_v1.types.backupvault_gce import ComputeInstanceTargetEnvironment
from google.cloud.backupdr_v1.types.backupvault_gce import ConfidentialInstanceConfig
from google.cloud.backupdr_v1.types.backupvault_gce import CustomerEncryptionKey
from google.cloud.backupdr_v1.types.backupvault_gce import DisplayDevice
from google.cloud.backupdr_v1.types.backupvault_gce import Entry
from google.cloud.backupdr_v1.types.backupvault_gce import GuestOsFeature
from google.cloud.backupdr_v1.types.backupvault_gce import InstanceParams
from google.cloud.backupdr_v1.types.backupvault_gce import Metadata
from google.cloud.backupdr_v1.types.backupvault_gce import NetworkInterface
from google.cloud.backupdr_v1.types.backupvault_gce import NetworkPerformanceConfig
from google.cloud.backupdr_v1.types.backupvault_gce import Scheduling
from google.cloud.backupdr_v1.types.backupvault_gce import SchedulingDuration
from google.cloud.backupdr_v1.types.backupvault_gce import ServiceAccount
from google.cloud.backupdr_v1.types.backupvault_gce import Tags
from google.cloud.backupdr_v1.types.backupvault_gce import KeyRevocationActionType
from google.cloud.backupdr_v1.types.datasourcereference import DataSourceBackupConfigInfo
from google.cloud.backupdr_v1.types.datasourcereference import DataSourceGcpResourceInfo
from google.cloud.backupdr_v1.types.datasourcereference import DataSourceReference
from google.cloud.backupdr_v1.types.datasourcereference import FetchDataSourceReferencesForResourceTypeRequest
from google.cloud.backupdr_v1.types.datasourcereference import FetchDataSourceReferencesForResourceTypeResponse
from google.cloud.backupdr_v1.types.datasourcereference import GetDataSourceReferenceRequest

__all__ = ('BackupDRClient',
    'BackupDRAsyncClient',
    'CreateManagementServerRequest',
    'DeleteManagementServerRequest',
    'GetManagementServerRequest',
    'InitializeServiceRequest',
    'InitializeServiceResponse',
    'ListManagementServersRequest',
    'ListManagementServersResponse',
    'ManagementServer',
    'ManagementURI',
    'NetworkConfig',
    'OperationMetadata',
    'WorkforceIdentityBasedManagementURI',
    'WorkforceIdentityBasedOAuth2ClientID',
    'BackupPlan',
    'BackupPlanRevision',
    'BackupRule',
    'BackupWindow',
    'CreateBackupPlanRequest',
    'DeleteBackupPlanRequest',
    'GetBackupPlanRequest',
    'GetBackupPlanRevisionRequest',
    'ListBackupPlanRevisionsRequest',
    'ListBackupPlanRevisionsResponse',
    'ListBackupPlansRequest',
    'ListBackupPlansResponse',
    'StandardSchedule',
    'UpdateBackupPlanRequest',
    'WeekDayOfMonth',
    'BackupPlanAssociation',
    'CreateBackupPlanAssociationRequest',
    'DeleteBackupPlanAssociationRequest',
    'FetchBackupPlanAssociationsForResourceTypeRequest',
    'FetchBackupPlanAssociationsForResourceTypeResponse',
    'GetBackupPlanAssociationRequest',
    'ListBackupPlanAssociationsRequest',
    'ListBackupPlanAssociationsResponse',
    'RuleConfigInfo',
    'TriggerBackupRequest',
    'UpdateBackupPlanAssociationRequest',
    'Backup',
    'BackupApplianceBackupConfig',
    'BackupApplianceLockInfo',
    'BackupConfigInfo',
    'BackupLock',
    'BackupVault',
    'CreateBackupVaultRequest',
    'DataSource',
    'DataSourceBackupApplianceApplication',
    'DataSourceGcpResource',
    'DeleteBackupRequest',
    'DeleteBackupVaultRequest',
    'FetchUsableBackupVaultsRequest',
    'FetchUsableBackupVaultsResponse',
    'GcpBackupConfig',
    'GcpResource',
    'GetBackupRequest',
    'GetBackupVaultRequest',
    'GetDataSourceRequest',
    'ListBackupsRequest',
    'ListBackupsResponse',
    'ListBackupVaultsRequest',
    'ListBackupVaultsResponse',
    'ListDataSourcesRequest',
    'ListDataSourcesResponse',
    'RestoreBackupRequest',
    'RestoreBackupResponse',
    'ServiceLockInfo',
    'TargetResource',
    'UpdateBackupRequest',
    'UpdateBackupVaultRequest',
    'UpdateDataSourceRequest',
    'BackupConfigState',
    'BackupVaultView',
    'BackupView',
    'BackupApplianceBackupProperties',
    'CloudSqlInstanceBackupPlanAssociationProperties',
    'CloudSqlInstanceBackupProperties',
    'CloudSqlInstanceDataSourceProperties',
    'CloudSqlInstanceDataSourceReferenceProperties',
    'CloudSqlInstanceInitializationConfig',
    'DiskBackupProperties',
    'DiskDataSourceProperties',
    'DiskRestoreProperties',
    'DiskTargetEnvironment',
    'RegionDiskTargetEnvironment',
    'AcceleratorConfig',
    'AccessConfig',
    'AdvancedMachineFeatures',
    'AliasIpRange',
    'AllocationAffinity',
    'AttachedDisk',
    'ComputeInstanceBackupProperties',
    'ComputeInstanceDataSourceProperties',
    'ComputeInstanceRestoreProperties',
    'ComputeInstanceTargetEnvironment',
    'ConfidentialInstanceConfig',
    'CustomerEncryptionKey',
    'DisplayDevice',
    'Entry',
    'GuestOsFeature',
    'InstanceParams',
    'Metadata',
    'NetworkInterface',
    'NetworkPerformanceConfig',
    'Scheduling',
    'SchedulingDuration',
    'ServiceAccount',
    'Tags',
    'KeyRevocationActionType',
    'DataSourceBackupConfigInfo',
    'DataSourceGcpResourceInfo',
    'DataSourceReference',
    'FetchDataSourceReferencesForResourceTypeRequest',
    'FetchDataSourceReferencesForResourceTypeResponse',
    'GetDataSourceReferenceRequest',
)
