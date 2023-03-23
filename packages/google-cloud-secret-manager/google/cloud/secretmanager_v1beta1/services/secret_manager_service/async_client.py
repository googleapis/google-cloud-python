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

from google.cloud.secretmanager_v1beta1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.secretmanager_v1beta1.services.secret_manager_service import pagers
from google.cloud.secretmanager_v1beta1.types import resources, service

from .client import SecretManagerServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, SecretManagerServiceTransport
from .transports.grpc_asyncio import SecretManagerServiceGrpcAsyncIOTransport


class SecretManagerServiceAsyncClient:
    """Secret Manager Service

    Manages secrets and operations using those secrets. Implements a
    REST model with the following objects:

    -  [Secret][google.cloud.secrets.v1beta1.Secret]
    -  [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion]
    """

    _client: SecretManagerServiceClient

    DEFAULT_ENDPOINT = SecretManagerServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SecretManagerServiceClient.DEFAULT_MTLS_ENDPOINT

    secret_path = staticmethod(SecretManagerServiceClient.secret_path)
    parse_secret_path = staticmethod(SecretManagerServiceClient.parse_secret_path)
    secret_version_path = staticmethod(SecretManagerServiceClient.secret_version_path)
    parse_secret_version_path = staticmethod(
        SecretManagerServiceClient.parse_secret_version_path
    )
    common_billing_account_path = staticmethod(
        SecretManagerServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        SecretManagerServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(SecretManagerServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        SecretManagerServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        SecretManagerServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        SecretManagerServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(SecretManagerServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        SecretManagerServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(SecretManagerServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        SecretManagerServiceClient.parse_common_location_path
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
            SecretManagerServiceAsyncClient: The constructed client.
        """
        return SecretManagerServiceClient.from_service_account_info.__func__(SecretManagerServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            SecretManagerServiceAsyncClient: The constructed client.
        """
        return SecretManagerServiceClient.from_service_account_file.__func__(SecretManagerServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return SecretManagerServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> SecretManagerServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            SecretManagerServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(SecretManagerServiceClient).get_transport_class,
        type(SecretManagerServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, SecretManagerServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the secret manager service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SecretManagerServiceTransport]): The
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
        self._client = SecretManagerServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_secrets(
        self,
        request: Optional[Union[service.ListSecretsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSecretsAsyncPager:
        r"""Lists [Secrets][google.cloud.secrets.v1beta1.Secret].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_list_secrets():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.ListSecretsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_secrets(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.ListSecretsRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.ListSecrets][google.cloud.secrets.v1beta1.SecretManagerService.ListSecrets].
            parent (:class:`str`):
                Required. The resource name of the project associated
                with the [Secrets][google.cloud.secrets.v1beta1.Secret],
                in the format ``projects/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.secretmanager_v1beta1.services.secret_manager_service.pagers.ListSecretsAsyncPager:
                Response message for
                [SecretManagerService.ListSecrets][google.cloud.secrets.v1beta1.SecretManagerService.ListSecrets].

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

        request = service.ListSecretsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_secrets,
            default_timeout=60.0,
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
        response = pagers.ListSecretsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_secret(
        self,
        request: Optional[Union[service.CreateSecretRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        secret_id: Optional[str] = None,
        secret: Optional[resources.Secret] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Secret:
        r"""Creates a new [Secret][google.cloud.secrets.v1beta1.Secret]
        containing no
        [SecretVersions][google.cloud.secrets.v1beta1.SecretVersion].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_create_secret():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.CreateSecretRequest(
                    parent="parent_value",
                    secret_id="secret_id_value",
                )

                # Make the request
                response = await client.create_secret(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.CreateSecretRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.CreateSecret][google.cloud.secrets.v1beta1.SecretManagerService.CreateSecret].
            parent (:class:`str`):
                Required. The resource name of the project to associate
                with the [Secret][google.cloud.secrets.v1beta1.Secret],
                in the format ``projects/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            secret_id (:class:`str`):
                Required. This must be unique within the project.

                A secret ID is a string with a maximum length of 255
                characters and can contain uppercase and lowercase
                letters, numerals, and the hyphen (``-``) and underscore
                (``_``) characters.

                This corresponds to the ``secret_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            secret (:class:`google.cloud.secretmanager_v1beta1.types.Secret`):
                Required. A
                [Secret][google.cloud.secrets.v1beta1.Secret] with
                initial field values.

                This corresponds to the ``secret`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.secretmanager_v1beta1.types.Secret:
                A [Secret][google.cloud.secrets.v1beta1.Secret] is a logical secret whose value and versions can
                   be accessed.

                   A [Secret][google.cloud.secrets.v1beta1.Secret] is
                   made up of zero or more
                   [SecretVersions][google.cloud.secrets.v1beta1.SecretVersion]
                   that represent the secret data.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, secret_id, secret])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.CreateSecretRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if secret_id is not None:
            request.secret_id = secret_id
        if secret is not None:
            request.secret = secret

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_secret,
            default_timeout=60.0,
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

    async def add_secret_version(
        self,
        request: Optional[Union[service.AddSecretVersionRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        payload: Optional[resources.SecretPayload] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.SecretVersion:
        r"""Creates a new
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion]
        containing secret data and attaches it to an existing
        [Secret][google.cloud.secrets.v1beta1.Secret].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_add_secret_version():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.AddSecretVersionRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.add_secret_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.AddSecretVersionRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.AddSecretVersion][google.cloud.secrets.v1beta1.SecretManagerService.AddSecretVersion].
            parent (:class:`str`):
                Required. The resource name of the
                [Secret][google.cloud.secrets.v1beta1.Secret] to
                associate with the
                [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion]
                in the format ``projects/*/secrets/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            payload (:class:`google.cloud.secretmanager_v1beta1.types.SecretPayload`):
                Required. The secret payload of the
                [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

                This corresponds to the ``payload`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.secretmanager_v1beta1.types.SecretVersion:
                A secret version resource in the
                Secret Manager API.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, payload])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.AddSecretVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if payload is not None:
            request.payload = payload

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.add_secret_version,
            default_timeout=60.0,
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

    async def get_secret(
        self,
        request: Optional[Union[service.GetSecretRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Secret:
        r"""Gets metadata for a given
        [Secret][google.cloud.secrets.v1beta1.Secret].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_get_secret():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.GetSecretRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_secret(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.GetSecretRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.GetSecret][google.cloud.secrets.v1beta1.SecretManagerService.GetSecret].
            name (:class:`str`):
                Required. The resource name of the
                [Secret][google.cloud.secrets.v1beta1.Secret], in the
                format ``projects/*/secrets/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.secretmanager_v1beta1.types.Secret:
                A [Secret][google.cloud.secrets.v1beta1.Secret] is a logical secret whose value and versions can
                   be accessed.

                   A [Secret][google.cloud.secrets.v1beta1.Secret] is
                   made up of zero or more
                   [SecretVersions][google.cloud.secrets.v1beta1.SecretVersion]
                   that represent the secret data.

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

        request = service.GetSecretRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_secret,
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

    async def update_secret(
        self,
        request: Optional[Union[service.UpdateSecretRequest, dict]] = None,
        *,
        secret: Optional[resources.Secret] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Secret:
        r"""Updates metadata of an existing
        [Secret][google.cloud.secrets.v1beta1.Secret].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_update_secret():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.UpdateSecretRequest(
                )

                # Make the request
                response = await client.update_secret(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.UpdateSecretRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.UpdateSecret][google.cloud.secrets.v1beta1.SecretManagerService.UpdateSecret].
            secret (:class:`google.cloud.secretmanager_v1beta1.types.Secret`):
                Required. [Secret][google.cloud.secrets.v1beta1.Secret]
                with updated field values.

                This corresponds to the ``secret`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Specifies the fields to be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.secretmanager_v1beta1.types.Secret:
                A [Secret][google.cloud.secrets.v1beta1.Secret] is a logical secret whose value and versions can
                   be accessed.

                   A [Secret][google.cloud.secrets.v1beta1.Secret] is
                   made up of zero or more
                   [SecretVersions][google.cloud.secrets.v1beta1.SecretVersion]
                   that represent the secret data.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([secret, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.UpdateSecretRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if secret is not None:
            request.secret = secret
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_secret,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("secret.name", request.secret.name),)
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

    async def delete_secret(
        self,
        request: Optional[Union[service.DeleteSecretRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a [Secret][google.cloud.secrets.v1beta1.Secret].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_delete_secret():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.DeleteSecretRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_secret(request=request)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.DeleteSecretRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.DeleteSecret][google.cloud.secrets.v1beta1.SecretManagerService.DeleteSecret].
            name (:class:`str`):
                Required. The resource name of the
                [Secret][google.cloud.secrets.v1beta1.Secret] to delete
                in the format ``projects/*/secrets/*``.

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

        request = service.DeleteSecretRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_secret,
            default_timeout=60.0,
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

    async def list_secret_versions(
        self,
        request: Optional[Union[service.ListSecretVersionsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSecretVersionsAsyncPager:
        r"""Lists
        [SecretVersions][google.cloud.secrets.v1beta1.SecretVersion].
        This call does not return secret data.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_list_secret_versions():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.ListSecretVersionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_secret_versions(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.ListSecretVersionsRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.ListSecretVersions][google.cloud.secrets.v1beta1.SecretManagerService.ListSecretVersions].
            parent (:class:`str`):
                Required. The resource name of the
                [Secret][google.cloud.secrets.v1beta1.Secret] associated
                with the
                [SecretVersions][google.cloud.secrets.v1beta1.SecretVersion]
                to list, in the format ``projects/*/secrets/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.secretmanager_v1beta1.services.secret_manager_service.pagers.ListSecretVersionsAsyncPager:
                Response message for
                [SecretManagerService.ListSecretVersions][google.cloud.secrets.v1beta1.SecretManagerService.ListSecretVersions].

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

        request = service.ListSecretVersionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_secret_versions,
            default_timeout=60.0,
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
        response = pagers.ListSecretVersionsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_secret_version(
        self,
        request: Optional[Union[service.GetSecretVersionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.SecretVersion:
        r"""Gets metadata for a
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        ``projects/*/secrets/*/versions/latest`` is an alias to the
        ``latest``
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_get_secret_version():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.GetSecretVersionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_secret_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.GetSecretVersionRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.GetSecretVersion][google.cloud.secrets.v1beta1.SecretManagerService.GetSecretVersion].
            name (:class:`str`):
                Required. The resource name of the
                [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion]
                in the format ``projects/*/secrets/*/versions/*``.
                ``projects/*/secrets/*/versions/latest`` is an alias to
                the ``latest``
                [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.secretmanager_v1beta1.types.SecretVersion:
                A secret version resource in the
                Secret Manager API.

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

        request = service.GetSecretVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_secret_version,
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

    async def access_secret_version(
        self,
        request: Optional[Union[service.AccessSecretVersionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.AccessSecretVersionResponse:
        r"""Accesses a
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].
        This call returns the secret data.

        ``projects/*/secrets/*/versions/latest`` is an alias to the
        ``latest``
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_access_secret_version():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.AccessSecretVersionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.access_secret_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.AccessSecretVersionRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.AccessSecretVersion][google.cloud.secrets.v1beta1.SecretManagerService.AccessSecretVersion].
            name (:class:`str`):
                Required. The resource name of the
                [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion]
                in the format ``projects/*/secrets/*/versions/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.secretmanager_v1beta1.types.AccessSecretVersionResponse:
                Response message for
                [SecretManagerService.AccessSecretVersion][google.cloud.secrets.v1beta1.SecretManagerService.AccessSecretVersion].

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

        request = service.AccessSecretVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.access_secret_version,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                    core_exceptions.Unknown,
                ),
                deadline=60.0,
            ),
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

    async def disable_secret_version(
        self,
        request: Optional[Union[service.DisableSecretVersionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.SecretVersion:
        r"""Disables a
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        Sets the
        [state][google.cloud.secrets.v1beta1.SecretVersion.state] of the
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion] to
        [DISABLED][google.cloud.secrets.v1beta1.SecretVersion.State.DISABLED].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_disable_secret_version():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.DisableSecretVersionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.disable_secret_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.DisableSecretVersionRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.DisableSecretVersion][google.cloud.secrets.v1beta1.SecretManagerService.DisableSecretVersion].
            name (:class:`str`):
                Required. The resource name of the
                [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion]
                to disable in the format
                ``projects/*/secrets/*/versions/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.secretmanager_v1beta1.types.SecretVersion:
                A secret version resource in the
                Secret Manager API.

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

        request = service.DisableSecretVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.disable_secret_version,
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

    async def enable_secret_version(
        self,
        request: Optional[Union[service.EnableSecretVersionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.SecretVersion:
        r"""Enables a
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        Sets the
        [state][google.cloud.secrets.v1beta1.SecretVersion.state] of the
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion] to
        [ENABLED][google.cloud.secrets.v1beta1.SecretVersion.State.ENABLED].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_enable_secret_version():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.EnableSecretVersionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.enable_secret_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.EnableSecretVersionRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.EnableSecretVersion][google.cloud.secrets.v1beta1.SecretManagerService.EnableSecretVersion].
            name (:class:`str`):
                Required. The resource name of the
                [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion]
                to enable in the format
                ``projects/*/secrets/*/versions/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.secretmanager_v1beta1.types.SecretVersion:
                A secret version resource in the
                Secret Manager API.

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

        request = service.EnableSecretVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.enable_secret_version,
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

    async def destroy_secret_version(
        self,
        request: Optional[Union[service.DestroySecretVersionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.SecretVersion:
        r"""Destroys a
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion].

        Sets the
        [state][google.cloud.secrets.v1beta1.SecretVersion.state] of the
        [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion] to
        [DESTROYED][google.cloud.secrets.v1beta1.SecretVersion.State.DESTROYED]
        and irrevocably destroys the secret data.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1

            async def sample_destroy_secret_version():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = secretmanager_v1beta1.DestroySecretVersionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.destroy_secret_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.secretmanager_v1beta1.types.DestroySecretVersionRequest, dict]]):
                The request object. Request message for
                [SecretManagerService.DestroySecretVersion][google.cloud.secrets.v1beta1.SecretManagerService.DestroySecretVersion].
            name (:class:`str`):
                Required. The resource name of the
                [SecretVersion][google.cloud.secrets.v1beta1.SecretVersion]
                to destroy in the format
                ``projects/*/secrets/*/versions/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.secretmanager_v1beta1.types.SecretVersion:
                A secret version resource in the
                Secret Manager API.

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

        request = service.DestroySecretVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.destroy_secret_version,
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

    async def set_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.SetIamPolicyRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the access control policy on the specified secret. Replaces
        any existing policy.

        Permissions on
        [SecretVersions][google.cloud.secrets.v1beta1.SecretVersion] are
        enforced according to the policy set on the associated
        [Secret][google.cloud.secrets.v1beta1.Secret].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            async def sample_set_iam_policy():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.SetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = await client.set_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]]):
                The request object. Request message for ``SetIamPolicy`` method.
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
            default_timeout=60.0,
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

    async def get_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.GetIamPolicyRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the access control policy for a secret.
        Returns empty policy if the secret exists and does not
        have a policy set.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            async def sample_get_iam_policy():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.GetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = await client.get_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]]):
                The request object. Request message for ``GetIamPolicy`` method.
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
            default_timeout=60.0,
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
        request: Optional[Union[iam_policy_pb2.TestIamPermissionsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns permissions that a caller has for the specified secret.
        If the secret does not exist, this call returns an empty set of
        permissions, not a NOT_FOUND error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for
        authorization checking. This operation may "fail open" without
        warning.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import secretmanager_v1beta1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            async def sample_test_iam_permissions():
                # Create a client
                client = secretmanager_v1beta1.SecretManagerServiceAsyncClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.TestIamPermissionsRequest(
                    resource="resource_value",
                    permissions=['permissions_value1', 'permissions_value2'],
                )

                # Make the request
                response = await client.test_iam_permissions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]]):
                The request object. Request message for ``TestIamPermissions`` method.
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
            default_timeout=60.0,
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


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("SecretManagerServiceAsyncClient",)
