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

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore
import pkg_resources

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore

from google.cloud.retail_v2beta.services.control_service import pagers
from google.cloud.retail_v2beta.types import common
from google.cloud.retail_v2beta.types import control
from google.cloud.retail_v2beta.types import control as gcr_control
from google.cloud.retail_v2beta.types import control_service, search_service

from .client import ControlServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, ControlServiceTransport
from .transports.grpc_asyncio import ControlServiceGrpcAsyncIOTransport


class ControlServiceAsyncClient:
    """Service for modifying Control."""

    _client: ControlServiceClient

    DEFAULT_ENDPOINT = ControlServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ControlServiceClient.DEFAULT_MTLS_ENDPOINT

    catalog_path = staticmethod(ControlServiceClient.catalog_path)
    parse_catalog_path = staticmethod(ControlServiceClient.parse_catalog_path)
    control_path = staticmethod(ControlServiceClient.control_path)
    parse_control_path = staticmethod(ControlServiceClient.parse_control_path)
    common_billing_account_path = staticmethod(
        ControlServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ControlServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ControlServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ControlServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ControlServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ControlServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ControlServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        ControlServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(ControlServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        ControlServiceClient.parse_common_location_path
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
            ControlServiceAsyncClient: The constructed client.
        """
        return ControlServiceClient.from_service_account_info.__func__(ControlServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ControlServiceAsyncClient: The constructed client.
        """
        return ControlServiceClient.from_service_account_file.__func__(ControlServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return ControlServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> ControlServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ControlServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ControlServiceClient).get_transport_class, type(ControlServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ControlServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the control service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ControlServiceTransport]): The
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
        self._client = ControlServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_control(
        self,
        request: Union[control_service.CreateControlRequest, dict] = None,
        *,
        parent: str = None,
        control: gcr_control.Control = None,
        control_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_control.Control:
        r"""Creates a Control.

        If the [Control][google.cloud.retail.v2beta.Control] to create
        already exists, an ALREADY_EXISTS error is returned.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_create_control():
                # Create a client
                client = retail_v2beta.ControlServiceAsyncClient()

                # Initialize request argument(s)
                control = retail_v2beta.Control()
                control.facet_spec.facet_key.key = "key_value"
                control.display_name = "display_name_value"
                control.solution_types = "SOLUTION_TYPE_SEARCH"

                request = retail_v2beta.CreateControlRequest(
                    parent="parent_value",
                    control=control,
                    control_id="control_id_value",
                )

                # Make the request
                response = await client.create_control(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.CreateControlRequest, dict]):
                The request object. Request for CreateControl method.
            parent (:class:`str`):
                Required. Full resource name of parent catalog. Format:
                ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            control (:class:`google.cloud.retail_v2beta.types.Control`):
                Required. The Control to create.
                This corresponds to the ``control`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            control_id (:class:`str`):
                Required. The ID to use for the Control, which will
                become the final component of the Control's resource
                name.

                This value should be 4-63 characters, and valid
                characters are /[a-z][0-9]-_/.

                This corresponds to the ``control_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.Control:
                Configures dynamic serving time
                metadata that is used to pre and post
                process search/recommendation model
                results.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, control, control_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = control_service.CreateControlRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if control is not None:
            request.control = control
        if control_id is not None:
            request.control_id = control_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_control,
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

    async def delete_control(
        self,
        request: Union[control_service.DeleteControlRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a Control.

        If the [Control][google.cloud.retail.v2beta.Control] to delete
        does not exist, a NOT_FOUND error is returned.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_delete_control():
                # Create a client
                client = retail_v2beta.ControlServiceAsyncClient()

                # Initialize request argument(s)
                request = retail_v2beta.DeleteControlRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_control(request=request)

        Args:
            request (Union[google.cloud.retail_v2beta.types.DeleteControlRequest, dict]):
                The request object. Request for DeleteControl method.
            name (:class:`str`):
                Required. The resource name of the Control to delete.
                Format:
                ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/controls/{control_id}``

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

        request = control_service.DeleteControlRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_control,
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

    async def update_control(
        self,
        request: Union[control_service.UpdateControlRequest, dict] = None,
        *,
        control: gcr_control.Control = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcr_control.Control:
        r"""Updates a Control.

        [Control][google.cloud.retail.v2beta.Control] cannot be set to a
        different oneof field, if so an INVALID_ARGUMENT is returned. If
        the [Control][google.cloud.retail.v2beta.Control] to delete does
        not exist, a NOT_FOUND error is returned.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_update_control():
                # Create a client
                client = retail_v2beta.ControlServiceAsyncClient()

                # Initialize request argument(s)
                control = retail_v2beta.Control()
                control.facet_spec.facet_key.key = "key_value"
                control.display_name = "display_name_value"
                control.solution_types = "SOLUTION_TYPE_SEARCH"

                request = retail_v2beta.UpdateControlRequest(
                    control=control,
                )

                # Make the request
                response = await client.update_control(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.UpdateControlRequest, dict]):
                The request object. Request for UpdateControl method.
            control (:class:`google.cloud.retail_v2beta.types.Control`):
                Required. The Control to update.
                This corresponds to the ``control`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Indicates which fields in the provided
                [Control][google.cloud.retail.v2beta.Control] to update.
                The following are NOT supported:

                -  [Control.name][google.cloud.retail.v2beta.Control.name]

                If not set or empty, all supported fields are updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.Control:
                Configures dynamic serving time
                metadata that is used to pre and post
                process search/recommendation model
                results.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([control, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = control_service.UpdateControlRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if control is not None:
            request.control = control
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_control,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("control.name", request.control.name),)
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

    async def get_control(
        self,
        request: Union[control_service.GetControlRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> control.Control:
        r"""Gets a Control.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_get_control():
                # Create a client
                client = retail_v2beta.ControlServiceAsyncClient()

                # Initialize request argument(s)
                request = retail_v2beta.GetControlRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_control(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.GetControlRequest, dict]):
                The request object. Request for GetControl method.
            name (:class:`str`):
                Required. The resource name of the Control to delete.
                Format:
                ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/controls/{control_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.types.Control:
                Configures dynamic serving time
                metadata that is used to pre and post
                process search/recommendation model
                results.

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

        request = control_service.GetControlRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_control,
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

    async def list_controls(
        self,
        request: Union[control_service.ListControlsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListControlsAsyncPager:
        r"""Lists all Controls linked to this catalog.

        .. code-block:: python

            from google.cloud import retail_v2beta

            async def sample_list_controls():
                # Create a client
                client = retail_v2beta.ControlServiceAsyncClient()

                # Initialize request argument(s)
                request = retail_v2beta.ListControlsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_controls(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.retail_v2beta.types.ListControlsRequest, dict]):
                The request object. Request for ListControls method.
            parent (:class:`str`):
                Required. The catalog resource name. Format:
                ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2beta.services.control_service.pagers.ListControlsAsyncPager:
                Response for ListControls method.
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

        request = control_service.ListControlsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_controls,
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
        response = pagers.ListControlsAsyncPager(
            method=rpc,
            request=request,
            response=response,
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
            "google-cloud-retail",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ControlServiceAsyncClient",)
