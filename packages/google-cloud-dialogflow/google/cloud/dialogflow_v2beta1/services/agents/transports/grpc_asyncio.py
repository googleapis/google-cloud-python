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
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import packaging.version

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.dialogflow_v2beta1.types import agent
from google.cloud.dialogflow_v2beta1.types import agent as gcd_agent
from google.cloud.dialogflow_v2beta1.types import validation_result
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from .base import AgentsTransport, DEFAULT_CLIENT_INFO
from .grpc import AgentsGrpcTransport


class AgentsGrpcAsyncIOTransport(AgentsTransport):
    """gRPC AsyncIO backend transport for Agents.

    Service for managing
    [Agents][google.cloud.dialogflow.v2beta1.Agent].

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
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
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

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
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
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

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
                "/google.cloud.dialogflow.v2beta1.Agents/GetAgent",
                request_serializer=agent.GetAgentRequest.serialize,
                response_deserializer=agent.Agent.deserialize,
            )
        return self._stubs["get_agent"]

    @property
    def set_agent(
        self,
    ) -> Callable[[gcd_agent.SetAgentRequest], Awaitable[gcd_agent.Agent]]:
        r"""Return a callable for the set agent method over gRPC.

        Creates/updates the specified agent.

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Returns:
            Callable[[~.SetAgentRequest],
                    Awaitable[~.Agent]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_agent" not in self._stubs:
            self._stubs["set_agent"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2beta1.Agents/SetAgent",
                request_serializer=gcd_agent.SetAgentRequest.serialize,
                response_deserializer=gcd_agent.Agent.deserialize,
            )
        return self._stubs["set_agent"]

    @property
    def delete_agent(
        self,
    ) -> Callable[[agent.DeleteAgentRequest], Awaitable[empty_pb2.Empty]]:
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
                "/google.cloud.dialogflow.v2beta1.Agents/DeleteAgent",
                request_serializer=agent.DeleteAgentRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_agent"]

    @property
    def search_agents(
        self,
    ) -> Callable[[agent.SearchAgentsRequest], Awaitable[agent.SearchAgentsResponse]]:
        r"""Return a callable for the search agents method over gRPC.

        Returns the list of agents. Since there is at most one
        conversational agent per project, this method is useful
        primarily for listing all agents across projects the caller has
        access to. One can achieve that with a wildcard project
        collection id "-". Refer to `List
        Sub-Collections <https://cloud.google.com/apis/design/design_patterns#list_sub-collections>`__.

        Returns:
            Callable[[~.SearchAgentsRequest],
                    Awaitable[~.SearchAgentsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_agents" not in self._stubs:
            self._stubs["search_agents"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2beta1.Agents/SearchAgents",
                request_serializer=agent.SearchAgentsRequest.serialize,
                response_deserializer=agent.SearchAgentsResponse.deserialize,
            )
        return self._stubs["search_agents"]

    @property
    def train_agent(
        self,
    ) -> Callable[[agent.TrainAgentRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the train agent method over gRPC.

        Trains the specified agent.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/es/docs/how/long-running-operations>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``: An empty `Struct
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct>`__
        -  ``response``: An `Empty
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#empty>`__

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Returns:
            Callable[[~.TrainAgentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "train_agent" not in self._stubs:
            self._stubs["train_agent"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2beta1.Agents/TrainAgent",
                request_serializer=agent.TrainAgentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["train_agent"]

    @property
    def export_agent(
        self,
    ) -> Callable[[agent.ExportAgentRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the export agent method over gRPC.

        Exports the specified agent to a ZIP file.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/es/docs/how/long-running-operations>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``: An empty `Struct
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct>`__
        -  ``response``:
           [ExportAgentResponse][google.cloud.dialogflow.v2beta1.ExportAgentResponse]

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
                "/google.cloud.dialogflow.v2beta1.Agents/ExportAgent",
                request_serializer=agent.ExportAgentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_agent"]

    @property
    def import_agent(
        self,
    ) -> Callable[[agent.ImportAgentRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the import agent method over gRPC.

        Imports the specified agent from a ZIP file.

        Uploads new intents and entity types without deleting the
        existing ones. Intents and entity types with the same name are
        replaced with the new versions from
        [ImportAgentRequest][google.cloud.dialogflow.v2beta1.ImportAgentRequest].
        After the import, the imported draft agent will be trained
        automatically (unless disabled in agent settings). However, once
        the import is done, training may not be completed yet. Please
        call
        [TrainAgent][google.cloud.dialogflow.v2beta1.Agents.TrainAgent]
        and wait for the operation it returns in order to train
        explicitly.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/es/docs/how/long-running-operations>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``: An empty `Struct
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct>`__
        -  ``response``: An `Empty
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#empty>`__

        The operation only tracks when importing is complete, not when
        it is done training.

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Returns:
            Callable[[~.ImportAgentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_agent" not in self._stubs:
            self._stubs["import_agent"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2beta1.Agents/ImportAgent",
                request_serializer=agent.ImportAgentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_agent"]

    @property
    def restore_agent(
        self,
    ) -> Callable[[agent.RestoreAgentRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the restore agent method over gRPC.

        Restores the specified agent from a ZIP file.

        Replaces the current agent version with a new one. All the
        intents and entity types in the older version are deleted. After
        the restore, the restored draft agent will be trained
        automatically (unless disabled in agent settings). However, once
        the restore is done, training may not be completed yet. Please
        call
        [TrainAgent][google.cloud.dialogflow.v2beta1.Agents.TrainAgent]
        and wait for the operation it returns in order to train
        explicitly.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/es/docs/how/long-running-operations>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``: An empty `Struct
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct>`__
        -  ``response``: An `Empty
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#empty>`__

        The operation only tracks when restoring is complete, not when
        it is done training.

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

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
                "/google.cloud.dialogflow.v2beta1.Agents/RestoreAgent",
                request_serializer=agent.RestoreAgentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restore_agent"]

    @property
    def get_validation_result(
        self,
    ) -> Callable[
        [agent.GetValidationResultRequest],
        Awaitable[validation_result.ValidationResult],
    ]:
        r"""Return a callable for the get validation result method over gRPC.

        Gets agent validation result. Agent validation is
        performed during training time and is updated
        automatically when training is completed.

        Returns:
            Callable[[~.GetValidationResultRequest],
                    Awaitable[~.ValidationResult]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_validation_result" not in self._stubs:
            self._stubs["get_validation_result"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.v2beta1.Agents/GetValidationResult",
                request_serializer=agent.GetValidationResultRequest.serialize,
                response_deserializer=validation_result.ValidationResult.deserialize,
            )
        return self._stubs["get_validation_result"]


__all__ = ("AgentsGrpcAsyncIOTransport",)
