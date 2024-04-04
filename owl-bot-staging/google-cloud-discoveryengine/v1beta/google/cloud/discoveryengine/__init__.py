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


from google.cloud.discoveryengine_v1beta.services.completion_service.client import CompletionServiceClient
from google.cloud.discoveryengine_v1beta.services.completion_service.async_client import CompletionServiceAsyncClient
from google.cloud.discoveryengine_v1beta.services.conversational_search_service.client import ConversationalSearchServiceClient
from google.cloud.discoveryengine_v1beta.services.conversational_search_service.async_client import ConversationalSearchServiceAsyncClient
from google.cloud.discoveryengine_v1beta.services.data_store_service.client import DataStoreServiceClient
from google.cloud.discoveryengine_v1beta.services.data_store_service.async_client import DataStoreServiceAsyncClient
from google.cloud.discoveryengine_v1beta.services.document_service.client import DocumentServiceClient
from google.cloud.discoveryengine_v1beta.services.document_service.async_client import DocumentServiceAsyncClient
from google.cloud.discoveryengine_v1beta.services.engine_service.client import EngineServiceClient
from google.cloud.discoveryengine_v1beta.services.engine_service.async_client import EngineServiceAsyncClient
from google.cloud.discoveryengine_v1beta.services.recommendation_service.client import RecommendationServiceClient
from google.cloud.discoveryengine_v1beta.services.recommendation_service.async_client import RecommendationServiceAsyncClient
from google.cloud.discoveryengine_v1beta.services.schema_service.client import SchemaServiceClient
from google.cloud.discoveryengine_v1beta.services.schema_service.async_client import SchemaServiceAsyncClient
from google.cloud.discoveryengine_v1beta.services.search_service.client import SearchServiceClient
from google.cloud.discoveryengine_v1beta.services.search_service.async_client import SearchServiceAsyncClient
from google.cloud.discoveryengine_v1beta.services.search_tuning_service.client import SearchTuningServiceClient
from google.cloud.discoveryengine_v1beta.services.search_tuning_service.async_client import SearchTuningServiceAsyncClient
from google.cloud.discoveryengine_v1beta.services.serving_config_service.client import ServingConfigServiceClient
from google.cloud.discoveryengine_v1beta.services.serving_config_service.async_client import ServingConfigServiceAsyncClient
from google.cloud.discoveryengine_v1beta.services.site_search_engine_service.client import SiteSearchEngineServiceClient
from google.cloud.discoveryengine_v1beta.services.site_search_engine_service.async_client import SiteSearchEngineServiceAsyncClient
from google.cloud.discoveryengine_v1beta.services.user_event_service.client import UserEventServiceClient
from google.cloud.discoveryengine_v1beta.services.user_event_service.async_client import UserEventServiceAsyncClient

