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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.apigateway_v1.types import apigateway

from .base import DEFAULT_CLIENT_INFO, ApiGatewayServiceTransport
from .grpc import ApiGatewayServiceGrpcTransport


class ApiGatewayServiceGrpcAsyncIOTransport(ApiGatewayServiceTransport):
    """gRPC AsyncIO backend transport for ApiGatewayService.

    The API Gateway Service is the interface for managing API
    Gateways.

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
        host: str = "apigateway.googleapis.com",
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
        host: str = "apigateway.googleapis.com",
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
    def list_gateways(
        self,
    ) -> Callable[
        [apigateway.ListGatewaysRequest], Awaitable[apigateway.ListGatewaysResponse]
    ]:
        r"""Return a callable for the list gateways method over gRPC.

        Lists Gateways in a given project and location.

        Returns:
            Callable[[~.ListGatewaysRequest],
                    Awaitable[~.ListGatewaysResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_gateways" not in self._stubs:
            self._stubs["list_gateways"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/ListGateways",
                request_serializer=apigateway.ListGatewaysRequest.serialize,
                response_deserializer=apigateway.ListGatewaysResponse.deserialize,
            )
        return self._stubs["list_gateways"]

    @property
    def get_gateway(
        self,
    ) -> Callable[[apigateway.GetGatewayRequest], Awaitable[apigateway.Gateway]]:
        r"""Return a callable for the get gateway method over gRPC.

        Gets details of a single Gateway.

        Returns:
            Callable[[~.GetGatewayRequest],
                    Awaitable[~.Gateway]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_gateway" not in self._stubs:
            self._stubs["get_gateway"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/GetGateway",
                request_serializer=apigateway.GetGatewayRequest.serialize,
                response_deserializer=apigateway.Gateway.deserialize,
            )
        return self._stubs["get_gateway"]

    @property
    def create_gateway(
        self,
    ) -> Callable[
        [apigateway.CreateGatewayRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create gateway method over gRPC.

        Creates a new Gateway in a given project and
        location.

        Returns:
            Callable[[~.CreateGatewayRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_gateway" not in self._stubs:
            self._stubs["create_gateway"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/CreateGateway",
                request_serializer=apigateway.CreateGatewayRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_gateway"]

    @property
    def update_gateway(
        self,
    ) -> Callable[
        [apigateway.UpdateGatewayRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update gateway method over gRPC.

        Updates the parameters of a single Gateway.

        Returns:
            Callable[[~.UpdateGatewayRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_gateway" not in self._stubs:
            self._stubs["update_gateway"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/UpdateGateway",
                request_serializer=apigateway.UpdateGatewayRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_gateway"]

    @property
    def delete_gateway(
        self,
    ) -> Callable[
        [apigateway.DeleteGatewayRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete gateway method over gRPC.

        Deletes a single Gateway.

        Returns:
            Callable[[~.DeleteGatewayRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_gateway" not in self._stubs:
            self._stubs["delete_gateway"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/DeleteGateway",
                request_serializer=apigateway.DeleteGatewayRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_gateway"]

    @property
    def list_apis(
        self,
    ) -> Callable[[apigateway.ListApisRequest], Awaitable[apigateway.ListApisResponse]]:
        r"""Return a callable for the list apis method over gRPC.

        Lists Apis in a given project and location.

        Returns:
            Callable[[~.ListApisRequest],
                    Awaitable[~.ListApisResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_apis" not in self._stubs:
            self._stubs["list_apis"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/ListApis",
                request_serializer=apigateway.ListApisRequest.serialize,
                response_deserializer=apigateway.ListApisResponse.deserialize,
            )
        return self._stubs["list_apis"]

    @property
    def get_api(
        self,
    ) -> Callable[[apigateway.GetApiRequest], Awaitable[apigateway.Api]]:
        r"""Return a callable for the get api method over gRPC.

        Gets details of a single Api.

        Returns:
            Callable[[~.GetApiRequest],
                    Awaitable[~.Api]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_api" not in self._stubs:
            self._stubs["get_api"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/GetApi",
                request_serializer=apigateway.GetApiRequest.serialize,
                response_deserializer=apigateway.Api.deserialize,
            )
        return self._stubs["get_api"]

    @property
    def create_api(
        self,
    ) -> Callable[[apigateway.CreateApiRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create api method over gRPC.

        Creates a new Api in a given project and location.

        Returns:
            Callable[[~.CreateApiRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_api" not in self._stubs:
            self._stubs["create_api"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/CreateApi",
                request_serializer=apigateway.CreateApiRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_api"]

    @property
    def update_api(
        self,
    ) -> Callable[[apigateway.UpdateApiRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the update api method over gRPC.

        Updates the parameters of a single Api.

        Returns:
            Callable[[~.UpdateApiRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_api" not in self._stubs:
            self._stubs["update_api"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/UpdateApi",
                request_serializer=apigateway.UpdateApiRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_api"]

    @property
    def delete_api(
        self,
    ) -> Callable[[apigateway.DeleteApiRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the delete api method over gRPC.

        Deletes a single Api.

        Returns:
            Callable[[~.DeleteApiRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_api" not in self._stubs:
            self._stubs["delete_api"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/DeleteApi",
                request_serializer=apigateway.DeleteApiRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_api"]

    @property
    def list_api_configs(
        self,
    ) -> Callable[
        [apigateway.ListApiConfigsRequest], Awaitable[apigateway.ListApiConfigsResponse]
    ]:
        r"""Return a callable for the list api configs method over gRPC.

        Lists ApiConfigs in a given project and location.

        Returns:
            Callable[[~.ListApiConfigsRequest],
                    Awaitable[~.ListApiConfigsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_api_configs" not in self._stubs:
            self._stubs["list_api_configs"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/ListApiConfigs",
                request_serializer=apigateway.ListApiConfigsRequest.serialize,
                response_deserializer=apigateway.ListApiConfigsResponse.deserialize,
            )
        return self._stubs["list_api_configs"]

    @property
    def get_api_config(
        self,
    ) -> Callable[[apigateway.GetApiConfigRequest], Awaitable[apigateway.ApiConfig]]:
        r"""Return a callable for the get api config method over gRPC.

        Gets details of a single ApiConfig.

        Returns:
            Callable[[~.GetApiConfigRequest],
                    Awaitable[~.ApiConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_api_config" not in self._stubs:
            self._stubs["get_api_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/GetApiConfig",
                request_serializer=apigateway.GetApiConfigRequest.serialize,
                response_deserializer=apigateway.ApiConfig.deserialize,
            )
        return self._stubs["get_api_config"]

    @property
    def create_api_config(
        self,
    ) -> Callable[
        [apigateway.CreateApiConfigRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create api config method over gRPC.

        Creates a new ApiConfig in a given project and
        location.

        Returns:
            Callable[[~.CreateApiConfigRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_api_config" not in self._stubs:
            self._stubs["create_api_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/CreateApiConfig",
                request_serializer=apigateway.CreateApiConfigRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_api_config"]

    @property
    def update_api_config(
        self,
    ) -> Callable[
        [apigateway.UpdateApiConfigRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update api config method over gRPC.

        Updates the parameters of a single ApiConfig.

        Returns:
            Callable[[~.UpdateApiConfigRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_api_config" not in self._stubs:
            self._stubs["update_api_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/UpdateApiConfig",
                request_serializer=apigateway.UpdateApiConfigRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_api_config"]

    @property
    def delete_api_config(
        self,
    ) -> Callable[
        [apigateway.DeleteApiConfigRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete api config method over gRPC.

        Deletes a single ApiConfig.

        Returns:
            Callable[[~.DeleteApiConfigRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_api_config" not in self._stubs:
            self._stubs["delete_api_config"] = self.grpc_channel.unary_unary(
                "/google.cloud.apigateway.v1.ApiGatewayService/DeleteApiConfig",
                request_serializer=apigateway.DeleteApiConfigRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_api_config"]

    def close(self):
        return self.grpc_channel.close()


__all__ = ("ApiGatewayServiceGrpcAsyncIOTransport",)
