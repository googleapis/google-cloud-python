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

from google.cloud.servicedirectory_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.servicedirectory_v1.types import lookup_service, service

from .client import LookupServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, LookupServiceTransport
from .transports.grpc_asyncio import LookupServiceGrpcAsyncIOTransport


class LookupServiceAsyncClient:
    """Service Directory API for looking up service data at runtime."""

    _client: LookupServiceClient

    DEFAULT_ENDPOINT = LookupServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = LookupServiceClient.DEFAULT_MTLS_ENDPOINT

    endpoint_path = staticmethod(LookupServiceClient.endpoint_path)
    parse_endpoint_path = staticmethod(LookupServiceClient.parse_endpoint_path)
    service_path = staticmethod(LookupServiceClient.service_path)
    parse_service_path = staticmethod(LookupServiceClient.parse_service_path)
    common_billing_account_path = staticmethod(
        LookupServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        LookupServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(LookupServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        LookupServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        LookupServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        LookupServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(LookupServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        LookupServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(LookupServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        LookupServiceClient.parse_common_location_path
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
            LookupServiceAsyncClient: The constructed client.
        """
        return LookupServiceClient.from_service_account_info.__func__(LookupServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            LookupServiceAsyncClient: The constructed client.
        """
        return LookupServiceClient.from_service_account_file.__func__(LookupServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return LookupServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> LookupServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            LookupServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(LookupServiceClient).get_transport_class, type(LookupServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, LookupServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the lookup service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.LookupServiceTransport]): The
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
        self._client = LookupServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def resolve_service(
        self,
        request: Optional[Union[lookup_service.ResolveServiceRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> lookup_service.ResolveServiceResponse:
        r"""Returns a [service][google.cloud.servicedirectory.v1.Service]
        and its associated endpoints. Resolving a service is not
        considered an active developer method.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import servicedirectory_v1

            async def sample_resolve_service():
                # Create a client
                client = servicedirectory_v1.LookupServiceAsyncClient()

                # Initialize request argument(s)
                request = servicedirectory_v1.ResolveServiceRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.resolve_service(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.servicedirectory_v1.types.ResolveServiceRequest, dict]]):
                The request object. The request message for
                [LookupService.ResolveService][google.cloud.servicedirectory.v1.LookupService.ResolveService].
                Looks up a service by its name, returns the service and
                its endpoints.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.servicedirectory_v1.types.ResolveServiceResponse:
                The response message for
                   [LookupService.ResolveService][google.cloud.servicedirectory.v1.LookupService.ResolveService].

        """
        # Create or coerce a protobuf request object.
        request = lookup_service.ResolveServiceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.resolve_service,
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

    async def __aenter__(self) -> "LookupServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("LookupServiceAsyncClient",)
