# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.video.stitcher_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore

from google.cloud.video.stitcher_v1.services.video_stitcher_service import pagers
from google.cloud.video.stitcher_v1.types import (
    ad_tag_details,
    cdn_keys,
    sessions,
    slates,
    stitch_details,
    video_stitcher_service,
)

from .client import VideoStitcherServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, VideoStitcherServiceTransport
from .transports.grpc_asyncio import VideoStitcherServiceGrpcAsyncIOTransport


class VideoStitcherServiceAsyncClient:
    """Video-On-Demand content stitching API allows you to insert
    ads into (VoD) video on demand files. You will be able to render
    custom scrubber bars with highlighted ads, enforce ad policies,
    allow seamless playback and tracking on native players and
    monetize content with any standard VMAP compliant ad server.
    """

    _client: VideoStitcherServiceClient

    DEFAULT_ENDPOINT = VideoStitcherServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = VideoStitcherServiceClient.DEFAULT_MTLS_ENDPOINT

    cdn_key_path = staticmethod(VideoStitcherServiceClient.cdn_key_path)
    parse_cdn_key_path = staticmethod(VideoStitcherServiceClient.parse_cdn_key_path)
    live_ad_tag_detail_path = staticmethod(
        VideoStitcherServiceClient.live_ad_tag_detail_path
    )
    parse_live_ad_tag_detail_path = staticmethod(
        VideoStitcherServiceClient.parse_live_ad_tag_detail_path
    )
    live_session_path = staticmethod(VideoStitcherServiceClient.live_session_path)
    parse_live_session_path = staticmethod(
        VideoStitcherServiceClient.parse_live_session_path
    )
    slate_path = staticmethod(VideoStitcherServiceClient.slate_path)
    parse_slate_path = staticmethod(VideoStitcherServiceClient.parse_slate_path)
    vod_ad_tag_detail_path = staticmethod(
        VideoStitcherServiceClient.vod_ad_tag_detail_path
    )
    parse_vod_ad_tag_detail_path = staticmethod(
        VideoStitcherServiceClient.parse_vod_ad_tag_detail_path
    )
    vod_session_path = staticmethod(VideoStitcherServiceClient.vod_session_path)
    parse_vod_session_path = staticmethod(
        VideoStitcherServiceClient.parse_vod_session_path
    )
    vod_stitch_detail_path = staticmethod(
        VideoStitcherServiceClient.vod_stitch_detail_path
    )
    parse_vod_stitch_detail_path = staticmethod(
        VideoStitcherServiceClient.parse_vod_stitch_detail_path
    )
    common_billing_account_path = staticmethod(
        VideoStitcherServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        VideoStitcherServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(VideoStitcherServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        VideoStitcherServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        VideoStitcherServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        VideoStitcherServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(VideoStitcherServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        VideoStitcherServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(VideoStitcherServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        VideoStitcherServiceClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            VideoStitcherServiceAsyncClient: The constructed client.
        """
        return VideoStitcherServiceClient.from_service_account_info.__func__(VideoStitcherServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            VideoStitcherServiceAsyncClient: The constructed client.
        """
        return VideoStitcherServiceClient.from_service_account_file.__func__(VideoStitcherServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        default mTLS endpoint; if the environment variabel is "never", use the default API
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
        return VideoStitcherServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> VideoStitcherServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            VideoStitcherServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(VideoStitcherServiceClient).get_transport_class,
        type(VideoStitcherServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, VideoStitcherServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the video stitcher service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.VideoStitcherServiceTransport]): The
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
        self._client = VideoStitcherServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_cdn_key(
        self,
        request: Optional[
            Union[video_stitcher_service.CreateCdnKeyRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        cdn_key: Optional[cdn_keys.CdnKey] = None,
        cdn_key_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cdn_keys.CdnKey:
        r"""Creates a new CDN key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_create_cdn_key():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.CreateCdnKeyRequest(
                    parent="parent_value",
                    cdn_key_id="cdn_key_id_value",
                )

                # Make the request
                response = await client.create_cdn_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.CreateCdnKeyRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.createCdnKey.
            parent (:class:`str`):
                Required. The project in which the CDN key should be
                created, in the form of
                ``projects/{project_number}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cdn_key (:class:`google.cloud.video.stitcher_v1.types.CdnKey`):
                Required. The CDN key resource to
                create.

                This corresponds to the ``cdn_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cdn_key_id (:class:`str`):
                Required. The ID to use for the CDN
                key, which will become the final
                component of the CDN key's resource
                name.
                This value should conform to RFC-1034,
                which restricts to lower-case letters,
                numbers, and hyphen, with the first
                character a letter, the last a letter or
                a number, and a 63 character maximum.

                This corresponds to the ``cdn_key_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.CdnKey:
                Configuration for a CDN key. Used by
                the Video Stitcher to sign URIs for
                fetching video manifests and signing
                media segments for playback.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, cdn_key, cdn_key_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_stitcher_service.CreateCdnKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if cdn_key is not None:
            request.cdn_key = cdn_key
        if cdn_key_id is not None:
            request.cdn_key_id = cdn_key_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_cdn_key,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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

    async def list_cdn_keys(
        self,
        request: Optional[
            Union[video_stitcher_service.ListCdnKeysRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCdnKeysAsyncPager:
        r"""Lists all CDN keys in the specified project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_list_cdn_keys():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.ListCdnKeysRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_cdn_keys(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.ListCdnKeysRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.listCdnKeys.
            parent (:class:`str`):
                Required. The project that contains the list of CDN
                keys, in the form of
                ``projects/{project_number}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.services.video_stitcher_service.pagers.ListCdnKeysAsyncPager:
                Response message for
                VideoStitcher.ListCdnKeys.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_stitcher_service.ListCdnKeysRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_cdn_keys,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListCdnKeysAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_cdn_key(
        self,
        request: Optional[Union[video_stitcher_service.GetCdnKeyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cdn_keys.CdnKey:
        r"""Returns the specified CDN key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_get_cdn_key():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetCdnKeyRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_cdn_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.GetCdnKeyRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.getCdnKey.
            name (:class:`str`):
                Required. The name of the CDN key to be retrieved, in
                the form of
                ``projects/{project}/locations/{location}/cdnKeys/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.CdnKey:
                Configuration for a CDN key. Used by
                the Video Stitcher to sign URIs for
                fetching video manifests and signing
                media segments for playback.

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

        request = video_stitcher_service.GetCdnKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_cdn_key,
            default_timeout=60.0,
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

    async def delete_cdn_key(
        self,
        request: Optional[
            Union[video_stitcher_service.DeleteCdnKeyRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified CDN key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_delete_cdn_key():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.DeleteCdnKeyRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_cdn_key(request=request)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.DeleteCdnKeyRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.deleteCdnKey.
            name (:class:`str`):
                Required. The name of the CDN key to be deleted, in the
                form of
                ``projects/{project_number}/locations/{location}/cdnKeys/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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

        request = video_stitcher_service.DeleteCdnKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_cdn_key,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def update_cdn_key(
        self,
        request: Optional[
            Union[video_stitcher_service.UpdateCdnKeyRequest, dict]
        ] = None,
        *,
        cdn_key: Optional[cdn_keys.CdnKey] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cdn_keys.CdnKey:
        r"""Updates the specified CDN key. Only update fields
        specified in the call method body.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_update_cdn_key():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.UpdateCdnKeyRequest(
                )

                # Make the request
                response = await client.update_cdn_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.UpdateCdnKeyRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.updateCdnKey.
            cdn_key (:class:`google.cloud.video.stitcher_v1.types.CdnKey`):
                Required. The CDN key resource which
                replaces the resource on the server.

                This corresponds to the ``cdn_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.CdnKey:
                Configuration for a CDN key. Used by
                the Video Stitcher to sign URIs for
                fetching video manifests and signing
                media segments for playback.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([cdn_key, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_stitcher_service.UpdateCdnKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if cdn_key is not None:
            request.cdn_key = cdn_key
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_cdn_key,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("cdn_key.name", request.cdn_key.name),)
            ),
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

    async def create_vod_session(
        self,
        request: Optional[
            Union[video_stitcher_service.CreateVodSessionRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        vod_session: Optional[sessions.VodSession] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> sessions.VodSession:
        r"""Creates a client side playback VOD session and
        returns the full tracking and playback metadata of the
        session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_create_vod_session():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                vod_session = stitcher_v1.VodSession()
                vod_session.source_uri = "source_uri_value"
                vod_session.ad_tag_uri = "ad_tag_uri_value"

                request = stitcher_v1.CreateVodSessionRequest(
                    parent="parent_value",
                    vod_session=vod_session,
                )

                # Make the request
                response = await client.create_vod_session(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.CreateVodSessionRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.createVodSession
            parent (:class:`str`):
                Required. The project and location in which the VOD
                session should be created, in the form of
                ``projects/{project_number}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            vod_session (:class:`google.cloud.video.stitcher_v1.types.VodSession`):
                Required. Parameters for creating a
                session.

                This corresponds to the ``vod_session`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.VodSession:
                Metadata for a VOD session.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, vod_session])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_stitcher_service.CreateVodSessionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if vod_session is not None:
            request.vod_session = vod_session

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_vod_session,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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

    async def get_vod_session(
        self,
        request: Optional[
            Union[video_stitcher_service.GetVodSessionRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> sessions.VodSession:
        r"""Returns the full tracking, playback metadata, and
        relevant ad-ops logs for the specified VOD session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_get_vod_session():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetVodSessionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_vod_session(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.GetVodSessionRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.getVodSession
            name (:class:`str`):
                Required. The name of the VOD session to be retrieved,
                in the form of
                ``projects/{project_number}/locations/{location}/vodSessions/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.VodSession:
                Metadata for a VOD session.
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

        request = video_stitcher_service.GetVodSessionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_vod_session,
            default_timeout=60.0,
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

    async def list_vod_stitch_details(
        self,
        request: Optional[
            Union[video_stitcher_service.ListVodStitchDetailsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVodStitchDetailsAsyncPager:
        r"""Returns a list of detailed stitching information of
        the specified VOD session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_list_vod_stitch_details():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.ListVodStitchDetailsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_vod_stitch_details(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.ListVodStitchDetailsRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.listVodStitchDetails.
            parent (:class:`str`):
                Required. The VOD session where the stitch details
                belong to, in the form of
                ``projects/{project}/locations/{location}/vodSessions/{id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.services.video_stitcher_service.pagers.ListVodStitchDetailsAsyncPager:
                Response message for
                VideoStitcherService.listVodStitchDetails.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_stitcher_service.ListVodStitchDetailsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_vod_stitch_details,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListVodStitchDetailsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_vod_stitch_detail(
        self,
        request: Optional[
            Union[video_stitcher_service.GetVodStitchDetailRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> stitch_details.VodStitchDetail:
        r"""Returns the specified stitching information for the
        specified VOD session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_get_vod_stitch_detail():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetVodStitchDetailRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_vod_stitch_detail(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.GetVodStitchDetailRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.getVodStitchDetail.
            name (:class:`str`):
                Required. The name of the stitch detail in the specified
                VOD session, in the form of
                ``projects/{project}/locations/{location}/vodSessions/{vod_session_id}/vodStitchDetails/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.VodStitchDetail:
                Detailed information related to the
                interstitial of a VOD session.

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

        request = video_stitcher_service.GetVodStitchDetailRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_vod_stitch_detail,
            default_timeout=60.0,
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

    async def list_vod_ad_tag_details(
        self,
        request: Optional[
            Union[video_stitcher_service.ListVodAdTagDetailsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVodAdTagDetailsAsyncPager:
        r"""Return the list of ad tag details for the specified
        VOD session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_list_vod_ad_tag_details():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.ListVodAdTagDetailsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_vod_ad_tag_details(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.ListVodAdTagDetailsRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.listVodAdTagDetails.
            parent (:class:`str`):
                Required. The VOD session which the ad tag details
                belong to, in the form of
                ``projects/{project}/locations/{location}/vodSessions/{vod_session_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.services.video_stitcher_service.pagers.ListVodAdTagDetailsAsyncPager:
                Response message for
                VideoStitcherService.listVodAdTagDetails.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_stitcher_service.ListVodAdTagDetailsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_vod_ad_tag_details,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListVodAdTagDetailsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_vod_ad_tag_detail(
        self,
        request: Optional[
            Union[video_stitcher_service.GetVodAdTagDetailRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ad_tag_details.VodAdTagDetail:
        r"""Returns the specified ad tag detail for the specified
        VOD session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_get_vod_ad_tag_detail():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetVodAdTagDetailRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_vod_ad_tag_detail(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.GetVodAdTagDetailRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.getVodAdTagDetail
            name (:class:`str`):
                Required. The name of the ad tag detail for the
                specified VOD session, in the form of
                ``projects/{project}/locations/{location}/vodSessions/{vod_session_id}/vodAdTagDetails/{vod_ad_tag_detail}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.VodAdTagDetail:
                Information related to the details
                for one ad tag.

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

        request = video_stitcher_service.GetVodAdTagDetailRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_vod_ad_tag_detail,
            default_timeout=60.0,
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

    async def list_live_ad_tag_details(
        self,
        request: Optional[
            Union[video_stitcher_service.ListLiveAdTagDetailsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListLiveAdTagDetailsAsyncPager:
        r"""Return the list of ad tag details for the specified
        live session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_list_live_ad_tag_details():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.ListLiveAdTagDetailsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_live_ad_tag_details(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.ListLiveAdTagDetailsRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.listLiveAdTagDetails.
            parent (:class:`str`):
                Required. The resource parent in the form of
                ``projects/{project}/locations/{location}/liveSessions/{live_session}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.services.video_stitcher_service.pagers.ListLiveAdTagDetailsAsyncPager:
                Response message for
                VideoStitcherService.listLiveAdTagDetails.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_stitcher_service.ListLiveAdTagDetailsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_live_ad_tag_details,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListLiveAdTagDetailsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_live_ad_tag_detail(
        self,
        request: Optional[
            Union[video_stitcher_service.GetLiveAdTagDetailRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ad_tag_details.LiveAdTagDetail:
        r"""Returns the specified ad tag detail for the specified
        live session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_get_live_ad_tag_detail():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetLiveAdTagDetailRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_live_ad_tag_detail(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.GetLiveAdTagDetailRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.getLiveAdTagDetail
            name (:class:`str`):
                Required. The resource name in the form of
                ``projects/{project}/locations/{location}/liveSessions/{live_session}/liveAdTagDetails/{live_ad_tag_detail}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.LiveAdTagDetail:
                Container for a live session's ad tag
                detail.

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

        request = video_stitcher_service.GetLiveAdTagDetailRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_live_ad_tag_detail,
            default_timeout=60.0,
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

    async def create_slate(
        self,
        request: Optional[
            Union[video_stitcher_service.CreateSlateRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        slate: Optional[slates.Slate] = None,
        slate_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> slates.Slate:
        r"""Creates a slate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_create_slate():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.CreateSlateRequest(
                    parent="parent_value",
                    slate_id="slate_id_value",
                )

                # Make the request
                response = await client.create_slate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.CreateSlateRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.createSlate.
            parent (:class:`str`):
                Required. The project in which the slate should be
                created, in the form of ``projects/{project_number}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            slate (:class:`google.cloud.video.stitcher_v1.types.Slate`):
                Required. The slate to create.
                This corresponds to the ``slate`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            slate_id (:class:`str`):
                Required. The unique identifier for
                the slate. This value should conform to
                RFC-1034, which restricts to lower-case
                letters, numbers, and hyphen, with the
                first character a letter, the last a
                letter or a number, and a 63 character
                maximum.

                This corresponds to the ``slate_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.Slate:
                Slate object
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, slate, slate_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_stitcher_service.CreateSlateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if slate is not None:
            request.slate = slate
        if slate_id is not None:
            request.slate_id = slate_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_slate,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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

    async def list_slates(
        self,
        request: Optional[Union[video_stitcher_service.ListSlatesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSlatesAsyncPager:
        r"""Lists all slates in the specified project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_list_slates():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.ListSlatesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_slates(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.ListSlatesRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.listSlates.
            parent (:class:`str`):
                Required. The project to list slates, in the form of
                ``projects/{project_number}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.services.video_stitcher_service.pagers.ListSlatesAsyncPager:
                Response message for
                VideoStitcherService.listSlates.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_stitcher_service.ListSlatesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_slates,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListSlatesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_slate(
        self,
        request: Optional[Union[video_stitcher_service.GetSlateRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> slates.Slate:
        r"""Returns the specified slate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_get_slate():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetSlateRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_slate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.GetSlateRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.getSlate.
            name (:class:`str`):
                Required. The name of the slate to be retrieved, of the
                slate, in the form of
                ``projects/{project_number}/locations/{location}/slates/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.Slate:
                Slate object
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

        request = video_stitcher_service.GetSlateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_slate,
            default_timeout=60.0,
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

    async def update_slate(
        self,
        request: Optional[
            Union[video_stitcher_service.UpdateSlateRequest, dict]
        ] = None,
        *,
        slate: Optional[slates.Slate] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> slates.Slate:
        r"""Updates the specified slate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_update_slate():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.UpdateSlateRequest(
                )

                # Make the request
                response = await client.update_slate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.UpdateSlateRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.updateSlate.
            slate (:class:`google.cloud.video.stitcher_v1.types.Slate`):
                Required. The resource with updated
                fields.

                This corresponds to the ``slate`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The update mask which
                specifies fields which should be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.Slate:
                Slate object
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([slate, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_stitcher_service.UpdateSlateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if slate is not None:
            request.slate = slate
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_slate,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("slate.name", request.slate.name),)
            ),
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

    async def delete_slate(
        self,
        request: Optional[
            Union[video_stitcher_service.DeleteSlateRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified slate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_delete_slate():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.DeleteSlateRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_slate(request=request)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.DeleteSlateRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.deleteSlate.
            name (:class:`str`):
                Required. The name of the slate to be deleted, in the
                form of
                ``projects/{project_number}/locations/{location}/slates/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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

        request = video_stitcher_service.DeleteSlateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_slate,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def create_live_session(
        self,
        request: Optional[
            Union[video_stitcher_service.CreateLiveSessionRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        live_session: Optional[sessions.LiveSession] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> sessions.LiveSession:
        r"""Creates a new live session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_create_live_session():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.CreateLiveSessionRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_live_session(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.CreateLiveSessionRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.createLiveSession.
            parent (:class:`str`):
                Required. The project and location in which the live
                session should be created, in the form of
                ``projects/{project_number}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            live_session (:class:`google.cloud.video.stitcher_v1.types.LiveSession`):
                Required. Parameters for creating a
                live session.

                This corresponds to the ``live_session`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.LiveSession:
                Metadata for a live session.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, live_session])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = video_stitcher_service.CreateLiveSessionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if live_session is not None:
            request.live_session = live_session

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_live_session,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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

    async def get_live_session(
        self,
        request: Optional[
            Union[video_stitcher_service.GetLiveSessionRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> sessions.LiveSession:
        r"""Returns the details for the specified live session.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.video import stitcher_v1

            async def sample_get_live_session():
                # Create a client
                client = stitcher_v1.VideoStitcherServiceAsyncClient()

                # Initialize request argument(s)
                request = stitcher_v1.GetLiveSessionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_live_session(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.video.stitcher_v1.types.GetLiveSessionRequest, dict]]):
                The request object. Request message for
                VideoStitcherService.getSession.
            name (:class:`str`):
                Required. The name of the live session, in the form of
                ``projects/{project_number}/locations/{location}/liveSessions/{id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.stitcher_v1.types.LiveSession:
                Metadata for a live session.
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

        request = video_stitcher_service.GetLiveSessionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_live_session,
            default_timeout=60.0,
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("VideoStitcherServiceAsyncClient",)
