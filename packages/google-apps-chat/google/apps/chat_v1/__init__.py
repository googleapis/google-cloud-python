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
from google.apps.chat_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.chat_service import ChatServiceAsyncClient, ChatServiceClient
from .types.action_status import ActionStatus
from .types.annotation import (
    Annotation,
    AnnotationType,
    DriveLinkData,
    RichLinkMetadata,
    SlashCommandMetadata,
    UserMentionMetadata,
)
from .types.attachment import (
    Attachment,
    AttachmentDataRef,
    DriveDataRef,
    GetAttachmentRequest,
    UploadAttachmentRequest,
    UploadAttachmentResponse,
)
from .types.contextual_addon import ContextualAddOnMarkup
from .types.deletion_metadata import DeletionMetadata
from .types.group import Group
from .types.history_state import HistoryState
from .types.matched_url import MatchedUrl
from .types.membership import (
    CreateMembershipRequest,
    DeleteMembershipRequest,
    GetMembershipRequest,
    ListMembershipsRequest,
    ListMembershipsResponse,
    Membership,
)
from .types.message import (
    ActionResponse,
    AttachedGif,
    CardWithId,
    CreateMessageRequest,
    DeleteMessageRequest,
    Dialog,
    DialogAction,
    GetMessageRequest,
    ListMessagesRequest,
    ListMessagesResponse,
    Message,
    QuotedMessageMetadata,
    Thread,
    UpdateMessageRequest,
)
from .types.reaction import (
    CreateReactionRequest,
    CustomEmoji,
    DeleteReactionRequest,
    Emoji,
    EmojiReactionSummary,
    ListReactionsRequest,
    ListReactionsResponse,
    Reaction,
)
from .types.slash_command import SlashCommand
from .types.space import (
    CompleteImportSpaceRequest,
    CompleteImportSpaceResponse,
    CreateSpaceRequest,
    DeleteSpaceRequest,
    FindDirectMessageRequest,
    GetSpaceRequest,
    ListSpacesRequest,
    ListSpacesResponse,
    Space,
    UpdateSpaceRequest,
)
from .types.space_setup import SetUpSpaceRequest
from .types.user import User
from .types.widgets import WidgetMarkup

__all__ = (
    "ChatServiceAsyncClient",
    "ActionResponse",
    "ActionStatus",
    "Annotation",
    "AnnotationType",
    "AttachedGif",
    "Attachment",
    "AttachmentDataRef",
    "CardWithId",
    "ChatServiceClient",
    "CompleteImportSpaceRequest",
    "CompleteImportSpaceResponse",
    "ContextualAddOnMarkup",
    "CreateMembershipRequest",
    "CreateMessageRequest",
    "CreateReactionRequest",
    "CreateSpaceRequest",
    "CustomEmoji",
    "DeleteMembershipRequest",
    "DeleteMessageRequest",
    "DeleteReactionRequest",
    "DeleteSpaceRequest",
    "DeletionMetadata",
    "Dialog",
    "DialogAction",
    "DriveDataRef",
    "DriveLinkData",
    "Emoji",
    "EmojiReactionSummary",
    "FindDirectMessageRequest",
    "GetAttachmentRequest",
    "GetMembershipRequest",
    "GetMessageRequest",
    "GetSpaceRequest",
    "Group",
    "HistoryState",
    "ListMembershipsRequest",
    "ListMembershipsResponse",
    "ListMessagesRequest",
    "ListMessagesResponse",
    "ListReactionsRequest",
    "ListReactionsResponse",
    "ListSpacesRequest",
    "ListSpacesResponse",
    "MatchedUrl",
    "Membership",
    "Message",
    "QuotedMessageMetadata",
    "Reaction",
    "RichLinkMetadata",
    "SetUpSpaceRequest",
    "SlashCommand",
    "SlashCommandMetadata",
    "Space",
    "Thread",
    "UpdateMessageRequest",
    "UpdateSpaceRequest",
    "UploadAttachmentRequest",
    "UploadAttachmentResponse",
    "User",
    "UserMentionMetadata",
    "WidgetMarkup",
)
