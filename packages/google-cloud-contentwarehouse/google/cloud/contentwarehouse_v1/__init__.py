# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.contentwarehouse_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.document_link_service import (
    DocumentLinkServiceAsyncClient,
    DocumentLinkServiceClient,
)
from .services.document_schema_service import (
    DocumentSchemaServiceAsyncClient,
    DocumentSchemaServiceClient,
)
from .services.document_service import DocumentServiceAsyncClient, DocumentServiceClient
from .services.pipeline_service import PipelineServiceAsyncClient, PipelineServiceClient
from .services.rule_set_service import RuleSetServiceAsyncClient, RuleSetServiceClient
from .services.synonym_set_service import (
    SynonymSetServiceAsyncClient,
    SynonymSetServiceClient,
)
from .types.async_document_service_request import (
    CreateDocumentMetadata,
    UpdateDocumentMetadata,
)
from .types.common import (
    AccessControlMode,
    DatabaseType,
    DocumentCreatorDefaultRole,
    MergeFieldsOptions,
    RequestMetadata,
    ResponseMetadata,
    UpdateOptions,
    UpdateType,
    UserInfo,
)
from .types.document import (
    ContentCategory,
    DateTimeArray,
    Document,
    DocumentReference,
    EnumArray,
    EnumValue,
    FloatArray,
    IntegerArray,
    MapProperty,
    Property,
    PropertyArray,
    RawDocumentFileType,
    TextArray,
    TimestampArray,
    TimestampValue,
    Value,
)
from .types.document_link_service import (
    CreateDocumentLinkRequest,
    DeleteDocumentLinkRequest,
    DocumentLink,
    ListLinkedSourcesRequest,
    ListLinkedSourcesResponse,
    ListLinkedTargetsRequest,
    ListLinkedTargetsResponse,
)
from .types.document_schema import (
    DateTimeTypeOptions,
    DocumentSchema,
    EnumTypeOptions,
    FloatTypeOptions,
    IntegerTypeOptions,
    MapTypeOptions,
    PropertyDefinition,
    PropertyTypeOptions,
    TextTypeOptions,
    TimestampTypeOptions,
)
from .types.document_schema_service import (
    CreateDocumentSchemaRequest,
    DeleteDocumentSchemaRequest,
    GetDocumentSchemaRequest,
    ListDocumentSchemasRequest,
    ListDocumentSchemasResponse,
    UpdateDocumentSchemaRequest,
)
from .types.document_service import (
    CreateDocumentResponse,
    FetchAclResponse,
    QAResult,
    SearchDocumentsResponse,
    SetAclResponse,
    UpdateDocumentResponse,
)
from .types.document_service_request import (
    CloudAIDocumentOption,
    CreateDocumentRequest,
    DeleteDocumentRequest,
    FetchAclRequest,
    GetDocumentRequest,
    LockDocumentRequest,
    SearchDocumentsRequest,
    SetAclRequest,
    UpdateDocumentRequest,
)
from .types.filters import (
    CustomWeightsMetadata,
    DocumentQuery,
    FileTypeFilter,
    PropertyFilter,
    TimeFilter,
    WeightedSchemaProperty,
)
from .types.histogram import (
    HistogramQuery,
    HistogramQueryPropertyNameFilter,
    HistogramQueryResult,
)
from .types.pipeline_service import RunPipelineRequest
from .types.pipelines import (
    ExportToCdwPipeline,
    GcsIngestPipeline,
    GcsIngestWithDocAiProcessorsPipeline,
    IngestPipelineConfig,
    ProcessorInfo,
    ProcessWithDocAiPipeline,
    RunPipelineMetadata,
    RunPipelineResponse,
)
from .types.rule_engine import (
    AccessControlAction,
    Action,
    ActionExecutorOutput,
    ActionOutput,
    AddToFolderAction,
    DataUpdateAction,
    DataValidationAction,
    DeleteDocumentAction,
    InvalidRule,
    PublishAction,
    RemoveFromFolderAction,
    Rule,
    RuleActionsPair,
    RuleEngineOutput,
    RuleEvaluatorOutput,
    RuleSet,
)
from .types.ruleset_service_request import (
    CreateRuleSetRequest,
    DeleteRuleSetRequest,
    GetRuleSetRequest,
    ListRuleSetsRequest,
    ListRuleSetsResponse,
    UpdateRuleSetRequest,
)
from .types.synonymset import SynonymSet
from .types.synonymset_service_request import (
    CreateSynonymSetRequest,
    DeleteSynonymSetRequest,
    GetSynonymSetRequest,
    ListSynonymSetsRequest,
    ListSynonymSetsResponse,
    UpdateSynonymSetRequest,
)

