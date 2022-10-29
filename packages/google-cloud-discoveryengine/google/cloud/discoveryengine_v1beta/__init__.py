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


from .services.document_service import DocumentServiceAsyncClient, DocumentServiceClient
from .services.recommendation_service import (
    RecommendationServiceAsyncClient,
    RecommendationServiceClient,
)
from .services.user_event_service import (
    UserEventServiceAsyncClient,
    UserEventServiceClient,
)
from .types.common import CustomAttribute, UserInfo
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
from .types.recommendation_service import RecommendRequest, RecommendResponse
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
    "DocumentServiceAsyncClient",
    "RecommendationServiceAsyncClient",
    "UserEventServiceAsyncClient",
    "BigQuerySource",
    "CollectUserEventRequest",
    "CompletionInfo",
    "CreateDocumentRequest",
    "CustomAttribute",
    "DeleteDocumentRequest",
    "Document",
    "DocumentInfo",
    "DocumentServiceClient",
    "GcsSource",
    "GetDocumentRequest",
    "ImportDocumentsMetadata",
    "ImportDocumentsRequest",
    "ImportDocumentsResponse",
    "ImportErrorConfig",
    "ImportUserEventsMetadata",
    "ImportUserEventsRequest",
    "ImportUserEventsResponse",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "MediaInfo",
    "PageInfo",
    "PanelInfo",
    "RecommendRequest",
    "RecommendResponse",
    "RecommendationServiceClient",
    "SearchInfo",
    "TransactionInfo",
    "UpdateDocumentRequest",
    "UserEvent",
    "UserEventServiceClient",
    "UserInfo",
    "WriteUserEventRequest",
)
