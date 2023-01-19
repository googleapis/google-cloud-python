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


from .services.document_service import DocumentServiceClient
from .services.document_service import DocumentServiceAsyncClient
from .services.recommendation_service import RecommendationServiceClient
from .services.recommendation_service import RecommendationServiceAsyncClient
from .services.user_event_service import UserEventServiceClient
from .services.user_event_service import UserEventServiceAsyncClient

from .types.common import CustomAttribute
from .types.common import UserInfo
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
from .types.recommendation_service import RecommendRequest
from .types.recommendation_service import RecommendResponse
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
    'DocumentServiceAsyncClient',
    'RecommendationServiceAsyncClient',
    'UserEventServiceAsyncClient',
'BigQuerySource',
'CollectUserEventRequest',
'CompletionInfo',
'CreateDocumentRequest',
'CustomAttribute',
'DeleteDocumentRequest',
'Document',
'DocumentInfo',
'DocumentServiceClient',
'GcsSource',
'GetDocumentRequest',
'ImportDocumentsMetadata',
'ImportDocumentsRequest',
'ImportDocumentsResponse',
'ImportErrorConfig',
'ImportUserEventsMetadata',
'ImportUserEventsRequest',
'ImportUserEventsResponse',
'ListDocumentsRequest',
'ListDocumentsResponse',
'MediaInfo',
'PageInfo',
'PanelInfo',
'RecommendRequest',
'RecommendResponse',
'RecommendationServiceClient',
'SearchInfo',
'TransactionInfo',
'UpdateDocumentRequest',
'UserEvent',
'UserEventServiceClient',
'UserInfo',
'WriteUserEventRequest',
)
