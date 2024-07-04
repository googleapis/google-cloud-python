# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore

from google.cloud.bigquery_migration_v2.types import (
    migration_entities,
    migration_service,
)

from .base import DEFAULT_CLIENT_INFO, MigrationServiceTransport


class MigrationServiceGrpcTransport(MigrationServiceTransport):
    """gRPC backend transport for MigrationService.

    Service to handle EDW migrations.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "bigquerymigration.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'bigquerymigration.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
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
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, grpc.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
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
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
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

    @classmethod
    def create_channel(
        cls,
        host: str = "bigquerymigration.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def create_migration_workflow(
        self,
    ) -> Callable[
        [migration_service.CreateMigrationWorkflowRequest],
        migration_entities.MigrationWorkflow,
    ]:
        r"""Return a callable for the create migration workflow method over gRPC.

        Creates a migration workflow.

        Returns:
            Callable[[~.CreateMigrationWorkflowRequest],
                    ~.MigrationWorkflow]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_migration_workflow" not in self._stubs:
            self._stubs["create_migration_workflow"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.migration.v2.MigrationService/CreateMigrationWorkflow",
                request_serializer=migration_service.CreateMigrationWorkflowRequest.serialize,
                response_deserializer=migration_entities.MigrationWorkflow.deserialize,
            )
        return self._stubs["create_migration_workflow"]

    @property
    def get_migration_workflow(
        self,
    ) -> Callable[
        [migration_service.GetMigrationWorkflowRequest],
        migration_entities.MigrationWorkflow,
    ]:
        r"""Return a callable for the get migration workflow method over gRPC.

        Gets a previously created migration workflow.

        Returns:
            Callable[[~.GetMigrationWorkflowRequest],
                    ~.MigrationWorkflow]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_migration_workflow" not in self._stubs:
            self._stubs["get_migration_workflow"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.migration.v2.MigrationService/GetMigrationWorkflow",
                request_serializer=migration_service.GetMigrationWorkflowRequest.serialize,
                response_deserializer=migration_entities.MigrationWorkflow.deserialize,
            )
        return self._stubs["get_migration_workflow"]

    @property
    def list_migration_workflows(
        self,
    ) -> Callable[
        [migration_service.ListMigrationWorkflowsRequest],
        migration_service.ListMigrationWorkflowsResponse,
    ]:
        r"""Return a callable for the list migration workflows method over gRPC.

        Lists previously created migration workflow.

        Returns:
            Callable[[~.ListMigrationWorkflowsRequest],
                    ~.ListMigrationWorkflowsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_migration_workflows" not in self._stubs:
            self._stubs["list_migration_workflows"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.migration.v2.MigrationService/ListMigrationWorkflows",
                request_serializer=migration_service.ListMigrationWorkflowsRequest.serialize,
                response_deserializer=migration_service.ListMigrationWorkflowsResponse.deserialize,
            )
        return self._stubs["list_migration_workflows"]

    @property
    def delete_migration_workflow(
        self,
    ) -> Callable[[migration_service.DeleteMigrationWorkflowRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete migration workflow method over gRPC.

        Deletes a migration workflow by name.

        Returns:
            Callable[[~.DeleteMigrationWorkflowRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_migration_workflow" not in self._stubs:
            self._stubs["delete_migration_workflow"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.migration.v2.MigrationService/DeleteMigrationWorkflow",
                request_serializer=migration_service.DeleteMigrationWorkflowRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_migration_workflow"]

    @property
    def start_migration_workflow(
        self,
    ) -> Callable[[migration_service.StartMigrationWorkflowRequest], empty_pb2.Empty]:
        r"""Return a callable for the start migration workflow method over gRPC.

        Starts a previously created migration workflow. I.e.,
        the state transitions from DRAFT to RUNNING. This is a
        no-op if the state is already RUNNING. An error will be
        signaled if the state is anything other than DRAFT or
        RUNNING.

        Returns:
            Callable[[~.StartMigrationWorkflowRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_migration_workflow" not in self._stubs:
            self._stubs["start_migration_workflow"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.migration.v2.MigrationService/StartMigrationWorkflow",
                request_serializer=migration_service.StartMigrationWorkflowRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["start_migration_workflow"]

    @property
    def get_migration_subtask(
        self,
    ) -> Callable[
        [migration_service.GetMigrationSubtaskRequest],
        migration_entities.MigrationSubtask,
    ]:
        r"""Return a callable for the get migration subtask method over gRPC.

        Gets a previously created migration subtask.

        Returns:
            Callable[[~.GetMigrationSubtaskRequest],
                    ~.MigrationSubtask]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_migration_subtask" not in self._stubs:
            self._stubs["get_migration_subtask"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.migration.v2.MigrationService/GetMigrationSubtask",
                request_serializer=migration_service.GetMigrationSubtaskRequest.serialize,
                response_deserializer=migration_entities.MigrationSubtask.deserialize,
            )
        return self._stubs["get_migration_subtask"]

    @property
    def list_migration_subtasks(
        self,
    ) -> Callable[
        [migration_service.ListMigrationSubtasksRequest],
        migration_service.ListMigrationSubtasksResponse,
    ]:
        r"""Return a callable for the list migration subtasks method over gRPC.

        Lists previously created migration subtasks.

        Returns:
            Callable[[~.ListMigrationSubtasksRequest],
                    ~.ListMigrationSubtasksResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_migration_subtasks" not in self._stubs:
            self._stubs["list_migration_subtasks"] = self.grpc_channel.unary_unary(
                "/google.cloud.bigquery.migration.v2.MigrationService/ListMigrationSubtasks",
                request_serializer=migration_service.ListMigrationSubtasksRequest.serialize,
                response_deserializer=migration_service.ListMigrationSubtasksResponse.deserialize,
            )
        return self._stubs["list_migration_subtasks"]

    def close(self):
        self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("MigrationServiceGrpcTransport",)
