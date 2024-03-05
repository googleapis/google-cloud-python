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
from google.cloud.bigquery_migration_v2alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.migration_service import (
    MigrationServiceAsyncClient,
    MigrationServiceClient,
)
from .services.sql_translation_service import (
    SqlTranslationServiceAsyncClient,
    SqlTranslationServiceClient,
)
from .types.assessment_task import (
    AssessmentOrchestrationResultDetails,
    AssessmentTaskDetails,
)
from .types.migration_entities import (
    MigrationSubtask,
    MigrationTask,
    MigrationTaskOrchestrationResult,
    MigrationWorkflow,
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
from .types.translation_service import (
    SqlTranslationError,
    SqlTranslationErrorDetail,
    SqlTranslationWarning,
    TranslateQueryRequest,
    TranslateQueryResponse,
)
from .types.translation_task import (
    BteqOptions,
    DatasetReference,
    Filter,
    IdentifierSettings,
    TeradataOptions,
    TranslationFileMapping,
    TranslationTaskDetails,
)

__all__ = (
    "MigrationServiceAsyncClient",
    "SqlTranslationServiceAsyncClient",
    "AssessmentOrchestrationResultDetails",
    "AssessmentTaskDetails",
    "BteqOptions",
    "CreateMigrationWorkflowRequest",
    "DatasetReference",
    "DeleteMigrationWorkflowRequest",
    "ErrorDetail",
    "ErrorLocation",
    "Filter",
    "GetMigrationSubtaskRequest",
    "GetMigrationWorkflowRequest",
    "IdentifierSettings",
    "ListMigrationSubtasksRequest",
    "ListMigrationSubtasksResponse",
    "ListMigrationWorkflowsRequest",
    "ListMigrationWorkflowsResponse",
    "MigrationServiceClient",
    "MigrationSubtask",
    "MigrationTask",
    "MigrationTaskOrchestrationResult",
    "MigrationWorkflow",
    "Point",
    "ResourceErrorDetail",
    "SqlTranslationError",
    "SqlTranslationErrorDetail",
    "SqlTranslationServiceClient",
    "SqlTranslationWarning",
    "StartMigrationWorkflowRequest",
    "TeradataOptions",
    "TimeInterval",
    "TimeSeries",
    "TranslateQueryRequest",
    "TranslateQueryResponse",
    "TranslationFileMapping",
    "TranslationTaskDetails",
    "TypedValue",
)
