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
from collections import OrderedDict
import logging as std_logging
import re
from typing import (
    Callable,
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

from google.cloud.retail_v2alpha import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore

from google.cloud.retail_v2alpha.types import (
    merchant_center_account_link as gcr_merchant_center_account_link,
)
from google.cloud.retail_v2alpha.types import merchant_center_account_link_service
from google.cloud.retail_v2alpha.types import merchant_center_account_link

from .client import MerchantCenterAccountLinkServiceClient
from .transports.base import (
    DEFAULT_CLIENT_INFO,
    MerchantCenterAccountLinkServiceTransport,
)
from .transports.grpc_asyncio import (
    MerchantCenterAccountLinkServiceGrpcAsyncIOTransport,
)

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class MerchantCenterAccountLinkServiceAsyncClient:
    """Merchant Center Link service to link a Branch to a Merchant
    Center Account.
    """

    _client: MerchantCenterAccountLinkServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = MerchantCenterAccountLinkServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = MerchantCenterAccountLinkServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = (
        MerchantCenterAccountLinkServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    )
    _DEFAULT_UNIVERSE = MerchantCenterAccountLinkServiceClient._DEFAULT_UNIVERSE

    catalog_path = staticmethod(MerchantCenterAccountLinkServiceClient.catalog_path)
    parse_catalog_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.parse_catalog_path
    )
    merchant_center_account_link_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.merchant_center_account_link_path
    )
    parse_merchant_center_account_link_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.parse_merchant_center_account_link_path
    )
    common_billing_account_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.common_folder_path
    )
    parse_common_folder_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        MerchantCenterAccountLinkServiceClient.parse_common_location_path
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
            MerchantCenterAccountLinkServiceAsyncClient: The constructed client.
        """
        return MerchantCenterAccountLinkServiceClient.from_service_account_info.__func__(MerchantCenterAccountLinkServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            MerchantCenterAccountLinkServiceAsyncClient: The constructed client.
        """
        return MerchantCenterAccountLinkServiceClient.from_service_account_file.__func__(MerchantCenterAccountLinkServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return MerchantCenterAccountLinkServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> MerchantCenterAccountLinkServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            MerchantCenterAccountLinkServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._client._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used
                by the client instance.
        """
        return self._client._universe_domain

    get_transport_class = MerchantCenterAccountLinkServiceClient.get_transport_class

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str,
                MerchantCenterAccountLinkServiceTransport,
                Callable[..., MerchantCenterAccountLinkServiceTransport],
            ]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the merchant center account link service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,MerchantCenterAccountLinkServiceTransport,Callable[..., MerchantCenterAccountLinkServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the MerchantCenterAccountLinkServiceTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = MerchantCenterAccountLinkServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

        if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        ):  # pragma: NO COVER
            _LOGGER.debug(
                "Created client `google.cloud.retail_v2alpha.MerchantCenterAccountLinkServiceAsyncClient`.",
                extra={
                    "serviceName": "google.cloud.retail.v2alpha.MerchantCenterAccountLinkService",
                    "universeDomain": getattr(
                        self._client._transport._credentials, "universe_domain", ""
                    ),
                    "credentialsType": f"{type(self._client._transport._credentials).__module__}.{type(self._client._transport._credentials).__qualname__}",
                    "credentialsInfo": getattr(
                        self.transport._credentials, "get_cred_info", lambda: None
                    )(),
                }
                if hasattr(self._client._transport, "_credentials")
                else {
                    "serviceName": "google.cloud.retail.v2alpha.MerchantCenterAccountLinkService",
                    "credentialsType": None,
                },
            )

    async def list_merchant_center_account_links(
        self,
        request: Optional[
            Union[
                merchant_center_account_link_service.ListMerchantCenterAccountLinksRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> merchant_center_account_link_service.ListMerchantCenterAccountLinksResponse:
        r"""Lists all
        [MerchantCenterAccountLink][google.cloud.retail.v2alpha.MerchantCenterAccountLink]s
        under the specified parent
        [Catalog][google.cloud.retail.v2alpha.Catalog].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            async def sample_list_merchant_center_account_links():
                # Create a client
                client = retail_v2alpha.MerchantCenterAccountLinkServiceAsyncClient()

                # Initialize request argument(s)
                request = retail_v2alpha.ListMerchantCenterAccountLinksRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.list_merchant_center_account_links(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.retail_v2alpha.types.ListMerchantCenterAccountLinksRequest, dict]]):
                The request object. Request for
                [MerchantCenterAccountLinkService.ListMerchantCenterAccountLinks][google.cloud.retail.v2alpha.MerchantCenterAccountLinkService.ListMerchantCenterAccountLinks]
                method.
            parent (:class:`str`):
                Required. The parent Catalog of the resource. It must
                match this format:
                ``projects/{PROJECT_NUMBER}/locations/global/catalogs/{CATALOG_ID}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.retail_v2alpha.types.ListMerchantCenterAccountLinksResponse:
                Response for
                   [MerchantCenterAccountLinkService.ListMerchantCenterAccountLinks][google.cloud.retail.v2alpha.MerchantCenterAccountLinkService.ListMerchantCenterAccountLinks]
                   method.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            merchant_center_account_link_service.ListMerchantCenterAccountLinksRequest,
        ):
            request = merchant_center_account_link_service.ListMerchantCenterAccountLinksRequest(
                request
            )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_merchant_center_account_links
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_merchant_center_account_link(
        self,
        request: Optional[
            Union[
                merchant_center_account_link_service.CreateMerchantCenterAccountLinkRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        merchant_center_account_link: Optional[
            gcr_merchant_center_account_link.MerchantCenterAccountLink
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a
        [MerchantCenterAccountLink][google.cloud.retail.v2alpha.MerchantCenterAccountLink].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            async def sample_create_merchant_center_account_link():
                # Create a client
                client = retail_v2alpha.MerchantCenterAccountLinkServiceAsyncClient()

                # Initialize request argument(s)
                merchant_center_account_link = retail_v2alpha.MerchantCenterAccountLink()
                merchant_center_account_link.merchant_center_account_id = 2730
                merchant_center_account_link.branch_id = "branch_id_value"

                request = retail_v2alpha.CreateMerchantCenterAccountLinkRequest(
                    parent="parent_value",
                    merchant_center_account_link=merchant_center_account_link,
                )

                # Make the request
                operation = client.create_merchant_center_account_link(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.retail_v2alpha.types.CreateMerchantCenterAccountLinkRequest, dict]]):
                The request object. Request for
                [MerchantCenterAccountLinkService.CreateMerchantCenterAccountLink][google.cloud.retail.v2alpha.MerchantCenterAccountLinkService.CreateMerchantCenterAccountLink]
                method.
            parent (:class:`str`):
                Required. The branch resource where this
                MerchantCenterAccountLink will be created. Format:
                ``projects/{PROJECT_NUMBER}/locations/global/catalogs/{CATALOG_ID}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            merchant_center_account_link (:class:`google.cloud.retail_v2alpha.types.MerchantCenterAccountLink`):
                Required. The
                [MerchantCenterAccountLink][google.cloud.retail.v2alpha.MerchantCenterAccountLink]
                to create.

                If the caller does not have permission to create the
                [MerchantCenterAccountLink][google.cloud.retail.v2alpha.MerchantCenterAccountLink],
                regardless of whether or not it exists, a
                PERMISSION_DENIED error is returned.

                This corresponds to the ``merchant_center_account_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2alpha.types.MerchantCenterAccountLink` Represents a link between a Merchant Center account and a branch.
                   After a link is established, products from the linked
                   Merchant Center account are streamed to the linked
                   branch.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, merchant_center_account_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            merchant_center_account_link_service.CreateMerchantCenterAccountLinkRequest,
        ):
            request = merchant_center_account_link_service.CreateMerchantCenterAccountLinkRequest(
                request
            )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if merchant_center_account_link is not None:
            request.merchant_center_account_link = merchant_center_account_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.create_merchant_center_account_link
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

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
            gcr_merchant_center_account_link.MerchantCenterAccountLink,
            metadata_type=gcr_merchant_center_account_link.CreateMerchantCenterAccountLinkMetadata,
        )

        # Done; return the response.
        return response

    async def delete_merchant_center_account_link(
        self,
        request: Optional[
            Union[
                merchant_center_account_link_service.DeleteMerchantCenterAccountLinkRequest,
                dict,
            ]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes a
        [MerchantCenterAccountLink][google.cloud.retail.v2alpha.MerchantCenterAccountLink].
        If the
        [MerchantCenterAccountLink][google.cloud.retail.v2alpha.MerchantCenterAccountLink]
        to delete does not exist, a NOT_FOUND error is returned.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import retail_v2alpha

            async def sample_delete_merchant_center_account_link():
                # Create a client
                client = retail_v2alpha.MerchantCenterAccountLinkServiceAsyncClient()

                # Initialize request argument(s)
                request = retail_v2alpha.DeleteMerchantCenterAccountLinkRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_merchant_center_account_link(request=request)

        Args:
            request (Optional[Union[google.cloud.retail_v2alpha.types.DeleteMerchantCenterAccountLinkRequest, dict]]):
                The request object. Request for
                [MerchantCenterAccountLinkService.DeleteMerchantCenterAccountLink][google.cloud.retail.v2alpha.MerchantCenterAccountLinkService.DeleteMerchantCenterAccountLink]
                method.
            name (:class:`str`):
                Required. Full resource name. Format:
                ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/merchantCenterAccountLinks/{merchant_center_account_link_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request,
            merchant_center_account_link_service.DeleteMerchantCenterAccountLinkRequest,
        ):
            request = merchant_center_account_link_service.DeleteMerchantCenterAccountLinkRequest(
                request
            )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.delete_merchant_center_account_link
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self.transport._wrapped_methods[self._client._transport.list_operations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self.transport._wrapped_methods[self._client._transport.get_operation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "MerchantCenterAccountLinkServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("MerchantCenterAccountLinkServiceAsyncClient",)
