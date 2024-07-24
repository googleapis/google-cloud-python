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


from .services.migration_service import MigrationServiceClient
from .services.migration_service import MigrationServiceAsyncClient

from .types.migration_entities import MigrationSubtask
from .types.migration_entities import MigrationTask
from .types.migration_entities import MigrationTaskResult
from .types.migration_entities import MigrationWorkflow
from .types.migration_entities import TranslationTaskResult
from .types.migration_error_details import ErrorDetail
from .types.migration_error_details import ErrorLocation
from .types.migration_error_details import ResourceErrorDetail
from .types.migration_metrics import Point
from .types.migration_metrics import TimeInterval
from .types.migration_metrics import TimeSeries
from .types.migration_metrics import TypedValue
from .types.migration_service import CreateMigrationWorkflowRequest
from .types.migration_service import DeleteMigrationWorkflowRequest
from .types.migration_service import GetMigrationSubtaskRequest
from .types.migration_service import GetMigrationWorkflowRequest
from .types.migration_service import ListMigrationSubtasksRequest
from .types.migration_service import ListMigrationSubtasksResponse
from .types.migration_service import ListMigrationWorkflowsRequest
from .types.migration_service import ListMigrationWorkflowsResponse
from .types.migration_service import StartMigrationWorkflowRequest
from .types.translation_config import AzureSynapseDialect
from .types.translation_config import BigQueryDialect
from .types.translation_config import DB2Dialect
from .types.translation_config import Dialect
from .types.translation_config import GreenplumDialect
from .types.translation_config import HiveQLDialect
from .types.translation_config import MySQLDialect
from .types.translation_config import NameMappingKey
from .types.translation_config import NameMappingValue
from .types.translation_config import NetezzaDialect
from .types.translation_config import ObjectNameMapping
from .types.translation_config import ObjectNameMappingList
from .types.translation_config import OracleDialect
from .types.translation_config import PostgresqlDialect
from .types.translation_config import PrestoDialect
from .types.translation_config import RedshiftDialect
from .types.translation_config import SnowflakeDialect
from .types.translation_config import SourceEnv
from .types.translation_config import SparkSQLDialect
from .types.translation_config import SQLiteDialect
from .types.translation_config import SQLServerDialect
from .types.translation_config import TeradataDialect
from .types.translation_config import TranslationConfigDetails
from .types.translation_config import VerticaDialect
from .types.translation_details import Literal
from .types.translation_details import SourceEnvironment
from .types.translation_details import SourceSpec
from .types.translation_details import SourceTargetMapping
from .types.translation_details import TargetSpec
from .types.translation_details import TranslationDetails
from .types.translation_suggestion import TranslationReportRecord
from .types.translation_usability import GcsReportLogMessage

__all__ = (
    'MigrationServiceAsyncClient',
'AzureSynapseDialect',
'BigQueryDialect',
'CreateMigrationWorkflowRequest',
'DB2Dialect',
'DeleteMigrationWorkflowRequest',
'Dialect',
'ErrorDetail',
'ErrorLocation',
'GcsReportLogMessage',
'GetMigrationSubtaskRequest',
'GetMigrationWorkflowRequest',
'GreenplumDialect',
'HiveQLDialect',
'ListMigrationSubtasksRequest',
'ListMigrationSubtasksResponse',
'ListMigrationWorkflowsRequest',
'ListMigrationWorkflowsResponse',
'Literal',
'MigrationServiceClient',
'MigrationSubtask',
'MigrationTask',
'MigrationTaskResult',
'MigrationWorkflow',
'MySQLDialect',
'NameMappingKey',
'NameMappingValue',
'NetezzaDialect',
'ObjectNameMapping',
'ObjectNameMappingList',
'OracleDialect',
'Point',
'PostgresqlDialect',
'PrestoDialect',
'RedshiftDialect',
'ResourceErrorDetail',
'SQLServerDialect',
'SQLiteDialect',
'SnowflakeDialect',
'SourceEnv',
'SourceEnvironment',
'SourceSpec',
'SourceTargetMapping',
'SparkSQLDialect',
'StartMigrationWorkflowRequest',
'TargetSpec',
'TeradataDialect',
'TimeInterval',
'TimeSeries',
'TranslationConfigDetails',
'TranslationDetails',
'TranslationReportRecord',
'TranslationTaskResult',
'TypedValue',
'VerticaDialect',
)
