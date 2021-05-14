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
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.appengine_admin_v1.services.authorized_certificates import pagers
from google.cloud.appengine_admin_v1.types import appengine
from google.cloud.appengine_admin_v1.types import certificate
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import AuthorizedCertificatesTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import AuthorizedCertificatesGrpcAsyncIOTransport
from .client import AuthorizedCertificatesClient


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
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, AuthorizedCertificatesTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
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
        request: appengine.ListAuthorizedCertificatesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAuthorizedCertificatesAsyncPager:
        r"""Lists all SSL certificates the user is authorized to
        administer.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.ListAuthorizedCertificatesRequest`):
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListAuthorizedCertificatesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_authorized_certificate(
        self,
        request: appengine.GetAuthorizedCertificateRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate.AuthorizedCertificate:
        r"""Gets the specified SSL certificate.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.GetAuthorizedCertificateRequest`):
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_authorized_certificate(
        self,
        request: appengine.CreateAuthorizedCertificateRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate.AuthorizedCertificate:
        r"""Uploads the specified SSL certificate.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.CreateAuthorizedCertificateRequest`):
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_authorized_certificate(
        self,
        request: appengine.UpdateAuthorizedCertificateRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate.AuthorizedCertificate:
        r"""Updates the specified SSL certificate. To renew a certificate
        and maintain its existing domain mappings, update
        ``certificate_data`` with a new certificate. The new certificate
        must be applicable to the same domains as the original
        certificate. The certificate ``display_name`` may also be
        updated.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.UpdateAuthorizedCertificateRequest`):
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_authorized_certificate(
        self,
        request: appengine.DeleteAuthorizedCertificateRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified SSL certificate.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.DeleteAuthorizedCertificateRequest`):
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
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-appengine-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("AuthorizedCertificatesAsyncClient",)
