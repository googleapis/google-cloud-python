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

from google.cloud.dialogflowcx_v3.services.transition_route_groups import pagers
from google.cloud.dialogflowcx_v3.types import page
from google.cloud.dialogflowcx_v3.types import transition_route_group
from google.cloud.dialogflowcx_v3.types import (
    transition_route_group as gcdc_transition_route_group,
)
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import TransitionRouteGroupsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import TransitionRouteGroupsGrpcAsyncIOTransport
from .client import TransitionRouteGroupsClient


class TransitionRouteGroupsAsyncClient:
    """Service for managing
    [TransitionRouteGroups][google.cloud.dialogflow.cx.v3.TransitionRouteGroup].
    """

    _client: TransitionRouteGroupsClient

    DEFAULT_ENDPOINT = TransitionRouteGroupsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = TransitionRouteGroupsClient.DEFAULT_MTLS_ENDPOINT

    flow_path = staticmethod(TransitionRouteGroupsClient.flow_path)
    parse_flow_path = staticmethod(TransitionRouteGroupsClient.parse_flow_path)
    intent_path = staticmethod(TransitionRouteGroupsClient.intent_path)
    parse_intent_path = staticmethod(TransitionRouteGroupsClient.parse_intent_path)
    page_path = staticmethod(TransitionRouteGroupsClient.page_path)
    parse_page_path = staticmethod(TransitionRouteGroupsClient.parse_page_path)
    transition_route_group_path = staticmethod(
        TransitionRouteGroupsClient.transition_route_group_path
    )
    parse_transition_route_group_path = staticmethod(
        TransitionRouteGroupsClient.parse_transition_route_group_path
    )
    webhook_path = staticmethod(TransitionRouteGroupsClient.webhook_path)
    parse_webhook_path = staticmethod(TransitionRouteGroupsClient.parse_webhook_path)
    common_billing_account_path = staticmethod(
        TransitionRouteGroupsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        TransitionRouteGroupsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(TransitionRouteGroupsClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        TransitionRouteGroupsClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        TransitionRouteGroupsClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        TransitionRouteGroupsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(TransitionRouteGroupsClient.common_project_path)
    parse_common_project_path = staticmethod(
        TransitionRouteGroupsClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        TransitionRouteGroupsClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        TransitionRouteGroupsClient.parse_common_location_path
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
            TransitionRouteGroupsAsyncClient: The constructed client.
        """
        return TransitionRouteGroupsClient.from_service_account_info.__func__(TransitionRouteGroupsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            TransitionRouteGroupsAsyncClient: The constructed client.
        """
        return TransitionRouteGroupsClient.from_service_account_file.__func__(TransitionRouteGroupsAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return TransitionRouteGroupsClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> TransitionRouteGroupsTransport:
        """Returns the transport used by the client instance.

        Returns:
            TransitionRouteGroupsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(TransitionRouteGroupsClient).get_transport_class,
        type(TransitionRouteGroupsClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, TransitionRouteGroupsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the transition route groups client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.TransitionRouteGroupsTransport]): The
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
        self._client = TransitionRouteGroupsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_transition_route_groups(
        self,
        request: Union[
            transition_route_group.ListTransitionRouteGroupsRequest, dict
        ] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTransitionRouteGroupsAsyncPager:
        r"""Returns the list of all transition route groups in
        the specified flow.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3

            async def sample_list_transition_route_groups():
                # Create a client
                client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient()

                # Initialize request argument(s)
                request = dialogflowcx_v3.ListTransitionRouteGroupsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_transition_route_groups(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.ListTransitionRouteGroupsRequest, dict]):
                The request object. The request message for
                [TransitionRouteGroups.ListTransitionRouteGroups][google.cloud.dialogflow.cx.v3.TransitionRouteGroups.ListTransitionRouteGroups].
            parent (:class:`str`):
                Required. The flow to list all transition route groups
                for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.services.transition_route_groups.pagers.ListTransitionRouteGroupsAsyncPager:
                The response message for
                [TransitionRouteGroups.ListTransitionRouteGroups][google.cloud.dialogflow.cx.v3.TransitionRouteGroups.ListTransitionRouteGroups].

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

        request = transition_route_group.ListTransitionRouteGroupsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_transition_route_groups,
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
        response = pagers.ListTransitionRouteGroupsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_transition_route_group(
        self,
        request: Union[
            transition_route_group.GetTransitionRouteGroupRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> transition_route_group.TransitionRouteGroup:
        r"""Retrieves the specified
        [TransitionRouteGroup][google.cloud.dialogflow.cx.v3.TransitionRouteGroup].

        .. code-block:: python

            from google.cloud import dialogflowcx_v3

            async def sample_get_transition_route_group():
                # Create a client
                client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient()

                # Initialize request argument(s)
                request = dialogflowcx_v3.GetTransitionRouteGroupRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_transition_route_group(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.GetTransitionRouteGroupRequest, dict]):
                The request object. The request message for
                [TransitionRouteGroups.GetTransitionRouteGroup][google.cloud.dialogflow.cx.v3.TransitionRouteGroups.GetTransitionRouteGroup].
            name (:class:`str`):
                Required. The name of the
                [TransitionRouteGroup][google.cloud.dialogflow.cx.v3.TransitionRouteGroup].
                Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/transitionRouteGroups/<Transition Route Group ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.TransitionRouteGroup:
                An TransitionRouteGroup represents a group of
                   [TransitionRoutes][google.cloud.dialogflow.cx.v3.TransitionRoute]
                   to be used by a
                   [Page][google.cloud.dialogflow.cx.v3.Page].

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

        request = transition_route_group.GetTransitionRouteGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_transition_route_group,
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

    async def create_transition_route_group(
        self,
        request: Union[
            gcdc_transition_route_group.CreateTransitionRouteGroupRequest, dict
        ] = None,
        *,
        parent: str = None,
        transition_route_group: gcdc_transition_route_group.TransitionRouteGroup = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_transition_route_group.TransitionRouteGroup:
        r"""Creates an
        [TransitionRouteGroup][google.cloud.dialogflow.cx.v3.TransitionRouteGroup]
        in the specified flow.

        Note: You should always train a flow prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/cx/docs/concept/training>`__.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3

            async def sample_create_transition_route_group():
                # Create a client
                client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient()

                # Initialize request argument(s)
                transition_route_group = dialogflowcx_v3.TransitionRouteGroup()
                transition_route_group.display_name = "display_name_value"

                request = dialogflowcx_v3.CreateTransitionRouteGroupRequest(
                    parent="parent_value",
                    transition_route_group=transition_route_group,
                )

                # Make the request
                response = await client.create_transition_route_group(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.CreateTransitionRouteGroupRequest, dict]):
                The request object. The request message for
                [TransitionRouteGroups.CreateTransitionRouteGroup][google.cloud.dialogflow.cx.v3.TransitionRouteGroups.CreateTransitionRouteGroup].
            parent (:class:`str`):
                Required. The flow to create an
                [TransitionRouteGroup][google.cloud.dialogflow.cx.v3.TransitionRouteGroup]
                for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            transition_route_group (:class:`google.cloud.dialogflowcx_v3.types.TransitionRouteGroup`):
                Required. The transition route group
                to create.

                This corresponds to the ``transition_route_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.TransitionRouteGroup:
                An TransitionRouteGroup represents a group of
                   [TransitionRoutes][google.cloud.dialogflow.cx.v3.TransitionRoute]
                   to be used by a
                   [Page][google.cloud.dialogflow.cx.v3.Page].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, transition_route_group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_transition_route_group.CreateTransitionRouteGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if transition_route_group is not None:
            request.transition_route_group = transition_route_group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_transition_route_group,
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

    async def update_transition_route_group(
        self,
        request: Union[
            gcdc_transition_route_group.UpdateTransitionRouteGroupRequest, dict
        ] = None,
        *,
        transition_route_group: gcdc_transition_route_group.TransitionRouteGroup = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_transition_route_group.TransitionRouteGroup:
        r"""Updates the specified
        [TransitionRouteGroup][google.cloud.dialogflow.cx.v3.TransitionRouteGroup].

        Note: You should always train a flow prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/cx/docs/concept/training>`__.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3

            async def sample_update_transition_route_group():
                # Create a client
                client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient()

                # Initialize request argument(s)
                transition_route_group = dialogflowcx_v3.TransitionRouteGroup()
                transition_route_group.display_name = "display_name_value"

                request = dialogflowcx_v3.UpdateTransitionRouteGroupRequest(
                    transition_route_group=transition_route_group,
                )

                # Make the request
                response = await client.update_transition_route_group(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.UpdateTransitionRouteGroupRequest, dict]):
                The request object. The request message for
                [TransitionRouteGroups.UpdateTransitionRouteGroup][google.cloud.dialogflow.cx.v3.TransitionRouteGroups.UpdateTransitionRouteGroup].
            transition_route_group (:class:`google.cloud.dialogflowcx_v3.types.TransitionRouteGroup`):
                Required. The transition route group
                to update.

                This corresponds to the ``transition_route_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The mask to control which fields get
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
            google.cloud.dialogflowcx_v3.types.TransitionRouteGroup:
                An TransitionRouteGroup represents a group of
                   [TransitionRoutes][google.cloud.dialogflow.cx.v3.TransitionRoute]
                   to be used by a
                   [Page][google.cloud.dialogflow.cx.v3.Page].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([transition_route_group, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_transition_route_group.UpdateTransitionRouteGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if transition_route_group is not None:
            request.transition_route_group = transition_route_group
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_transition_route_group,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("transition_route_group.name", request.transition_route_group.name),)
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

    async def delete_transition_route_group(
        self,
        request: Union[
            transition_route_group.DeleteTransitionRouteGroupRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified
        [TransitionRouteGroup][google.cloud.dialogflow.cx.v3.TransitionRouteGroup].

        Note: You should always train a flow prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/cx/docs/concept/training>`__.

        .. code-block:: python

            from google.cloud import dialogflowcx_v3

            async def sample_delete_transition_route_group():
                # Create a client
                client = dialogflowcx_v3.TransitionRouteGroupsAsyncClient()

                # Initialize request argument(s)
                request = dialogflowcx_v3.DeleteTransitionRouteGroupRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_transition_route_group(request=request)

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.DeleteTransitionRouteGroupRequest, dict]):
                The request object. The request message for
                [TransitionRouteGroups.DeleteTransitionRouteGroup][google.cloud.dialogflow.cx.v3.TransitionRouteGroups.DeleteTransitionRouteGroup].
            name (:class:`str`):
                Required. The name of the
                [TransitionRouteGroup][google.cloud.dialogflow.cx.v3.TransitionRouteGroup]
                to delete. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/transitionRouteGroups/<Transition Route Group ID>``.

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

        request = transition_route_group.DeleteTransitionRouteGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_transition_route_group,
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


__all__ = ("TransitionRouteGroupsAsyncClient",)
