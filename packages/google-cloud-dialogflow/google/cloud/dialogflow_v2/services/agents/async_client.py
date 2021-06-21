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
from google.cloud.dialogflow_v2.services.agents import pagers
from google.cloud.dialogflow_v2.types import agent
from google.cloud.dialogflow_v2.types import agent as gcd_agent
from google.cloud.dialogflow_v2.types import validation_result
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from .transports.base import AgentsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import AgentsGrpcAsyncIOTransport
from .client import AgentsClient


class AgentsAsyncClient:
    """Service for managing [Agents][google.cloud.dialogflow.v2.Agent]."""

    _client: AgentsClient

    DEFAULT_ENDPOINT = AgentsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AgentsClient.DEFAULT_MTLS_ENDPOINT

    agent_path = staticmethod(AgentsClient.agent_path)
    parse_agent_path = staticmethod(AgentsClient.parse_agent_path)
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

    async def get_agent(
        self,
        request: agent.GetAgentRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> agent.Agent:
        r"""Retrieves the specified agent.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.GetAgentRequest`):
                The request object. The request message for
                [Agents.GetAgent][google.cloud.dialogflow.v2.Agents.GetAgent].
            parent (:class:`str`):
                Required. The project that the agent to fetch is
                associated with. Format: ``projects/<Project ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Agent:
                A Dialogflow agent is a virtual agent that handles conversations with your
                   end-users. It is a natural language understanding
                   module that understands the nuances of human
                   language. Dialogflow translates end-user text or
                   audio during a conversation to structured data that
                   your apps and services can understand. You design and
                   build a Dialogflow agent to handle the types of
                   conversations required for your system.

                   For more information about agents, see the [Agent
                   guide](\ https://cloud.google.com/dialogflow/docs/agents-overview).

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

        request = agent.GetAgentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

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
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def set_agent(
        self,
        request: gcd_agent.SetAgentRequest = None,
        *,
        agent: gcd_agent.Agent = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_agent.Agent:
        r"""Creates/updates the specified agent.

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.SetAgentRequest`):
                The request object. The request message for
                [Agents.SetAgent][google.cloud.dialogflow.v2.Agents.SetAgent].
            agent (:class:`google.cloud.dialogflow_v2.types.Agent`):
                Required. The agent to update.
                This corresponds to the ``agent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Agent:
                A Dialogflow agent is a virtual agent that handles conversations with your
                   end-users. It is a natural language understanding
                   module that understands the nuances of human
                   language. Dialogflow translates end-user text or
                   audio during a conversation to structured data that
                   your apps and services can understand. You design and
                   build a Dialogflow agent to handle the types of
                   conversations required for your system.

                   For more information about agents, see the [Agent
                   guide](\ https://cloud.google.com/dialogflow/docs/agents-overview).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([agent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_agent.SetAgentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if agent is not None:
            request.agent = agent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_agent,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("agent.parent", request.agent.parent),)
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
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified agent.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.DeleteAgentRequest`):
                The request object. The request message for
                [Agents.DeleteAgent][google.cloud.dialogflow.v2.Agents.DeleteAgent].
            parent (:class:`str`):
                Required. The project that the agent to delete is
                associated with. Format: ``projects/<Project ID>``.

                This corresponds to the ``parent`` field
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
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = agent.DeleteAgentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

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
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def search_agents(
        self,
        request: agent.SearchAgentsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchAgentsAsyncPager:
        r"""Returns the list of agents.

        Since there is at most one conversational agent per project,
        this method is useful primarily for listing all agents across
        projects the caller has access to. One can achieve that with a
        wildcard project collection id "-". Refer to `List
        Sub-Collections <https://cloud.google.com/apis/design/design_patterns#list_sub-collections>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.SearchAgentsRequest`):
                The request object. The request message for
                [Agents.SearchAgents][google.cloud.dialogflow.v2.Agents.SearchAgents].
            parent (:class:`str`):
                Required. The project to list agents from. Format:
                ``projects/<Project ID or '-'>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.services.agents.pagers.SearchAgentsAsyncPager:
                The response message for
                [Agents.SearchAgents][google.cloud.dialogflow.v2.Agents.SearchAgents].

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

        request = agent.SearchAgentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_agents,
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
        response = pagers.SearchAgentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def train_agent(
        self,
        request: agent.TrainAgentRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Trains the specified agent.

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.TrainAgentRequest`):
                The request object. The request message for
                [Agents.TrainAgent][google.cloud.dialogflow.v2.Agents.TrainAgent].
            parent (:class:`str`):
                Required. The project that the agent to train is
                associated with. Format: ``projects/<Project ID>``.

                This corresponds to the ``parent`` field
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
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = agent.TrainAgentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.train_agent,
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
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

        # Done; return the response.
        return response

    async def export_agent(
        self,
        request: agent.ExportAgentRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Exports the specified agent to a ZIP file.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.ExportAgentRequest`):
                The request object. The request message for
                [Agents.ExportAgent][google.cloud.dialogflow.v2.Agents.ExportAgent].
            parent (:class:`str`):
                Required. The project that the agent to export is
                associated with. Format: ``projects/<Project ID>``.

                This corresponds to the ``parent`` field
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

                The result type for the operation will be
                :class:`google.cloud.dialogflow_v2.types.ExportAgentResponse`
                The response message for
                [Agents.ExportAgent][google.cloud.dialogflow.v2.Agents.ExportAgent].

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

        request = agent.ExportAgentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

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
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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

    async def import_agent(
        self,
        request: agent.ImportAgentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Imports the specified agent from a ZIP file.

        Uploads new intents and entity types without deleting the
        existing ones. Intents and entity types with the same name are
        replaced with the new versions from
        [ImportAgentRequest][google.cloud.dialogflow.v2.ImportAgentRequest].
        After the import, the imported draft agent will be trained
        automatically (unless disabled in agent settings). However, once
        the import is done, training may not be completed yet. Please
        call [TrainAgent][google.cloud.dialogflow.v2.Agents.TrainAgent]
        and wait for the operation it returns in order to train
        explicitly.

        An operation which tracks when importing is complete. It only
        tracks when the draft agent is updated not when it is done
        training.

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.ImportAgentRequest`):
                The request object. The request message for
                [Agents.ImportAgent][google.cloud.dialogflow.v2.Agents.ImportAgent].
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
        request = agent.ImportAgentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.import_agent,
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
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
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

        Replaces the current agent version with a new one. All the
        intents and entity types in the older version are deleted. After
        the restore, the restored draft agent will be trained
        automatically (unless disabled in agent settings). However, once
        the restore is done, training may not be completed yet. Please
        call [TrainAgent][google.cloud.dialogflow.v2.Agents.TrainAgent]
        and wait for the operation it returns in order to train
        explicitly.

        An operation which tracks when restoring is complete. It only
        tracks when the draft agent is updated not when it is done
        training.

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.RestoreAgentRequest`):
                The request object. The request message for
                [Agents.RestoreAgent][google.cloud.dialogflow.v2.Agents.RestoreAgent].
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
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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

    async def get_validation_result(
        self,
        request: agent.GetValidationResultRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> validation_result.ValidationResult:
        r"""Gets agent validation result. Agent validation is
        performed during training time and is updated
        automatically when training is completed.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.GetValidationResultRequest`):
                The request object. The request message for
                [Agents.GetValidationResult][google.cloud.dialogflow.v2.Agents.GetValidationResult].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.ValidationResult:
                Represents the output of agent
                validation.

        """
        # Create or coerce a protobuf request object.
        request = agent.GetValidationResultRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_validation_result,
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflow",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("AgentsAsyncClient",)
