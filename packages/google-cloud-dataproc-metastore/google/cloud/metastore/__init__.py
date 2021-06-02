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

from google.cloud.metastore_v1.services.dataproc_metastore.client import (
    DataprocMetastoreClient,
)
from google.cloud.metastore_v1.services.dataproc_metastore.async_client import (
    DataprocMetastoreAsyncClient,
)

from google.cloud.metastore_v1.types.metastore import CreateMetadataImportRequest
from google.cloud.metastore_v1.types.metastore import CreateServiceRequest
from google.cloud.metastore_v1.types.metastore import DatabaseDumpSpec
from google.cloud.metastore_v1.types.metastore import DeleteServiceRequest
from google.cloud.metastore_v1.types.metastore import ExportMetadataRequest
from google.cloud.metastore_v1.types.metastore import GetMetadataImportRequest
from google.cloud.metastore_v1.types.metastore import GetServiceRequest
from google.cloud.metastore_v1.types.metastore import HiveMetastoreConfig
from google.cloud.metastore_v1.types.metastore import KerberosConfig
from google.cloud.metastore_v1.types.metastore import ListMetadataImportsRequest
from google.cloud.metastore_v1.types.metastore import ListMetadataImportsResponse
from google.cloud.metastore_v1.types.metastore import ListServicesRequest
from google.cloud.metastore_v1.types.metastore import ListServicesResponse
from google.cloud.metastore_v1.types.metastore import LocationMetadata
from google.cloud.metastore_v1.types.metastore import MaintenanceWindow
from google.cloud.metastore_v1.types.metastore import MetadataExport
from google.cloud.metastore_v1.types.metastore import MetadataImport
from google.cloud.metastore_v1.types.metastore import MetadataManagementActivity
from google.cloud.metastore_v1.types.metastore import OperationMetadata
from google.cloud.metastore_v1.types.metastore import Secret
from google.cloud.metastore_v1.types.metastore import Service
from google.cloud.metastore_v1.types.metastore import UpdateMetadataImportRequest
from google.cloud.metastore_v1.types.metastore import UpdateServiceRequest

__all__ = (
    "DataprocMetastoreClient",
    "DataprocMetastoreAsyncClient",
    "CreateMetadataImportRequest",
    "CreateServiceRequest",
    "DatabaseDumpSpec",
    "DeleteServiceRequest",
    "ExportMetadataRequest",
    "GetMetadataImportRequest",
    "GetServiceRequest",
    "HiveMetastoreConfig",
    "KerberosConfig",
    "ListMetadataImportsRequest",
    "ListMetadataImportsResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "LocationMetadata",
    "MaintenanceWindow",
    "MetadataExport",
    "MetadataImport",
    "MetadataManagementActivity",
    "OperationMetadata",
    "Secret",
    "Service",
    "UpdateMetadataImportRequest",
    "UpdateServiceRequest",
)
