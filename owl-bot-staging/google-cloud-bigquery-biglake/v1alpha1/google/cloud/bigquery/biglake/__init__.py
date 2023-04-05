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
from google.cloud.bigquery.biglake import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.bigquery.biglake_v1alpha1.services.metastore_service.client import MetastoreServiceClient
from google.cloud.bigquery.biglake_v1alpha1.services.metastore_service.async_client import MetastoreServiceAsyncClient

from google.cloud.bigquery.biglake_v1alpha1.types.metastore import Catalog
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import CheckLockRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import CreateCatalogRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import CreateDatabaseRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import CreateLockRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import CreateTableRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import Database
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import DeleteCatalogRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import DeleteDatabaseRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import DeleteLockRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import DeleteTableRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import GetCatalogRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import GetDatabaseRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import GetTableRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import HiveDatabaseOptions
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import HiveTableOptions
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import ListCatalogsRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import ListCatalogsResponse
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import ListDatabasesRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import ListDatabasesResponse
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import ListLocksRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import ListLocksResponse
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import ListTablesRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import ListTablesResponse
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import Lock
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import RenameTableRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import Table
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import UpdateDatabaseRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import UpdateTableRequest
from google.cloud.bigquery.biglake_v1alpha1.types.metastore import TableView

__all__ = ('MetastoreServiceClient',
    'MetastoreServiceAsyncClient',
    'Catalog',
    'CheckLockRequest',
    'CreateCatalogRequest',
    'CreateDatabaseRequest',
    'CreateLockRequest',
    'CreateTableRequest',
    'Database',
    'DeleteCatalogRequest',
    'DeleteDatabaseRequest',
    'DeleteLockRequest',
    'DeleteTableRequest',
    'GetCatalogRequest',
    'GetDatabaseRequest',
    'GetTableRequest',
    'HiveDatabaseOptions',
    'HiveTableOptions',
    'ListCatalogsRequest',
    'ListCatalogsResponse',
    'ListDatabasesRequest',
    'ListDatabasesResponse',
    'ListLocksRequest',
    'ListLocksResponse',
    'ListTablesRequest',
    'ListTablesResponse',
    'Lock',
    'RenameTableRequest',
    'Table',
    'UpdateDatabaseRequest',
    'UpdateTableRequest',
    'TableView',
)
