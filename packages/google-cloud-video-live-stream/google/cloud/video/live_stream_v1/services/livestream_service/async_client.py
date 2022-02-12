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
from collections import OrderedDict
import functools
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.video.live_stream_v1.services.livestream_service import pagers
from google.cloud.video.live_stream_v1.types import outputs
from google.cloud.video.live_stream_v1.types import resources
from google.cloud.video.live_stream_v1.types import service
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import LivestreamServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import LivestreamServiceGrpcAsyncIOTransport
from .client import LivestreamServiceClient


class LivestreamServiceAsyncClient:
    """Using Live Stream API, you can generate live streams in the
    various renditions and streaming formats. The streaming format
    include HTTP Live Streaming (HLS) and Dynamic Adaptive Streaming
    over HTTP (DASH). You can send a source stream in the various
    ways, including Real-Time Messaging Protocol (RTMP) and Secure
    Reliable Transport (SRT).
    """

    _client: LivestreamServiceClient

    DEFAULT_ENDPOINT = LivestreamServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = LivestreamServiceClient.DEFAULT_MTLS_ENDPOINT

    channel_path = staticmethod(LivestreamServiceClient.channel_path)
    parse_channel_path = staticmethod(LivestreamServiceClient.parse_channel_path)
    event_path = staticmethod(LivestreamServiceClient.event_path)
    parse_event_path = staticmethod(LivestreamServiceClient.parse_event_path)
    input_path = staticmethod(LivestreamServiceClient.input_path)
    parse_input_path = staticmethod(LivestreamServiceClient.parse_input_path)
    common_billing_account_path = staticmethod(
        LivestreamServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        LivestreamServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(LivestreamServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        LivestreamServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        LivestreamServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        LivestreamServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(LivestreamServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        LivestreamServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(LivestreamServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        LivestreamServiceClient.parse_common_location_path
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
            LivestreamServiceAsyncClient: The constructed client.
        """
        return LivestreamServiceClient.from_service_account_info.__func__(LivestreamServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            LivestreamServiceAsyncClient: The constructed client.
        """
        return LivestreamServiceClient.from_service_account_file.__func__(LivestreamServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return LivestreamServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> LivestreamServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            LivestreamServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(LivestreamServiceClient).get_transport_class, type(LivestreamServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, LivestreamServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the livestream service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.LivestreamServiceTransport]): The
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
        self._client = LivestreamServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_channel(
        self,
        request: Union[service.CreateChannelRequest, dict] = None,
        *,
        parent: str = None,
        channel: resources.Channel = None,
        channel_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a channel with the provided unique ID in the
        specified region.


        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_create_channel():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.CreateChannelRequest(
                    parent="parent_value",
                    channel_id="channel_id_value",
                )

                # Make the request
                operation = client.create_channel(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.CreateChannelRequest, dict]):
                The request object. Request message for
                "LivestreamService.CreateChannel".
            parent (:class:`str`):
                Required. The parent location for the resource, in the
                form of: ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            channel (:class:`google.cloud.video.live_stream_v1.types.Channel`):
                Required. The channel resource to be
                created.

                This corresponds to the ``channel`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            channel_id (:class:`str`):
                Required. The ID of the channel resource to be created.
                This value must be 1-63 characters, begin and end with
                ``[a-z0-9]``, could contain dashes (-) in between.

                This corresponds to the ``channel_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.video.live_stream_v1.types.Channel` Channel resource represents the processor that does a user-defined
                   "streaming" operation, which includes getting an
                   input stream through an input, transcoding it to
                   multiple renditions, and publishing output live
                   streams in certain formats (for example, HLS or DASH)
                   to the specified location.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, channel, channel_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.CreateChannelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if channel is not None:
            request.channel = channel
        if channel_id is not None:
            request.channel_id = channel_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_channel_,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            resources.Channel,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_channels(
        self,
        request: Union[service.ListChannelsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListChannelsAsyncPager:
        r"""Returns a list of all channels in the specified
        region.


        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_list_channels():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.ListChannelsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_channels(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.ListChannelsRequest, dict]):
                The request object. Request message for
                "LivestreamService.ListChannels".
            parent (:class:`str`):
                Required. The parent location for the resource, in the
                form of: ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.live_stream_v1.services.livestream_service.pagers.ListChannelsAsyncPager:
                Response message for
                "LivestreamService.ListChannels".
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

        request = service.ListChannelsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_channels,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListChannelsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_channel(
        self,
        request: Union[service.GetChannelRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Channel:
        r"""Returns the specified channel.

        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_get_channel():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.GetChannelRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_channel(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.GetChannelRequest, dict]):
                The request object. Request message for
                "LivestreamService.GetChannel".
            name (:class:`str`):
                Required. The name of the channel resource, in the form
                of:
                ``projects/{project}/locations/{location}/channels/{channelId}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.live_stream_v1.types.Channel:
                Channel resource represents the
                processor that does a user-defined
                "streaming" operation, which includes
                getting an input stream through an
                input, transcoding it to multiple
                renditions, and publishing output live
                streams in certain formats (for example,
                HLS or DASH) to the specified location.

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

        request = service.GetChannelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_channel,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_channel(
        self,
        request: Union[service.DeleteChannelRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes the specified channel.

        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_delete_channel():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.DeleteChannelRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_channel(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.DeleteChannelRequest, dict]):
                The request object. Request message for
                "LivestreamService.DeleteChannel".
            name (:class:`str`):
                Required. The name of the channel resource, in the form
                of:
                ``projects/{project}/locations/{location}/channels/{channelId}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

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

        request = service.DeleteChannelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_channel,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_channel(
        self,
        request: Union[service.UpdateChannelRequest, dict] = None,
        *,
        channel: resources.Channel = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the specified channel.

        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_update_channel():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.UpdateChannelRequest(
                )

                # Make the request
                operation = client.update_channel(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.UpdateChannelRequest, dict]):
                The request object. Request message for
                "LivestreamService.UpdateChannel".
            channel (:class:`google.cloud.video.live_stream_v1.types.Channel`):
                Required. The channel resource to be
                updated.

                This corresponds to the ``channel`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Field mask is used to specify the fields to be
                overwritten in the Channel resource by the update. You
                can only update the following fields:

                -  ```inputAttachments`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#inputattachment>`__
                -  ```output`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#output>`__
                -  ```elementaryStreams`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#ElementaryStream>`__
                -  ```muxStreams`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#muxstream>`__
                -  ```manifests`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#Manifest>`__
                -  ```spritesheets`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#spritesheet>`__

                The fields specified in the update_mask are relative to
                the resource, not the full request. A field will be
                overwritten if it is in the mask.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.video.live_stream_v1.types.Channel` Channel resource represents the processor that does a user-defined
                   "streaming" operation, which includes getting an
                   input stream through an input, transcoding it to
                   multiple renditions, and publishing output live
                   streams in certain formats (for example, HLS or DASH)
                   to the specified location.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([channel, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.UpdateChannelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if channel is not None:
            request.channel = channel
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_channel,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("channel.name", request.channel.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            resources.Channel,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def start_channel(
        self,
        request: Union[service.StartChannelRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Starts the specified channel. Part of the video
        pipeline will be created only when the StartChannel
        request is received by the server.


        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_start_channel():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.StartChannelRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.start_channel(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.StartChannelRequest, dict]):
                The request object. Request message for
                "LivestreamService.StartChannel".
            name (:class:`str`):
                Required. The name of the channel resource, in the form
                of:
                ``projects/{project}/locations/{location}/channels/{channelId}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.video.live_stream_v1.types.ChannelOperationResponse`
                Response message for Start/Stop Channel long-running
                operations.

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

        request = service.StartChannelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.start_channel,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            service.ChannelOperationResponse,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def stop_channel(
        self,
        request: Union[service.StopChannelRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Stops the specified channel. Part of the video
        pipeline will be released when the StopChannel request
        is received by the server.


        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_stop_channel():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.StopChannelRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.stop_channel(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.StopChannelRequest, dict]):
                The request object. Request message for
                "LivestreamService.StopChannel".
            name (:class:`str`):
                Required. The name of the channel resource, in the form
                of:
                ``projects/{project}/locations/{location}/channels/{channelId}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.video.live_stream_v1.types.ChannelOperationResponse`
                Response message for Start/Stop Channel long-running
                operations.

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

        request = service.StopChannelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.stop_channel,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            service.ChannelOperationResponse,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def create_input(
        self,
        request: Union[service.CreateInputRequest, dict] = None,
        *,
        parent: str = None,
        input: resources.Input = None,
        input_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates an input with the provided unique ID in the
        specified region.


        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_create_input():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.CreateInputRequest(
                    parent="parent_value",
                    input_id="input_id_value",
                )

                # Make the request
                operation = client.create_input(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.CreateInputRequest, dict]):
                The request object. Request message for
                "LivestreamService.CreateInput".
            parent (:class:`str`):
                Required. The parent location for the resource, in the
                form of: ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            input (:class:`google.cloud.video.live_stream_v1.types.Input`):
                Required. The input resource to be
                created.

                This corresponds to the ``input`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            input_id (:class:`str`):
                Required. The ID of the input resource to be created.
                This value must be 1-63 characters, begin and end with
                ``[a-z0-9]``, could contain dashes (-) in between.

                This corresponds to the ``input_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.video.live_stream_v1.types.Input` Input resource represents the endpoint from which the channel ingests
                   the input stream.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, input, input_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.CreateInputRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if input is not None:
            request.input = input
        if input_id is not None:
            request.input_id = input_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_input,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            resources.Input,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_inputs(
        self,
        request: Union[service.ListInputsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInputsAsyncPager:
        r"""Returns a list of all inputs in the specified region.

        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_list_inputs():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.ListInputsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_inputs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.ListInputsRequest, dict]):
                The request object. Request message for
                "LivestreamService.ListInputs".
            parent (:class:`str`):
                Required. The parent location for the resource, in the
                form of: ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.live_stream_v1.services.livestream_service.pagers.ListInputsAsyncPager:
                Response message for
                "LivestreamService.ListInputs".
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

        request = service.ListInputsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_inputs,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListInputsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_input(
        self,
        request: Union[service.GetInputRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Input:
        r"""Returns the specified input.

        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_get_input():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.GetInputRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_input(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.GetInputRequest, dict]):
                The request object. Request message for
                "LivestreamService.GetInput".
            name (:class:`str`):
                Required. The name of the input resource, in the form
                of:
                ``projects/{project}/locations/{location}/inputs/{inputId}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.live_stream_v1.types.Input:
                Input resource represents the
                endpoint from which the channel ingests
                the input stream.

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

        request = service.GetInputRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_input,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_input(
        self,
        request: Union[service.DeleteInputRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes the specified input.

        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_delete_input():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.DeleteInputRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_input(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.DeleteInputRequest, dict]):
                The request object. Request message for
                "LivestreamService.DeleteInput".
            name (:class:`str`):
                Required. The name of the input resource, in the form
                of:
                ``projects/{project}/locations/{location}/inputs/{inputId}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

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

        request = service.DeleteInputRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_input,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_input(
        self,
        request: Union[service.UpdateInputRequest, dict] = None,
        *,
        input: resources.Input = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the specified input.

        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_update_input():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.UpdateInputRequest(
                )

                # Make the request
                operation = client.update_input(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.UpdateInputRequest, dict]):
                The request object. Request message for
                "LivestreamService.UpdateInput".
            input (:class:`google.cloud.video.live_stream_v1.types.Input`):
                Required. The input resource to be
                updated.

                This corresponds to the ``input`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Field mask is used to specify the fields to be
                overwritten in the Input resource by the update. You can
                only update the following fields:

                -  ```preprocessingConfig`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.inputs#PreprocessingConfig>`__
                -  ```securityRules`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.inputs#SecurityRule>`__

                The fields specified in the update_mask are relative to
                the resource, not the full request. A field will be
                overwritten if it is in the mask.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.video.live_stream_v1.types.Input` Input resource represents the endpoint from which the channel ingests
                   the input stream.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([input, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.UpdateInputRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if input is not None:
            request.input = input
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_input,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("input.name", request.input.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            resources.Input,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def create_event(
        self,
        request: Union[service.CreateEventRequest, dict] = None,
        *,
        parent: str = None,
        event: resources.Event = None,
        event_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Event:
        r"""Creates an event with the provided unique ID in the
        specified channel.


        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_create_event():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.CreateEventRequest(
                    parent="parent_value",
                    event_id="event_id_value",
                )

                # Make the request
                response = client.create_event(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.CreateEventRequest, dict]):
                The request object. Request message for
                "LivestreamService.CreateEvent".
            parent (:class:`str`):
                Required. The parent channel for the resource, in the
                form of:
                ``projects/{project}/locations/{location}/channels/{channelId}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            event (:class:`google.cloud.video.live_stream_v1.types.Event`):
                Required. The event resource to be
                created.

                This corresponds to the ``event`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            event_id (:class:`str`):
                Required. The ID of the event resource to be created.
                This value must be 1-63 characters, begin and end with
                ``[a-z0-9]``, could contain dashes (-) in between.

                This corresponds to the ``event_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.live_stream_v1.types.Event:
                Event is a sub-resource of a channel,
                which can be scheduled by the user to
                execute operations on a channel resource
                without having to stop the channel.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, event, event_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.CreateEventRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if event is not None:
            request.event = event
        if event_id is not None:
            request.event_id = event_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_event,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_events(
        self,
        request: Union[service.ListEventsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEventsAsyncPager:
        r"""Returns a list of all events in the specified
        channel.


        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_list_events():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.ListEventsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_events(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.ListEventsRequest, dict]):
                The request object. Request message for
                "LivestreamService.ListEvents".
            parent (:class:`str`):
                Required. The parent channel for the resource, in the
                form of:
                ``projects/{project}/locations/{location}/channels/{channelId}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.live_stream_v1.services.livestream_service.pagers.ListEventsAsyncPager:
                Response message for
                "LivestreamService.ListEvents".
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

        request = service.ListEventsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_events,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListEventsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_event(
        self,
        request: Union[service.GetEventRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Event:
        r"""Returns the specified event.

        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_get_event():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.GetEventRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_event(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.GetEventRequest, dict]):
                The request object. Request message for
                "LivestreamService.GetEvent".
            name (:class:`str`):
                Required. The name of the event resource, in the form
                of:
                ``projects/{project}/locations/{location}/channels/{channelId}/events/{eventId}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.live_stream_v1.types.Event:
                Event is a sub-resource of a channel,
                which can be scheduled by the user to
                execute operations on a channel resource
                without having to stop the channel.

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

        request = service.GetEventRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_event,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_event(
        self,
        request: Union[service.DeleteEventRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified event.

        .. code-block::

            from google.cloud.video import live_stream_v1

            def sample_delete_event():
                # Create a client
                client = live_stream_v1.LivestreamServiceClient()

                # Initialize request argument(s)
                request = live_stream_v1.DeleteEventRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_event(request=request)

        Args:
            request (Union[google.cloud.video.live_stream_v1.types.DeleteEventRequest, dict]):
                The request object. Request message for
                "LivestreamService.DeleteEvent".
            name (:class:`str`):
                Required. The name of the event resource, in the form
                of:
                ``projects/{project}/locations/{location}/channels/{channelId}/events/{eventId}``.

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

        request = service.DeleteEventRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_event,
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
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-video-live-stream",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("LivestreamServiceAsyncClient",)
