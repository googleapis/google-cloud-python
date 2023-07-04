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
from google.cloud.metastore_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.dataproc_metastore import DataprocMetastoreClient
from .services.dataproc_metastore import DataprocMetastoreAsyncClient
from .services.dataproc_metastore_federation import DataprocMetastoreFederationClient
from .services.dataproc_metastore_federation import DataprocMetastoreFederationAsyncClient

from .types.metastore import AuxiliaryVersionConfig
from .types.metastore import Backup
from .types.metastore import CreateBackupRequest
from .types.metastore import CreateMetadataImportRequest
from .types.metastore import CreateServiceRequest
from .types.metastore import DatabaseDumpSpec
from .types.metastore import DeleteBackupRequest
from .types.metastore import DeleteServiceRequest
from .types.metastore import EncryptionConfig
from .types.metastore import ExportMetadataRequest
from .types.metastore import GetBackupRequest
from .types.metastore import GetMetadataImportRequest
from .types.metastore import GetServiceRequest
from .types.metastore import HiveMetastoreConfig
from .types.metastore import KerberosConfig
from .types.metastore import ListBackupsRequest
from .types.metastore import ListBackupsResponse
from .types.metastore import ListMetadataImportsRequest
from .types.metastore import ListMetadataImportsResponse
from .types.metastore import ListServicesRequest
from .types.metastore import ListServicesResponse
from .types.metastore import LocationMetadata
from .types.metastore import MaintenanceWindow
from .types.metastore import MetadataExport
from .types.metastore import MetadataImport
from .types.metastore import MetadataManagementActivity
from .types.metastore import NetworkConfig
from .types.metastore import OperationMetadata
from .types.metastore import Restore
from .types.metastore import RestoreServiceRequest
from .types.metastore import ScalingConfig
from .types.metastore import Secret
from .types.metastore import Service
from .types.metastore import TelemetryConfig
from .types.metastore import UpdateMetadataImportRequest
from .types.metastore import UpdateServiceRequest
from .types.metastore_federation import BackendMetastore
from .types.metastore_federation import CreateFederationRequest
from .types.metastore_federation import DeleteFederationRequest
from .types.metastore_federation import Federation
from .types.metastore_federation import GetFederationRequest
from .types.metastore_federation import ListFederationsRequest
from .types.metastore_federation import ListFederationsResponse
from .types.metastore_federation import UpdateFederationRequest

__all__ = (
    'DataprocMetastoreAsyncClient',
    'DataprocMetastoreFederationAsyncClient',
'AuxiliaryVersionConfig',
'BackendMetastore',
'Backup',
'CreateBackupRequest',
'CreateFederationRequest',
'CreateMetadataImportRequest',
'CreateServiceRequest',
'DatabaseDumpSpec',
'DataprocMetastoreClient',
'DataprocMetastoreFederationClient',
'DeleteBackupRequest',
'DeleteFederationRequest',
'DeleteServiceRequest',
'EncryptionConfig',
'ExportMetadataRequest',
'Federation',
'GetBackupRequest',
'GetFederationRequest',
'GetMetadataImportRequest',
'GetServiceRequest',
'HiveMetastoreConfig',
'KerberosConfig',
'ListBackupsRequest',
'ListBackupsResponse',
'ListFederationsRequest',
'ListFederationsResponse',
'ListMetadataImportsRequest',
'ListMetadataImportsResponse',
'ListServicesRequest',
'ListServicesResponse',
'LocationMetadata',
'MaintenanceWindow',
'MetadataExport',
'MetadataImport',
'MetadataManagementActivity',
'NetworkConfig',
'OperationMetadata',
'Restore',
'RestoreServiceRequest',
'ScalingConfig',
'Secret',
'Service',
'TelemetryConfig',
'UpdateFederationRequest',
'UpdateMetadataImportRequest',
'UpdateServiceRequest',
)
