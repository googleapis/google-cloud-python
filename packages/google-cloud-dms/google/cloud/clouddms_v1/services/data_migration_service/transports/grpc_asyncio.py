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
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1
from google.api_core import grpc_helpers_async
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.clouddms_v1.types import clouddms
from google.cloud.clouddms_v1.types import clouddms_resources
from google.longrunning import operations_pb2  # type: ignore
from .base import DataMigrationServiceTransport, DEFAULT_CLIENT_INFO
from .grpc import DataMigrationServiceGrpcTransport


class DataMigrationServiceGrpcAsyncIOTransport(DataMigrationServiceTransport):
    """gRPC AsyncIO backend transport for DataMigrationService.

    Database Migration service

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
        host: str = "datamigration.googleapis.com",
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
        host: str = "datamigration.googleapis.com",
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
    def list_migration_jobs(
        self,
    ) -> Callable[
        [clouddms.ListMigrationJobsRequest],
        Awaitable[clouddms.ListMigrationJobsResponse],
    ]:
        r"""Return a callable for the list migration jobs method over gRPC.

        Lists migration jobs in a given project and location.

        Returns:
            Callable[[~.ListMigrationJobsRequest],
                    Awaitable[~.ListMigrationJobsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_migration_jobs" not in self._stubs:
            self._stubs["list_migration_jobs"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/ListMigrationJobs",
                request_serializer=clouddms.ListMigrationJobsRequest.serialize,
                response_deserializer=clouddms.ListMigrationJobsResponse.deserialize,
            )
        return self._stubs["list_migration_jobs"]

    @property
    def get_migration_job(
        self,
    ) -> Callable[
        [clouddms.GetMigrationJobRequest], Awaitable[clouddms_resources.MigrationJob]
    ]:
        r"""Return a callable for the get migration job method over gRPC.

        Gets details of a single migration job.

        Returns:
            Callable[[~.GetMigrationJobRequest],
                    Awaitable[~.MigrationJob]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_migration_job" not in self._stubs:
            self._stubs["get_migration_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/GetMigrationJob",
                request_serializer=clouddms.GetMigrationJobRequest.serialize,
                response_deserializer=clouddms_resources.MigrationJob.deserialize,
            )
        return self._stubs["get_migration_job"]

    @property
    def create_migration_job(
        self,
    ) -> Callable[
        [clouddms.CreateMigrationJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create migration job method over gRPC.

        Creates a new migration job in a given project and
        location.

        Returns:
            Callable[[~.CreateMigrationJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_migration_job" not in self._stubs:
            self._stubs["create_migration_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/CreateMigrationJob",
                request_serializer=clouddms.CreateMigrationJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_migration_job"]

    @property
    def update_migration_job(
        self,
    ) -> Callable[
        [clouddms.UpdateMigrationJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update migration job method over gRPC.

        Updates the parameters of a single migration job.

        Returns:
            Callable[[~.UpdateMigrationJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_migration_job" not in self._stubs:
            self._stubs["update_migration_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/UpdateMigrationJob",
                request_serializer=clouddms.UpdateMigrationJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_migration_job"]

    @property
    def delete_migration_job(
        self,
    ) -> Callable[
        [clouddms.DeleteMigrationJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete migration job method over gRPC.

        Deletes a single migration job.

        Returns:
            Callable[[~.DeleteMigrationJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_migration_job" not in self._stubs:
            self._stubs["delete_migration_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/DeleteMigrationJob",
                request_serializer=clouddms.DeleteMigrationJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_migration_job"]

    @property
    def start_migration_job(
        self,
    ) -> Callable[
        [clouddms.StartMigrationJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the start migration job method over gRPC.

        Start an already created migration job.

        Returns:
            Callable[[~.StartMigrationJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_migration_job" not in self._stubs:
            self._stubs["start_migration_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/StartMigrationJob",
                request_serializer=clouddms.StartMigrationJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["start_migration_job"]

    @property
    def stop_migration_job(
        self,
    ) -> Callable[
        [clouddms.StopMigrationJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the stop migration job method over gRPC.

        Stops a running migration job.

        Returns:
            Callable[[~.StopMigrationJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "stop_migration_job" not in self._stubs:
            self._stubs["stop_migration_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/StopMigrationJob",
                request_serializer=clouddms.StopMigrationJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["stop_migration_job"]

    @property
    def resume_migration_job(
        self,
    ) -> Callable[
        [clouddms.ResumeMigrationJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the resume migration job method over gRPC.

        Resume a migration job that is currently stopped and
        is resumable (was stopped during CDC phase).

        Returns:
            Callable[[~.ResumeMigrationJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "resume_migration_job" not in self._stubs:
            self._stubs["resume_migration_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/ResumeMigrationJob",
                request_serializer=clouddms.ResumeMigrationJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["resume_migration_job"]

    @property
    def promote_migration_job(
        self,
    ) -> Callable[
        [clouddms.PromoteMigrationJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the promote migration job method over gRPC.

        Promote a migration job, stopping replication to the
        destination and promoting the destination to be a
        standalone database.

        Returns:
            Callable[[~.PromoteMigrationJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "promote_migration_job" not in self._stubs:
            self._stubs["promote_migration_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/PromoteMigrationJob",
                request_serializer=clouddms.PromoteMigrationJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["promote_migration_job"]

    @property
    def verify_migration_job(
        self,
    ) -> Callable[
        [clouddms.VerifyMigrationJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the verify migration job method over gRPC.

        Verify a migration job, making sure the destination
        can reach the source and that all configuration and
        prerequisites are met.

        Returns:
            Callable[[~.VerifyMigrationJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "verify_migration_job" not in self._stubs:
            self._stubs["verify_migration_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/VerifyMigrationJob",
                request_serializer=clouddms.VerifyMigrationJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["verify_migration_job"]

    @property
    def restart_migration_job(
        self,
    ) -> Callable[
        [clouddms.RestartMigrationJobRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the restart migration job method over gRPC.

        Restart a stopped or failed migration job, resetting
        the destination instance to its original state and
        starting the migration process from scratch.

        Returns:
            Callable[[~.RestartMigrationJobRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restart_migration_job" not in self._stubs:
            self._stubs["restart_migration_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/RestartMigrationJob",
                request_serializer=clouddms.RestartMigrationJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restart_migration_job"]

    @property
    def generate_ssh_script(
        self,
    ) -> Callable[[clouddms.GenerateSshScriptRequest], Awaitable[clouddms.SshScript]]:
        r"""Return a callable for the generate ssh script method over gRPC.

        Generate a SSH configuration script to configure the
        reverse SSH connectivity.

        Returns:
            Callable[[~.GenerateSshScriptRequest],
                    Awaitable[~.SshScript]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_ssh_script" not in self._stubs:
            self._stubs["generate_ssh_script"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/GenerateSshScript",
                request_serializer=clouddms.GenerateSshScriptRequest.serialize,
                response_deserializer=clouddms.SshScript.deserialize,
            )
        return self._stubs["generate_ssh_script"]

    @property
    def list_connection_profiles(
        self,
    ) -> Callable[
        [clouddms.ListConnectionProfilesRequest],
        Awaitable[clouddms.ListConnectionProfilesResponse],
    ]:
        r"""Return a callable for the list connection profiles method over gRPC.

        Retrieve a list of all connection profiles in a given
        project and location.

        Returns:
            Callable[[~.ListConnectionProfilesRequest],
                    Awaitable[~.ListConnectionProfilesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_connection_profiles" not in self._stubs:
            self._stubs["list_connection_profiles"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/ListConnectionProfiles",
                request_serializer=clouddms.ListConnectionProfilesRequest.serialize,
                response_deserializer=clouddms.ListConnectionProfilesResponse.deserialize,
            )
        return self._stubs["list_connection_profiles"]

    @property
    def get_connection_profile(
        self,
    ) -> Callable[
        [clouddms.GetConnectionProfileRequest],
        Awaitable[clouddms_resources.ConnectionProfile],
    ]:
        r"""Return a callable for the get connection profile method over gRPC.

        Gets details of a single connection profile.

        Returns:
            Callable[[~.GetConnectionProfileRequest],
                    Awaitable[~.ConnectionProfile]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_connection_profile" not in self._stubs:
            self._stubs["get_connection_profile"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/GetConnectionProfile",
                request_serializer=clouddms.GetConnectionProfileRequest.serialize,
                response_deserializer=clouddms_resources.ConnectionProfile.deserialize,
            )
        return self._stubs["get_connection_profile"]

    @property
    def create_connection_profile(
        self,
    ) -> Callable[
        [clouddms.CreateConnectionProfileRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create connection profile method over gRPC.

        Creates a new connection profile in a given project
        and location.

        Returns:
            Callable[[~.CreateConnectionProfileRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_connection_profile" not in self._stubs:
            self._stubs["create_connection_profile"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/CreateConnectionProfile",
                request_serializer=clouddms.CreateConnectionProfileRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_connection_profile"]

    @property
    def update_connection_profile(
        self,
    ) -> Callable[
        [clouddms.UpdateConnectionProfileRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update connection profile method over gRPC.

        Update the configuration of a single connection
        profile.

        Returns:
            Callable[[~.UpdateConnectionProfileRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_connection_profile" not in self._stubs:
            self._stubs["update_connection_profile"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/UpdateConnectionProfile",
                request_serializer=clouddms.UpdateConnectionProfileRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_connection_profile"]

    @property
    def delete_connection_profile(
        self,
    ) -> Callable[
        [clouddms.DeleteConnectionProfileRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete connection profile method over gRPC.

        Deletes a single Database Migration Service
        connection profile. A connection profile can only be
        deleted if it is not in use by any active migration
        jobs.

        Returns:
            Callable[[~.DeleteConnectionProfileRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_connection_profile" not in self._stubs:
            self._stubs["delete_connection_profile"] = self.grpc_channel.unary_unary(
                "/google.cloud.clouddms.v1.DataMigrationService/DeleteConnectionProfile",
                request_serializer=clouddms.DeleteConnectionProfileRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_connection_profile"]

    def close(self):
        return self.grpc_channel.close()


__all__ = ("DataMigrationServiceGrpcAsyncIOTransport",)
