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

from .services.migration_service import (
    MigrationServiceAsyncClient,
    MigrationServiceClient,
)
from .types.migration_entities import MigrationSubtask, MigrationTask, MigrationWorkflow
from .types.migration_error_details import (
    ErrorDetail,
    ErrorLocation,
    ResourceErrorDetail,
)
from .types.migration_metrics import Point, TimeInterval, TimeSeries, TypedValue
from .types.migration_service import (
    CreateMigrationWorkflowRequest,
    DeleteMigrationWorkflowRequest,
    GetMigrationSubtaskRequest,
    GetMigrationWorkflowRequest,
    ListMigrationSubtasksRequest,
    ListMigrationSubtasksResponse,
    ListMigrationWorkflowsRequest,
    ListMigrationWorkflowsResponse,
    StartMigrationWorkflowRequest,
)
from .types.translation_config import (
    AzureSynapseDialect,
    BigQueryDialect,
    Dialect,
    HiveQLDialect,
    NameMappingKey,
    NameMappingValue,
    NetezzaDialect,
    ObjectNameMapping,
    ObjectNameMappingList,
    OracleDialect,
    RedshiftDialect,
    SnowflakeDialect,
    SourceEnv,
    SparkSQLDialect,
    SQLServerDialect,
    TeradataDialect,
    TranslationConfigDetails,
    VerticaDialect,
)

__all__ = (
    "MigrationServiceAsyncClient",
    "AzureSynapseDialect",
    "BigQueryDialect",
    "CreateMigrationWorkflowRequest",
    "DeleteMigrationWorkflowRequest",
    "Dialect",
    "ErrorDetail",
    "ErrorLocation",
    "GetMigrationSubtaskRequest",
    "GetMigrationWorkflowRequest",
    "HiveQLDialect",
    "ListMigrationSubtasksRequest",
    "ListMigrationSubtasksResponse",
    "ListMigrationWorkflowsRequest",
    "ListMigrationWorkflowsResponse",
    "MigrationServiceClient",
    "MigrationSubtask",
    "MigrationTask",
    "MigrationWorkflow",
    "NameMappingKey",
    "NameMappingValue",
    "NetezzaDialect",
    "ObjectNameMapping",
    "ObjectNameMappingList",
    "OracleDialect",
    "Point",
    "RedshiftDialect",
    "ResourceErrorDetail",
    "SQLServerDialect",
    "SnowflakeDialect",
    "SourceEnv",
    "SparkSQLDialect",
    "StartMigrationWorkflowRequest",
    "TeradataDialect",
    "TimeInterval",
    "TimeSeries",
    "TranslationConfigDetails",
    "TypedValue",
    "VerticaDialect",
)
