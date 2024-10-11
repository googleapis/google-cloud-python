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
import inspect
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.maps.routing_v2.types import routes_service

from .base import DEFAULT_CLIENT_INFO, RoutesTransport
from .grpc import RoutesGrpcTransport


class RoutesGrpcAsyncIOTransport(RoutesTransport):
    """gRPC AsyncIO backend transport for Routes.

    The Routes API.

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
        host: str = "routes.googleapis.com",
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
        host: str = "routes.googleapis.com",
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
                 The hostname to connect to (default: 'routes.googleapis.com').
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
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
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
    def compute_routes(
        self,
    ) -> Callable[
        [routes_service.ComputeRoutesRequest],
        Awaitable[routes_service.ComputeRoutesResponse],
    ]:
        r"""Return a callable for the compute routes method over gRPC.

        Returns the primary route along with optional alternate routes,
        given a set of terminal and intermediate waypoints.

        **NOTE:** This method requires that you specify a response field
        mask in the input. You can provide the response field mask by
        using URL parameter ``$fields`` or ``fields``, or by using an
        HTTP/gRPC header ``X-Goog-FieldMask`` (see the `available URL
        parameters and
        headers <https://cloud.google.com/apis/docs/system-parameters>`__).
        The value is a comma separated list of field paths. See detailed
        documentation about `how to construct the field
        paths <https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/field_mask.proto>`__.

        For example, in this method:

        -  Field mask of all available fields (for manual inspection):
           ``X-Goog-FieldMask: *``
        -  Field mask of Route-level duration, distance, and polyline
           (an example production setup):
           ``X-Goog-FieldMask: routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline``

        Google discourage the use of the wildcard (``*``) response field
        mask, or specifying the field mask at the top level
        (``routes``), because:

        -  Selecting only the fields that you need helps our server save
           computation cycles, allowing us to return the result to you
           with a lower latency.
        -  Selecting only the fields that you need in your production
           job ensures stable latency performance. We might add more
           response fields in the future, and those new fields might
           require extra computation time. If you select all fields, or
           if you select all fields at the top level, then you might
           experience performance degradation because any new field we
           add will be automatically included in the response.
        -  Selecting only the fields that you need results in a smaller
           response size, and thus higher network throughput.

        Returns:
            Callable[[~.ComputeRoutesRequest],
                    Awaitable[~.ComputeRoutesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "compute_routes" not in self._stubs:
            self._stubs["compute_routes"] = self.grpc_channel.unary_unary(
                "/google.maps.routing.v2.Routes/ComputeRoutes",
                request_serializer=routes_service.ComputeRoutesRequest.serialize,
                response_deserializer=routes_service.ComputeRoutesResponse.deserialize,
            )
        return self._stubs["compute_routes"]

    @property
    def compute_route_matrix(
        self,
    ) -> Callable[
        [routes_service.ComputeRouteMatrixRequest],
        Awaitable[routes_service.RouteMatrixElement],
    ]:
        r"""Return a callable for the compute route matrix method over gRPC.

        Takes in a list of origins and destinations and returns a stream
        containing route information for each combination of origin and
        destination.

        **NOTE:** This method requires that you specify a response field
        mask in the input. You can provide the response field mask by
        using the URL parameter ``$fields`` or ``fields``, or by using
        the HTTP/gRPC header ``X-Goog-FieldMask`` (see the `available
        URL parameters and
        headers <https://cloud.google.com/apis/docs/system-parameters>`__).
        The value is a comma separated list of field paths. See this
        detailed documentation about `how to construct the field
        paths <https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/field_mask.proto>`__.

        For example, in this method:

        -  Field mask of all available fields (for manual inspection):
           ``X-Goog-FieldMask: *``
        -  Field mask of route durations, distances, element status,
           condition, and element indices (an example production setup):
           ``X-Goog-FieldMask: originIndex,destinationIndex,status,condition,distanceMeters,duration``

        It is critical that you include ``status`` in your field mask as
        otherwise all messages will appear to be OK. Google discourages
        the use of the wildcard (``*``) response field mask, because:

        -  Selecting only the fields that you need helps our server save
           computation cycles, allowing us to return the result to you
           with a lower latency.
        -  Selecting only the fields that you need in your production
           job ensures stable latency performance. We might add more
           response fields in the future, and those new fields might
           require extra computation time. If you select all fields, or
           if you select all fields at the top level, then you might
           experience performance degradation because any new field we
           add will be automatically included in the response.
        -  Selecting only the fields that you need results in a smaller
           response size, and thus higher network throughput.

        Returns:
            Callable[[~.ComputeRouteMatrixRequest],
                    Awaitable[~.RouteMatrixElement]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "compute_route_matrix" not in self._stubs:
            self._stubs["compute_route_matrix"] = self.grpc_channel.unary_stream(
                "/google.maps.routing.v2.Routes/ComputeRouteMatrix",
                request_serializer=routes_service.ComputeRouteMatrixRequest.serialize,
                response_deserializer=routes_service.RouteMatrixElement.deserialize,
            )
        return self._stubs["compute_route_matrix"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.compute_routes: self._wrap_method(
                self.compute_routes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.compute_route_matrix: self._wrap_method(
                self.compute_route_matrix,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"


__all__ = ("RoutesGrpcAsyncIOTransport",)