from google.cloud.discoveryengine_v1beta.types.common import CustomAttribute
from google.cloud.discoveryengine_v1beta.types.common import DoubleList
from google.cloud.discoveryengine_v1beta.types.common import EmbeddingConfig
from google.cloud.discoveryengine_v1beta.types.common import Interval
from google.cloud.discoveryengine_v1beta.types.common import UserInfo
from google.cloud.discoveryengine_v1beta.types.common import IndustryVertical
from google.cloud.discoveryengine_v1beta.types.common import SearchAddOn
from google.cloud.discoveryengine_v1beta.types.common import SearchTier
from google.cloud.discoveryengine_v1beta.types.common import SolutionType
from google.cloud.discoveryengine_v1beta.types.completion import SuggestionDenyListEntry
from google.cloud.discoveryengine_v1beta.types.completion_service import CompleteQueryRequest
from google.cloud.discoveryengine_v1beta.types.completion_service import CompleteQueryResponse
from google.cloud.discoveryengine_v1beta.types.conversation import Conversation
from google.cloud.discoveryengine_v1beta.types.conversation import ConversationContext
from google.cloud.discoveryengine_v1beta.types.conversation import ConversationMessage
from google.cloud.discoveryengine_v1beta.types.conversation import Reply
from google.cloud.discoveryengine_v1beta.types.conversation import TextInput
from google.cloud.discoveryengine_v1beta.types.conversational_search_service import ConverseConversationRequest
from google.cloud.discoveryengine_v1beta.types.conversational_search_service import ConverseConversationResponse
from google.cloud.discoveryengine_v1beta.types.conversational_search_service import CreateConversationRequest
from google.cloud.discoveryengine_v1beta.types.conversational_search_service import DeleteConversationRequest
from google.cloud.discoveryengine_v1beta.types.conversational_search_service import GetConversationRequest
from google.cloud.discoveryengine_v1beta.types.conversational_search_service import ListConversationsRequest
from google.cloud.discoveryengine_v1beta.types.conversational_search_service import ListConversationsResponse
from google.cloud.discoveryengine_v1beta.types.conversational_search_service import UpdateConversationRequest
from google.cloud.discoveryengine_v1beta.types.data_store import DataStore
from google.cloud.discoveryengine_v1beta.types.data_store_service import CreateDataStoreMetadata
from google.cloud.discoveryengine_v1beta.types.data_store_service import CreateDataStoreRequest
from google.cloud.discoveryengine_v1beta.types.data_store_service import DeleteDataStoreMetadata
from google.cloud.discoveryengine_v1beta.types.data_store_service import DeleteDataStoreRequest
from google.cloud.discoveryengine_v1beta.types.data_store_service import GetDataStoreRequest
from google.cloud.discoveryengine_v1beta.types.data_store_service import ListDataStoresRequest
from google.cloud.discoveryengine_v1beta.types.data_store_service import ListDataStoresResponse
from google.cloud.discoveryengine_v1beta.types.data_store_service import UpdateDataStoreRequest
from google.cloud.discoveryengine_v1beta.types.document import Document
from google.cloud.discoveryengine_v1beta.types.document_processing_config import DocumentProcessingConfig
from google.cloud.discoveryengine_v1beta.types.document_service import CreateDocumentRequest
from google.cloud.discoveryengine_v1beta.types.document_service import DeleteDocumentRequest
from google.cloud.discoveryengine_v1beta.types.document_service import GetDocumentRequest
from google.cloud.discoveryengine_v1beta.types.document_service import ListDocumentsRequest
from google.cloud.discoveryengine_v1beta.types.document_service import ListDocumentsResponse
from google.cloud.discoveryengine_v1beta.types.document_service import UpdateDocumentRequest
from google.cloud.discoveryengine_v1beta.types.engine import Engine
from google.cloud.discoveryengine_v1beta.types.engine_service import CreateEngineMetadata
from google.cloud.discoveryengine_v1beta.types.engine_service import CreateEngineRequest
from google.cloud.discoveryengine_v1beta.types.engine_service import DeleteEngineMetadata
from google.cloud.discoveryengine_v1beta.types.engine_service import DeleteEngineRequest
from google.cloud.discoveryengine_v1beta.types.engine_service import GetEngineRequest
from google.cloud.discoveryengine_v1beta.types.engine_service import ListEnginesRequest
from google.cloud.discoveryengine_v1beta.types.engine_service import ListEnginesResponse
from google.cloud.discoveryengine_v1beta.types.engine_service import UpdateEngineRequest
from google.cloud.discoveryengine_v1beta.types.import_config import BigQuerySource
from google.cloud.discoveryengine_v1beta.types.import_config import GcsSource
from google.cloud.discoveryengine_v1beta.types.import_config import ImportDocumentsMetadata
from google.cloud.discoveryengine_v1beta.types.import_config import ImportDocumentsRequest
from google.cloud.discoveryengine_v1beta.types.import_config import ImportDocumentsResponse
from google.cloud.discoveryengine_v1beta.types.import_config import ImportErrorConfig
from google.cloud.discoveryengine_v1beta.types.import_config import ImportSuggestionDenyListEntriesMetadata
from google.cloud.discoveryengine_v1beta.types.import_config import ImportSuggestionDenyListEntriesRequest
from google.cloud.discoveryengine_v1beta.types.import_config import ImportSuggestionDenyListEntriesResponse
from google.cloud.discoveryengine_v1beta.types.import_config import ImportUserEventsMetadata
from google.cloud.discoveryengine_v1beta.types.import_config import ImportUserEventsRequest
from google.cloud.discoveryengine_v1beta.types.import_config import ImportUserEventsResponse
from google.cloud.discoveryengine_v1beta.types.purge_config import PurgeDocumentsMetadata
from google.cloud.discoveryengine_v1beta.types.purge_config import PurgeDocumentsRequest
from google.cloud.discoveryengine_v1beta.types.purge_config import PurgeDocumentsResponse
from google.cloud.discoveryengine_v1beta.types.purge_config import PurgeSuggestionDenyListEntriesMetadata
from google.cloud.discoveryengine_v1beta.types.purge_config import PurgeSuggestionDenyListEntriesRequest
from google.cloud.discoveryengine_v1beta.types.purge_config import PurgeSuggestionDenyListEntriesResponse
from google.cloud.discoveryengine_v1beta.types.recommendation_service import RecommendRequest
from google.cloud.discoveryengine_v1beta.types.recommendation_service import RecommendResponse
from google.cloud.discoveryengine_v1beta.types.schema import Schema
from google.cloud.discoveryengine_v1beta.types.schema_service import CreateSchemaMetadata
from google.cloud.discoveryengine_v1beta.types.schema_service import CreateSchemaRequest
from google.cloud.discoveryengine_v1beta.types.schema_service import DeleteSchemaMetadata
from google.cloud.discoveryengine_v1beta.types.schema_service import DeleteSchemaRequest
from google.cloud.discoveryengine_v1beta.types.schema_service import GetSchemaRequest
from google.cloud.discoveryengine_v1beta.types.schema_service import ListSchemasRequest
from google.cloud.discoveryengine_v1beta.types.schema_service import ListSchemasResponse
from google.cloud.discoveryengine_v1beta.types.schema_service import UpdateSchemaMetadata
from google.cloud.discoveryengine_v1beta.types.schema_service import UpdateSchemaRequest
from google.cloud.discoveryengine_v1beta.types.search_service import SearchRequest
from google.cloud.discoveryengine_v1beta.types.search_service import SearchResponse
from google.cloud.discoveryengine_v1beta.types.search_tuning_service import TrainCustomModelMetadata
from google.cloud.discoveryengine_v1beta.types.search_tuning_service import TrainCustomModelRequest
from google.cloud.discoveryengine_v1beta.types.search_tuning_service import TrainCustomModelResponse
from google.cloud.discoveryengine_v1beta.types.serving_config import ServingConfig
from google.cloud.discoveryengine_v1beta.types.serving_config_service import GetServingConfigRequest
from google.cloud.discoveryengine_v1beta.types.serving_config_service import ListServingConfigsRequest
from google.cloud.discoveryengine_v1beta.types.serving_config_service import ListServingConfigsResponse
from google.cloud.discoveryengine_v1beta.types.serving_config_service import UpdateServingConfigRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine import SiteSearchEngine
from google.cloud.discoveryengine_v1beta.types.site_search_engine import SiteVerificationInfo
from google.cloud.discoveryengine_v1beta.types.site_search_engine import TargetSite
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import BatchCreateTargetSiteMetadata
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import BatchCreateTargetSitesRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import BatchCreateTargetSitesResponse
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import BatchVerifyTargetSitesMetadata
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import BatchVerifyTargetSitesRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import BatchVerifyTargetSitesResponse
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import CreateTargetSiteMetadata
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import CreateTargetSiteRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import DeleteTargetSiteMetadata
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import DeleteTargetSiteRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import DisableAdvancedSiteSearchMetadata
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import DisableAdvancedSiteSearchRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import DisableAdvancedSiteSearchResponse
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import EnableAdvancedSiteSearchMetadata
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import EnableAdvancedSiteSearchRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import EnableAdvancedSiteSearchResponse
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import FetchDomainVerificationStatusRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import FetchDomainVerificationStatusResponse
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import GetSiteSearchEngineRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import GetTargetSiteRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import ListTargetSitesRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import ListTargetSitesResponse
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import RecrawlUrisMetadata
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import RecrawlUrisRequest
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import RecrawlUrisResponse
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import UpdateTargetSiteMetadata
from google.cloud.discoveryengine_v1beta.types.site_search_engine_service import UpdateTargetSiteRequest
from google.cloud.discoveryengine_v1beta.types.user_event import CompletionInfo
from google.cloud.discoveryengine_v1beta.types.user_event import DocumentInfo
from google.cloud.discoveryengine_v1beta.types.user_event import MediaInfo
from google.cloud.discoveryengine_v1beta.types.user_event import PageInfo
from google.cloud.discoveryengine_v1beta.types.user_event import PanelInfo
from google.cloud.discoveryengine_v1beta.types.user_event import SearchInfo
from google.cloud.discoveryengine_v1beta.types.user_event import TransactionInfo
from google.cloud.discoveryengine_v1beta.types.user_event import UserEvent
from google.cloud.discoveryengine_v1beta.types.user_event_service import CollectUserEventRequest
from google.cloud.discoveryengine_v1beta.types.user_event_service import WriteUserEventRequest

