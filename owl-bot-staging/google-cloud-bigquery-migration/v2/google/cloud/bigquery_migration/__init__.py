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
from google.cloud.bigquery_migration import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.bigquery_migration_v2.services.migration_service.client import MigrationServiceClient
from google.cloud.bigquery_migration_v2.services.migration_service.async_client import MigrationServiceAsyncClient

from google.cloud.bigquery_migration_v2.types.migration_entities import MigrationSubtask
from google.cloud.bigquery_migration_v2.types.migration_entities import MigrationTask
from google.cloud.bigquery_migration_v2.types.migration_entities import MigrationTaskResult
from google.cloud.bigquery_migration_v2.types.migration_entities import MigrationWorkflow
from google.cloud.bigquery_migration_v2.types.migration_entities import TranslationTaskResult
from google.cloud.bigquery_migration_v2.types.migration_error_details import ErrorDetail
from google.cloud.bigquery_migration_v2.types.migration_error_details import ErrorLocation
from google.cloud.bigquery_migration_v2.types.migration_error_details import ResourceErrorDetail
from google.cloud.bigquery_migration_v2.types.migration_metrics import Point
from google.cloud.bigquery_migration_v2.types.migration_metrics import TimeInterval
from google.cloud.bigquery_migration_v2.types.migration_metrics import TimeSeries
from google.cloud.bigquery_migration_v2.types.migration_metrics import TypedValue
from google.cloud.bigquery_migration_v2.types.migration_service import CreateMigrationWorkflowRequest
from google.cloud.bigquery_migration_v2.types.migration_service import DeleteMigrationWorkflowRequest
from google.cloud.bigquery_migration_v2.types.migration_service import GetMigrationSubtaskRequest
from google.cloud.bigquery_migration_v2.types.migration_service import GetMigrationWorkflowRequest
from google.cloud.bigquery_migration_v2.types.migration_service import ListMigrationSubtasksRequest
from google.cloud.bigquery_migration_v2.types.migration_service import ListMigrationSubtasksResponse
from google.cloud.bigquery_migration_v2.types.migration_service import ListMigrationWorkflowsRequest
from google.cloud.bigquery_migration_v2.types.migration_service import ListMigrationWorkflowsResponse
from google.cloud.bigquery_migration_v2.types.migration_service import StartMigrationWorkflowRequest
from google.cloud.bigquery_migration_v2.types.translation_config import AzureSynapseDialect
from google.cloud.bigquery_migration_v2.types.translation_config import BigQueryDialect
from google.cloud.bigquery_migration_v2.types.translation_config import DB2Dialect
from google.cloud.bigquery_migration_v2.types.translation_config import Dialect
from google.cloud.bigquery_migration_v2.types.translation_config import GreenplumDialect
from google.cloud.bigquery_migration_v2.types.translation_config import HiveQLDialect
from google.cloud.bigquery_migration_v2.types.translation_config import MySQLDialect
from google.cloud.bigquery_migration_v2.types.translation_config import NameMappingKey
from google.cloud.bigquery_migration_v2.types.translation_config import NameMappingValue
from google.cloud.bigquery_migration_v2.types.translation_config import NetezzaDialect
from google.cloud.bigquery_migration_v2.types.translation_config import ObjectNameMapping
from google.cloud.bigquery_migration_v2.types.translation_config import ObjectNameMappingList
from google.cloud.bigquery_migration_v2.types.translation_config import OracleDialect
from google.cloud.bigquery_migration_v2.types.translation_config import PostgresqlDialect
from google.cloud.bigquery_migration_v2.types.translation_config import PrestoDialect
from google.cloud.bigquery_migration_v2.types.translation_config import RedshiftDialect
from google.cloud.bigquery_migration_v2.types.translation_config import SnowflakeDialect
from google.cloud.bigquery_migration_v2.types.translation_config import SourceEnv
from google.cloud.bigquery_migration_v2.types.translation_config import SparkSQLDialect
from google.cloud.bigquery_migration_v2.types.translation_config import SQLiteDialect
from google.cloud.bigquery_migration_v2.types.translation_config import SQLServerDialect
from google.cloud.bigquery_migration_v2.types.translation_config import TeradataDialect
from google.cloud.bigquery_migration_v2.types.translation_config import TranslationConfigDetails
from google.cloud.bigquery_migration_v2.types.translation_config import VerticaDialect
from google.cloud.bigquery_migration_v2.types.translation_details import Literal
from google.cloud.bigquery_migration_v2.types.translation_details import SourceEnvironment
from google.cloud.bigquery_migration_v2.types.translation_details import SourceSpec
from google.cloud.bigquery_migration_v2.types.translation_details import SourceTargetMapping
from google.cloud.bigquery_migration_v2.types.translation_details import TargetSpec
from google.cloud.bigquery_migration_v2.types.translation_details import TranslationDetails
from google.cloud.bigquery_migration_v2.types.translation_suggestion import TranslationReportRecord
from google.cloud.bigquery_migration_v2.types.translation_usability import GcsReportLogMessage

__all__ = ('MigrationServiceClient',
    'MigrationServiceAsyncClient',
    'MigrationSubtask',
    'MigrationTask',
    'MigrationTaskResult',
    'MigrationWorkflow',
    'TranslationTaskResult',
    'ErrorDetail',
    'ErrorLocation',
    'ResourceErrorDetail',
    'Point',
    'TimeInterval',
    'TimeSeries',
    'TypedValue',
    'CreateMigrationWorkflowRequest',
    'DeleteMigrationWorkflowRequest',
    'GetMigrationSubtaskRequest',
    'GetMigrationWorkflowRequest',
    'ListMigrationSubtasksRequest',
    'ListMigrationSubtasksResponse',
    'ListMigrationWorkflowsRequest',
    'ListMigrationWorkflowsResponse',
    'StartMigrationWorkflowRequest',
    'AzureSynapseDialect',
    'BigQueryDialect',
    'DB2Dialect',
    'Dialect',
    'GreenplumDialect',
    'HiveQLDialect',
    'MySQLDialect',
    'NameMappingKey',
    'NameMappingValue',
    'NetezzaDialect',
    'ObjectNameMapping',
    'ObjectNameMappingList',
    'OracleDialect',
    'PostgresqlDialect',
    'PrestoDialect',
    'RedshiftDialect',
    'SnowflakeDialect',
    'SourceEnv',
    'SparkSQLDialect',
    'SQLiteDialect',
    'SQLServerDialect',
    'TeradataDialect',
    'TranslationConfigDetails',
    'VerticaDialect',
    'Literal',
    'SourceEnvironment',
    'SourceSpec',
    'SourceTargetMapping',
    'TargetSpec',
    'TranslationDetails',
    'TranslationReportRecord',
    'GcsReportLogMessage',
)
