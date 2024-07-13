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
from google.cloud.bigquery_migration_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.migration_service import (
    MigrationServiceAsyncClient,
    MigrationServiceClient,
)
from .types.migration_entities import (
    MigrationSubtask,
    MigrationTask,
    MigrationTaskResult,
    MigrationWorkflow,
    TranslationTaskResult,
)
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
    DB2Dialect,
    Dialect,
    GreenplumDialect,
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
    SQLiteDialect,
    SQLServerDialect,
    TeradataDialect,
    TranslationConfigDetails,
    VerticaDialect,
)
from .types.translation_details import (
    Literal,
    SourceEnvironment,
    SourceSpec,
    SourceTargetMapping,
    TargetSpec,
    TranslationDetails,
)
from .types.translation_suggestion import TranslationReportRecord
from .types.translation_usability import GcsReportLogMessage

__all__ = (
    "MigrationServiceAsyncClient",
    "AzureSynapseDialect",
    "BigQueryDialect",
    "CreateMigrationWorkflowRequest",
    "DB2Dialect",
    "DeleteMigrationWorkflowRequest",
    "Dialect",
    "ErrorDetail",
    "ErrorLocation",
    "GcsReportLogMessage",
    "GetMigrationSubtaskRequest",
    "GetMigrationWorkflowRequest",
    "GreenplumDialect",
    "HiveQLDialect",
    "ListMigrationSubtasksRequest",
    "ListMigrationSubtasksResponse",
    "ListMigrationWorkflowsRequest",
    "ListMigrationWorkflowsResponse",
    "Literal",
    "MigrationServiceClient",
    "MigrationSubtask",
    "MigrationTask",
    "MigrationTaskResult",
    "MigrationWorkflow",
    "MySQLDialect",
    "NameMappingKey",
    "NameMappingValue",
    "NetezzaDialect",
    "ObjectNameMapping",
    "ObjectNameMappingList",
    "OracleDialect",
    "Point",
    "PostgresqlDialect",
    "PrestoDialect",
    "RedshiftDialect",
    "ResourceErrorDetail",
    "SQLServerDialect",
    "SQLiteDialect",
    "SnowflakeDialect",
    "SourceEnv",
    "SourceEnvironment",
    "SourceSpec",
    "SourceTargetMapping",
    "SparkSQLDialect",
    "StartMigrationWorkflowRequest",
    "TargetSpec",
    "TeradataDialect",
    "TimeInterval",
    "TimeSeries",
    "TranslationConfigDetails",
    "TranslationDetails",
    "TranslationReportRecord",
    "TranslationTaskResult",
    "TypedValue",
    "VerticaDialect",
)
