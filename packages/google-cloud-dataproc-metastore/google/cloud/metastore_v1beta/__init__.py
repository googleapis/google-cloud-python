# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.metastore_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.dataproc_metastore import (
    DataprocMetastoreAsyncClient,
    DataprocMetastoreClient,
)
from .services.dataproc_metastore_federation import (
    DataprocMetastoreFederationAsyncClient,
    DataprocMetastoreFederationClient,
)
from .types.metastore import (
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
from .types.metastore_federation import (
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
    "DataprocMetastoreAsyncClient",
    "DataprocMetastoreFederationAsyncClient",
    "AlterMetadataResourceLocationRequest",
    "AlterMetadataResourceLocationResponse",
    "AuxiliaryVersionConfig",
    "BackendMetastore",
    "Backup",
    "CreateBackupRequest",
    "CreateFederationRequest",
    "CreateMetadataImportRequest",
    "CreateServiceRequest",
    "DataCatalogConfig",
    "DatabaseDumpSpec",
    "DataplexConfig",
    "DataprocMetastoreClient",
    "DataprocMetastoreFederationClient",
    "DeleteBackupRequest",
    "DeleteFederationRequest",
    "DeleteServiceRequest",
    "EncryptionConfig",
    "ErrorDetails",
    "ExportMetadataRequest",
    "Federation",
    "GetBackupRequest",
    "GetFederationRequest",
    "GetMetadataImportRequest",
    "GetServiceRequest",
    "HiveMetastoreConfig",
    "KerberosConfig",
    "Lake",
    "ListBackupsRequest",
    "ListBackupsResponse",
    "ListFederationsRequest",
    "ListFederationsResponse",
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
    "UpdateFederationRequest",
    "UpdateMetadataImportRequest",
    "UpdateServiceRequest",
)
