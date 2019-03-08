# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

from google.cloud.bigtable_admin_v2.proto import bigtable_table_admin_pb2_grpc


class BigtableTableAdminGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.bigtable.admin.v2 BigtableTableAdmin API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/bigtable.admin",
        "https://www.googleapis.com/auth/bigtable.admin.cluster",
        "https://www.googleapis.com/auth/bigtable.admin.instance",
        "https://www.googleapis.com/auth/bigtable.admin.table",
        "https://www.googleapis.com/auth/cloud-bigtable.admin",
        "https://www.googleapis.com/auth/cloud-bigtable.admin.cluster",
        "https://www.googleapis.com/auth/cloud-bigtable.admin.table",
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
    )

    def __init__(
        self, channel=None, credentials=None, address="bigtableadmin.googleapis.com:443"
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
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "bigtable_table_admin_stub": bigtable_table_admin_pb2_grpc.BigtableTableAdminStub(
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
        cls, address="bigtableadmin.googleapis.com:443", credentials=None
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address,
            credentials=credentials,
            scopes=cls._OAUTH_SCOPES,
            options={
                "grpc.max_send_message_length": -1,
                "grpc.max_receive_message_length": -1,
            }.items(),
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def create_table(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.create_table`.

        Creates a new table in the specified instance.
        The table can be created with a full set of initial column families,
        specified in the request.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].CreateTable

    @property
    def create_table_from_snapshot(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.create_table_from_snapshot`.

        Creates a new table from the specified snapshot. The target table must
        not exist. The snapshot and the table must be in the same instance.

        Note: This is a private alpha release of Cloud Bigtable snapshots. This
        feature is not currently available to most Cloud Bigtable customers. This
        feature might be changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any SLA or deprecation
        policy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].CreateTableFromSnapshot

    @property
    def list_tables(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.list_tables`.

        Lists all tables served from a specified instance.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].ListTables

    @property
    def get_table(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.get_table`.

        Gets metadata information about the specified table.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].GetTable

    @property
    def delete_table(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.delete_table`.

        Permanently deletes a specified table and all of its data.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].DeleteTable

    @property
    def modify_column_families(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.modify_column_families`.

        Performs a series of column family modifications on the specified table.
        Either all or none of the modifications will occur before this method
        returns, but data requests received prior to that point may see a table
        where only some modifications have taken effect.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].ModifyColumnFamilies

    @property
    def drop_row_range(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.drop_row_range`.

        Permanently drop/delete a row range from a specified table. The request can
        specify whether to delete all rows in a table, or only those that match a
        particular prefix.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].DropRowRange

    @property
    def generate_consistency_token(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.generate_consistency_token`.

        Generates a consistency token for a Table, which can be used in
        CheckConsistency to check whether mutations to the table that finished
        before this call started have been replicated. The tokens will be available
        for 90 days.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].GenerateConsistencyToken

    @property
    def check_consistency(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.check_consistency`.

        Checks replication consistency based on a consistency token, that is, if
        replication has caught up based on the conditions specified in the token
        and the check request.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].CheckConsistency

    @property
    def snapshot_table(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.snapshot_table`.

        Creates a new snapshot in the specified cluster from the specified
        source table. The cluster and the table must be in the same instance.

        Note: This is a private alpha release of Cloud Bigtable snapshots. This
        feature is not currently available to most Cloud Bigtable customers. This
        feature might be changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any SLA or deprecation
        policy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].SnapshotTable

    @property
    def get_snapshot(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.get_snapshot`.

        Gets metadata information about the specified snapshot.

        Note: This is a private alpha release of Cloud Bigtable snapshots. This
        feature is not currently available to most Cloud Bigtable customers. This
        feature might be changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any SLA or deprecation
        policy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].GetSnapshot

    @property
    def list_snapshots(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.list_snapshots`.

        Lists all snapshots associated with the specified cluster.

        Note: This is a private alpha release of Cloud Bigtable snapshots. This
        feature is not currently available to most Cloud Bigtable customers. This
        feature might be changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any SLA or deprecation
        policy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].ListSnapshots

    @property
    def delete_snapshot(self):
        """Return the gRPC stub for :meth:`BigtableTableAdminClient.delete_snapshot`.

        Permanently deletes the specified snapshot.

        Note: This is a private alpha release of Cloud Bigtable snapshots. This
        feature is not currently available to most Cloud Bigtable customers. This
        feature might be changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any SLA or deprecation
        policy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_table_admin_stub"].DeleteSnapshot
