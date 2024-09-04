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


from google.cloud.discoveryengine_v1.services.completion_service.client import CompletionServiceClient
from google.cloud.discoveryengine_v1.services.completion_service.async_client import CompletionServiceAsyncClient
from google.cloud.discoveryengine_v1.services.control_service.client import ControlServiceClient
from google.cloud.discoveryengine_v1.services.control_service.async_client import ControlServiceAsyncClient
from google.cloud.discoveryengine_v1.services.conversational_search_service.client import ConversationalSearchServiceClient
from google.cloud.discoveryengine_v1.services.conversational_search_service.async_client import ConversationalSearchServiceAsyncClient
from google.cloud.discoveryengine_v1.services.data_store_service.client import DataStoreServiceClient
from google.cloud.discoveryengine_v1.services.data_store_service.async_client import DataStoreServiceAsyncClient
from google.cloud.discoveryengine_v1.services.document_service.client import DocumentServiceClient
from google.cloud.discoveryengine_v1.services.document_service.async_client import DocumentServiceAsyncClient
from google.cloud.discoveryengine_v1.services.engine_service.client import EngineServiceClient
from google.cloud.discoveryengine_v1.services.engine_service.async_client import EngineServiceAsyncClient
from google.cloud.discoveryengine_v1.services.grounded_generation_service.client import GroundedGenerationServiceClient
from google.cloud.discoveryengine_v1.services.grounded_generation_service.async_client import GroundedGenerationServiceAsyncClient
from google.cloud.discoveryengine_v1.services.project_service.client import ProjectServiceClient
from google.cloud.discoveryengine_v1.services.project_service.async_client import ProjectServiceAsyncClient
from google.cloud.discoveryengine_v1.services.rank_service.client import RankServiceClient
from google.cloud.discoveryengine_v1.services.rank_service.async_client import RankServiceAsyncClient
from google.cloud.discoveryengine_v1.services.recommendation_service.client import RecommendationServiceClient
from google.cloud.discoveryengine_v1.services.recommendation_service.async_client import RecommendationServiceAsyncClient
from google.cloud.discoveryengine_v1.services.schema_service.client import SchemaServiceClient
from google.cloud.discoveryengine_v1.services.schema_service.async_client import SchemaServiceAsyncClient
from google.cloud.discoveryengine_v1.services.search_service.client import SearchServiceClient
from google.cloud.discoveryengine_v1.services.search_service.async_client import SearchServiceAsyncClient
from google.cloud.discoveryengine_v1.services.site_search_engine_service.client import SiteSearchEngineServiceClient
from google.cloud.discoveryengine_v1.services.site_search_engine_service.async_client import SiteSearchEngineServiceAsyncClient
from google.cloud.discoveryengine_v1.services.user_event_service.client import UserEventServiceClient
from google.cloud.discoveryengine_v1.services.user_event_service.async_client import UserEventServiceAsyncClient

