# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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


from google.cloud.metastore_v1alpha.services.dataproc_metastore.client import DataprocMetastoreClient
from google.cloud.metastore_v1alpha.services.dataproc_metastore.async_client import DataprocMetastoreAsyncClient
from google.cloud.metastore_v1alpha.services.dataproc_metastore_federation.client import DataprocMetastoreFederationClient
from google.cloud.metastore_v1alpha.services.dataproc_metastore_federation.async_client import DataprocMetastoreFederationAsyncClient

from google.cloud.metastore_v1alpha.types.metastore import AlterMetadataResourceLocationRequest
from google.cloud.metastore_v1alpha.types.metastore import AlterMetadataResourceLocationResponse
from google.cloud.metastore_v1alpha.types.metastore import AuxiliaryVersionConfig
from google.cloud.metastore_v1alpha.types.metastore import Backup
from google.cloud.metastore_v1alpha.types.metastore import CreateBackupRequest
from google.cloud.metastore_v1alpha.types.metastore import CreateMetadataImportRequest
from google.cloud.metastore_v1alpha.types.metastore import CreateServiceRequest
from google.cloud.metastore_v1alpha.types.metastore import DatabaseDumpSpec
from google.cloud.metastore_v1alpha.types.metastore import DataCatalogConfig
from google.cloud.metastore_v1alpha.types.metastore import DataplexConfig
from google.cloud.metastore_v1alpha.types.metastore import DeleteBackupRequest
from google.cloud.metastore_v1alpha.types.metastore import DeleteServiceRequest
from google.cloud.metastore_v1alpha.types.metastore import EncryptionConfig
from google.cloud.metastore_v1alpha.types.metastore import ErrorDetails
from google.cloud.metastore_v1alpha.types.metastore import ExportMetadataRequest
from google.cloud.metastore_v1alpha.types.metastore import GetBackupRequest
from google.cloud.metastore_v1alpha.types.metastore import GetMetadataImportRequest
from google.cloud.metastore_v1alpha.types.metastore import GetServiceRequest
from google.cloud.metastore_v1alpha.types.metastore import HiveMetastoreConfig
from google.cloud.metastore_v1alpha.types.metastore import KerberosConfig
from google.cloud.metastore_v1alpha.types.metastore import Lake
from google.cloud.metastore_v1alpha.types.metastore import ListBackupsRequest
from google.cloud.metastore_v1alpha.types.metastore import ListBackupsResponse
from google.cloud.metastore_v1alpha.types.metastore import ListMetadataImportsRequest
from google.cloud.metastore_v1alpha.types.metastore import ListMetadataImportsResponse
from google.cloud.metastore_v1alpha.types.metastore import ListServicesRequest
from google.cloud.metastore_v1alpha.types.metastore import ListServicesResponse
from google.cloud.metastore_v1alpha.types.metastore import LocationMetadata
from google.cloud.metastore_v1alpha.types.metastore import MaintenanceWindow
from google.cloud.metastore_v1alpha.types.metastore import MetadataExport
from google.cloud.metastore_v1alpha.types.metastore import MetadataImport
from google.cloud.metastore_v1alpha.types.metastore import MetadataIntegration
from google.cloud.metastore_v1alpha.types.metastore import MetadataManagementActivity
from google.cloud.metastore_v1alpha.types.metastore import MoveTableToDatabaseRequest
from google.cloud.metastore_v1alpha.types.metastore import MoveTableToDatabaseResponse
from google.cloud.metastore_v1alpha.types.metastore import NetworkConfig
from google.cloud.metastore_v1alpha.types.metastore import OperationMetadata
from google.cloud.metastore_v1alpha.types.metastore import QueryMetadataRequest
from google.cloud.metastore_v1alpha.types.metastore import QueryMetadataResponse
from google.cloud.metastore_v1alpha.types.metastore import RemoveIamPolicyRequest
from google.cloud.metastore_v1alpha.types.metastore import RemoveIamPolicyResponse
from google.cloud.metastore_v1alpha.types.metastore import Restore
from google.cloud.metastore_v1alpha.types.metastore import RestoreServiceRequest
from google.cloud.metastore_v1alpha.types.metastore import ScalingConfig
from google.cloud.metastore_v1alpha.types.metastore import Secret
from google.cloud.metastore_v1alpha.types.metastore import Service
from google.cloud.metastore_v1alpha.types.metastore import TelemetryConfig
from google.cloud.metastore_v1alpha.types.metastore import UpdateMetadataImportRequest
from google.cloud.metastore_v1alpha.types.metastore import UpdateServiceRequest
from google.cloud.metastore_v1alpha.types.metastore_federation import BackendMetastore
from google.cloud.metastore_v1alpha.types.metastore_federation import CreateFederationRequest
from google.cloud.metastore_v1alpha.types.metastore_federation import DeleteFederationRequest
from google.cloud.metastore_v1alpha.types.metastore_federation import Federation
from google.cloud.metastore_v1alpha.types.metastore_federation import GetFederationRequest
from google.cloud.metastore_v1alpha.types.metastore_federation import ListFederationsRequest
from google.cloud.metastore_v1alpha.types.metastore_federation import ListFederationsResponse
from google.cloud.metastore_v1alpha.types.metastore_federation import UpdateFederationRequest

__all__ = ('DataprocMetastoreClient',
    'DataprocMetastoreAsyncClient',
    'DataprocMetastoreFederationClient',
    'DataprocMetastoreFederationAsyncClient',
    'AlterMetadataResourceLocationRequest',
    'AlterMetadataResourceLocationResponse',
    'AuxiliaryVersionConfig',
    'Backup',
    'CreateBackupRequest',
    'CreateMetadataImportRequest',
    'CreateServiceRequest',
    'DatabaseDumpSpec',
    'DataCatalogConfig',
    'DataplexConfig',
    'DeleteBackupRequest',
    'DeleteServiceRequest',
    'EncryptionConfig',
    'ErrorDetails',
    'ExportMetadataRequest',
    'GetBackupRequest',
    'GetMetadataImportRequest',
    'GetServiceRequest',
    'HiveMetastoreConfig',
    'KerberosConfig',
    'Lake',
    'ListBackupsRequest',
    'ListBackupsResponse',
    'ListMetadataImportsRequest',
    'ListMetadataImportsResponse',
    'ListServicesRequest',
    'ListServicesResponse',
    'LocationMetadata',
    'MaintenanceWindow',
    'MetadataExport',
    'MetadataImport',
    'MetadataIntegration',
    'MetadataManagementActivity',
    'MoveTableToDatabaseRequest',
    'MoveTableToDatabaseResponse',
    'NetworkConfig',
    'OperationMetadata',
    'QueryMetadataRequest',
    'QueryMetadataResponse',
    'RemoveIamPolicyRequest',
    'RemoveIamPolicyResponse',
    'Restore',
    'RestoreServiceRequest',
    'ScalingConfig',
    'Secret',
    'Service',
    'TelemetryConfig',
    'UpdateMetadataImportRequest',
    'UpdateServiceRequest',
    'BackendMetastore',
    'CreateFederationRequest',
    'DeleteFederationRequest',
    'Federation',
    'GetFederationRequest',
    'ListFederationsRequest',
    'ListFederationsResponse',
    'UpdateFederationRequest',
)
