# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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


from .services.completion_service import CompletionServiceClient
from .services.completion_service import CompletionServiceAsyncClient
from .services.conversational_search_service import ConversationalSearchServiceClient
from .services.conversational_search_service import ConversationalSearchServiceAsyncClient
from .services.data_store_service import DataStoreServiceClient
from .services.data_store_service import DataStoreServiceAsyncClient
from .services.document_service import DocumentServiceClient
from .services.document_service import DocumentServiceAsyncClient
from .services.engine_service import EngineServiceClient
from .services.engine_service import EngineServiceAsyncClient
from .services.recommendation_service import RecommendationServiceClient
from .services.recommendation_service import RecommendationServiceAsyncClient
from .services.schema_service import SchemaServiceClient
from .services.schema_service import SchemaServiceAsyncClient
from .services.search_service import SearchServiceClient
from .services.search_service import SearchServiceAsyncClient
from .services.site_search_engine_service import SiteSearchEngineServiceClient
from .services.site_search_engine_service import SiteSearchEngineServiceAsyncClient
from .services.user_event_service import UserEventServiceClient
from .services.user_event_service import UserEventServiceAsyncClient

from .types.common import CustomAttribute
from .types.common import DoubleList
from .types.common import Interval
from .types.common import UserInfo
from .types.common import IndustryVertical
from .types.common import SearchAddOn
from .types.common import SearchTier
from .types.common import SolutionType
from .types.completion_service import CompleteQueryRequest
from .types.completion_service import CompleteQueryResponse
from .types.conversation import Conversation
from .types.conversation import ConversationContext
from .types.conversation import ConversationMessage
from .types.conversation import Reply
from .types.conversation import TextInput
from .types.conversational_search_service import ConverseConversationRequest
from .types.conversational_search_service import ConverseConversationResponse
from .types.conversational_search_service import CreateConversationRequest
from .types.conversational_search_service import DeleteConversationRequest
from .types.conversational_search_service import GetConversationRequest
from .types.conversational_search_service import ListConversationsRequest
from .types.conversational_search_service import ListConversationsResponse
from .types.conversational_search_service import UpdateConversationRequest
from .types.data_store import DataStore
from .types.data_store_service import CreateDataStoreMetadata
from .types.data_store_service import CreateDataStoreRequest
from .types.data_store_service import DeleteDataStoreMetadata
from .types.data_store_service import DeleteDataStoreRequest
from .types.data_store_service import GetDataStoreRequest
from .types.data_store_service import ListDataStoresRequest
from .types.data_store_service import ListDataStoresResponse
from .types.data_store_service import UpdateDataStoreRequest
from .types.document import Document
from .types.document_service import CreateDocumentRequest
from .types.document_service import DeleteDocumentRequest
from .types.document_service import GetDocumentRequest
from .types.document_service import ListDocumentsRequest
from .types.document_service import ListDocumentsResponse
from .types.document_service import UpdateDocumentRequest
from .types.engine import Engine
from .types.engine_service import CreateEngineMetadata
from .types.engine_service import CreateEngineRequest
from .types.engine_service import DeleteEngineMetadata
from .types.engine_service import DeleteEngineRequest
from .types.engine_service import GetEngineRequest
from .types.engine_service import ListEnginesRequest
from .types.engine_service import ListEnginesResponse
from .types.engine_service import PauseEngineRequest
from .types.engine_service import ResumeEngineRequest
from .types.engine_service import TuneEngineMetadata
from .types.engine_service import TuneEngineRequest
from .types.engine_service import TuneEngineResponse
from .types.engine_service import UpdateEngineRequest
from .types.import_config import BigQuerySource
from .types.import_config import GcsSource
from .types.import_config import ImportDocumentsMetadata
from .types.import_config import ImportDocumentsRequest
from .types.import_config import ImportDocumentsResponse
from .types.import_config import ImportErrorConfig
from .types.import_config import ImportUserEventsMetadata
from .types.import_config import ImportUserEventsRequest
from .types.import_config import ImportUserEventsResponse
from .types.purge_config import PurgeDocumentsMetadata
from .types.purge_config import PurgeDocumentsRequest
from .types.purge_config import PurgeDocumentsResponse
from .types.purge_config import PurgeUserEventsMetadata
from .types.purge_config import PurgeUserEventsRequest
from .types.purge_config import PurgeUserEventsResponse
from .types.recommendation_service import RecommendRequest
from .types.recommendation_service import RecommendResponse
from .types.schema import FieldConfig
from .types.schema import Schema
from .types.schema_service import CreateSchemaMetadata
from .types.schema_service import CreateSchemaRequest
from .types.schema_service import DeleteSchemaMetadata
from .types.schema_service import DeleteSchemaRequest
from .types.schema_service import GetSchemaRequest
from .types.schema_service import ListSchemasRequest
from .types.schema_service import ListSchemasResponse
from .types.schema_service import UpdateSchemaMetadata
from .types.schema_service import UpdateSchemaRequest
from .types.search_service import SearchRequest
from .types.search_service import SearchResponse
from .types.site_search_engine_service import RecrawlUrisMetadata
from .types.site_search_engine_service import RecrawlUrisRequest
from .types.site_search_engine_service import RecrawlUrisResponse
from .types.user_event import CompletionInfo
from .types.user_event import DocumentInfo
from .types.user_event import MediaInfo
from .types.user_event import PageInfo
from .types.user_event import PanelInfo
from .types.user_event import SearchInfo
from .types.user_event import TransactionInfo
from .types.user_event import UserEvent
from .types.user_event_service import CollectUserEventRequest
from .types.user_event_service import WriteUserEventRequest

