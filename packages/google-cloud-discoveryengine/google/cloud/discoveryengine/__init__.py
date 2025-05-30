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
from google.cloud.discoveryengine import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.discoveryengine_v1.services.completion_service.async_client import (
    CompletionServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.completion_service.client import (
    CompletionServiceClient,
)
from google.cloud.discoveryengine_v1.services.control_service.async_client import (
    ControlServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.control_service.client import (
    ControlServiceClient,
)
from google.cloud.discoveryengine_v1.services.conversational_search_service.async_client import (
    ConversationalSearchServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.conversational_search_service.client import (
    ConversationalSearchServiceClient,
)
from google.cloud.discoveryengine_v1.services.data_store_service.async_client import (
    DataStoreServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.data_store_service.client import (
    DataStoreServiceClient,
)
from google.cloud.discoveryengine_v1.services.document_service.async_client import (
    DocumentServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.document_service.client import (
    DocumentServiceClient,
)
from google.cloud.discoveryengine_v1.services.engine_service.async_client import (
    EngineServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.engine_service.client import (
    EngineServiceClient,
)
from google.cloud.discoveryengine_v1.services.grounded_generation_service.async_client import (
    GroundedGenerationServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.grounded_generation_service.client import (
    GroundedGenerationServiceClient,
)
from google.cloud.discoveryengine_v1.services.project_service.async_client import (
    ProjectServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.project_service.client import (
    ProjectServiceClient,
)
from google.cloud.discoveryengine_v1.services.rank_service.async_client import (
    RankServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.rank_service.client import (
    RankServiceClient,
)
from google.cloud.discoveryengine_v1.services.recommendation_service.async_client import (
    RecommendationServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.recommendation_service.client import (
    RecommendationServiceClient,
)
from google.cloud.discoveryengine_v1.services.schema_service.async_client import (
    SchemaServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.schema_service.client import (
    SchemaServiceClient,
)
from google.cloud.discoveryengine_v1.services.search_service.async_client import (
    SearchServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.search_service.client import (
    SearchServiceClient,
)
from google.cloud.discoveryengine_v1.services.search_tuning_service.async_client import (
    SearchTuningServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.search_tuning_service.client import (
    SearchTuningServiceClient,
)
from google.cloud.discoveryengine_v1.services.serving_config_service.async_client import (
    ServingConfigServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.serving_config_service.client import (
    ServingConfigServiceClient,
)
from google.cloud.discoveryengine_v1.services.site_search_engine_service.async_client import (
    SiteSearchEngineServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.site_search_engine_service.client import (
    SiteSearchEngineServiceClient,
)
from google.cloud.discoveryengine_v1.services.user_event_service.async_client import (
    UserEventServiceAsyncClient,
)
from google.cloud.discoveryengine_v1.services.user_event_service.client import (
    UserEventServiceClient,
)
from google.cloud.discoveryengine_v1.types.answer import Answer
from google.cloud.discoveryengine_v1.types.chunk import Chunk
from google.cloud.discoveryengine_v1.types.common import (
    CustomAttribute,
    DoubleList,
    IndustryVertical,
    Interval,
    SearchAddOn,
    SearchLinkPromotion,
    SearchTier,
    SearchUseCase,
    SolutionType,
    UserInfo,
)
from google.cloud.discoveryengine_v1.types.completion import (
    CompletionSuggestion,
    SuggestionDenyListEntry,
)
from google.cloud.discoveryengine_v1.types.completion_service import (
    CompleteQueryRequest,
    CompleteQueryResponse,
)
from google.cloud.discoveryengine_v1.types.control import Condition, Control
from google.cloud.discoveryengine_v1.types.control_service import (
    CreateControlRequest,
    DeleteControlRequest,
    GetControlRequest,
    ListControlsRequest,
    ListControlsResponse,
    UpdateControlRequest,
)
from google.cloud.discoveryengine_v1.types.conversation import (
    Conversation,
    ConversationContext,
    ConversationMessage,
    Reply,
    TextInput,
)
from google.cloud.discoveryengine_v1.types.conversational_search_service import (
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
from google.cloud.discoveryengine_v1.types.custom_tuning_model import CustomTuningModel
from google.cloud.discoveryengine_v1.types.data_store import (
    AdvancedSiteSearchConfig,
    DataStore,
    WorkspaceConfig,
)
from google.cloud.discoveryengine_v1.types.data_store_service import (
    CreateDataStoreMetadata,
    CreateDataStoreRequest,
    DeleteDataStoreMetadata,
    DeleteDataStoreRequest,
    GetDataStoreRequest,
    ListDataStoresRequest,
    ListDataStoresResponse,
    UpdateDataStoreRequest,
)
from google.cloud.discoveryengine_v1.types.document import Document
from google.cloud.discoveryengine_v1.types.document_processing_config import (
    DocumentProcessingConfig,
)
from google.cloud.discoveryengine_v1.types.document_service import (
    BatchGetDocumentsMetadataRequest,
    BatchGetDocumentsMetadataResponse,
    CreateDocumentRequest,
    DeleteDocumentRequest,
    GetDocumentRequest,
    ListDocumentsRequest,
    ListDocumentsResponse,
    UpdateDocumentRequest,
)
from google.cloud.discoveryengine_v1.types.engine import Engine
from google.cloud.discoveryengine_v1.types.engine_service import (
    CreateEngineMetadata,
    CreateEngineRequest,
    DeleteEngineMetadata,
    DeleteEngineRequest,
    GetEngineRequest,
    ListEnginesRequest,
    ListEnginesResponse,
    UpdateEngineRequest,
)
from google.cloud.discoveryengine_v1.types.grounded_generation_service import (
    CheckGroundingRequest,
    CheckGroundingResponse,
    CheckGroundingSpec,
    GenerateGroundedContentRequest,
    GenerateGroundedContentResponse,
    GroundedGenerationContent,
)
from google.cloud.discoveryengine_v1.types.grounding import FactChunk, GroundingFact
from google.cloud.discoveryengine_v1.types.import_config import (
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
from google.cloud.discoveryengine_v1.types.project import Project
from google.cloud.discoveryengine_v1.types.project_service import (
    ProvisionProjectMetadata,
    ProvisionProjectRequest,
)
from google.cloud.discoveryengine_v1.types.purge_config import (
    PurgeCompletionSuggestionsMetadata,
    PurgeCompletionSuggestionsRequest,
    PurgeCompletionSuggestionsResponse,
    PurgeDocumentsMetadata,
    PurgeDocumentsRequest,
    PurgeDocumentsResponse,
    PurgeErrorConfig,
    PurgeSuggestionDenyListEntriesMetadata,
    PurgeSuggestionDenyListEntriesRequest,
    PurgeSuggestionDenyListEntriesResponse,
    PurgeUserEventsMetadata,
    PurgeUserEventsRequest,
    PurgeUserEventsResponse,
)
from google.cloud.discoveryengine_v1.types.rank_service import (
    RankingRecord,
    RankRequest,
    RankResponse,
)
from google.cloud.discoveryengine_v1.types.recommendation_service import (
    RecommendRequest,
    RecommendResponse,
)
from google.cloud.discoveryengine_v1.types.safety import HarmCategory, SafetyRating
from google.cloud.discoveryengine_v1.types.schema import Schema
from google.cloud.discoveryengine_v1.types.schema_service import (
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
from google.cloud.discoveryengine_v1.types.search_service import (
    SearchRequest,
    SearchResponse,
)
from google.cloud.discoveryengine_v1.types.search_tuning_service import (
    ListCustomModelsRequest,
    ListCustomModelsResponse,
    TrainCustomModelMetadata,
    TrainCustomModelRequest,
    TrainCustomModelResponse,
)
from google.cloud.discoveryengine_v1.types.serving_config import ServingConfig
from google.cloud.discoveryengine_v1.types.serving_config_service import (
    UpdateServingConfigRequest,
)
from google.cloud.discoveryengine_v1.types.session import Query, Session
from google.cloud.discoveryengine_v1.types.site_search_engine import (
    Sitemap,
    SiteSearchEngine,
    SiteVerificationInfo,
    TargetSite,
)
from google.cloud.discoveryengine_v1.types.site_search_engine_service import (
    BatchCreateTargetSiteMetadata,
    BatchCreateTargetSitesRequest,
    BatchCreateTargetSitesResponse,
    BatchVerifyTargetSitesMetadata,
    BatchVerifyTargetSitesRequest,
    BatchVerifyTargetSitesResponse,
    CreateSitemapMetadata,
    CreateSitemapRequest,
    CreateTargetSiteMetadata,
    CreateTargetSiteRequest,
    DeleteSitemapMetadata,
    DeleteSitemapRequest,
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
    FetchSitemapsRequest,
    FetchSitemapsResponse,
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
from google.cloud.discoveryengine_v1.types.user_event import (
    CompletionInfo,
    DocumentInfo,
    MediaInfo,
    PageInfo,
    PanelInfo,
    SearchInfo,
    TransactionInfo,
    UserEvent,
)
from google.cloud.discoveryengine_v1.types.user_event_service import (
    CollectUserEventRequest,
    WriteUserEventRequest,
)

__all__ = (
    "CompletionServiceClient",
    "CompletionServiceAsyncClient",
    "ControlServiceClient",
    "ControlServiceAsyncClient",
    "ConversationalSearchServiceClient",
    "ConversationalSearchServiceAsyncClient",
    "DataStoreServiceClient",
    "DataStoreServiceAsyncClient",
    "DocumentServiceClient",
    "DocumentServiceAsyncClient",
    "EngineServiceClient",
    "EngineServiceAsyncClient",
    "GroundedGenerationServiceClient",
    "GroundedGenerationServiceAsyncClient",
    "ProjectServiceClient",
    "ProjectServiceAsyncClient",
    "RankServiceClient",
    "RankServiceAsyncClient",
    "RecommendationServiceClient",
    "RecommendationServiceAsyncClient",
    "SchemaServiceClient",
    "SchemaServiceAsyncClient",
    "SearchServiceClient",
    "SearchServiceAsyncClient",
    "SearchTuningServiceClient",
    "SearchTuningServiceAsyncClient",
    "ServingConfigServiceClient",
    "ServingConfigServiceAsyncClient",
    "SiteSearchEngineServiceClient",
    "SiteSearchEngineServiceAsyncClient",
    "UserEventServiceClient",
    "UserEventServiceAsyncClient",
    "Answer",
    "Chunk",
    "CustomAttribute",
    "DoubleList",
    "Interval",
    "SearchLinkPromotion",
    "UserInfo",
    "IndustryVertical",
    "SearchAddOn",
    "SearchTier",
    "SearchUseCase",
    "SolutionType",
    "CompletionSuggestion",
    "SuggestionDenyListEntry",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "Condition",
    "Control",
    "CreateControlRequest",
    "DeleteControlRequest",
    "GetControlRequest",
    "ListControlsRequest",
    "ListControlsResponse",
    "UpdateControlRequest",
    "Conversation",
    "ConversationContext",
    "ConversationMessage",
    "Reply",
    "TextInput",
    "AnswerQueryRequest",
    "AnswerQueryResponse",
    "ConverseConversationRequest",
    "ConverseConversationResponse",
    "CreateConversationRequest",
    "CreateSessionRequest",
    "DeleteConversationRequest",
    "DeleteSessionRequest",
    "GetAnswerRequest",
    "GetConversationRequest",
    "GetSessionRequest",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "ListSessionsRequest",
    "ListSessionsResponse",
    "UpdateConversationRequest",
    "UpdateSessionRequest",
    "CustomTuningModel",
    "AdvancedSiteSearchConfig",
    "DataStore",
    "WorkspaceConfig",
    "CreateDataStoreMetadata",
    "CreateDataStoreRequest",
    "DeleteDataStoreMetadata",
    "DeleteDataStoreRequest",
    "GetDataStoreRequest",
    "ListDataStoresRequest",
    "ListDataStoresResponse",
    "UpdateDataStoreRequest",
    "Document",
    "DocumentProcessingConfig",
    "BatchGetDocumentsMetadataRequest",
    "BatchGetDocumentsMetadataResponse",
    "CreateDocumentRequest",
    "DeleteDocumentRequest",
    "GetDocumentRequest",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "UpdateDocumentRequest",
    "Engine",
    "CreateEngineMetadata",
    "CreateEngineRequest",
    "DeleteEngineMetadata",
    "DeleteEngineRequest",
    "GetEngineRequest",
    "ListEnginesRequest",
    "ListEnginesResponse",
    "UpdateEngineRequest",
    "CheckGroundingRequest",
    "CheckGroundingResponse",
    "CheckGroundingSpec",
    "GenerateGroundedContentRequest",
    "GenerateGroundedContentResponse",
    "GroundedGenerationContent",
    "FactChunk",
    "GroundingFact",
    "AlloyDbSource",
    "BigQuerySource",
    "BigtableOptions",
    "BigtableSource",
    "CloudSqlSource",
    "FhirStoreSource",
    "FirestoreSource",
    "GcsSource",
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
    "SpannerSource",
    "Project",
    "ProvisionProjectMetadata",
    "ProvisionProjectRequest",
    "PurgeCompletionSuggestionsMetadata",
    "PurgeCompletionSuggestionsRequest",
    "PurgeCompletionSuggestionsResponse",
    "PurgeDocumentsMetadata",
    "PurgeDocumentsRequest",
    "PurgeDocumentsResponse",
    "PurgeErrorConfig",
    "PurgeSuggestionDenyListEntriesMetadata",
    "PurgeSuggestionDenyListEntriesRequest",
    "PurgeSuggestionDenyListEntriesResponse",
    "PurgeUserEventsMetadata",
    "PurgeUserEventsRequest",
    "PurgeUserEventsResponse",
    "RankingRecord",
    "RankRequest",
    "RankResponse",
    "RecommendRequest",
    "RecommendResponse",
    "SafetyRating",
    "HarmCategory",
    "Schema",
    "CreateSchemaMetadata",
    "CreateSchemaRequest",
    "DeleteSchemaMetadata",
    "DeleteSchemaRequest",
    "GetSchemaRequest",
    "ListSchemasRequest",
    "ListSchemasResponse",
    "UpdateSchemaMetadata",
    "UpdateSchemaRequest",
    "SearchRequest",
    "SearchResponse",
    "ListCustomModelsRequest",
    "ListCustomModelsResponse",
    "TrainCustomModelMetadata",
    "TrainCustomModelRequest",
    "TrainCustomModelResponse",
    "ServingConfig",
    "UpdateServingConfigRequest",
    "Query",
    "Session",
    "Sitemap",
    "SiteSearchEngine",
    "SiteVerificationInfo",
    "TargetSite",
    "BatchCreateTargetSiteMetadata",
    "BatchCreateTargetSitesRequest",
    "BatchCreateTargetSitesResponse",
    "BatchVerifyTargetSitesMetadata",
    "BatchVerifyTargetSitesRequest",
    "BatchVerifyTargetSitesResponse",
    "CreateSitemapMetadata",
    "CreateSitemapRequest",
    "CreateTargetSiteMetadata",
    "CreateTargetSiteRequest",
    "DeleteSitemapMetadata",
    "DeleteSitemapRequest",
    "DeleteTargetSiteMetadata",
    "DeleteTargetSiteRequest",
    "DisableAdvancedSiteSearchMetadata",
    "DisableAdvancedSiteSearchRequest",
    "DisableAdvancedSiteSearchResponse",
    "EnableAdvancedSiteSearchMetadata",
    "EnableAdvancedSiteSearchRequest",
    "EnableAdvancedSiteSearchResponse",
    "FetchDomainVerificationStatusRequest",
    "FetchDomainVerificationStatusResponse",
    "FetchSitemapsRequest",
    "FetchSitemapsResponse",
    "GetSiteSearchEngineRequest",
    "GetTargetSiteRequest",
    "ListTargetSitesRequest",
    "ListTargetSitesResponse",
    "RecrawlUrisMetadata",
    "RecrawlUrisRequest",
    "RecrawlUrisResponse",
    "UpdateTargetSiteMetadata",
    "UpdateTargetSiteRequest",
    "CompletionInfo",
    "DocumentInfo",
    "MediaInfo",
    "PageInfo",
    "PanelInfo",
    "SearchInfo",
    "TransactionInfo",
    "UserEvent",
    "CollectUserEventRequest",
    "WriteUserEventRequest",
)
