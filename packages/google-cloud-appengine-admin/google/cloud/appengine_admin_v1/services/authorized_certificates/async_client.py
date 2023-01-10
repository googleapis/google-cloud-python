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

from google.cloud.appengine_admin_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.appengine_admin_v1.services.authorized_certificates import pagers
from google.cloud.appengine_admin_v1.types import appengine, certificate

from .client import AuthorizedCertificatesClient
from .transports.base import DEFAULT_CLIENT_INFO, AuthorizedCertificatesTransport
from .transports.grpc_asyncio import AuthorizedCertificatesGrpcAsyncIOTransport


class AuthorizedCertificatesAsyncClient:
    """Manages SSL certificates a user is authorized to administer.
    A user can administer any SSL certificates applicable to their
    authorized domains.
    """

    _client: AuthorizedCertificatesClient

    DEFAULT_ENDPOINT = AuthorizedCertificatesClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AuthorizedCertificatesClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        AuthorizedCertificatesClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        AuthorizedCertificatesClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AuthorizedCertificatesClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        AuthorizedCertificatesClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        AuthorizedCertificatesClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        AuthorizedCertificatesClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AuthorizedCertificatesClient.common_project_path)
    parse_common_project_path = staticmethod(
        AuthorizedCertificatesClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        AuthorizedCertificatesClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        AuthorizedCertificatesClient.parse_common_location_path
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
            AuthorizedCertificatesAsyncClient: The constructed client.
        """
        return AuthorizedCertificatesClient.from_service_account_info.__func__(AuthorizedCertificatesAsyncClient, info, *args, **kwargs)  # type: ignore

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
            AuthorizedCertificatesAsyncClient: The constructed client.
        """
        return AuthorizedCertificatesClient.from_service_account_file.__func__(AuthorizedCertificatesAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return AuthorizedCertificatesClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> AuthorizedCertificatesTransport:
        """Returns the transport used by the client instance.

        Returns:
            AuthorizedCertificatesTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(AuthorizedCertificatesClient).get_transport_class,
        type(AuthorizedCertificatesClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, AuthorizedCertificatesTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the authorized certificates client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AuthorizedCertificatesTransport]): The
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
        self._client = AuthorizedCertificatesClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_authorized_certificates(
        self,
        request: Optional[
            Union[appengine.ListAuthorizedCertificatesRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAuthorizedCertificatesAsyncPager:
        r"""Lists all SSL certificates the user is authorized to
        administer.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import appengine_admin_v1

            async def sample_list_authorized_certificates():
                # Create a client
                client = appengine_admin_v1.AuthorizedCertificatesAsyncClient()

                # Initialize request argument(s)
                request = appengine_admin_v1.ListAuthorizedCertificatesRequest(
                )

                # Make the request
                page_result = client.list_authorized_certificates(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.appengine_admin_v1.types.ListAuthorizedCertificatesRequest, dict]]):
                The request object. Request message for
                `AuthorizedCertificates.ListAuthorizedCertificates`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.services.authorized_certificates.pagers.ListAuthorizedCertificatesAsyncPager:
                Response message for
                AuthorizedCertificates.ListAuthorizedCertificates.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = appengine.ListAuthorizedCertificatesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_authorized_certificates,
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
        response = pagers.ListAuthorizedCertificatesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_authorized_certificate(
        self,
        request: Optional[
            Union[appengine.GetAuthorizedCertificateRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate.AuthorizedCertificate:
        r"""Gets the specified SSL certificate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import appengine_admin_v1

            async def sample_get_authorized_certificate():
                # Create a client
                client = appengine_admin_v1.AuthorizedCertificatesAsyncClient()

                # Initialize request argument(s)
                request = appengine_admin_v1.GetAuthorizedCertificateRequest(
                )

                # Make the request
                response = await client.get_authorized_certificate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.appengine_admin_v1.types.GetAuthorizedCertificateRequest, dict]]):
                The request object. Request message for
                `AuthorizedCertificates.GetAuthorizedCertificate`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.types.AuthorizedCertificate:
                An SSL certificate that a user has
                been authorized to administer. A user is
                authorized to administer any certificate
                that applies to one of their authorized
                domains.

        """
        # Create or coerce a protobuf request object.
        request = appengine.GetAuthorizedCertificateRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_authorized_certificate,
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

    async def create_authorized_certificate(
        self,
        request: Optional[
            Union[appengine.CreateAuthorizedCertificateRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate.AuthorizedCertificate:
        r"""Uploads the specified SSL certificate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import appengine_admin_v1

            async def sample_create_authorized_certificate():
                # Create a client
                client = appengine_admin_v1.AuthorizedCertificatesAsyncClient()

                # Initialize request argument(s)
                request = appengine_admin_v1.CreateAuthorizedCertificateRequest(
                )

                # Make the request
                response = await client.create_authorized_certificate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.appengine_admin_v1.types.CreateAuthorizedCertificateRequest, dict]]):
                The request object. Request message for
                `AuthorizedCertificates.CreateAuthorizedCertificate`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.types.AuthorizedCertificate:
                An SSL certificate that a user has
                been authorized to administer. A user is
                authorized to administer any certificate
                that applies to one of their authorized
                domains.

        """
        # Create or coerce a protobuf request object.
        request = appengine.CreateAuthorizedCertificateRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_authorized_certificate,
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

    async def update_authorized_certificate(
        self,
        request: Optional[
            Union[appengine.UpdateAuthorizedCertificateRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate.AuthorizedCertificate:
        r"""Updates the specified SSL certificate. To renew a certificate
        and maintain its existing domain mappings, update
        ``certificate_data`` with a new certificate. The new certificate
        must be applicable to the same domains as the original
        certificate. The certificate ``display_name`` may also be
        updated.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import appengine_admin_v1

            async def sample_update_authorized_certificate():
                # Create a client
                client = appengine_admin_v1.AuthorizedCertificatesAsyncClient()

                # Initialize request argument(s)
                request = appengine_admin_v1.UpdateAuthorizedCertificateRequest(
                )

                # Make the request
                response = await client.update_authorized_certificate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.appengine_admin_v1.types.UpdateAuthorizedCertificateRequest, dict]]):
                The request object. Request message for
                `AuthorizedCertificates.UpdateAuthorizedCertificate`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.types.AuthorizedCertificate:
                An SSL certificate that a user has
                been authorized to administer. A user is
                authorized to administer any certificate
                that applies to one of their authorized
                domains.

        """
        # Create or coerce a protobuf request object.
        request = appengine.UpdateAuthorizedCertificateRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_authorized_certificate,
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

    async def delete_authorized_certificate(
        self,
        request: Optional[
            Union[appengine.DeleteAuthorizedCertificateRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified SSL certificate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import appengine_admin_v1

            async def sample_delete_authorized_certificate():
                # Create a client
                client = appengine_admin_v1.AuthorizedCertificatesAsyncClient()

                # Initialize request argument(s)
                request = appengine_admin_v1.DeleteAuthorizedCertificateRequest(
                )

                # Make the request
                await client.delete_authorized_certificate(request=request)

        Args:
            request (Optional[Union[google.cloud.appengine_admin_v1.types.DeleteAuthorizedCertificateRequest, dict]]):
                The request object. Request message for
                `AuthorizedCertificates.DeleteAuthorizedCertificate`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = appengine.DeleteAuthorizedCertificateRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_authorized_certificate,
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("AuthorizedCertificatesAsyncClient",)
