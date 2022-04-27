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
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.bigquery_data_exchange_v1beta1 import common  # type: ignore
from google.cloud.bigquery_data_exchange_v1beta1.services.analytics_hub_service import (
    pagers,
)
from google.cloud.bigquery_data_exchange_v1beta1.types import dataexchange
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import AnalyticsHubServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import AnalyticsHubServiceGrpcAsyncIOTransport
from .client import AnalyticsHubServiceClient


class AnalyticsHubServiceAsyncClient:
    """The AnalyticsHubService API facilitates data sharing within
    and across organizations. It allows data providers to publish
    Listings --- a discoverable and searchable SKU representing a
    dataset. Data consumers can subscribe to Listings. Upon
    subscription, AnalyticsHub provisions a "Linked Datasets"
    surfacing the data in the consumer's project.
    """

    _client: AnalyticsHubServiceClient

    DEFAULT_ENDPOINT = AnalyticsHubServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AnalyticsHubServiceClient.DEFAULT_MTLS_ENDPOINT

    data_exchange_path = staticmethod(AnalyticsHubServiceClient.data_exchange_path)
    parse_data_exchange_path = staticmethod(
        AnalyticsHubServiceClient.parse_data_exchange_path
    )
    dataset_path = staticmethod(AnalyticsHubServiceClient.dataset_path)
    parse_dataset_path = staticmethod(AnalyticsHubServiceClient.parse_dataset_path)
    listing_path = staticmethod(AnalyticsHubServiceClient.listing_path)
    parse_listing_path = staticmethod(AnalyticsHubServiceClient.parse_listing_path)
    common_billing_account_path = staticmethod(
        AnalyticsHubServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        AnalyticsHubServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AnalyticsHubServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        AnalyticsHubServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        AnalyticsHubServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        AnalyticsHubServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AnalyticsHubServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        AnalyticsHubServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(AnalyticsHubServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        AnalyticsHubServiceClient.parse_common_location_path
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
            AnalyticsHubServiceAsyncClient: The constructed client.
        """
        return AnalyticsHubServiceClient.from_service_account_info.__func__(AnalyticsHubServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            AnalyticsHubServiceAsyncClient: The constructed client.
        """
        return AnalyticsHubServiceClient.from_service_account_file.__func__(AnalyticsHubServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return AnalyticsHubServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> AnalyticsHubServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            AnalyticsHubServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(AnalyticsHubServiceClient).get_transport_class,
        type(AnalyticsHubServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, AnalyticsHubServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the analytics hub service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AnalyticsHubServiceTransport]): The
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
        self._client = AnalyticsHubServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_data_exchanges(
        self,
        request: Union[dataexchange.ListDataExchangesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDataExchangesAsyncPager:
        r"""Lists DataExchanges in a given project and location.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_list_data_exchanges():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                request = bigquery_data_exchange_v1beta1.ListDataExchangesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_data_exchanges(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.ListDataExchangesRequest, dict]):
                The request object. Message for requesting list of
                DataExchanges.
            parent (:class:`str`):
                Required. The parent resource path of the DataExchanges.
                e.g. ``projects/myproject/locations/US``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_data_exchange_v1beta1.services.analytics_hub_service.pagers.ListDataExchangesAsyncPager:
                Message for response to listing
                DataExchanges.
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

        request = dataexchange.ListDataExchangesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_data_exchanges,
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
        response = pagers.ListDataExchangesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_org_data_exchanges(
        self,
        request: Union[dataexchange.ListOrgDataExchangesRequest, dict] = None,
        *,
        organization: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListOrgDataExchangesAsyncPager:
        r"""Lists DataExchanges from projects in a given
        organization and location.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_list_org_data_exchanges():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                request = bigquery_data_exchange_v1beta1.ListOrgDataExchangesRequest(
                    organization="organization_value",
                )

                # Make the request
                page_result = client.list_org_data_exchanges(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.ListOrgDataExchangesRequest, dict]):
                The request object. Message for requesting list of
                DataExchanges from projects in an organization and
                location.
            organization (:class:`str`):
                Required. The organization resource path of the projects
                containing DataExchanges. e.g.
                ``organizations/myorg/locations/US``.

                This corresponds to the ``organization`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_data_exchange_v1beta1.services.analytics_hub_service.pagers.ListOrgDataExchangesAsyncPager:
                Message for response to listing
                DataExchanges in an organization and
                location.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([organization])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = dataexchange.ListOrgDataExchangesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if organization is not None:
            request.organization = organization

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_org_data_exchanges,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("organization", request.organization),)
            ),
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
        response = pagers.ListOrgDataExchangesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_data_exchange(
        self,
        request: Union[dataexchange.GetDataExchangeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataexchange.DataExchange:
        r"""Gets details of a single DataExchange.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_get_data_exchange():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                request = bigquery_data_exchange_v1beta1.GetDataExchangeRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_data_exchange(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.GetDataExchangeRequest, dict]):
                The request object. Message for getting a DataExchange.
            name (:class:`str`):
                Required. The resource name of the DataExchange. e.g.
                ``projects/myproject/locations/US/dataExchanges/123``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_data_exchange_v1beta1.types.DataExchange:
                A data exchange is a container that
                enables data sharing. It contains a set
                of listings of the data sources along
                with descriptive information of the data
                exchange.

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

        request = dataexchange.GetDataExchangeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_data_exchange,
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

    async def create_data_exchange(
        self,
        request: Union[dataexchange.CreateDataExchangeRequest, dict] = None,
        *,
        parent: str = None,
        data_exchange: dataexchange.DataExchange = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataexchange.DataExchange:
        r"""Creates a new DataExchange in a given project and
        location.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_create_data_exchange():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                data_exchange = bigquery_data_exchange_v1beta1.DataExchange()
                data_exchange.display_name = "display_name_value"

                request = bigquery_data_exchange_v1beta1.CreateDataExchangeRequest(
                    parent="parent_value",
                    data_exchange_id="data_exchange_id_value",
                    data_exchange=data_exchange,
                )

                # Make the request
                response = await client.create_data_exchange(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.CreateDataExchangeRequest, dict]):
                The request object. Message for creating a DataExchange.
            parent (:class:`str`):
                Required. The parent resource path of the DataExchange.
                e.g. ``projects/myproject/locations/US``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            data_exchange (:class:`google.cloud.bigquery_data_exchange_v1beta1.types.DataExchange`):
                Required. The DataExchange to create.
                This corresponds to the ``data_exchange`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_data_exchange_v1beta1.types.DataExchange:
                A data exchange is a container that
                enables data sharing. It contains a set
                of listings of the data sources along
                with descriptive information of the data
                exchange.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, data_exchange])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = dataexchange.CreateDataExchangeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if data_exchange is not None:
            request.data_exchange = data_exchange

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_data_exchange,
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

    async def update_data_exchange(
        self,
        request: Union[dataexchange.UpdateDataExchangeRequest, dict] = None,
        *,
        data_exchange: dataexchange.DataExchange = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataexchange.DataExchange:
        r"""Updates the parameters of a single DataExchange.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_update_data_exchange():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                data_exchange = bigquery_data_exchange_v1beta1.DataExchange()
                data_exchange.display_name = "display_name_value"

                request = bigquery_data_exchange_v1beta1.UpdateDataExchangeRequest(
                    data_exchange=data_exchange,
                )

                # Make the request
                response = await client.update_data_exchange(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.UpdateDataExchangeRequest, dict]):
                The request object. Message for updating a DataExchange.
            data_exchange (:class:`google.cloud.bigquery_data_exchange_v1beta1.types.DataExchange`):
                Required. The DataExchange to update.
                This corresponds to the ``data_exchange`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Field mask is used to specify the fields to be
                overwritten in the DataExchange resource by the update.
                The fields specified in the update_mask are relative to
                the resource, not the full request.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_data_exchange_v1beta1.types.DataExchange:
                A data exchange is a container that
                enables data sharing. It contains a set
                of listings of the data sources along
                with descriptive information of the data
                exchange.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([data_exchange, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = dataexchange.UpdateDataExchangeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if data_exchange is not None:
            request.data_exchange = data_exchange
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_data_exchange,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("data_exchange.name", request.data_exchange.name),)
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

    async def delete_data_exchange(
        self,
        request: Union[dataexchange.DeleteDataExchangeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a single DataExchange.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_delete_data_exchange():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                request = bigquery_data_exchange_v1beta1.DeleteDataExchangeRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_data_exchange(request=request)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.DeleteDataExchangeRequest, dict]):
                The request object. Message for deleting a DataExchange.
            name (:class:`str`):
                Required. Resource name of the DataExchange to delete.
                e.g.
                ``projects/myproject/locations/US/dataExchanges/123``.

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

        request = dataexchange.DeleteDataExchangeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_data_exchange,
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

    async def list_listings(
        self,
        request: Union[dataexchange.ListListingsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListListingsAsyncPager:
        r"""Lists Listings in a given project and location.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_list_listings():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                request = bigquery_data_exchange_v1beta1.ListListingsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_listings(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.ListListingsRequest, dict]):
                The request object. Message for requesting list of
                Listings.
            parent (:class:`str`):
                Required. The parent resource path of the listing. e.g.
                ``projects/myproject/locations/US/dataExchanges/123``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_data_exchange_v1beta1.services.analytics_hub_service.pagers.ListListingsAsyncPager:
                Message for response to listing
                Listings.
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

        request = dataexchange.ListListingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_listings,
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
        response = pagers.ListListingsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_listing(
        self,
        request: Union[dataexchange.GetListingRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataexchange.Listing:
        r"""Gets details of a single Listing.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_get_listing():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                request = bigquery_data_exchange_v1beta1.GetListingRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_listing(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.GetListingRequest, dict]):
                The request object. Message for getting a Listing.
            name (:class:`str`):
                Required. The resource name of the listing. e.g.
                ``projects/myproject/locations/US/dataExchanges/123/listings/456``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_data_exchange_v1beta1.types.Listing:
                A listing is what gets published into
                a data exchange that a subscriber can
                subscribe to. It contains a reference to
                the data source along with descriptive
                information that will help subscribers
                find and subscribe the data.

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

        request = dataexchange.GetListingRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_listing,
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

    async def create_listing(
        self,
        request: Union[dataexchange.CreateListingRequest, dict] = None,
        *,
        parent: str = None,
        listing: dataexchange.Listing = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataexchange.Listing:
        r"""Creates a new Listing in a given project and
        location.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_create_listing():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                listing = bigquery_data_exchange_v1beta1.Listing()
                listing.display_name = "display_name_value"

                request = bigquery_data_exchange_v1beta1.CreateListingRequest(
                    parent="parent_value",
                    listing_id="listing_id_value",
                    listing=listing,
                )

                # Make the request
                response = await client.create_listing(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.CreateListingRequest, dict]):
                The request object. Message for creating a Listing.
            parent (:class:`str`):
                Required. The parent resource path of the listing. e.g.
                ``projects/myproject/locations/US/dataExchanges/123``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            listing (:class:`google.cloud.bigquery_data_exchange_v1beta1.types.Listing`):
                Required. The listing to create.
                This corresponds to the ``listing`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_data_exchange_v1beta1.types.Listing:
                A listing is what gets published into
                a data exchange that a subscriber can
                subscribe to. It contains a reference to
                the data source along with descriptive
                information that will help subscribers
                find and subscribe the data.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, listing])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = dataexchange.CreateListingRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if listing is not None:
            request.listing = listing

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_listing,
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

    async def update_listing(
        self,
        request: Union[dataexchange.UpdateListingRequest, dict] = None,
        *,
        listing: dataexchange.Listing = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataexchange.Listing:
        r"""Updates the parameters of a single Listing.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_update_listing():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                listing = bigquery_data_exchange_v1beta1.Listing()
                listing.display_name = "display_name_value"

                request = bigquery_data_exchange_v1beta1.UpdateListingRequest(
                    listing=listing,
                )

                # Make the request
                response = await client.update_listing(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.UpdateListingRequest, dict]):
                The request object. Message for updating a Listing.
            listing (:class:`google.cloud.bigquery_data_exchange_v1beta1.types.Listing`):
                Required. The listing to update.
                This corresponds to the ``listing`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Field mask is used to specify the fields to be
                overwritten in the Listing resource by the update. The
                fields specified in the update_mask are relative to the
                resource, not the full request.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_data_exchange_v1beta1.types.Listing:
                A listing is what gets published into
                a data exchange that a subscriber can
                subscribe to. It contains a reference to
                the data source along with descriptive
                information that will help subscribers
                find and subscribe the data.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([listing, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = dataexchange.UpdateListingRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if listing is not None:
            request.listing = listing
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_listing,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("listing.name", request.listing.name),)
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

    async def delete_listing(
        self,
        request: Union[dataexchange.DeleteListingRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a single Listing, as long as there are no
        subscriptions associated with the source of this
        Listing.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_delete_listing():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                request = bigquery_data_exchange_v1beta1.DeleteListingRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_listing(request=request)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.DeleteListingRequest, dict]):
                The request object. Message for deleting a Listing.
            name (:class:`str`):
                Required. Resource name of the listing to delete. e.g.
                ``projects/myproject/locations/US/dataExchanges/123/listings/456``.

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

        request = dataexchange.DeleteListingRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_listing,
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

    async def subscribe_listing(
        self,
        request: Union[dataexchange.SubscribeListingRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataexchange.SubscribeListingResponse:
        r"""Subscribes to a single Listing.
        Data Exchange currently supports one type of Listing: a
        BigQuery dataset. Upon subscription to a Listing for a
        BigQuery dataset, Data Exchange creates a linked dataset
        in the subscriber's project.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1

            async def sample_subscribe_listing():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                destination_dataset = bigquery_data_exchange_v1beta1.DestinationDataset()
                destination_dataset.dataset_reference.dataset_id = "dataset_id_value"
                destination_dataset.dataset_reference.project_id = "project_id_value"
                destination_dataset.location = "location_value"

                request = bigquery_data_exchange_v1beta1.SubscribeListingRequest(
                    destination_dataset=destination_dataset,
                    name="name_value",
                )

                # Make the request
                response = await client.subscribe_listing(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_data_exchange_v1beta1.types.SubscribeListingRequest, dict]):
                The request object. Message for subscribing a Listing.
            name (:class:`str`):
                Required. Resource name of the listing to subscribe to.
                e.g.
                ``projects/myproject/locations/US/dataExchanges/123/listings/456``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_data_exchange_v1beta1.types.SubscribeListingResponse:
                Message for response to subscribing a
                Listing. Empty for now.

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

        request = dataexchange.SubscribeListingRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.subscribe_listing,
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

    async def get_iam_policy(
        self,
        request: Union[iam_policy_pb2.GetIamPolicyRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the IAM policy for a dataExchange or a listing.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            async def sample_get_iam_policy():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.GetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = await client.get_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]):
                The request object. Request message for `GetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": [ "user:eve@example.com" ],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ], "etag": "BwWWja0YfJA=", "version": 3

                      }

                   **YAML example:**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z') etag:
                      BwWWja0YfJA= version: 3

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_iam_policy,
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

        # Done; return the response.
        return response

    async def set_iam_policy(
        self,
        request: Union[iam_policy_pb2.SetIamPolicyRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the IAM policy for a dataExchange or a listing.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            async def sample_set_iam_policy():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.SetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = await client.set_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]):
                The request object. Request message for `SetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": [ "user:eve@example.com" ],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ], "etag": "BwWWja0YfJA=", "version": 3

                      }

                   **YAML example:**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z') etag:
                      BwWWja0YfJA= version: 3

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_iam_policy,
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

        # Done; return the response.
        return response

    async def test_iam_permissions(
        self,
        request: Union[iam_policy_pb2.TestIamPermissionsRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns the permissions that a caller has on a
        specified dataExchange or listing.

        .. code-block:: python

            from google.cloud import bigquery_data_exchange_v1beta1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            async def sample_test_iam_permissions():
                # Create a client
                client = bigquery_data_exchange_v1beta1.AnalyticsHubServiceAsyncClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.TestIamPermissionsRequest(
                    resource="resource_value",
                    permissions=['permissions_value_1', 'permissions_value_2'],
                )

                # Make the request
                response = await client.test_iam_permissions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]):
                The request object. Request message for
                `TestIamPermissions` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.test_iam_permissions,
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

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bigquery-data-exchange",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("AnalyticsHubServiceAsyncClient",)