__all__ = ('CompletionServiceClient',
    'CompletionServiceAsyncClient',
    'ConversationalSearchServiceClient',
    'ConversationalSearchServiceAsyncClient',
    'DataStoreServiceClient',
    'DataStoreServiceAsyncClient',
    'DocumentServiceClient',
    'DocumentServiceAsyncClient',
    'EngineServiceClient',
    'EngineServiceAsyncClient',
    'RecommendationServiceClient',
    'RecommendationServiceAsyncClient',
    'SchemaServiceClient',
    'SchemaServiceAsyncClient',
    'SearchServiceClient',
    'SearchServiceAsyncClient',
    'SearchTuningServiceClient',
    'SearchTuningServiceAsyncClient',
    'ServingConfigServiceClient',
    'ServingConfigServiceAsyncClient',
    'SiteSearchEngineServiceClient',
    'SiteSearchEngineServiceAsyncClient',
    'UserEventServiceClient',
    'UserEventServiceAsyncClient',
    'CustomAttribute',
    'DoubleList',
    'EmbeddingConfig',
    'Interval',
    'UserInfo',
    'IndustryVertical',
    'SearchAddOn',
    'SearchTier',
    'SolutionType',
    'SuggestionDenyListEntry',
    'CompleteQueryRequest',
    'CompleteQueryResponse',
    'Conversation',
    'ConversationContext',
    'ConversationMessage',
    'Reply',
    'TextInput',
    'ConverseConversationRequest',
    'ConverseConversationResponse',
    'CreateConversationRequest',
    'DeleteConversationRequest',
    'GetConversationRequest',
    'ListConversationsRequest',
    'ListConversationsResponse',
    'UpdateConversationRequest',
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
    'BigQuerySource',
    'GcsSource',
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
    'PurgeDocumentsMetadata',
    'PurgeDocumentsRequest',
    'PurgeDocumentsResponse',
    'PurgeSuggestionDenyListEntriesMetadata',
    'PurgeSuggestionDenyListEntriesRequest',
    'PurgeSuggestionDenyListEntriesResponse',
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
    'TrainCustomModelMetadata',
    'TrainCustomModelRequest',
    'TrainCustomModelResponse',
    'ServingConfig',
    'GetServingConfigRequest',
    'ListServingConfigsRequest',
    'ListServingConfigsResponse',
    'UpdateServingConfigRequest',
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
