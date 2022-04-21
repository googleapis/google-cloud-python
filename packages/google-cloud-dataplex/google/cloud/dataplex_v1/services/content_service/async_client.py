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
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore
import pkg_resources

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.dataplex_v1.services.content_service import pagers
from google.cloud.dataplex_v1.types import analyze
from google.cloud.dataplex_v1.types import content
from google.cloud.dataplex_v1.types import content as gcd_content

from .client import ContentServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, ContentServiceTransport
from .transports.grpc_asyncio import ContentServiceGrpcAsyncIOTransport


class ContentServiceAsyncClient:
    """ContentService manages Notebook and SQL Scripts for Dataplex."""

    _client: ContentServiceClient

    DEFAULT_ENDPOINT = ContentServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ContentServiceClient.DEFAULT_MTLS_ENDPOINT

    content_path = staticmethod(ContentServiceClient.content_path)
    parse_content_path = staticmethod(ContentServiceClient.parse_content_path)
    lake_path = staticmethod(ContentServiceClient.lake_path)
    parse_lake_path = staticmethod(ContentServiceClient.parse_lake_path)
    common_billing_account_path = staticmethod(
        ContentServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ContentServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ContentServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ContentServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ContentServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ContentServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ContentServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        ContentServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(ContentServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        ContentServiceClient.parse_common_location_path
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
            ContentServiceAsyncClient: The constructed client.
        """
        return ContentServiceClient.from_service_account_info.__func__(ContentServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ContentServiceAsyncClient: The constructed client.
        """
        return ContentServiceClient.from_service_account_file.__func__(ContentServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return ContentServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> ContentServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ContentServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ContentServiceClient).get_transport_class, type(ContentServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ContentServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the content service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ContentServiceTransport]): The
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
        self._client = ContentServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_content(
        self,
        request: Union[gcd_content.CreateContentRequest, dict] = None,
        *,
        parent: str = None,
        content: analyze.Content = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analyze.Content:
        r"""Create a content.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_create_content():
                # Create a client
                client = dataplex_v1.ContentServiceClient()

                # Initialize request argument(s)
                content = dataplex_v1.Content()
                content.data_text = "data_text_value"
                content.sql_script.engine = "SPARK"
                content.path = "path_value"

                request = dataplex_v1.CreateContentRequest(
                    parent="parent_value",
                    content=content,
                )

                # Make the request
                response = client.create_content(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataplex_v1.types.CreateContentRequest, dict]):
                The request object. Create content request.
            parent (:class:`str`):
                Required. The resource name of the parent lake:
                projects/{project_id}/locations/{location_id}/lakes/{lake_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            content (:class:`google.cloud.dataplex_v1.types.Content`):
                Required. Content resource.
                This corresponds to the ``content`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataplex_v1.types.Content:
                Content represents a user-visible
                notebook or a sql script

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, content])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_content.CreateContentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if content is not None:
            request.content = content

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_content,
            default_timeout=None,
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

    async def update_content(
        self,
        request: Union[gcd_content.UpdateContentRequest, dict] = None,
        *,
        content: analyze.Content = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analyze.Content:
        r"""Update a content. Only supports full resource update.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_update_content():
                # Create a client
                client = dataplex_v1.ContentServiceClient()

                # Initialize request argument(s)
                content = dataplex_v1.Content()
                content.data_text = "data_text_value"
                content.sql_script.engine = "SPARK"
                content.path = "path_value"

                request = dataplex_v1.UpdateContentRequest(
                    content=content,
                )

                # Make the request
                response = client.update_content(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataplex_v1.types.UpdateContentRequest, dict]):
                The request object. Update content request.
            content (:class:`google.cloud.dataplex_v1.types.Content`):
                Required. Update description. Only fields specified in
                ``update_mask`` are updated.

                This corresponds to the ``content`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Mask of fields to update.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataplex_v1.types.Content:
                Content represents a user-visible
                notebook or a sql script

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([content, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_content.UpdateContentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if content is not None:
            request.content = content
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_content,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("content.name", request.content.name),)
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

    async def delete_content(
        self,
        request: Union[content.DeleteContentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Delete a content.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_delete_content():
                # Create a client
                client = dataplex_v1.ContentServiceClient()

                # Initialize request argument(s)
                request = dataplex_v1.DeleteContentRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_content(request=request)

        Args:
            request (Union[google.cloud.dataplex_v1.types.DeleteContentRequest, dict]):
                The request object. Delete content request.
            name (:class:`str`):
                Required. The resource name of the content:
                projects/{project_id}/locations/{location_id}/lakes/{lake_id}/content/{content_id}

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

        request = content.DeleteContentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_content,
            default_timeout=None,
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

    async def get_content(
        self,
        request: Union[content.GetContentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analyze.Content:
        r"""Get a content resource.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_get_content():
                # Create a client
                client = dataplex_v1.ContentServiceClient()

                # Initialize request argument(s)
                request = dataplex_v1.GetContentRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_content(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataplex_v1.types.GetContentRequest, dict]):
                The request object. Get content request.
            name (:class:`str`):
                Required. The resource name of the content:
                projects/{project_id}/locations/{location_id}/lakes/{lake_id}/content/{content_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataplex_v1.types.Content:
                Content represents a user-visible
                notebook or a sql script

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

        request = content.GetContentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_content,
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

    async def list_content(
        self,
        request: Union[content.ListContentRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListContentAsyncPager:
        r"""List content.

        .. code-block:: python

            from google.cloud import dataplex_v1

            def sample_list_content():
                # Create a client
                client = dataplex_v1.ContentServiceClient()

                # Initialize request argument(s)
                request = dataplex_v1.ListContentRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_content(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataplex_v1.types.ListContentRequest, dict]):
                The request object. List content request. Returns the
                BASIC Content view.
            parent (:class:`str`):
                Required. The resource name of the parent lake:
                projects/{project_id}/locations/{location_id}/lakes/{lake_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataplex_v1.services.content_service.pagers.ListContentAsyncPager:
                List content response.
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

        request = content.ListContentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_content,
            default_timeout=None,
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
        response = pagers.ListContentAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dataplex",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ContentServiceAsyncClient",)
