# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import google.api_core.grpc_helpers
import google.api_core.operations_v1

from google.cloud.spanner_admin_database_v1.proto import spanner_database_admin_pb2_grpc


class DatabaseAdminGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.spanner.admin.database.v1 DatabaseAdmin API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/spanner.admin",
    )

    def __init__(
        self, channel=None, credentials=None, address="spanner.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "database_admin_stub": spanner_database_admin_pb2_grpc.DatabaseAdminStub(
                channel
            )
        }

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="spanner.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def create_database(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.create_database`.

        Creates a new Cloud Spanner database and starts to prepare it for
        serving. The returned ``long-running operation`` will have a name of the
        format ``<database_name>/operations/<operation_id>`` and can be used to
        track preparation of the database. The ``metadata`` field type is
        ``CreateDatabaseMetadata``. The ``response`` field type is ``Database``,
        if successful.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].CreateDatabase

    @property
    def update_database_ddl(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.update_database_ddl`.

        Updates the schema of a Cloud Spanner database by
        creating/altering/dropping tables, columns, indexes, etc. The returned
        ``long-running operation`` will have a name of the format
        ``<database_name>/operations/<operation_id>`` and can be used to track
        execution of the schema change(s). The ``metadata`` field type is
        ``UpdateDatabaseDdlMetadata``. The operation has no response.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].UpdateDatabaseDdl

    @property
    def create_backup(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.create_backup`.

        Starts creating a new Cloud Spanner Backup. The returned backup
        ``long-running operation`` will have a name of the format
        ``projects/<project>/instances/<instance>/backups/<backup>/operations/<operation_id>``
        and can be used to track creation of the backup. The ``metadata`` field
        type is ``CreateBackupMetadata``. The ``response`` field type is
        ``Backup``, if successful. Cancelling the returned operation will stop
        the creation and delete the backup. There can be only one pending backup
        creation per database. Backup creation of different databases can run
        concurrently.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].CreateBackup

    @property
    def restore_database(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.restore_database`.

        Create a new database by restoring from a completed backup. The new
        database must be in the same project and in an instance with the same
        instance configuration as the instance containing the backup. The
        returned database ``long-running operation`` has a name of the format
        ``projects/<project>/instances/<instance>/databases/<database>/operations/<operation_id>``,
        and can be used to track the progress of the operation, and to cancel
        it. The ``metadata`` field type is ``RestoreDatabaseMetadata``. The
        ``response`` type is ``Database``, if successful. Cancelling the
        returned operation will stop the restore and delete the database. There
        can be only one database being restored into an instance at a time. Once
        the restore operation completes, a new restore operation can be
        initiated, without waiting for the optimize operation associated with
        the first restore to complete.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].RestoreDatabase

    @property
    def list_databases(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.list_databases`.

        Lists Cloud Spanner databases.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].ListDatabases

    @property
    def get_database(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.get_database`.

        Gets the state of a Cloud Spanner database.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].GetDatabase

    @property
    def drop_database(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.drop_database`.

        Drops (aka deletes) a Cloud Spanner database. Completed backups for
        the database will be retained according to their ``expire_time``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].DropDatabase

    @property
    def get_database_ddl(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.get_database_ddl`.

        Returns the schema of a Cloud Spanner database as a list of
        formatted DDL statements. This method does not show pending schema
        updates, those may be queried using the ``Operations`` API.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].GetDatabaseDdl

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.set_iam_policy`.

        Sets the access control policy on a database or backup resource.
        Replaces any existing policy.

        Authorization requires ``spanner.databases.setIamPolicy`` permission on
        ``resource``. For backups, authorization requires
        ``spanner.backups.setIamPolicy`` permission on ``resource``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].SetIamPolicy

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.get_iam_policy`.

        Gets the access control policy for a database or backup resource.
        Returns an empty policy if a database or backup exists but does not have
        a policy set.

        Authorization requires ``spanner.databases.getIamPolicy`` permission on
        ``resource``. For backups, authorization requires
        ``spanner.backups.getIamPolicy`` permission on ``resource``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].GetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.test_iam_permissions`.

        Returns permissions that the caller has on the specified database or
        backup resource.

        Attempting this RPC on a non-existent Cloud Spanner database will result
        in a NOT_FOUND error if the user has ``spanner.databases.list``
        permission on the containing Cloud Spanner instance. Otherwise returns
        an empty set of permissions. Calling this method on a backup that does
        not exist will result in a NOT_FOUND error if the user has
        ``spanner.backups.list`` permission on the containing instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].TestIamPermissions

    @property
    def get_backup(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.get_backup`.

        Gets metadata on a pending or completed ``Backup``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].GetBackup

    @property
    def update_backup(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.update_backup`.

        Updates a pending or completed ``Backup``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].UpdateBackup

    @property
    def delete_backup(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.delete_backup`.

        Deletes a pending or completed ``Backup``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].DeleteBackup

    @property
    def list_backups(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.list_backups`.

        Lists completed and pending backups. Backups returned are ordered by
        ``create_time`` in descending order, starting from the most recent
        ``create_time``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].ListBackups

    @property
    def list_database_operations(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.list_database_operations`.

        Lists database ``longrunning-operations``. A database operation has
        a name of the form
        ``projects/<project>/instances/<instance>/databases/<database>/operations/<operation>``.
        The long-running operation ``metadata`` field type ``metadata.type_url``
        describes the type of the metadata. Operations returned include those
        that have completed/failed/canceled within the last 7 days, and pending
        operations.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].ListDatabaseOperations

    @property
    def list_backup_operations(self):
        """Return the gRPC stub for :meth:`DatabaseAdminClient.list_backup_operations`.

        Lists the backup ``long-running operations`` in the given instance.
        A backup operation has a name of the form
        ``projects/<project>/instances/<instance>/backups/<backup>/operations/<operation>``.
        The long-running operation ``metadata`` field type ``metadata.type_url``
        describes the type of the metadata. Operations returned include those
        that have completed/failed/canceled within the last 7 days, and pending
        operations. Operations returned are ordered by
        ``operation.metadata.value.progress.start_time`` in descending order
        starting from the most recently started operation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["database_admin_stub"].ListBackupOperations
