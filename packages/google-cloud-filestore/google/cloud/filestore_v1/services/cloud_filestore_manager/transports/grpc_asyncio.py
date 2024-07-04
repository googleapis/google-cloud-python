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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.filestore_v1.types import cloud_filestore_service

from .base import DEFAULT_CLIENT_INFO, CloudFilestoreManagerTransport
from .grpc import CloudFilestoreManagerGrpcTransport


class CloudFilestoreManagerGrpcAsyncIOTransport(CloudFilestoreManagerTransport):
    """gRPC AsyncIO backend transport for CloudFilestoreManager.

    Configures and manages Filestore resources.

    Filestore Manager v1.

    The ``file.googleapis.com`` service implements the Filestore API and
    defines the following resource model for managing instances:

    -  The service works with a collection of cloud projects, named:
       ``/projects/*``
    -  Each project has a collection of available locations, named:
       ``/locations/*``
    -  Each location has a collection of instances and backups, named:
       ``/instances/*`` and ``/backups/*`` respectively.
    -  As such, Filestore instances are resources of the form:
       ``/projects/{project_number}/locations/{location_id}/instances/{instance_id}``
       and backups are resources of the form:
       ``/projects/{project_number}/locations/{location_id}/backup/{backup_id}``

    Note that location_id must be a Google Cloud ``zone`` for instances,
    but a Google Cloud ``region`` for backups; for example:

    -  ``projects/12345/locations/us-central1-c/instances/my-filestore``
    -  ``projects/12345/locations/us-central1/backups/my-backup``

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
        host: str = "file.googleapis.com",
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
        host: str = "file.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
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
                 The hostname to connect to (default: 'file.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
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

        if isinstance(channel, aio.Channel):
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
    def list_instances(
        self,
    ) -> Callable[
        [cloud_filestore_service.ListInstancesRequest],
        Awaitable[cloud_filestore_service.ListInstancesResponse],
    ]:
        r"""Return a callable for the list instances method over gRPC.

        Lists all instances in a project for either a
        specified location or for all locations.

        Returns:
            Callable[[~.ListInstancesRequest],
                    Awaitable[~.ListInstancesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_instances" not in self._stubs:
            self._stubs["list_instances"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/ListInstances",
                request_serializer=cloud_filestore_service.ListInstancesRequest.serialize,
                response_deserializer=cloud_filestore_service.ListInstancesResponse.deserialize,
            )
        return self._stubs["list_instances"]

    @property
    def get_instance(
        self,
    ) -> Callable[
        [cloud_filestore_service.GetInstanceRequest],
        Awaitable[cloud_filestore_service.Instance],
    ]:
        r"""Return a callable for the get instance method over gRPC.

        Gets the details of a specific instance.

        Returns:
            Callable[[~.GetInstanceRequest],
                    Awaitable[~.Instance]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_instance" not in self._stubs:
            self._stubs["get_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/GetInstance",
                request_serializer=cloud_filestore_service.GetInstanceRequest.serialize,
                response_deserializer=cloud_filestore_service.Instance.deserialize,
            )
        return self._stubs["get_instance"]

    @property
    def create_instance(
        self,
    ) -> Callable[
        [cloud_filestore_service.CreateInstanceRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create instance method over gRPC.

        Creates an instance.
        When creating from a backup, the capacity of the new
        instance needs to be equal to or larger than the
        capacity of the backup (and also equal to or larger than
        the minimum capacity of the tier).

        Returns:
            Callable[[~.CreateInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_instance" not in self._stubs:
            self._stubs["create_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/CreateInstance",
                request_serializer=cloud_filestore_service.CreateInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_instance"]

    @property
    def update_instance(
        self,
    ) -> Callable[
        [cloud_filestore_service.UpdateInstanceRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update instance method over gRPC.

        Updates the settings of a specific instance.

        Returns:
            Callable[[~.UpdateInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_instance" not in self._stubs:
            self._stubs["update_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/UpdateInstance",
                request_serializer=cloud_filestore_service.UpdateInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_instance"]

    @property
    def restore_instance(
        self,
    ) -> Callable[
        [cloud_filestore_service.RestoreInstanceRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the restore instance method over gRPC.

        Restores an existing instance's file share from a
        backup.
        The capacity of the instance needs to be equal to or
        larger than the capacity of the backup (and also equal
        to or larger than the minimum capacity of the tier).

        Returns:
            Callable[[~.RestoreInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restore_instance" not in self._stubs:
            self._stubs["restore_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/RestoreInstance",
                request_serializer=cloud_filestore_service.RestoreInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restore_instance"]

    @property
    def revert_instance(
        self,
    ) -> Callable[
        [cloud_filestore_service.RevertInstanceRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the revert instance method over gRPC.

        Revert an existing instance's file system to a
        specified snapshot.

        Returns:
            Callable[[~.RevertInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "revert_instance" not in self._stubs:
            self._stubs["revert_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/RevertInstance",
                request_serializer=cloud_filestore_service.RevertInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["revert_instance"]

    @property
    def delete_instance(
        self,
    ) -> Callable[
        [cloud_filestore_service.DeleteInstanceRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete instance method over gRPC.

        Deletes an instance.

        Returns:
            Callable[[~.DeleteInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_instance" not in self._stubs:
            self._stubs["delete_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/DeleteInstance",
                request_serializer=cloud_filestore_service.DeleteInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_instance"]

    @property
    def list_snapshots(
        self,
    ) -> Callable[
        [cloud_filestore_service.ListSnapshotsRequest],
        Awaitable[cloud_filestore_service.ListSnapshotsResponse],
    ]:
        r"""Return a callable for the list snapshots method over gRPC.

        Lists all snapshots in a project for either a
        specified location or for all locations.

        Returns:
            Callable[[~.ListSnapshotsRequest],
                    Awaitable[~.ListSnapshotsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_snapshots" not in self._stubs:
            self._stubs["list_snapshots"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/ListSnapshots",
                request_serializer=cloud_filestore_service.ListSnapshotsRequest.serialize,
                response_deserializer=cloud_filestore_service.ListSnapshotsResponse.deserialize,
            )
        return self._stubs["list_snapshots"]

    @property
    def get_snapshot(
        self,
    ) -> Callable[
        [cloud_filestore_service.GetSnapshotRequest],
        Awaitable[cloud_filestore_service.Snapshot],
    ]:
        r"""Return a callable for the get snapshot method over gRPC.

        Gets the details of a specific snapshot.

        Returns:
            Callable[[~.GetSnapshotRequest],
                    Awaitable[~.Snapshot]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_snapshot" not in self._stubs:
            self._stubs["get_snapshot"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/GetSnapshot",
                request_serializer=cloud_filestore_service.GetSnapshotRequest.serialize,
                response_deserializer=cloud_filestore_service.Snapshot.deserialize,
            )
        return self._stubs["get_snapshot"]

    @property
    def create_snapshot(
        self,
    ) -> Callable[
        [cloud_filestore_service.CreateSnapshotRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create snapshot method over gRPC.

        Creates a snapshot.

        Returns:
            Callable[[~.CreateSnapshotRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_snapshot" not in self._stubs:
            self._stubs["create_snapshot"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/CreateSnapshot",
                request_serializer=cloud_filestore_service.CreateSnapshotRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_snapshot"]

    @property
    def delete_snapshot(
        self,
    ) -> Callable[
        [cloud_filestore_service.DeleteSnapshotRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete snapshot method over gRPC.

        Deletes a snapshot.

        Returns:
            Callable[[~.DeleteSnapshotRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_snapshot" not in self._stubs:
            self._stubs["delete_snapshot"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/DeleteSnapshot",
                request_serializer=cloud_filestore_service.DeleteSnapshotRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_snapshot"]

    @property
    def update_snapshot(
        self,
    ) -> Callable[
        [cloud_filestore_service.UpdateSnapshotRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update snapshot method over gRPC.

        Updates the settings of a specific snapshot.

        Returns:
            Callable[[~.UpdateSnapshotRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_snapshot" not in self._stubs:
            self._stubs["update_snapshot"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/UpdateSnapshot",
                request_serializer=cloud_filestore_service.UpdateSnapshotRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_snapshot"]

    @property
    def list_backups(
        self,
    ) -> Callable[
        [cloud_filestore_service.ListBackupsRequest],
        Awaitable[cloud_filestore_service.ListBackupsResponse],
    ]:
        r"""Return a callable for the list backups method over gRPC.

        Lists all backups in a project for either a specified
        location or for all locations.

        Returns:
            Callable[[~.ListBackupsRequest],
                    Awaitable[~.ListBackupsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backups" not in self._stubs:
            self._stubs["list_backups"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/ListBackups",
                request_serializer=cloud_filestore_service.ListBackupsRequest.serialize,
                response_deserializer=cloud_filestore_service.ListBackupsResponse.deserialize,
            )
        return self._stubs["list_backups"]

    @property
    def get_backup(
        self,
    ) -> Callable[
        [cloud_filestore_service.GetBackupRequest],
        Awaitable[cloud_filestore_service.Backup],
    ]:
        r"""Return a callable for the get backup method over gRPC.

        Gets the details of a specific backup.

        Returns:
            Callable[[~.GetBackupRequest],
                    Awaitable[~.Backup]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup" not in self._stubs:
            self._stubs["get_backup"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/GetBackup",
                request_serializer=cloud_filestore_service.GetBackupRequest.serialize,
                response_deserializer=cloud_filestore_service.Backup.deserialize,
            )
        return self._stubs["get_backup"]

    @property
    def create_backup(
        self,
    ) -> Callable[
        [cloud_filestore_service.CreateBackupRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create backup method over gRPC.

        Creates a backup.

        Returns:
            Callable[[~.CreateBackupRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_backup" not in self._stubs:
            self._stubs["create_backup"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/CreateBackup",
                request_serializer=cloud_filestore_service.CreateBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_backup"]

    @property
    def delete_backup(
        self,
    ) -> Callable[
        [cloud_filestore_service.DeleteBackupRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete backup method over gRPC.

        Deletes a backup.

        Returns:
            Callable[[~.DeleteBackupRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup" not in self._stubs:
            self._stubs["delete_backup"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/DeleteBackup",
                request_serializer=cloud_filestore_service.DeleteBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_backup"]

    @property
    def update_backup(
        self,
    ) -> Callable[
        [cloud_filestore_service.UpdateBackupRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update backup method over gRPC.

        Updates the settings of a specific backup.

        Returns:
            Callable[[~.UpdateBackupRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_backup" not in self._stubs:
            self._stubs["update_backup"] = self.grpc_channel.unary_unary(
                "/google.cloud.filestore.v1.CloudFilestoreManager/UpdateBackup",
                request_serializer=cloud_filestore_service.UpdateBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_backup"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_instances: gapic_v1.method_async.wrap_method(
                self.list_instances,
                default_retry=retries.AsyncRetry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_instance: gapic_v1.method_async.wrap_method(
                self.get_instance,
                default_retry=retries.AsyncRetry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_instance: gapic_v1.method_async.wrap_method(
                self.create_instance,
                default_timeout=60000.0,
                client_info=client_info,
            ),
            self.update_instance: gapic_v1.method_async.wrap_method(
                self.update_instance,
                default_timeout=14400.0,
                client_info=client_info,
            ),
            self.restore_instance: gapic_v1.method_async.wrap_method(
                self.restore_instance,
                default_timeout=60000.0,
                client_info=client_info,
            ),
            self.revert_instance: gapic_v1.method_async.wrap_method(
                self.revert_instance,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_instance: gapic_v1.method_async.wrap_method(
                self.delete_instance,
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.list_snapshots: gapic_v1.method_async.wrap_method(
                self.list_snapshots,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_snapshot: gapic_v1.method_async.wrap_method(
                self.get_snapshot,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_snapshot: gapic_v1.method_async.wrap_method(
                self.create_snapshot,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_snapshot: gapic_v1.method_async.wrap_method(
                self.delete_snapshot,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_snapshot: gapic_v1.method_async.wrap_method(
                self.update_snapshot,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_backups: gapic_v1.method_async.wrap_method(
                self.list_backups,
                default_retry=retries.AsyncRetry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_backup: gapic_v1.method_async.wrap_method(
                self.get_backup,
                default_retry=retries.AsyncRetry(
                    initial=0.25,
                    maximum=32.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_backup: gapic_v1.method_async.wrap_method(
                self.create_backup,
                default_timeout=60000.0,
                client_info=client_info,
            ),
            self.delete_backup: gapic_v1.method_async.wrap_method(
                self.delete_backup,
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.update_backup: gapic_v1.method_async.wrap_method(
                self.update_backup,
                default_timeout=600.0,
                client_info=client_info,
            ),
        }

    def close(self):
        return self.grpc_channel.close()

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
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]


__all__ = ("CloudFilestoreManagerGrpcAsyncIOTransport",)
