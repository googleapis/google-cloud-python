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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.dialogflowcx_v3beta1.services.flows import pagers
from google.cloud.dialogflowcx_v3beta1.types import flow
from google.cloud.dialogflowcx_v3beta1.types import flow as gcdc_flow
from google.cloud.dialogflowcx_v3beta1.types import page
from google.cloud.dialogflowcx_v3beta1.types import validation_message
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import FlowsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import FlowsGrpcAsyncIOTransport
from .client import FlowsClient


class FlowsAsyncClient:
    """Service for managing
    [Flows][google.cloud.dialogflow.cx.v3beta1.Flow].
    """

    _client: FlowsClient

    DEFAULT_ENDPOINT = FlowsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = FlowsClient.DEFAULT_MTLS_ENDPOINT

    flow_path = staticmethod(FlowsClient.flow_path)
    parse_flow_path = staticmethod(FlowsClient.parse_flow_path)
    flow_validation_result_path = staticmethod(FlowsClient.flow_validation_result_path)
    parse_flow_validation_result_path = staticmethod(
        FlowsClient.parse_flow_validation_result_path
    )
    intent_path = staticmethod(FlowsClient.intent_path)
    parse_intent_path = staticmethod(FlowsClient.parse_intent_path)
    page_path = staticmethod(FlowsClient.page_path)
    parse_page_path = staticmethod(FlowsClient.parse_page_path)
    transition_route_group_path = staticmethod(FlowsClient.transition_route_group_path)
    parse_transition_route_group_path = staticmethod(
        FlowsClient.parse_transition_route_group_path
    )
    webhook_path = staticmethod(FlowsClient.webhook_path)
    parse_webhook_path = staticmethod(FlowsClient.parse_webhook_path)
    common_billing_account_path = staticmethod(FlowsClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(
        FlowsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(FlowsClient.common_folder_path)
    parse_common_folder_path = staticmethod(FlowsClient.parse_common_folder_path)
    common_organization_path = staticmethod(FlowsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        FlowsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(FlowsClient.common_project_path)
    parse_common_project_path = staticmethod(FlowsClient.parse_common_project_path)
    common_location_path = staticmethod(FlowsClient.common_location_path)
    parse_common_location_path = staticmethod(FlowsClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            FlowsAsyncClient: The constructed client.
        """
        return FlowsClient.from_service_account_info.__func__(FlowsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            FlowsAsyncClient: The constructed client.
        """
        return FlowsClient.from_service_account_file.__func__(FlowsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> FlowsTransport:
        """Returns the transport used by the client instance.

        Returns:
            FlowsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(FlowsClient).get_transport_class, type(FlowsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, FlowsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the flows client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.FlowsTransport]): The
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
        self._client = FlowsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_flow(
        self,
        request: gcdc_flow.CreateFlowRequest = None,
        *,
        parent: str = None,
        flow: gcdc_flow.Flow = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_flow.Flow:
        r"""Creates a flow in the specified agent.

        Note: You should always train a flow prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/cx/docs/concept/training>`__.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.CreateFlowRequest`):
                The request object. The request message for
                [Flows.CreateFlow][google.cloud.dialogflow.cx.v3beta1.Flows.CreateFlow].
            parent (:class:`str`):
                Required. The agent to create a flow for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            flow (:class:`google.cloud.dialogflowcx_v3beta1.types.Flow`):
                Required. The flow to create.
                This corresponds to the ``flow`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.Flow:
                Flows represents the conversation
                flows when you build your chatbot agent.
                A flow consists of many pages connected
                by the transition routes. Conversations
                always start with the built-in Start
                Flow (with an all-0 ID). Transition
                routes can direct the conversation
                session from the current flow (parent
                flow) to another flow (sub flow). When
                the sub flow is finished, Dialogflow
                will bring the session back to the
                parent flow, where the sub flow is
                started.

                Usually, when a transition route is
                followed by a matched intent, the intent
                will be "consumed". This means the
                intent won't activate more transition
                routes. However, when the followed
                transition route moves the conversation
                session into a different flow, the
                matched intent can be carried over and
                to be consumed in the target flow.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, flow])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_flow.CreateFlowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if flow is not None:
            request.flow = flow

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_flow,
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

    async def delete_flow(
        self,
        request: flow.DeleteFlowRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a specified flow.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.DeleteFlowRequest`):
                The request object. The request message for
                [Flows.DeleteFlow][google.cloud.dialogflow.cx.v3beta1.Flows.DeleteFlow].
            name (:class:`str`):
                Required. The name of the flow to delete. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.

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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = flow.DeleteFlowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_flow,
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

    async def list_flows(
        self,
        request: flow.ListFlowsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListFlowsAsyncPager:
        r"""Returns the list of all flows in the specified agent.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.ListFlowsRequest`):
                The request object. The request message for
                [Flows.ListFlows][google.cloud.dialogflow.cx.v3beta1.Flows.ListFlows].
            parent (:class:`str`):
                Required. The agent containing the flows. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.services.flows.pagers.ListFlowsAsyncPager:
                The response message for
                [Flows.ListFlows][google.cloud.dialogflow.cx.v3beta1.Flows.ListFlows].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = flow.ListFlowsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_flows,
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
        response = pagers.ListFlowsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_flow(
        self,
        request: flow.GetFlowRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> flow.Flow:
        r"""Retrieves the specified flow.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.GetFlowRequest`):
                The request object. The response message for
                [Flows.GetFlow][google.cloud.dialogflow.cx.v3beta1.Flows.GetFlow].
            name (:class:`str`):
                Required. The name of the flow to get. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.Flow:
                Flows represents the conversation
                flows when you build your chatbot agent.
                A flow consists of many pages connected
                by the transition routes. Conversations
                always start with the built-in Start
                Flow (with an all-0 ID). Transition
                routes can direct the conversation
                session from the current flow (parent
                flow) to another flow (sub flow). When
                the sub flow is finished, Dialogflow
                will bring the session back to the
                parent flow, where the sub flow is
                started.

                Usually, when a transition route is
                followed by a matched intent, the intent
                will be "consumed". This means the
                intent won't activate more transition
                routes. However, when the followed
                transition route moves the conversation
                session into a different flow, the
                matched intent can be carried over and
                to be consumed in the target flow.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = flow.GetFlowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_flow,
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

    async def update_flow(
        self,
        request: gcdc_flow.UpdateFlowRequest = None,
        *,
        flow: gcdc_flow.Flow = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_flow.Flow:
        r"""Updates the specified flow.

        Note: You should always train a flow prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/cx/docs/concept/training>`__.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.UpdateFlowRequest`):
                The request object. The request message for
                [Flows.UpdateFlow][google.cloud.dialogflow.cx.v3beta1.Flows.UpdateFlow].
            flow (:class:`google.cloud.dialogflowcx_v3beta1.types.Flow`):
                Required. The flow to update.
                This corresponds to the ``flow`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The mask to control which fields get updated.
                If ``update_mask`` is not specified, an error will be
                returned.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.Flow:
                Flows represents the conversation
                flows when you build your chatbot agent.
                A flow consists of many pages connected
                by the transition routes. Conversations
                always start with the built-in Start
                Flow (with an all-0 ID). Transition
                routes can direct the conversation
                session from the current flow (parent
                flow) to another flow (sub flow). When
                the sub flow is finished, Dialogflow
                will bring the session back to the
                parent flow, where the sub flow is
                started.

                Usually, when a transition route is
                followed by a matched intent, the intent
                will be "consumed". This means the
                intent won't activate more transition
                routes. However, when the followed
                transition route moves the conversation
                session into a different flow, the
                matched intent can be carried over and
                to be consumed in the target flow.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([flow, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_flow.UpdateFlowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if flow is not None:
            request.flow = flow
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_flow,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("flow.name", request.flow.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def train_flow(
        self,
        request: flow.TrainFlowRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Trains the specified flow. Note that only the flow in 'draft'
        environment is trained.

        Note: You should always train a flow prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/cx/docs/concept/training>`__.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.TrainFlowRequest`):
                The request object. The request message for
                [Flows.TrainFlow][google.cloud.dialogflow.cx.v3beta1.Flows.TrainFlow].
            name (:class:`str`):
                Required. The flow to train. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = flow.TrainFlowRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.train_flow,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

        # Done; return the response.
        return response

    async def validate_flow(
        self,
        request: flow.ValidateFlowRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> flow.FlowValidationResult:
        r"""Validates the specified flow and creates or updates
        validation results. Please call this API after the
        training is completed to get the complete validation
        results.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.ValidateFlowRequest`):
                The request object. The request message for
                [Flows.ValidateFlow][google.cloud.dialogflow.cx.v3beta1.Flows.ValidateFlow].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.FlowValidationResult:
                The response message for
                [Flows.GetFlowValidationResult][google.cloud.dialogflow.cx.v3beta1.Flows.GetFlowValidationResult].

        """
        # Create or coerce a protobuf request object.
        request = flow.ValidateFlowRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.validate_flow,
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

    async def get_flow_validation_result(
        self,
        request: flow.GetFlowValidationResultRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> flow.FlowValidationResult:
        r"""Gets the latest flow validation result. Flow
        validation is performed when ValidateFlow is called.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.GetFlowValidationResultRequest`):
                The request object. The request message for
                [Flows.GetFlowValidationResult][google.cloud.dialogflow.cx.v3beta1.Flows.GetFlowValidationResult].
            name (:class:`str`):
                Required. The flow name. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/validationResult``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.FlowValidationResult:
                The response message for
                [Flows.GetFlowValidationResult][google.cloud.dialogflow.cx.v3beta1.Flows.GetFlowValidationResult].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = flow.GetFlowValidationResultRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_flow_validation_result,
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

    async def import_flow(
        self,
        request: flow.ImportFlowRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Imports the specified flow to the specified agent from a binary
        file.

        Note: You should always train a flow prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/cx/docs/concept/training>`__.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.ImportFlowRequest`):
                The request object. The request message for
                [Flows.ImportFlow][google.cloud.dialogflow.cx.v3beta1.Flows.ImportFlow].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflowcx_v3beta1.types.ImportFlowResponse`
                The response message for
                [Flows.ImportFlow][google.cloud.dialogflow.cx.v3beta1.Flows.ImportFlow].

        """
        # Create or coerce a protobuf request object.
        request = flow.ImportFlowRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.import_flow,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            flow.ImportFlowResponse,
            metadata_type=struct_pb2.Struct,
        )

        # Done; return the response.
        return response

    async def export_flow(
        self,
        request: flow.ExportFlowRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Exports the specified flow to a binary file.
        Note that resources (e.g. intents, entities, webhooks)
        that the flow references will also be exported.

        Args:
            request (:class:`google.cloud.dialogflowcx_v3beta1.types.ExportFlowRequest`):
                The request object. The request message for
                [Flows.ExportFlow][google.cloud.dialogflow.cx.v3beta1.Flows.ExportFlow].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflowcx_v3beta1.types.ExportFlowResponse`
                The response message for
                [Flows.ExportFlow][google.cloud.dialogflow.cx.v3beta1.Flows.ExportFlow].

        """
        # Create or coerce a protobuf request object.
        request = flow.ExportFlowRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.export_flow,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            flow.ExportFlowResponse,
            metadata_type=struct_pb2.Struct,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflowcx",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("FlowsAsyncClient",)
