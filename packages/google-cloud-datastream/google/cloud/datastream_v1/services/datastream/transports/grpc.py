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
import json
import logging as std_logging
import pickle
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers, operations_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
import proto  # type: ignore

from google.cloud.datastream_v1.types import datastream, datastream_resources

from .base import DEFAULT_CLIENT_INFO, DatastreamTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):  # pragma: NO COVER
    def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = f"{type(request).__name__}: {pickle.dumps(request)}"

            request_metadata = {
                key: value.decode("utf-8") if isinstance(value, bytes) else value
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.cloud.datastream.v1.Datastream",
                    "rpcName": client_call_details.method,
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )

        response = continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = response.result()
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = f"{type(result).__name__}: {pickle.dumps(result)}"
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response for {client_call_details.method}.",
                extra={
                    "serviceName": "google.cloud.datastream.v1.Datastream",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class DatastreamGrpcTransport(DatastreamTransport):
    """gRPC backend transport for Datastream.

    Datastream service

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
        host: str = "datastream.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
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
                 The hostname to connect to (default: 'datastream.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
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
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, grpc.Channel):
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

        self._interceptor = _LoggingClientInterceptor()
        self._logged_channel = grpc.intercept_channel(
            self._grpc_channel, self._interceptor
        )

        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "datastream.googleapis.com",
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
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(
                self._logged_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def list_connection_profiles(
        self,
    ) -> Callable[
        [datastream.ListConnectionProfilesRequest],
        datastream.ListConnectionProfilesResponse,
    ]:
        r"""Return a callable for the list connection profiles method over gRPC.

        Use this method to list connection profiles created
        in a project and location.

        Returns:
            Callable[[~.ListConnectionProfilesRequest],
                    ~.ListConnectionProfilesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_connection_profiles" not in self._stubs:
            self._stubs["list_connection_profiles"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/ListConnectionProfiles",
                request_serializer=datastream.ListConnectionProfilesRequest.serialize,
                response_deserializer=datastream.ListConnectionProfilesResponse.deserialize,
            )
        return self._stubs["list_connection_profiles"]

    @property
    def get_connection_profile(
        self,
    ) -> Callable[
        [datastream.GetConnectionProfileRequest], datastream_resources.ConnectionProfile
    ]:
        r"""Return a callable for the get connection profile method over gRPC.

        Use this method to get details about a connection
        profile.

        Returns:
            Callable[[~.GetConnectionProfileRequest],
                    ~.ConnectionProfile]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_connection_profile" not in self._stubs:
            self._stubs["get_connection_profile"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/GetConnectionProfile",
                request_serializer=datastream.GetConnectionProfileRequest.serialize,
                response_deserializer=datastream_resources.ConnectionProfile.deserialize,
            )
        return self._stubs["get_connection_profile"]

    @property
    def create_connection_profile(
        self,
    ) -> Callable[
        [datastream.CreateConnectionProfileRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the create connection profile method over gRPC.

        Use this method to create a connection profile in a
        project and location.

        Returns:
            Callable[[~.CreateConnectionProfileRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_connection_profile" not in self._stubs:
            self._stubs["create_connection_profile"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/CreateConnectionProfile",
                request_serializer=datastream.CreateConnectionProfileRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_connection_profile"]

    @property
    def update_connection_profile(
        self,
    ) -> Callable[
        [datastream.UpdateConnectionProfileRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the update connection profile method over gRPC.

        Use this method to update the parameters of a
        connection profile.

        Returns:
            Callable[[~.UpdateConnectionProfileRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_connection_profile" not in self._stubs:
            self._stubs["update_connection_profile"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/UpdateConnectionProfile",
                request_serializer=datastream.UpdateConnectionProfileRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_connection_profile"]

    @property
    def delete_connection_profile(
        self,
    ) -> Callable[
        [datastream.DeleteConnectionProfileRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the delete connection profile method over gRPC.

        Use this method to delete a connection profile.

        Returns:
            Callable[[~.DeleteConnectionProfileRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_connection_profile" not in self._stubs:
            self._stubs["delete_connection_profile"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/DeleteConnectionProfile",
                request_serializer=datastream.DeleteConnectionProfileRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_connection_profile"]

    @property
    def discover_connection_profile(
        self,
    ) -> Callable[
        [datastream.DiscoverConnectionProfileRequest],
        datastream.DiscoverConnectionProfileResponse,
    ]:
        r"""Return a callable for the discover connection profile method over gRPC.

        Use this method to discover a connection profile.
        The discover API call exposes the data objects and
        metadata belonging to the profile. Typically, a request
        returns children data objects of a parent data object
        that's optionally supplied in the request.

        Returns:
            Callable[[~.DiscoverConnectionProfileRequest],
                    ~.DiscoverConnectionProfileResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "discover_connection_profile" not in self._stubs:
            self._stubs[
                "discover_connection_profile"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/DiscoverConnectionProfile",
                request_serializer=datastream.DiscoverConnectionProfileRequest.serialize,
                response_deserializer=datastream.DiscoverConnectionProfileResponse.deserialize,
            )
        return self._stubs["discover_connection_profile"]

    @property
    def list_streams(
        self,
    ) -> Callable[[datastream.ListStreamsRequest], datastream.ListStreamsResponse]:
        r"""Return a callable for the list streams method over gRPC.

        Use this method to list streams in a project and
        location.

        Returns:
            Callable[[~.ListStreamsRequest],
                    ~.ListStreamsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_streams" not in self._stubs:
            self._stubs["list_streams"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/ListStreams",
                request_serializer=datastream.ListStreamsRequest.serialize,
                response_deserializer=datastream.ListStreamsResponse.deserialize,
            )
        return self._stubs["list_streams"]

    @property
    def get_stream(
        self,
    ) -> Callable[[datastream.GetStreamRequest], datastream_resources.Stream]:
        r"""Return a callable for the get stream method over gRPC.

        Use this method to get details about a stream.

        Returns:
            Callable[[~.GetStreamRequest],
                    ~.Stream]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_stream" not in self._stubs:
            self._stubs["get_stream"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/GetStream",
                request_serializer=datastream.GetStreamRequest.serialize,
                response_deserializer=datastream_resources.Stream.deserialize,
            )
        return self._stubs["get_stream"]

    @property
    def create_stream(
        self,
    ) -> Callable[[datastream.CreateStreamRequest], operations_pb2.Operation]:
        r"""Return a callable for the create stream method over gRPC.

        Use this method to create a stream.

        Returns:
            Callable[[~.CreateStreamRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_stream" not in self._stubs:
            self._stubs["create_stream"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/CreateStream",
                request_serializer=datastream.CreateStreamRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_stream"]

    @property
    def update_stream(
        self,
    ) -> Callable[[datastream.UpdateStreamRequest], operations_pb2.Operation]:
        r"""Return a callable for the update stream method over gRPC.

        Use this method to update the configuration of a
        stream.

        Returns:
            Callable[[~.UpdateStreamRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_stream" not in self._stubs:
            self._stubs["update_stream"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/UpdateStream",
                request_serializer=datastream.UpdateStreamRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_stream"]

    @property
    def delete_stream(
        self,
    ) -> Callable[[datastream.DeleteStreamRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete stream method over gRPC.

        Use this method to delete a stream.

        Returns:
            Callable[[~.DeleteStreamRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_stream" not in self._stubs:
            self._stubs["delete_stream"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/DeleteStream",
                request_serializer=datastream.DeleteStreamRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_stream"]

    @property
    def run_stream(
        self,
    ) -> Callable[[datastream.RunStreamRequest], operations_pb2.Operation]:
        r"""Return a callable for the run stream method over gRPC.

        Use this method to start, resume or recover a stream
        with a non default CDC strategy.

        Returns:
            Callable[[~.RunStreamRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_stream" not in self._stubs:
            self._stubs["run_stream"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/RunStream",
                request_serializer=datastream.RunStreamRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["run_stream"]

    @property
    def get_stream_object(
        self,
    ) -> Callable[
        [datastream.GetStreamObjectRequest], datastream_resources.StreamObject
    ]:
        r"""Return a callable for the get stream object method over gRPC.

        Use this method to get details about a stream object.

        Returns:
            Callable[[~.GetStreamObjectRequest],
                    ~.StreamObject]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_stream_object" not in self._stubs:
            self._stubs["get_stream_object"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/GetStreamObject",
                request_serializer=datastream.GetStreamObjectRequest.serialize,
                response_deserializer=datastream_resources.StreamObject.deserialize,
            )
        return self._stubs["get_stream_object"]

    @property
    def lookup_stream_object(
        self,
    ) -> Callable[
        [datastream.LookupStreamObjectRequest], datastream_resources.StreamObject
    ]:
        r"""Return a callable for the lookup stream object method over gRPC.

        Use this method to look up a stream object by its
        source object identifier.

        Returns:
            Callable[[~.LookupStreamObjectRequest],
                    ~.StreamObject]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "lookup_stream_object" not in self._stubs:
            self._stubs["lookup_stream_object"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/LookupStreamObject",
                request_serializer=datastream.LookupStreamObjectRequest.serialize,
                response_deserializer=datastream_resources.StreamObject.deserialize,
            )
        return self._stubs["lookup_stream_object"]

    @property
    def list_stream_objects(
        self,
    ) -> Callable[
        [datastream.ListStreamObjectsRequest], datastream.ListStreamObjectsResponse
    ]:
        r"""Return a callable for the list stream objects method over gRPC.

        Use this method to list the objects of a specific
        stream.

        Returns:
            Callable[[~.ListStreamObjectsRequest],
                    ~.ListStreamObjectsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_stream_objects" not in self._stubs:
            self._stubs["list_stream_objects"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/ListStreamObjects",
                request_serializer=datastream.ListStreamObjectsRequest.serialize,
                response_deserializer=datastream.ListStreamObjectsResponse.deserialize,
            )
        return self._stubs["list_stream_objects"]

    @property
    def start_backfill_job(
        self,
    ) -> Callable[
        [datastream.StartBackfillJobRequest], datastream.StartBackfillJobResponse
    ]:
        r"""Return a callable for the start backfill job method over gRPC.

        Use this method to start a backfill job for the
        specified stream object.

        Returns:
            Callable[[~.StartBackfillJobRequest],
                    ~.StartBackfillJobResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_backfill_job" not in self._stubs:
            self._stubs["start_backfill_job"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/StartBackfillJob",
                request_serializer=datastream.StartBackfillJobRequest.serialize,
                response_deserializer=datastream.StartBackfillJobResponse.deserialize,
            )
        return self._stubs["start_backfill_job"]

    @property
    def stop_backfill_job(
        self,
    ) -> Callable[
        [datastream.StopBackfillJobRequest], datastream.StopBackfillJobResponse
    ]:
        r"""Return a callable for the stop backfill job method over gRPC.

        Use this method to stop a backfill job for the
        specified stream object.

        Returns:
            Callable[[~.StopBackfillJobRequest],
                    ~.StopBackfillJobResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "stop_backfill_job" not in self._stubs:
            self._stubs["stop_backfill_job"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/StopBackfillJob",
                request_serializer=datastream.StopBackfillJobRequest.serialize,
                response_deserializer=datastream.StopBackfillJobResponse.deserialize,
            )
        return self._stubs["stop_backfill_job"]

    @property
    def fetch_static_ips(
        self,
    ) -> Callable[
        [datastream.FetchStaticIpsRequest], datastream.FetchStaticIpsResponse
    ]:
        r"""Return a callable for the fetch static ips method over gRPC.

        The FetchStaticIps API call exposes the static IP
        addresses used by Datastream.

        Returns:
            Callable[[~.FetchStaticIpsRequest],
                    ~.FetchStaticIpsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_static_ips" not in self._stubs:
            self._stubs["fetch_static_ips"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/FetchStaticIps",
                request_serializer=datastream.FetchStaticIpsRequest.serialize,
                response_deserializer=datastream.FetchStaticIpsResponse.deserialize,
            )
        return self._stubs["fetch_static_ips"]

    @property
    def create_private_connection(
        self,
    ) -> Callable[
        [datastream.CreatePrivateConnectionRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the create private connection method over gRPC.

        Use this method to create a private connectivity
        configuration.

        Returns:
            Callable[[~.CreatePrivateConnectionRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_private_connection" not in self._stubs:
            self._stubs["create_private_connection"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/CreatePrivateConnection",
                request_serializer=datastream.CreatePrivateConnectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_private_connection"]

    @property
    def get_private_connection(
        self,
    ) -> Callable[
        [datastream.GetPrivateConnectionRequest], datastream_resources.PrivateConnection
    ]:
        r"""Return a callable for the get private connection method over gRPC.

        Use this method to get details about a private
        connectivity configuration.

        Returns:
            Callable[[~.GetPrivateConnectionRequest],
                    ~.PrivateConnection]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_private_connection" not in self._stubs:
            self._stubs["get_private_connection"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/GetPrivateConnection",
                request_serializer=datastream.GetPrivateConnectionRequest.serialize,
                response_deserializer=datastream_resources.PrivateConnection.deserialize,
            )
        return self._stubs["get_private_connection"]

    @property
    def list_private_connections(
        self,
    ) -> Callable[
        [datastream.ListPrivateConnectionsRequest],
        datastream.ListPrivateConnectionsResponse,
    ]:
        r"""Return a callable for the list private connections method over gRPC.

        Use this method to list private connectivity
        configurations in a project and location.

        Returns:
            Callable[[~.ListPrivateConnectionsRequest],
                    ~.ListPrivateConnectionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_private_connections" not in self._stubs:
            self._stubs["list_private_connections"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/ListPrivateConnections",
                request_serializer=datastream.ListPrivateConnectionsRequest.serialize,
                response_deserializer=datastream.ListPrivateConnectionsResponse.deserialize,
            )
        return self._stubs["list_private_connections"]

    @property
    def delete_private_connection(
        self,
    ) -> Callable[
        [datastream.DeletePrivateConnectionRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the delete private connection method over gRPC.

        Use this method to delete a private connectivity
        configuration.

        Returns:
            Callable[[~.DeletePrivateConnectionRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_private_connection" not in self._stubs:
            self._stubs["delete_private_connection"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/DeletePrivateConnection",
                request_serializer=datastream.DeletePrivateConnectionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_private_connection"]

    @property
    def create_route(
        self,
    ) -> Callable[[datastream.CreateRouteRequest], operations_pb2.Operation]:
        r"""Return a callable for the create route method over gRPC.

        Use this method to create a route for a private
        connectivity configuration in a project and location.

        Returns:
            Callable[[~.CreateRouteRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_route" not in self._stubs:
            self._stubs["create_route"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/CreateRoute",
                request_serializer=datastream.CreateRouteRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_route"]

    @property
    def get_route(
        self,
    ) -> Callable[[datastream.GetRouteRequest], datastream_resources.Route]:
        r"""Return a callable for the get route method over gRPC.

        Use this method to get details about a route.

        Returns:
            Callable[[~.GetRouteRequest],
                    ~.Route]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_route" not in self._stubs:
            self._stubs["get_route"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/GetRoute",
                request_serializer=datastream.GetRouteRequest.serialize,
                response_deserializer=datastream_resources.Route.deserialize,
            )
        return self._stubs["get_route"]

    @property
    def list_routes(
        self,
    ) -> Callable[[datastream.ListRoutesRequest], datastream.ListRoutesResponse]:
        r"""Return a callable for the list routes method over gRPC.

        Use this method to list routes created for a private
        connectivity configuration in a project and location.

        Returns:
            Callable[[~.ListRoutesRequest],
                    ~.ListRoutesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_routes" not in self._stubs:
            self._stubs["list_routes"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/ListRoutes",
                request_serializer=datastream.ListRoutesRequest.serialize,
                response_deserializer=datastream.ListRoutesResponse.deserialize,
            )
        return self._stubs["list_routes"]

    @property
    def delete_route(
        self,
    ) -> Callable[[datastream.DeleteRouteRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete route method over gRPC.

        Use this method to delete a route.

        Returns:
            Callable[[~.DeleteRouteRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_route" not in self._stubs:
            self._stubs["delete_route"] = self._logged_channel.unary_unary(
                "/google.cloud.datastream.v1.Datastream/DeleteRoute",
                request_serializer=datastream.DeleteRouteRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_route"]

    def close(self):
        self._logged_channel.close()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("DatastreamGrpcTransport",)
