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
from .common import CustomAttribute, DoubleList, Interval, SolutionType, UserInfo
from .completion_service import CompleteQueryRequest, CompleteQueryResponse
from .conversation import (
    Conversation,
    ConversationContext,
    ConversationMessage,
    Reply,
    TextInput,
)
from .conversational_search_service import (
    ConverseConversationRequest,
    ConverseConversationResponse,
    CreateConversationRequest,
    DeleteConversationRequest,
    GetConversationRequest,
    ListConversationsRequest,
    ListConversationsResponse,
    UpdateConversationRequest,
)
from .document import Document
from .document_service import (
    CreateDocumentRequest,
    DeleteDocumentRequest,
    GetDocumentRequest,
    ListDocumentsRequest,
    ListDocumentsResponse,
    UpdateDocumentRequest,
)
from .import_config import (
    BigQuerySource,
    GcsSource,
    ImportDocumentsMetadata,
    ImportDocumentsRequest,
    ImportDocumentsResponse,
    ImportErrorConfig,
    ImportUserEventsMetadata,
    ImportUserEventsRequest,
    ImportUserEventsResponse,
)
from .purge_config import (
    PurgeDocumentsMetadata,
    PurgeDocumentsRequest,
    PurgeDocumentsResponse,
    PurgeUserEventsMetadata,
    PurgeUserEventsRequest,
    PurgeUserEventsResponse,
)
from .recommendation_service import RecommendRequest, RecommendResponse
from .schema import FieldConfig, Schema
from .schema_service import (
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
from .search_service import SearchRequest, SearchResponse
from .site_search_engine_service import (
    RecrawlUrisMetadata,
    RecrawlUrisRequest,
    RecrawlUrisResponse,
)
from .user_event import (
    CompletionInfo,
    DocumentInfo,
    MediaInfo,
    PageInfo,
    PanelInfo,
    SearchInfo,
    TransactionInfo,
    UserEvent,
)
from .user_event_service import CollectUserEventRequest, WriteUserEventRequest

__all__ = (
    "CustomAttribute",
    "DoubleList",
    "Interval",
    "UserInfo",
    "SolutionType",
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
    "Document",
    "CreateDocumentRequest",
    "DeleteDocumentRequest",
    "GetDocumentRequest",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "UpdateDocumentRequest",
    "BigQuerySource",
    "GcsSource",
    "ImportDocumentsMetadata",
    "ImportDocumentsRequest",
    "ImportDocumentsResponse",
    "ImportErrorConfig",
    "ImportUserEventsMetadata",
    "ImportUserEventsRequest",
    "ImportUserEventsResponse",
    "PurgeDocumentsMetadata",
    "PurgeDocumentsRequest",
    "PurgeDocumentsResponse",
    "PurgeUserEventsMetadata",
    "PurgeUserEventsRequest",
    "PurgeUserEventsResponse",
    "RecommendRequest",
    "RecommendResponse",
    "FieldConfig",
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
    "RecrawlUrisMetadata",
    "RecrawlUrisRequest",
    "RecrawlUrisResponse",
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
