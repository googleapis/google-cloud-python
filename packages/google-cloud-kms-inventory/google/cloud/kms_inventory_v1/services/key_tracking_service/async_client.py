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

from google.cloud.kms_inventory_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.kms_inventory_v1.services.key_tracking_service import pagers
from google.cloud.kms_inventory_v1.types import key_tracking_service

from .client import KeyTrackingServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, KeyTrackingServiceTransport
from .transports.grpc_asyncio import KeyTrackingServiceGrpcAsyncIOTransport


class KeyTrackingServiceAsyncClient:
    """Returns information about the resources in an org that are
    protected by a given Cloud KMS key via CMEK.
    """

    _client: KeyTrackingServiceClient

    DEFAULT_ENDPOINT = KeyTrackingServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = KeyTrackingServiceClient.DEFAULT_MTLS_ENDPOINT

    asset_path = staticmethod(KeyTrackingServiceClient.asset_path)
    parse_asset_path = staticmethod(KeyTrackingServiceClient.parse_asset_path)
    crypto_key_version_path = staticmethod(
        KeyTrackingServiceClient.crypto_key_version_path
    )
    parse_crypto_key_version_path = staticmethod(
        KeyTrackingServiceClient.parse_crypto_key_version_path
    )
    protected_resources_summary_path = staticmethod(
        KeyTrackingServiceClient.protected_resources_summary_path
    )
    parse_protected_resources_summary_path = staticmethod(
        KeyTrackingServiceClient.parse_protected_resources_summary_path
    )
    common_billing_account_path = staticmethod(
        KeyTrackingServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        KeyTrackingServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(KeyTrackingServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        KeyTrackingServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        KeyTrackingServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        KeyTrackingServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(KeyTrackingServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        KeyTrackingServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(KeyTrackingServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        KeyTrackingServiceClient.parse_common_location_path
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
            KeyTrackingServiceAsyncClient: The constructed client.
        """
        return KeyTrackingServiceClient.from_service_account_info.__func__(KeyTrackingServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            KeyTrackingServiceAsyncClient: The constructed client.
        """
        return KeyTrackingServiceClient.from_service_account_file.__func__(KeyTrackingServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return KeyTrackingServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> KeyTrackingServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            KeyTrackingServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(KeyTrackingServiceClient).get_transport_class,
        type(KeyTrackingServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, KeyTrackingServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the key tracking service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.KeyTrackingServiceTransport]): The
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
        self._client = KeyTrackingServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_protected_resources_summary(
        self,
        request: Optional[
            Union[key_tracking_service.GetProtectedResourcesSummaryRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> key_tracking_service.ProtectedResourcesSummary:
        r"""Returns aggregate information about the resources protected by
        the given Cloud KMS [CryptoKey][google.cloud.kms.v1.CryptoKey].
        Only resources within the same Cloud organization as the key
        will be returned. The project that holds the key must be part of
        an organization in order for this call to succeed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import kms_inventory_v1

            async def sample_get_protected_resources_summary():
                # Create a client
                client = kms_inventory_v1.KeyTrackingServiceAsyncClient()

                # Initialize request argument(s)
                request = kms_inventory_v1.GetProtectedResourcesSummaryRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_protected_resources_summary(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.kms_inventory_v1.types.GetProtectedResourcesSummaryRequest, dict]]):
                The request object. Request message for
                [KeyTrackingService.GetProtectedResourcesSummary][google.cloud.kms.inventory.v1.KeyTrackingService.GetProtectedResourcesSummary].
            name (:class:`str`):
                Required. The resource name of the
                [CryptoKey][google.cloud.kms.v1.CryptoKey].

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.kms_inventory_v1.types.ProtectedResourcesSummary:
                Aggregate information about the
                resources protected by a Cloud KMS key
                in the same Cloud organization as the
                key.

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

        request = key_tracking_service.GetProtectedResourcesSummaryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_protected_resources_summary,
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

    async def search_protected_resources(
        self,
        request: Optional[
            Union[key_tracking_service.SearchProtectedResourcesRequest, dict]
        ] = None,
        *,
        scope: Optional[str] = None,
        crypto_key: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchProtectedResourcesAsyncPager:
        r"""Returns metadata about the resources protected by the given
        Cloud KMS [CryptoKey][google.cloud.kms.v1.CryptoKey] in the
        given Cloud organization.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import kms_inventory_v1

            async def sample_search_protected_resources():
                # Create a client
                client = kms_inventory_v1.KeyTrackingServiceAsyncClient()

                # Initialize request argument(s)
                request = kms_inventory_v1.SearchProtectedResourcesRequest(
                    scope="scope_value",
                    crypto_key="crypto_key_value",
                )

                # Make the request
                page_result = client.search_protected_resources(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.kms_inventory_v1.types.SearchProtectedResourcesRequest, dict]]):
                The request object. Request message for
                [KeyTrackingService.SearchProtectedResources][google.cloud.kms.inventory.v1.KeyTrackingService.SearchProtectedResources].
            scope (:class:`str`):
                Required. Resource name of the
                organization. Example: organizations/123

                This corresponds to the ``scope`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            crypto_key (:class:`str`):
                Required. The resource name of the
                [CryptoKey][google.cloud.kms.v1.CryptoKey].

                This corresponds to the ``crypto_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.kms_inventory_v1.services.key_tracking_service.pagers.SearchProtectedResourcesAsyncPager:
                Response message for
                   [KeyTrackingService.SearchProtectedResources][google.cloud.kms.inventory.v1.KeyTrackingService.SearchProtectedResources].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([scope, crypto_key])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = key_tracking_service.SearchProtectedResourcesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if scope is not None:
            request.scope = scope
        if crypto_key is not None:
            request.crypto_key = crypto_key

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_protected_resources,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("scope", request.scope),)),
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
        response = pagers.SearchProtectedResourcesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "KeyTrackingServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("KeyTrackingServiceAsyncClient",)
