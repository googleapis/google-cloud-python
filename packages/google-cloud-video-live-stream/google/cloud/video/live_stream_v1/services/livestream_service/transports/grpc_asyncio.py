# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.video.live_stream_v1.types import resources
from google.cloud.video.live_stream_v1.types import service
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from .base import LivestreamServiceTransport, DEFAULT_CLIENT_INFO
from .grpc import LivestreamServiceGrpcTransport


class LivestreamServiceGrpcAsyncIOTransport(LivestreamServiceTransport):
    """gRPC AsyncIO backend transport for LivestreamService.

    Using Live Stream API, you can generate live streams in the
    various renditions and streaming formats. The streaming format
    include HTTP Live Streaming (HLS) and Dynamic Adaptive Streaming
    over HTTP (DASH). You can send a source stream in the various
    ways, including Real-Time Messaging Protocol (RTMP) and Secure
    Reliable Transport (SRT).

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
        host: str = "livestream.googleapis.com",
        credentials: ga_credentials.Credentials = None,
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
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "livestream.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
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
    def create_channel_(
        self,
    ) -> Callable[[service.CreateChannelRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create channel method over gRPC.

        Creates a channel with the provided unique ID in the
        specified region.

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
        if "create_channel_" not in self._stubs:
            self._stubs["create_channel_"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/CreateChannel",
                request_serializer=service.CreateChannelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_channel_"]

    @property
    def list_channels(
        self,
    ) -> Callable[
        [service.ListChannelsRequest], Awaitable[service.ListChannelsResponse]
    ]:
        r"""Return a callable for the list channels method over gRPC.

        Returns a list of all channels in the specified
        region.

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
        if "list_channels" not in self._stubs:
            self._stubs["list_channels"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/ListChannels",
                request_serializer=service.ListChannelsRequest.serialize,
                response_deserializer=service.ListChannelsResponse.deserialize,
            )
        return self._stubs["list_channels"]

    @property
    def get_channel(
        self,
    ) -> Callable[[service.GetChannelRequest], Awaitable[resources.Channel]]:
        r"""Return a callable for the get channel method over gRPC.

        Returns the specified channel.

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
        if "get_channel" not in self._stubs:
            self._stubs["get_channel"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/GetChannel",
                request_serializer=service.GetChannelRequest.serialize,
                response_deserializer=resources.Channel.deserialize,
            )
        return self._stubs["get_channel"]

    @property
    def delete_channel(
        self,
    ) -> Callable[[service.DeleteChannelRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete channel method over gRPC.

        Deletes the specified channel.

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
        if "delete_channel" not in self._stubs:
            self._stubs["delete_channel"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/DeleteChannel",
                request_serializer=service.DeleteChannelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_channel"]

    @property
    def update_channel(
        self,
    ) -> Callable[[service.UpdateChannelRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the update channel method over gRPC.

        Updates the specified channel.

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
        if "update_channel" not in self._stubs:
            self._stubs["update_channel"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/UpdateChannel",
                request_serializer=service.UpdateChannelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_channel"]

    @property
    def start_channel(
        self,
    ) -> Callable[[service.StartChannelRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the start channel method over gRPC.

        Starts the specified channel. Part of the video
        pipeline will be created only when the StartChannel
        request is received by the server.

        Returns:
            Callable[[~.StartChannelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_channel" not in self._stubs:
            self._stubs["start_channel"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/StartChannel",
                request_serializer=service.StartChannelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["start_channel"]

    @property
    def stop_channel(
        self,
    ) -> Callable[[service.StopChannelRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the stop channel method over gRPC.

        Stops the specified channel. Part of the video
        pipeline will be released when the StopChannel request
        is received by the server.

        Returns:
            Callable[[~.StopChannelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "stop_channel" not in self._stubs:
            self._stubs["stop_channel"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/StopChannel",
                request_serializer=service.StopChannelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["stop_channel"]

    @property
    def create_input(
        self,
    ) -> Callable[[service.CreateInputRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create input method over gRPC.

        Creates an input with the provided unique ID in the
        specified region.

        Returns:
            Callable[[~.CreateInputRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_input" not in self._stubs:
            self._stubs["create_input"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/CreateInput",
                request_serializer=service.CreateInputRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_input"]

    @property
    def list_inputs(
        self,
    ) -> Callable[[service.ListInputsRequest], Awaitable[service.ListInputsResponse]]:
        r"""Return a callable for the list inputs method over gRPC.

        Returns a list of all inputs in the specified region.

        Returns:
            Callable[[~.ListInputsRequest],
                    Awaitable[~.ListInputsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_inputs" not in self._stubs:
            self._stubs["list_inputs"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/ListInputs",
                request_serializer=service.ListInputsRequest.serialize,
                response_deserializer=service.ListInputsResponse.deserialize,
            )
        return self._stubs["list_inputs"]

    @property
    def get_input(
        self,
    ) -> Callable[[service.GetInputRequest], Awaitable[resources.Input]]:
        r"""Return a callable for the get input method over gRPC.

        Returns the specified input.

        Returns:
            Callable[[~.GetInputRequest],
                    Awaitable[~.Input]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_input" not in self._stubs:
            self._stubs["get_input"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/GetInput",
                request_serializer=service.GetInputRequest.serialize,
                response_deserializer=resources.Input.deserialize,
            )
        return self._stubs["get_input"]

    @property
    def delete_input(
        self,
    ) -> Callable[[service.DeleteInputRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete input method over gRPC.

        Deletes the specified input.

        Returns:
            Callable[[~.DeleteInputRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_input" not in self._stubs:
            self._stubs["delete_input"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/DeleteInput",
                request_serializer=service.DeleteInputRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_input"]

    @property
    def update_input(
        self,
    ) -> Callable[[service.UpdateInputRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the update input method over gRPC.

        Updates the specified input.

        Returns:
            Callable[[~.UpdateInputRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_input" not in self._stubs:
            self._stubs["update_input"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/UpdateInput",
                request_serializer=service.UpdateInputRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_input"]

    @property
    def create_event(
        self,
    ) -> Callable[[service.CreateEventRequest], Awaitable[resources.Event]]:
        r"""Return a callable for the create event method over gRPC.

        Creates an event with the provided unique ID in the
        specified channel.

        Returns:
            Callable[[~.CreateEventRequest],
                    Awaitable[~.Event]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_event" not in self._stubs:
            self._stubs["create_event"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/CreateEvent",
                request_serializer=service.CreateEventRequest.serialize,
                response_deserializer=resources.Event.deserialize,
            )
        return self._stubs["create_event"]

    @property
    def list_events(
        self,
    ) -> Callable[[service.ListEventsRequest], Awaitable[service.ListEventsResponse]]:
        r"""Return a callable for the list events method over gRPC.

        Returns a list of all events in the specified
        channel.

        Returns:
            Callable[[~.ListEventsRequest],
                    Awaitable[~.ListEventsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_events" not in self._stubs:
            self._stubs["list_events"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/ListEvents",
                request_serializer=service.ListEventsRequest.serialize,
                response_deserializer=service.ListEventsResponse.deserialize,
            )
        return self._stubs["list_events"]

    @property
    def get_event(
        self,
    ) -> Callable[[service.GetEventRequest], Awaitable[resources.Event]]:
        r"""Return a callable for the get event method over gRPC.

        Returns the specified event.

        Returns:
            Callable[[~.GetEventRequest],
                    Awaitable[~.Event]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_event" not in self._stubs:
            self._stubs["get_event"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/GetEvent",
                request_serializer=service.GetEventRequest.serialize,
                response_deserializer=resources.Event.deserialize,
            )
        return self._stubs["get_event"]

    @property
    def delete_event(
        self,
    ) -> Callable[[service.DeleteEventRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete event method over gRPC.

        Deletes the specified event.

        Returns:
            Callable[[~.DeleteEventRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_event" not in self._stubs:
            self._stubs["delete_event"] = self.grpc_channel.unary_unary(
                "/google.cloud.video.livestream.v1.LivestreamService/DeleteEvent",
                request_serializer=service.DeleteEventRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_event"]

    def close(self):
        return self.grpc_channel.close()


__all__ = ("LivestreamServiceGrpcAsyncIOTransport",)
