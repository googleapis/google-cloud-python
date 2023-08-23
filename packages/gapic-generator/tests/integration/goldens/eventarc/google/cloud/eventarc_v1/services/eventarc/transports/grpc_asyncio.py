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
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1
from google.api_core import grpc_helpers_async
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials   # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc                        # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.eventarc_v1.types import channel
from google.cloud.eventarc_v1.types import channel_connection
from google.cloud.eventarc_v1.types import discovery
from google.cloud.eventarc_v1.types import eventarc
from google.cloud.eventarc_v1.types import google_channel_config
from google.cloud.eventarc_v1.types import google_channel_config as gce_google_channel_config
from google.cloud.eventarc_v1.types import trigger
from google.cloud.location import locations_pb2 # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2 # type: ignore
from .base import EventarcTransport, DEFAULT_CLIENT_INFO
from .grpc import EventarcGrpcTransport


class EventarcGrpcAsyncIOTransport(EventarcTransport):
    """gRPC AsyncIO backend transport for Eventarc.

    Eventarc allows users to subscribe to various events that are
    provided by Google Cloud services and forward them to supported
    destinations.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(cls,
                       host: str = 'eventarc.googleapis.com',
                       credentials: Optional[ga_credentials.Credentials] = None,
                       credentials_file: Optional[str] = None,
                       scopes: Optional[Sequence[str]] = None,
                       quota_project_id: Optional[str] = None,
                       **kwargs) -> aio.Channel:
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
                This argument is ignored if ``channel`` is provided.
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
            **kwargs
        )

    def __init__(self, *,
            host: str = 'eventarc.googleapis.com',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            channel: Optional[aio.Channel] = None,
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
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
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
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

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

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def get_trigger(self) -> Callable[
            [eventarc.GetTriggerRequest],
            Awaitable[trigger.Trigger]]:
        r"""Return a callable for the get trigger method over gRPC.

        Get a single trigger.

        Returns:
            Callable[[~.GetTriggerRequest],
                    Awaitable[~.Trigger]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_trigger' not in self._stubs:
            self._stubs['get_trigger'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/GetTrigger',
                request_serializer=eventarc.GetTriggerRequest.serialize,
                response_deserializer=trigger.Trigger.deserialize,
            )
        return self._stubs['get_trigger']

    @property
    def list_triggers(self) -> Callable[
            [eventarc.ListTriggersRequest],
            Awaitable[eventarc.ListTriggersResponse]]:
        r"""Return a callable for the list triggers method over gRPC.

        List triggers.

        Returns:
            Callable[[~.ListTriggersRequest],
                    Awaitable[~.ListTriggersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_triggers' not in self._stubs:
            self._stubs['list_triggers'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/ListTriggers',
                request_serializer=eventarc.ListTriggersRequest.serialize,
                response_deserializer=eventarc.ListTriggersResponse.deserialize,
            )
        return self._stubs['list_triggers']

    @property
    def create_trigger(self) -> Callable[
            [eventarc.CreateTriggerRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create trigger method over gRPC.

        Create a new trigger in a particular project and
        location.

        Returns:
            Callable[[~.CreateTriggerRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_trigger' not in self._stubs:
            self._stubs['create_trigger'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/CreateTrigger',
                request_serializer=eventarc.CreateTriggerRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_trigger']

    @property
    def update_trigger(self) -> Callable[
            [eventarc.UpdateTriggerRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the update trigger method over gRPC.

        Update a single trigger.

        Returns:
            Callable[[~.UpdateTriggerRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_trigger' not in self._stubs:
            self._stubs['update_trigger'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/UpdateTrigger',
                request_serializer=eventarc.UpdateTriggerRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_trigger']

    @property
    def delete_trigger(self) -> Callable[
            [eventarc.DeleteTriggerRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete trigger method over gRPC.

        Delete a single trigger.

        Returns:
            Callable[[~.DeleteTriggerRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_trigger' not in self._stubs:
            self._stubs['delete_trigger'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/DeleteTrigger',
                request_serializer=eventarc.DeleteTriggerRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_trigger']

    @property
    def get_channel(self) -> Callable[
            [eventarc.GetChannelRequest],
            Awaitable[channel.Channel]]:
        r"""Return a callable for the get channel method over gRPC.

        Get a single Channel.

        Returns:
            Callable[[~.GetChannelRequest],
                    Awaitable[~.Channel]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_channel' not in self._stubs:
            self._stubs['get_channel'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/GetChannel',
                request_serializer=eventarc.GetChannelRequest.serialize,
                response_deserializer=channel.Channel.deserialize,
            )
        return self._stubs['get_channel']

    @property
    def list_channels(self) -> Callable[
            [eventarc.ListChannelsRequest],
            Awaitable[eventarc.ListChannelsResponse]]:
        r"""Return a callable for the list channels method over gRPC.

        List channels.

        Returns:
            Callable[[~.ListChannelsRequest],
                    Awaitable[~.ListChannelsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_channels' not in self._stubs:
            self._stubs['list_channels'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/ListChannels',
                request_serializer=eventarc.ListChannelsRequest.serialize,
                response_deserializer=eventarc.ListChannelsResponse.deserialize,
            )
        return self._stubs['list_channels']

    @property
    def create_channel_(self) -> Callable[
            [eventarc.CreateChannelRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create channel method over gRPC.

        Create a new channel in a particular project and
        location.

        Returns:
            Callable[[~.CreateChannelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_channel_' not in self._stubs:
            self._stubs['create_channel_'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/CreateChannel',
                request_serializer=eventarc.CreateChannelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_channel_']

    @property
    def update_channel(self) -> Callable[
            [eventarc.UpdateChannelRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the update channel method over gRPC.

        Update a single channel.

        Returns:
            Callable[[~.UpdateChannelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_channel' not in self._stubs:
            self._stubs['update_channel'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/UpdateChannel',
                request_serializer=eventarc.UpdateChannelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_channel']

    @property
    def delete_channel(self) -> Callable[
            [eventarc.DeleteChannelRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete channel method over gRPC.

        Delete a single channel.

        Returns:
            Callable[[~.DeleteChannelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_channel' not in self._stubs:
            self._stubs['delete_channel'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/DeleteChannel',
                request_serializer=eventarc.DeleteChannelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_channel']

    @property
    def get_provider(self) -> Callable[
            [eventarc.GetProviderRequest],
            Awaitable[discovery.Provider]]:
        r"""Return a callable for the get provider method over gRPC.

        Get a single Provider.

        Returns:
            Callable[[~.GetProviderRequest],
                    Awaitable[~.Provider]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_provider' not in self._stubs:
            self._stubs['get_provider'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/GetProvider',
                request_serializer=eventarc.GetProviderRequest.serialize,
                response_deserializer=discovery.Provider.deserialize,
            )
        return self._stubs['get_provider']

    @property
    def list_providers(self) -> Callable[
            [eventarc.ListProvidersRequest],
            Awaitable[eventarc.ListProvidersResponse]]:
        r"""Return a callable for the list providers method over gRPC.

        List providers.

        Returns:
            Callable[[~.ListProvidersRequest],
                    Awaitable[~.ListProvidersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_providers' not in self._stubs:
            self._stubs['list_providers'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/ListProviders',
                request_serializer=eventarc.ListProvidersRequest.serialize,
                response_deserializer=eventarc.ListProvidersResponse.deserialize,
            )
        return self._stubs['list_providers']

    @property
    def get_channel_connection(self) -> Callable[
            [eventarc.GetChannelConnectionRequest],
            Awaitable[channel_connection.ChannelConnection]]:
        r"""Return a callable for the get channel connection method over gRPC.

        Get a single ChannelConnection.

        Returns:
            Callable[[~.GetChannelConnectionRequest],
                    Awaitable[~.ChannelConnection]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_channel_connection' not in self._stubs:
            self._stubs['get_channel_connection'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/GetChannelConnection',
                request_serializer=eventarc.GetChannelConnectionRequest.serialize,
                response_deserializer=channel_connection.ChannelConnection.deserialize,
            )
        return self._stubs['get_channel_connection']

    @property
    def list_channel_connections(self) -> Callable[
            [eventarc.ListChannelConnectionsRequest],
            Awaitable[eventarc.ListChannelConnectionsResponse]]:
        r"""Return a callable for the list channel connections method over gRPC.

        List channel connections.

        Returns:
            Callable[[~.ListChannelConnectionsRequest],
                    Awaitable[~.ListChannelConnectionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_channel_connections' not in self._stubs:
            self._stubs['list_channel_connections'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/ListChannelConnections',
                request_serializer=eventarc.ListChannelConnectionsRequest.serialize,
                response_deserializer=eventarc.ListChannelConnectionsResponse.deserialize,
            )
        return self._stubs['list_channel_connections']

    @property
    def create_channel_connection(self) -> Callable[
            [eventarc.CreateChannelConnectionRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create channel connection method over gRPC.

        Create a new ChannelConnection in a particular
        project and location.

        Returns:
            Callable[[~.CreateChannelConnectionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_channel_connection' not in self._stubs:
            self._stubs['create_channel_connection'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/CreateChannelConnection',
                request_serializer=eventarc.CreateChannelConnectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_channel_connection']

    @property
    def delete_channel_connection(self) -> Callable[
            [eventarc.DeleteChannelConnectionRequest],
            Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete channel connection method over gRPC.

        Delete a single ChannelConnection.

        Returns:
            Callable[[~.DeleteChannelConnectionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_channel_connection' not in self._stubs:
            self._stubs['delete_channel_connection'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/DeleteChannelConnection',
                request_serializer=eventarc.DeleteChannelConnectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_channel_connection']

    @property
    def get_google_channel_config(self) -> Callable[
            [eventarc.GetGoogleChannelConfigRequest],
            Awaitable[google_channel_config.GoogleChannelConfig]]:
        r"""Return a callable for the get google channel config method over gRPC.

        Get a GoogleChannelConfig

        Returns:
            Callable[[~.GetGoogleChannelConfigRequest],
                    Awaitable[~.GoogleChannelConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_google_channel_config' not in self._stubs:
            self._stubs['get_google_channel_config'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/GetGoogleChannelConfig',
                request_serializer=eventarc.GetGoogleChannelConfigRequest.serialize,
                response_deserializer=google_channel_config.GoogleChannelConfig.deserialize,
            )
        return self._stubs['get_google_channel_config']

    @property
    def update_google_channel_config(self) -> Callable[
            [eventarc.UpdateGoogleChannelConfigRequest],
            Awaitable[gce_google_channel_config.GoogleChannelConfig]]:
        r"""Return a callable for the update google channel config method over gRPC.

        Update a single GoogleChannelConfig

        Returns:
            Callable[[~.UpdateGoogleChannelConfigRequest],
                    Awaitable[~.GoogleChannelConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_google_channel_config' not in self._stubs:
            self._stubs['update_google_channel_config'] = self.grpc_channel.unary_unary(
                '/google.cloud.eventarc.v1.Eventarc/UpdateGoogleChannelConfig',
                request_serializer=eventarc.UpdateGoogleChannelConfigRequest.serialize,
                response_deserializer=gce_google_channel_config.GoogleChannelConfig.deserialize,
            )
        return self._stubs['update_google_channel_config']

    def close(self):
        return self.grpc_channel.close()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[[operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse]:
        r"""Return a callable for the list_operations method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[[locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse]:
        r"""Return a callable for the list locations method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the set iam policy method over gRPC.
        Sets the IAM access control policy on the specified
        function. Replaces any existing policy.
        Returns:
            Callable[[~.SetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the get iam policy method over gRPC.
        Gets the IAM access control policy for a function.
        Returns an empty policy if the function exists and does
        not have a policy set.
        Returns:
            Callable[[~.GetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest], iam_policy_pb2.TestIamPermissionsResponse
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.
        Tests the specified permissions against the IAM access control
        policy for a function. If the function does not exist, this will
        return an empty set of permissions, not a NOT_FOUND error.
        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    ~.TestIamPermissionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]


__all__ = (
    'EventarcGrpcAsyncIOTransport',
)
