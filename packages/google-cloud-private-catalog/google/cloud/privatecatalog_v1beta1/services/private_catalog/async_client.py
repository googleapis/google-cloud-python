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
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.privatecatalog_v1beta1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.privatecatalog_v1beta1.services.private_catalog import pagers
from google.cloud.privatecatalog_v1beta1.types import private_catalog

from .client import PrivateCatalogClient
from .transports.base import DEFAULT_CLIENT_INFO, PrivateCatalogTransport
from .transports.grpc_asyncio import PrivateCatalogGrpcAsyncIOTransport


class PrivateCatalogAsyncClient:
    """``PrivateCatalog`` allows catalog consumers to retrieve ``Catalog``,
    ``Product`` and ``Version`` resources under a target resource
    context.

    ``Catalog`` is computed based on the [Association][]s linked to the
    target resource and its ancestors. Each association's
    [google.cloud.privatecatalogproducer.v1beta.Catalog][] is
    transformed into a ``Catalog``. If multiple associations have the
    same parent [google.cloud.privatecatalogproducer.v1beta.Catalog][],
    they are de-duplicated into one ``Catalog``. Users must have
    ``cloudprivatecatalog.catalogTargets.get`` IAM permission on the
    resource context in order to access catalogs. ``Catalog`` contains
    the resource name and a subset of data of the original
    [google.cloud.privatecatalogproducer.v1beta.Catalog][].

    ``Product`` is child resource of the catalog. A ``Product`` contains
    the resource name and a subset of the data of the original
    [google.cloud.privatecatalogproducer.v1beta.Product][].

    ``Version`` is child resource of the product. A ``Version`` contains
    the resource name and a subset of the data of the original
    [google.cloud.privatecatalogproducer.v1beta.Version][].
    """

    _client: PrivateCatalogClient

    DEFAULT_ENDPOINT = PrivateCatalogClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = PrivateCatalogClient.DEFAULT_MTLS_ENDPOINT

    catalog_path = staticmethod(PrivateCatalogClient.catalog_path)
    parse_catalog_path = staticmethod(PrivateCatalogClient.parse_catalog_path)
    product_path = staticmethod(PrivateCatalogClient.product_path)
    parse_product_path = staticmethod(PrivateCatalogClient.parse_product_path)
    version_path = staticmethod(PrivateCatalogClient.version_path)
    parse_version_path = staticmethod(PrivateCatalogClient.parse_version_path)
    common_billing_account_path = staticmethod(
        PrivateCatalogClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        PrivateCatalogClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(PrivateCatalogClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        PrivateCatalogClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        PrivateCatalogClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        PrivateCatalogClient.parse_common_organization_path
    )
    common_project_path = staticmethod(PrivateCatalogClient.common_project_path)
    parse_common_project_path = staticmethod(
        PrivateCatalogClient.parse_common_project_path
    )
    common_location_path = staticmethod(PrivateCatalogClient.common_location_path)
    parse_common_location_path = staticmethod(
        PrivateCatalogClient.parse_common_location_path
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
            PrivateCatalogAsyncClient: The constructed client.
        """
        return PrivateCatalogClient.from_service_account_info.__func__(PrivateCatalogAsyncClient, info, *args, **kwargs)  # type: ignore

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
            PrivateCatalogAsyncClient: The constructed client.
        """
        return PrivateCatalogClient.from_service_account_file.__func__(PrivateCatalogAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return PrivateCatalogClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> PrivateCatalogTransport:
        """Returns the transport used by the client instance.

        Returns:
            PrivateCatalogTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(PrivateCatalogClient).get_transport_class, type(PrivateCatalogClient)
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, PrivateCatalogTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the private catalog client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.PrivateCatalogTransport]): The
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
        self._client = PrivateCatalogClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def search_catalogs(
        self,
        request: Optional[Union[private_catalog.SearchCatalogsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchCatalogsAsyncPager:
        r"""Search [Catalog][google.cloud.privatecatalog.v1beta1.Catalog]
        resources that consumers have access to, within the scope of the
        consumer cloud resource hierarchy context.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import privatecatalog_v1beta1

            async def sample_search_catalogs():
                # Create a client
                client = privatecatalog_v1beta1.PrivateCatalogAsyncClient()

                # Initialize request argument(s)
                request = privatecatalog_v1beta1.SearchCatalogsRequest(
                    resource="resource_value",
                )

                # Make the request
                page_result = client.search_catalogs(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.privatecatalog_v1beta1.types.SearchCatalogsRequest, dict]]):
                The request object. Request message for
                [PrivateCatalog.SearchCatalogs][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchCatalogs].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.privatecatalog_v1beta1.services.private_catalog.pagers.SearchCatalogsAsyncPager:
                Response message for
                [PrivateCatalog.SearchCatalogs][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchCatalogs].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = private_catalog.SearchCatalogsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_catalogs,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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
        response = pagers.SearchCatalogsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def search_products(
        self,
        request: Optional[Union[private_catalog.SearchProductsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchProductsAsyncPager:
        r"""Search [Product][google.cloud.privatecatalog.v1beta1.Product]
        resources that consumers have access to, within the scope of the
        consumer cloud resource hierarchy context.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import privatecatalog_v1beta1

            async def sample_search_products():
                # Create a client
                client = privatecatalog_v1beta1.PrivateCatalogAsyncClient()

                # Initialize request argument(s)
                request = privatecatalog_v1beta1.SearchProductsRequest(
                    resource="resource_value",
                )

                # Make the request
                page_result = client.search_products(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.privatecatalog_v1beta1.types.SearchProductsRequest, dict]]):
                The request object. Request message for
                [PrivateCatalog.SearchProducts][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchProducts].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.privatecatalog_v1beta1.services.private_catalog.pagers.SearchProductsAsyncPager:
                Response message for
                [PrivateCatalog.SearchProducts][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchProducts].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = private_catalog.SearchProductsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_products,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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
        response = pagers.SearchProductsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def search_versions(
        self,
        request: Optional[Union[private_catalog.SearchVersionsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchVersionsAsyncPager:
        r"""Search [Version][google.cloud.privatecatalog.v1beta1.Version]
        resources that consumers have access to, within the scope of the
        consumer cloud resource hierarchy context.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import privatecatalog_v1beta1

            async def sample_search_versions():
                # Create a client
                client = privatecatalog_v1beta1.PrivateCatalogAsyncClient()

                # Initialize request argument(s)
                request = privatecatalog_v1beta1.SearchVersionsRequest(
                    resource="resource_value",
                    query="query_value",
                )

                # Make the request
                page_result = client.search_versions(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.privatecatalog_v1beta1.types.SearchVersionsRequest, dict]]):
                The request object. Request message for
                [PrivateCatalog.SearchVersions][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchVersions].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.privatecatalog_v1beta1.services.private_catalog.pagers.SearchVersionsAsyncPager:
                Response message for
                [PrivateCatalog.SearchVersions][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchVersions].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = private_catalog.SearchVersionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_versions,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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
        response = pagers.SearchVersionsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "PrivateCatalogAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("PrivateCatalogAsyncClient",)
