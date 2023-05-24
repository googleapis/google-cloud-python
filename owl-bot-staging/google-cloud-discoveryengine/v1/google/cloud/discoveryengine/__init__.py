# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.cloud.discoveryengine_v1.services.document_service.client import DocumentServiceClient
from google.cloud.discoveryengine_v1.services.document_service.async_client import DocumentServiceAsyncClient
from google.cloud.discoveryengine_v1.services.schema_service.client import SchemaServiceClient
from google.cloud.discoveryengine_v1.services.schema_service.async_client import SchemaServiceAsyncClient
from google.cloud.discoveryengine_v1.services.search_service.client import SearchServiceClient
from google.cloud.discoveryengine_v1.services.search_service.async_client import SearchServiceAsyncClient
from google.cloud.discoveryengine_v1.services.user_event_service.client import UserEventServiceClient
from google.cloud.discoveryengine_v1.services.user_event_service.async_client import UserEventServiceAsyncClient

from google.cloud.discoveryengine_v1.types.common import CustomAttribute
from google.cloud.discoveryengine_v1.types.common import UserInfo
from google.cloud.discoveryengine_v1.types.completion_service import CompleteQueryRequest
from google.cloud.discoveryengine_v1.types.completion_service import CompleteQueryResponse
from google.cloud.discoveryengine_v1.types.document import Document
from google.cloud.discoveryengine_v1.types.document_service import CreateDocumentRequest
from google.cloud.discoveryengine_v1.types.document_service import DeleteDocumentRequest
from google.cloud.discoveryengine_v1.types.document_service import GetDocumentRequest
from google.cloud.discoveryengine_v1.types.document_service import ListDocumentsRequest
from google.cloud.discoveryengine_v1.types.document_service import ListDocumentsResponse
from google.cloud.discoveryengine_v1.types.document_service import UpdateDocumentRequest
from google.cloud.discoveryengine_v1.types.import_config import BigQuerySource
from google.cloud.discoveryengine_v1.types.import_config import GcsSource
from google.cloud.discoveryengine_v1.types.import_config import ImportDocumentsMetadata
from google.cloud.discoveryengine_v1.types.import_config import ImportDocumentsRequest
from google.cloud.discoveryengine_v1.types.import_config import ImportDocumentsResponse
from google.cloud.discoveryengine_v1.types.import_config import ImportErrorConfig
from google.cloud.discoveryengine_v1.types.import_config import ImportUserEventsMetadata
from google.cloud.discoveryengine_v1.types.import_config import ImportUserEventsRequest
from google.cloud.discoveryengine_v1.types.import_config import ImportUserEventsResponse
from google.cloud.discoveryengine_v1.types.purge_config import PurgeDocumentsMetadata
from google.cloud.discoveryengine_v1.types.purge_config import PurgeDocumentsRequest
from google.cloud.discoveryengine_v1.types.purge_config import PurgeDocumentsResponse
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
    'DocumentServiceClient',
    'DocumentServiceAsyncClient',
    'SchemaServiceClient',
    'SchemaServiceAsyncClient',
    'SearchServiceClient',
    'SearchServiceAsyncClient',
    'UserEventServiceClient',
    'UserEventServiceAsyncClient',
    'CustomAttribute',
    'UserInfo',
    'CompleteQueryRequest',
    'CompleteQueryResponse',
    'Document',
    'CreateDocumentRequest',
    'DeleteDocumentRequest',
    'GetDocumentRequest',
    'ListDocumentsRequest',
    'ListDocumentsResponse',
    'UpdateDocumentRequest',
    'BigQuerySource',
    'GcsSource',
    'ImportDocumentsMetadata',
    'ImportDocumentsRequest',
    'ImportDocumentsResponse',
    'ImportErrorConfig',
    'ImportUserEventsMetadata',
    'ImportUserEventsRequest',
    'ImportUserEventsResponse',
    'PurgeDocumentsMetadata',
    'PurgeDocumentsRequest',
    'PurgeDocumentsResponse',
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
