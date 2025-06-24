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
import dataclasses
import json  # type: ignore
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
import google.protobuf
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.apps.chat_v1.types import (
    space_notification_setting as gc_space_notification_setting,
)
from google.apps.chat_v1.types import attachment
from google.apps.chat_v1.types import membership
from google.apps.chat_v1.types import membership as gc_membership
from google.apps.chat_v1.types import message
from google.apps.chat_v1.types import message as gc_message
from google.apps.chat_v1.types import reaction
from google.apps.chat_v1.types import reaction as gc_reaction
from google.apps.chat_v1.types import space
from google.apps.chat_v1.types import space as gc_space
from google.apps.chat_v1.types import space_event
from google.apps.chat_v1.types import space_notification_setting
from google.apps.chat_v1.types import space_read_state
from google.apps.chat_v1.types import space_read_state as gc_space_read_state
from google.apps.chat_v1.types import space_setup, thread_read_state

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseChatServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class ChatServiceRestInterceptor:
    """Interceptor for ChatService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ChatServiceRestTransport.

    .. code-block:: python
        class MyCustomChatServiceInterceptor(ChatServiceRestInterceptor):
            def pre_complete_import_space(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_complete_import_space(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_custom_emoji(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_custom_emoji(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_membership(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_membership(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_message(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_message(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_reaction(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_reaction(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_space(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_space(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_custom_emoji(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_membership(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_membership(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_message(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_reaction(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_space(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_find_direct_message(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_find_direct_message(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_custom_emoji(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_custom_emoji(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_membership(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_membership(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_message(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_message(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_space(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_space(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_space_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_space_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_space_notification_setting(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_space_notification_setting(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_space_read_state(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_space_read_state(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_thread_read_state(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_thread_read_state(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_custom_emojis(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_custom_emojis(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_memberships(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_memberships(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_messages(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_messages(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_reactions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_reactions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_space_events(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_space_events(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_spaces(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_spaces(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_spaces(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_spaces(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_up_space(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_up_space(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_membership(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_membership(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_message(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_message(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_space(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_space(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_space_notification_setting(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_space_notification_setting(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_space_read_state(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_space_read_state(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_upload_attachment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_upload_attachment(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ChatServiceRestTransport(interceptor=MyCustomChatServiceInterceptor())
        client = ChatServiceClient(transport=transport)


    """

    def pre_complete_import_space(
        self,
        request: space.CompleteImportSpaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        space.CompleteImportSpaceRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for complete_import_space

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_complete_import_space(
        self, response: space.CompleteImportSpaceResponse
    ) -> space.CompleteImportSpaceResponse:
        """Post-rpc interceptor for complete_import_space

        DEPRECATED. Please use the `post_complete_import_space_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_complete_import_space` interceptor runs
        before the `post_complete_import_space_with_metadata` interceptor.
        """
        return response

    def post_complete_import_space_with_metadata(
        self,
        response: space.CompleteImportSpaceResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        space.CompleteImportSpaceResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for complete_import_space

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_complete_import_space_with_metadata`
        interceptor in new development instead of the `post_complete_import_space` interceptor.
        When both interceptors are used, this `post_complete_import_space_with_metadata` interceptor runs after the
        `post_complete_import_space` interceptor. The (possibly modified) response returned by
        `post_complete_import_space` will be passed to
        `post_complete_import_space_with_metadata`.
        """
        return response, metadata

    def pre_create_custom_emoji(
        self,
        request: reaction.CreateCustomEmojiRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        reaction.CreateCustomEmojiRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_custom_emoji

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_create_custom_emoji(
        self, response: reaction.CustomEmoji
    ) -> reaction.CustomEmoji:
        """Post-rpc interceptor for create_custom_emoji

        DEPRECATED. Please use the `post_create_custom_emoji_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_create_custom_emoji` interceptor runs
        before the `post_create_custom_emoji_with_metadata` interceptor.
        """
        return response

    def post_create_custom_emoji_with_metadata(
        self,
        response: reaction.CustomEmoji,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[reaction.CustomEmoji, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_custom_emoji

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_create_custom_emoji_with_metadata`
        interceptor in new development instead of the `post_create_custom_emoji` interceptor.
        When both interceptors are used, this `post_create_custom_emoji_with_metadata` interceptor runs after the
        `post_create_custom_emoji` interceptor. The (possibly modified) response returned by
        `post_create_custom_emoji` will be passed to
        `post_create_custom_emoji_with_metadata`.
        """
        return response, metadata

    def pre_create_membership(
        self,
        request: gc_membership.CreateMembershipRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gc_membership.CreateMembershipRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_membership

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_create_membership(
        self, response: gc_membership.Membership
    ) -> gc_membership.Membership:
        """Post-rpc interceptor for create_membership

        DEPRECATED. Please use the `post_create_membership_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_create_membership` interceptor runs
        before the `post_create_membership_with_metadata` interceptor.
        """
        return response

    def post_create_membership_with_metadata(
        self,
        response: gc_membership.Membership,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[gc_membership.Membership, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_membership

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_create_membership_with_metadata`
        interceptor in new development instead of the `post_create_membership` interceptor.
        When both interceptors are used, this `post_create_membership_with_metadata` interceptor runs after the
        `post_create_membership` interceptor. The (possibly modified) response returned by
        `post_create_membership` will be passed to
        `post_create_membership_with_metadata`.
        """
        return response, metadata

    def pre_create_message(
        self,
        request: gc_message.CreateMessageRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gc_message.CreateMessageRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_message

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_create_message(self, response: gc_message.Message) -> gc_message.Message:
        """Post-rpc interceptor for create_message

        DEPRECATED. Please use the `post_create_message_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_create_message` interceptor runs
        before the `post_create_message_with_metadata` interceptor.
        """
        return response

    def post_create_message_with_metadata(
        self,
        response: gc_message.Message,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[gc_message.Message, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_message

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_create_message_with_metadata`
        interceptor in new development instead of the `post_create_message` interceptor.
        When both interceptors are used, this `post_create_message_with_metadata` interceptor runs after the
        `post_create_message` interceptor. The (possibly modified) response returned by
        `post_create_message` will be passed to
        `post_create_message_with_metadata`.
        """
        return response, metadata

    def pre_create_reaction(
        self,
        request: gc_reaction.CreateReactionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gc_reaction.CreateReactionRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for create_reaction

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_create_reaction(
        self, response: gc_reaction.Reaction
    ) -> gc_reaction.Reaction:
        """Post-rpc interceptor for create_reaction

        DEPRECATED. Please use the `post_create_reaction_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_create_reaction` interceptor runs
        before the `post_create_reaction_with_metadata` interceptor.
        """
        return response

    def post_create_reaction_with_metadata(
        self,
        response: gc_reaction.Reaction,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[gc_reaction.Reaction, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_reaction

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_create_reaction_with_metadata`
        interceptor in new development instead of the `post_create_reaction` interceptor.
        When both interceptors are used, this `post_create_reaction_with_metadata` interceptor runs after the
        `post_create_reaction` interceptor. The (possibly modified) response returned by
        `post_create_reaction` will be passed to
        `post_create_reaction_with_metadata`.
        """
        return response, metadata

    def pre_create_space(
        self,
        request: gc_space.CreateSpaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[gc_space.CreateSpaceRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for create_space

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_create_space(self, response: gc_space.Space) -> gc_space.Space:
        """Post-rpc interceptor for create_space

        DEPRECATED. Please use the `post_create_space_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_create_space` interceptor runs
        before the `post_create_space_with_metadata` interceptor.
        """
        return response

    def post_create_space_with_metadata(
        self,
        response: gc_space.Space,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[gc_space.Space, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_space

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_create_space_with_metadata`
        interceptor in new development instead of the `post_create_space` interceptor.
        When both interceptors are used, this `post_create_space_with_metadata` interceptor runs after the
        `post_create_space` interceptor. The (possibly modified) response returned by
        `post_create_space` will be passed to
        `post_create_space_with_metadata`.
        """
        return response, metadata

    def pre_delete_custom_emoji(
        self,
        request: reaction.DeleteCustomEmojiRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        reaction.DeleteCustomEmojiRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_custom_emoji

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def pre_delete_membership(
        self,
        request: membership.DeleteMembershipRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        membership.DeleteMembershipRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_membership

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_delete_membership(
        self, response: membership.Membership
    ) -> membership.Membership:
        """Post-rpc interceptor for delete_membership

        DEPRECATED. Please use the `post_delete_membership_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_delete_membership` interceptor runs
        before the `post_delete_membership_with_metadata` interceptor.
        """
        return response

    def post_delete_membership_with_metadata(
        self,
        response: membership.Membership,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[membership.Membership, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_membership

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_delete_membership_with_metadata`
        interceptor in new development instead of the `post_delete_membership` interceptor.
        When both interceptors are used, this `post_delete_membership_with_metadata` interceptor runs after the
        `post_delete_membership` interceptor. The (possibly modified) response returned by
        `post_delete_membership` will be passed to
        `post_delete_membership_with_metadata`.
        """
        return response, metadata

    def pre_delete_message(
        self,
        request: message.DeleteMessageRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[message.DeleteMessageRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_message

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def pre_delete_reaction(
        self,
        request: reaction.DeleteReactionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[reaction.DeleteReactionRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_reaction

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def pre_delete_space(
        self,
        request: space.DeleteSpaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[space.DeleteSpaceRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_space

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def pre_find_direct_message(
        self,
        request: space.FindDirectMessageRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[space.FindDirectMessageRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for find_direct_message

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_find_direct_message(self, response: space.Space) -> space.Space:
        """Post-rpc interceptor for find_direct_message

        DEPRECATED. Please use the `post_find_direct_message_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_find_direct_message` interceptor runs
        before the `post_find_direct_message_with_metadata` interceptor.
        """
        return response

    def post_find_direct_message_with_metadata(
        self, response: space.Space, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[space.Space, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for find_direct_message

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_find_direct_message_with_metadata`
        interceptor in new development instead of the `post_find_direct_message` interceptor.
        When both interceptors are used, this `post_find_direct_message_with_metadata` interceptor runs after the
        `post_find_direct_message` interceptor. The (possibly modified) response returned by
        `post_find_direct_message` will be passed to
        `post_find_direct_message_with_metadata`.
        """
        return response, metadata

    def pre_get_attachment(
        self,
        request: attachment.GetAttachmentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        attachment.GetAttachmentRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_get_attachment(
        self, response: attachment.Attachment
    ) -> attachment.Attachment:
        """Post-rpc interceptor for get_attachment

        DEPRECATED. Please use the `post_get_attachment_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_get_attachment` interceptor runs
        before the `post_get_attachment_with_metadata` interceptor.
        """
        return response

    def post_get_attachment_with_metadata(
        self,
        response: attachment.Attachment,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[attachment.Attachment, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_attachment

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_get_attachment_with_metadata`
        interceptor in new development instead of the `post_get_attachment` interceptor.
        When both interceptors are used, this `post_get_attachment_with_metadata` interceptor runs after the
        `post_get_attachment` interceptor. The (possibly modified) response returned by
        `post_get_attachment` will be passed to
        `post_get_attachment_with_metadata`.
        """
        return response, metadata

    def pre_get_custom_emoji(
        self,
        request: reaction.GetCustomEmojiRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[reaction.GetCustomEmojiRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_custom_emoji

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_get_custom_emoji(
        self, response: reaction.CustomEmoji
    ) -> reaction.CustomEmoji:
        """Post-rpc interceptor for get_custom_emoji

        DEPRECATED. Please use the `post_get_custom_emoji_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_get_custom_emoji` interceptor runs
        before the `post_get_custom_emoji_with_metadata` interceptor.
        """
        return response

    def post_get_custom_emoji_with_metadata(
        self,
        response: reaction.CustomEmoji,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[reaction.CustomEmoji, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_custom_emoji

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_get_custom_emoji_with_metadata`
        interceptor in new development instead of the `post_get_custom_emoji` interceptor.
        When both interceptors are used, this `post_get_custom_emoji_with_metadata` interceptor runs after the
        `post_get_custom_emoji` interceptor. The (possibly modified) response returned by
        `post_get_custom_emoji` will be passed to
        `post_get_custom_emoji_with_metadata`.
        """
        return response, metadata

    def pre_get_membership(
        self,
        request: membership.GetMembershipRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        membership.GetMembershipRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_membership

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_get_membership(
        self, response: membership.Membership
    ) -> membership.Membership:
        """Post-rpc interceptor for get_membership

        DEPRECATED. Please use the `post_get_membership_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_get_membership` interceptor runs
        before the `post_get_membership_with_metadata` interceptor.
        """
        return response

    def post_get_membership_with_metadata(
        self,
        response: membership.Membership,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[membership.Membership, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_membership

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_get_membership_with_metadata`
        interceptor in new development instead of the `post_get_membership` interceptor.
        When both interceptors are used, this `post_get_membership_with_metadata` interceptor runs after the
        `post_get_membership` interceptor. The (possibly modified) response returned by
        `post_get_membership` will be passed to
        `post_get_membership_with_metadata`.
        """
        return response, metadata

    def pre_get_message(
        self,
        request: message.GetMessageRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[message.GetMessageRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_message

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_get_message(self, response: message.Message) -> message.Message:
        """Post-rpc interceptor for get_message

        DEPRECATED. Please use the `post_get_message_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_get_message` interceptor runs
        before the `post_get_message_with_metadata` interceptor.
        """
        return response

    def post_get_message_with_metadata(
        self,
        response: message.Message,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[message.Message, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_message

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_get_message_with_metadata`
        interceptor in new development instead of the `post_get_message` interceptor.
        When both interceptors are used, this `post_get_message_with_metadata` interceptor runs after the
        `post_get_message` interceptor. The (possibly modified) response returned by
        `post_get_message` will be passed to
        `post_get_message_with_metadata`.
        """
        return response, metadata

    def pre_get_space(
        self,
        request: space.GetSpaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[space.GetSpaceRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_space

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_get_space(self, response: space.Space) -> space.Space:
        """Post-rpc interceptor for get_space

        DEPRECATED. Please use the `post_get_space_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_get_space` interceptor runs
        before the `post_get_space_with_metadata` interceptor.
        """
        return response

    def post_get_space_with_metadata(
        self, response: space.Space, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[space.Space, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_space

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_get_space_with_metadata`
        interceptor in new development instead of the `post_get_space` interceptor.
        When both interceptors are used, this `post_get_space_with_metadata` interceptor runs after the
        `post_get_space` interceptor. The (possibly modified) response returned by
        `post_get_space` will be passed to
        `post_get_space_with_metadata`.
        """
        return response, metadata

    def pre_get_space_event(
        self,
        request: space_event.GetSpaceEventRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        space_event.GetSpaceEventRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_space_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_get_space_event(
        self, response: space_event.SpaceEvent
    ) -> space_event.SpaceEvent:
        """Post-rpc interceptor for get_space_event

        DEPRECATED. Please use the `post_get_space_event_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_get_space_event` interceptor runs
        before the `post_get_space_event_with_metadata` interceptor.
        """
        return response

    def post_get_space_event_with_metadata(
        self,
        response: space_event.SpaceEvent,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[space_event.SpaceEvent, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_space_event

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_get_space_event_with_metadata`
        interceptor in new development instead of the `post_get_space_event` interceptor.
        When both interceptors are used, this `post_get_space_event_with_metadata` interceptor runs after the
        `post_get_space_event` interceptor. The (possibly modified) response returned by
        `post_get_space_event` will be passed to
        `post_get_space_event_with_metadata`.
        """
        return response, metadata

    def pre_get_space_notification_setting(
        self,
        request: space_notification_setting.GetSpaceNotificationSettingRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        space_notification_setting.GetSpaceNotificationSettingRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_space_notification_setting

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_get_space_notification_setting(
        self, response: space_notification_setting.SpaceNotificationSetting
    ) -> space_notification_setting.SpaceNotificationSetting:
        """Post-rpc interceptor for get_space_notification_setting

        DEPRECATED. Please use the `post_get_space_notification_setting_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_get_space_notification_setting` interceptor runs
        before the `post_get_space_notification_setting_with_metadata` interceptor.
        """
        return response

    def post_get_space_notification_setting_with_metadata(
        self,
        response: space_notification_setting.SpaceNotificationSetting,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        space_notification_setting.SpaceNotificationSetting,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for get_space_notification_setting

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_get_space_notification_setting_with_metadata`
        interceptor in new development instead of the `post_get_space_notification_setting` interceptor.
        When both interceptors are used, this `post_get_space_notification_setting_with_metadata` interceptor runs after the
        `post_get_space_notification_setting` interceptor. The (possibly modified) response returned by
        `post_get_space_notification_setting` will be passed to
        `post_get_space_notification_setting_with_metadata`.
        """
        return response, metadata

    def pre_get_space_read_state(
        self,
        request: space_read_state.GetSpaceReadStateRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        space_read_state.GetSpaceReadStateRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_space_read_state

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_get_space_read_state(
        self, response: space_read_state.SpaceReadState
    ) -> space_read_state.SpaceReadState:
        """Post-rpc interceptor for get_space_read_state

        DEPRECATED. Please use the `post_get_space_read_state_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_get_space_read_state` interceptor runs
        before the `post_get_space_read_state_with_metadata` interceptor.
        """
        return response

    def post_get_space_read_state_with_metadata(
        self,
        response: space_read_state.SpaceReadState,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        space_read_state.SpaceReadState, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for get_space_read_state

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_get_space_read_state_with_metadata`
        interceptor in new development instead of the `post_get_space_read_state` interceptor.
        When both interceptors are used, this `post_get_space_read_state_with_metadata` interceptor runs after the
        `post_get_space_read_state` interceptor. The (possibly modified) response returned by
        `post_get_space_read_state` will be passed to
        `post_get_space_read_state_with_metadata`.
        """
        return response, metadata

    def pre_get_thread_read_state(
        self,
        request: thread_read_state.GetThreadReadStateRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        thread_read_state.GetThreadReadStateRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_thread_read_state

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_get_thread_read_state(
        self, response: thread_read_state.ThreadReadState
    ) -> thread_read_state.ThreadReadState:
        """Post-rpc interceptor for get_thread_read_state

        DEPRECATED. Please use the `post_get_thread_read_state_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_get_thread_read_state` interceptor runs
        before the `post_get_thread_read_state_with_metadata` interceptor.
        """
        return response

    def post_get_thread_read_state_with_metadata(
        self,
        response: thread_read_state.ThreadReadState,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        thread_read_state.ThreadReadState, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for get_thread_read_state

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_get_thread_read_state_with_metadata`
        interceptor in new development instead of the `post_get_thread_read_state` interceptor.
        When both interceptors are used, this `post_get_thread_read_state_with_metadata` interceptor runs after the
        `post_get_thread_read_state` interceptor. The (possibly modified) response returned by
        `post_get_thread_read_state` will be passed to
        `post_get_thread_read_state_with_metadata`.
        """
        return response, metadata

    def pre_list_custom_emojis(
        self,
        request: reaction.ListCustomEmojisRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        reaction.ListCustomEmojisRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_custom_emojis

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_list_custom_emojis(
        self, response: reaction.ListCustomEmojisResponse
    ) -> reaction.ListCustomEmojisResponse:
        """Post-rpc interceptor for list_custom_emojis

        DEPRECATED. Please use the `post_list_custom_emojis_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_list_custom_emojis` interceptor runs
        before the `post_list_custom_emojis_with_metadata` interceptor.
        """
        return response

    def post_list_custom_emojis_with_metadata(
        self,
        response: reaction.ListCustomEmojisResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        reaction.ListCustomEmojisResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_custom_emojis

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_list_custom_emojis_with_metadata`
        interceptor in new development instead of the `post_list_custom_emojis` interceptor.
        When both interceptors are used, this `post_list_custom_emojis_with_metadata` interceptor runs after the
        `post_list_custom_emojis` interceptor. The (possibly modified) response returned by
        `post_list_custom_emojis` will be passed to
        `post_list_custom_emojis_with_metadata`.
        """
        return response, metadata

    def pre_list_memberships(
        self,
        request: membership.ListMembershipsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        membership.ListMembershipsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_memberships

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_list_memberships(
        self, response: membership.ListMembershipsResponse
    ) -> membership.ListMembershipsResponse:
        """Post-rpc interceptor for list_memberships

        DEPRECATED. Please use the `post_list_memberships_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_list_memberships` interceptor runs
        before the `post_list_memberships_with_metadata` interceptor.
        """
        return response

    def post_list_memberships_with_metadata(
        self,
        response: membership.ListMembershipsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        membership.ListMembershipsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_memberships

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_list_memberships_with_metadata`
        interceptor in new development instead of the `post_list_memberships` interceptor.
        When both interceptors are used, this `post_list_memberships_with_metadata` interceptor runs after the
        `post_list_memberships` interceptor. The (possibly modified) response returned by
        `post_list_memberships` will be passed to
        `post_list_memberships_with_metadata`.
        """
        return response, metadata

    def pre_list_messages(
        self,
        request: message.ListMessagesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[message.ListMessagesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_messages

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_list_messages(
        self, response: message.ListMessagesResponse
    ) -> message.ListMessagesResponse:
        """Post-rpc interceptor for list_messages

        DEPRECATED. Please use the `post_list_messages_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_list_messages` interceptor runs
        before the `post_list_messages_with_metadata` interceptor.
        """
        return response

    def post_list_messages_with_metadata(
        self,
        response: message.ListMessagesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[message.ListMessagesResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_messages

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_list_messages_with_metadata`
        interceptor in new development instead of the `post_list_messages` interceptor.
        When both interceptors are used, this `post_list_messages_with_metadata` interceptor runs after the
        `post_list_messages` interceptor. The (possibly modified) response returned by
        `post_list_messages` will be passed to
        `post_list_messages_with_metadata`.
        """
        return response, metadata

    def pre_list_reactions(
        self,
        request: reaction.ListReactionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[reaction.ListReactionsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_reactions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_list_reactions(
        self, response: reaction.ListReactionsResponse
    ) -> reaction.ListReactionsResponse:
        """Post-rpc interceptor for list_reactions

        DEPRECATED. Please use the `post_list_reactions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_list_reactions` interceptor runs
        before the `post_list_reactions_with_metadata` interceptor.
        """
        return response

    def post_list_reactions_with_metadata(
        self,
        response: reaction.ListReactionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[reaction.ListReactionsResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_reactions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_list_reactions_with_metadata`
        interceptor in new development instead of the `post_list_reactions` interceptor.
        When both interceptors are used, this `post_list_reactions_with_metadata` interceptor runs after the
        `post_list_reactions` interceptor. The (possibly modified) response returned by
        `post_list_reactions` will be passed to
        `post_list_reactions_with_metadata`.
        """
        return response, metadata

    def pre_list_space_events(
        self,
        request: space_event.ListSpaceEventsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        space_event.ListSpaceEventsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_space_events

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_list_space_events(
        self, response: space_event.ListSpaceEventsResponse
    ) -> space_event.ListSpaceEventsResponse:
        """Post-rpc interceptor for list_space_events

        DEPRECATED. Please use the `post_list_space_events_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_list_space_events` interceptor runs
        before the `post_list_space_events_with_metadata` interceptor.
        """
        return response

    def post_list_space_events_with_metadata(
        self,
        response: space_event.ListSpaceEventsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        space_event.ListSpaceEventsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_space_events

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_list_space_events_with_metadata`
        interceptor in new development instead of the `post_list_space_events` interceptor.
        When both interceptors are used, this `post_list_space_events_with_metadata` interceptor runs after the
        `post_list_space_events` interceptor. The (possibly modified) response returned by
        `post_list_space_events` will be passed to
        `post_list_space_events_with_metadata`.
        """
        return response, metadata

    def pre_list_spaces(
        self,
        request: space.ListSpacesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[space.ListSpacesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_spaces

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_list_spaces(
        self, response: space.ListSpacesResponse
    ) -> space.ListSpacesResponse:
        """Post-rpc interceptor for list_spaces

        DEPRECATED. Please use the `post_list_spaces_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_list_spaces` interceptor runs
        before the `post_list_spaces_with_metadata` interceptor.
        """
        return response

    def post_list_spaces_with_metadata(
        self,
        response: space.ListSpacesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[space.ListSpacesResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for list_spaces

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_list_spaces_with_metadata`
        interceptor in new development instead of the `post_list_spaces` interceptor.
        When both interceptors are used, this `post_list_spaces_with_metadata` interceptor runs after the
        `post_list_spaces` interceptor. The (possibly modified) response returned by
        `post_list_spaces` will be passed to
        `post_list_spaces_with_metadata`.
        """
        return response, metadata

    def pre_search_spaces(
        self,
        request: space.SearchSpacesRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[space.SearchSpacesRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for search_spaces

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_search_spaces(
        self, response: space.SearchSpacesResponse
    ) -> space.SearchSpacesResponse:
        """Post-rpc interceptor for search_spaces

        DEPRECATED. Please use the `post_search_spaces_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_search_spaces` interceptor runs
        before the `post_search_spaces_with_metadata` interceptor.
        """
        return response

    def post_search_spaces_with_metadata(
        self,
        response: space.SearchSpacesResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[space.SearchSpacesResponse, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for search_spaces

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_search_spaces_with_metadata`
        interceptor in new development instead of the `post_search_spaces` interceptor.
        When both interceptors are used, this `post_search_spaces_with_metadata` interceptor runs after the
        `post_search_spaces` interceptor. The (possibly modified) response returned by
        `post_search_spaces` will be passed to
        `post_search_spaces_with_metadata`.
        """
        return response, metadata

    def pre_set_up_space(
        self,
        request: space_setup.SetUpSpaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[space_setup.SetUpSpaceRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for set_up_space

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_set_up_space(self, response: space.Space) -> space.Space:
        """Post-rpc interceptor for set_up_space

        DEPRECATED. Please use the `post_set_up_space_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_set_up_space` interceptor runs
        before the `post_set_up_space_with_metadata` interceptor.
        """
        return response

    def post_set_up_space_with_metadata(
        self, response: space.Space, metadata: Sequence[Tuple[str, Union[str, bytes]]]
    ) -> Tuple[space.Space, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for set_up_space

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_set_up_space_with_metadata`
        interceptor in new development instead of the `post_set_up_space` interceptor.
        When both interceptors are used, this `post_set_up_space_with_metadata` interceptor runs after the
        `post_set_up_space` interceptor. The (possibly modified) response returned by
        `post_set_up_space` will be passed to
        `post_set_up_space_with_metadata`.
        """
        return response, metadata

    def pre_update_membership(
        self,
        request: gc_membership.UpdateMembershipRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gc_membership.UpdateMembershipRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_membership

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_update_membership(
        self, response: gc_membership.Membership
    ) -> gc_membership.Membership:
        """Post-rpc interceptor for update_membership

        DEPRECATED. Please use the `post_update_membership_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_update_membership` interceptor runs
        before the `post_update_membership_with_metadata` interceptor.
        """
        return response

    def post_update_membership_with_metadata(
        self,
        response: gc_membership.Membership,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[gc_membership.Membership, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_membership

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_update_membership_with_metadata`
        interceptor in new development instead of the `post_update_membership` interceptor.
        When both interceptors are used, this `post_update_membership_with_metadata` interceptor runs after the
        `post_update_membership` interceptor. The (possibly modified) response returned by
        `post_update_membership` will be passed to
        `post_update_membership_with_metadata`.
        """
        return response, metadata

    def pre_update_message(
        self,
        request: gc_message.UpdateMessageRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gc_message.UpdateMessageRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for update_message

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_update_message(self, response: gc_message.Message) -> gc_message.Message:
        """Post-rpc interceptor for update_message

        DEPRECATED. Please use the `post_update_message_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_update_message` interceptor runs
        before the `post_update_message_with_metadata` interceptor.
        """
        return response

    def post_update_message_with_metadata(
        self,
        response: gc_message.Message,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[gc_message.Message, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_message

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_update_message_with_metadata`
        interceptor in new development instead of the `post_update_message` interceptor.
        When both interceptors are used, this `post_update_message_with_metadata` interceptor runs after the
        `post_update_message` interceptor. The (possibly modified) response returned by
        `post_update_message` will be passed to
        `post_update_message_with_metadata`.
        """
        return response, metadata

    def pre_update_space(
        self,
        request: gc_space.UpdateSpaceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[gc_space.UpdateSpaceRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for update_space

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_update_space(self, response: gc_space.Space) -> gc_space.Space:
        """Post-rpc interceptor for update_space

        DEPRECATED. Please use the `post_update_space_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_update_space` interceptor runs
        before the `post_update_space_with_metadata` interceptor.
        """
        return response

    def post_update_space_with_metadata(
        self,
        response: gc_space.Space,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[gc_space.Space, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_space

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_update_space_with_metadata`
        interceptor in new development instead of the `post_update_space` interceptor.
        When both interceptors are used, this `post_update_space_with_metadata` interceptor runs after the
        `post_update_space` interceptor. The (possibly modified) response returned by
        `post_update_space` will be passed to
        `post_update_space_with_metadata`.
        """
        return response, metadata

    def pre_update_space_notification_setting(
        self,
        request: gc_space_notification_setting.UpdateSpaceNotificationSettingRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gc_space_notification_setting.UpdateSpaceNotificationSettingRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_space_notification_setting

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_update_space_notification_setting(
        self, response: gc_space_notification_setting.SpaceNotificationSetting
    ) -> gc_space_notification_setting.SpaceNotificationSetting:
        """Post-rpc interceptor for update_space_notification_setting

        DEPRECATED. Please use the `post_update_space_notification_setting_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_update_space_notification_setting` interceptor runs
        before the `post_update_space_notification_setting_with_metadata` interceptor.
        """
        return response

    def post_update_space_notification_setting_with_metadata(
        self,
        response: gc_space_notification_setting.SpaceNotificationSetting,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gc_space_notification_setting.SpaceNotificationSetting,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for update_space_notification_setting

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_update_space_notification_setting_with_metadata`
        interceptor in new development instead of the `post_update_space_notification_setting` interceptor.
        When both interceptors are used, this `post_update_space_notification_setting_with_metadata` interceptor runs after the
        `post_update_space_notification_setting` interceptor. The (possibly modified) response returned by
        `post_update_space_notification_setting` will be passed to
        `post_update_space_notification_setting_with_metadata`.
        """
        return response, metadata

    def pre_update_space_read_state(
        self,
        request: gc_space_read_state.UpdateSpaceReadStateRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gc_space_read_state.UpdateSpaceReadStateRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_space_read_state

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_update_space_read_state(
        self, response: gc_space_read_state.SpaceReadState
    ) -> gc_space_read_state.SpaceReadState:
        """Post-rpc interceptor for update_space_read_state

        DEPRECATED. Please use the `post_update_space_read_state_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_update_space_read_state` interceptor runs
        before the `post_update_space_read_state_with_metadata` interceptor.
        """
        return response

    def post_update_space_read_state_with_metadata(
        self,
        response: gc_space_read_state.SpaceReadState,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        gc_space_read_state.SpaceReadState, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for update_space_read_state

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_update_space_read_state_with_metadata`
        interceptor in new development instead of the `post_update_space_read_state` interceptor.
        When both interceptors are used, this `post_update_space_read_state_with_metadata` interceptor runs after the
        `post_update_space_read_state` interceptor. The (possibly modified) response returned by
        `post_update_space_read_state` will be passed to
        `post_update_space_read_state_with_metadata`.
        """
        return response, metadata

    def pre_upload_attachment(
        self,
        request: attachment.UploadAttachmentRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        attachment.UploadAttachmentRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for upload_attachment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ChatService server.
        """
        return request, metadata

    def post_upload_attachment(
        self, response: attachment.UploadAttachmentResponse
    ) -> attachment.UploadAttachmentResponse:
        """Post-rpc interceptor for upload_attachment

        DEPRECATED. Please use the `post_upload_attachment_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the ChatService server but before
        it is returned to user code. This `post_upload_attachment` interceptor runs
        before the `post_upload_attachment_with_metadata` interceptor.
        """
        return response

    def post_upload_attachment_with_metadata(
        self,
        response: attachment.UploadAttachmentResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        attachment.UploadAttachmentResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for upload_attachment

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the ChatService server but before it is returned to user code.

        We recommend only using this `post_upload_attachment_with_metadata`
        interceptor in new development instead of the `post_upload_attachment` interceptor.
        When both interceptors are used, this `post_upload_attachment_with_metadata` interceptor runs after the
        `post_upload_attachment` interceptor. The (possibly modified) response returned by
        `post_upload_attachment` will be passed to
        `post_upload_attachment_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class ChatServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ChatServiceRestInterceptor


class ChatServiceRestTransport(_BaseChatServiceRestTransport):
    """REST backend synchronous transport for ChatService.

    Enables developers to build Chat apps and
    integrations on Google Chat Platform.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "chat.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ChatServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'chat.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ChatServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CompleteImportSpace(
        _BaseChatServiceRestTransport._BaseCompleteImportSpace, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.CompleteImportSpace")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: space.CompleteImportSpaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> space.CompleteImportSpaceResponse:
            r"""Call the complete import space method over HTTP.

            Args:
                request (~.space.CompleteImportSpaceRequest):
                    The request object. Request message for completing the
                import process for a space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.space.CompleteImportSpaceResponse:
                    Response message for completing the
                import process for a space.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseCompleteImportSpace._get_http_options()
            )

            request, metadata = self._interceptor.pre_complete_import_space(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseCompleteImportSpace._get_transcoded_request(
                http_options, request
            )

            body = _BaseChatServiceRestTransport._BaseCompleteImportSpace._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseCompleteImportSpace._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.CompleteImportSpace",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CompleteImportSpace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._CompleteImportSpace._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = space.CompleteImportSpaceResponse()
            pb_resp = space.CompleteImportSpaceResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_complete_import_space(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_complete_import_space_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = space.CompleteImportSpaceResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.complete_import_space",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CompleteImportSpace",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateCustomEmoji(
        _BaseChatServiceRestTransport._BaseCreateCustomEmoji, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.CreateCustomEmoji")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: reaction.CreateCustomEmojiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> reaction.CustomEmoji:
            r"""Call the create custom emoji method over HTTP.

            Args:
                request (~.reaction.CreateCustomEmojiRequest):
                    The request object. A request to create a custom emoji.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.reaction.CustomEmoji:
                    Represents a `custom
                emoji <https://support.google.com/chat/answer/12800149>`__.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseCreateCustomEmoji._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_custom_emoji(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseCreateCustomEmoji._get_transcoded_request(
                http_options, request
            )

            body = _BaseChatServiceRestTransport._BaseCreateCustomEmoji._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseCreateCustomEmoji._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.CreateCustomEmoji",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CreateCustomEmoji",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._CreateCustomEmoji._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = reaction.CustomEmoji()
            pb_resp = reaction.CustomEmoji.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_custom_emoji(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_custom_emoji_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = reaction.CustomEmoji.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.create_custom_emoji",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CreateCustomEmoji",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateMembership(
        _BaseChatServiceRestTransport._BaseCreateMembership, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.CreateMembership")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gc_membership.CreateMembershipRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gc_membership.Membership:
            r"""Call the create membership method over HTTP.

            Args:
                request (~.gc_membership.CreateMembershipRequest):
                    The request object. Request message for creating a
                membership.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.gc_membership.Membership:
                    Represents a membership relation in
                Google Chat, such as whether a user or
                Chat app is invited to, part of, or
                absent from a space.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseCreateMembership._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_membership(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseCreateMembership._get_transcoded_request(
                http_options, request
            )

            body = _BaseChatServiceRestTransport._BaseCreateMembership._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseCreateMembership._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.CreateMembership",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CreateMembership",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._CreateMembership._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gc_membership.Membership()
            pb_resp = gc_membership.Membership.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_membership(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_membership_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = gc_membership.Membership.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.create_membership",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CreateMembership",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateMessage(
        _BaseChatServiceRestTransport._BaseCreateMessage, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.CreateMessage")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gc_message.CreateMessageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gc_message.Message:
            r"""Call the create message method over HTTP.

            Args:
                request (~.gc_message.CreateMessageRequest):
                    The request object. Creates a message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.gc_message.Message:
                    A message in a Google Chat space.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseCreateMessage._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_message(request, metadata)
            transcoded_request = _BaseChatServiceRestTransport._BaseCreateMessage._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseChatServiceRestTransport._BaseCreateMessage._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseCreateMessage._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.CreateMessage",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CreateMessage",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._CreateMessage._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gc_message.Message()
            pb_resp = gc_message.Message.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_message(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_message_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = gc_message.Message.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.create_message",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CreateMessage",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateReaction(
        _BaseChatServiceRestTransport._BaseCreateReaction, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.CreateReaction")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gc_reaction.CreateReactionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gc_reaction.Reaction:
            r"""Call the create reaction method over HTTP.

            Args:
                request (~.gc_reaction.CreateReactionRequest):
                    The request object. Creates a reaction to a message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.gc_reaction.Reaction:
                    A reaction to a message.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseCreateReaction._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_reaction(request, metadata)
            transcoded_request = _BaseChatServiceRestTransport._BaseCreateReaction._get_transcoded_request(
                http_options, request
            )

            body = _BaseChatServiceRestTransport._BaseCreateReaction._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseCreateReaction._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.CreateReaction",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CreateReaction",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._CreateReaction._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gc_reaction.Reaction()
            pb_resp = gc_reaction.Reaction.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_reaction(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_reaction_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = gc_reaction.Reaction.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.create_reaction",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CreateReaction",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateSpace(
        _BaseChatServiceRestTransport._BaseCreateSpace, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.CreateSpace")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gc_space.CreateSpaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gc_space.Space:
            r"""Call the create space method over HTTP.

            Args:
                request (~.gc_space.CreateSpaceRequest):
                    The request object. A request to create a named space
                with no members.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.gc_space.Space:
                    A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseCreateSpace._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_space(request, metadata)
            transcoded_request = (
                _BaseChatServiceRestTransport._BaseCreateSpace._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseChatServiceRestTransport._BaseCreateSpace._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseCreateSpace._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.CreateSpace",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CreateSpace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._CreateSpace._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gc_space.Space()
            pb_resp = gc_space.Space.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_space(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_space_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = gc_space.Space.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.create_space",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "CreateSpace",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteCustomEmoji(
        _BaseChatServiceRestTransport._BaseDeleteCustomEmoji, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.DeleteCustomEmoji")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: reaction.DeleteCustomEmojiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete custom emoji method over HTTP.

            Args:
                request (~.reaction.DeleteCustomEmojiRequest):
                    The request object. Request for deleting a custom emoji.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseDeleteCustomEmoji._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_custom_emoji(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseDeleteCustomEmoji._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseDeleteCustomEmoji._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.DeleteCustomEmoji",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "DeleteCustomEmoji",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._DeleteCustomEmoji._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteMembership(
        _BaseChatServiceRestTransport._BaseDeleteMembership, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.DeleteMembership")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: membership.DeleteMembershipRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> membership.Membership:
            r"""Call the delete membership method over HTTP.

            Args:
                request (~.membership.DeleteMembershipRequest):
                    The request object. Request to delete a membership in a
                space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.membership.Membership:
                    Represents a membership relation in
                Google Chat, such as whether a user or
                Chat app is invited to, part of, or
                absent from a space.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseDeleteMembership._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_membership(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseDeleteMembership._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseDeleteMembership._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.DeleteMembership",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "DeleteMembership",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._DeleteMembership._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = membership.Membership()
            pb_resp = membership.Membership.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete_membership(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_membership_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = membership.Membership.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.delete_membership",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "DeleteMembership",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteMessage(
        _BaseChatServiceRestTransport._BaseDeleteMessage, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.DeleteMessage")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: message.DeleteMessageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete message method over HTTP.

            Args:
                request (~.message.DeleteMessageRequest):
                    The request object. Request to delete a message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseDeleteMessage._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_message(request, metadata)
            transcoded_request = _BaseChatServiceRestTransport._BaseDeleteMessage._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseDeleteMessage._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.DeleteMessage",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "DeleteMessage",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._DeleteMessage._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteReaction(
        _BaseChatServiceRestTransport._BaseDeleteReaction, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.DeleteReaction")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: reaction.DeleteReactionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete reaction method over HTTP.

            Args:
                request (~.reaction.DeleteReactionRequest):
                    The request object. Deletes a reaction to a message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseDeleteReaction._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_reaction(request, metadata)
            transcoded_request = _BaseChatServiceRestTransport._BaseDeleteReaction._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseDeleteReaction._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.DeleteReaction",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "DeleteReaction",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._DeleteReaction._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteSpace(
        _BaseChatServiceRestTransport._BaseDeleteSpace, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.DeleteSpace")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: space.DeleteSpaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete space method over HTTP.

            Args:
                request (~.space.DeleteSpaceRequest):
                    The request object. Request for deleting a space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseDeleteSpace._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_space(request, metadata)
            transcoded_request = (
                _BaseChatServiceRestTransport._BaseDeleteSpace._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseDeleteSpace._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.DeleteSpace",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "DeleteSpace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._DeleteSpace._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _FindDirectMessage(
        _BaseChatServiceRestTransport._BaseFindDirectMessage, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.FindDirectMessage")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: space.FindDirectMessageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> space.Space:
            r"""Call the find direct message method over HTTP.

            Args:
                request (~.space.FindDirectMessageRequest):
                    The request object. A request to get direct message space
                based on the user resource.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.space.Space:
                    A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseFindDirectMessage._get_http_options()
            )

            request, metadata = self._interceptor.pre_find_direct_message(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseFindDirectMessage._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseFindDirectMessage._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.FindDirectMessage",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "FindDirectMessage",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._FindDirectMessage._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = space.Space()
            pb_resp = space.Space.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_find_direct_message(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_find_direct_message_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = space.Space.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.find_direct_message",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "FindDirectMessage",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetAttachment(
        _BaseChatServiceRestTransport._BaseGetAttachment, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.GetAttachment")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: attachment.GetAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> attachment.Attachment:
            r"""Call the get attachment method over HTTP.

            Args:
                request (~.attachment.GetAttachmentRequest):
                    The request object. Request to get an attachment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.attachment.Attachment:
                    An attachment in Google Chat.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseGetAttachment._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_attachment(request, metadata)
            transcoded_request = _BaseChatServiceRestTransport._BaseGetAttachment._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseGetAttachment._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.GetAttachment",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetAttachment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._GetAttachment._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = attachment.Attachment()
            pb_resp = attachment.Attachment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_attachment(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_attachment_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = attachment.Attachment.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.get_attachment",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetAttachment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetCustomEmoji(
        _BaseChatServiceRestTransport._BaseGetCustomEmoji, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.GetCustomEmoji")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: reaction.GetCustomEmojiRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> reaction.CustomEmoji:
            r"""Call the get custom emoji method over HTTP.

            Args:
                request (~.reaction.GetCustomEmojiRequest):
                    The request object. A request to return a single custom
                emoji.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.reaction.CustomEmoji:
                    Represents a `custom
                emoji <https://support.google.com/chat/answer/12800149>`__.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseGetCustomEmoji._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_custom_emoji(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseGetCustomEmoji._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseGetCustomEmoji._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.GetCustomEmoji",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetCustomEmoji",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._GetCustomEmoji._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = reaction.CustomEmoji()
            pb_resp = reaction.CustomEmoji.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_custom_emoji(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_custom_emoji_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = reaction.CustomEmoji.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.get_custom_emoji",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetCustomEmoji",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetMembership(
        _BaseChatServiceRestTransport._BaseGetMembership, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.GetMembership")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: membership.GetMembershipRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> membership.Membership:
            r"""Call the get membership method over HTTP.

            Args:
                request (~.membership.GetMembershipRequest):
                    The request object. Request to get a membership of a
                space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.membership.Membership:
                    Represents a membership relation in
                Google Chat, such as whether a user or
                Chat app is invited to, part of, or
                absent from a space.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseGetMembership._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_membership(request, metadata)
            transcoded_request = _BaseChatServiceRestTransport._BaseGetMembership._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseGetMembership._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.GetMembership",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetMembership",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._GetMembership._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = membership.Membership()
            pb_resp = membership.Membership.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_membership(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_membership_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = membership.Membership.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.get_membership",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetMembership",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetMessage(
        _BaseChatServiceRestTransport._BaseGetMessage, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.GetMessage")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: message.GetMessageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> message.Message:
            r"""Call the get message method over HTTP.

            Args:
                request (~.message.GetMessageRequest):
                    The request object. Request to get a message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.message.Message:
                    A message in a Google Chat space.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseGetMessage._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_message(request, metadata)
            transcoded_request = (
                _BaseChatServiceRestTransport._BaseGetMessage._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseGetMessage._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.GetMessage",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetMessage",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._GetMessage._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = message.Message()
            pb_resp = message.Message.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_message(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_message_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = message.Message.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.get_message",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetMessage",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetSpace(_BaseChatServiceRestTransport._BaseGetSpace, ChatServiceRestStub):
        def __hash__(self):
            return hash("ChatServiceRestTransport.GetSpace")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: space.GetSpaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> space.Space:
            r"""Call the get space method over HTTP.

            Args:
                request (~.space.GetSpaceRequest):
                    The request object. A request to return a single space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.space.Space:
                    A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseGetSpace._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_space(request, metadata)
            transcoded_request = (
                _BaseChatServiceRestTransport._BaseGetSpace._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseGetSpace._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.GetSpace",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetSpace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._GetSpace._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = space.Space()
            pb_resp = space.Space.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_space(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_space_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = space.Space.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.get_space",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetSpace",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetSpaceEvent(
        _BaseChatServiceRestTransport._BaseGetSpaceEvent, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.GetSpaceEvent")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: space_event.GetSpaceEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> space_event.SpaceEvent:
            r"""Call the get space event method over HTTP.

            Args:
                request (~.space_event.GetSpaceEventRequest):
                    The request object. Request message for getting a space
                event.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.space_event.SpaceEvent:
                    An event that represents a change or activity in a
                Google Chat space. To learn more, see `Work with events
                from Google
                Chat <https://developers.google.com/workspace/chat/events-overview>`__.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseGetSpaceEvent._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_space_event(request, metadata)
            transcoded_request = _BaseChatServiceRestTransport._BaseGetSpaceEvent._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseGetSpaceEvent._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.GetSpaceEvent",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetSpaceEvent",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._GetSpaceEvent._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = space_event.SpaceEvent()
            pb_resp = space_event.SpaceEvent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_space_event(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_space_event_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = space_event.SpaceEvent.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.get_space_event",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetSpaceEvent",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetSpaceNotificationSetting(
        _BaseChatServiceRestTransport._BaseGetSpaceNotificationSetting,
        ChatServiceRestStub,
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.GetSpaceNotificationSetting")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: space_notification_setting.GetSpaceNotificationSettingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> space_notification_setting.SpaceNotificationSetting:
            r"""Call the get space notification
            setting method over HTTP.

                Args:
                    request (~.space_notification_setting.GetSpaceNotificationSettingRequest):
                        The request object. Request message to get space
                    notification setting. Only supports
                    getting notification setting for the
                    calling user.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.space_notification_setting.SpaceNotificationSetting:
                        The notification setting of a user in
                    a space.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseGetSpaceNotificationSetting._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_space_notification_setting(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseGetSpaceNotificationSetting._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseGetSpaceNotificationSetting._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.GetSpaceNotificationSetting",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetSpaceNotificationSetting",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ChatServiceRestTransport._GetSpaceNotificationSetting._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = space_notification_setting.SpaceNotificationSetting()
            pb_resp = space_notification_setting.SpaceNotificationSetting.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_space_notification_setting(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_get_space_notification_setting_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        space_notification_setting.SpaceNotificationSetting.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.get_space_notification_setting",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetSpaceNotificationSetting",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetSpaceReadState(
        _BaseChatServiceRestTransport._BaseGetSpaceReadState, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.GetSpaceReadState")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: space_read_state.GetSpaceReadStateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> space_read_state.SpaceReadState:
            r"""Call the get space read state method over HTTP.

            Args:
                request (~.space_read_state.GetSpaceReadStateRequest):
                    The request object. Request message for GetSpaceReadState
                API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.space_read_state.SpaceReadState:
                    A user's read state within a space,
                used to identify read and unread
                messages.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseGetSpaceReadState._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_space_read_state(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseGetSpaceReadState._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseGetSpaceReadState._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.GetSpaceReadState",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetSpaceReadState",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._GetSpaceReadState._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = space_read_state.SpaceReadState()
            pb_resp = space_read_state.SpaceReadState.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_space_read_state(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_space_read_state_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = space_read_state.SpaceReadState.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.get_space_read_state",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetSpaceReadState",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetThreadReadState(
        _BaseChatServiceRestTransport._BaseGetThreadReadState, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.GetThreadReadState")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: thread_read_state.GetThreadReadStateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> thread_read_state.ThreadReadState:
            r"""Call the get thread read state method over HTTP.

            Args:
                request (~.thread_read_state.GetThreadReadStateRequest):
                    The request object. Request message for
                GetThreadReadStateRequest API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.thread_read_state.ThreadReadState:
                    A user's read state within a thread,
                used to identify read and unread
                messages.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseGetThreadReadState._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_thread_read_state(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseGetThreadReadState._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseGetThreadReadState._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.GetThreadReadState",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetThreadReadState",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._GetThreadReadState._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = thread_read_state.ThreadReadState()
            pb_resp = thread_read_state.ThreadReadState.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_thread_read_state(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_thread_read_state_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = thread_read_state.ThreadReadState.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.get_thread_read_state",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "GetThreadReadState",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListCustomEmojis(
        _BaseChatServiceRestTransport._BaseListCustomEmojis, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.ListCustomEmojis")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: reaction.ListCustomEmojisRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> reaction.ListCustomEmojisResponse:
            r"""Call the list custom emojis method over HTTP.

            Args:
                request (~.reaction.ListCustomEmojisRequest):
                    The request object. A request to return a list of custom
                emojis.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.reaction.ListCustomEmojisResponse:
                    A response to list custom emojis.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseListCustomEmojis._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_custom_emojis(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseListCustomEmojis._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseListCustomEmojis._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.ListCustomEmojis",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListCustomEmojis",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._ListCustomEmojis._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = reaction.ListCustomEmojisResponse()
            pb_resp = reaction.ListCustomEmojisResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_custom_emojis(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_custom_emojis_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = reaction.ListCustomEmojisResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.list_custom_emojis",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListCustomEmojis",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListMemberships(
        _BaseChatServiceRestTransport._BaseListMemberships, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.ListMemberships")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: membership.ListMembershipsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> membership.ListMembershipsResponse:
            r"""Call the list memberships method over HTTP.

            Args:
                request (~.membership.ListMembershipsRequest):
                    The request object. Request message for listing
                memberships.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.membership.ListMembershipsResponse:
                    Response to list memberships of the
                space.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseListMemberships._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_memberships(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseListMemberships._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseListMemberships._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.ListMemberships",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListMemberships",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._ListMemberships._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = membership.ListMembershipsResponse()
            pb_resp = membership.ListMembershipsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_memberships(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_memberships_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = membership.ListMembershipsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.list_memberships",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListMemberships",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListMessages(
        _BaseChatServiceRestTransport._BaseListMessages, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.ListMessages")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: message.ListMessagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> message.ListMessagesResponse:
            r"""Call the list messages method over HTTP.

            Args:
                request (~.message.ListMessagesRequest):
                    The request object. Lists messages in the specified
                space, that the user is a member of.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.message.ListMessagesResponse:
                    Response message for listing
                messages.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseListMessages._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_messages(request, metadata)
            transcoded_request = (
                _BaseChatServiceRestTransport._BaseListMessages._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseListMessages._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.ListMessages",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListMessages",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._ListMessages._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = message.ListMessagesResponse()
            pb_resp = message.ListMessagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_messages(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_messages_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = message.ListMessagesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.list_messages",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListMessages",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListReactions(
        _BaseChatServiceRestTransport._BaseListReactions, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.ListReactions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: reaction.ListReactionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> reaction.ListReactionsResponse:
            r"""Call the list reactions method over HTTP.

            Args:
                request (~.reaction.ListReactionsRequest):
                    The request object. Lists reactions to a message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.reaction.ListReactionsResponse:
                    Response to a list reactions request.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseListReactions._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_reactions(request, metadata)
            transcoded_request = _BaseChatServiceRestTransport._BaseListReactions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseListReactions._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.ListReactions",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListReactions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._ListReactions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = reaction.ListReactionsResponse()
            pb_resp = reaction.ListReactionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_reactions(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_reactions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = reaction.ListReactionsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.list_reactions",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListReactions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListSpaceEvents(
        _BaseChatServiceRestTransport._BaseListSpaceEvents, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.ListSpaceEvents")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: space_event.ListSpaceEventsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> space_event.ListSpaceEventsResponse:
            r"""Call the list space events method over HTTP.

            Args:
                request (~.space_event.ListSpaceEventsRequest):
                    The request object. Request message for listing space
                events.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.space_event.ListSpaceEventsResponse:
                    Response message for listing space
                events.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseListSpaceEvents._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_space_events(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseListSpaceEvents._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseListSpaceEvents._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.ListSpaceEvents",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListSpaceEvents",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._ListSpaceEvents._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = space_event.ListSpaceEventsResponse()
            pb_resp = space_event.ListSpaceEventsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_space_events(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_space_events_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = space_event.ListSpaceEventsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.list_space_events",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListSpaceEvents",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListSpaces(
        _BaseChatServiceRestTransport._BaseListSpaces, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.ListSpaces")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: space.ListSpacesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> space.ListSpacesResponse:
            r"""Call the list spaces method over HTTP.

            Args:
                request (~.space.ListSpacesRequest):
                    The request object. A request to list the spaces the
                caller is a member of.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.space.ListSpacesResponse:
                    The response for a list spaces
                request.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseListSpaces._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_spaces(request, metadata)
            transcoded_request = (
                _BaseChatServiceRestTransport._BaseListSpaces._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseListSpaces._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.ListSpaces",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListSpaces",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._ListSpaces._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = space.ListSpacesResponse()
            pb_resp = space.ListSpacesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_spaces(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_spaces_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = space.ListSpacesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.list_spaces",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "ListSpaces",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SearchSpaces(
        _BaseChatServiceRestTransport._BaseSearchSpaces, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.SearchSpaces")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: space.SearchSpacesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> space.SearchSpacesResponse:
            r"""Call the search spaces method over HTTP.

            Args:
                request (~.space.SearchSpacesRequest):
                    The request object. Request to search for a list of
                spaces based on a query.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.space.SearchSpacesResponse:
                    Response with a list of spaces
                corresponding to the search spaces
                request.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseSearchSpaces._get_http_options()
            )

            request, metadata = self._interceptor.pre_search_spaces(request, metadata)
            transcoded_request = (
                _BaseChatServiceRestTransport._BaseSearchSpaces._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseSearchSpaces._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.SearchSpaces",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "SearchSpaces",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._SearchSpaces._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = space.SearchSpacesResponse()
            pb_resp = space.SearchSpacesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_search_spaces(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_search_spaces_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = space.SearchSpacesResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.search_spaces",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "SearchSpaces",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SetUpSpace(
        _BaseChatServiceRestTransport._BaseSetUpSpace, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.SetUpSpace")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: space_setup.SetUpSpaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> space.Space:
            r"""Call the set up space method over HTTP.

            Args:
                request (~.space_setup.SetUpSpaceRequest):
                    The request object. Request to create a space and add
                specified users to it.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.space.Space:
                    A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseSetUpSpace._get_http_options()
            )

            request, metadata = self._interceptor.pre_set_up_space(request, metadata)
            transcoded_request = (
                _BaseChatServiceRestTransport._BaseSetUpSpace._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseChatServiceRestTransport._BaseSetUpSpace._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseSetUpSpace._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.SetUpSpace",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "SetUpSpace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._SetUpSpace._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = space.Space()
            pb_resp = space.Space.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_set_up_space(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_set_up_space_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = space.Space.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.set_up_space",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "SetUpSpace",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateMembership(
        _BaseChatServiceRestTransport._BaseUpdateMembership, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.UpdateMembership")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gc_membership.UpdateMembershipRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gc_membership.Membership:
            r"""Call the update membership method over HTTP.

            Args:
                request (~.gc_membership.UpdateMembershipRequest):
                    The request object. Request message for updating a
                membership.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.gc_membership.Membership:
                    Represents a membership relation in
                Google Chat, such as whether a user or
                Chat app is invited to, part of, or
                absent from a space.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseUpdateMembership._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_membership(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseUpdateMembership._get_transcoded_request(
                http_options, request
            )

            body = _BaseChatServiceRestTransport._BaseUpdateMembership._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseUpdateMembership._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.UpdateMembership",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UpdateMembership",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._UpdateMembership._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gc_membership.Membership()
            pb_resp = gc_membership.Membership.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_membership(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_membership_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = gc_membership.Membership.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.update_membership",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UpdateMembership",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateMessage(
        _BaseChatServiceRestTransport._BaseUpdateMessage, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.UpdateMessage")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gc_message.UpdateMessageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gc_message.Message:
            r"""Call the update message method over HTTP.

            Args:
                request (~.gc_message.UpdateMessageRequest):
                    The request object. Request to update a message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.gc_message.Message:
                    A message in a Google Chat space.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseUpdateMessage._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_message(request, metadata)
            transcoded_request = _BaseChatServiceRestTransport._BaseUpdateMessage._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseChatServiceRestTransport._BaseUpdateMessage._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseUpdateMessage._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.UpdateMessage",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UpdateMessage",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._UpdateMessage._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gc_message.Message()
            pb_resp = gc_message.Message.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_message(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_message_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = gc_message.Message.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.update_message",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UpdateMessage",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateSpace(
        _BaseChatServiceRestTransport._BaseUpdateSpace, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.UpdateSpace")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gc_space.UpdateSpaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gc_space.Space:
            r"""Call the update space method over HTTP.

            Args:
                request (~.gc_space.UpdateSpaceRequest):
                    The request object. A request to update a single space.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.gc_space.Space:
                    A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseUpdateSpace._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_space(request, metadata)
            transcoded_request = (
                _BaseChatServiceRestTransport._BaseUpdateSpace._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseChatServiceRestTransport._BaseUpdateSpace._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseChatServiceRestTransport._BaseUpdateSpace._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.UpdateSpace",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UpdateSpace",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._UpdateSpace._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gc_space.Space()
            pb_resp = gc_space.Space.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_space(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_space_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = gc_space.Space.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.update_space",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UpdateSpace",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateSpaceNotificationSetting(
        _BaseChatServiceRestTransport._BaseUpdateSpaceNotificationSetting,
        ChatServiceRestStub,
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.UpdateSpaceNotificationSetting")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gc_space_notification_setting.UpdateSpaceNotificationSettingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gc_space_notification_setting.SpaceNotificationSetting:
            r"""Call the update space notification
            setting method over HTTP.

                Args:
                    request (~.gc_space_notification_setting.UpdateSpaceNotificationSettingRequest):
                        The request object. Request to update the space
                    notification settings. Only supports
                    updating notification setting for the
                    calling user.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.gc_space_notification_setting.SpaceNotificationSetting:
                        The notification setting of a user in
                    a space.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseUpdateSpaceNotificationSetting._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_space_notification_setting(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseUpdateSpaceNotificationSetting._get_transcoded_request(
                http_options, request
            )

            body = _BaseChatServiceRestTransport._BaseUpdateSpaceNotificationSetting._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseUpdateSpaceNotificationSetting._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.UpdateSpaceNotificationSetting",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UpdateSpaceNotificationSetting",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                ChatServiceRestTransport._UpdateSpaceNotificationSetting._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gc_space_notification_setting.SpaceNotificationSetting()
            pb_resp = gc_space_notification_setting.SpaceNotificationSetting.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_space_notification_setting(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_update_space_notification_setting_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        gc_space_notification_setting.SpaceNotificationSetting.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.update_space_notification_setting",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UpdateSpaceNotificationSetting",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateSpaceReadState(
        _BaseChatServiceRestTransport._BaseUpdateSpaceReadState, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.UpdateSpaceReadState")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: gc_space_read_state.UpdateSpaceReadStateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gc_space_read_state.SpaceReadState:
            r"""Call the update space read state method over HTTP.

            Args:
                request (~.gc_space_read_state.UpdateSpaceReadStateRequest):
                    The request object. Request message for
                UpdateSpaceReadState API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.gc_space_read_state.SpaceReadState:
                    A user's read state within a space,
                used to identify read and unread
                messages.

            """

            http_options = (
                _BaseChatServiceRestTransport._BaseUpdateSpaceReadState._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_space_read_state(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseUpdateSpaceReadState._get_transcoded_request(
                http_options, request
            )

            body = _BaseChatServiceRestTransport._BaseUpdateSpaceReadState._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseUpdateSpaceReadState._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.UpdateSpaceReadState",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UpdateSpaceReadState",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._UpdateSpaceReadState._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gc_space_read_state.SpaceReadState()
            pb_resp = gc_space_read_state.SpaceReadState.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_space_read_state(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_space_read_state_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = gc_space_read_state.SpaceReadState.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.update_space_read_state",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UpdateSpaceReadState",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UploadAttachment(
        _BaseChatServiceRestTransport._BaseUploadAttachment, ChatServiceRestStub
    ):
        def __hash__(self):
            return hash("ChatServiceRestTransport.UploadAttachment")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: attachment.UploadAttachmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> attachment.UploadAttachmentResponse:
            r"""Call the upload attachment method over HTTP.

            Args:
                request (~.attachment.UploadAttachmentRequest):
                    The request object. Request to upload an attachment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.attachment.UploadAttachmentResponse:
                    Response of uploading an attachment.
            """

            http_options = (
                _BaseChatServiceRestTransport._BaseUploadAttachment._get_http_options()
            )

            request, metadata = self._interceptor.pre_upload_attachment(
                request, metadata
            )
            transcoded_request = _BaseChatServiceRestTransport._BaseUploadAttachment._get_transcoded_request(
                http_options, request
            )

            body = _BaseChatServiceRestTransport._BaseUploadAttachment._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseChatServiceRestTransport._BaseUploadAttachment._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.chat_v1.ChatServiceClient.UploadAttachment",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UploadAttachment",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = ChatServiceRestTransport._UploadAttachment._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = attachment.UploadAttachmentResponse()
            pb_resp = attachment.UploadAttachmentResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_upload_attachment(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_upload_attachment_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = attachment.UploadAttachmentResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.chat_v1.ChatServiceClient.upload_attachment",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "rpcName": "UploadAttachment",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def complete_import_space(
        self,
    ) -> Callable[
        [space.CompleteImportSpaceRequest], space.CompleteImportSpaceResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CompleteImportSpace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_custom_emoji(
        self,
    ) -> Callable[[reaction.CreateCustomEmojiRequest], reaction.CustomEmoji]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCustomEmoji(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_membership(
        self,
    ) -> Callable[[gc_membership.CreateMembershipRequest], gc_membership.Membership]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateMembership(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_message(
        self,
    ) -> Callable[[gc_message.CreateMessageRequest], gc_message.Message]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateMessage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_reaction(
        self,
    ) -> Callable[[gc_reaction.CreateReactionRequest], gc_reaction.Reaction]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateReaction(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_space(self) -> Callable[[gc_space.CreateSpaceRequest], gc_space.Space]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSpace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_custom_emoji(
        self,
    ) -> Callable[[reaction.DeleteCustomEmojiRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCustomEmoji(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_membership(
        self,
    ) -> Callable[[membership.DeleteMembershipRequest], membership.Membership]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteMembership(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_message(
        self,
    ) -> Callable[[message.DeleteMessageRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteMessage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_reaction(
        self,
    ) -> Callable[[reaction.DeleteReactionRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteReaction(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_space(self) -> Callable[[space.DeleteSpaceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSpace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def find_direct_message(
        self,
    ) -> Callable[[space.FindDirectMessageRequest], space.Space]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FindDirectMessage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_attachment(
        self,
    ) -> Callable[[attachment.GetAttachmentRequest], attachment.Attachment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_custom_emoji(
        self,
    ) -> Callable[[reaction.GetCustomEmojiRequest], reaction.CustomEmoji]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCustomEmoji(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_membership(
        self,
    ) -> Callable[[membership.GetMembershipRequest], membership.Membership]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMembership(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_message(self) -> Callable[[message.GetMessageRequest], message.Message]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMessage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_space(self) -> Callable[[space.GetSpaceRequest], space.Space]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSpace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_space_event(
        self,
    ) -> Callable[[space_event.GetSpaceEventRequest], space_event.SpaceEvent]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSpaceEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_space_notification_setting(
        self,
    ) -> Callable[
        [space_notification_setting.GetSpaceNotificationSettingRequest],
        space_notification_setting.SpaceNotificationSetting,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSpaceNotificationSetting(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_space_read_state(
        self,
    ) -> Callable[
        [space_read_state.GetSpaceReadStateRequest], space_read_state.SpaceReadState
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSpaceReadState(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_thread_read_state(
        self,
    ) -> Callable[
        [thread_read_state.GetThreadReadStateRequest], thread_read_state.ThreadReadState
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetThreadReadState(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_custom_emojis(
        self,
    ) -> Callable[
        [reaction.ListCustomEmojisRequest], reaction.ListCustomEmojisResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCustomEmojis(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_memberships(
        self,
    ) -> Callable[
        [membership.ListMembershipsRequest], membership.ListMembershipsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMemberships(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_messages(
        self,
    ) -> Callable[[message.ListMessagesRequest], message.ListMessagesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMessages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_reactions(
        self,
    ) -> Callable[[reaction.ListReactionsRequest], reaction.ListReactionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReactions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_space_events(
        self,
    ) -> Callable[
        [space_event.ListSpaceEventsRequest], space_event.ListSpaceEventsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSpaceEvents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_spaces(
        self,
    ) -> Callable[[space.ListSpacesRequest], space.ListSpacesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSpaces(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_spaces(
        self,
    ) -> Callable[[space.SearchSpacesRequest], space.SearchSpacesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchSpaces(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_up_space(self) -> Callable[[space_setup.SetUpSpaceRequest], space.Space]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetUpSpace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_membership(
        self,
    ) -> Callable[[gc_membership.UpdateMembershipRequest], gc_membership.Membership]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateMembership(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_message(
        self,
    ) -> Callable[[gc_message.UpdateMessageRequest], gc_message.Message]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateMessage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_space(self) -> Callable[[gc_space.UpdateSpaceRequest], gc_space.Space]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSpace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_space_notification_setting(
        self,
    ) -> Callable[
        [gc_space_notification_setting.UpdateSpaceNotificationSettingRequest],
        gc_space_notification_setting.SpaceNotificationSetting,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSpaceNotificationSetting(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_space_read_state(
        self,
    ) -> Callable[
        [gc_space_read_state.UpdateSpaceReadStateRequest],
        gc_space_read_state.SpaceReadState,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSpaceReadState(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def upload_attachment(
        self,
    ) -> Callable[
        [attachment.UploadAttachmentRequest], attachment.UploadAttachmentResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UploadAttachment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ChatServiceRestTransport",)
