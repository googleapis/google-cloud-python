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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.vmmigration_v1.types import vmmigration

from .base import DEFAULT_CLIENT_INFO, VmMigrationTransport
from .grpc import VmMigrationGrpcTransport


class VmMigrationGrpcAsyncIOTransport(VmMigrationTransport):
    """gRPC AsyncIO backend transport for VmMigration.

    VM Migration Service

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
        host: str = "vmmigration.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
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
        host: str = "vmmigration.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[aio.Channel] = None,
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
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
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
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

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
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def list_sources(
        self,
    ) -> Callable[
        [vmmigration.ListSourcesRequest], Awaitable[vmmigration.ListSourcesResponse]
    ]:
        r"""Return a callable for the list sources method over gRPC.

        Lists Sources in a given project and location.

        Returns:
            Callable[[~.ListSourcesRequest],
                    Awaitable[~.ListSourcesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_sources" not in self._stubs:
            self._stubs["list_sources"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/ListSources",
                request_serializer=vmmigration.ListSourcesRequest.serialize,
                response_deserializer=vmmigration.ListSourcesResponse.deserialize,
            )
        return self._stubs["list_sources"]

    @property
    def get_source(
        self,
    ) -> Callable[[vmmigration.GetSourceRequest], Awaitable[vmmigration.Source]]:
        r"""Return a callable for the get source method over gRPC.

        Gets details of a single Source.

        Returns:
            Callable[[~.GetSourceRequest],
                    Awaitable[~.Source]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_source" not in self._stubs:
            self._stubs["get_source"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/GetSource",
                request_serializer=vmmigration.GetSourceRequest.serialize,
                response_deserializer=vmmigration.Source.deserialize,
            )
        return self._stubs["get_source"]

    @property
    def create_source(
        self,
    ) -> Callable[
        [vmmigration.CreateSourceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create source method over gRPC.

        Creates a new Source in a given project and location.

        Returns:
            Callable[[~.CreateSourceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_source" not in self._stubs:
            self._stubs["create_source"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/CreateSource",
                request_serializer=vmmigration.CreateSourceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_source"]

    @property
    def update_source(
        self,
    ) -> Callable[
        [vmmigration.UpdateSourceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update source method over gRPC.

        Updates the parameters of a single Source.

        Returns:
            Callable[[~.UpdateSourceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_source" not in self._stubs:
            self._stubs["update_source"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/UpdateSource",
                request_serializer=vmmigration.UpdateSourceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_source"]

    @property
    def delete_source(
        self,
    ) -> Callable[
        [vmmigration.DeleteSourceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete source method over gRPC.

        Deletes a single Source.

        Returns:
            Callable[[~.DeleteSourceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_source" not in self._stubs:
            self._stubs["delete_source"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/DeleteSource",
                request_serializer=vmmigration.DeleteSourceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_source"]

    @property
    def fetch_inventory(
        self,
    ) -> Callable[
        [vmmigration.FetchInventoryRequest],
        Awaitable[vmmigration.FetchInventoryResponse],
    ]:
        r"""Return a callable for the fetch inventory method over gRPC.

        List remote source's inventory of VMs.
        The remote source is the onprem vCenter (remote in the
        sense it's not in Compute Engine). The inventory
        describes the list of existing VMs in that source. Note
        that this operation lists the VMs on the remote source,
        as opposed to listing the MigratingVms resources in the
        vmmigration service.

        Returns:
            Callable[[~.FetchInventoryRequest],
                    Awaitable[~.FetchInventoryResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_inventory" not in self._stubs:
            self._stubs["fetch_inventory"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/FetchInventory",
                request_serializer=vmmigration.FetchInventoryRequest.serialize,
                response_deserializer=vmmigration.FetchInventoryResponse.deserialize,
            )
        return self._stubs["fetch_inventory"]

    @property
    def list_utilization_reports(
        self,
    ) -> Callable[
        [vmmigration.ListUtilizationReportsRequest],
        Awaitable[vmmigration.ListUtilizationReportsResponse],
    ]:
        r"""Return a callable for the list utilization reports method over gRPC.

        Lists Utilization Reports of the given Source.

        Returns:
            Callable[[~.ListUtilizationReportsRequest],
                    Awaitable[~.ListUtilizationReportsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_utilization_reports" not in self._stubs:
            self._stubs["list_utilization_reports"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/ListUtilizationReports",
                request_serializer=vmmigration.ListUtilizationReportsRequest.serialize,
                response_deserializer=vmmigration.ListUtilizationReportsResponse.deserialize,
            )
        return self._stubs["list_utilization_reports"]

    @property
    def get_utilization_report(
        self,
    ) -> Callable[
        [vmmigration.GetUtilizationReportRequest],
        Awaitable[vmmigration.UtilizationReport],
    ]:
        r"""Return a callable for the get utilization report method over gRPC.

        Gets a single Utilization Report.

        Returns:
            Callable[[~.GetUtilizationReportRequest],
                    Awaitable[~.UtilizationReport]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_utilization_report" not in self._stubs:
            self._stubs["get_utilization_report"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/GetUtilizationReport",
                request_serializer=vmmigration.GetUtilizationReportRequest.serialize,
                response_deserializer=vmmigration.UtilizationReport.deserialize,
            )
        return self._stubs["get_utilization_report"]

    @property
    def create_utilization_report(
        self,
    ) -> Callable[
        [vmmigration.CreateUtilizationReportRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create utilization report method over gRPC.

        Creates a new UtilizationReport.

        Returns:
            Callable[[~.CreateUtilizationReportRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_utilization_report" not in self._stubs:
            self._stubs["create_utilization_report"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/CreateUtilizationReport",
                request_serializer=vmmigration.CreateUtilizationReportRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_utilization_report"]

    @property
    def delete_utilization_report(
        self,
    ) -> Callable[
        [vmmigration.DeleteUtilizationReportRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete utilization report method over gRPC.

        Deletes a single Utilization Report.

        Returns:
            Callable[[~.DeleteUtilizationReportRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_utilization_report" not in self._stubs:
            self._stubs["delete_utilization_report"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/DeleteUtilizationReport",
                request_serializer=vmmigration.DeleteUtilizationReportRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_utilization_report"]

    @property
    def list_datacenter_connectors(
        self,
    ) -> Callable[
        [vmmigration.ListDatacenterConnectorsRequest],
        Awaitable[vmmigration.ListDatacenterConnectorsResponse],
    ]:
        r"""Return a callable for the list datacenter connectors method over gRPC.

        Lists DatacenterConnectors in a given Source.

        Returns:
            Callable[[~.ListDatacenterConnectorsRequest],
                    Awaitable[~.ListDatacenterConnectorsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_datacenter_connectors" not in self._stubs:
            self._stubs["list_datacenter_connectors"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/ListDatacenterConnectors",
                request_serializer=vmmigration.ListDatacenterConnectorsRequest.serialize,
                response_deserializer=vmmigration.ListDatacenterConnectorsResponse.deserialize,
            )
        return self._stubs["list_datacenter_connectors"]

    @property
    def get_datacenter_connector(
        self,
    ) -> Callable[
        [vmmigration.GetDatacenterConnectorRequest],
        Awaitable[vmmigration.DatacenterConnector],
    ]:
        r"""Return a callable for the get datacenter connector method over gRPC.

        Gets details of a single DatacenterConnector.

        Returns:
            Callable[[~.GetDatacenterConnectorRequest],
                    Awaitable[~.DatacenterConnector]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_datacenter_connector" not in self._stubs:
            self._stubs["get_datacenter_connector"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/GetDatacenterConnector",
                request_serializer=vmmigration.GetDatacenterConnectorRequest.serialize,
                response_deserializer=vmmigration.DatacenterConnector.deserialize,
            )
        return self._stubs["get_datacenter_connector"]

    @property
    def create_datacenter_connector(
        self,
    ) -> Callable[
        [vmmigration.CreateDatacenterConnectorRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create datacenter connector method over gRPC.

        Creates a new DatacenterConnector in a given Source.

        Returns:
            Callable[[~.CreateDatacenterConnectorRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_datacenter_connector" not in self._stubs:
            self._stubs["create_datacenter_connector"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/CreateDatacenterConnector",
                request_serializer=vmmigration.CreateDatacenterConnectorRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_datacenter_connector"]

    @property
    def delete_datacenter_connector(
        self,
    ) -> Callable[
        [vmmigration.DeleteDatacenterConnectorRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete datacenter connector method over gRPC.

        Deletes a single DatacenterConnector.

        Returns:
            Callable[[~.DeleteDatacenterConnectorRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_datacenter_connector" not in self._stubs:
            self._stubs["delete_datacenter_connector"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/DeleteDatacenterConnector",
                request_serializer=vmmigration.DeleteDatacenterConnectorRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_datacenter_connector"]

    @property
    def upgrade_appliance(
        self,
    ) -> Callable[
        [vmmigration.UpgradeApplianceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the upgrade appliance method over gRPC.

        Upgrades the appliance relate to this
        DatacenterConnector to the in-place updateable version.

        Returns:
            Callable[[~.UpgradeApplianceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "upgrade_appliance" not in self._stubs:
            self._stubs["upgrade_appliance"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/UpgradeAppliance",
                request_serializer=vmmigration.UpgradeApplianceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["upgrade_appliance"]

    @property
    def create_migrating_vm(
        self,
    ) -> Callable[
        [vmmigration.CreateMigratingVmRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create migrating vm method over gRPC.

        Creates a new MigratingVm in a given Source.

        Returns:
            Callable[[~.CreateMigratingVmRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_migrating_vm" not in self._stubs:
            self._stubs["create_migrating_vm"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/CreateMigratingVm",
                request_serializer=vmmigration.CreateMigratingVmRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_migrating_vm"]

    @property
    def list_migrating_vms(
        self,
    ) -> Callable[
        [vmmigration.ListMigratingVmsRequest],
        Awaitable[vmmigration.ListMigratingVmsResponse],
    ]:
        r"""Return a callable for the list migrating vms method over gRPC.

        Lists MigratingVms in a given Source.

        Returns:
            Callable[[~.ListMigratingVmsRequest],
                    Awaitable[~.ListMigratingVmsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_migrating_vms" not in self._stubs:
            self._stubs["list_migrating_vms"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/ListMigratingVms",
                request_serializer=vmmigration.ListMigratingVmsRequest.serialize,
                response_deserializer=vmmigration.ListMigratingVmsResponse.deserialize,
            )
        return self._stubs["list_migrating_vms"]

    @property
    def get_migrating_vm(
        self,
    ) -> Callable[
        [vmmigration.GetMigratingVmRequest], Awaitable[vmmigration.MigratingVm]
    ]:
        r"""Return a callable for the get migrating vm method over gRPC.

        Gets details of a single MigratingVm.

        Returns:
            Callable[[~.GetMigratingVmRequest],
                    Awaitable[~.MigratingVm]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_migrating_vm" not in self._stubs:
            self._stubs["get_migrating_vm"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/GetMigratingVm",
                request_serializer=vmmigration.GetMigratingVmRequest.serialize,
                response_deserializer=vmmigration.MigratingVm.deserialize,
            )
        return self._stubs["get_migrating_vm"]

    @property
    def update_migrating_vm(
        self,
    ) -> Callable[
        [vmmigration.UpdateMigratingVmRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update migrating vm method over gRPC.

        Updates the parameters of a single MigratingVm.

        Returns:
            Callable[[~.UpdateMigratingVmRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_migrating_vm" not in self._stubs:
            self._stubs["update_migrating_vm"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/UpdateMigratingVm",
                request_serializer=vmmigration.UpdateMigratingVmRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_migrating_vm"]

    @property
    def delete_migrating_vm(
        self,
    ) -> Callable[
        [vmmigration.DeleteMigratingVmRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete migrating vm method over gRPC.

        Deletes a single MigratingVm.

        Returns:
            Callable[[~.DeleteMigratingVmRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_migrating_vm" not in self._stubs:
            self._stubs["delete_migrating_vm"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/DeleteMigratingVm",
                request_serializer=vmmigration.DeleteMigratingVmRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_migrating_vm"]

    @property
    def start_migration(
        self,
    ) -> Callable[
        [vmmigration.StartMigrationRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the start migration method over gRPC.

        Starts migration for a VM. Starts the process of
        uploading data and creating snapshots, in replication
        cycles scheduled by the policy.

        Returns:
            Callable[[~.StartMigrationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_migration" not in self._stubs:
            self._stubs["start_migration"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/StartMigration",
                request_serializer=vmmigration.StartMigrationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["start_migration"]

    @property
    def resume_migration(
        self,
    ) -> Callable[
        [vmmigration.ResumeMigrationRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the resume migration method over gRPC.

        Resumes a migration for a VM. When called on a paused
        migration, will start the process of uploading data and
        creating snapshots; when called on a completed cut-over
        migration, will update the migration to active state and
        start the process of uploading data and creating
        snapshots.

        Returns:
            Callable[[~.ResumeMigrationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "resume_migration" not in self._stubs:
            self._stubs["resume_migration"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/ResumeMigration",
                request_serializer=vmmigration.ResumeMigrationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["resume_migration"]

    @property
    def pause_migration(
        self,
    ) -> Callable[
        [vmmigration.PauseMigrationRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the pause migration method over gRPC.

        Pauses a migration for a VM. If cycle tasks are
        running they will be cancelled, preserving source task
        data. Further replication cycles will not be triggered
        while the VM is paused.

        Returns:
            Callable[[~.PauseMigrationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "pause_migration" not in self._stubs:
            self._stubs["pause_migration"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/PauseMigration",
                request_serializer=vmmigration.PauseMigrationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["pause_migration"]

    @property
    def finalize_migration(
        self,
    ) -> Callable[
        [vmmigration.FinalizeMigrationRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the finalize migration method over gRPC.

        Marks a migration as completed, deleting migration
        resources that are no longer being used. Only applicable
        after cutover is done.

        Returns:
            Callable[[~.FinalizeMigrationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "finalize_migration" not in self._stubs:
            self._stubs["finalize_migration"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/FinalizeMigration",
                request_serializer=vmmigration.FinalizeMigrationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["finalize_migration"]

    @property
    def create_clone_job(
        self,
    ) -> Callable[
        [vmmigration.CreateCloneJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create clone job method over gRPC.

        Initiates a Clone of a specific migrating VM.

        Returns:
            Callable[[~.CreateCloneJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_clone_job" not in self._stubs:
            self._stubs["create_clone_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/CreateCloneJob",
                request_serializer=vmmigration.CreateCloneJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_clone_job"]

    @property
    def cancel_clone_job(
        self,
    ) -> Callable[
        [vmmigration.CancelCloneJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the cancel clone job method over gRPC.

        Initiates the cancellation of a running clone job.

        Returns:
            Callable[[~.CancelCloneJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_clone_job" not in self._stubs:
            self._stubs["cancel_clone_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/CancelCloneJob",
                request_serializer=vmmigration.CancelCloneJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["cancel_clone_job"]

    @property
    def list_clone_jobs(
        self,
    ) -> Callable[
        [vmmigration.ListCloneJobsRequest], Awaitable[vmmigration.ListCloneJobsResponse]
    ]:
        r"""Return a callable for the list clone jobs method over gRPC.

        Lists CloneJobs of a given migrating VM.

        Returns:
            Callable[[~.ListCloneJobsRequest],
                    Awaitable[~.ListCloneJobsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_clone_jobs" not in self._stubs:
            self._stubs["list_clone_jobs"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/ListCloneJobs",
                request_serializer=vmmigration.ListCloneJobsRequest.serialize,
                response_deserializer=vmmigration.ListCloneJobsResponse.deserialize,
            )
        return self._stubs["list_clone_jobs"]

    @property
    def get_clone_job(
        self,
    ) -> Callable[[vmmigration.GetCloneJobRequest], Awaitable[vmmigration.CloneJob]]:
        r"""Return a callable for the get clone job method over gRPC.

        Gets details of a single CloneJob.

        Returns:
            Callable[[~.GetCloneJobRequest],
                    Awaitable[~.CloneJob]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_clone_job" not in self._stubs:
            self._stubs["get_clone_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/GetCloneJob",
                request_serializer=vmmigration.GetCloneJobRequest.serialize,
                response_deserializer=vmmigration.CloneJob.deserialize,
            )
        return self._stubs["get_clone_job"]

    @property
    def create_cutover_job(
        self,
    ) -> Callable[
        [vmmigration.CreateCutoverJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create cutover job method over gRPC.

        Initiates a Cutover of a specific migrating VM.
        The returned LRO is completed when the cutover job
        resource is created and the job is initiated.

        Returns:
            Callable[[~.CreateCutoverJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_cutover_job" not in self._stubs:
            self._stubs["create_cutover_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/CreateCutoverJob",
                request_serializer=vmmigration.CreateCutoverJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_cutover_job"]

    @property
    def cancel_cutover_job(
        self,
    ) -> Callable[
        [vmmigration.CancelCutoverJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the cancel cutover job method over gRPC.

        Initiates the cancellation of a running cutover job.

        Returns:
            Callable[[~.CancelCutoverJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_cutover_job" not in self._stubs:
            self._stubs["cancel_cutover_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/CancelCutoverJob",
                request_serializer=vmmigration.CancelCutoverJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["cancel_cutover_job"]

    @property
    def list_cutover_jobs(
        self,
    ) -> Callable[
        [vmmigration.ListCutoverJobsRequest],
        Awaitable[vmmigration.ListCutoverJobsResponse],
    ]:
        r"""Return a callable for the list cutover jobs method over gRPC.

        Lists CutoverJobs of a given migrating VM.

        Returns:
            Callable[[~.ListCutoverJobsRequest],
                    Awaitable[~.ListCutoverJobsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_cutover_jobs" not in self._stubs:
            self._stubs["list_cutover_jobs"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/ListCutoverJobs",
                request_serializer=vmmigration.ListCutoverJobsRequest.serialize,
                response_deserializer=vmmigration.ListCutoverJobsResponse.deserialize,
            )
        return self._stubs["list_cutover_jobs"]

    @property
    def get_cutover_job(
        self,
    ) -> Callable[
        [vmmigration.GetCutoverJobRequest], Awaitable[vmmigration.CutoverJob]
    ]:
        r"""Return a callable for the get cutover job method over gRPC.

        Gets details of a single CutoverJob.

        Returns:
            Callable[[~.GetCutoverJobRequest],
                    Awaitable[~.CutoverJob]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_cutover_job" not in self._stubs:
            self._stubs["get_cutover_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/GetCutoverJob",
                request_serializer=vmmigration.GetCutoverJobRequest.serialize,
                response_deserializer=vmmigration.CutoverJob.deserialize,
            )
        return self._stubs["get_cutover_job"]

    @property
    def list_groups(
        self,
    ) -> Callable[
        [vmmigration.ListGroupsRequest], Awaitable[vmmigration.ListGroupsResponse]
    ]:
        r"""Return a callable for the list groups method over gRPC.

        Lists Groups in a given project and location.

        Returns:
            Callable[[~.ListGroupsRequest],
                    Awaitable[~.ListGroupsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_groups" not in self._stubs:
            self._stubs["list_groups"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/ListGroups",
                request_serializer=vmmigration.ListGroupsRequest.serialize,
                response_deserializer=vmmigration.ListGroupsResponse.deserialize,
            )
        return self._stubs["list_groups"]

    @property
    def get_group(
        self,
    ) -> Callable[[vmmigration.GetGroupRequest], Awaitable[vmmigration.Group]]:
        r"""Return a callable for the get group method over gRPC.

        Gets details of a single Group.

        Returns:
            Callable[[~.GetGroupRequest],
                    Awaitable[~.Group]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_group" not in self._stubs:
            self._stubs["get_group"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/GetGroup",
                request_serializer=vmmigration.GetGroupRequest.serialize,
                response_deserializer=vmmigration.Group.deserialize,
            )
        return self._stubs["get_group"]

    @property
    def create_group(
        self,
    ) -> Callable[
        [vmmigration.CreateGroupRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create group method over gRPC.

        Creates a new Group in a given project and location.

        Returns:
            Callable[[~.CreateGroupRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_group" not in self._stubs:
            self._stubs["create_group"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/CreateGroup",
                request_serializer=vmmigration.CreateGroupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_group"]

    @property
    def update_group(
        self,
    ) -> Callable[
        [vmmigration.UpdateGroupRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update group method over gRPC.

        Updates the parameters of a single Group.

        Returns:
            Callable[[~.UpdateGroupRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_group" not in self._stubs:
            self._stubs["update_group"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/UpdateGroup",
                request_serializer=vmmigration.UpdateGroupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_group"]

    @property
    def delete_group(
        self,
    ) -> Callable[
        [vmmigration.DeleteGroupRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete group method over gRPC.

        Deletes a single Group.

        Returns:
            Callable[[~.DeleteGroupRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_group" not in self._stubs:
            self._stubs["delete_group"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/DeleteGroup",
                request_serializer=vmmigration.DeleteGroupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_group"]

    @property
    def add_group_migration(
        self,
    ) -> Callable[
        [vmmigration.AddGroupMigrationRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the add group migration method over gRPC.

        Adds a MigratingVm to a Group.

        Returns:
            Callable[[~.AddGroupMigrationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "add_group_migration" not in self._stubs:
            self._stubs["add_group_migration"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/AddGroupMigration",
                request_serializer=vmmigration.AddGroupMigrationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["add_group_migration"]

    @property
    def remove_group_migration(
        self,
    ) -> Callable[
        [vmmigration.RemoveGroupMigrationRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the remove group migration method over gRPC.

        Removes a MigratingVm from a Group.

        Returns:
            Callable[[~.RemoveGroupMigrationRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "remove_group_migration" not in self._stubs:
            self._stubs["remove_group_migration"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/RemoveGroupMigration",
                request_serializer=vmmigration.RemoveGroupMigrationRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["remove_group_migration"]

    @property
    def list_target_projects(
        self,
    ) -> Callable[
        [vmmigration.ListTargetProjectsRequest],
        Awaitable[vmmigration.ListTargetProjectsResponse],
    ]:
        r"""Return a callable for the list target projects method over gRPC.

        Lists TargetProjects in a given project.

        NOTE: TargetProject is a global resource; hence the only
        supported value for location is ``global``.

        Returns:
            Callable[[~.ListTargetProjectsRequest],
                    Awaitable[~.ListTargetProjectsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_target_projects" not in self._stubs:
            self._stubs["list_target_projects"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/ListTargetProjects",
                request_serializer=vmmigration.ListTargetProjectsRequest.serialize,
                response_deserializer=vmmigration.ListTargetProjectsResponse.deserialize,
            )
        return self._stubs["list_target_projects"]

    @property
    def get_target_project(
        self,
    ) -> Callable[
        [vmmigration.GetTargetProjectRequest], Awaitable[vmmigration.TargetProject]
    ]:
        r"""Return a callable for the get target project method over gRPC.

        Gets details of a single TargetProject.

        NOTE: TargetProject is a global resource; hence the only
        supported value for location is ``global``.

        Returns:
            Callable[[~.GetTargetProjectRequest],
                    Awaitable[~.TargetProject]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_target_project" not in self._stubs:
            self._stubs["get_target_project"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/GetTargetProject",
                request_serializer=vmmigration.GetTargetProjectRequest.serialize,
                response_deserializer=vmmigration.TargetProject.deserialize,
            )
        return self._stubs["get_target_project"]

    @property
    def create_target_project(
        self,
    ) -> Callable[
        [vmmigration.CreateTargetProjectRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create target project method over gRPC.

        Creates a new TargetProject in a given project.

        NOTE: TargetProject is a global resource; hence the only
        supported value for location is ``global``.

        Returns:
            Callable[[~.CreateTargetProjectRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_target_project" not in self._stubs:
            self._stubs["create_target_project"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/CreateTargetProject",
                request_serializer=vmmigration.CreateTargetProjectRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_target_project"]

    @property
    def update_target_project(
        self,
    ) -> Callable[
        [vmmigration.UpdateTargetProjectRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update target project method over gRPC.

        Updates the parameters of a single TargetProject.

        NOTE: TargetProject is a global resource; hence the only
        supported value for location is ``global``.

        Returns:
            Callable[[~.UpdateTargetProjectRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_target_project" not in self._stubs:
            self._stubs["update_target_project"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/UpdateTargetProject",
                request_serializer=vmmigration.UpdateTargetProjectRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_target_project"]

    @property
    def delete_target_project(
        self,
    ) -> Callable[
        [vmmigration.DeleteTargetProjectRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete target project method over gRPC.

        Deletes a single TargetProject.

        NOTE: TargetProject is a global resource; hence the only
        supported value for location is ``global``.

        Returns:
            Callable[[~.DeleteTargetProjectRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_target_project" not in self._stubs:
            self._stubs["delete_target_project"] = self.grpc_channel.unary_unary(
                "/google.cloud.vmmigration.v1.VmMigration/DeleteTargetProject",
                request_serializer=vmmigration.DeleteTargetProjectRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_target_project"]

    def close(self):
        return self.grpc_channel.close()


__all__ = ("VmMigrationGrpcAsyncIOTransport",)
