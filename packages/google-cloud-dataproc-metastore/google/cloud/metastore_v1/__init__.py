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
from google.cloud.metastore import gapic_version as package_version

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
    Backup,
    CreateBackupRequest,
    CreateMetadataImportRequest,
    CreateServiceRequest,
    DatabaseDumpSpec,
    DeleteBackupRequest,
    DeleteServiceRequest,
    EncryptionConfig,
    ExportMetadataRequest,
    GetBackupRequest,
    GetMetadataImportRequest,
    GetServiceRequest,
    HiveMetastoreConfig,
    KerberosConfig,
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
    MetadataManagementActivity,
    NetworkConfig,
    OperationMetadata,
    Restore,
    RestoreServiceRequest,
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
    "BackendMetastore",
    "Backup",
    "CreateBackupRequest",
    "CreateFederationRequest",
    "CreateMetadataImportRequest",
    "CreateServiceRequest",
    "DatabaseDumpSpec",
    "DataprocMetastoreClient",
    "DataprocMetastoreFederationClient",
    "DeleteBackupRequest",
    "DeleteFederationRequest",
    "DeleteServiceRequest",
    "EncryptionConfig",
    "ExportMetadataRequest",
    "Federation",
    "GetBackupRequest",
    "GetFederationRequest",
    "GetMetadataImportRequest",
    "GetServiceRequest",
    "HiveMetastoreConfig",
    "KerberosConfig",
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
    "MetadataManagementActivity",
    "NetworkConfig",
    "OperationMetadata",
    "Restore",
    "RestoreServiceRequest",
    "Secret",
    "Service",
    "TelemetryConfig",
    "UpdateFederationRequest",
    "UpdateMetadataImportRequest",
    "UpdateServiceRequest",
)
