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

from google.area120.tables_v1alpha1.services.tables_service.client import (
    TablesServiceClient,
)
from google.area120.tables_v1alpha1.services.tables_service.async_client import (
    TablesServiceAsyncClient,
)

from google.area120.tables_v1alpha1.types.tables import BatchCreateRowsRequest
from google.area120.tables_v1alpha1.types.tables import BatchCreateRowsResponse
from google.area120.tables_v1alpha1.types.tables import BatchDeleteRowsRequest
from google.area120.tables_v1alpha1.types.tables import BatchUpdateRowsRequest
from google.area120.tables_v1alpha1.types.tables import BatchUpdateRowsResponse
from google.area120.tables_v1alpha1.types.tables import ColumnDescription
from google.area120.tables_v1alpha1.types.tables import CreateRowRequest
from google.area120.tables_v1alpha1.types.tables import DeleteRowRequest
from google.area120.tables_v1alpha1.types.tables import GetRowRequest
from google.area120.tables_v1alpha1.types.tables import GetTableRequest
from google.area120.tables_v1alpha1.types.tables import GetWorkspaceRequest
from google.area120.tables_v1alpha1.types.tables import LabeledItem
from google.area120.tables_v1alpha1.types.tables import ListRowsRequest
from google.area120.tables_v1alpha1.types.tables import ListRowsResponse
from google.area120.tables_v1alpha1.types.tables import ListTablesRequest
from google.area120.tables_v1alpha1.types.tables import ListTablesResponse
from google.area120.tables_v1alpha1.types.tables import ListWorkspacesRequest
from google.area120.tables_v1alpha1.types.tables import ListWorkspacesResponse
from google.area120.tables_v1alpha1.types.tables import LookupDetails
from google.area120.tables_v1alpha1.types.tables import RelationshipDetails
from google.area120.tables_v1alpha1.types.tables import Row
from google.area120.tables_v1alpha1.types.tables import Table
from google.area120.tables_v1alpha1.types.tables import UpdateRowRequest
from google.area120.tables_v1alpha1.types.tables import Workspace
from google.area120.tables_v1alpha1.types.tables import View

__all__ = (
    "TablesServiceClient",
    "TablesServiceAsyncClient",
    "BatchCreateRowsRequest",
    "BatchCreateRowsResponse",
    "BatchDeleteRowsRequest",
    "BatchUpdateRowsRequest",
    "BatchUpdateRowsResponse",
    "ColumnDescription",
    "CreateRowRequest",
    "DeleteRowRequest",
    "GetRowRequest",
    "GetTableRequest",
    "GetWorkspaceRequest",
    "LabeledItem",
    "ListRowsRequest",
    "ListRowsResponse",
    "ListTablesRequest",
    "ListTablesResponse",
    "ListWorkspacesRequest",
    "ListWorkspacesResponse",
    "LookupDetails",
    "RelationshipDetails",
    "Row",
    "Table",
    "UpdateRowRequest",
    "Workspace",
    "View",
)
