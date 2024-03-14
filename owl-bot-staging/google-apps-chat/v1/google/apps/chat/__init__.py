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


from google.apps.chat_v1.services.chat_service.client import ChatServiceClient
from google.apps.chat_v1.services.chat_service.async_client import ChatServiceAsyncClient

from google.apps.chat_v1.types.action_status import ActionStatus
from google.apps.chat_v1.types.annotation import Annotation
from google.apps.chat_v1.types.annotation import DriveLinkData
from google.apps.chat_v1.types.annotation import RichLinkMetadata
from google.apps.chat_v1.types.annotation import SlashCommandMetadata
from google.apps.chat_v1.types.annotation import UserMentionMetadata
from google.apps.chat_v1.types.annotation import AnnotationType
from google.apps.chat_v1.types.attachment import Attachment
from google.apps.chat_v1.types.attachment import AttachmentDataRef
from google.apps.chat_v1.types.attachment import DriveDataRef
from google.apps.chat_v1.types.attachment import GetAttachmentRequest
from google.apps.chat_v1.types.attachment import UploadAttachmentRequest
from google.apps.chat_v1.types.attachment import UploadAttachmentResponse
from google.apps.chat_v1.types.contextual_addon import ContextualAddOnMarkup
from google.apps.chat_v1.types.deletion_metadata import DeletionMetadata
from google.apps.chat_v1.types.group import Group
from google.apps.chat_v1.types.history_state import HistoryState
from google.apps.chat_v1.types.matched_url import MatchedUrl
from google.apps.chat_v1.types.membership import CreateMembershipRequest
from google.apps.chat_v1.types.membership import DeleteMembershipRequest
from google.apps.chat_v1.types.membership import GetMembershipRequest
from google.apps.chat_v1.types.membership import ListMembershipsRequest
from google.apps.chat_v1.types.membership import ListMembershipsResponse
from google.apps.chat_v1.types.membership import Membership
from google.apps.chat_v1.types.message import ActionResponse
from google.apps.chat_v1.types.message import AttachedGif
from google.apps.chat_v1.types.message import CardWithId
from google.apps.chat_v1.types.message import CreateMessageRequest
from google.apps.chat_v1.types.message import DeleteMessageRequest
from google.apps.chat_v1.types.message import Dialog
from google.apps.chat_v1.types.message import DialogAction
from google.apps.chat_v1.types.message import GetMessageRequest
from google.apps.chat_v1.types.message import ListMessagesRequest
from google.apps.chat_v1.types.message import ListMessagesResponse
from google.apps.chat_v1.types.message import Message
from google.apps.chat_v1.types.message import QuotedMessageMetadata
from google.apps.chat_v1.types.message import Thread
from google.apps.chat_v1.types.message import UpdateMessageRequest
from google.apps.chat_v1.types.reaction import CreateReactionRequest
from google.apps.chat_v1.types.reaction import CustomEmoji
from google.apps.chat_v1.types.reaction import DeleteReactionRequest
from google.apps.chat_v1.types.reaction import Emoji
from google.apps.chat_v1.types.reaction import EmojiReactionSummary
from google.apps.chat_v1.types.reaction import ListReactionsRequest
from google.apps.chat_v1.types.reaction import ListReactionsResponse
from google.apps.chat_v1.types.reaction import Reaction
from google.apps.chat_v1.types.slash_command import SlashCommand
from google.apps.chat_v1.types.space import CompleteImportSpaceRequest
from google.apps.chat_v1.types.space import CompleteImportSpaceResponse
from google.apps.chat_v1.types.space import CreateSpaceRequest
from google.apps.chat_v1.types.space import DeleteSpaceRequest
from google.apps.chat_v1.types.space import FindDirectMessageRequest
from google.apps.chat_v1.types.space import GetSpaceRequest
from google.apps.chat_v1.types.space import ListSpacesRequest
from google.apps.chat_v1.types.space import ListSpacesResponse
from google.apps.chat_v1.types.space import Space
from google.apps.chat_v1.types.space import UpdateSpaceRequest
from google.apps.chat_v1.types.space_setup import SetUpSpaceRequest
from google.apps.chat_v1.types.user import User
from google.apps.chat_v1.types.widgets import WidgetMarkup

__all__ = ('ChatServiceClient',
    'ChatServiceAsyncClient',
    'ActionStatus',
    'Annotation',
    'DriveLinkData',
    'RichLinkMetadata',
    'SlashCommandMetadata',
    'UserMentionMetadata',
    'AnnotationType',
    'Attachment',
    'AttachmentDataRef',
    'DriveDataRef',
    'GetAttachmentRequest',
    'UploadAttachmentRequest',
    'UploadAttachmentResponse',
    'ContextualAddOnMarkup',
    'DeletionMetadata',
    'Group',
    'HistoryState',
    'MatchedUrl',
    'CreateMembershipRequest',
    'DeleteMembershipRequest',
    'GetMembershipRequest',
    'ListMembershipsRequest',
    'ListMembershipsResponse',
    'Membership',
    'ActionResponse',
    'AttachedGif',
    'CardWithId',
    'CreateMessageRequest',
    'DeleteMessageRequest',
    'Dialog',
    'DialogAction',
    'GetMessageRequest',
    'ListMessagesRequest',
    'ListMessagesResponse',
    'Message',
    'QuotedMessageMetadata',
    'Thread',
    'UpdateMessageRequest',
    'CreateReactionRequest',
    'CustomEmoji',
    'DeleteReactionRequest',
    'Emoji',
    'EmojiReactionSummary',
    'ListReactionsRequest',
    'ListReactionsResponse',
    'Reaction',
    'SlashCommand',
    'CompleteImportSpaceRequest',
    'CompleteImportSpaceResponse',
    'CreateSpaceRequest',
    'DeleteSpaceRequest',
    'FindDirectMessageRequest',
    'GetSpaceRequest',
    'ListSpacesRequest',
    'ListSpacesResponse',
    'Space',
    'UpdateSpaceRequest',
    'SetUpSpaceRequest',
    'User',
    'WidgetMarkup',
)
