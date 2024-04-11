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
from google.cloud.discoveryengine_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.acl_config_service import (
    AclConfigServiceAsyncClient,
    AclConfigServiceClient,
)
from .services.chunk_service import ChunkServiceAsyncClient, ChunkServiceClient
from .services.completion_service import (
    CompletionServiceAsyncClient,
    CompletionServiceClient,
)
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
from .services.estimate_billing_service import (
    EstimateBillingServiceAsyncClient,
    EstimateBillingServiceClient,
)
from .services.recommendation_service import (
    RecommendationServiceAsyncClient,
    RecommendationServiceClient,
)
from .services.schema_service import SchemaServiceAsyncClient, SchemaServiceClient
from .services.search_service import SearchServiceAsyncClient, SearchServiceClient
from .services.search_tuning_service import (
    SearchTuningServiceAsyncClient,
    SearchTuningServiceClient,
)
from .services.serving_config_service import (
    ServingConfigServiceAsyncClient,
    ServingConfigServiceClient,
)
from .services.site_search_engine_service import (
    SiteSearchEngineServiceAsyncClient,
    SiteSearchEngineServiceClient,
)
from .services.user_event_service import (
    UserEventServiceAsyncClient,
    UserEventServiceClient,
)
from .types.acl_config import AclConfig
from .types.acl_config_service import GetAclConfigRequest, UpdateAclConfigRequest
from .types.chunk import Chunk
from .types.chunk_service import GetChunkRequest, ListChunksRequest, ListChunksResponse
from .types.common import (
    CustomAttribute,
    CustomFineTuningSpec,
    DoubleList,
    EmbeddingConfig,
    GuidedSearchSpec,
    IdpConfig,
    IndustryVertical,
    Interval,
    Principal,
    SearchAddOn,
    SearchTier,
    SolutionType,
    UserInfo,
)
from .types.completion import SuggestionDenyListEntry
from .types.completion_service import CompleteQueryRequest, CompleteQueryResponse
from .types.conversation import (
    Conversation,
    ConversationContext,
    ConversationMessage,
    Reply,
    TextInput,
)
from .types.conversational_search_service import (
    ConverseConversationRequest,
    ConverseConversationResponse,
    CreateConversationRequest,
    DeleteConversationRequest,
    GetConversationRequest,
    ListConversationsRequest,
    ListConversationsResponse,
    UpdateConversationRequest,
)
from .types.data_store import DataStore
from .types.data_store_service import (
    CreateDataStoreMetadata,
    CreateDataStoreRequest,
    DeleteDataStoreMetadata,
    DeleteDataStoreRequest,
    GetDataStoreRequest,
    GetDocumentProcessingConfigRequest,
    ListDataStoresRequest,
    ListDataStoresResponse,
    UpdateDataStoreRequest,
    UpdateDocumentProcessingConfigRequest,
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
    PauseEngineRequest,
    ResumeEngineRequest,
    TuneEngineMetadata,
    TuneEngineRequest,
    TuneEngineResponse,
    UpdateEngineRequest,
)
from .types.estimate_billing_service import (
    EstimateDataSizeMetadata,
    EstimateDataSizeRequest,
    EstimateDataSizeResponse,
)
from .types.import_config import (
    BigQuerySource,
    GcsSource,
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
)
from .types.purge_config import (
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
from .types.recommendation_service import RecommendRequest, RecommendResponse
from .types.schema import FieldConfig, Schema
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
from .types.search_tuning_service import (
    TrainCustomModelMetadata,
    TrainCustomModelRequest,
    TrainCustomModelResponse,
)
from .types.serving_config import ServingConfig
from .types.serving_config_service import (
    GetServingConfigRequest,
    ListServingConfigsRequest,
    ListServingConfigsResponse,
    UpdateServingConfigRequest,
)
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
    "AclConfigServiceAsyncClient",
    "ChunkServiceAsyncClient",
    "CompletionServiceAsyncClient",
    "ConversationalSearchServiceAsyncClient",
    "DataStoreServiceAsyncClient",
    "DocumentServiceAsyncClient",
    "EngineServiceAsyncClient",
    "EstimateBillingServiceAsyncClient",
    "RecommendationServiceAsyncClient",
    "SchemaServiceAsyncClient",
    "SearchServiceAsyncClient",
    "SearchTuningServiceAsyncClient",
    "ServingConfigServiceAsyncClient",
    "SiteSearchEngineServiceAsyncClient",
    "UserEventServiceAsyncClient",
    "AclConfig",
    "AclConfigServiceClient",
    "BatchCreateTargetSiteMetadata",
    "BatchCreateTargetSitesRequest",
    "BatchCreateTargetSitesResponse",
    "BatchVerifyTargetSitesMetadata",
    "BatchVerifyTargetSitesRequest",
    "BatchVerifyTargetSitesResponse",
    "BigQuerySource",
    "Chunk",
    "ChunkServiceClient",
    "CollectUserEventRequest",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "CompletionInfo",
    "CompletionServiceClient",
    "Conversation",
    "ConversationContext",
    "ConversationMessage",
    "ConversationalSearchServiceClient",
    "ConverseConversationRequest",
    "ConverseConversationResponse",
    "CreateConversationRequest",
    "CreateDataStoreMetadata",
    "CreateDataStoreRequest",
    "CreateDocumentRequest",
    "CreateEngineMetadata",
    "CreateEngineRequest",
    "CreateSchemaMetadata",
    "CreateSchemaRequest",
    "CreateTargetSiteMetadata",
    "CreateTargetSiteRequest",
    "CustomAttribute",
    "CustomFineTuningSpec",
    "DataStore",
    "DataStoreServiceClient",
    "DeleteConversationRequest",
    "DeleteDataStoreMetadata",
    "DeleteDataStoreRequest",
    "DeleteDocumentRequest",
    "DeleteEngineMetadata",
    "DeleteEngineRequest",
    "DeleteSchemaMetadata",
    "DeleteSchemaRequest",
    "DeleteTargetSiteMetadata",
    "DeleteTargetSiteRequest",
    "DisableAdvancedSiteSearchMetadata",
    "DisableAdvancedSiteSearchRequest",
    "DisableAdvancedSiteSearchResponse",
    "Document",
    "DocumentInfo",
    "DocumentProcessingConfig",
    "DocumentServiceClient",
    "DoubleList",
    "EmbeddingConfig",
    "EnableAdvancedSiteSearchMetadata",
    "EnableAdvancedSiteSearchRequest",
    "EnableAdvancedSiteSearchResponse",
    "Engine",
    "EngineServiceClient",
    "EstimateBillingServiceClient",
    "EstimateDataSizeMetadata",
    "EstimateDataSizeRequest",
    "EstimateDataSizeResponse",
    "FetchDomainVerificationStatusRequest",
    "FetchDomainVerificationStatusResponse",
    "FieldConfig",
    "GcsSource",
    "GetAclConfigRequest",
    "GetChunkRequest",
    "GetConversationRequest",
    "GetDataStoreRequest",
    "GetDocumentProcessingConfigRequest",
    "GetDocumentRequest",
    "GetEngineRequest",
    "GetSchemaRequest",
    "GetServingConfigRequest",
    "GetSiteSearchEngineRequest",
    "GetTargetSiteRequest",
    "GuidedSearchSpec",
    "IdpConfig",
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
    "ListChunksRequest",
    "ListChunksResponse",
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
    "ListServingConfigsRequest",
    "ListServingConfigsResponse",
    "ListTargetSitesRequest",
    "ListTargetSitesResponse",
    "MediaInfo",
    "PageInfo",
    "PanelInfo",
    "PauseEngineRequest",
    "Principal",
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
    "RecommendRequest",
    "RecommendResponse",
    "RecommendationServiceClient",
    "RecrawlUrisMetadata",
    "RecrawlUrisRequest",
    "RecrawlUrisResponse",
    "Reply",
    "ResumeEngineRequest",
    "Schema",
    "SchemaServiceClient",
    "SearchAddOn",
    "SearchInfo",
    "SearchRequest",
    "SearchResponse",
    "SearchServiceClient",
    "SearchTier",
    "SearchTuningServiceClient",
    "ServingConfig",
    "ServingConfigServiceClient",
    "SiteSearchEngine",
    "SiteSearchEngineServiceClient",
    "SiteVerificationInfo",
    "SolutionType",
    "SuggestionDenyListEntry",
    "TargetSite",
    "TextInput",
    "TrainCustomModelMetadata",
    "TrainCustomModelRequest",
    "TrainCustomModelResponse",
    "TransactionInfo",
    "TuneEngineMetadata",
    "TuneEngineRequest",
    "TuneEngineResponse",
    "UpdateAclConfigRequest",
    "UpdateConversationRequest",
    "UpdateDataStoreRequest",
    "UpdateDocumentProcessingConfigRequest",
    "UpdateDocumentRequest",
    "UpdateEngineRequest",
    "UpdateSchemaMetadata",
    "UpdateSchemaRequest",
    "UpdateServingConfigRequest",
    "UpdateTargetSiteMetadata",
    "UpdateTargetSiteRequest",
    "UserEvent",
    "UserEventServiceClient",
    "UserInfo",
    "WriteUserEventRequest",
)
