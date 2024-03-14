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
from google.cloud.discoveryengine import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.discoveryengine_v1beta.services.completion_service.async_client import (
    CompletionServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.completion_service.client import (
    CompletionServiceClient,
)
from google.cloud.discoveryengine_v1beta.services.conversational_search_service.async_client import (
    ConversationalSearchServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.conversational_search_service.client import (
    ConversationalSearchServiceClient,
)
from google.cloud.discoveryengine_v1beta.services.data_store_service.async_client import (
    DataStoreServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.data_store_service.client import (
    DataStoreServiceClient,
)
from google.cloud.discoveryengine_v1beta.services.document_service.async_client import (
    DocumentServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.document_service.client import (
    DocumentServiceClient,
)
from google.cloud.discoveryengine_v1beta.services.engine_service.async_client import (
    EngineServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.engine_service.client import (
    EngineServiceClient,
)
from google.cloud.discoveryengine_v1beta.services.recommendation_service.async_client import (
    RecommendationServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.recommendation_service.client import (
    RecommendationServiceClient,
)
from google.cloud.discoveryengine_v1beta.services.schema_service.async_client import (
    SchemaServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.schema_service.client import (
    SchemaServiceClient,
)
from google.cloud.discoveryengine_v1beta.services.search_service.async_client import (
    SearchServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.search_service.client import (
    SearchServiceClient,
)
from google.cloud.discoveryengine_v1beta.services.search_tuning_service.async_client import (
    SearchTuningServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.search_tuning_service.client import (
    SearchTuningServiceClient,
)
from google.cloud.discoveryengine_v1beta.services.serving_config_service.async_client import (
    ServingConfigServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.serving_config_service.client import (
    ServingConfigServiceClient,
)
from google.cloud.discoveryengine_v1beta.services.site_search_engine_service.async_client import (
    SiteSearchEngineServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.site_search_engine_service.client import (
    SiteSearchEngineServiceClient,
)
from google.cloud.discoveryengine_v1beta.services.user_event_service.async_client import (
    UserEventServiceAsyncClient,
)
from google.cloud.discoveryengine_v1beta.services.user_event_service.client import (
    UserEventServiceClient,
)
from google.cloud.discoveryengine_v1beta.types.common import (
    CustomAttribute,
    DoubleList,
    EmbeddingConfig,
    IndustryVertical,
    Interval,
    SearchAddOn,
    SearchTier,
    SolutionType,
    UserInfo,
)
from google.cloud.discoveryengine_v1beta.types.completion import SuggestionDenyListEntry
from google.cloud.discoveryengine_v1beta.types.completion_service import (
    CompleteQueryRequest,
    CompleteQueryResponse,
)
from google.cloud.discoveryengine_v1beta.types.conversation import (
    Conversation,
    ConversationContext,
    ConversationMessage,
    Reply,
    TextInput,
)
from google.cloud.discoveryengine_v1beta.types.conversational_search_service import (
    ConverseConversationRequest,
    ConverseConversationResponse,
    CreateConversationRequest,
    DeleteConversationRequest,
    GetConversationRequest,
    ListConversationsRequest,
    ListConversationsResponse,
    UpdateConversationRequest,
)
from google.cloud.discoveryengine_v1beta.types.data_store import DataStore
from google.cloud.discoveryengine_v1beta.types.data_store_service import (
    CreateDataStoreMetadata,
    CreateDataStoreRequest,
    DeleteDataStoreMetadata,
    DeleteDataStoreRequest,
    GetDataStoreRequest,
    ListDataStoresRequest,
    ListDataStoresResponse,
    UpdateDataStoreRequest,
)
from google.cloud.discoveryengine_v1beta.types.document import Document
from google.cloud.discoveryengine_v1beta.types.document_processing_config import (
    DocumentProcessingConfig,
)
from google.cloud.discoveryengine_v1beta.types.document_service import (
    CreateDocumentRequest,
    DeleteDocumentRequest,
    GetDocumentRequest,
    ListDocumentsRequest,
    ListDocumentsResponse,
    UpdateDocumentRequest,
)
from google.cloud.discoveryengine_v1beta.types.engine import Engine
from google.cloud.discoveryengine_v1beta.types.engine_service import (
    CreateEngineMetadata,
    CreateEngineRequest,
    DeleteEngineMetadata,
    DeleteEngineRequest,
    GetEngineRequest,
    ListEnginesRequest,
    ListEnginesResponse,
    UpdateEngineRequest,
)
from google.cloud.discoveryengine_v1beta.types.import_config import (
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
from google.cloud.discoveryengine_v1beta.types.purge_config import (
    PurgeDocumentsMetadata,
    PurgeDocumentsRequest,
    PurgeDocumentsResponse,
    PurgeSuggestionDenyListEntriesMetadata,
    PurgeSuggestionDenyListEntriesRequest,
    PurgeSuggestionDenyListEntriesResponse,
)
from google.cloud.discoveryengine_v1beta.types.recommendation_service import (
    RecommendRequest,
    RecommendResponse,
)
from google.cloud.discoveryengine_v1beta.types.schema import Schema
from google.cloud.discoveryengine_v1beta.types.schema_service import (
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
from google.cloud.discoveryengine_v1beta.types.search_service import (
    SearchRequest,
    SearchResponse,
)
from google.cloud.discoveryengine_v1beta.types.search_tuning_service import (
    TrainCustomModelMetadata,
    TrainCustomModelRequest,
    TrainCustomModelResponse,
)
from google.cloud.discoveryengine_v1beta.types.serving_config import ServingConfig
from google.cloud.discoveryengine_v1beta.types.serving_config_service import (
    GetServingConfigRequest,
    ListServingConfigsRequest,
    ListServingConfigsResponse,
    UpdateServingConfigRequest,
)
from google.cloud.discoveryengine_v1beta.types.site_search_engine import (
    SiteSearchEngine,
    SiteVerificationInfo,
    TargetSite,
)
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import (
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
from google.cloud.discoveryengine_v1beta.types.user_event import (
    CompletionInfo,
    DocumentInfo,
    MediaInfo,
    PageInfo,
    PanelInfo,
    SearchInfo,
    TransactionInfo,
    UserEvent,
)
from google.cloud.discoveryengine_v1beta.types.user_event_service import (
    CollectUserEventRequest,
    WriteUserEventRequest,
)

__all__ = (
    "CompletionServiceClient",
    "CompletionServiceAsyncClient",
    "ConversationalSearchServiceClient",
    "ConversationalSearchServiceAsyncClient",
    "DataStoreServiceClient",
    "DataStoreServiceAsyncClient",
    "DocumentServiceClient",
    "DocumentServiceAsyncClient",
    "EngineServiceClient",
    "EngineServiceAsyncClient",
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
    "CustomAttribute",
    "DoubleList",
    "EmbeddingConfig",
    "Interval",
    "UserInfo",
    "IndustryVertical",
    "SearchAddOn",
    "SearchTier",
    "SolutionType",
    "SuggestionDenyListEntry",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "Conversation",
    "ConversationContext",
    "ConversationMessage",
    "Reply",
    "TextInput",
    "ConverseConversationRequest",
    "ConverseConversationResponse",
    "CreateConversationRequest",
    "DeleteConversationRequest",
    "GetConversationRequest",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "UpdateConversationRequest",
    "DataStore",
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
    "BigQuerySource",
    "GcsSource",
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
    "PurgeDocumentsMetadata",
    "PurgeDocumentsRequest",
    "PurgeDocumentsResponse",
    "PurgeSuggestionDenyListEntriesMetadata",
    "PurgeSuggestionDenyListEntriesRequest",
    "PurgeSuggestionDenyListEntriesResponse",
    "RecommendRequest",
    "RecommendResponse",
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
    "TrainCustomModelMetadata",
    "TrainCustomModelRequest",
    "TrainCustomModelResponse",
    "ServingConfig",
    "GetServingConfigRequest",
    "ListServingConfigsRequest",
    "ListServingConfigsResponse",
    "UpdateServingConfigRequest",
    "SiteSearchEngine",
    "SiteVerificationInfo",
    "TargetSite",
    "BatchCreateTargetSiteMetadata",
    "BatchCreateTargetSitesRequest",
    "BatchCreateTargetSitesResponse",
    "BatchVerifyTargetSitesMetadata",
    "BatchVerifyTargetSitesRequest",
    "BatchVerifyTargetSitesResponse",
    "CreateTargetSiteMetadata",
    "CreateTargetSiteRequest",
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
