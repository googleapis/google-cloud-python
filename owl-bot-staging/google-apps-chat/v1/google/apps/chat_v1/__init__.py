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


from .services.chat_service import ChatServiceClient
from .services.chat_service import ChatServiceAsyncClient

from .types.action_status import ActionStatus
from .types.annotation import Annotation
from .types.annotation import DriveLinkData
from .types.annotation import RichLinkMetadata
from .types.annotation import SlashCommandMetadata
from .types.annotation import UserMentionMetadata
from .types.annotation import AnnotationType
from .types.attachment import Attachment
from .types.attachment import AttachmentDataRef
from .types.attachment import DriveDataRef
from .types.attachment import GetAttachmentRequest
from .types.attachment import UploadAttachmentRequest
from .types.attachment import UploadAttachmentResponse
from .types.contextual_addon import ContextualAddOnMarkup
from .types.deletion_metadata import DeletionMetadata
from .types.event_payload import MembershipBatchCreatedEventData
from .types.event_payload import MembershipBatchDeletedEventData
from .types.event_payload import MembershipBatchUpdatedEventData
from .types.event_payload import MembershipCreatedEventData
from .types.event_payload import MembershipDeletedEventData
from .types.event_payload import MembershipUpdatedEventData
from .types.event_payload import MessageBatchCreatedEventData
from .types.event_payload import MessageBatchDeletedEventData
from .types.event_payload import MessageBatchUpdatedEventData
from .types.event_payload import MessageCreatedEventData
from .types.event_payload import MessageDeletedEventData
from .types.event_payload import MessageUpdatedEventData
from .types.event_payload import ReactionBatchCreatedEventData
from .types.event_payload import ReactionBatchDeletedEventData
from .types.event_payload import ReactionCreatedEventData
from .types.event_payload import ReactionDeletedEventData
from .types.event_payload import SpaceBatchUpdatedEventData
from .types.event_payload import SpaceUpdatedEventData
from .types.group import Group
from .types.history_state import HistoryState
from .types.matched_url import MatchedUrl
from .types.membership import CreateMembershipRequest
from .types.membership import DeleteMembershipRequest
from .types.membership import GetMembershipRequest
from .types.membership import ListMembershipsRequest
from .types.membership import ListMembershipsResponse
from .types.membership import Membership
from .types.membership import UpdateMembershipRequest
from .types.message import AccessoryWidget
from .types.message import ActionResponse
from .types.message import AttachedGif
from .types.message import CardWithId
from .types.message import CreateMessageRequest
from .types.message import DeleteMessageRequest
from .types.message import Dialog
from .types.message import DialogAction
from .types.message import GetMessageRequest
from .types.message import ListMessagesRequest
from .types.message import ListMessagesResponse
from .types.message import Message
from .types.message import QuotedMessageMetadata
from .types.message import Thread
from .types.message import UpdateMessageRequest
from .types.reaction import CreateReactionRequest
from .types.reaction import CustomEmoji
from .types.reaction import DeleteReactionRequest
from .types.reaction import Emoji
from .types.reaction import EmojiReactionSummary
from .types.reaction import ListReactionsRequest
from .types.reaction import ListReactionsResponse
from .types.reaction import Reaction
from .types.slash_command import SlashCommand
from .types.space import CompleteImportSpaceRequest
from .types.space import CompleteImportSpaceResponse
from .types.space import CreateSpaceRequest
from .types.space import DeleteSpaceRequest
from .types.space import FindDirectMessageRequest
from .types.space import GetSpaceRequest
from .types.space import ListSpacesRequest
from .types.space import ListSpacesResponse
from .types.space import Space
from .types.space import UpdateSpaceRequest
from .types.space_event import GetSpaceEventRequest
from .types.space_event import ListSpaceEventsRequest
from .types.space_event import ListSpaceEventsResponse
from .types.space_event import SpaceEvent
from .types.space_read_state import GetSpaceReadStateRequest
from .types.space_read_state import SpaceReadState
from .types.space_read_state import UpdateSpaceReadStateRequest
from .types.space_setup import SetUpSpaceRequest
from .types.thread_read_state import GetThreadReadStateRequest
from .types.thread_read_state import ThreadReadState
from .types.user import User
from .types.widgets import WidgetMarkup

__all__ = (
    'ChatServiceAsyncClient',
'AccessoryWidget',
'ActionResponse',
'ActionStatus',
'Annotation',
'AnnotationType',
'AttachedGif',
'Attachment',
'AttachmentDataRef',
'CardWithId',
'ChatServiceClient',
'CompleteImportSpaceRequest',
'CompleteImportSpaceResponse',
'ContextualAddOnMarkup',
'CreateMembershipRequest',
'CreateMessageRequest',
'CreateReactionRequest',
'CreateSpaceRequest',
'CustomEmoji',
'DeleteMembershipRequest',
'DeleteMessageRequest',
'DeleteReactionRequest',
'DeleteSpaceRequest',
'DeletionMetadata',
'Dialog',
'DialogAction',
'DriveDataRef',
'DriveLinkData',
'Emoji',
'EmojiReactionSummary',
'FindDirectMessageRequest',
'GetAttachmentRequest',
'GetMembershipRequest',
'GetMessageRequest',
'GetSpaceEventRequest',
'GetSpaceReadStateRequest',
'GetSpaceRequest',
'GetThreadReadStateRequest',
'Group',
'HistoryState',
'ListMembershipsRequest',
'ListMembershipsResponse',
'ListMessagesRequest',
'ListMessagesResponse',
'ListReactionsRequest',
'ListReactionsResponse',
'ListSpaceEventsRequest',
'ListSpaceEventsResponse',
'ListSpacesRequest',
'ListSpacesResponse',
'MatchedUrl',
'Membership',
'MembershipBatchCreatedEventData',
'MembershipBatchDeletedEventData',
'MembershipBatchUpdatedEventData',
'MembershipCreatedEventData',
'MembershipDeletedEventData',
'MembershipUpdatedEventData',
'Message',
'MessageBatchCreatedEventData',
'MessageBatchDeletedEventData',
'MessageBatchUpdatedEventData',
'MessageCreatedEventData',
'MessageDeletedEventData',
'MessageUpdatedEventData',
'QuotedMessageMetadata',
'Reaction',
'ReactionBatchCreatedEventData',
'ReactionBatchDeletedEventData',
'ReactionCreatedEventData',
'ReactionDeletedEventData',
'RichLinkMetadata',
'SetUpSpaceRequest',
'SlashCommand',
'SlashCommandMetadata',
'Space',
'SpaceBatchUpdatedEventData',
'SpaceEvent',
'SpaceReadState',
'SpaceUpdatedEventData',
'Thread',
'ThreadReadState',
'UpdateMembershipRequest',
'UpdateMessageRequest',
'UpdateSpaceReadStateRequest',
'UpdateSpaceRequest',
'UploadAttachmentRequest',
'UploadAttachmentResponse',
'User',
'UserMentionMetadata',
'WidgetMarkup',
)
