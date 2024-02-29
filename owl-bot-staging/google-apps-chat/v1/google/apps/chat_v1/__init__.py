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
from google.apps.chat_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.chat_service import ChatServiceClient
from .services.chat_service import ChatServiceAsyncClient

from .types.action_status import ActionStatus
from .types.annotation import Annotation
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
from .types.group import Group
from .types.history_state import HistoryState
from .types.matched_url import MatchedUrl
from .types.membership import CreateMembershipRequest
from .types.membership import DeleteMembershipRequest
from .types.membership import GetMembershipRequest
from .types.membership import ListMembershipsRequest
from .types.membership import ListMembershipsResponse
from .types.membership import Membership
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
from .types.space_setup import SetUpSpaceRequest
from .types.user import User
from .types.widgets import WidgetMarkup

__all__ = (
    'ChatServiceAsyncClient',
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
'Emoji',
'EmojiReactionSummary',
'FindDirectMessageRequest',
'GetAttachmentRequest',
'GetMembershipRequest',
'GetMessageRequest',
'GetSpaceRequest',
'Group',
'HistoryState',
'ListMembershipsRequest',
'ListMembershipsResponse',
'ListMessagesRequest',
'ListMessagesResponse',
'ListReactionsRequest',
'ListReactionsResponse',
'ListSpacesRequest',
'ListSpacesResponse',
'MatchedUrl',
'Membership',
'Message',
'QuotedMessageMetadata',
'Reaction',
'SetUpSpaceRequest',
'SlashCommand',
'SlashCommandMetadata',
'Space',
'Thread',
'UpdateMessageRequest',
'UpdateSpaceRequest',
'UploadAttachmentRequest',
'UploadAttachmentResponse',
'User',
'UserMentionMetadata',
'WidgetMarkup',
)
