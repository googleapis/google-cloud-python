# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.support import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.support_v2beta.services.case_attachment_service.client import CaseAttachmentServiceClient
from google.cloud.support_v2beta.services.case_attachment_service.async_client import CaseAttachmentServiceAsyncClient
from google.cloud.support_v2beta.services.case_service.client import CaseServiceClient
from google.cloud.support_v2beta.services.case_service.async_client import CaseServiceAsyncClient
from google.cloud.support_v2beta.services.comment_service.client import CommentServiceClient
from google.cloud.support_v2beta.services.comment_service.async_client import CommentServiceAsyncClient
from google.cloud.support_v2beta.services.feed_service.client import FeedServiceClient
from google.cloud.support_v2beta.services.feed_service.async_client import FeedServiceAsyncClient

from google.cloud.support_v2beta.types.actor import Actor
from google.cloud.support_v2beta.types.attachment import Attachment
from google.cloud.support_v2beta.types.attachment_service import GetAttachmentRequest
from google.cloud.support_v2beta.types.attachment_service import ListAttachmentsRequest
from google.cloud.support_v2beta.types.attachment_service import ListAttachmentsResponse
from google.cloud.support_v2beta.types.case import Case
from google.cloud.support_v2beta.types.case import CaseClassification
from google.cloud.support_v2beta.types.case import Product
from google.cloud.support_v2beta.types.case import ProductLine
from google.cloud.support_v2beta.types.case_service import CloseCaseRequest
from google.cloud.support_v2beta.types.case_service import CreateCaseRequest
from google.cloud.support_v2beta.types.case_service import EscalateCaseRequest
from google.cloud.support_v2beta.types.case_service import GetCaseRequest
from google.cloud.support_v2beta.types.case_service import ListCasesRequest
from google.cloud.support_v2beta.types.case_service import ListCasesResponse
from google.cloud.support_v2beta.types.case_service import SearchCaseClassificationsRequest
from google.cloud.support_v2beta.types.case_service import SearchCaseClassificationsResponse
from google.cloud.support_v2beta.types.case_service import SearchCasesRequest
from google.cloud.support_v2beta.types.case_service import SearchCasesResponse
from google.cloud.support_v2beta.types.case_service import UpdateCaseRequest
from google.cloud.support_v2beta.types.comment import Comment
from google.cloud.support_v2beta.types.comment_service import CreateCommentRequest
from google.cloud.support_v2beta.types.comment_service import GetCommentRequest
from google.cloud.support_v2beta.types.comment_service import ListCommentsRequest
from google.cloud.support_v2beta.types.comment_service import ListCommentsResponse
from google.cloud.support_v2beta.types.content import TextContent
from google.cloud.support_v2beta.types.email_message import EmailMessage
from google.cloud.support_v2beta.types.escalation import Escalation
from google.cloud.support_v2beta.types.feed_item import FeedItem
from google.cloud.support_v2beta.types.feed_service import ShowFeedRequest
from google.cloud.support_v2beta.types.feed_service import ShowFeedResponse

__all__ = ('CaseAttachmentServiceClient',
    'CaseAttachmentServiceAsyncClient',
    'CaseServiceClient',
    'CaseServiceAsyncClient',
    'CommentServiceClient',
    'CommentServiceAsyncClient',
    'FeedServiceClient',
    'FeedServiceAsyncClient',
    'Actor',
    'Attachment',
    'GetAttachmentRequest',
    'ListAttachmentsRequest',
    'ListAttachmentsResponse',
    'Case',
    'CaseClassification',
    'Product',
    'ProductLine',
    'CloseCaseRequest',
    'CreateCaseRequest',
    'EscalateCaseRequest',
    'GetCaseRequest',
    'ListCasesRequest',
    'ListCasesResponse',
    'SearchCaseClassificationsRequest',
    'SearchCaseClassificationsResponse',
    'SearchCasesRequest',
    'SearchCasesResponse',
    'UpdateCaseRequest',
    'Comment',
    'CreateCommentRequest',
    'GetCommentRequest',
    'ListCommentsRequest',
    'ListCommentsResponse',
    'TextContent',
    'EmailMessage',
    'Escalation',
    'FeedItem',
    'ShowFeedRequest',
    'ShowFeedResponse',
)
