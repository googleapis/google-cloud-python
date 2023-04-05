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
from google.cloud.bigquery.biglake_v1alpha1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.metastore_service import MetastoreServiceClient
from .services.metastore_service import MetastoreServiceAsyncClient

from .types.metastore import Catalog
from .types.metastore import CheckLockRequest
from .types.metastore import CreateCatalogRequest
from .types.metastore import CreateDatabaseRequest
from .types.metastore import CreateLockRequest
from .types.metastore import CreateTableRequest
from .types.metastore import Database
from .types.metastore import DeleteCatalogRequest
from .types.metastore import DeleteDatabaseRequest
from .types.metastore import DeleteLockRequest
from .types.metastore import DeleteTableRequest
from .types.metastore import GetCatalogRequest
from .types.metastore import GetDatabaseRequest
from .types.metastore import GetTableRequest
from .types.metastore import HiveDatabaseOptions
from .types.metastore import HiveTableOptions
from .types.metastore import ListCatalogsRequest
from .types.metastore import ListCatalogsResponse
from .types.metastore import ListDatabasesRequest
from .types.metastore import ListDatabasesResponse
from .types.metastore import ListLocksRequest
from .types.metastore import ListLocksResponse
from .types.metastore import ListTablesRequest
from .types.metastore import ListTablesResponse
from .types.metastore import Lock
from .types.metastore import RenameTableRequest
from .types.metastore import Table
from .types.metastore import UpdateDatabaseRequest
from .types.metastore import UpdateTableRequest
from .types.metastore import TableView

__all__ = (
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
'MetastoreServiceClient',
'RenameTableRequest',
'Table',
'TableView',
'UpdateDatabaseRequest',
'UpdateTableRequest',
)