from google.cloud.discoveryengine_v1.types.answer import Answer
from google.cloud.discoveryengine_v1.types.chunk import Chunk
from google.cloud.discoveryengine_v1.types.common import CustomAttribute
from google.cloud.discoveryengine_v1.types.common import Interval
from google.cloud.discoveryengine_v1.types.common import UserInfo
from google.cloud.discoveryengine_v1.types.common import IndustryVertical
from google.cloud.discoveryengine_v1.types.common import SearchAddOn
from google.cloud.discoveryengine_v1.types.common import SearchTier
from google.cloud.discoveryengine_v1.types.common import SearchUseCase
from google.cloud.discoveryengine_v1.types.common import SolutionType
from google.cloud.discoveryengine_v1.types.completion import CompletionSuggestion
from google.cloud.discoveryengine_v1.types.completion import SuggestionDenyListEntry
from google.cloud.discoveryengine_v1.types.completion_service import CompleteQueryRequest
from google.cloud.discoveryengine_v1.types.completion_service import CompleteQueryResponse
from google.cloud.discoveryengine_v1.types.control import Condition
from google.cloud.discoveryengine_v1.types.control import Control
from google.cloud.discoveryengine_v1.types.control_service import CreateControlRequest
from google.cloud.discoveryengine_v1.types.control_service import DeleteControlRequest
from google.cloud.discoveryengine_v1.types.control_service import GetControlRequest
from google.cloud.discoveryengine_v1.types.control_service import ListControlsRequest
from google.cloud.discoveryengine_v1.types.control_service import ListControlsResponse
from google.cloud.discoveryengine_v1.types.control_service import UpdateControlRequest
from google.cloud.discoveryengine_v1.types.conversation import Conversation
from google.cloud.discoveryengine_v1.types.conversation import ConversationContext
from google.cloud.discoveryengine_v1.types.conversation import ConversationMessage
from google.cloud.discoveryengine_v1.types.conversation import Reply
from google.cloud.discoveryengine_v1.types.conversation import TextInput
from google.cloud.discoveryengine_v1.types.conversational_search_service import AnswerQueryRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import AnswerQueryResponse
from google.cloud.discoveryengine_v1.types.conversational_search_service import ConverseConversationRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import ConverseConversationResponse
from google.cloud.discoveryengine_v1.types.conversational_search_service import CreateConversationRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import CreateSessionRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import DeleteConversationRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import DeleteSessionRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import GetAnswerRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import GetConversationRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import GetSessionRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import ListConversationsRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import ListConversationsResponse
from google.cloud.discoveryengine_v1.types.conversational_search_service import ListSessionsRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import ListSessionsResponse
from google.cloud.discoveryengine_v1.types.conversational_search_service import UpdateConversationRequest
from google.cloud.discoveryengine_v1.types.conversational_search_service import UpdateSessionRequest
from google.cloud.discoveryengine_v1.types.data_store import DataStore
from google.cloud.discoveryengine_v1.types.data_store_service import CreateDataStoreMetadata
from google.cloud.discoveryengine_v1.types.data_store_service import CreateDataStoreRequest
from google.cloud.discoveryengine_v1.types.data_store_service import DeleteDataStoreMetadata
from google.cloud.discoveryengine_v1.types.data_store_service import DeleteDataStoreRequest
from google.cloud.discoveryengine_v1.types.data_store_service import GetDataStoreRequest
from google.cloud.discoveryengine_v1.types.data_store_service import ListDataStoresRequest
from google.cloud.discoveryengine_v1.types.data_store_service import ListDataStoresResponse
from google.cloud.discoveryengine_v1.types.data_store_service import UpdateDataStoreRequest
from google.cloud.discoveryengine_v1.types.document import Document
from google.cloud.discoveryengine_v1.types.document_processing_config import DocumentProcessingConfig
from google.cloud.discoveryengine_v1.types.document_service import CreateDocumentRequest
from google.cloud.discoveryengine_v1.types.document_service import DeleteDocumentRequest
from google.cloud.discoveryengine_v1.types.document_service import GetDocumentRequest
from google.cloud.discoveryengine_v1.types.document_service import ListDocumentsRequest
from google.cloud.discoveryengine_v1.types.document_service import ListDocumentsResponse
from google.cloud.discoveryengine_v1.types.document_service import UpdateDocumentRequest
from google.cloud.discoveryengine_v1.types.engine import Engine
from google.cloud.discoveryengine_v1.types.engine_service import CreateEngineMetadata
from google.cloud.discoveryengine_v1.types.engine_service import CreateEngineRequest
from google.cloud.discoveryengine_v1.types.engine_service import DeleteEngineMetadata
from google.cloud.discoveryengine_v1.types.engine_service import DeleteEngineRequest
from google.cloud.discoveryengine_v1.types.engine_service import GetEngineRequest
from google.cloud.discoveryengine_v1.types.engine_service import ListEnginesRequest
from google.cloud.discoveryengine_v1.types.engine_service import ListEnginesResponse
from google.cloud.discoveryengine_v1.types.engine_service import UpdateEngineRequest
from google.cloud.discoveryengine_v1.types.grounded_generation_service import CheckGroundingRequest
from google.cloud.discoveryengine_v1.types.grounded_generation_service import CheckGroundingResponse
from google.cloud.discoveryengine_v1.types.grounded_generation_service import CheckGroundingSpec
from google.cloud.discoveryengine_v1.types.grounding import FactChunk
from google.cloud.discoveryengine_v1.types.grounding import GroundingFact
from google.cloud.discoveryengine_v1.types.import_config import AlloyDbSource
from google.cloud.discoveryengine_v1.types.import_config import BigQuerySource
from google.cloud.discoveryengine_v1.types.import_config import BigtableOptions
from google.cloud.discoveryengine_v1.types.import_config import BigtableSource
from google.cloud.discoveryengine_v1.types.import_config import CloudSqlSource
from google.cloud.discoveryengine_v1.types.import_config import FhirStoreSource
from google.cloud.discoveryengine_v1.types.import_config import FirestoreSource
from google.cloud.discoveryengine_v1.types.import_config import GcsSource
from google.cloud.discoveryengine_v1.types.import_config import ImportCompletionSuggestionsMetadata
from google.cloud.discoveryengine_v1.types.import_config import ImportCompletionSuggestionsRequest
from google.cloud.discoveryengine_v1.types.import_config import ImportCompletionSuggestionsResponse
from google.cloud.discoveryengine_v1.types.import_config import ImportDocumentsMetadata
from google.cloud.discoveryengine_v1.types.import_config import ImportDocumentsRequest
from google.cloud.discoveryengine_v1.types.import_config import ImportDocumentsResponse
from google.cloud.discoveryengine_v1.types.import_config import ImportErrorConfig
from google.cloud.discoveryengine_v1.types.import_config import ImportSuggestionDenyListEntriesMetadata
from google.cloud.discoveryengine_v1.types.import_config import ImportSuggestionDenyListEntriesRequest
from google.cloud.discoveryengine_v1.types.import_config import ImportSuggestionDenyListEntriesResponse
from google.cloud.discoveryengine_v1.types.import_config import ImportUserEventsMetadata
from google.cloud.discoveryengine_v1.types.import_config import ImportUserEventsRequest
from google.cloud.discoveryengine_v1.types.import_config import ImportUserEventsResponse
from google.cloud.discoveryengine_v1.types.import_config import SpannerSource
from google.cloud.discoveryengine_v1.types.project import Project
from google.cloud.discoveryengine_v1.types.project_service import ProvisionProjectMetadata
from google.cloud.discoveryengine_v1.types.project_service import ProvisionProjectRequest
from google.cloud.discoveryengine_v1.types.purge_config import PurgeCompletionSuggestionsMetadata
from google.cloud.discoveryengine_v1.types.purge_config import PurgeCompletionSuggestionsRequest
from google.cloud.discoveryengine_v1.types.purge_config import PurgeCompletionSuggestionsResponse
from google.cloud.discoveryengine_v1.types.purge_config import PurgeDocumentsMetadata
from google.cloud.discoveryengine_v1.types.purge_config import PurgeDocumentsRequest
from google.cloud.discoveryengine_v1.types.purge_config import PurgeDocumentsResponse
from google.cloud.discoveryengine_v1.types.purge_config import PurgeSuggestionDenyListEntriesMetadata
from google.cloud.discoveryengine_v1.types.purge_config import PurgeSuggestionDenyListEntriesRequest
from google.cloud.discoveryengine_v1.types.purge_config import PurgeSuggestionDenyListEntriesResponse
from google.cloud.discoveryengine_v1.types.rank_service import RankingRecord
from google.cloud.discoveryengine_v1.types.rank_service import RankRequest
from google.cloud.discoveryengine_v1.types.rank_service import RankResponse
from google.cloud.discoveryengine_v1.types.recommendation_service import RecommendRequest
from google.cloud.discoveryengine_v1.types.recommendation_service import RecommendResponse
from google.cloud.discoveryengine_v1.types.schema import Schema
from google.cloud.discoveryengine_v1.types.schema_service import CreateSchemaMetadata
from google.cloud.discoveryengine_v1.types.schema_service import CreateSchemaRequest
from google.cloud.discoveryengine_v1.types.schema_service import DeleteSchemaMetadata
from google.cloud.discoveryengine_v1.types.schema_service import DeleteSchemaRequest
from google.cloud.discoveryengine_v1.types.schema_service import GetSchemaRequest
from google.cloud.discoveryengine_v1.types.schema_service import ListSchemasRequest
from google.cloud.discoveryengine_v1.types.schema_service import ListSchemasResponse
from google.cloud.discoveryengine_v1.types.schema_service import UpdateSchemaMetadata
from google.cloud.discoveryengine_v1.types.schema_service import UpdateSchemaRequest
from google.cloud.discoveryengine_v1.types.search_service import SearchRequest
from google.cloud.discoveryengine_v1.types.search_service import SearchResponse
from google.cloud.discoveryengine_v1.types.session import Query
from google.cloud.discoveryengine_v1.types.session import Session
from google.cloud.discoveryengine_v1.types.site_search_engine import SiteSearchEngine
from google.cloud.discoveryengine_v1.types.site_search_engine import SiteVerificationInfo
from google.cloud.discoveryengine_v1.types.site_search_engine import TargetSite
from google.cloud.discoveryengine_v1.types.site_search_engine_service import BatchCreateTargetSiteMetadata
from google.cloud.discoveryengine_v1.types.site_search_engine_service import BatchCreateTargetSitesRequest
from google.cloud.discoveryengine_v1.types.site_search_engine_service import BatchCreateTargetSitesResponse
from google.cloud.discoveryengine_v1.types.site_search_engine_service import BatchVerifyTargetSitesMetadata
from google.cloud.discoveryengine_v1.types.site_search_engine_service import BatchVerifyTargetSitesRequest
from google.cloud.discoveryengine_v1.types.site_search_engine_service import BatchVerifyTargetSitesResponse
from google.cloud.discoveryengine_v1.types.site_search_engine_service import CreateTargetSiteMetadata
from google.cloud.discoveryengine_v1.types.site_search_engine_service import CreateTargetSiteRequest
from google.cloud.discoveryengine_v1.types.site_search_engine_service import DeleteTargetSiteMetadata
from google.cloud.discoveryengine_v1.types.site_search_engine_service import DeleteTargetSiteRequest
from google.cloud.discoveryengine_v1.types.site_search_engine_service import DisableAdvancedSiteSearchMetadata
from google.cloud.discoveryengine_v1.types.site_search_engine_service import DisableAdvancedSiteSearchRequest
from google.cloud.discoveryengine_v1.types.site_search_engine_service import DisableAdvancedSiteSearchResponse
from google.cloud.discoveryengine_v1.types.site_search_engine_service import EnableAdvancedSiteSearchMetadata
from google.cloud.discoveryengine_v1.types.site_search_engine_service import EnableAdvancedSiteSearchRequest
from google.cloud.discoveryengine_v1.types.site_search_engine_service import EnableAdvancedSiteSearchResponse
from google.cloud.discoveryengine_v1.types.site_search_engine_service import FetchDomainVerificationStatusRequest
from google.cloud.discoveryengine_v1.types.site_search_engine_service import FetchDomainVerificationStatusResponse
from google.cloud.discoveryengine_v1.types.site_search_engine_service import GetSiteSearchEngineRequest
from google.cloud.discoveryengine_v1.types.site_search_engine_service import GetTargetSiteRequest
from google.cloud.discoveryengine_v1.types.site_search_engine_service import ListTargetSitesRequest
from google.cloud.discoveryengine_v1.types.site_search_engine_service import ListTargetSitesResponse
from google.cloud.discoveryengine_v1.types.site_search_engine_service import RecrawlUrisMetadata
from google.cloud.discoveryengine_v1.types.site_search_engine_service import RecrawlUrisRequest
from google.cloud.discoveryengine_v1.types.site_search_engine_service import RecrawlUrisResponse
from google.cloud.discoveryengine_v1.types.site_search_engine_service import UpdateTargetSiteMetadata
from google.cloud.discoveryengine_v1.types.site_search_engine_service import UpdateTargetSiteRequest
from google.cloud.discoveryengine_v1.types.user_event import CompletionInfo
from google.cloud.discoveryengine_v1.types.user_event import DocumentInfo
from google.cloud.discoveryengine_v1.types.user_event import MediaInfo
from google.cloud.discoveryengine_v1.types.user_event import PageInfo
from google.cloud.discoveryengine_v1.types.user_event import PanelInfo
from google.cloud.discoveryengine_v1.types.user_event import SearchInfo
from google.cloud.discoveryengine_v1.types.user_event import TransactionInfo
from google.cloud.discoveryengine_v1.types.user_event import UserEvent
from google.cloud.discoveryengine_v1.types.user_event_service import CollectUserEventRequest
from google.cloud.discoveryengine_v1.types.user_event_service import WriteUserEventRequest

