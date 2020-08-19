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
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation
from google.api_core import operation_async
from google.cloud.dialogflowcx_v3beta1.services.agents import pagers
from google.cloud.dialogflowcx_v3beta1.types import agent
from google.cloud.dialogflowcx_v3beta1.types import agent as gcdc_agent
from google.protobuf import empty_pb2 as empty  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import struct_pb2 as struct  # type: ignore

from .transports.base import AgentsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import AgentsGrpcAsyncIOTransport
from .client import AgentsClient


class AgentsAsyncClient:
    """Service for managing
    [Agents][google.cloud.dialogflow.cx.v3beta1.Agent].
    """

    _client: AgentsClient

    DEFAULT_ENDPOINT = AgentsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AgentsClient.DEFAULT_MTLS_ENDPOINT

    agent_path = staticmethod(AgentsClient.agent_path)

    from_service_account_file = AgentsClient.from_service_account_file
    from_service_account_json = from_service_account_file

    get_transport_class = functools.partial(
        type(AgentsClient).get_transport_class, type(AgentsClient)
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, AgentsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the agents client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AgentsTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        self._client = AgentsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_agents(
        self,
        request: agent.ListAgentsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAgentsAsyncPager:
        r"""Returns the list of all agents in the specified
        location.

        Args:
            request (:class:`~.agent.ListAgentsRequest`):
                The request object. The request message for
                [Agents.ListAgents][google.cloud.dialogflow.cx.v3beta1.Agents.ListAgents].
            parent (:class:`str`):
                Required. The location to list all agents for. Format:
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
            ~.pagers.ListAgentsAsyncPager:
                The response message for
                [Agents.ListAgents][google.cloud.dialogflow.cx.v3beta1.Agents.ListAgents].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = agent.ListAgentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_agents,
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
        response = pagers.ListAgentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_agent(
        self,
        request: agent.GetAgentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> agent.Agent:
        r"""Retrieves the specified agent.

        Args:
            request (:class:`~.agent.GetAgentRequest`):
                The request object. The request message for
                [Agents.GetAgent][google.cloud.dialogflow.cx.v3beta1.Agents.GetAgent].
            name (:class:`str`):
                Required. The name of the agent. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.agent.Agent:
                Agents are best described as Natural Language
                Understanding (NLU) modules that transform user requests
                into actionable data. You can include agents in your
                app, product, or service to determine user intent and
                respond to the user in a natural way.

                After you create an agent, you can add
                [Intents][google.cloud.dialogflow.cx.v3beta1.Intent],
                [Entity
                Types][google.cloud.dialogflow.cx.v3beta1.EntityType],
                [Flows][google.cloud.dialogflow.cx.v3beta1.Flow],
                [Fulfillments][google.cloud.dialogflow.cx.v3beta1.Fulfillment],
                [Webhooks][google.cloud.dialogflow.cx.v3beta1.Webhook],
                and so on to manage the conversation flows..

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = agent.GetAgentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_agent,
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

    async def create_agent(
        self,
        request: gcdc_agent.CreateAgentRequest = None,
        *,
        parent: str = None,
        agent: gcdc_agent.Agent = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_agent.Agent:
        r"""Creates an agent in the specified location.

        Args:
            request (:class:`~.gcdc_agent.CreateAgentRequest`):
                The request object. The request message for
                [Agents.CreateAgent][google.cloud.dialogflow.cx.v3beta1.Agents.CreateAgent].
            parent (:class:`str`):
                Required. The location to create a agent for. Format:
                ``projects/<Project ID>/locations/<Location ID>``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            agent (:class:`~.gcdc_agent.Agent`):
                Required. The agent to create.
                This corresponds to the ``agent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcdc_agent.Agent:
                Agents are best described as Natural Language
                Understanding (NLU) modules that transform user requests
                into actionable data. You can include agents in your
                app, product, or service to determine user intent and
                respond to the user in a natural way.

                After you create an agent, you can add
                [Intents][google.cloud.dialogflow.cx.v3beta1.Intent],
                [Entity
                Types][google.cloud.dialogflow.cx.v3beta1.EntityType],
                [Flows][google.cloud.dialogflow.cx.v3beta1.Flow],
                [Fulfillments][google.cloud.dialogflow.cx.v3beta1.Fulfillment],
                [Webhooks][google.cloud.dialogflow.cx.v3beta1.Webhook],
                and so on to manage the conversation flows..

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, agent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_agent.CreateAgentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent
        if agent is not None:
            request.agent = agent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_agent,
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

    async def update_agent(
        self,
        request: gcdc_agent.UpdateAgentRequest = None,
        *,
        agent: gcdc_agent.Agent = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_agent.Agent:
        r"""Updates the specified agent.

        Args:
            request (:class:`~.gcdc_agent.UpdateAgentRequest`):
                The request object. The request message for
                [Agents.UpdateAgent][google.cloud.dialogflow.cx.v3beta1.Agents.UpdateAgent].
            agent (:class:`~.gcdc_agent.Agent`):
                Required. The agent to update.
                This corresponds to the ``agent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                The mask to control which fields get
                updated. If the mask is not present, all
                fields will be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcdc_agent.Agent:
                Agents are best described as Natural Language
                Understanding (NLU) modules that transform user requests
                into actionable data. You can include agents in your
                app, product, or service to determine user intent and
                respond to the user in a natural way.

                After you create an agent, you can add
                [Intents][google.cloud.dialogflow.cx.v3beta1.Intent],
                [Entity
                Types][google.cloud.dialogflow.cx.v3beta1.EntityType],
                [Flows][google.cloud.dialogflow.cx.v3beta1.Flow],
                [Fulfillments][google.cloud.dialogflow.cx.v3beta1.Fulfillment],
                [Webhooks][google.cloud.dialogflow.cx.v3beta1.Webhook],
                and so on to manage the conversation flows..

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([agent, update_mask]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_agent.UpdateAgentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if agent is not None:
            request.agent = agent
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_agent,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("agent.name", request.agent.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_agent(
        self,
        request: agent.DeleteAgentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified agent.

        Args:
            request (:class:`~.agent.DeleteAgentRequest`):
                The request object. The request message for
                [Agents.DeleteAgent][google.cloud.dialogflow.cx.v3beta1.Agents.DeleteAgent].
            name (:class:`str`):
                Required. The name of the agent to delete. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
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
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = agent.DeleteAgentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_agent,
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

    async def export_agent(
        self,
        request: agent.ExportAgentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Exports the specified agent to a ZIP file.

        Args:
            request (:class:`~.agent.ExportAgentRequest`):
                The request object. The request message for
                [Agents.ExportAgent][google.cloud.dialogflow.cx.v3beta1.Agents.ExportAgent].

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.agent.ExportAgentResponse``: The response
                message for
                [Agents.ExportAgent][google.cloud.dialogflow.cx.v3beta1.Agents.ExportAgent].

        """
        # Create or coerce a protobuf request object.

        request = agent.ExportAgentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.export_agent,
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
            agent.ExportAgentResponse,
            metadata_type=struct.Struct,
        )

        # Done; return the response.
        return response

    async def restore_agent(
        self,
        request: agent.RestoreAgentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Restores the specified agent from a ZIP file.
        Note that all existing intents, intent routes, entity
        types, pages and webhooks in the agent will be deleted.

        Args:
            request (:class:`~.agent.RestoreAgentRequest`):
                The request object. The request message for
                [Agents.RestoreAgent][google.cloud.dialogflow.cx.v3beta1.Agents.RestoreAgent].

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.empty.Empty``: A generic empty message that
                you can re-use to avoid defining duplicated empty
                messages in your APIs. A typical example is to use it as
                the request or the response type of an API method. For
                instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON
                object ``{}``.

        """
        # Create or coerce a protobuf request object.

        request = agent.RestoreAgentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.restore_agent,
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
            empty.Empty,
            metadata_type=struct.Struct,
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


__all__ = ("AgentsAsyncClient",)
