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
from google.cloud.discoveryengine_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.completion_service import (
    CompletionServiceAsyncClient,
    CompletionServiceClient,
)
from .services.control_service import ControlServiceAsyncClient, ControlServiceClient
from .services.conversational_search_service import (
    ConversationalSearchServiceAsyncClient,
    ConversationalSearchServiceClient,
)
from .services.data_store_service import (
    DataStoreServiceAsyncClient,
    DataStoreServiceClient,
)
from .services.document_service import DocumentServiceAsyncClient, DocumentServiceClient
from .services.engine_service import EngineServiceAsyncClient, EngineServiceClient
from .services.grounded_generation_service import (
    GroundedGenerationServiceAsyncClient,
    GroundedGenerationServiceClient,
)
from .services.project_service import ProjectServiceAsyncClient, ProjectServiceClient
from .services.rank_service import RankServiceAsyncClient, RankServiceClient
from .services.recommendation_service import (
    RecommendationServiceAsyncClient,
    RecommendationServiceClient,
)
from .services.schema_service import SchemaServiceAsyncClient, SchemaServiceClient
from .services.search_service import SearchServiceAsyncClient, SearchServiceClient
from .services.site_search_engine_service import (
    SiteSearchEngineServiceAsyncClient,
    SiteSearchEngineServiceClient,
)
from .services.user_event_service import (
    UserEventServiceAsyncClient,
    UserEventServiceClient,
)
from .types.answer import Answer
from .types.chunk import Chunk
from .types.common import (
    CustomAttribute,
    IndustryVertical,
    Interval,
    SearchAddOn,
    SearchTier,
    SearchUseCase,
    SolutionType,
    UserInfo,
)
from .types.completion import CompletionSuggestion, SuggestionDenyListEntry
from .types.completion_service import CompleteQueryRequest, CompleteQueryResponse
from .types.control import Condition, Control
from .types.control_service import (
    CreateControlRequest,
    DeleteControlRequest,
    GetControlRequest,
    ListControlsRequest,
    ListControlsResponse,
    UpdateControlRequest,
)
from .types.conversation import (
    Conversation,
    ConversationContext,
    ConversationMessage,
    Reply,
    TextInput,
)
from .types.conversational_search_service import (
    AnswerQueryRequest,
    AnswerQueryResponse,
    ConverseConversationRequest,
    ConverseConversationResponse,
    CreateConversationRequest,
    CreateSessionRequest,
    DeleteConversationRequest,
    DeleteSessionRequest,
    GetAnswerRequest,
    GetConversationRequest,
    GetSessionRequest,
    ListConversationsRequest,
    ListConversationsResponse,
    ListSessionsRequest,
    ListSessionsResponse,
    UpdateConversationRequest,
    UpdateSessionRequest,
)
from .types.data_store import DataStore
from .types.data_store_service import (
    CreateDataStoreMetadata,
    CreateDataStoreRequest,
    DeleteDataStoreMetadata,
    DeleteDataStoreRequest,
    GetDataStoreRequest,
    ListDataStoresRequest,
    ListDataStoresResponse,
    UpdateDataStoreRequest,
)
from .types.document import Document
from .types.document_processing_config import DocumentProcessingConfig
from .types.document_service import (
    CreateDocumentRequest,
    DeleteDocumentRequest,
    GetDocumentRequest,
    ListDocumentsRequest,
    ListDocumentsResponse,
    UpdateDocumentRequest,
)
from .types.engine import Engine
from .types.engine_service import (
    CreateEngineMetadata,
    CreateEngineRequest,
    DeleteEngineMetadata,
    DeleteEngineRequest,
    GetEngineRequest,
    ListEnginesRequest,
    ListEnginesResponse,
    UpdateEngineRequest,
)
from .types.grounded_generation_service import (
    CheckGroundingRequest,
    CheckGroundingResponse,
    CheckGroundingSpec,
)
from .types.grounding import FactChunk, GroundingFact
from .types.import_config import (
    AlloyDbSource,
    BigQuerySource,
    BigtableOptions,
    BigtableSource,
    CloudSqlSource,
    FhirStoreSource,
    FirestoreSource,
    GcsSource,
    ImportCompletionSuggestionsMetadata,
    ImportCompletionSuggestionsRequest,
    ImportCompletionSuggestionsResponse,
    ImportDocumentsMetadata,
    ImportDocumentsRequest,
    ImportDocumentsResponse,
    ImportErrorConfig,
    ImportSuggestionDenyListEntriesMetadata,
    ImportSuggestionDenyListEntriesRequest,
    ImportSuggestionDenyListEntriesResponse,
    ImportUserEventsMetadata,
    ImportUserEventsRequest,
    ImportUserEventsResponse,
    SpannerSource,
)
from .types.project import Project
from .types.project_service import ProvisionProjectMetadata, ProvisionProjectRequest
from .types.purge_config import (
    PurgeCompletionSuggestionsMetadata,
    PurgeCompletionSuggestionsRequest,
    PurgeCompletionSuggestionsResponse,
    PurgeDocumentsMetadata,
    PurgeDocumentsRequest,
    PurgeDocumentsResponse,
    PurgeSuggestionDenyListEntriesMetadata,
    PurgeSuggestionDenyListEntriesRequest,
    PurgeSuggestionDenyListEntriesResponse,
)
from .types.rank_service import RankingRecord, RankRequest, RankResponse
from .types.recommendation_service import RecommendRequest, RecommendResponse
from .types.schema import Schema
from .types.schema_service import (
    CreateSchemaMetadata,
    CreateSchemaRequest,
    DeleteSchemaMetadata,
    DeleteSchemaRequest,
    GetSchemaRequest,
    ListSchemasRequest,
    ListSchemasResponse,
    UpdateSchemaMetadata,
    UpdateSchemaRequest,
)
from .types.search_service import SearchRequest, SearchResponse
from .types.session import Query, Session
from .types.site_search_engine import SiteSearchEngine, SiteVerificationInfo, TargetSite
from .types.site_search_engine_service import (
    BatchCreateTargetSiteMetadata,
    BatchCreateTargetSitesRequest,
    BatchCreateTargetSitesResponse,
    BatchVerifyTargetSitesMetadata,
    BatchVerifyTargetSitesRequest,
    BatchVerifyTargetSitesResponse,
    CreateTargetSiteMetadata,
    CreateTargetSiteRequest,
    DeleteTargetSiteMetadata,
    DeleteTargetSiteRequest,
    DisableAdvancedSiteSearchMetadata,
    DisableAdvancedSiteSearchRequest,
    DisableAdvancedSiteSearchResponse,
    EnableAdvancedSiteSearchMetadata,
    EnableAdvancedSiteSearchRequest,
    EnableAdvancedSiteSearchResponse,
    FetchDomainVerificationStatusRequest,
    FetchDomainVerificationStatusResponse,
    GetSiteSearchEngineRequest,
    GetTargetSiteRequest,
    ListTargetSitesRequest,
    ListTargetSitesResponse,
    RecrawlUrisMetadata,
    RecrawlUrisRequest,
    RecrawlUrisResponse,
    UpdateTargetSiteMetadata,
    UpdateTargetSiteRequest,
)
from .types.user_event import (
    CompletionInfo,
    DocumentInfo,
    MediaInfo,
    PageInfo,
    PanelInfo,
    SearchInfo,
    TransactionInfo,
    UserEvent,
)
from .types.user_event_service import CollectUserEventRequest, WriteUserEventRequest

