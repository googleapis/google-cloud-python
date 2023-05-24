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
from google.cloud.discoveryengine_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.completion_service import CompletionServiceClient
from .services.completion_service import CompletionServiceAsyncClient
from .services.document_service import DocumentServiceClient
from .services.document_service import DocumentServiceAsyncClient
from .services.schema_service import SchemaServiceClient
from .services.schema_service import SchemaServiceAsyncClient
from .services.search_service import SearchServiceClient
from .services.search_service import SearchServiceAsyncClient
from .services.user_event_service import UserEventServiceClient
from .services.user_event_service import UserEventServiceAsyncClient

from .types.common import CustomAttribute
from .types.common import UserInfo
from .types.completion_service import CompleteQueryRequest
from .types.completion_service import CompleteQueryResponse
from .types.document import Document
from .types.document_service import CreateDocumentRequest
from .types.document_service import DeleteDocumentRequest
from .types.document_service import GetDocumentRequest
from .types.document_service import ListDocumentsRequest
from .types.document_service import ListDocumentsResponse
from .types.document_service import UpdateDocumentRequest
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
    'DocumentServiceAsyncClient',
    'SchemaServiceAsyncClient',
    'SearchServiceAsyncClient',
    'UserEventServiceAsyncClient',
'BigQuerySource',
'CollectUserEventRequest',
'CompleteQueryRequest',
'CompleteQueryResponse',
'CompletionInfo',
'CompletionServiceClient',
'CreateDocumentRequest',
'CreateSchemaMetadata',
'CreateSchemaRequest',
'CustomAttribute',
'DeleteDocumentRequest',
'DeleteSchemaMetadata',
'DeleteSchemaRequest',
'Document',
'DocumentInfo',
'DocumentServiceClient',
'GcsSource',
'GetDocumentRequest',
'GetSchemaRequest',
'ImportDocumentsMetadata',
'ImportDocumentsRequest',
'ImportDocumentsResponse',
'ImportErrorConfig',
'ImportUserEventsMetadata',
'ImportUserEventsRequest',
'ImportUserEventsResponse',
'ListDocumentsRequest',
'ListDocumentsResponse',
'ListSchemasRequest',
'ListSchemasResponse',
'MediaInfo',
'PageInfo',
'PanelInfo',
'PurgeDocumentsMetadata',
'PurgeDocumentsRequest',
'PurgeDocumentsResponse',
'Schema',
'SchemaServiceClient',
'SearchInfo',
'SearchRequest',
'SearchResponse',
'SearchServiceClient',
'TransactionInfo',
'UpdateDocumentRequest',
'UpdateSchemaMetadata',
'UpdateSchemaRequest',
'UserEvent',
'UserEventServiceClient',
'UserInfo',
'WriteUserEventRequest',
)
