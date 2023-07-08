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
from google.cloud.support_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.case_attachment_service import (
    CaseAttachmentServiceAsyncClient,
    CaseAttachmentServiceClient,
)
from .services.case_service import CaseServiceAsyncClient, CaseServiceClient
from .services.comment_service import CommentServiceAsyncClient, CommentServiceClient
from .types.actor import Actor
from .types.attachment import Attachment
from .types.attachment_service import ListAttachmentsRequest, ListAttachmentsResponse
from .types.case import Case, CaseClassification
from .types.case_service import (
    CloseCaseRequest,
    CreateCaseRequest,
    EscalateCaseRequest,
    GetCaseRequest,
    ListCasesRequest,
    ListCasesResponse,
    SearchCaseClassificationsRequest,
    SearchCaseClassificationsResponse,
    SearchCasesRequest,
    SearchCasesResponse,
    UpdateCaseRequest,
)
from .types.comment import Comment
from .types.comment_service import (
    CreateCommentRequest,
    ListCommentsRequest,
    ListCommentsResponse,
)
from .types.escalation import Escalation

__all__ = (
    "CaseAttachmentServiceAsyncClient",
    "CaseServiceAsyncClient",
    "CommentServiceAsyncClient",
    "Actor",
    "Attachment",
    "Case",
    "CaseAttachmentServiceClient",
    "CaseClassification",
    "CaseServiceClient",
    "CloseCaseRequest",
    "Comment",
    "CommentServiceClient",
    "CreateCaseRequest",
    "CreateCommentRequest",
    "EscalateCaseRequest",
    "Escalation",
    "GetCaseRequest",
    "ListAttachmentsRequest",
    "ListAttachmentsResponse",
    "ListCasesRequest",
    "ListCasesResponse",
    "ListCommentsRequest",
    "ListCommentsResponse",
    "SearchCaseClassificationsRequest",
    "SearchCaseClassificationsResponse",
    "SearchCasesRequest",
    "SearchCasesResponse",
    "UpdateCaseRequest",
)