__all__ = ('CompletionServiceClient',
    'CompletionServiceAsyncClient',
    'ControlServiceClient',
    'ControlServiceAsyncClient',
    'ConversationalSearchServiceClient',
    'ConversationalSearchServiceAsyncClient',
    'DataStoreServiceClient',
    'DataStoreServiceAsyncClient',
    'DocumentServiceClient',
    'DocumentServiceAsyncClient',
    'EngineServiceClient',
    'EngineServiceAsyncClient',
    'GroundedGenerationServiceClient',
    'GroundedGenerationServiceAsyncClient',
    'ProjectServiceClient',
    'ProjectServiceAsyncClient',
    'RankServiceClient',
    'RankServiceAsyncClient',
    'RecommendationServiceClient',
    'RecommendationServiceAsyncClient',
    'SchemaServiceClient',
    'SchemaServiceAsyncClient',
    'SearchServiceClient',
    'SearchServiceAsyncClient',
    'SiteSearchEngineServiceClient',
    'SiteSearchEngineServiceAsyncClient',
    'UserEventServiceClient',
    'UserEventServiceAsyncClient',
    'Answer',
    'Chunk',
    'CustomAttribute',
    'Interval',
    'UserInfo',
    'IndustryVertical',
    'SearchAddOn',
    'SearchTier',
    'SearchUseCase',
    'SolutionType',
    'CompletionSuggestion',
    'SuggestionDenyListEntry',
    'CompleteQueryRequest',
    'CompleteQueryResponse',
    'Condition',
    'Control',
    'CreateControlRequest',
    'DeleteControlRequest',
    'GetControlRequest',
    'ListControlsRequest',
    'ListControlsResponse',
    'UpdateControlRequest',
    'Conversation',
    'ConversationContext',
    'ConversationMessage',
    'Reply',
    'TextInput',
    'AnswerQueryRequest',
    'AnswerQueryResponse',
    'ConverseConversationRequest',
    'ConverseConversationResponse',
    'CreateConversationRequest',
    'CreateSessionRequest',
    'DeleteConversationRequest',
    'DeleteSessionRequest',
    'GetAnswerRequest',
    'GetConversationRequest',
    'GetSessionRequest',
    'ListConversationsRequest',
    'ListConversationsResponse',
    'ListSessionsRequest',
    'ListSessionsResponse',
    'UpdateConversationRequest',
    'UpdateSessionRequest',
    'DataStore',
    'CreateDataStoreMetadata',
    'CreateDataStoreRequest',
    'DeleteDataStoreMetadata',
    'DeleteDataStoreRequest',
    'GetDataStoreRequest',
    'ListDataStoresRequest',
    'ListDataStoresResponse',
    'UpdateDataStoreRequest',
    'Document',
    'DocumentProcessingConfig',
    'CreateDocumentRequest',
    'DeleteDocumentRequest',
    'GetDocumentRequest',
    'ListDocumentsRequest',
    'ListDocumentsResponse',
    'UpdateDocumentRequest',
    'Engine',
    'CreateEngineMetadata',
    'CreateEngineRequest',
    'DeleteEngineMetadata',
    'DeleteEngineRequest',
    'GetEngineRequest',
    'ListEnginesRequest',
    'ListEnginesResponse',
    'UpdateEngineRequest',
    'CheckGroundingRequest',
    'CheckGroundingResponse',
    'CheckGroundingSpec',
    'FactChunk',
    'GroundingFact',
    'AlloyDbSource',
    'BigQuerySource',
    'BigtableOptions',
    'BigtableSource',
    'CloudSqlSource',
    'FhirStoreSource',
    'FirestoreSource',
    'GcsSource',
    'ImportCompletionSuggestionsMetadata',
    'ImportCompletionSuggestionsRequest',
    'ImportCompletionSuggestionsResponse',
    'ImportDocumentsMetadata',
    'ImportDocumentsRequest',
    'ImportDocumentsResponse',
    'ImportErrorConfig',
    'ImportSuggestionDenyListEntriesMetadata',
    'ImportSuggestionDenyListEntriesRequest',
    'ImportSuggestionDenyListEntriesResponse',
    'ImportUserEventsMetadata',
    'ImportUserEventsRequest',
    'ImportUserEventsResponse',
    'SpannerSource',
    'Project',
    'ProvisionProjectMetadata',
    'ProvisionProjectRequest',
    'PurgeCompletionSuggestionsMetadata',
    'PurgeCompletionSuggestionsRequest',
    'PurgeCompletionSuggestionsResponse',
    'PurgeDocumentsMetadata',
    'PurgeDocumentsRequest',
    'PurgeDocumentsResponse',
    'PurgeSuggestionDenyListEntriesMetadata',
    'PurgeSuggestionDenyListEntriesRequest',
    'PurgeSuggestionDenyListEntriesResponse',
    'RankingRecord',
    'RankRequest',
    'RankResponse',
    'RecommendRequest',
    'RecommendResponse',
    'Schema',
    'CreateSchemaMetadata',
    'CreateSchemaRequest',
    'DeleteSchemaMetadata',
    'DeleteSchemaRequest',
    'GetSchemaRequest',
    'ListSchemasRequest',
    'ListSchemasResponse',
    'UpdateSchemaMetadata',
    'UpdateSchemaRequest',
    'SearchRequest',
    'SearchResponse',
    'Query',
    'Session',
    'SiteSearchEngine',
    'SiteVerificationInfo',
    'TargetSite',
    'BatchCreateTargetSiteMetadata',
    'BatchCreateTargetSitesRequest',
    'BatchCreateTargetSitesResponse',
    'BatchVerifyTargetSitesMetadata',
    'BatchVerifyTargetSitesRequest',
    'BatchVerifyTargetSitesResponse',
    'CreateTargetSiteMetadata',
    'CreateTargetSiteRequest',
    'DeleteTargetSiteMetadata',
    'DeleteTargetSiteRequest',
    'DisableAdvancedSiteSearchMetadata',
    'DisableAdvancedSiteSearchRequest',
    'DisableAdvancedSiteSearchResponse',
    'EnableAdvancedSiteSearchMetadata',
    'EnableAdvancedSiteSearchRequest',
    'EnableAdvancedSiteSearchResponse',
    'FetchDomainVerificationStatusRequest',
    'FetchDomainVerificationStatusResponse',
    'GetSiteSearchEngineRequest',
    'GetTargetSiteRequest',
    'ListTargetSitesRequest',
    'ListTargetSitesResponse',
    'RecrawlUrisMetadata',
    'RecrawlUrisRequest',
    'RecrawlUrisResponse',
    'UpdateTargetSiteMetadata',
    'UpdateTargetSiteRequest',
    'CompletionInfo',
    'DocumentInfo',
    'MediaInfo',
    'PageInfo',
    'PanelInfo',
    'SearchInfo',
    'TransactionInfo',
    'UserEvent',
    'CollectUserEventRequest',
    'WriteUserEventRequest',
)
