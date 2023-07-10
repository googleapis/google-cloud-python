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
from google.cloud.discoveryengine_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.completion_service import (
    CompletionServiceAsyncClient,
    CompletionServiceClient,
)
from .services.document_service import DocumentServiceAsyncClient, DocumentServiceClient
from .services.schema_service import SchemaServiceAsyncClient, SchemaServiceClient
from .services.search_service import SearchServiceAsyncClient, SearchServiceClient
from .services.user_event_service import (
    UserEventServiceAsyncClient,
    UserEventServiceClient,
)
from .types.common import CustomAttribute, UserInfo
from .types.completion_service import CompleteQueryRequest, CompleteQueryResponse
from .types.document import Document
from .types.document_service import (
    CreateDocumentRequest,
    DeleteDocumentRequest,
    GetDocumentRequest,
    ListDocumentsRequest,
    ListDocumentsResponse,
    UpdateDocumentRequest,
)
from .types.import_config import (
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
from .types.purge_config import (
    PurgeDocumentsMetadata,
    PurgeDocumentsRequest,
    PurgeDocumentsResponse,
)
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
    "DocumentServiceAsyncClient",
    "SchemaServiceAsyncClient",
    "SearchServiceAsyncClient",
    "UserEventServiceAsyncClient",
    "BigQuerySource",
    "CollectUserEventRequest",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "CompletionInfo",
    "CompletionServiceClient",
    "CreateDocumentRequest",
    "CreateSchemaMetadata",
    "CreateSchemaRequest",
    "CustomAttribute",
    "DeleteDocumentRequest",
    "DeleteSchemaMetadata",
    "DeleteSchemaRequest",
    "Document",
    "DocumentInfo",
    "DocumentServiceClient",
    "GcsSource",
    "GetDocumentRequest",
    "GetSchemaRequest",
    "ImportDocumentsMetadata",
    "ImportDocumentsRequest",
    "ImportDocumentsResponse",
    "ImportErrorConfig",
    "ImportUserEventsMetadata",
    "ImportUserEventsRequest",
    "ImportUserEventsResponse",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "ListSchemasRequest",
    "ListSchemasResponse",
    "MediaInfo",
    "PageInfo",
    "PanelInfo",
    "PurgeDocumentsMetadata",
    "PurgeDocumentsRequest",
    "PurgeDocumentsResponse",
    "Schema",
    "SchemaServiceClient",
    "SearchInfo",
    "SearchRequest",
    "SearchResponse",
    "SearchServiceClient",
    "TransactionInfo",
    "UpdateDocumentRequest",
    "UpdateSchemaMetadata",
    "UpdateSchemaRequest",
    "UserEvent",
    "UserEventServiceClient",
    "UserInfo",
    "WriteUserEventRequest",
)
