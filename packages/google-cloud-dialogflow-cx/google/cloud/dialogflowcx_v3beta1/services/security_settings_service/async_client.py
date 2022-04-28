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

from google.cloud.dialogflowcx_v3beta1.services.security_settings_service import pagers
from google.cloud.dialogflowcx_v3beta1.types import security_settings
from google.cloud.dialogflowcx_v3beta1.types import (
    security_settings as gcdc_security_settings,
)
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import SecuritySettingsServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import SecuritySettingsServiceGrpcAsyncIOTransport
from .client import SecuritySettingsServiceClient


class SecuritySettingsServiceAsyncClient:
    """Service for managing security settings for Dialogflow."""

    _client: SecuritySettingsServiceClient

    DEFAULT_ENDPOINT = SecuritySettingsServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SecuritySettingsServiceClient.DEFAULT_MTLS_ENDPOINT

    deidentify_template_path = staticmethod(
        SecuritySettingsServiceClient.deidentify_template_path
    )
    parse_deidentify_template_path = staticmethod(
        SecuritySettingsServiceClient.parse_deidentify_template_path
    )
    inspect_template_path = staticmethod(
        SecuritySettingsServiceClient.inspect_template_path
    )
    parse_inspect_template_path = staticmethod(
        SecuritySettingsServiceClient.parse_inspect_template_path
    )
    security_settings_path = staticmethod(
        SecuritySettingsServiceClient.security_settings_path
    )
    parse_security_settings_path = staticmethod(
        SecuritySettingsServiceClient.parse_security_settings_path
    )
    common_billing_account_path = staticmethod(
        SecuritySettingsServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        SecuritySettingsServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(SecuritySettingsServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        SecuritySettingsServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        SecuritySettingsServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        SecuritySettingsServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        SecuritySettingsServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        SecuritySettingsServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        SecuritySettingsServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        SecuritySettingsServiceClient.parse_common_location_path
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
            SecuritySettingsServiceAsyncClient: The constructed client.
        """
        return SecuritySettingsServiceClient.from_service_account_info.__func__(SecuritySettingsServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            SecuritySettingsServiceAsyncClient: The constructed client.
        """
        return SecuritySettingsServiceClient.from_service_account_file.__func__(SecuritySettingsServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return SecuritySettingsServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> SecuritySettingsServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            SecuritySettingsServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(SecuritySettingsServiceClient).get_transport_class,
        type(SecuritySettingsServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, SecuritySettingsServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the security settings service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SecuritySettingsServiceTransport]): The
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
        self._client = SecuritySettingsServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_security_settings(
        self,
        request: Union[
            gcdc_security_settings.CreateSecuritySettingsRequest, dict
        ] = None,
        *,
        parent: str = None,
        security_settings: gcdc_security_settings.SecuritySettings = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_security_settings.SecuritySettings:
        r"""Create security settings in the specified location.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3beta1

            async def sample_create_security_settings():
                # Create a client
                client = dialogflowcx_v3beta1.SecuritySettingsServiceAsyncClient()

                # Initialize request argument(s)
                security_settings = dialogflowcx_v3beta1.SecuritySettings()
                security_settings.retention_window_days = 2271
                security_settings.display_name = "display_name_value"

                request = dialogflowcx_v3beta1.CreateSecuritySettingsRequest(
                    parent="parent_value",
                    security_settings=security_settings,
                )

                # Make the request
                response = await client.create_security_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.CreateSecuritySettingsRequest, dict]):
                The request object. The request message for
                [SecuritySettings.CreateSecuritySettings][].
            parent (:class:`str`):
                Required. The location to create an
                [SecuritySettings][google.cloud.dialogflow.cx.v3beta1.SecuritySettings]
                for. Format:
                ``projects/<Project ID>/locations/<Location ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_settings (:class:`google.cloud.dialogflowcx_v3beta1.types.SecuritySettings`):
                Required. The security settings to
                create.

                This corresponds to the ``security_settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.SecuritySettings:
                Represents the settings related to
                security issues, such as data redaction
                and data retention. It may take hours
                for updates on the settings to propagate
                to all the related components and take
                effect.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, security_settings])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_security_settings.CreateSecuritySettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if security_settings is not None:
            request.security_settings = security_settings

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_security_settings,
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

    async def get_security_settings(
        self,
        request: Union[security_settings.GetSecuritySettingsRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> security_settings.SecuritySettings:
        r"""Retrieves the specified
        [SecuritySettings][google.cloud.dialogflow.cx.v3beta1.SecuritySettings].
        The returned settings may be stale by up to 1 minute.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3beta1

            async def sample_get_security_settings():
                # Create a client
                client = dialogflowcx_v3beta1.SecuritySettingsServiceAsyncClient()

                # Initialize request argument(s)
                request = dialogflowcx_v3beta1.GetSecuritySettingsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_security_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.GetSecuritySettingsRequest, dict]):
                The request object. The request message for
                [SecuritySettingsService.GetSecuritySettings][google.cloud.dialogflow.cx.v3beta1.SecuritySettingsService.GetSecuritySettings].
            name (:class:`str`):
                Required. Resource name of the settings. Format:
                ``projects/<Project ID>/locations/<Location ID>/securitySettings/<security settings ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.SecuritySettings:
                Represents the settings related to
                security issues, such as data redaction
                and data retention. It may take hours
                for updates on the settings to propagate
                to all the related components and take
                effect.

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

        request = security_settings.GetSecuritySettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_security_settings,
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

    async def update_security_settings(
        self,
        request: Union[
            gcdc_security_settings.UpdateSecuritySettingsRequest, dict
        ] = None,
        *,
        security_settings: gcdc_security_settings.SecuritySettings = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_security_settings.SecuritySettings:
        r"""Updates the specified
        [SecuritySettings][google.cloud.dialogflow.cx.v3beta1.SecuritySettings].

        .. code-block:: python

            from google.cloud import dialogflowcx_v3beta1

            async def sample_update_security_settings():
                # Create a client
                client = dialogflowcx_v3beta1.SecuritySettingsServiceAsyncClient()

                # Initialize request argument(s)
                security_settings = dialogflowcx_v3beta1.SecuritySettings()
                security_settings.retention_window_days = 2271
                security_settings.display_name = "display_name_value"

                request = dialogflowcx_v3beta1.UpdateSecuritySettingsRequest(
                    security_settings=security_settings,
                )

                # Make the request
                response = await client.update_security_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.UpdateSecuritySettingsRequest, dict]):
                The request object. The request message for
                [SecuritySettingsService.UpdateSecuritySettings][google.cloud.dialogflow.cx.v3beta1.SecuritySettingsService.UpdateSecuritySettings].
            security_settings (:class:`google.cloud.dialogflowcx_v3beta1.types.SecuritySettings`):
                Required. [SecuritySettings] object that contains values
                for each of the fields to update.

                This corresponds to the ``security_settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The mask to control which
                fields get updated. If the mask is not
                present, all fields will be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.SecuritySettings:
                Represents the settings related to
                security issues, such as data redaction
                and data retention. It may take hours
                for updates on the settings to propagate
                to all the related components and take
                effect.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([security_settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_security_settings.UpdateSecuritySettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if security_settings is not None:
            request.security_settings = security_settings
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_security_settings,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("security_settings.name", request.security_settings.name),)
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

    async def list_security_settings(
        self,
        request: Union[security_settings.ListSecuritySettingsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSecuritySettingsAsyncPager:
        r"""Returns the list of all security settings in the
        specified location.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3beta1

            async def sample_list_security_settings():
                # Create a client
                client = dialogflowcx_v3beta1.SecuritySettingsServiceAsyncClient()

                # Initialize request argument(s)
                request = dialogflowcx_v3beta1.ListSecuritySettingsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_security_settings(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.ListSecuritySettingsRequest, dict]):
                The request object. The request message for
                [SecuritySettings.ListSecuritySettings][].
            parent (:class:`str`):
                Required. The location to list all security settings
                for. Format:
                ``projects/<Project ID>/locations/<Location ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.services.security_settings_service.pagers.ListSecuritySettingsAsyncPager:
                The response message for
                [SecuritySettings.ListSecuritySettings][].

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

        request = security_settings.ListSecuritySettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_security_settings,
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
        response = pagers.ListSecuritySettingsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_security_settings(
        self,
        request: Union[security_settings.DeleteSecuritySettingsRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified
        [SecuritySettings][google.cloud.dialogflow.cx.v3beta1.SecuritySettings].

        .. code-block:: python

            from google.cloud import dialogflowcx_v3beta1

            async def sample_delete_security_settings():
                # Create a client
                client = dialogflowcx_v3beta1.SecuritySettingsServiceAsyncClient()

                # Initialize request argument(s)
                request = dialogflowcx_v3beta1.DeleteSecuritySettingsRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_security_settings(request=request)

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.DeleteSecuritySettingsRequest, dict]):
                The request object. The request message for
                [SecuritySettings.DeleteSecuritySettings][].
            name (:class:`str`):
                Required. The name of the
                [SecuritySettings][google.cloud.dialogflow.cx.v3beta1.SecuritySettings]
                to delete. Format:
                ``projects/<Project ID>/locations/<Location ID>/securitySettings/<Security Settings ID>``.

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

        request = security_settings.DeleteSecuritySettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_security_settings,
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflowcx",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("SecuritySettingsServiceAsyncClient",)
