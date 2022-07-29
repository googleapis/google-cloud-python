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

from google.cloud.retail_v2beta.services.catalog_service import pagers
from google.cloud.retail_v2beta.types import catalog_service, common, import_config
from google.cloud.retail_v2beta.types import catalog
from google.cloud.retail_v2beta.types import catalog as gcr_catalog

from .client import CatalogServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, CatalogServiceTransport
from .transports.grpc_asyncio import CatalogServiceGrpcAsyncIOTransport


class CatalogServiceAsyncClient:
    """Service for managing catalog configuration."""

    _client: CatalogServiceClient

    DEFAULT_ENDPOINT = CatalogServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CatalogServiceClient.DEFAULT_MTLS_ENDPOINT

    attributes_config_path = staticmethod(CatalogServiceClient.attributes_config_path)
    parse_attributes_config_path = staticmethod(
        CatalogServiceClient.parse_attributes_config_path
    )
    branch_path = staticmethod(CatalogServiceClient.branch_path)
    parse_branch_path = staticmethod(CatalogServiceClient.parse_branch_path)
    catalog_path = staticmethod(CatalogServiceClient.catalog_path)
    parse_catalog_path = staticmethod(CatalogServiceClient.parse_catalog_path)
    completion_config_path = staticmethod(CatalogServiceClient.completion_config_path)
    parse_completion_config_path = staticmethod(
        CatalogServiceClient.parse_completion_config_path
    )
    common_billing_account_path = staticmethod(
        CatalogServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CatalogServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CatalogServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        CatalogServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        CatalogServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        CatalogServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CatalogServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        CatalogServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(CatalogServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        CatalogServiceClient.parse_common_location_path
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
            CatalogServiceAsyncClient: The constructed client.
        """
        return CatalogServiceClient.from_service_account_info.__func__(CatalogServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            CatalogServiceAsyncClient: The constructed client.
        """
        return CatalogServiceClient.from_service_account_file.__func__(CatalogServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return CatalogServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> CatalogServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            CatalogServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CatalogServiceClient).get_transport_class, type(CatalogServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CatalogServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the catalog service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CatalogServiceTransport]): The
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
        self._client = CatalogServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_catalogs(
        self,
        request: Union[catalog_service.ListCatalogsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCatalogsAsyncPager:
        r"""Lists all the [Catalog][google.cloud.retail.v2beta.Catalog]s
        associated with the project.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_list_catalogs():
                # Create a client
                client = retail_v2beta.CatalogServiceAsyncClient()

                # Initialize request argument(s)
                request = retail_v2beta.ListCatalogsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_catalogs(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.ListCatalogsRequest, dict]):
                The request object. Request for
                [CatalogService.ListCatalogs][google.cloud.retail.v2beta.CatalogService.ListCatalogs]
                method.
            parent (:class:`str`):
                Required. The account resource name with an associated
                location.

                If the caller does not have permission to list
                [Catalog][google.cloud.retail.v2beta.Catalog]s under
                this location, regardless of whether or not this
                location exists, a PERMISSION_DENIED error is returned.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.services.catalog_service.pagers.ListCatalogsAsyncPager:
                Response for
                   [CatalogService.ListCatalogs][google.cloud.retail.v2beta.CatalogService.ListCatalogs]
                   method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        request = catalog_service.ListCatalogsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_catalogs,
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
        response = pagers.ListCatalogsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_catalog(
        self,
        request: Union[catalog_service.UpdateCatalogRequest, dict] = None,
        *,
        catalog: gcr_catalog.Catalog = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_catalog.Catalog:
        r"""Updates the [Catalog][google.cloud.retail.v2beta.Catalog]s.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_update_catalog():
                # Create a client
                client = retail_v2beta.CatalogServiceAsyncClient()

                # Initialize request argument(s)
                catalog = retail_v2beta.Catalog()
                catalog.name = "name_value"
                catalog.display_name = "display_name_value"

                request = retail_v2beta.UpdateCatalogRequest(
                    catalog=catalog,
                )

                # Make the request
                response = await client.update_catalog(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.UpdateCatalogRequest, dict]):
                The request object. Request for
                [CatalogService.UpdateCatalog][google.cloud.retail.v2beta.CatalogService.UpdateCatalog]
                method.
            catalog (:class:`google.cloud.retail_v2beta.types.Catalog`):
                Required. The
                [Catalog][google.cloud.retail.v2beta.Catalog] to update.

                If the caller does not have permission to update the
                [Catalog][google.cloud.retail.v2beta.Catalog],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                If the [Catalog][google.cloud.retail.v2beta.Catalog] to
                update does not exist, a NOT_FOUND error is returned.

                This corresponds to the ``catalog`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Indicates which fields in the provided
                [Catalog][google.cloud.retail.v2beta.Catalog] to update.

                If an unsupported or unknown field is provided, an
                INVALID_ARGUMENT error is returned.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.Catalog:
                The catalog configuration.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([catalog, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = catalog_service.UpdateCatalogRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if catalog is not None:
            request.catalog = catalog
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_catalog,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("catalog.name", request.catalog.name),)
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

    async def set_default_branch(
        self,
        request: Union[catalog_service.SetDefaultBranchRequest, dict] = None,
        *,
        catalog: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Set a specified branch id as default branch. API methods such as
        [SearchService.Search][google.cloud.retail.v2beta.SearchService.Search],
        [ProductService.GetProduct][google.cloud.retail.v2beta.ProductService.GetProduct],
        [ProductService.ListProducts][google.cloud.retail.v2beta.ProductService.ListProducts]
        will treat requests using "default_branch" to the actual branch
        id set as default.

        For example, if ``projects/*/locations/*/catalogs/*/branches/1``
        is set as default, setting
        [SearchRequest.branch][google.cloud.retail.v2beta.SearchRequest.branch]
        to ``projects/*/locations/*/catalogs/*/branches/default_branch``
        is equivalent to setting
        [SearchRequest.branch][google.cloud.retail.v2beta.SearchRequest.branch]
        to ``projects/*/locations/*/catalogs/*/branches/1``.

        Using multiple branches can be useful when developers would like
        to have a staging branch to test and verify for future usage.
        When it becomes ready, developers switch on the staging branch
        using this API while keeping using
        ``projects/*/locations/*/catalogs/*/branches/default_branch`` as
        [SearchRequest.branch][google.cloud.retail.v2beta.SearchRequest.branch]
        to route the traffic to this staging branch.

        CAUTION: If you have live predict/search traffic, switching the
        default branch could potentially cause outages if the ID space
        of the new branch is very different from the old one.

        More specifically:

        -  PredictionService will only return product IDs from branch
           {newBranch}.
        -  SearchService will only return product IDs from branch
           {newBranch} (if branch is not explicitly set).
        -  UserEventService will only join events with products from
           branch {newBranch}.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_set_default_branch():
                # Create a client
                client = retail_v2beta.CatalogServiceAsyncClient()

                # Initialize request argument(s)
                request = retail_v2beta.SetDefaultBranchRequest(
                )

                # Make the request
                await client.set_default_branch(request=request)

        Args:
            request (Union[google.cloud.retail_v2beta.types.SetDefaultBranchRequest, dict]):
                The request object. Request message to set a specified
                branch as new default_branch.
            catalog (:class:`str`):
                Full resource name of the catalog, such as
                ``projects/*/locations/global/catalogs/default_catalog``.

                This corresponds to the ``catalog`` field
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
        has_flattened_params = any([catalog])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = catalog_service.SetDefaultBranchRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if catalog is not None:
            request.catalog = catalog

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_default_branch,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("catalog", request.catalog),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def get_default_branch(
        self,
        request: Union[catalog_service.GetDefaultBranchRequest, dict] = None,
        *,
        catalog: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> catalog_service.GetDefaultBranchResponse:
        r"""Get which branch is currently default branch set by
        [CatalogService.SetDefaultBranch][google.cloud.retail.v2beta.CatalogService.SetDefaultBranch]
        method under a specified parent catalog.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_get_default_branch():
                # Create a client
                client = retail_v2beta.CatalogServiceAsyncClient()

                # Initialize request argument(s)
                request = retail_v2beta.GetDefaultBranchRequest(
                )

                # Make the request
                response = await client.get_default_branch(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.GetDefaultBranchRequest, dict]):
                The request object. Request message to show which branch
                is currently the default branch.
            catalog (:class:`str`):
                The parent catalog resource name, such as
                ``projects/*/locations/global/catalogs/default_catalog``.

                This corresponds to the ``catalog`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.GetDefaultBranchResponse:
                Response message of
                   [CatalogService.GetDefaultBranch][google.cloud.retail.v2beta.CatalogService.GetDefaultBranch].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([catalog])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = catalog_service.GetDefaultBranchRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if catalog is not None:
            request.catalog = catalog

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_default_branch,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("catalog", request.catalog),)),
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

    async def get_completion_config(
        self,
        request: Union[catalog_service.GetCompletionConfigRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> catalog.CompletionConfig:
        r"""Gets a
        [CompletionConfig][google.cloud.retail.v2beta.CompletionConfig].

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_get_completion_config():
                # Create a client
                client = retail_v2beta.CatalogServiceAsyncClient()

                # Initialize request argument(s)
                request = retail_v2beta.GetCompletionConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_completion_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.GetCompletionConfigRequest, dict]):
                The request object. Request for
                [CatalogService.GetCompletionConfig][google.cloud.retail.v2beta.CatalogService.GetCompletionConfig]
                method.
            name (:class:`str`):
                Required. Full CompletionConfig resource name. Format:
                projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/completionConfig

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.CompletionConfig:
                Catalog level autocomplete config for
                customers to customize autocomplete
                feature's settings.

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

        request = catalog_service.GetCompletionConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_completion_config,
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

    async def update_completion_config(
        self,
        request: Union[catalog_service.UpdateCompletionConfigRequest, dict] = None,
        *,
        completion_config: catalog.CompletionConfig = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> catalog.CompletionConfig:
        r"""Updates the
        [CompletionConfig][google.cloud.retail.v2beta.CompletionConfig]s.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_update_completion_config():
                # Create a client
                client = retail_v2beta.CatalogServiceAsyncClient()

                # Initialize request argument(s)
                completion_config = retail_v2beta.CompletionConfig()
                completion_config.name = "name_value"

                request = retail_v2beta.UpdateCompletionConfigRequest(
                    completion_config=completion_config,
                )

                # Make the request
                response = await client.update_completion_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.UpdateCompletionConfigRequest, dict]):
                The request object. Request for
                [CatalogService.UpdateCompletionConfig][google.cloud.retail.v2beta.CatalogService.UpdateCompletionConfig]
                method.
            completion_config (:class:`google.cloud.retail_v2beta.types.CompletionConfig`):
                Required. The
                [CompletionConfig][google.cloud.retail.v2beta.CompletionConfig]
                to update.

                If the caller does not have permission to update the
                [CompletionConfig][google.cloud.retail.v2beta.CompletionConfig],
                then a PERMISSION_DENIED error is returned.

                If the
                [CompletionConfig][google.cloud.retail.v2beta.CompletionConfig]
                to update does not exist, a NOT_FOUND error is returned.

                This corresponds to the ``completion_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Indicates which fields in the provided
                [CompletionConfig][google.cloud.retail.v2beta.CompletionConfig]
                to update. The following are the only supported fields:

                -  [CompletionConfig.matching_order][google.cloud.retail.v2beta.CompletionConfig.matching_order]
                -  [CompletionConfig.max_suggestions][google.cloud.retail.v2beta.CompletionConfig.max_suggestions]
                -  [CompletionConfig.min_prefix_length][google.cloud.retail.v2beta.CompletionConfig.min_prefix_length]
                -  [CompletionConfig.auto_learning][google.cloud.retail.v2beta.CompletionConfig.auto_learning]

                If not set, all supported fields are updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.CompletionConfig:
                Catalog level autocomplete config for
                customers to customize autocomplete
                feature's settings.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([completion_config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = catalog_service.UpdateCompletionConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if completion_config is not None:
            request.completion_config = completion_config
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_completion_config,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("completion_config.name", request.completion_config.name),)
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

    async def get_attributes_config(
        self,
        request: Union[catalog_service.GetAttributesConfigRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> catalog.AttributesConfig:
        r"""Gets an
        [AttributesConfig][google.cloud.retail.v2beta.AttributesConfig].

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_get_attributes_config():
                # Create a client
                client = retail_v2beta.CatalogServiceAsyncClient()

                # Initialize request argument(s)
                request = retail_v2beta.GetAttributesConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_attributes_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.GetAttributesConfigRequest, dict]):
                The request object. Request for
                [CatalogService.GetAttributesConfig][google.cloud.retail.v2beta.CatalogService.GetAttributesConfig]
                method.
            name (:class:`str`):
                Required. Full AttributesConfig resource name. Format:
                ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/attributesConfig``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.AttributesConfig:
                Catalog level attribute config.
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

        request = catalog_service.GetAttributesConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_attributes_config,
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

    async def update_attributes_config(
        self,
        request: Union[catalog_service.UpdateAttributesConfigRequest, dict] = None,
        *,
        attributes_config: catalog.AttributesConfig = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> catalog.AttributesConfig:
        r"""Updates the
        [AttributesConfig][google.cloud.retail.v2beta.AttributesConfig].

        The catalog attributes in the request will be updated in the
        catalog, or inserted if they do not exist. Existing catalog
        attributes not included in the request will remain unchanged.
        Attributes that are assigned to products, but do not exist at
        the catalog level, are always included in the response. The
        product attribute is assigned default values for missing catalog
        attribute fields, e.g., searchable and dynamic facetable
        options.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_update_attributes_config():
                # Create a client
                client = retail_v2beta.CatalogServiceAsyncClient()

                # Initialize request argument(s)
                attributes_config = retail_v2beta.AttributesConfig()
                attributes_config.name = "name_value"

                request = retail_v2beta.UpdateAttributesConfigRequest(
                    attributes_config=attributes_config,
                )

                # Make the request
                response = await client.update_attributes_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.UpdateAttributesConfigRequest, dict]):
                The request object. Request for
                [CatalogService.UpdateAttributesConfig][google.cloud.retail.v2beta.CatalogService.UpdateAttributesConfig]
                method.
            attributes_config (:class:`google.cloud.retail_v2beta.types.AttributesConfig`):
                Required. The
                [AttributesConfig][google.cloud.retail.v2beta.AttributesConfig]
                to update.

                This corresponds to the ``attributes_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Indicates which fields in the provided
                [AttributesConfig][google.cloud.retail.v2beta.AttributesConfig]
                to update. The following is the only supported field:

                -  [AttributesConfig.catalog_attributes][google.cloud.retail.v2beta.AttributesConfig.catalog_attributes]

                If not set, all supported fields are updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.AttributesConfig:
                Catalog level attribute config.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([attributes_config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = catalog_service.UpdateAttributesConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if attributes_config is not None:
            request.attributes_config = attributes_config
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_attributes_config,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("attributes_config.name", request.attributes_config.name),)
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

    async def add_catalog_attribute(
        self,
        request: Union[catalog_service.AddCatalogAttributeRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> catalog.AttributesConfig:
        r"""Adds the specified
        [CatalogAttribute][google.cloud.retail.v2beta.CatalogAttribute]
        to the
        [AttributesConfig][google.cloud.retail.v2beta.AttributesConfig].

        If the
        [CatalogAttribute][google.cloud.retail.v2beta.CatalogAttribute]
        to add already exists, an ALREADY_EXISTS error is returned.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_add_catalog_attribute():
                # Create a client
                client = retail_v2beta.CatalogServiceAsyncClient()

                # Initialize request argument(s)
                catalog_attribute = retail_v2beta.CatalogAttribute()
                catalog_attribute.key = "key_value"

                request = retail_v2beta.AddCatalogAttributeRequest(
                    attributes_config="attributes_config_value",
                    catalog_attribute=catalog_attribute,
                )

                # Make the request
                response = await client.add_catalog_attribute(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.AddCatalogAttributeRequest, dict]):
                The request object. Request for
                [CatalogService.AddCatalogAttribute][google.cloud.retail.v2beta.CatalogService.AddCatalogAttribute]
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.AttributesConfig:
                Catalog level attribute config.
        """
        # Create or coerce a protobuf request object.
        request = catalog_service.AddCatalogAttributeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.add_catalog_attribute,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("attributes_config", request.attributes_config),)
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

    async def remove_catalog_attribute(
        self,
        request: Union[catalog_service.RemoveCatalogAttributeRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> catalog.AttributesConfig:
        r"""Removes the specified
        [CatalogAttribute][google.cloud.retail.v2beta.CatalogAttribute]
        from the
        [AttributesConfig][google.cloud.retail.v2beta.AttributesConfig].

        If the
        [CatalogAttribute][google.cloud.retail.v2beta.CatalogAttribute]
        to remove does not exist, a NOT_FOUND error is returned.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_remove_catalog_attribute():
                # Create a client
                client = retail_v2beta.CatalogServiceAsyncClient()

                # Initialize request argument(s)
                request = retail_v2beta.RemoveCatalogAttributeRequest(
                    attributes_config="attributes_config_value",
                    key="key_value",
                )

                # Make the request
                response = await client.remove_catalog_attribute(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.RemoveCatalogAttributeRequest, dict]):
                The request object. Request for
                [CatalogService.RemoveCatalogAttribute][google.cloud.retail.v2beta.CatalogService.RemoveCatalogAttribute]
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.AttributesConfig:
                Catalog level attribute config.
        """
        # Create or coerce a protobuf request object.
        request = catalog_service.RemoveCatalogAttributeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.remove_catalog_attribute,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("attributes_config", request.attributes_config),)
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

    async def replace_catalog_attribute(
        self,
        request: Union[catalog_service.ReplaceCatalogAttributeRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> catalog.AttributesConfig:
        r"""Replaces the specified
        [CatalogAttribute][google.cloud.retail.v2beta.CatalogAttribute]
        in the
        [AttributesConfig][google.cloud.retail.v2beta.AttributesConfig]
        by updating the catalog attribute with the same
        [CatalogAttribute.key][google.cloud.retail.v2beta.CatalogAttribute.key].

        If the
        [CatalogAttribute][google.cloud.retail.v2beta.CatalogAttribute]
        to replace does not exist, a NOT_FOUND error is returned.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_replace_catalog_attribute():
                # Create a client
                client = retail_v2beta.CatalogServiceAsyncClient()

                # Initialize request argument(s)
                catalog_attribute = retail_v2beta.CatalogAttribute()
                catalog_attribute.key = "key_value"

                request = retail_v2beta.ReplaceCatalogAttributeRequest(
                    attributes_config="attributes_config_value",
                    catalog_attribute=catalog_attribute,
                )

                # Make the request
                response = await client.replace_catalog_attribute(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.ReplaceCatalogAttributeRequest, dict]):
                The request object. Request for
                [CatalogService.ReplaceCatalogAttribute][google.cloud.retail.v2beta.CatalogService.ReplaceCatalogAttribute]
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.AttributesConfig:
                Catalog level attribute config.
        """
        # Create or coerce a protobuf request object.
        request = catalog_service.ReplaceCatalogAttributeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.replace_catalog_attribute,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("attributes_config", request.attributes_config),)
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-retail",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CatalogServiceAsyncClient",)
