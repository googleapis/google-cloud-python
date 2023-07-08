# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.api_core import gapic_v1, grpc_helpers, operations_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore

from google.cloud.datacatalog.lineage_v1.types import lineage

from .base import DEFAULT_CLIENT_INFO, LineageTransport


class LineageGrpcTransport(LineageTransport):
    """gRPC backend transport for Lineage.

    Lineage is used to track data flows between assets over time. You
    can create
    [LineageEvents][google.cloud.datacatalog.lineage.v1.LineageEvent] to
    record lineage between multiple sources and a single target, for
    example, when table data is based on data from multiple tables.

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
        host: str = "datalineage.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[grpc.Channel] = None,
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
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
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
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsClient] = None

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
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
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
        host: str = "datalineage.googleapis.com",
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
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(self.grpc_channel)

        # Return the client from cache.
        return self._operations_client

    @property
    def create_process(
        self,
    ) -> Callable[[lineage.CreateProcessRequest], lineage.Process]:
        r"""Return a callable for the create process method over gRPC.

        Creates a new process.

        Returns:
            Callable[[~.CreateProcessRequest],
                    ~.Process]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_process" not in self._stubs:
            self._stubs["create_process"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/CreateProcess",
                request_serializer=lineage.CreateProcessRequest.serialize,
                response_deserializer=lineage.Process.deserialize,
            )
        return self._stubs["create_process"]

    @property
    def update_process(
        self,
    ) -> Callable[[lineage.UpdateProcessRequest], lineage.Process]:
        r"""Return a callable for the update process method over gRPC.

        Updates a process.

        Returns:
            Callable[[~.UpdateProcessRequest],
                    ~.Process]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_process" not in self._stubs:
            self._stubs["update_process"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/UpdateProcess",
                request_serializer=lineage.UpdateProcessRequest.serialize,
                response_deserializer=lineage.Process.deserialize,
            )
        return self._stubs["update_process"]

    @property
    def get_process(self) -> Callable[[lineage.GetProcessRequest], lineage.Process]:
        r"""Return a callable for the get process method over gRPC.

        Gets the details of the specified process.

        Returns:
            Callable[[~.GetProcessRequest],
                    ~.Process]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_process" not in self._stubs:
            self._stubs["get_process"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/GetProcess",
                request_serializer=lineage.GetProcessRequest.serialize,
                response_deserializer=lineage.Process.deserialize,
            )
        return self._stubs["get_process"]

    @property
    def list_processes(
        self,
    ) -> Callable[[lineage.ListProcessesRequest], lineage.ListProcessesResponse]:
        r"""Return a callable for the list processes method over gRPC.

        List processes in the given project and location.
        List order is descending by insertion time.

        Returns:
            Callable[[~.ListProcessesRequest],
                    ~.ListProcessesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_processes" not in self._stubs:
            self._stubs["list_processes"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/ListProcesses",
                request_serializer=lineage.ListProcessesRequest.serialize,
                response_deserializer=lineage.ListProcessesResponse.deserialize,
            )
        return self._stubs["list_processes"]

    @property
    def delete_process(
        self,
    ) -> Callable[[lineage.DeleteProcessRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete process method over gRPC.

        Deletes the process with the specified name.

        Returns:
            Callable[[~.DeleteProcessRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_process" not in self._stubs:
            self._stubs["delete_process"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/DeleteProcess",
                request_serializer=lineage.DeleteProcessRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_process"]

    @property
    def create_run(self) -> Callable[[lineage.CreateRunRequest], lineage.Run]:
        r"""Return a callable for the create run method over gRPC.

        Creates a new run.

        Returns:
            Callable[[~.CreateRunRequest],
                    ~.Run]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_run" not in self._stubs:
            self._stubs["create_run"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/CreateRun",
                request_serializer=lineage.CreateRunRequest.serialize,
                response_deserializer=lineage.Run.deserialize,
            )
        return self._stubs["create_run"]

    @property
    def update_run(self) -> Callable[[lineage.UpdateRunRequest], lineage.Run]:
        r"""Return a callable for the update run method over gRPC.

        Updates a run.

        Returns:
            Callable[[~.UpdateRunRequest],
                    ~.Run]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_run" not in self._stubs:
            self._stubs["update_run"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/UpdateRun",
                request_serializer=lineage.UpdateRunRequest.serialize,
                response_deserializer=lineage.Run.deserialize,
            )
        return self._stubs["update_run"]

    @property
    def get_run(self) -> Callable[[lineage.GetRunRequest], lineage.Run]:
        r"""Return a callable for the get run method over gRPC.

        Gets the details of the specified run.

        Returns:
            Callable[[~.GetRunRequest],
                    ~.Run]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_run" not in self._stubs:
            self._stubs["get_run"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/GetRun",
                request_serializer=lineage.GetRunRequest.serialize,
                response_deserializer=lineage.Run.deserialize,
            )
        return self._stubs["get_run"]

    @property
    def list_runs(
        self,
    ) -> Callable[[lineage.ListRunsRequest], lineage.ListRunsResponse]:
        r"""Return a callable for the list runs method over gRPC.

        Lists runs in the given project and location. List order is
        descending by ``start_time``.

        Returns:
            Callable[[~.ListRunsRequest],
                    ~.ListRunsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_runs" not in self._stubs:
            self._stubs["list_runs"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/ListRuns",
                request_serializer=lineage.ListRunsRequest.serialize,
                response_deserializer=lineage.ListRunsResponse.deserialize,
            )
        return self._stubs["list_runs"]

    @property
    def delete_run(
        self,
    ) -> Callable[[lineage.DeleteRunRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete run method over gRPC.

        Deletes the run with the specified name.

        Returns:
            Callable[[~.DeleteRunRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_run" not in self._stubs:
            self._stubs["delete_run"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/DeleteRun",
                request_serializer=lineage.DeleteRunRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_run"]

    @property
    def create_lineage_event(
        self,
    ) -> Callable[[lineage.CreateLineageEventRequest], lineage.LineageEvent]:
        r"""Return a callable for the create lineage event method over gRPC.

        Creates a new lineage event.

        Returns:
            Callable[[~.CreateLineageEventRequest],
                    ~.LineageEvent]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_lineage_event" not in self._stubs:
            self._stubs["create_lineage_event"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/CreateLineageEvent",
                request_serializer=lineage.CreateLineageEventRequest.serialize,
                response_deserializer=lineage.LineageEvent.deserialize,
            )
        return self._stubs["create_lineage_event"]

    @property
    def get_lineage_event(
        self,
    ) -> Callable[[lineage.GetLineageEventRequest], lineage.LineageEvent]:
        r"""Return a callable for the get lineage event method over gRPC.

        Gets details of a specified lineage event.

        Returns:
            Callable[[~.GetLineageEventRequest],
                    ~.LineageEvent]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_lineage_event" not in self._stubs:
            self._stubs["get_lineage_event"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/GetLineageEvent",
                request_serializer=lineage.GetLineageEventRequest.serialize,
                response_deserializer=lineage.LineageEvent.deserialize,
            )
        return self._stubs["get_lineage_event"]

    @property
    def list_lineage_events(
        self,
    ) -> Callable[
        [lineage.ListLineageEventsRequest], lineage.ListLineageEventsResponse
    ]:
        r"""Return a callable for the list lineage events method over gRPC.

        Lists lineage events in the given project and
        location. The list order is not defined.

        Returns:
            Callable[[~.ListLineageEventsRequest],
                    ~.ListLineageEventsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_lineage_events" not in self._stubs:
            self._stubs["list_lineage_events"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/ListLineageEvents",
                request_serializer=lineage.ListLineageEventsRequest.serialize,
                response_deserializer=lineage.ListLineageEventsResponse.deserialize,
            )
        return self._stubs["list_lineage_events"]

    @property
    def delete_lineage_event(
        self,
    ) -> Callable[[lineage.DeleteLineageEventRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete lineage event method over gRPC.

        Deletes the lineage event with the specified name.

        Returns:
            Callable[[~.DeleteLineageEventRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_lineage_event" not in self._stubs:
            self._stubs["delete_lineage_event"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/DeleteLineageEvent",
                request_serializer=lineage.DeleteLineageEventRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_lineage_event"]

    @property
    def search_links(
        self,
    ) -> Callable[[lineage.SearchLinksRequest], lineage.SearchLinksResponse]:
        r"""Return a callable for the search links method over gRPC.

        Retrieve a list of links connected to a specific asset. Links
        represent the data flow between **source** (upstream) and
        **target** (downstream) assets in transformation pipelines.
        Links are stored in the same project as the Lineage Events that
        create them.

        You can retrieve links in every project where you have the
        ``datalineage.events.get`` permission. The project provided in
        the URL is used for Billing and Quota.

        Returns:
            Callable[[~.SearchLinksRequest],
                    ~.SearchLinksResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_links" not in self._stubs:
            self._stubs["search_links"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/SearchLinks",
                request_serializer=lineage.SearchLinksRequest.serialize,
                response_deserializer=lineage.SearchLinksResponse.deserialize,
            )
        return self._stubs["search_links"]

    @property
    def batch_search_link_processes(
        self,
    ) -> Callable[
        [lineage.BatchSearchLinkProcessesRequest],
        lineage.BatchSearchLinkProcessesResponse,
    ]:
        r"""Return a callable for the batch search link processes method over gRPC.

        Retrieve information about LineageProcesses associated with
        specific links. LineageProcesses are transformation pipelines
        that result in data flowing from **source** to **target**
        assets. Links between assets represent this operation.

        If you have specific link names, you can use this method to
        verify which LineageProcesses contribute to creating those
        links. See the
        [SearchLinks][google.cloud.datacatalog.lineage.v1.Lineage.SearchLinks]
        method for more information on how to retrieve link name.

        You can retrieve the LineageProcess information in every project
        where you have the ``datalineage.events.get`` permission. The
        project provided in the URL is used for Billing and Quota.

        Returns:
            Callable[[~.BatchSearchLinkProcessesRequest],
                    ~.BatchSearchLinkProcessesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_search_link_processes" not in self._stubs:
            self._stubs["batch_search_link_processes"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.lineage.v1.Lineage/BatchSearchLinkProcesses",
                request_serializer=lineage.BatchSearchLinkProcessesRequest.serialize,
                response_deserializer=lineage.BatchSearchLinkProcessesResponse.deserialize,
            )
        return self._stubs["batch_search_link_processes"]

    def close(self):
        self.grpc_channel.close()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("LineageGrpcTransport",)