__all__ = (
    "CompletionServiceAsyncClient",
    "ControlServiceAsyncClient",
    "ConversationalSearchServiceAsyncClient",
    "DataStoreServiceAsyncClient",
    "DocumentServiceAsyncClient",
    "EngineServiceAsyncClient",
    "GroundedGenerationServiceAsyncClient",
    "ProjectServiceAsyncClient",
    "RankServiceAsyncClient",
    "RecommendationServiceAsyncClient",
    "SchemaServiceAsyncClient",
    "SearchServiceAsyncClient",
    "SiteSearchEngineServiceAsyncClient",
    "UserEventServiceAsyncClient",
    "AlloyDbSource",
    "Answer",
    "AnswerQueryRequest",
    "AnswerQueryResponse",
    "BatchCreateTargetSiteMetadata",
    "BatchCreateTargetSitesRequest",
    "BatchCreateTargetSitesResponse",
    "BatchVerifyTargetSitesMetadata",
    "BatchVerifyTargetSitesRequest",
    "BatchVerifyTargetSitesResponse",
    "BigQuerySource",
    "BigtableOptions",
    "BigtableSource",
    "CheckGroundingRequest",
    "CheckGroundingResponse",
    "CheckGroundingSpec",
    "Chunk",
    "CloudSqlSource",
    "CollectUserEventRequest",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "CompletionInfo",
    "CompletionServiceClient",
    "CompletionSuggestion",
    "Condition",
    "Control",
    "ControlServiceClient",
    "Conversation",
    "ConversationContext",
    "ConversationMessage",
    "ConversationalSearchServiceClient",
    "ConverseConversationRequest",
    "ConverseConversationResponse",
    "CreateControlRequest",
    "CreateConversationRequest",
    "CreateDataStoreMetadata",
    "CreateDataStoreRequest",
    "CreateDocumentRequest",
    "CreateEngineMetadata",
    "CreateEngineRequest",
    "CreateSchemaMetadata",
    "CreateSchemaRequest",
    "CreateSessionRequest",
    "CreateTargetSiteMetadata",
    "CreateTargetSiteRequest",
    "CustomAttribute",
    "DataStore",
    "DataStoreServiceClient",
    "DeleteControlRequest",
    "DeleteConversationRequest",
    "DeleteDataStoreMetadata",
    "DeleteDataStoreRequest",
    "DeleteDocumentRequest",
    "DeleteEngineMetadata",
    "DeleteEngineRequest",
    "DeleteSchemaMetadata",
    "DeleteSchemaRequest",
    "DeleteSessionRequest",
    "DeleteTargetSiteMetadata",
    "DeleteTargetSiteRequest",
    "DisableAdvancedSiteSearchMetadata",
    "DisableAdvancedSiteSearchRequest",
    "DisableAdvancedSiteSearchResponse",
    "Document",
    "DocumentInfo",
    "DocumentProcessingConfig",
    "DocumentServiceClient",
    "EnableAdvancedSiteSearchMetadata",
    "EnableAdvancedSiteSearchRequest",
    "EnableAdvancedSiteSearchResponse",
    "Engine",
    "EngineServiceClient",
    "FactChunk",
    "FetchDomainVerificationStatusRequest",
    "FetchDomainVerificationStatusResponse",
    "FhirStoreSource",
    "FirestoreSource",
    "GcsSource",
    "GetAnswerRequest",
    "GetControlRequest",
    "GetConversationRequest",
    "GetDataStoreRequest",
    "GetDocumentRequest",
    "GetEngineRequest",
    "GetSchemaRequest",
    "GetSessionRequest",
    "GetSiteSearchEngineRequest",
    "GetTargetSiteRequest",
    "GroundedGenerationServiceClient",
    "GroundingFact",
    "ImportCompletionSuggestionsMetadata",
    "ImportCompletionSuggestionsRequest",
    "ImportCompletionSuggestionsResponse",
    "ImportDocumentsMetadata",
    "ImportDocumentsRequest",
    "ImportDocumentsResponse",
    "ImportErrorConfig",
    "ImportSuggestionDenyListEntriesMetadata",
    "ImportSuggestionDenyListEntriesRequest",
    "ImportSuggestionDenyListEntriesResponse",
    "ImportUserEventsMetadata",
    "ImportUserEventsRequest",
    "ImportUserEventsResponse",
    "IndustryVertical",
    "Interval",
    "ListControlsRequest",
    "ListControlsResponse",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "ListDataStoresRequest",
    "ListDataStoresResponse",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "ListEnginesRequest",
    "ListEnginesResponse",
    "ListSchemasRequest",
    "ListSchemasResponse",
    "ListSessionsRequest",
    "ListSessionsResponse",
    "ListTargetSitesRequest",
    "ListTargetSitesResponse",
    "MediaInfo",
    "PageInfo",
    "PanelInfo",
    "Project",
    "ProjectServiceClient",
    "ProvisionProjectMetadata",
    "ProvisionProjectRequest",
    "PurgeCompletionSuggestionsMetadata",
    "PurgeCompletionSuggestionsRequest",
    "PurgeCompletionSuggestionsResponse",
    "PurgeDocumentsMetadata",
    "PurgeDocumentsRequest",
    "PurgeDocumentsResponse",
    "PurgeSuggestionDenyListEntriesMetadata",
    "PurgeSuggestionDenyListEntriesRequest",
    "PurgeSuggestionDenyListEntriesResponse",
    "Query",
    "RankRequest",
    "RankResponse",
    "RankServiceClient",
    "RankingRecord",
    "RecommendRequest",
    "RecommendResponse",
    "RecommendationServiceClient",
    "RecrawlUrisMetadata",
    "RecrawlUrisRequest",
    "RecrawlUrisResponse",
    "Reply",
    "Schema",
    "SchemaServiceClient",
    "SearchAddOn",
    "SearchInfo",
    "SearchRequest",
    "SearchResponse",
    "SearchServiceClient",
    "SearchTier",
    "SearchUseCase",
    "Session",
    "SiteSearchEngine",
    "SiteSearchEngineServiceClient",
    "SiteVerificationInfo",
    "SolutionType",
    "SpannerSource",
    "SuggestionDenyListEntry",
    "TargetSite",
    "TextInput",
    "TransactionInfo",
    "UpdateControlRequest",
    "UpdateConversationRequest",
    "UpdateDataStoreRequest",
    "UpdateDocumentRequest",
    "UpdateEngineRequest",
    "UpdateSchemaMetadata",
    "UpdateSchemaRequest",
    "UpdateSessionRequest",
    "UpdateTargetSiteMetadata",
    "UpdateTargetSiteRequest",
    "UserEvent",
    "UserEventServiceClient",
    "UserInfo",
    "WriteUserEventRequest",
)
