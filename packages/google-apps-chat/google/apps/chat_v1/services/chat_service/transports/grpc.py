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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore

from google.apps.chat_v1.types import attachment
from google.apps.chat_v1.types import membership
from google.apps.chat_v1.types import membership as gc_membership
from google.apps.chat_v1.types import message
from google.apps.chat_v1.types import message as gc_message
from google.apps.chat_v1.types import reaction
from google.apps.chat_v1.types import reaction as gc_reaction
from google.apps.chat_v1.types import space
from google.apps.chat_v1.types import space as gc_space
from google.apps.chat_v1.types import space_setup

from .base import DEFAULT_CLIENT_INFO, ChatServiceTransport


class ChatServiceGrpcTransport(ChatServiceTransport):
    """gRPC backend transport for ChatService.

    Enables developers to build Chat apps and
    integrations on Google Chat Platform.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "chat.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[grpc.Channel] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
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
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "chat.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def create_message(
        self,
    ) -> Callable[[gc_message.CreateMessageRequest], gc_message.Message]:
        r"""Return a callable for the create message method over gRPC.

        Creates a message in a Google Chat space. For an example, see
        `Create a
        message <https://developers.google.com/chat/api/guides/v1/messages/create>`__.

        Calling this method requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__
        and supports the following authentication types:

        -  For text messages, user authentication or app authentication
           are supported.
        -  For card messages, only app authentication is supported.
           (Only Chat apps can create card messages.)

        Returns:
            Callable[[~.CreateMessageRequest],
                    ~.Message]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_message" not in self._stubs:
            self._stubs["create_message"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/CreateMessage",
                request_serializer=gc_message.CreateMessageRequest.serialize,
                response_deserializer=gc_message.Message.deserialize,
            )
        return self._stubs["create_message"]

    @property
    def list_messages(
        self,
    ) -> Callable[[message.ListMessagesRequest], message.ListMessagesResponse]:
        r"""Return a callable for the list messages method over gRPC.

        Lists messages in a space that the caller is a member of,
        including messages from blocked members and spaces. For an
        example, see `List
        messages </chat/api/guides/v1/messages/list>`__. Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Returns:
            Callable[[~.ListMessagesRequest],
                    ~.ListMessagesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_messages" not in self._stubs:
            self._stubs["list_messages"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/ListMessages",
                request_serializer=message.ListMessagesRequest.serialize,
                response_deserializer=message.ListMessagesResponse.deserialize,
            )
        return self._stubs["list_messages"]

    @property
    def list_memberships(
        self,
    ) -> Callable[
        [membership.ListMembershipsRequest], membership.ListMembershipsResponse
    ]:
        r"""Return a callable for the list memberships method over gRPC.

        Lists memberships in a space. For an example, see `List
        memberships <https://developers.google.com/chat/api/guides/v1/members/list>`__.
        Listing memberships with `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        lists memberships in spaces that the Chat app has access to, but
        excludes Chat app memberships, including its own. Listing
        memberships with `User
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__
        lists memberships in spaces that the authenticated user has
        access to.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Returns:
            Callable[[~.ListMembershipsRequest],
                    ~.ListMembershipsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_memberships" not in self._stubs:
            self._stubs["list_memberships"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/ListMemberships",
                request_serializer=membership.ListMembershipsRequest.serialize,
                response_deserializer=membership.ListMembershipsResponse.deserialize,
            )
        return self._stubs["list_memberships"]

    @property
    def get_membership(
        self,
    ) -> Callable[[membership.GetMembershipRequest], membership.Membership]:
        r"""Return a callable for the get membership method over gRPC.

        Returns details about a membership. For an example, see `Get a
        membership <https://developers.google.com/chat/api/guides/v1/members/get>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Returns:
            Callable[[~.GetMembershipRequest],
                    ~.Membership]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_membership" not in self._stubs:
            self._stubs["get_membership"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/GetMembership",
                request_serializer=membership.GetMembershipRequest.serialize,
                response_deserializer=membership.Membership.deserialize,
            )
        return self._stubs["get_membership"]

    @property
    def get_message(self) -> Callable[[message.GetMessageRequest], message.Message]:
        r"""Return a callable for the get message method over gRPC.

        Returns details about a message. For an example, see `Read a
        message <https://developers.google.com/chat/api/guides/v1/messages/get>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Note: Might return a message from a blocked member or space.

        Returns:
            Callable[[~.GetMessageRequest],
                    ~.Message]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_message" not in self._stubs:
            self._stubs["get_message"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/GetMessage",
                request_serializer=message.GetMessageRequest.serialize,
                response_deserializer=message.Message.deserialize,
            )
        return self._stubs["get_message"]

    @property
    def update_message(
        self,
    ) -> Callable[[gc_message.UpdateMessageRequest], gc_message.Message]:
        r"""Return a callable for the update message method over gRPC.

        Updates a message. There's a difference between the ``patch``
        and ``update`` methods. The ``patch`` method uses a ``patch``
        request while the ``update`` method uses a ``put`` request. We
        recommend using the ``patch`` method. For an example, see
        `Update a
        message <https://developers.google.com/chat/api/guides/v1/messages/update>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.
        When using app authentication, requests can only update messages
        created by the calling Chat app.

        Returns:
            Callable[[~.UpdateMessageRequest],
                    ~.Message]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_message" not in self._stubs:
            self._stubs["update_message"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/UpdateMessage",
                request_serializer=gc_message.UpdateMessageRequest.serialize,
                response_deserializer=gc_message.Message.deserialize,
            )
        return self._stubs["update_message"]

    @property
    def delete_message(
        self,
    ) -> Callable[[message.DeleteMessageRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete message method over gRPC.

        Deletes a message. For an example, see `Delete a
        message <https://developers.google.com/chat/api/guides/v1/messages/delete>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.
        When using app authentication, requests can only delete messages
        created by the calling Chat app.

        Returns:
            Callable[[~.DeleteMessageRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_message" not in self._stubs:
            self._stubs["delete_message"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/DeleteMessage",
                request_serializer=message.DeleteMessageRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_message"]

    @property
    def get_attachment(
        self,
    ) -> Callable[[attachment.GetAttachmentRequest], attachment.Attachment]:
        r"""Return a callable for the get attachment method over gRPC.

        Gets the metadata of a message attachment. The attachment data
        is fetched using the `media
        API <https://developers.google.com/chat/api/reference/rest/v1/media/download>`__.
        For an example, see `Get a message
        attachment <https://developers.google.com/chat/api/guides/v1/media-and-attachments/get>`__.
        Requires `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__.

        Returns:
            Callable[[~.GetAttachmentRequest],
                    ~.Attachment]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_attachment" not in self._stubs:
            self._stubs["get_attachment"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/GetAttachment",
                request_serializer=attachment.GetAttachmentRequest.serialize,
                response_deserializer=attachment.Attachment.deserialize,
            )
        return self._stubs["get_attachment"]

    @property
    def upload_attachment(
        self,
    ) -> Callable[
        [attachment.UploadAttachmentRequest], attachment.UploadAttachmentResponse
    ]:
        r"""Return a callable for the upload attachment method over gRPC.

        Uploads an attachment. For an example, see `Upload media as a
        file
        attachment <https://developers.google.com/chat/api/guides/v1/media-and-attachments/upload>`__.
        Requires user
        `authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        You can upload attachments up to 200 MB. Certain file types
        aren't supported. For details, see `File types blocked by Google
        Chat <https://support.google.com/chat/answer/7651457?&co=GENIE.Platform%3DDesktop#File%20types%20blocked%20in%20Google%20Chat>`__.

        Returns:
            Callable[[~.UploadAttachmentRequest],
                    ~.UploadAttachmentResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "upload_attachment" not in self._stubs:
            self._stubs["upload_attachment"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/UploadAttachment",
                request_serializer=attachment.UploadAttachmentRequest.serialize,
                response_deserializer=attachment.UploadAttachmentResponse.deserialize,
            )
        return self._stubs["upload_attachment"]

    @property
    def list_spaces(
        self,
    ) -> Callable[[space.ListSpacesRequest], space.ListSpacesResponse]:
        r"""Return a callable for the list spaces method over gRPC.

        Lists spaces the caller is a member of. Group chats and DMs
        aren't listed until the first message is sent. For an example,
        see `List
        spaces <https://developers.google.com/chat/api/guides/v1/spaces/list>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Lists spaces visible to the caller or authenticated user. Group
        chats and DMs aren't listed until the first message is sent.

        Returns:
            Callable[[~.ListSpacesRequest],
                    ~.ListSpacesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_spaces" not in self._stubs:
            self._stubs["list_spaces"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/ListSpaces",
                request_serializer=space.ListSpacesRequest.serialize,
                response_deserializer=space.ListSpacesResponse.deserialize,
            )
        return self._stubs["list_spaces"]

    @property
    def get_space(self) -> Callable[[space.GetSpaceRequest], space.Space]:
        r"""Return a callable for the get space method over gRPC.

        Returns details about a space. For an example, see `Get a
        space <https://developers.google.com/chat/api/guides/v1/spaces/get>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Returns:
            Callable[[~.GetSpaceRequest],
                    ~.Space]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_space" not in self._stubs:
            self._stubs["get_space"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/GetSpace",
                request_serializer=space.GetSpaceRequest.serialize,
                response_deserializer=space.Space.deserialize,
            )
        return self._stubs["get_space"]

    @property
    def create_space(self) -> Callable[[gc_space.CreateSpaceRequest], gc_space.Space]:
        r"""Return a callable for the create space method over gRPC.

        Creates a named space. Spaces grouped by topics aren't
        supported. For an example, see `Create a
        space <https://developers.google.com/chat/api/guides/v1/spaces/create>`__.

        If you receive the error message ``ALREADY_EXISTS`` when
        creating a space, try a different ``displayName``. An existing
        space within the Google Workspace organization might already use
        this display name.

        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Returns:
            Callable[[~.CreateSpaceRequest],
                    ~.Space]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_space" not in self._stubs:
            self._stubs["create_space"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/CreateSpace",
                request_serializer=gc_space.CreateSpaceRequest.serialize,
                response_deserializer=gc_space.Space.deserialize,
            )
        return self._stubs["create_space"]

    @property
    def set_up_space(self) -> Callable[[space_setup.SetUpSpaceRequest], space.Space]:
        r"""Return a callable for the set up space method over gRPC.

        Creates a space and adds specified users to it. The calling user
        is automatically added to the space, and shouldn't be specified
        as a membership in the request. For an example, see `Set up a
        space <https://developers.google.com/chat/api/guides/v1/spaces/set-up>`__.

        To specify the human members to add, add memberships with the
        appropriate ``member.name`` in the ``SetUpSpaceRequest``. To add
        a human user, use ``users/{user}``, where ``{user}`` can be the
        email address for the user. For users in the same Workspace
        organization ``{user}`` can also be the ``id`` for the person
        from the People API, or the ``id`` for the user in the Directory
        API. For example, if the People API Person profile ID for
        ``user@example.com`` is ``123456789``, you can add the user to
        the space by setting the ``membership.member.name`` to
        ``users/user@example.com`` or ``users/123456789``.

        For a space or group chat, if the caller blocks or is blocked by
        some members, then those members aren't added to the created
        space.

        To create a direct message (DM) between the calling user and
        another human user, specify exactly one membership to represent
        the human user. If one user blocks the other, the request fails
        and the DM isn't created.

        To create a DM between the calling user and the calling app, set
        ``Space.singleUserBotDm`` to ``true`` and don't specify any
        memberships. You can only use this method to set up a DM with
        the calling app. To add the calling app as a member of a space
        or an existing DM between two human users, see `create a
        membership <https://developers.google.com/chat/api/guides/v1/members/create>`__.

        If a DM already exists between two users, even when one user
        blocks the other at the time a request is made, then the
        existing DM is returned.

        Spaces with threaded replies aren't supported. If you receive
        the error message ``ALREADY_EXISTS`` when setting up a space,
        try a different ``displayName``. An existing space within the
        Google Workspace organization might already use this display
        name.

        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Returns:
            Callable[[~.SetUpSpaceRequest],
                    ~.Space]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_up_space" not in self._stubs:
            self._stubs["set_up_space"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/SetUpSpace",
                request_serializer=space_setup.SetUpSpaceRequest.serialize,
                response_deserializer=space.Space.deserialize,
            )
        return self._stubs["set_up_space"]

    @property
    def update_space(self) -> Callable[[gc_space.UpdateSpaceRequest], gc_space.Space]:
        r"""Return a callable for the update space method over gRPC.

        Updates a space. For an example, see `Update a
        space <https://developers.google.com/chat/api/guides/v1/spaces/update>`__.

        If you're updating the ``displayName`` field and receive the
        error message ``ALREADY_EXISTS``, try a different display name..
        An existing space within the Google Workspace organization might
        already use this display name.

        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Returns:
            Callable[[~.UpdateSpaceRequest],
                    ~.Space]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_space" not in self._stubs:
            self._stubs["update_space"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/UpdateSpace",
                request_serializer=gc_space.UpdateSpaceRequest.serialize,
                response_deserializer=gc_space.Space.deserialize,
            )
        return self._stubs["update_space"]

    @property
    def delete_space(self) -> Callable[[space.DeleteSpaceRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete space method over gRPC.

        Deletes a named space. Always performs a cascading delete, which
        means that the space's child resources—like messages posted in
        the space and memberships in the space—are also deleted. For an
        example, see `Delete a
        space <https://developers.google.com/chat/api/guides/v1/spaces/delete>`__.
        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__
        from a user who has permission to delete the space.

        Returns:
            Callable[[~.DeleteSpaceRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_space" not in self._stubs:
            self._stubs["delete_space"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/DeleteSpace",
                request_serializer=space.DeleteSpaceRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_space"]

    @property
    def complete_import_space(
        self,
    ) -> Callable[
        [space.CompleteImportSpaceRequest], space.CompleteImportSpaceResponse
    ]:
        r"""Return a callable for the complete import space method over gRPC.

        Completes the `import
        process <https://developers.google.com/chat/api/guides/import-data>`__
        for the specified space and makes it visible to users. Requires
        app authentication and domain-wide delegation. For more
        information, see `Authorize Google Chat apps to import
        data <https://developers.google.com/chat/api/guides/authorize-import>`__.

        Returns:
            Callable[[~.CompleteImportSpaceRequest],
                    ~.CompleteImportSpaceResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "complete_import_space" not in self._stubs:
            self._stubs["complete_import_space"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/CompleteImportSpace",
                request_serializer=space.CompleteImportSpaceRequest.serialize,
                response_deserializer=space.CompleteImportSpaceResponse.deserialize,
            )
        return self._stubs["complete_import_space"]

    @property
    def find_direct_message(
        self,
    ) -> Callable[[space.FindDirectMessageRequest], space.Space]:
        r"""Return a callable for the find direct message method over gRPC.

        Returns the existing direct message with the specified user. If
        no direct message space is found, returns a ``404 NOT_FOUND``
        error. For an example, see `Find a direct
        message </chat/api/guides/v1/spaces/find-direct-message>`__.

        With `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__,
        returns the direct message space between the specified user and
        the authenticated user.

        With `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__,
        returns the direct message space between the specified user and
        the calling Chat app.

        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__
        or `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__.

        Returns:
            Callable[[~.FindDirectMessageRequest],
                    ~.Space]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "find_direct_message" not in self._stubs:
            self._stubs["find_direct_message"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/FindDirectMessage",
                request_serializer=space.FindDirectMessageRequest.serialize,
                response_deserializer=space.Space.deserialize,
            )
        return self._stubs["find_direct_message"]

    @property
    def create_membership(
        self,
    ) -> Callable[[gc_membership.CreateMembershipRequest], gc_membership.Membership]:
        r"""Return a callable for the create membership method over gRPC.

        Creates a human membership or app membership for the calling
        app. Creating memberships for other apps isn't supported. For an
        example, see `Create a
        membership <https://developers.google.com/chat/api/guides/v1/members/create>`__.
        When creating a membership, if the specified member has their
        auto-accept policy turned off, then they're invited, and must
        accept the space invitation before joining. Otherwise, creating
        a membership adds the member directly to the specified space.
        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        To specify the member to add, set the ``membership.member.name``
        in the ``CreateMembershipRequest``:

        -  To add the calling app to a space or a direct message between
           two human users, use ``users/app``. Unable to add other apps
           to the space.

        -  To add a human user, use ``users/{user}``, where ``{user}``
           can be the email address for the user. For users in the same
           Workspace organization ``{user}`` can also be the ``id`` for
           the person from the People API, or the ``id`` for the user in
           the Directory API. For example, if the People API Person
           profile ID for ``user@example.com`` is ``123456789``, you can
           add the user to the space by setting the
           ``membership.member.name`` to ``users/user@example.com`` or
           ``users/123456789``.

        Returns:
            Callable[[~.CreateMembershipRequest],
                    ~.Membership]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_membership" not in self._stubs:
            self._stubs["create_membership"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/CreateMembership",
                request_serializer=gc_membership.CreateMembershipRequest.serialize,
                response_deserializer=gc_membership.Membership.deserialize,
            )
        return self._stubs["create_membership"]

    @property
    def delete_membership(
        self,
    ) -> Callable[[membership.DeleteMembershipRequest], membership.Membership]:
        r"""Return a callable for the delete membership method over gRPC.

        Deletes a membership. For an example, see `Delete a
        membership <https://developers.google.com/chat/api/guides/v1/members/delete>`__.

        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Returns:
            Callable[[~.DeleteMembershipRequest],
                    ~.Membership]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_membership" not in self._stubs:
            self._stubs["delete_membership"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/DeleteMembership",
                request_serializer=membership.DeleteMembershipRequest.serialize,
                response_deserializer=membership.Membership.deserialize,
            )
        return self._stubs["delete_membership"]

    @property
    def create_reaction(
        self,
    ) -> Callable[[gc_reaction.CreateReactionRequest], gc_reaction.Reaction]:
        r"""Return a callable for the create reaction method over gRPC.

        Creates a reaction and adds it to a message. For an example, see
        `Create a
        reaction <https://developers.google.com/chat/api/guides/v1/reactions/create>`__.
        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.
        Only unicode emoji are supported.

        Returns:
            Callable[[~.CreateReactionRequest],
                    ~.Reaction]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_reaction" not in self._stubs:
            self._stubs["create_reaction"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/CreateReaction",
                request_serializer=gc_reaction.CreateReactionRequest.serialize,
                response_deserializer=gc_reaction.Reaction.deserialize,
            )
        return self._stubs["create_reaction"]

    @property
    def list_reactions(
        self,
    ) -> Callable[[reaction.ListReactionsRequest], reaction.ListReactionsResponse]:
        r"""Return a callable for the list reactions method over gRPC.

        Lists reactions to a message. For an example, see `List
        reactions <https://developers.google.com/chat/api/guides/v1/reactions/list>`__.
        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Returns:
            Callable[[~.ListReactionsRequest],
                    ~.ListReactionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_reactions" not in self._stubs:
            self._stubs["list_reactions"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/ListReactions",
                request_serializer=reaction.ListReactionsRequest.serialize,
                response_deserializer=reaction.ListReactionsResponse.deserialize,
            )
        return self._stubs["list_reactions"]

    @property
    def delete_reaction(
        self,
    ) -> Callable[[reaction.DeleteReactionRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete reaction method over gRPC.

        Deletes a reaction to a message. For an example, see `Delete a
        reaction <https://developers.google.com/chat/api/guides/v1/reactions/delete>`__.
        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Returns:
            Callable[[~.DeleteReactionRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_reaction" not in self._stubs:
            self._stubs["delete_reaction"] = self.grpc_channel.unary_unary(
                "/google.chat.v1.ChatService/DeleteReaction",
                request_serializer=reaction.DeleteReactionRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_reaction"]

    def close(self):
        self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("ChatServiceGrpcTransport",)