__all__ = (
    'CompletionServiceAsyncClient',
    'ConversationalSearchServiceAsyncClient',
    'DataStoreServiceAsyncClient',
    'DocumentServiceAsyncClient',
    'EngineServiceAsyncClient',
    'RecommendationServiceAsyncClient',
    'SchemaServiceAsyncClient',
    'SearchServiceAsyncClient',
    'SiteSearchEngineServiceAsyncClient',
    'UserEventServiceAsyncClient',
'BigQuerySource',
'CollectUserEventRequest',
'CompleteQueryRequest',
'CompleteQueryResponse',
'CompletionInfo',
'CompletionServiceClient',
'Conversation',
'ConversationContext',
'ConversationMessage',
'ConversationalSearchServiceClient',
'ConverseConversationRequest',
'ConverseConversationResponse',
'CreateConversationRequest',
'CreateDataStoreMetadata',
'CreateDataStoreRequest',
'CreateDocumentRequest',
'CreateEngineMetadata',
'CreateEngineRequest',
'CreateSchemaMetadata',
'CreateSchemaRequest',
'CustomAttribute',
'DataStore',
'DataStoreServiceClient',
'DeleteConversationRequest',
'DeleteDataStoreMetadata',
'DeleteDataStoreRequest',
'DeleteDocumentRequest',
'DeleteEngineMetadata',
'DeleteEngineRequest',
'DeleteSchemaMetadata',
'DeleteSchemaRequest',
'Document',
'DocumentInfo',
'DocumentServiceClient',
'DoubleList',
'Engine',
'EngineServiceClient',
'FieldConfig',
'GcsSource',
'GetConversationRequest',
'GetDataStoreRequest',
'GetDocumentRequest',
'GetEngineRequest',
'GetSchemaRequest',
'ImportDocumentsMetadata',
'ImportDocumentsRequest',
'ImportDocumentsResponse',
'ImportErrorConfig',
'ImportUserEventsMetadata',
'ImportUserEventsRequest',
'ImportUserEventsResponse',
'IndustryVertical',
'Interval',
'ListConversationsRequest',
'ListConversationsResponse',
'ListDataStoresRequest',
'ListDataStoresResponse',
'ListDocumentsRequest',
'ListDocumentsResponse',
'ListEnginesRequest',
'ListEnginesResponse',
'ListSchemasRequest',
'ListSchemasResponse',
'MediaInfo',
'PageInfo',
'PanelInfo',
'PauseEngineRequest',
'PurgeDocumentsMetadata',
'PurgeDocumentsRequest',
'PurgeDocumentsResponse',
'PurgeUserEventsMetadata',
'PurgeUserEventsRequest',
'PurgeUserEventsResponse',
'RecommendRequest',
'RecommendResponse',
'RecommendationServiceClient',
'RecrawlUrisMetadata',
'RecrawlUrisRequest',
'RecrawlUrisResponse',
'Reply',
'ResumeEngineRequest',
'Schema',
'SchemaServiceClient',
'SearchAddOn',
'SearchInfo',
'SearchRequest',
'SearchResponse',
'SearchServiceClient',
'SearchTier',
'SiteSearchEngineServiceClient',
'SolutionType',
'TextInput',
'TransactionInfo',
'TuneEngineMetadata',
'TuneEngineRequest',
'TuneEngineResponse',
'UpdateConversationRequest',
'UpdateDataStoreRequest',
'UpdateDocumentRequest',
'UpdateEngineRequest',
'UpdateSchemaMetadata',
'UpdateSchemaRequest',
'UserEvent',
'UserEventServiceClient',
'UserInfo',
'WriteUserEventRequest',
)