__all__ = (
    "DocumentLinkServiceAsyncClient",
    "DocumentSchemaServiceAsyncClient",
    "DocumentServiceAsyncClient",
    "PipelineServiceAsyncClient",
    "RuleSetServiceAsyncClient",
    "SynonymSetServiceAsyncClient",
    "AccessControlAction",
    "AccessControlMode",
    "Action",
    "ActionExecutorOutput",
    "ActionOutput",
    "AddToFolderAction",
    "CloudAIDocumentOption",
    "ContentCategory",
    "CreateDocumentLinkRequest",
    "CreateDocumentMetadata",
    "CreateDocumentRequest",
    "CreateDocumentResponse",
    "CreateDocumentSchemaRequest",
    "CreateRuleSetRequest",
    "CreateSynonymSetRequest",
    "CustomWeightsMetadata",
    "DataUpdateAction",
    "DataValidationAction",
    "DatabaseType",
    "DateTimeArray",
    "DateTimeTypeOptions",
    "DeleteDocumentAction",
    "DeleteDocumentLinkRequest",
    "DeleteDocumentRequest",
    "DeleteDocumentSchemaRequest",
    "DeleteRuleSetRequest",
    "DeleteSynonymSetRequest",
    "Document",
    "DocumentCreatorDefaultRole",
    "DocumentLink",
    "DocumentLinkServiceClient",
    "DocumentQuery",
    "DocumentReference",
    "DocumentSchema",
    "DocumentSchemaServiceClient",
    "DocumentServiceClient",
    "EnumArray",
    "EnumTypeOptions",
    "EnumValue",
    "ExportToCdwPipeline",
    "FetchAclRequest",
    "FetchAclResponse",
    "FileTypeFilter",
    "FloatArray",
    "FloatTypeOptions",
    "GcsIngestPipeline",
    "GcsIngestWithDocAiProcessorsPipeline",
    "GetDocumentRequest",
    "GetDocumentSchemaRequest",
    "GetRuleSetRequest",
    "GetSynonymSetRequest",
    "HistogramQuery",
    "HistogramQueryPropertyNameFilter",
    "HistogramQueryResult",
    "IngestPipelineConfig",
    "IntegerArray",
    "IntegerTypeOptions",
    "InvalidRule",
    "ListDocumentSchemasRequest",
    "ListDocumentSchemasResponse",
    "ListLinkedSourcesRequest",
    "ListLinkedSourcesResponse",
    "ListLinkedTargetsRequest",
    "ListLinkedTargetsResponse",
    "ListRuleSetsRequest",
    "ListRuleSetsResponse",
    "ListSynonymSetsRequest",
    "ListSynonymSetsResponse",
    "LockDocumentRequest",
    "MapProperty",
    "MapTypeOptions",
    "MergeFieldsOptions",
    "PipelineServiceClient",
    "ProcessWithDocAiPipeline",
    "ProcessorInfo",
    "Property",
    "PropertyArray",
    "PropertyDefinition",
    "PropertyFilter",
    "PropertyTypeOptions",
    "PublishAction",
    "QAResult",
    "RawDocumentFileType",
    "RemoveFromFolderAction",
    "RequestMetadata",
    "ResponseMetadata",
    "Rule",
    "RuleActionsPair",
    "RuleEngineOutput",
    "RuleEvaluatorOutput",
    "RuleSet",
    "RuleSetServiceClient",
    "RunPipelineMetadata",
    "RunPipelineRequest",
    "RunPipelineResponse",
    "SearchDocumentsRequest",
    "SearchDocumentsResponse",
    "SetAclRequest",
    "SetAclResponse",
    "SynonymSet",
    "SynonymSetServiceClient",
    "TextArray",
    "TextTypeOptions",
    "TimeFilter",
    "TimestampArray",
    "TimestampTypeOptions",
    "TimestampValue",
    "UpdateDocumentMetadata",
    "UpdateDocumentRequest",
    "UpdateDocumentResponse",
    "UpdateDocumentSchemaRequest",
    "UpdateOptions",
    "UpdateRuleSetRequest",
    "UpdateSynonymSetRequest",
    "UpdateType",
    "UserInfo",
    "Value",
    "WeightedSchemaProperty",
)
