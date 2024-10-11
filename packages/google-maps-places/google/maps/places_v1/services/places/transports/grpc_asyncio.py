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

from google.maps.places_v1.types import place, places_service

from .base import DEFAULT_CLIENT_INFO, PlacesTransport
from .grpc import PlacesGrpcTransport


class PlacesGrpcAsyncIOTransport(PlacesTransport):
    """gRPC AsyncIO backend transport for Places.

    Service definition for the Places API. Note: every request (except
    for Autocomplete requests) requires a field mask set outside of the
    request proto (``all/*``, is not assumed). The field mask can be set
    via the HTTP header ``X-Goog-FieldMask``. See:
    https://developers.google.com/maps/documentation/places/web-service/choose-fields

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
        host: str = "places.googleapis.com",
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
        host: str = "places.googleapis.com",
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
                 The hostname to connect to (default: 'places.googleapis.com').
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
    def search_nearby(
        self,
    ) -> Callable[
        [places_service.SearchNearbyRequest],
        Awaitable[places_service.SearchNearbyResponse],
    ]:
        r"""Return a callable for the search nearby method over gRPC.

        Search for places near locations.

        Returns:
            Callable[[~.SearchNearbyRequest],
                    Awaitable[~.SearchNearbyResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_nearby" not in self._stubs:
            self._stubs["search_nearby"] = self.grpc_channel.unary_unary(
                "/google.maps.places.v1.Places/SearchNearby",
                request_serializer=places_service.SearchNearbyRequest.serialize,
                response_deserializer=places_service.SearchNearbyResponse.deserialize,
            )
        return self._stubs["search_nearby"]

    @property
    def search_text(
        self,
    ) -> Callable[
        [places_service.SearchTextRequest], Awaitable[places_service.SearchTextResponse]
    ]:
        r"""Return a callable for the search text method over gRPC.

        Text query based place search.

        Returns:
            Callable[[~.SearchTextRequest],
                    Awaitable[~.SearchTextResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_text" not in self._stubs:
            self._stubs["search_text"] = self.grpc_channel.unary_unary(
                "/google.maps.places.v1.Places/SearchText",
                request_serializer=places_service.SearchTextRequest.serialize,
                response_deserializer=places_service.SearchTextResponse.deserialize,
            )
        return self._stubs["search_text"]

    @property
    def get_photo_media(
        self,
    ) -> Callable[
        [places_service.GetPhotoMediaRequest], Awaitable[places_service.PhotoMedia]
    ]:
        r"""Return a callable for the get photo media method over gRPC.

        Get a photo media with a photo reference string.

        Returns:
            Callable[[~.GetPhotoMediaRequest],
                    Awaitable[~.PhotoMedia]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_photo_media" not in self._stubs:
            self._stubs["get_photo_media"] = self.grpc_channel.unary_unary(
                "/google.maps.places.v1.Places/GetPhotoMedia",
                request_serializer=places_service.GetPhotoMediaRequest.serialize,
                response_deserializer=places_service.PhotoMedia.deserialize,
            )
        return self._stubs["get_photo_media"]

    @property
    def get_place(
        self,
    ) -> Callable[[places_service.GetPlaceRequest], Awaitable[place.Place]]:
        r"""Return a callable for the get place method over gRPC.

        Get the details of a place based on its resource name, which is
        a string in the ``places/{place_id}`` format.

        Returns:
            Callable[[~.GetPlaceRequest],
                    Awaitable[~.Place]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_place" not in self._stubs:
            self._stubs["get_place"] = self.grpc_channel.unary_unary(
                "/google.maps.places.v1.Places/GetPlace",
                request_serializer=places_service.GetPlaceRequest.serialize,
                response_deserializer=place.Place.deserialize,
            )
        return self._stubs["get_place"]

    @property
    def autocomplete_places(
        self,
    ) -> Callable[
        [places_service.AutocompletePlacesRequest],
        Awaitable[places_service.AutocompletePlacesResponse],
    ]:
        r"""Return a callable for the autocomplete places method over gRPC.

        Returns predictions for the given input.

        Returns:
            Callable[[~.AutocompletePlacesRequest],
                    Awaitable[~.AutocompletePlacesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "autocomplete_places" not in self._stubs:
            self._stubs["autocomplete_places"] = self.grpc_channel.unary_unary(
                "/google.maps.places.v1.Places/AutocompletePlaces",
                request_serializer=places_service.AutocompletePlacesRequest.serialize,
                response_deserializer=places_service.AutocompletePlacesResponse.deserialize,
            )
        return self._stubs["autocomplete_places"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.search_nearby: self._wrap_method(
                self.search_nearby,
                default_timeout=None,
                client_info=client_info,
            ),
            self.search_text: self._wrap_method(
                self.search_text,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_photo_media: self._wrap_method(
                self.get_photo_media,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_place: self._wrap_method(
                self.get_place,
                default_timeout=None,
                client_info=client_info,
            ),
            self.autocomplete_places: self._wrap_method(
                self.autocomplete_places,
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


__all__ = ("PlacesGrpcAsyncIOTransport",)
