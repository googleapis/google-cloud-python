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
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union

import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.apps.chat_v1 import gapic_version as package_version
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
from google.apps.chat_v1.types import space_read_state
from google.apps.chat_v1.types import space_read_state as gc_space_read_state
from google.apps.chat_v1.types import space_setup, thread_read_state

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class ChatServiceTransport(abc.ABC):
    """Abstract transport class for ChatService."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/chat.admin.delete",
        "https://www.googleapis.com/auth/chat.admin.memberships",
        "https://www.googleapis.com/auth/chat.admin.memberships.readonly",
        "https://www.googleapis.com/auth/chat.admin.spaces",
        "https://www.googleapis.com/auth/chat.admin.spaces.readonly",
        "https://www.googleapis.com/auth/chat.bot",
        "https://www.googleapis.com/auth/chat.delete",
        "https://www.googleapis.com/auth/chat.import",
        "https://www.googleapis.com/auth/chat.memberships",
        "https://www.googleapis.com/auth/chat.memberships.app",
        "https://www.googleapis.com/auth/chat.memberships.readonly",
        "https://www.googleapis.com/auth/chat.messages",
        "https://www.googleapis.com/auth/chat.messages.create",
        "https://www.googleapis.com/auth/chat.messages.reactions",
        "https://www.googleapis.com/auth/chat.messages.reactions.create",
        "https://www.googleapis.com/auth/chat.messages.reactions.readonly",
        "https://www.googleapis.com/auth/chat.messages.readonly",
        "https://www.googleapis.com/auth/chat.spaces",
        "https://www.googleapis.com/auth/chat.spaces.create",
        "https://www.googleapis.com/auth/chat.spaces.readonly",
        "https://www.googleapis.com/auth/chat.users.readstate",
        "https://www.googleapis.com/auth/chat.users.readstate.readonly",
    )

    DEFAULT_HOST: str = "chat.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
        **kwargs,
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
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
        """

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes
        if not hasattr(self, "_ignore_credentials"):
            self._ignore_credentials: bool = False

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )
        elif credentials is None and not self._ignore_credentials:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )
            # Don't apply audience if the credentials file passed from user.
            if hasattr(credentials, "with_gdch_audience"):
                credentials = credentials.with_gdch_audience(
                    api_audience if api_audience else host
                )

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

    @property
    def host(self):
        return self._host

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_message: gapic_v1.method.wrap_method(
                self.create_message,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_messages: gapic_v1.method.wrap_method(
                self.list_messages,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_memberships: gapic_v1.method.wrap_method(
                self.list_memberships,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_membership: gapic_v1.method.wrap_method(
                self.get_membership,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_message: gapic_v1.method.wrap_method(
                self.get_message,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_message: gapic_v1.method.wrap_method(
                self.update_message,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_message: gapic_v1.method.wrap_method(
                self.delete_message,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_attachment: gapic_v1.method.wrap_method(
                self.get_attachment,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.upload_attachment: gapic_v1.method.wrap_method(
                self.upload_attachment,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_spaces: gapic_v1.method.wrap_method(
                self.list_spaces,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.search_spaces: gapic_v1.method.wrap_method(
                self.search_spaces,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_space: gapic_v1.method.wrap_method(
                self.get_space,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_space: gapic_v1.method.wrap_method(
                self.create_space,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.set_up_space: gapic_v1.method.wrap_method(
                self.set_up_space,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_space: gapic_v1.method.wrap_method(
                self.update_space,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_space: gapic_v1.method.wrap_method(
                self.delete_space,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.complete_import_space: gapic_v1.method.wrap_method(
                self.complete_import_space,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.find_direct_message: gapic_v1.method.wrap_method(
                self.find_direct_message,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_membership: gapic_v1.method.wrap_method(
                self.create_membership,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_membership: gapic_v1.method.wrap_method(
                self.update_membership,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_membership: gapic_v1.method.wrap_method(
                self.delete_membership,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_reaction: gapic_v1.method.wrap_method(
                self.create_reaction,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_reactions: gapic_v1.method.wrap_method(
                self.list_reactions,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_reaction: gapic_v1.method.wrap_method(
                self.delete_reaction,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_space_read_state: gapic_v1.method.wrap_method(
                self.get_space_read_state,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_space_read_state: gapic_v1.method.wrap_method(
                self.update_space_read_state,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_thread_read_state: gapic_v1.method.wrap_method(
                self.get_thread_read_state,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_space_event: gapic_v1.method.wrap_method(
                self.get_space_event,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_space_events: gapic_v1.method.wrap_method(
                self.list_space_events,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
        }

    def close(self):
        """Closes resources associated with the transport.

        .. warning::
             Only call this method if the transport is NOT shared
             with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def create_message(
        self,
    ) -> Callable[
        [gc_message.CreateMessageRequest],
        Union[gc_message.Message, Awaitable[gc_message.Message]],
    ]:
        raise NotImplementedError()

    @property
    def list_messages(
        self,
    ) -> Callable[
        [message.ListMessagesRequest],
        Union[message.ListMessagesResponse, Awaitable[message.ListMessagesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def list_memberships(
        self,
    ) -> Callable[
        [membership.ListMembershipsRequest],
        Union[
            membership.ListMembershipsResponse,
            Awaitable[membership.ListMembershipsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_membership(
        self,
    ) -> Callable[
        [membership.GetMembershipRequest],
        Union[membership.Membership, Awaitable[membership.Membership]],
    ]:
        raise NotImplementedError()

    @property
    def get_message(
        self,
    ) -> Callable[
        [message.GetMessageRequest], Union[message.Message, Awaitable[message.Message]]
    ]:
        raise NotImplementedError()

    @property
    def update_message(
        self,
    ) -> Callable[
        [gc_message.UpdateMessageRequest],
        Union[gc_message.Message, Awaitable[gc_message.Message]],
    ]:
        raise NotImplementedError()

    @property
    def delete_message(
        self,
    ) -> Callable[
        [message.DeleteMessageRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_attachment(
        self,
    ) -> Callable[
        [attachment.GetAttachmentRequest],
        Union[attachment.Attachment, Awaitable[attachment.Attachment]],
    ]:
        raise NotImplementedError()

    @property
    def upload_attachment(
        self,
    ) -> Callable[
        [attachment.UploadAttachmentRequest],
        Union[
            attachment.UploadAttachmentResponse,
            Awaitable[attachment.UploadAttachmentResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_spaces(
        self,
    ) -> Callable[
        [space.ListSpacesRequest],
        Union[space.ListSpacesResponse, Awaitable[space.ListSpacesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def search_spaces(
        self,
    ) -> Callable[
        [space.SearchSpacesRequest],
        Union[space.SearchSpacesResponse, Awaitable[space.SearchSpacesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_space(
        self,
    ) -> Callable[[space.GetSpaceRequest], Union[space.Space, Awaitable[space.Space]]]:
        raise NotImplementedError()

    @property
    def create_space(
        self,
    ) -> Callable[
        [gc_space.CreateSpaceRequest], Union[gc_space.Space, Awaitable[gc_space.Space]]
    ]:
        raise NotImplementedError()

    @property
    def set_up_space(
        self,
    ) -> Callable[
        [space_setup.SetUpSpaceRequest], Union[space.Space, Awaitable[space.Space]]
    ]:
        raise NotImplementedError()

    @property
    def update_space(
        self,
    ) -> Callable[
        [gc_space.UpdateSpaceRequest], Union[gc_space.Space, Awaitable[gc_space.Space]]
    ]:
        raise NotImplementedError()

    @property
    def delete_space(
        self,
    ) -> Callable[
        [space.DeleteSpaceRequest], Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]]
    ]:
        raise NotImplementedError()

    @property
    def complete_import_space(
        self,
    ) -> Callable[
        [space.CompleteImportSpaceRequest],
        Union[
            space.CompleteImportSpaceResponse,
            Awaitable[space.CompleteImportSpaceResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def find_direct_message(
        self,
    ) -> Callable[
        [space.FindDirectMessageRequest], Union[space.Space, Awaitable[space.Space]]
    ]:
        raise NotImplementedError()

    @property
    def create_membership(
        self,
    ) -> Callable[
        [gc_membership.CreateMembershipRequest],
        Union[gc_membership.Membership, Awaitable[gc_membership.Membership]],
    ]:
        raise NotImplementedError()

    @property
    def update_membership(
        self,
    ) -> Callable[
        [gc_membership.UpdateMembershipRequest],
        Union[gc_membership.Membership, Awaitable[gc_membership.Membership]],
    ]:
        raise NotImplementedError()

    @property
    def delete_membership(
        self,
    ) -> Callable[
        [membership.DeleteMembershipRequest],
        Union[membership.Membership, Awaitable[membership.Membership]],
    ]:
        raise NotImplementedError()

    @property
    def create_reaction(
        self,
    ) -> Callable[
        [gc_reaction.CreateReactionRequest],
        Union[gc_reaction.Reaction, Awaitable[gc_reaction.Reaction]],
    ]:
        raise NotImplementedError()

    @property
    def list_reactions(
        self,
    ) -> Callable[
        [reaction.ListReactionsRequest],
        Union[
            reaction.ListReactionsResponse, Awaitable[reaction.ListReactionsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_reaction(
        self,
    ) -> Callable[
        [reaction.DeleteReactionRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_space_read_state(
        self,
    ) -> Callable[
        [space_read_state.GetSpaceReadStateRequest],
        Union[
            space_read_state.SpaceReadState, Awaitable[space_read_state.SpaceReadState]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_space_read_state(
        self,
    ) -> Callable[
        [gc_space_read_state.UpdateSpaceReadStateRequest],
        Union[
            gc_space_read_state.SpaceReadState,
            Awaitable[gc_space_read_state.SpaceReadState],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_thread_read_state(
        self,
    ) -> Callable[
        [thread_read_state.GetThreadReadStateRequest],
        Union[
            thread_read_state.ThreadReadState,
            Awaitable[thread_read_state.ThreadReadState],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_space_event(
        self,
    ) -> Callable[
        [space_event.GetSpaceEventRequest],
        Union[space_event.SpaceEvent, Awaitable[space_event.SpaceEvent]],
    ]:
        raise NotImplementedError()

    @property
    def list_space_events(
        self,
    ) -> Callable[
        [space_event.ListSpaceEventsRequest],
        Union[
            space_event.ListSpaceEventsResponse,
            Awaitable[space_event.ListSpaceEventsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = ("ChatServiceTransport",)
