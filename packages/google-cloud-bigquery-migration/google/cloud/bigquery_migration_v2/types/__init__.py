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
from .migration_entities import MigrationSubtask, MigrationTask, MigrationWorkflow
from .migration_error_details import ErrorDetail, ErrorLocation, ResourceErrorDetail
from .migration_metrics import Point, TimeInterval, TimeSeries, TypedValue
from .migration_service import (
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
from .translation_config import (
    AzureSynapseDialect,
    BigQueryDialect,
    Dialect,
    HiveQLDialect,
    MySQLDialect,
    NameMappingKey,
    NameMappingValue,
    NetezzaDialect,
    ObjectNameMapping,
    ObjectNameMappingList,
    OracleDialect,
    PostgresqlDialect,
    PrestoDialect,
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
    "MigrationSubtask",
    "MigrationTask",
    "MigrationWorkflow",
    "ErrorDetail",
    "ErrorLocation",
    "ResourceErrorDetail",
    "Point",
    "TimeInterval",
    "TimeSeries",
    "TypedValue",
    "CreateMigrationWorkflowRequest",
    "DeleteMigrationWorkflowRequest",
    "GetMigrationSubtaskRequest",
    "GetMigrationWorkflowRequest",
    "ListMigrationSubtasksRequest",
    "ListMigrationSubtasksResponse",
    "ListMigrationWorkflowsRequest",
    "ListMigrationWorkflowsResponse",
    "StartMigrationWorkflowRequest",
    "AzureSynapseDialect",
    "BigQueryDialect",
    "Dialect",
    "HiveQLDialect",
    "MySQLDialect",
    "NameMappingKey",
    "NameMappingValue",
    "NetezzaDialect",
    "ObjectNameMapping",
    "ObjectNameMappingList",
    "OracleDialect",
    "PostgresqlDialect",
    "PrestoDialect",
    "RedshiftDialect",
    "SnowflakeDialect",
    "SourceEnv",
    "SparkSQLDialect",
    "SQLServerDialect",
    "TeradataDialect",
    "TranslationConfigDetails",
    "VerticaDialect",
)
