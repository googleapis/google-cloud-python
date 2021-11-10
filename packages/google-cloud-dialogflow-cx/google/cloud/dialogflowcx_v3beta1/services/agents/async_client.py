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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.dialogflowcx_v3beta1.services.agents import pagers
from google.cloud.dialogflowcx_v3beta1.types import advanced_settings
from google.cloud.dialogflowcx_v3beta1.types import agent
from google.cloud.dialogflowcx_v3beta1.types import agent as gcdc_agent
from google.cloud.dialogflowcx_v3beta1.types import flow
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
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
    parse_agent_path = staticmethod(AgentsClient.parse_agent_path)
    agent_validation_result_path = staticmethod(
        AgentsClient.agent_validation_result_path
    )
    parse_agent_validation_result_path = staticmethod(
        AgentsClient.parse_agent_validation_result_path
    )
    environment_path = staticmethod(AgentsClient.environment_path)
    parse_environment_path = staticmethod(AgentsClient.parse_environment_path)
    flow_path = staticmethod(AgentsClient.flow_path)
    parse_flow_path = staticmethod(AgentsClient.parse_flow_path)
    flow_validation_result_path = staticmethod(AgentsClient.flow_validation_result_path)
    parse_flow_validation_result_path = staticmethod(
        AgentsClient.parse_flow_validation_result_path
    )
    security_settings_path = staticmethod(AgentsClient.security_settings_path)
    parse_security_settings_path = staticmethod(
        AgentsClient.parse_security_settings_path
    )
    common_billing_account_path = staticmethod(AgentsClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(
        AgentsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AgentsClient.common_folder_path)
    parse_common_folder_path = staticmethod(AgentsClient.parse_common_folder_path)
    common_organization_path = staticmethod(AgentsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        AgentsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AgentsClient.common_project_path)
    parse_common_project_path = staticmethod(AgentsClient.parse_common_project_path)
    common_location_path = staticmethod(AgentsClient.common_location_path)
    parse_common_location_path = staticmethod(AgentsClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            AgentsAsyncClient: The constructed client.
        """
        return AgentsClient.from_service_account_info.__func__(AgentsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            AgentsAsyncClient: The constructed client.
        """
        return AgentsClient.from_service_account_file.__func__(AgentsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> AgentsTransport:
        """Returns the transport used by the client instance.

        Returns:
            AgentsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(AgentsClient).get_transport_class, type(AgentsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, AgentsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the agents client.

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
        self._client = AgentsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_agents(
        self,
        request: Union[agent.ListAgentsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAgentsAsyncPager:
        r"""Returns the list of all agents in the specified
        location.

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.ListAgentsRequest, dict]):
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
            google.cloud.dialogflowcx_v3beta1.services.agents.pagers.ListAgentsAsyncPager:
                The response message for
                [Agents.ListAgents][google.cloud.dialogflow.cx.v3beta1.Agents.ListAgents].

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
        request: Union[agent.GetAgentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> agent.Agent:
        r"""Retrieves the specified agent.

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.GetAgentRequest, dict]):
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
            google.cloud.dialogflowcx_v3beta1.types.Agent:
                Agents are best described as Natural Language Understanding (NLU) modules
                   that transform user requests into actionable data.
                   You can include agents in your app, product, or
                   service to determine user intent and respond to the
                   user in a natural way.

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
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
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
        request: Union[gcdc_agent.CreateAgentRequest, dict] = None,
        *,
        parent: str = None,
        agent: gcdc_agent.Agent = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_agent.Agent:
        r"""Creates an agent in the specified location.

        Note: You should always train a flow prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/cx/docs/concept/training>`__.

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.CreateAgentRequest, dict]):
                The request object. The request message for
                [Agents.CreateAgent][google.cloud.dialogflow.cx.v3beta1.Agents.CreateAgent].
            parent (:class:`str`):
                Required. The location to create a agent for. Format:
                ``projects/<Project ID>/locations/<Location ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            agent (:class:`google.cloud.dialogflowcx_v3beta1.types.Agent`):
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
            google.cloud.dialogflowcx_v3beta1.types.Agent:
                Agents are best described as Natural Language Understanding (NLU) modules
                   that transform user requests into actionable data.
                   You can include agents in your app, product, or
                   service to determine user intent and respond to the
                   user in a natural way.

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
        has_flattened_params = any([parent, agent])
        if request is not None and has_flattened_params:
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
        request: Union[gcdc_agent.UpdateAgentRequest, dict] = None,
        *,
        agent: gcdc_agent.Agent = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_agent.Agent:
        r"""Updates the specified agent.

        Note: You should always train a flow prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/cx/docs/concept/training>`__.

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.UpdateAgentRequest, dict]):
                The request object. The request message for
                [Agents.UpdateAgent][google.cloud.dialogflow.cx.v3beta1.Agents.UpdateAgent].
            agent (:class:`google.cloud.dialogflowcx_v3beta1.types.Agent`):
                Required. The agent to update.
                This corresponds to the ``agent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
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
            google.cloud.dialogflowcx_v3beta1.types.Agent:
                Agents are best described as Natural Language Understanding (NLU) modules
                   that transform user requests into actionable data.
                   You can include agents in your app, product, or
                   service to determine user intent and respond to the
                   user in a natural way.

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
        has_flattened_params = any([agent, update_mask])
        if request is not None and has_flattened_params:
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
        request: Union[agent.DeleteAgentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified agent.

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.DeleteAgentRequest, dict]):
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
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
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
        request: Union[agent.ExportAgentRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Exports the specified agent to a binary file.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``: An empty `Struct
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct>`__
        -  ``response``:
           [ExportAgentResponse][google.cloud.dialogflow.cx.v3beta1.ExportAgentResponse]

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.ExportAgentRequest, dict]):
                The request object. The request message for
                [Agents.ExportAgent][google.cloud.dialogflow.cx.v3beta1.Agents.ExportAgent].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflowcx_v3beta1.types.ExportAgentResponse`
                The response message for
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
            metadata_type=struct_pb2.Struct,
        )

        # Done; return the response.
        return response

    async def restore_agent(
        self,
        request: Union[agent.RestoreAgentRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Restores the specified agent from a binary file.

        Replaces the current agent with a new one. Note that all
        existing resources in agent (e.g. intents, entity types, flows)
        will be removed.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``: An empty `Struct
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct>`__
        -  ``response``: An `Empty
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#empty>`__

        Note: You should always train a flow prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/cx/docs/concept/training>`__.

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.RestoreAgentRequest, dict]):
                The request object. The request message for
                [Agents.RestoreAgent][google.cloud.dialogflow.cx.v3beta1.Agents.RestoreAgent].
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
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

        # Done; return the response.
        return response

    async def validate_agent(
        self,
        request: Union[agent.ValidateAgentRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> agent.AgentValidationResult:
        r"""Validates the specified agent and creates or updates
        validation results. The agent in draft version is
        validated. Please call this API after the training is
        completed to get the complete validation results.

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.ValidateAgentRequest, dict]):
                The request object. The request message for
                [Agents.ValidateAgent][google.cloud.dialogflow.cx.v3beta1.Agents.ValidateAgent].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.AgentValidationResult:
                The response message for
                [Agents.GetAgentValidationResult][google.cloud.dialogflow.cx.v3beta1.Agents.GetAgentValidationResult].

        """
        # Create or coerce a protobuf request object.
        request = agent.ValidateAgentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.validate_agent,
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

    async def get_agent_validation_result(
        self,
        request: Union[agent.GetAgentValidationResultRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> agent.AgentValidationResult:
        r"""Gets the latest agent validation result. Agent
        validation is performed when ValidateAgent is called.

        Args:
            request (Union[google.cloud.dialogflowcx_v3beta1.types.GetAgentValidationResultRequest, dict]):
                The request object. The request message for
                [Agents.GetAgentValidationResult][google.cloud.dialogflow.cx.v3beta1.Agents.GetAgentValidationResult].
            name (:class:`str`):
                Required. The agent name. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/validationResult``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3beta1.types.AgentValidationResult:
                The response message for
                [Agents.GetAgentValidationResult][google.cloud.dialogflow.cx.v3beta1.Agents.GetAgentValidationResult].

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

        request = agent.GetAgentValidationResultRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_agent_validation_result,
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


__all__ = ("AgentsAsyncClient",)
