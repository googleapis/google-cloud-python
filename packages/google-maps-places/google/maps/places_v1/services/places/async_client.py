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
from collections import OrderedDict
import functools
import re
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry_async as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.maps.places_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object]  # type: ignore

from google.geo.type.types import viewport
from google.type import latlng_pb2  # type: ignore
from google.type import localized_text_pb2  # type: ignore

from google.maps.places_v1.types import (
    ev_charging,
    fuel_options,
    photo,
    place,
    places_service,
    review,
)

from .client import PlacesClient
from .transports.base import DEFAULT_CLIENT_INFO, PlacesTransport
from .transports.grpc_asyncio import PlacesGrpcAsyncIOTransport


class PlacesAsyncClient:
    """Service definition for the Places API. Note: every request actually
    requires a field mask set outside of the request proto (all/'*' is
    not assumed). That can be set via either a side channel
    (SystemParameterContext) over RPC, or a header (X-Goog-FieldMask)
    over HTTP. See: https://cloud.google.com/apis/docs/system-parameters
    """

    _client: PlacesClient

    DEFAULT_ENDPOINT = PlacesClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = PlacesClient.DEFAULT_MTLS_ENDPOINT

    photo_path = staticmethod(PlacesClient.photo_path)
    parse_photo_path = staticmethod(PlacesClient.parse_photo_path)
    photo_media_path = staticmethod(PlacesClient.photo_media_path)
    parse_photo_media_path = staticmethod(PlacesClient.parse_photo_media_path)
    place_path = staticmethod(PlacesClient.place_path)
    parse_place_path = staticmethod(PlacesClient.parse_place_path)
    review_path = staticmethod(PlacesClient.review_path)
    parse_review_path = staticmethod(PlacesClient.parse_review_path)
    common_billing_account_path = staticmethod(PlacesClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(
        PlacesClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(PlacesClient.common_folder_path)
    parse_common_folder_path = staticmethod(PlacesClient.parse_common_folder_path)
    common_organization_path = staticmethod(PlacesClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        PlacesClient.parse_common_organization_path
    )
    common_project_path = staticmethod(PlacesClient.common_project_path)
    parse_common_project_path = staticmethod(PlacesClient.parse_common_project_path)
    common_location_path = staticmethod(PlacesClient.common_location_path)
    parse_common_location_path = staticmethod(PlacesClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            PlacesAsyncClient: The constructed client.
        """
        return PlacesClient.from_service_account_info.__func__(PlacesAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            PlacesAsyncClient: The constructed client.
        """
        return PlacesClient.from_service_account_file.__func__(PlacesAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return PlacesClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> PlacesTransport:
        """Returns the transport used by the client instance.

        Returns:
            PlacesTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(PlacesClient).get_transport_class, type(PlacesClient)
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, PlacesTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the places client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.PlacesTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = PlacesClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def search_nearby(
        self,
        request: Optional[Union[places_service.SearchNearbyRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> places_service.SearchNearbyResponse:
        r"""Search for places near locations.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.maps import places_v1

            async def sample_search_nearby():
                # Create a client
                client = places_v1.PlacesAsyncClient()

                # Initialize request argument(s)
                location_restriction = places_v1.LocationRestriction()
                location_restriction.circle.radius = 0.648

                request = places_v1.SearchNearbyRequest(
                    location_restriction=location_restriction,
                )

                # Make the request
                response = await client.search_nearby(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.maps.places_v1.types.SearchNearbyRequest, dict]]):
                The request object. Request proto for Search Nearby.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.maps.places_v1.types.SearchNearbyResponse:
                Response proto for Search Nearby.
        """
        # Create or coerce a protobuf request object.
        request = places_service.SearchNearbyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_nearby,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def search_text(
        self,
        request: Optional[Union[places_service.SearchTextRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> places_service.SearchTextResponse:
        r"""Text query based place search.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.maps import places_v1

            async def sample_search_text():
                # Create a client
                client = places_v1.PlacesAsyncClient()

                # Initialize request argument(s)
                request = places_v1.SearchTextRequest(
                    text_query="text_query_value",
                )

                # Make the request
                response = await client.search_text(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.maps.places_v1.types.SearchTextRequest, dict]]):
                The request object. Request proto for SearchText.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.maps.places_v1.types.SearchTextResponse:
                Response proto for SearchText.
        """
        # Create or coerce a protobuf request object.
        request = places_service.SearchTextRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_text,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_photo_media(
        self,
        request: Optional[Union[places_service.GetPhotoMediaRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> places_service.PhotoMedia:
        r"""Get a photo media with a photo reference string.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.maps import places_v1

            async def sample_get_photo_media():
                # Create a client
                client = places_v1.PlacesAsyncClient()

                # Initialize request argument(s)
                request = places_v1.GetPhotoMediaRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_photo_media(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.maps.places_v1.types.GetPhotoMediaRequest, dict]]):
                The request object. Request for fetching a photo of a
                place using a photo resource name.
            name (:class:`str`):
                Required. The resource name of a photo. It is returned
                in Place's photos.name field. Format:
                places/<place_id>/photos/<photo_reference>/media.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.maps.places_v1.types.PhotoMedia:
                A photo media from Places API.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = places_service.GetPhotoMediaRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_photo_media,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_place(
        self,
        request: Optional[Union[places_service.GetPlaceRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> place.Place:
        r"""Get a Place with a place id (in a name) string.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.maps import places_v1

            async def sample_get_place():
                # Create a client
                client = places_v1.PlacesAsyncClient()

                # Initialize request argument(s)
                request = places_v1.GetPlaceRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_place(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.maps.places_v1.types.GetPlaceRequest, dict]]):
                The request object. Request for fetching a Place with a
                place id (in a name) string.
            name (:class:`str`):
                Required. A place_id returned in a Place (with "places/"
                prefix), or equivalently the name in the same Place.
                Format: places/<place_id>.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.maps.places_v1.types.Place:
                All the information representing a
                Place.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = places_service.GetPlaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_place,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "PlacesAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("PlacesAsyncClient",)
