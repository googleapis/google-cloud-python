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
from .metastore import (
    AlterMetadataResourceLocationRequest,
    AlterMetadataResourceLocationResponse,
    AuxiliaryVersionConfig,
    Backup,
    CreateBackupRequest,
    CreateMetadataImportRequest,
    CreateServiceRequest,
    DatabaseDumpSpec,
    DataCatalogConfig,
    DataplexConfig,
    DeleteBackupRequest,
    DeleteServiceRequest,
    EncryptionConfig,
    ErrorDetails,
    ExportMetadataRequest,
    GetBackupRequest,
    GetMetadataImportRequest,
    GetServiceRequest,
    HiveMetastoreConfig,
    KerberosConfig,
    Lake,
    ListBackupsRequest,
    ListBackupsResponse,
    ListMetadataImportsRequest,
    ListMetadataImportsResponse,
    ListServicesRequest,
    ListServicesResponse,
    LocationMetadata,
    MaintenanceWindow,
    MetadataExport,
    MetadataImport,
    MetadataIntegration,
    MetadataManagementActivity,
    MoveTableToDatabaseRequest,
    MoveTableToDatabaseResponse,
    NetworkConfig,
    OperationMetadata,
    QueryMetadataRequest,
    QueryMetadataResponse,
    RemoveIamPolicyRequest,
    RemoveIamPolicyResponse,
    Restore,
    RestoreServiceRequest,
    ScalingConfig,
    Secret,
    Service,
    TelemetryConfig,
    UpdateMetadataImportRequest,
    UpdateServiceRequest,
)
from .metastore_federation import (
    BackendMetastore,
    CreateFederationRequest,
    DeleteFederationRequest,
    Federation,
    GetFederationRequest,
    ListFederationsRequest,
    ListFederationsResponse,
    UpdateFederationRequest,
)

__all__ = (
    "AlterMetadataResourceLocationRequest",
    "AlterMetadataResourceLocationResponse",
    "AuxiliaryVersionConfig",
    "Backup",
    "CreateBackupRequest",
    "CreateMetadataImportRequest",
    "CreateServiceRequest",
    "DatabaseDumpSpec",
    "DataCatalogConfig",
    "DataplexConfig",
    "DeleteBackupRequest",
    "DeleteServiceRequest",
    "EncryptionConfig",
    "ErrorDetails",
    "ExportMetadataRequest",
    "GetBackupRequest",
    "GetMetadataImportRequest",
    "GetServiceRequest",
    "HiveMetastoreConfig",
    "KerberosConfig",
    "Lake",
    "ListBackupsRequest",
    "ListBackupsResponse",
    "ListMetadataImportsRequest",
    "ListMetadataImportsResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "LocationMetadata",
    "MaintenanceWindow",
    "MetadataExport",
    "MetadataImport",
    "MetadataIntegration",
    "MetadataManagementActivity",
    "MoveTableToDatabaseRequest",
    "MoveTableToDatabaseResponse",
    "NetworkConfig",
    "OperationMetadata",
    "QueryMetadataRequest",
    "QueryMetadataResponse",
    "RemoveIamPolicyRequest",
    "RemoveIamPolicyResponse",
    "Restore",
    "RestoreServiceRequest",
    "ScalingConfig",
    "Secret",
    "Service",
    "TelemetryConfig",
    "UpdateMetadataImportRequest",
    "UpdateServiceRequest",
    "BackendMetastore",
    "CreateFederationRequest",
    "DeleteFederationRequest",
    "Federation",
    "GetFederationRequest",
    "ListFederationsRequest",
    "ListFederationsResponse",
    "UpdateFederationRequest",
)
