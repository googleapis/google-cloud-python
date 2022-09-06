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
import pkg_resources

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials   # type: ignore
from google.oauth2 import service_account              # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.asset_v1.services.asset_service import pagers
from google.cloud.asset_v1.types import asset_service
from google.cloud.asset_v1.types import assets
from google.type import expr_pb2  # type: ignore
from .transports.base import AssetServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import AssetServiceGrpcAsyncIOTransport
from .client import AssetServiceClient


class AssetServiceAsyncClient:
    """Asset service definition."""

    _client: AssetServiceClient

    DEFAULT_ENDPOINT = AssetServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AssetServiceClient.DEFAULT_MTLS_ENDPOINT

    asset_path = staticmethod(AssetServiceClient.asset_path)
    parse_asset_path = staticmethod(AssetServiceClient.parse_asset_path)
    feed_path = staticmethod(AssetServiceClient.feed_path)
    parse_feed_path = staticmethod(AssetServiceClient.parse_feed_path)
    common_billing_account_path = staticmethod(AssetServiceClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(AssetServiceClient.parse_common_billing_account_path)
    common_folder_path = staticmethod(AssetServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(AssetServiceClient.parse_common_folder_path)
    common_organization_path = staticmethod(AssetServiceClient.common_organization_path)
    parse_common_organization_path = staticmethod(AssetServiceClient.parse_common_organization_path)
    common_project_path = staticmethod(AssetServiceClient.common_project_path)
    parse_common_project_path = staticmethod(AssetServiceClient.parse_common_project_path)
    common_location_path = staticmethod(AssetServiceClient.common_location_path)
    parse_common_location_path = staticmethod(AssetServiceClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            AssetServiceAsyncClient: The constructed client.
        """
        return AssetServiceClient.from_service_account_info.__func__(AssetServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            AssetServiceAsyncClient: The constructed client.
        """
        return AssetServiceClient.from_service_account_file.__func__(AssetServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(cls, client_options: Optional[ClientOptions] = None):
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
        return AssetServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> AssetServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            AssetServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(type(AssetServiceClient).get_transport_class, type(AssetServiceClient))

    def __init__(self, *,
            credentials: ga_credentials.Credentials = None,
            transport: Union[str, AssetServiceTransport] = "grpc_asyncio",
            client_options: ClientOptions = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiates the asset service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AssetServiceTransport]): The
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
        self._client = AssetServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,

        )

    async def export_assets(self,
            request: Union[asset_service.ExportAssetsRequest, dict] = None,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Exports assets with time and resource types to a given Cloud
        Storage location/BigQuery table. For Cloud Storage location
        destinations, the output format is newline-delimited JSON. Each
        line represents a
        [google.cloud.asset.v1.Asset][google.cloud.asset.v1.Asset] in
        the JSON format; for BigQuery table destinations, the output
        table stores the fields in asset proto as columns. This API
        implements the
        [google.longrunning.Operation][google.longrunning.Operation] API
        , which allows you to keep track of the export. We recommend
        intervals of at least 2 seconds with exponential retry to poll
        the export operation result. For regular-size resource parent,
        the export operation usually finishes within 5 minutes.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_export_assets():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                output_config = asset_v1.OutputConfig()
                output_config.gcs_destination.uri = "uri_value"

                request = asset_v1.ExportAssetsRequest(
                    parent="parent_value",
                    output_config=output_config,
                )

                # Make the request
                operation = client.export_assets(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.asset_v1.types.ExportAssetsRequest, dict]):
                The request object. Export asset request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.asset_v1.types.ExportAssetsResponse` The export asset response. This message is returned by the
                   [google.longrunning.Operations.GetOperation][google.longrunning.Operations.GetOperation]
                   method in the returned
                   [google.longrunning.Operation.response][google.longrunning.Operation.response]
                   field.

        """
        # Create or coerce a protobuf request object.
        request = asset_service.ExportAssetsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.export_assets,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            asset_service.ExportAssetsResponse,
            metadata_type=asset_service.ExportAssetsRequest,
        )

        # Done; return the response.
        return response

    async def list_assets(self,
            request: Union[asset_service.ListAssetsRequest, dict] = None,
            *,
            parent: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListAssetsAsyncPager:
        r"""Lists assets with time and resource types and returns
        paged results in response.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_list_assets():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                request = asset_v1.ListAssetsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_assets(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.asset_v1.types.ListAssetsRequest, dict]):
                The request object. ListAssets request.
            parent (:class:`str`):
                Required. Name of the organization or project the assets
                belong to. Format: "organizations/[organization-number]"
                (such as "organizations/123"), "projects/[project-id]"
                (such as "projects/my-project-id"), or
                "projects/[project-number]" (such as "projects/12345").

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.asset_v1.services.asset_service.pagers.ListAssetsAsyncPager:
                ListAssets response.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = asset_service.ListAssetsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_assets,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
        response = pagers.ListAssetsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def batch_get_assets_history(self,
            request: Union[asset_service.BatchGetAssetsHistoryRequest, dict] = None,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> asset_service.BatchGetAssetsHistoryResponse:
        r"""Batch gets the update history of assets that overlap a time
        window. For IAM_POLICY content, this API outputs history when
        the asset and its attached IAM POLICY both exist. This can
        create gaps in the output history. Otherwise, this API outputs
        history with asset in both non-delete or deleted status. If a
        specified asset does not exist, this API returns an
        INVALID_ARGUMENT error.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_batch_get_assets_history():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                request = asset_v1.BatchGetAssetsHistoryRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.batch_get_assets_history(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.asset_v1.types.BatchGetAssetsHistoryRequest, dict]):
                The request object. Batch get assets history request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.asset_v1.types.BatchGetAssetsHistoryResponse:
                Batch get assets history response.
        """
        # Create or coerce a protobuf request object.
        request = asset_service.BatchGetAssetsHistoryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_get_assets_history,
            default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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

    async def create_feed(self,
            request: Union[asset_service.CreateFeedRequest, dict] = None,
            *,
            parent: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> asset_service.Feed:
        r"""Creates a feed in a parent
        project/folder/organization to listen to its asset
        updates.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_create_feed():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                feed = asset_v1.Feed()
                feed.name = "name_value"

                request = asset_v1.CreateFeedRequest(
                    parent="parent_value",
                    feed_id="feed_id_value",
                    feed=feed,
                )

                # Make the request
                response = await client.create_feed(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.asset_v1.types.CreateFeedRequest, dict]):
                The request object. Create asset feed request.
            parent (:class:`str`):
                Required. The name of the
                project/folder/organization where this
                feed should be created in. It can only
                be an organization number (such as
                "organizations/123"), a folder number
                (such as "folders/123"), a project ID
                (such as "projects/my-project-id")", or
                a project number (such as
                "projects/12345").

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.asset_v1.types.Feed:
                An asset feed used to export asset
                updates to a destinations. An asset feed
                filter controls what updates are
                exported. The asset feed must be created
                within a project, organization, or
                folder. Supported destinations are:
                Pub/Sub topics.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = asset_service.CreateFeedRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_feed,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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

    async def get_feed(self,
            request: Union[asset_service.GetFeedRequest, dict] = None,
            *,
            name: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> asset_service.Feed:
        r"""Gets details about an asset feed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_get_feed():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                request = asset_v1.GetFeedRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_feed(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.asset_v1.types.GetFeedRequest, dict]):
                The request object. Get asset feed request.
            name (:class:`str`):
                Required. The name of the Feed and it must be in the
                format of: projects/project_number/feeds/feed_id
                folders/folder_number/feeds/feed_id
                organizations/organization_number/feeds/feed_id

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.asset_v1.types.Feed:
                An asset feed used to export asset
                updates to a destinations. An asset feed
                filter controls what updates are
                exported. The asset feed must be created
                within a project, organization, or
                folder. Supported destinations are:
                Pub/Sub topics.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = asset_service.GetFeedRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_feed,
            default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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

    async def list_feeds(self,
            request: Union[asset_service.ListFeedsRequest, dict] = None,
            *,
            parent: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> asset_service.ListFeedsResponse:
        r"""Lists all asset feeds in a parent
        project/folder/organization.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_list_feeds():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                request = asset_v1.ListFeedsRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.list_feeds(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.asset_v1.types.ListFeedsRequest, dict]):
                The request object. List asset feeds request.
            parent (:class:`str`):
                Required. The parent
                project/folder/organization whose feeds
                are to be listed. It can only be using
                project/folder/organization number (such
                as "folders/12345")", or a project ID
                (such as "projects/my-project-id").

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.asset_v1.types.ListFeedsResponse:

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = asset_service.ListFeedsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_feeds,
            default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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

    async def update_feed(self,
            request: Union[asset_service.UpdateFeedRequest, dict] = None,
            *,
            feed: asset_service.Feed = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> asset_service.Feed:
        r"""Updates an asset feed configuration.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_update_feed():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                feed = asset_v1.Feed()
                feed.name = "name_value"

                request = asset_v1.UpdateFeedRequest(
                    feed=feed,
                )

                # Make the request
                response = await client.update_feed(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.asset_v1.types.UpdateFeedRequest, dict]):
                The request object. Update asset feed request.
            feed (:class:`google.cloud.asset_v1.types.Feed`):
                Required. The new values of feed details. It must match
                an existing feed and the field ``name`` must be in the
                format of: projects/project_number/feeds/feed_id or
                folders/folder_number/feeds/feed_id or
                organizations/organization_number/feeds/feed_id.

                This corresponds to the ``feed`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.asset_v1.types.Feed:
                An asset feed used to export asset
                updates to a destinations. An asset feed
                filter controls what updates are
                exported. The asset feed must be created
                within a project, organization, or
                folder. Supported destinations are:
                Pub/Sub topics.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([feed])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = asset_service.UpdateFeedRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if feed is not None:
            request.feed = feed

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_feed,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("feed.name", request.feed.name),
            )),
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

    async def delete_feed(self,
            request: Union[asset_service.DeleteFeedRequest, dict] = None,
            *,
            name: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Deletes an asset feed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_delete_feed():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                request = asset_v1.DeleteFeedRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_feed(request=request)

        Args:
            request (Union[google.cloud.asset_v1.types.DeleteFeedRequest, dict]):
                The request object.
            name (:class:`str`):
                Required. The name of the feed and it must be in the
                format of: projects/project_number/feeds/feed_id
                folders/folder_number/feeds/feed_id
                organizations/organization_number/feeds/feed_id

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
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = asset_service.DeleteFeedRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_feed,
            default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def search_all_resources(self,
            request: Union[asset_service.SearchAllResourcesRequest, dict] = None,
            *,
            scope: str = None,
            query: str = None,
            asset_types: Sequence[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.SearchAllResourcesAsyncPager:
        r"""Searches all Cloud resources within the specified scope, such as
        a project, folder, or organization. The caller must be granted
        the ``cloudasset.assets.searchAllResources`` permission on the
        desired scope, otherwise the request will be rejected.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_search_all_resources():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                request = asset_v1.SearchAllResourcesRequest(
                    scope="scope_value",
                )

                # Make the request
                page_result = client.search_all_resources(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.asset_v1.types.SearchAllResourcesRequest, dict]):
                The request object. Search all resources request.
            scope (:class:`str`):
                Required. A scope can be a project, a folder, or an
                organization. The search is limited to the resources
                within the ``scope``. The caller must be granted the
                ```cloudasset.assets.searchAllResources`` <https://cloud.google.com/asset-inventory/docs/access-control#required_permissions>`__
                permission on the desired scope.

                The allowed values are:

                -  projects/{PROJECT_ID} (e.g., "projects/foo-bar")
                -  projects/{PROJECT_NUMBER} (e.g., "projects/12345678")
                -  folders/{FOLDER_NUMBER} (e.g., "folders/1234567")
                -  organizations/{ORGANIZATION_NUMBER} (e.g.,
                   "organizations/123456")

                This corresponds to the ``scope`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (:class:`str`):
                Optional. The query statement. See `how to construct a
                query <https://cloud.google.com/asset-inventory/docs/searching-resources#how_to_construct_a_query>`__
                for more information. If not specified or empty, it will
                search all the resources within the specified ``scope``.

                Examples:

                -  ``name:Important`` to find Cloud resources whose name
                   contains "Important" as a word.
                -  ``name=Important`` to find the Cloud resource whose
                   name is exactly "Important".
                -  ``displayName:Impor*`` to find Cloud resources whose
                   display name contains "Impor" as a prefix of any word
                   in the field.
                -  ``location:us-west*`` to find Cloud resources whose
                   location contains both "us" and "west" as prefixes.
                -  ``labels:prod`` to find Cloud resources whose labels
                   contain "prod" as a key or value.
                -  ``labels.env:prod`` to find Cloud resources that have
                   a label "env" and its value is "prod".
                -  ``labels.env:*`` to find Cloud resources that have a
                   label "env".
                -  ``kmsKey:key`` to find Cloud resources encrypted with
                   a customer-managed encryption key whose name contains
                   the word "key".
                -  ``state:ACTIVE`` to find Cloud resources whose state
                   contains "ACTIVE" as a word.
                -  ``NOT state:ACTIVE`` to find {{gcp_name}} resources
                   whose state doesn't contain "ACTIVE" as a word.
                -  ``createTime<1609459200`` to find Cloud resources
                   that were created before "2021-01-01 00:00:00 UTC".
                   1609459200 is the epoch timestamp of "2021-01-01
                   00:00:00 UTC" in seconds.
                -  ``updateTime>1609459200`` to find Cloud resources
                   that were updated after "2021-01-01 00:00:00 UTC".
                   1609459200 is the epoch timestamp of "2021-01-01
                   00:00:00 UTC" in seconds.
                -  ``Important`` to find Cloud resources that contain
                   "Important" as a word in any of the searchable
                   fields.
                -  ``Impor*`` to find Cloud resources that contain
                   "Impor" as a prefix of any word in any of the
                   searchable fields.
                -  ``Important location:(us-west1 OR global)`` to find
                   Cloud resources that contain "Important" as a word in
                   any of the searchable fields and are also located in
                   the "us-west1" region or the "global" location.

                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            asset_types (:class:`Sequence[str]`):
                Optional. A list of asset types that this request
                searches for. If empty, it will search all the
                `searchable asset
                types <https://cloud.google.com/asset-inventory/docs/supported-asset-types#searchable_asset_types>`__.

                Regular expressions are also supported. For example:

                -  "compute.googleapis.com.*" snapshots resources whose
                   asset type starts with "compute.googleapis.com".
                -  ".*Instance" snapshots resources whose asset type
                   ends with "Instance".
                -  ".*Instance.*" snapshots resources whose asset type
                   contains "Instance".

                See `RE2 <https://github.com/google/re2/wiki/Syntax>`__
                for all supported regular expression syntax. If the
                regular expression does not match any supported asset
                type, an INVALID_ARGUMENT error will be returned.

                This corresponds to the ``asset_types`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.asset_v1.services.asset_service.pagers.SearchAllResourcesAsyncPager:
                Search all resources response.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([scope, query, asset_types])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = asset_service.SearchAllResourcesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if scope is not None:
            request.scope = scope
        if query is not None:
            request.query = query
        if asset_types:
            request.asset_types.extend(asset_types)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_all_resources,
            default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=15.0,
            ),
            default_timeout=15.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("scope", request.scope),
            )),
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
        response = pagers.SearchAllResourcesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def search_all_iam_policies(self,
            request: Union[asset_service.SearchAllIamPoliciesRequest, dict] = None,
            *,
            scope: str = None,
            query: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.SearchAllIamPoliciesAsyncPager:
        r"""Searches all IAM policies within the specified scope, such as a
        project, folder, or organization. The caller must be granted the
        ``cloudasset.assets.searchAllIamPolicies`` permission on the
        desired scope, otherwise the request will be rejected.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_search_all_iam_policies():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                request = asset_v1.SearchAllIamPoliciesRequest(
                    scope="scope_value",
                )

                # Make the request
                page_result = client.search_all_iam_policies(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.asset_v1.types.SearchAllIamPoliciesRequest, dict]):
                The request object. Search all IAM policies request.
            scope (:class:`str`):
                Required. A scope can be a project, a folder, or an
                organization. The search is limited to the IAM policies
                within the ``scope``. The caller must be granted the
                ```cloudasset.assets.searchAllIamPolicies`` <https://cloud.google.com/asset-inventory/docs/access-control#required_permissions>`__
                permission on the desired scope.

                The allowed values are:

                -  projects/{PROJECT_ID} (e.g., "projects/foo-bar")
                -  projects/{PROJECT_NUMBER} (e.g., "projects/12345678")
                -  folders/{FOLDER_NUMBER} (e.g., "folders/1234567")
                -  organizations/{ORGANIZATION_NUMBER} (e.g.,
                   "organizations/123456")

                This corresponds to the ``scope`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (:class:`str`):
                Optional. The query statement. See `how to construct a
                query <https://cloud.google.com/asset-inventory/docs/searching-iam-policies#how_to_construct_a_query>`__
                for more information. If not specified or empty, it will
                search all the IAM policies within the specified
                ``scope``. Note that the query string is compared
                against each Cloud IAM policy binding, including its
                members, roles, and Cloud IAM conditions. The returned
                Cloud IAM policies will only contain the bindings that
                match your query. To learn more about the IAM policy
                structure, see `IAM policy
                doc <https://cloud.google.com/iam/docs/policies#structure>`__.

                Examples:

                -  ``policy:amy@gmail.com`` to find IAM policy bindings
                   that specify user "amy@gmail.com".
                -  ``policy:roles/compute.admin`` to find IAM policy
                   bindings that specify the Compute Admin role.
                -  ``policy:comp*`` to find IAM policy bindings that
                   contain "comp" as a prefix of any word in the
                   binding.
                -  ``policy.role.permissions:storage.buckets.update`` to
                   find IAM policy bindings that specify a role
                   containing "storage.buckets.update" permission. Note
                   that if callers don't have ``iam.roles.get`` access
                   to a role's included permissions, policy bindings
                   that specify this role will be dropped from the
                   search results.
                -  ``policy.role.permissions:upd*`` to find IAM policy
                   bindings that specify a role containing "upd" as a
                   prefix of any word in the role permission. Note that
                   if callers don't have ``iam.roles.get`` access to a
                   role's included permissions, policy bindings that
                   specify this role will be dropped from the search
                   results.
                -  ``resource:organizations/123456`` to find IAM policy
                   bindings that are set on "organizations/123456".
                -  ``resource=//cloudresourcemanager.googleapis.com/projects/myproject``
                   to find IAM policy bindings that are set on the
                   project named "myproject".
                -  ``Important`` to find IAM policy bindings that
                   contain "Important" as a word in any of the
                   searchable fields (except for the included
                   permissions).
                -  ``resource:(instance1 OR instance2) policy:amy`` to
                   find IAM policy bindings that are set on resources
                   "instance1" or "instance2" and also specify user
                   "amy".
                -  ``roles:roles/compute.admin`` to find IAM policy
                   bindings that specify the Compute Admin role.
                -  ``memberTypes:user`` to find IAM policy bindings that
                   contain the "user" member type.

                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.asset_v1.services.asset_service.pagers.SearchAllIamPoliciesAsyncPager:
                Search all IAM policies response.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([scope, query])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = asset_service.SearchAllIamPoliciesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if scope is not None:
            request.scope = scope
        if query is not None:
            request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_all_iam_policies,
            default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=15.0,
            ),
            default_timeout=15.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("scope", request.scope),
            )),
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
        response = pagers.SearchAllIamPoliciesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def analyze_iam_policy(self,
            request: Union[asset_service.AnalyzeIamPolicyRequest, dict] = None,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> asset_service.AnalyzeIamPolicyResponse:
        r"""Analyzes IAM policies to answer which identities have
        what accesses on which resources.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_analyze_iam_policy():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                analysis_query = asset_v1.IamPolicyAnalysisQuery()
                analysis_query.scope = "scope_value"

                request = asset_v1.AnalyzeIamPolicyRequest(
                    analysis_query=analysis_query,
                )

                # Make the request
                response = await client.analyze_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.asset_v1.types.AnalyzeIamPolicyRequest, dict]):
                The request object. A request message for
                [AssetService.AnalyzeIamPolicy][google.cloud.asset.v1.AssetService.AnalyzeIamPolicy].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.asset_v1.types.AnalyzeIamPolicyResponse:
                A response message for
                [AssetService.AnalyzeIamPolicy][google.cloud.asset.v1.AssetService.AnalyzeIamPolicy].

        """
        # Create or coerce a protobuf request object.
        request = asset_service.AnalyzeIamPolicyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.analyze_iam_policy,
            default_retry=retries.Retry(
initial=0.1,maximum=60.0,multiplier=1.3,                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("analysis_query.scope", request.analysis_query.scope),
            )),
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

    async def analyze_iam_policy_longrunning(self,
            request: Union[asset_service.AnalyzeIamPolicyLongrunningRequest, dict] = None,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Analyzes IAM policies asynchronously to answer which identities
        have what accesses on which resources, and writes the analysis
        results to a Google Cloud Storage or a BigQuery destination. For
        Cloud Storage destination, the output format is the JSON format
        that represents a
        [AnalyzeIamPolicyResponse][google.cloud.asset.v1.AnalyzeIamPolicyResponse].
        This method implements the
        [google.longrunning.Operation][google.longrunning.Operation],
        which allows you to track the operation status. We recommend
        intervals of at least 2 seconds with exponential backoff retry
        to poll the operation result. The metadata contains the request
        to help callers to map responses to requests.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import asset_v1

            async def sample_analyze_iam_policy_longrunning():
                # Create a client
                client = asset_v1.AssetServiceAsyncClient()

                # Initialize request argument(s)
                analysis_query = asset_v1.IamPolicyAnalysisQuery()
                analysis_query.scope = "scope_value"

                output_config = asset_v1.IamPolicyAnalysisOutputConfig()
                output_config.gcs_destination.uri = "uri_value"

                request = asset_v1.AnalyzeIamPolicyLongrunningRequest(
                    analysis_query=analysis_query,
                    output_config=output_config,
                )

                # Make the request
                operation = client.analyze_iam_policy_longrunning(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.asset_v1.types.AnalyzeIamPolicyLongrunningRequest, dict]):
                The request object. A request message for
                [AssetService.AnalyzeIamPolicyLongrunning][google.cloud.asset.v1.AssetService.AnalyzeIamPolicyLongrunning].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.asset_v1.types.AnalyzeIamPolicyLongrunningResponse`
                A response message for
                [AssetService.AnalyzeIamPolicyLongrunning][google.cloud.asset.v1.AssetService.AnalyzeIamPolicyLongrunning].

        """
        # Create or coerce a protobuf request object.
        request = asset_service.AnalyzeIamPolicyLongrunningRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.analyze_iam_policy_longrunning,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("analysis_query.scope", request.analysis_query.scope),
            )),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            asset_service.AnalyzeIamPolicyLongrunningResponse,
            metadata_type=asset_service.AnalyzeIamPolicyLongrunningRequest,
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
            "google-cloud-asset",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = (
    "AssetServiceAsyncClient",
)
