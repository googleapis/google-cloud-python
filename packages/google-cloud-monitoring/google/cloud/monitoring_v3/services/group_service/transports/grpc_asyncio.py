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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.monitoring_v3.types import group
from google.cloud.monitoring_v3.types import group as gm_group
from google.cloud.monitoring_v3.types import group_service

from .base import DEFAULT_CLIENT_INFO, GroupServiceTransport
from .grpc import GroupServiceGrpcTransport


class GroupServiceGrpcAsyncIOTransport(GroupServiceTransport):
    """gRPC AsyncIO backend transport for GroupService.

    The Group API lets you inspect and manage your
    `groups <#google.monitoring.v3.Group>`__.

    A group is a named filter that is used to identify a collection of
    monitored resources. Groups are typically used to mirror the
    physical and/or logical topology of the environment. Because group
    membership is computed dynamically, monitored resources that are
    started in the future are automatically placed in matching groups.
    By using a group to name monitored resources in, for example, an
    alert policy, the target of that alert policy is updated
    automatically as monitored resources are added and removed from the
    infrastructure.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "monitoring.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "monitoring.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
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
                 The hostname to connect to (default: 'monitoring.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
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
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
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

        if isinstance(channel, aio.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
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
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
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

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def list_groups(
        self,
    ) -> Callable[
        [group_service.ListGroupsRequest], Awaitable[group_service.ListGroupsResponse]
    ]:
        r"""Return a callable for the list groups method over gRPC.

        Lists the existing groups.

        Returns:
            Callable[[~.ListGroupsRequest],
                    Awaitable[~.ListGroupsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_groups" not in self._stubs:
            self._stubs["list_groups"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.GroupService/ListGroups",
                request_serializer=group_service.ListGroupsRequest.serialize,
                response_deserializer=group_service.ListGroupsResponse.deserialize,
            )
        return self._stubs["list_groups"]

    @property
    def get_group(
        self,
    ) -> Callable[[group_service.GetGroupRequest], Awaitable[group.Group]]:
        r"""Return a callable for the get group method over gRPC.

        Gets a single group.

        Returns:
            Callable[[~.GetGroupRequest],
                    Awaitable[~.Group]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_group" not in self._stubs:
            self._stubs["get_group"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.GroupService/GetGroup",
                request_serializer=group_service.GetGroupRequest.serialize,
                response_deserializer=group.Group.deserialize,
            )
        return self._stubs["get_group"]

    @property
    def create_group(
        self,
    ) -> Callable[[group_service.CreateGroupRequest], Awaitable[gm_group.Group]]:
        r"""Return a callable for the create group method over gRPC.

        Creates a new group.

        Returns:
            Callable[[~.CreateGroupRequest],
                    Awaitable[~.Group]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_group" not in self._stubs:
            self._stubs["create_group"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.GroupService/CreateGroup",
                request_serializer=group_service.CreateGroupRequest.serialize,
                response_deserializer=gm_group.Group.deserialize,
            )
        return self._stubs["create_group"]

    @property
    def update_group(
        self,
    ) -> Callable[[group_service.UpdateGroupRequest], Awaitable[gm_group.Group]]:
        r"""Return a callable for the update group method over gRPC.

        Updates an existing group. You can change any group attributes
        except ``name``.

        Returns:
            Callable[[~.UpdateGroupRequest],
                    Awaitable[~.Group]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_group" not in self._stubs:
            self._stubs["update_group"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.GroupService/UpdateGroup",
                request_serializer=group_service.UpdateGroupRequest.serialize,
                response_deserializer=gm_group.Group.deserialize,
            )
        return self._stubs["update_group"]

    @property
    def delete_group(
        self,
    ) -> Callable[[group_service.DeleteGroupRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete group method over gRPC.

        Deletes an existing group.

        Returns:
            Callable[[~.DeleteGroupRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_group" not in self._stubs:
            self._stubs["delete_group"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.GroupService/DeleteGroup",
                request_serializer=group_service.DeleteGroupRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_group"]

    @property
    def list_group_members(
        self,
    ) -> Callable[
        [group_service.ListGroupMembersRequest],
        Awaitable[group_service.ListGroupMembersResponse],
    ]:
        r"""Return a callable for the list group members method over gRPC.

        Lists the monitored resources that are members of a
        group.

        Returns:
            Callable[[~.ListGroupMembersRequest],
                    Awaitable[~.ListGroupMembersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_group_members" not in self._stubs:
            self._stubs["list_group_members"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.GroupService/ListGroupMembers",
                request_serializer=group_service.ListGroupMembersRequest.serialize,
                response_deserializer=group_service.ListGroupMembersResponse.deserialize,
            )
        return self._stubs["list_group_members"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_groups: gapic_v1.method_async.wrap_method(
                self.list_groups,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_group: gapic_v1.method_async.wrap_method(
                self.get_group,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_group: gapic_v1.method_async.wrap_method(
                self.create_group,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_group: gapic_v1.method_async.wrap_method(
                self.update_group,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=180.0,
                ),
                default_timeout=180.0,
                client_info=client_info,
            ),
            self.delete_group: gapic_v1.method_async.wrap_method(
                self.delete_group,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_group_members: gapic_v1.method_async.wrap_method(
                self.list_group_members,
                default_retry=retries.AsyncRetry(
                    initial=0.1,
                    maximum=30.0,
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
        return self.grpc_channel.close()


__all__ = ("GroupServiceGrpcAsyncIOTransport",)
