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

from google.iam.credentials_v1.types import common
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import IAMCredentialsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import IAMCredentialsGrpcAsyncIOTransport
from .client import IAMCredentialsClient


class IAMCredentialsAsyncClient:
    """A service account is a special type of Google account that
    belongs to your application or a virtual machine (VM), instead
    of to an individual end user. Your application assumes the
    identity of the service account to call Google APIs, so that the
    users aren't directly involved.

    Service account credentials are used to temporarily assume the
    identity of the service account. Supported credential types
    include OAuth 2.0 access tokens, OpenID Connect ID tokens,
    self-signed JSON Web Tokens (JWTs), and more.
    """

    _client: IAMCredentialsClient

    DEFAULT_ENDPOINT = IAMCredentialsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = IAMCredentialsClient.DEFAULT_MTLS_ENDPOINT

    service_account_path = staticmethod(IAMCredentialsClient.service_account_path)
    parse_service_account_path = staticmethod(IAMCredentialsClient.parse_service_account_path)
    common_billing_account_path = staticmethod(IAMCredentialsClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(IAMCredentialsClient.parse_common_billing_account_path)
    common_folder_path = staticmethod(IAMCredentialsClient.common_folder_path)
    parse_common_folder_path = staticmethod(IAMCredentialsClient.parse_common_folder_path)
    common_organization_path = staticmethod(IAMCredentialsClient.common_organization_path)
    parse_common_organization_path = staticmethod(IAMCredentialsClient.parse_common_organization_path)
    common_project_path = staticmethod(IAMCredentialsClient.common_project_path)
    parse_common_project_path = staticmethod(IAMCredentialsClient.parse_common_project_path)
    common_location_path = staticmethod(IAMCredentialsClient.common_location_path)
    parse_common_location_path = staticmethod(IAMCredentialsClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            IAMCredentialsAsyncClient: The constructed client.
        """
        return IAMCredentialsClient.from_service_account_info.__func__(IAMCredentialsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            IAMCredentialsAsyncClient: The constructed client.
        """
        return IAMCredentialsClient.from_service_account_file.__func__(IAMCredentialsAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return IAMCredentialsClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> IAMCredentialsTransport:
        """Returns the transport used by the client instance.

        Returns:
            IAMCredentialsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(type(IAMCredentialsClient).get_transport_class, type(IAMCredentialsClient))

    def __init__(self, *,
            credentials: ga_credentials.Credentials = None,
            transport: Union[str, IAMCredentialsTransport] = "grpc_asyncio",
            client_options: ClientOptions = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiates the iam credentials client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.IAMCredentialsTransport]): The
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
        self._client = IAMCredentialsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,

        )

    async def generate_access_token(self,
            request: Union[common.GenerateAccessTokenRequest, dict] = None,
            *,
            name: str = None,
            delegates: Sequence[str] = None,
            scope: Sequence[str] = None,
            lifetime: duration_pb2.Duration = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> common.GenerateAccessTokenResponse:
        r"""Generates an OAuth 2.0 access token for a service
        account.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.iam import credentials_v1

            async def sample_generate_access_token():
                # Create a client
                client = credentials_v1.IAMCredentialsAsyncClient()

                # Initialize request argument(s)
                request = credentials_v1.GenerateAccessTokenRequest(
                    name="name_value",
                    scope=['scope_value1', 'scope_value2'],
                )

                # Make the request
                response = await client.generate_access_token(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.credentials_v1.types.GenerateAccessTokenRequest, dict]):
                The request object.
            name (:class:`str`):
                Required. The resource name of the service account for
                which the credentials are requested, in the following
                format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``.
                The ``-`` wildcard character is required; replacing it
                with a project ID is invalid.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            delegates (:class:`Sequence[str]`):
                The sequence of service accounts in a delegation chain.
                Each service account must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on its
                next service account in the chain. The last service
                account in the chain must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on the
                service account that is specified in the ``name`` field
                of the request.

                The delegates must have the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``.
                The ``-`` wildcard character is required; replacing it
                with a project ID is invalid.

                This corresponds to the ``delegates`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            scope (:class:`Sequence[str]`):
                Required. Code to identify the scopes
                to be included in the OAuth 2.0 access
                token. See
                https://developers.google.com/identity/protocols/googlescopes
                for more information.
                At least one value required.

                This corresponds to the ``scope`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            lifetime (:class:`google.protobuf.duration_pb2.Duration`):
                The desired lifetime duration of the
                access token in seconds. Must be set to
                a value less than or equal to 3600 (1
                hour). If a value is not specified, the
                token's lifetime will be set to a
                default value of one hour.

                This corresponds to the ``lifetime`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.credentials_v1.types.GenerateAccessTokenResponse:

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, delegates, scope, lifetime])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = common.GenerateAccessTokenRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if lifetime is not None:
            request.lifetime = lifetime
        if delegates:
            request.delegates.extend(delegates)
        if scope:
            request.scope.extend(scope)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.generate_access_token,
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

    async def generate_id_token(self,
            request: Union[common.GenerateIdTokenRequest, dict] = None,
            *,
            name: str = None,
            delegates: Sequence[str] = None,
            audience: str = None,
            include_email: bool = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> common.GenerateIdTokenResponse:
        r"""Generates an OpenID Connect ID token for a service
        account.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.iam import credentials_v1

            async def sample_generate_id_token():
                # Create a client
                client = credentials_v1.IAMCredentialsAsyncClient()

                # Initialize request argument(s)
                request = credentials_v1.GenerateIdTokenRequest(
                    name="name_value",
                    audience="audience_value",
                )

                # Make the request
                response = await client.generate_id_token(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.credentials_v1.types.GenerateIdTokenRequest, dict]):
                The request object.
            name (:class:`str`):
                Required. The resource name of the service account for
                which the credentials are requested, in the following
                format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``.
                The ``-`` wildcard character is required; replacing it
                with a project ID is invalid.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            delegates (:class:`Sequence[str]`):
                The sequence of service accounts in a delegation chain.
                Each service account must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on its
                next service account in the chain. The last service
                account in the chain must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on the
                service account that is specified in the ``name`` field
                of the request.

                The delegates must have the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``.
                The ``-`` wildcard character is required; replacing it
                with a project ID is invalid.

                This corresponds to the ``delegates`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            audience (:class:`str`):
                Required. The audience for the token,
                such as the API or account that this
                token grants access to.

                This corresponds to the ``audience`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            include_email (:class:`bool`):
                Include the service account email in the token. If set
                to ``true``, the token will contain ``email`` and
                ``email_verified`` claims.

                This corresponds to the ``include_email`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.credentials_v1.types.GenerateIdTokenResponse:

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, delegates, audience, include_email])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = common.GenerateIdTokenRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if audience is not None:
            request.audience = audience
        if include_email is not None:
            request.include_email = include_email
        if delegates:
            request.delegates.extend(delegates)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.generate_id_token,
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

    async def sign_blob(self,
            request: Union[common.SignBlobRequest, dict] = None,
            *,
            name: str = None,
            delegates: Sequence[str] = None,
            payload: bytes = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> common.SignBlobResponse:
        r"""Signs a blob using a service account's system-managed
        private key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.iam import credentials_v1

            async def sample_sign_blob():
                # Create a client
                client = credentials_v1.IAMCredentialsAsyncClient()

                # Initialize request argument(s)
                request = credentials_v1.SignBlobRequest(
                    name="name_value",
                    payload=b'payload_blob',
                )

                # Make the request
                response = await client.sign_blob(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.credentials_v1.types.SignBlobRequest, dict]):
                The request object.
            name (:class:`str`):
                Required. The resource name of the service account for
                which the credentials are requested, in the following
                format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``.
                The ``-`` wildcard character is required; replacing it
                with a project ID is invalid.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            delegates (:class:`Sequence[str]`):
                The sequence of service accounts in a delegation chain.
                Each service account must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on its
                next service account in the chain. The last service
                account in the chain must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on the
                service account that is specified in the ``name`` field
                of the request.

                The delegates must have the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``.
                The ``-`` wildcard character is required; replacing it
                with a project ID is invalid.

                This corresponds to the ``delegates`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            payload (:class:`bytes`):
                Required. The bytes to sign.
                This corresponds to the ``payload`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.credentials_v1.types.SignBlobResponse:

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, delegates, payload])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = common.SignBlobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if payload is not None:
            request.payload = payload
        if delegates:
            request.delegates.extend(delegates)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.sign_blob,
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

    async def sign_jwt(self,
            request: Union[common.SignJwtRequest, dict] = None,
            *,
            name: str = None,
            delegates: Sequence[str] = None,
            payload: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> common.SignJwtResponse:
        r"""Signs a JWT using a service account's system-managed
        private key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.iam import credentials_v1

            async def sample_sign_jwt():
                # Create a client
                client = credentials_v1.IAMCredentialsAsyncClient()

                # Initialize request argument(s)
                request = credentials_v1.SignJwtRequest(
                    name="name_value",
                    payload="payload_value",
                )

                # Make the request
                response = await client.sign_jwt(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.credentials_v1.types.SignJwtRequest, dict]):
                The request object.
            name (:class:`str`):
                Required. The resource name of the service account for
                which the credentials are requested, in the following
                format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``.
                The ``-`` wildcard character is required; replacing it
                with a project ID is invalid.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            delegates (:class:`Sequence[str]`):
                The sequence of service accounts in a delegation chain.
                Each service account must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on its
                next service account in the chain. The last service
                account in the chain must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on the
                service account that is specified in the ``name`` field
                of the request.

                The delegates must have the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``.
                The ``-`` wildcard character is required; replacing it
                with a project ID is invalid.

                This corresponds to the ``delegates`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            payload (:class:`str`):
                Required. The JWT payload to sign: a
                JSON object that contains a JWT Claims
                Set.

                This corresponds to the ``payload`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.credentials_v1.types.SignJwtResponse:

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, delegates, payload])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = common.SignJwtRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if payload is not None:
            request.payload = payload
        if delegates:
            request.delegates.extend(delegates)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.sign_jwt,
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-iam-credentials",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = (
    "IAMCredentialsAsyncClient",
)
