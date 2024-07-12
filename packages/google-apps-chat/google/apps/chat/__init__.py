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
from google.apps.chat import gapic_version as package_version

__version__ = package_version.__version__


from google.apps.chat_v1.services.chat_service.async_client import (
    ChatServiceAsyncClient,
)
from google.apps.chat_v1.services.chat_service.client import ChatServiceClient
from google.apps.chat_v1.types.action_status import ActionStatus
from google.apps.chat_v1.types.annotation import (
    Annotation,
    AnnotationType,
    DriveLinkData,
    RichLinkMetadata,
    SlashCommandMetadata,
    UserMentionMetadata,
)
from google.apps.chat_v1.types.attachment import (
    Attachment,
    AttachmentDataRef,
    DriveDataRef,
    GetAttachmentRequest,
    UploadAttachmentRequest,
    UploadAttachmentResponse,
)
from google.apps.chat_v1.types.contextual_addon import ContextualAddOnMarkup
from google.apps.chat_v1.types.deletion_metadata import DeletionMetadata
from google.apps.chat_v1.types.event_payload import (
    MembershipBatchCreatedEventData,
    MembershipBatchDeletedEventData,
    MembershipBatchUpdatedEventData,
    MembershipCreatedEventData,
    MembershipDeletedEventData,
    MembershipUpdatedEventData,
    MessageBatchCreatedEventData,
    MessageBatchDeletedEventData,
    MessageBatchUpdatedEventData,
    MessageCreatedEventData,
    MessageDeletedEventData,
    MessageUpdatedEventData,
    ReactionBatchCreatedEventData,
    ReactionBatchDeletedEventData,
    ReactionCreatedEventData,
    ReactionDeletedEventData,
    SpaceBatchUpdatedEventData,
    SpaceUpdatedEventData,
)
from google.apps.chat_v1.types.group import Group
from google.apps.chat_v1.types.history_state import HistoryState
from google.apps.chat_v1.types.matched_url import MatchedUrl
from google.apps.chat_v1.types.membership import (
    CreateMembershipRequest,
    DeleteMembershipRequest,
    GetMembershipRequest,
    ListMembershipsRequest,
    ListMembershipsResponse,
    Membership,
    UpdateMembershipRequest,
)
from google.apps.chat_v1.types.message import (
    AccessoryWidget,
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
from google.apps.chat_v1.types.reaction import (
    CreateReactionRequest,
    CustomEmoji,
    DeleteReactionRequest,
    Emoji,
    EmojiReactionSummary,
    ListReactionsRequest,
    ListReactionsResponse,
    Reaction,
)
from google.apps.chat_v1.types.slash_command import SlashCommand
from google.apps.chat_v1.types.space import (
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
from google.apps.chat_v1.types.space_event import (
    GetSpaceEventRequest,
    ListSpaceEventsRequest,
    ListSpaceEventsResponse,
    SpaceEvent,
)
from google.apps.chat_v1.types.space_read_state import (
    GetSpaceReadStateRequest,
    SpaceReadState,
    UpdateSpaceReadStateRequest,
)
from google.apps.chat_v1.types.space_setup import SetUpSpaceRequest
from google.apps.chat_v1.types.thread_read_state import (
    GetThreadReadStateRequest,
    ThreadReadState,
)
from google.apps.chat_v1.types.user import User
from google.apps.chat_v1.types.widgets import WidgetMarkup

__all__ = (
    "ChatServiceClient",
    "ChatServiceAsyncClient",
    "ActionStatus",
    "Annotation",
    "DriveLinkData",
    "RichLinkMetadata",
    "SlashCommandMetadata",
    "UserMentionMetadata",
    "AnnotationType",
    "Attachment",
    "AttachmentDataRef",
    "DriveDataRef",
    "GetAttachmentRequest",
    "UploadAttachmentRequest",
    "UploadAttachmentResponse",
    "ContextualAddOnMarkup",
    "DeletionMetadata",
    "MembershipBatchCreatedEventData",
    "MembershipBatchDeletedEventData",
    "MembershipBatchUpdatedEventData",
    "MembershipCreatedEventData",
    "MembershipDeletedEventData",
    "MembershipUpdatedEventData",
    "MessageBatchCreatedEventData",
    "MessageBatchDeletedEventData",
    "MessageBatchUpdatedEventData",
    "MessageCreatedEventData",
    "MessageDeletedEventData",
    "MessageUpdatedEventData",
    "ReactionBatchCreatedEventData",
    "ReactionBatchDeletedEventData",
    "ReactionCreatedEventData",
    "ReactionDeletedEventData",
    "SpaceBatchUpdatedEventData",
    "SpaceUpdatedEventData",
    "Group",
    "HistoryState",
    "MatchedUrl",
    "CreateMembershipRequest",
    "DeleteMembershipRequest",
    "GetMembershipRequest",
    "ListMembershipsRequest",
    "ListMembershipsResponse",
    "Membership",
    "UpdateMembershipRequest",
    "AccessoryWidget",
    "ActionResponse",
    "AttachedGif",
    "CardWithId",
    "CreateMessageRequest",
    "DeleteMessageRequest",
    "Dialog",
    "DialogAction",
    "GetMessageRequest",
    "ListMessagesRequest",
    "ListMessagesResponse",
    "Message",
    "QuotedMessageMetadata",
    "Thread",
    "UpdateMessageRequest",
    "CreateReactionRequest",
    "CustomEmoji",
    "DeleteReactionRequest",
    "Emoji",
    "EmojiReactionSummary",
    "ListReactionsRequest",
    "ListReactionsResponse",
    "Reaction",
    "SlashCommand",
    "CompleteImportSpaceRequest",
    "CompleteImportSpaceResponse",
    "CreateSpaceRequest",
    "DeleteSpaceRequest",
    "FindDirectMessageRequest",
    "GetSpaceRequest",
    "ListSpacesRequest",
    "ListSpacesResponse",
    "Space",
    "UpdateSpaceRequest",
    "GetSpaceEventRequest",
    "ListSpaceEventsRequest",
    "ListSpaceEventsResponse",
    "SpaceEvent",
    "GetSpaceReadStateRequest",
    "SpaceReadState",
    "UpdateSpaceReadStateRequest",
    "SetUpSpaceRequest",
    "GetThreadReadStateRequest",
    "ThreadReadState",
    "User",
    "WidgetMarkup",
)
