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
from google.area120.tables import gapic_version as package_version

__version__ = package_version.__version__


from google.area120.tables_v1alpha1.services.tables_service.async_client import (
    TablesServiceAsyncClient,
)
from google.area120.tables_v1alpha1.services.tables_service.client import (
    TablesServiceClient,
)
from google.area120.tables_v1alpha1.types.tables import (
    BatchCreateRowsRequest,
    BatchCreateRowsResponse,
    BatchDeleteRowsRequest,
    BatchUpdateRowsRequest,
    BatchUpdateRowsResponse,
    ColumnDescription,
    CreateRowRequest,
    DeleteRowRequest,
    GetRowRequest,
    GetTableRequest,
    GetWorkspaceRequest,
    LabeledItem,
    ListRowsRequest,
    ListRowsResponse,
    ListTablesRequest,
    ListTablesResponse,
    ListWorkspacesRequest,
    ListWorkspacesResponse,
    LookupDetails,
    RelationshipDetails,
    Row,
    Table,
    UpdateRowRequest,
    View,
    Workspace,
)

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
