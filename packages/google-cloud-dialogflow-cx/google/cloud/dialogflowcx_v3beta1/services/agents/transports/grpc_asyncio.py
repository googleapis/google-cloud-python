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

from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.dialogflowcx_v3beta1.types import agent
from google.cloud.dialogflowcx_v3beta1.types import agent as gcdc_agent
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import AgentsTransport, DEFAULT_CLIENT_INFO
from .grpc import AgentsGrpcTransport


class AgentsGrpcAsyncIOTransport(AgentsTransport):
    """gRPC AsyncIO backend transport for Agents.

    Service for managing
    [Agents][google.cloud.dialogflow.cx.v3beta1.Agent].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "dialogflow.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

        self._stubs = {}

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def list_agents(
        self,
    ) -> Callable[[agent.ListAgentsRequest], Awaitable[agent.ListAgentsResponse]]:
        r"""Return a callable for the list agents method over gRPC.

        Returns the list of all agents in the specified
        location.

        Returns:
            Callable[[~.ListAgentsRequest],
                    Awaitable[~.ListAgentsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_agents" not in self._stubs:
            self._stubs["list_agents"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.Agents/ListAgents",
                request_serializer=agent.ListAgentsRequest.serialize,
                response_deserializer=agent.ListAgentsResponse.deserialize,
            )
        return self._stubs["list_agents"]

    @property
    def get_agent(self) -> Callable[[agent.GetAgentRequest], Awaitable[agent.Agent]]:
        r"""Return a callable for the get agent method over gRPC.

        Retrieves the specified agent.

        Returns:
            Callable[[~.GetAgentRequest],
                    Awaitable[~.Agent]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_agent" not in self._stubs:
            self._stubs["get_agent"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.Agents/GetAgent",
                request_serializer=agent.GetAgentRequest.serialize,
                response_deserializer=agent.Agent.deserialize,
            )
        return self._stubs["get_agent"]

    @property
    def create_agent(
        self,
    ) -> Callable[[gcdc_agent.CreateAgentRequest], Awaitable[gcdc_agent.Agent]]:
        r"""Return a callable for the create agent method over gRPC.

        Creates an agent in the specified location.

        Returns:
            Callable[[~.CreateAgentRequest],
                    Awaitable[~.Agent]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_agent" not in self._stubs:
            self._stubs["create_agent"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.Agents/CreateAgent",
                request_serializer=gcdc_agent.CreateAgentRequest.serialize,
                response_deserializer=gcdc_agent.Agent.deserialize,
            )
        return self._stubs["create_agent"]

    @property
    def update_agent(
        self,
    ) -> Callable[[gcdc_agent.UpdateAgentRequest], Awaitable[gcdc_agent.Agent]]:
        r"""Return a callable for the update agent method over gRPC.

        Updates the specified agent.

        Returns:
            Callable[[~.UpdateAgentRequest],
                    Awaitable[~.Agent]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_agent" not in self._stubs:
            self._stubs["update_agent"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.Agents/UpdateAgent",
                request_serializer=gcdc_agent.UpdateAgentRequest.serialize,
                response_deserializer=gcdc_agent.Agent.deserialize,
            )
        return self._stubs["update_agent"]

    @property
    def delete_agent(
        self,
    ) -> Callable[[agent.DeleteAgentRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete agent method over gRPC.

        Deletes the specified agent.

        Returns:
            Callable[[~.DeleteAgentRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_agent" not in self._stubs:
            self._stubs["delete_agent"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.Agents/DeleteAgent",
                request_serializer=agent.DeleteAgentRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_agent"]

    @property
    def export_agent(
        self,
    ) -> Callable[[agent.ExportAgentRequest], Awaitable[operations.Operation]]:
        r"""Return a callable for the export agent method over gRPC.

        Exports the specified agent to a ZIP file.

        Returns:
            Callable[[~.ExportAgentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_agent" not in self._stubs:
            self._stubs["export_agent"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.Agents/ExportAgent",
                request_serializer=agent.ExportAgentRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["export_agent"]

    @property
    def restore_agent(
        self,
    ) -> Callable[[agent.RestoreAgentRequest], Awaitable[operations.Operation]]:
        r"""Return a callable for the restore agent method over gRPC.

        Restores the specified agent from a ZIP file.
        Note that all existing intents, intent routes, entity
        types, pages and webhooks in the agent will be deleted.

        Returns:
            Callable[[~.RestoreAgentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restore_agent" not in self._stubs:
            self._stubs["restore_agent"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.Agents/RestoreAgent",
                request_serializer=agent.RestoreAgentRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["restore_agent"]


__all__ = ("AgentsGrpcAsyncIOTransport",)
