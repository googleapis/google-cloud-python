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
import proto  # type: ignore

from google.cloud.bigtable_admin_v2.types import common
from google.cloud.bigtable_admin_v2.types import table as gba_table
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.bigtable.admin.v2",
    manifest={
        "RestoreTableRequest",
        "RestoreTableMetadata",
        "OptimizeRestoredTableMetadata",
        "CreateTableRequest",
        "CreateTableFromSnapshotRequest",
        "DropRowRangeRequest",
        "ListTablesRequest",
        "ListTablesResponse",
        "GetTableRequest",
        "DeleteTableRequest",
        "ModifyColumnFamiliesRequest",
        "GenerateConsistencyTokenRequest",
        "GenerateConsistencyTokenResponse",
        "CheckConsistencyRequest",
        "CheckConsistencyResponse",
        "SnapshotTableRequest",
        "GetSnapshotRequest",
        "ListSnapshotsRequest",
        "ListSnapshotsResponse",
        "DeleteSnapshotRequest",
        "SnapshotTableMetadata",
        "CreateTableFromSnapshotMetadata",
        "CreateBackupRequest",
        "CreateBackupMetadata",
        "UpdateBackupRequest",
        "GetBackupRequest",
        "DeleteBackupRequest",
        "ListBackupsRequest",
        "ListBackupsResponse",
    },
)


class RestoreTableRequest(proto.Message):
    r"""The request for
    [RestoreTable][google.bigtable.admin.v2.BigtableTableAdmin.RestoreTable].


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        parent (str):
            Required. The name of the instance in which to create the
            restored table. This instance must be in the same project as
            the source backup. Values are of the form
            ``projects/<project>/instances/<instance>``.
        table_id (str):
            Required. The id of the table to create and restore to. This
            table must not already exist. The ``table_id`` appended to
            ``parent`` forms the full table name of the form
            ``projects/<project>/instances/<instance>/tables/<table_id>``.
        backup (str):
            Name of the backup from which to restore. Values are of the
            form
            ``projects/<project>/instances/<instance>/clusters/<cluster>/backups/<backup>``.

            This field is a member of `oneof`_ ``source``.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    table_id = proto.Field(
        proto.STRING,
        number=2,
    )
    backup = proto.Field(
        proto.STRING,
        number=3,
        oneof="source",
    )


class RestoreTableMetadata(proto.Message):
    r"""Metadata type for the long-running operation returned by
    [RestoreTable][google.bigtable.admin.v2.BigtableTableAdmin.RestoreTable].


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Name of the table being created and restored
            to.
        source_type (google.cloud.bigtable_admin_v2.types.RestoreSourceType):
            The type of the restore source.
        backup_info (google.cloud.bigtable_admin_v2.types.BackupInfo):

            This field is a member of `oneof`_ ``source_info``.
        optimize_table_operation_name (str):
            If exists, the name of the long-running operation that will
            be used to track the post-restore optimization process to
            optimize the performance of the restored table. The metadata
            type of the long-running operation is
            [OptimizeRestoreTableMetadata][]. The response type is
            [Empty][google.protobuf.Empty]. This long-running operation
            may be automatically created by the system if applicable
            after the RestoreTable long-running operation completes
            successfully. This operation may not be created if the table
            is already optimized or the restore was not successful.
        progress (google.cloud.bigtable_admin_v2.types.OperationProgress):
            The progress of the
            [RestoreTable][google.bigtable.admin.v2.BigtableTableAdmin.RestoreTable]
            operation.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    source_type = proto.Field(
        proto.ENUM,
        number=2,
        enum=gba_table.RestoreSourceType,
    )
    backup_info = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="source_info",
        message=gba_table.BackupInfo,
    )
    optimize_table_operation_name = proto.Field(
        proto.STRING,
        number=4,
    )
    progress = proto.Field(
        proto.MESSAGE,
        number=5,
        message=common.OperationProgress,
    )


class OptimizeRestoredTableMetadata(proto.Message):
    r"""Metadata type for the long-running operation used to track
    the progress of optimizations performed on a newly restored
    table. This long-running operation is automatically created by
    the system after the successful completion of a table restore,
    and cannot be cancelled.

    Attributes:
        name (str):
            Name of the restored table being optimized.
        progress (google.cloud.bigtable_admin_v2.types.OperationProgress):
            The progress of the post-restore
            optimizations.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    progress = proto.Field(
        proto.MESSAGE,
        number=2,
        message=common.OperationProgress,
    )


class CreateTableRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.CreateTable][google.bigtable.admin.v2.BigtableTableAdmin.CreateTable]

    Attributes:
        parent (str):
            Required. The unique name of the instance in which to create
            the table. Values are of the form
            ``projects/{project}/instances/{instance}``.
        table_id (str):
            Required. The name by which the new table should be referred
            to within the parent instance, e.g., ``foobar`` rather than
            ``{parent}/tables/foobar``. Maximum 50 characters.
        table (google.cloud.bigtable_admin_v2.types.Table):
            Required. The Table to create.
        initial_splits (Sequence[google.cloud.bigtable_admin_v2.types.CreateTableRequest.Split]):
            The optional list of row keys that will be used to initially
            split the table into several tablets (tablets are similar to
            HBase regions). Given two split keys, ``s1`` and ``s2``,
            three tablets will be created, spanning the key ranges:
            ``[, s1), [s1, s2), [s2, )``.

            Example:

            -  Row keys :=
               ``["a", "apple", "custom", "customer_1", "customer_2",``
               ``"other", "zz"]``
            -  initial_split_keys :=
               ``["apple", "customer_1", "customer_2", "other"]``
            -  Key assignment:

               -  Tablet 1 ``[, apple) => {"a"}.``
               -  Tablet 2
                  ``[apple, customer_1) => {"apple", "custom"}.``
               -  Tablet 3
                  ``[customer_1, customer_2) => {"customer_1"}.``
               -  Tablet 4 ``[customer_2, other) => {"customer_2"}.``
               -  Tablet 5 ``[other, ) => {"other", "zz"}.``
    """

    class Split(proto.Message):
        r"""An initial split point for a newly created table.

        Attributes:
            key (bytes):
                Row key to use as an initial tablet boundary.
        """

        key = proto.Field(
            proto.BYTES,
            number=1,
        )

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    table_id = proto.Field(
        proto.STRING,
        number=2,
    )
    table = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gba_table.Table,
    )
    initial_splits = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=Split,
    )


class CreateTableFromSnapshotRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.CreateTableFromSnapshot][google.bigtable.admin.v2.BigtableTableAdmin.CreateTableFromSnapshot]

    Note: This is a private alpha release of Cloud Bigtable snapshots.
    This feature is not currently available to most Cloud Bigtable
    customers. This feature might be changed in backward-incompatible
    ways and is not recommended for production use. It is not subject to
    any SLA or deprecation policy.

    Attributes:
        parent (str):
            Required. The unique name of the instance in which to create
            the table. Values are of the form
            ``projects/{project}/instances/{instance}``.
        table_id (str):
            Required. The name by which the new table should be referred
            to within the parent instance, e.g., ``foobar`` rather than
            ``{parent}/tables/foobar``.
        source_snapshot (str):
            Required. The unique name of the snapshot from which to
            restore the table. The snapshot and the table must be in the
            same instance. Values are of the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/{snapshot}``.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    table_id = proto.Field(
        proto.STRING,
        number=2,
    )
    source_snapshot = proto.Field(
        proto.STRING,
        number=3,
    )


class DropRowRangeRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.DropRowRange][google.bigtable.admin.v2.BigtableTableAdmin.DropRowRange]

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. The unique name of the table on which to drop a
            range of rows. Values are of the form
            ``projects/{project}/instances/{instance}/tables/{table}``.
        row_key_prefix (bytes):
            Delete all rows that start with this row key
            prefix. Prefix cannot be zero length.

            This field is a member of `oneof`_ ``target``.
        delete_all_data_from_table (bool):
            Delete all rows in the table. Setting this to
            false is a no-op.

            This field is a member of `oneof`_ ``target``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    row_key_prefix = proto.Field(
        proto.BYTES,
        number=2,
        oneof="target",
    )
    delete_all_data_from_table = proto.Field(
        proto.BOOL,
        number=3,
        oneof="target",
    )


class ListTablesRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.ListTables][google.bigtable.admin.v2.BigtableTableAdmin.ListTables]

    Attributes:
        parent (str):
            Required. The unique name of the instance for which tables
            should be listed. Values are of the form
            ``projects/{project}/instances/{instance}``.
        view (google.cloud.bigtable_admin_v2.types.Table.View):
            The view to be applied to the returned tables' fields. Only
            NAME_ONLY view (default) and REPLICATION_VIEW are supported.
        page_size (int):
            Maximum number of results per page.

            A page_size of zero lets the server choose the number of
            items to return. A page_size which is strictly positive will
            return at most that many items. A negative page_size will
            cause an error.

            Following the first request, subsequent paginated calls are
            not required to pass a page_size. If a page_size is set in
            subsequent calls, it must match the page_size given in the
            first request.
        page_token (str):
            The value of ``next_page_token`` returned by a previous
            call.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    view = proto.Field(
        proto.ENUM,
        number=2,
        enum=gba_table.Table.View,
    )
    page_size = proto.Field(
        proto.INT32,
        number=4,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListTablesResponse(proto.Message):
    r"""Response message for
    [google.bigtable.admin.v2.BigtableTableAdmin.ListTables][google.bigtable.admin.v2.BigtableTableAdmin.ListTables]

    Attributes:
        tables (Sequence[google.cloud.bigtable_admin_v2.types.Table]):
            The tables present in the requested instance.
        next_page_token (str):
            Set if not all tables could be returned in a single
            response. Pass this value to ``page_token`` in another
            request to get the next page of results.
    """

    @property
    def raw_page(self):
        return self

    tables = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gba_table.Table,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetTableRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.GetTable][google.bigtable.admin.v2.BigtableTableAdmin.GetTable]

    Attributes:
        name (str):
            Required. The unique name of the requested table. Values are
            of the form
            ``projects/{project}/instances/{instance}/tables/{table}``.
        view (google.cloud.bigtable_admin_v2.types.Table.View):
            The view to be applied to the returned table's fields.
            Defaults to ``SCHEMA_VIEW`` if unspecified.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    view = proto.Field(
        proto.ENUM,
        number=2,
        enum=gba_table.Table.View,
    )


class DeleteTableRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.DeleteTable][google.bigtable.admin.v2.BigtableTableAdmin.DeleteTable]

    Attributes:
        name (str):
            Required. The unique name of the table to be deleted. Values
            are of the form
            ``projects/{project}/instances/{instance}/tables/{table}``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ModifyColumnFamiliesRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.ModifyColumnFamilies][google.bigtable.admin.v2.BigtableTableAdmin.ModifyColumnFamilies]

    Attributes:
        name (str):
            Required. The unique name of the table whose families should
            be modified. Values are of the form
            ``projects/{project}/instances/{instance}/tables/{table}``.
        modifications (Sequence[google.cloud.bigtable_admin_v2.types.ModifyColumnFamiliesRequest.Modification]):
            Required. Modifications to be atomically
            applied to the specified table's families.
            Entries are applied in order, meaning that
            earlier modifications can be masked by later
            ones (in the case of repeated updates to the
            same family, for example).
    """

    class Modification(proto.Message):
        r"""A create, update, or delete of a particular column family.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            id (str):
                The ID of the column family to be modified.
            create (google.cloud.bigtable_admin_v2.types.ColumnFamily):
                Create a new column family with the specified
                schema, or fail if one already exists with the
                given ID.

                This field is a member of `oneof`_ ``mod``.
            update (google.cloud.bigtable_admin_v2.types.ColumnFamily):
                Update an existing column family to the
                specified schema, or fail if no column family
                exists with the given ID.

                This field is a member of `oneof`_ ``mod``.
            drop (bool):
                Drop (delete) the column family with the
                given ID, or fail if no such family exists.

                This field is a member of `oneof`_ ``mod``.
        """

        id = proto.Field(
            proto.STRING,
            number=1,
        )
        create = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="mod",
            message=gba_table.ColumnFamily,
        )
        update = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="mod",
            message=gba_table.ColumnFamily,
        )
        drop = proto.Field(
            proto.BOOL,
            number=4,
            oneof="mod",
        )

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    modifications = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=Modification,
    )


class GenerateConsistencyTokenRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken][google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken]

    Attributes:
        name (str):
            Required. The unique name of the Table for which to create a
            consistency token. Values are of the form
            ``projects/{project}/instances/{instance}/tables/{table}``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class GenerateConsistencyTokenResponse(proto.Message):
    r"""Response message for
    [google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken][google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken]

    Attributes:
        consistency_token (str):
            The generated consistency token.
    """

    consistency_token = proto.Field(
        proto.STRING,
        number=1,
    )


class CheckConsistencyRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency][google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency]

    Attributes:
        name (str):
            Required. The unique name of the Table for which to check
            replication consistency. Values are of the form
            ``projects/{project}/instances/{instance}/tables/{table}``.
        consistency_token (str):
            Required. The token created using
            GenerateConsistencyToken for the Table.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    consistency_token = proto.Field(
        proto.STRING,
        number=2,
    )


class CheckConsistencyResponse(proto.Message):
    r"""Response message for
    [google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency][google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency]

    Attributes:
        consistent (bool):
            True only if the token is consistent. A token
            is consistent if replication has caught up with
            the restrictions specified in the request.
    """

    consistent = proto.Field(
        proto.BOOL,
        number=1,
    )


class SnapshotTableRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.SnapshotTable][google.bigtable.admin.v2.BigtableTableAdmin.SnapshotTable]

    Note: This is a private alpha release of Cloud Bigtable snapshots.
    This feature is not currently available to most Cloud Bigtable
    customers. This feature might be changed in backward-incompatible
    ways and is not recommended for production use. It is not subject to
    any SLA or deprecation policy.

    Attributes:
        name (str):
            Required. The unique name of the table to have the snapshot
            taken. Values are of the form
            ``projects/{project}/instances/{instance}/tables/{table}``.
        cluster (str):
            Required. The name of the cluster where the snapshot will be
            created in. Values are of the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}``.
        snapshot_id (str):
            Required. The ID by which the new snapshot should be
            referred to within the parent cluster, e.g., ``mysnapshot``
            of the form: ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*`` rather than
            ``projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/mysnapshot``.
        ttl (google.protobuf.duration_pb2.Duration):
            The amount of time that the new snapshot can
            stay active after it is created. Once 'ttl'
            expires, the snapshot will get deleted. The
            maximum amount of time a snapshot can stay
            active is 7 days. If 'ttl' is not specified, the
            default value of 24 hours will be used.
        description (str):
            Description of the snapshot.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    cluster = proto.Field(
        proto.STRING,
        number=2,
    )
    snapshot_id = proto.Field(
        proto.STRING,
        number=3,
    )
    ttl = proto.Field(
        proto.MESSAGE,
        number=4,
        message=duration_pb2.Duration,
    )
    description = proto.Field(
        proto.STRING,
        number=5,
    )


class GetSnapshotRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.GetSnapshot][google.bigtable.admin.v2.BigtableTableAdmin.GetSnapshot]

    Note: This is a private alpha release of Cloud Bigtable snapshots.
    This feature is not currently available to most Cloud Bigtable
    customers. This feature might be changed in backward-incompatible
    ways and is not recommended for production use. It is not subject to
    any SLA or deprecation policy.

    Attributes:
        name (str):
            Required. The unique name of the requested snapshot. Values
            are of the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/{snapshot}``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListSnapshotsRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots][google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots]

    Note: This is a private alpha release of Cloud Bigtable snapshots.
    This feature is not currently available to most Cloud Bigtable
    customers. This feature might be changed in backward-incompatible
    ways and is not recommended for production use. It is not subject to
    any SLA or deprecation policy.

    Attributes:
        parent (str):
            Required. The unique name of the cluster for which snapshots
            should be listed. Values are of the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}``.
            Use ``{cluster} = '-'`` to list snapshots for all clusters
            in an instance, e.g.,
            ``projects/{project}/instances/{instance}/clusters/-``.
        page_size (int):
            The maximum number of snapshots to return per
            page. CURRENTLY UNIMPLEMENTED AND IGNORED.
        page_token (str):
            The value of ``next_page_token`` returned by a previous
            call.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListSnapshotsResponse(proto.Message):
    r"""Response message for
    [google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots][google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots]

    Note: This is a private alpha release of Cloud Bigtable snapshots.
    This feature is not currently available to most Cloud Bigtable
    customers. This feature might be changed in backward-incompatible
    ways and is not recommended for production use. It is not subject to
    any SLA or deprecation policy.

    Attributes:
        snapshots (Sequence[google.cloud.bigtable_admin_v2.types.Snapshot]):
            The snapshots present in the requested
            cluster.
        next_page_token (str):
            Set if not all snapshots could be returned in a single
            response. Pass this value to ``page_token`` in another
            request to get the next page of results.
    """

    @property
    def raw_page(self):
        return self

    snapshots = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gba_table.Snapshot,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteSnapshotRequest(proto.Message):
    r"""Request message for
    [google.bigtable.admin.v2.BigtableTableAdmin.DeleteSnapshot][google.bigtable.admin.v2.BigtableTableAdmin.DeleteSnapshot]

    Note: This is a private alpha release of Cloud Bigtable snapshots.
    This feature is not currently available to most Cloud Bigtable
    customers. This feature might be changed in backward-incompatible
    ways and is not recommended for production use. It is not subject to
    any SLA or deprecation policy.

    Attributes:
        name (str):
            Required. The unique name of the snapshot to be deleted.
            Values are of the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/{snapshot}``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class SnapshotTableMetadata(proto.Message):
    r"""The metadata for the Operation returned by SnapshotTable.
    Note: This is a private alpha release of Cloud Bigtable
    snapshots. This feature is not currently available to most Cloud
    Bigtable customers. This feature might be changed in
    backward-incompatible ways and is not recommended for production
    use. It is not subject to any SLA or deprecation policy.

    Attributes:
        original_request (google.cloud.bigtable_admin_v2.types.SnapshotTableRequest):
            The request that prompted the initiation of
            this SnapshotTable operation.
        request_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the original request was
            received.
        finish_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the operation failed or was
            completed successfully.
    """

    original_request = proto.Field(
        proto.MESSAGE,
        number=1,
        message="SnapshotTableRequest",
    )
    request_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    finish_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


class CreateTableFromSnapshotMetadata(proto.Message):
    r"""The metadata for the Operation returned by
    CreateTableFromSnapshot.
    Note: This is a private alpha release of Cloud Bigtable
    snapshots. This feature is not currently available to most Cloud
    Bigtable customers. This feature might be changed in
    backward-incompatible ways and is not recommended for production
    use. It is not subject to any SLA or deprecation policy.

    Attributes:
        original_request (google.cloud.bigtable_admin_v2.types.CreateTableFromSnapshotRequest):
            The request that prompted the initiation of
            this CreateTableFromSnapshot operation.
        request_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the original request was
            received.
        finish_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the operation failed or was
            completed successfully.
    """

    original_request = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CreateTableFromSnapshotRequest",
    )
    request_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    finish_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


class CreateBackupRequest(proto.Message):
    r"""The request for
    [CreateBackup][google.bigtable.admin.v2.BigtableTableAdmin.CreateBackup].

    Attributes:
        parent (str):
            Required. This must be one of the clusters in the instance
            in which this table is located. The backup will be stored in
            this cluster. Values are of the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}``.
        backup_id (str):
            Required. The id of the backup to be created. The
            ``backup_id`` along with the parent ``parent`` are combined
            as {parent}/backups/{backup_id} to create the full backup
            name, of the form:
            ``projects/{project}/instances/{instance}/clusters/{cluster}/backups/{backup_id}``.
            This string must be between 1 and 50 characters in length
            and match the regex [*a-zA-Z0-9][-*.a-zA-Z0-9]*.
        backup (google.cloud.bigtable_admin_v2.types.Backup):
            Required. The backup to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    backup_id = proto.Field(
        proto.STRING,
        number=2,
    )
    backup = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gba_table.Backup,
    )


class CreateBackupMetadata(proto.Message):
    r"""Metadata type for the operation returned by
    [CreateBackup][google.bigtable.admin.v2.BigtableTableAdmin.CreateBackup].

    Attributes:
        name (str):
            The name of the backup being created.
        source_table (str):
            The name of the table the backup is created
            from.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which this operation started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            If set, the time at which this operation
            finished or was cancelled.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    source_table = proto.Field(
        proto.STRING,
        number=2,
    )
    start_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )


class UpdateBackupRequest(proto.Message):
    r"""The request for
    [UpdateBackup][google.bigtable.admin.v2.BigtableTableAdmin.UpdateBackup].

    Attributes:
        backup (google.cloud.bigtable_admin_v2.types.Backup):
            Required. The backup to update. ``backup.name``, and the
            fields to be updated as specified by ``update_mask`` are
            required. Other fields are ignored. Update is only supported
            for the following fields:

            -  ``backup.expire_time``.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. A mask specifying which fields (e.g.
            ``expire_time``) in the Backup resource should be updated.
            This mask is relative to the Backup resource, not to the
            request message. The field mask must always be specified;
            this prevents any future fields from being erased
            accidentally by clients that do not know about them.
    """

    backup = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gba_table.Backup,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class GetBackupRequest(proto.Message):
    r"""The request for
    [GetBackup][google.bigtable.admin.v2.BigtableTableAdmin.GetBackup].

    Attributes:
        name (str):
            Required. Name of the backup. Values are of the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}/backups/{backup}``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteBackupRequest(proto.Message):
    r"""The request for
    [DeleteBackup][google.bigtable.admin.v2.BigtableTableAdmin.DeleteBackup].

    Attributes:
        name (str):
            Required. Name of the backup to delete. Values are of the
            form
            ``projects/{project}/instances/{instance}/clusters/{cluster}/backups/{backup}``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListBackupsRequest(proto.Message):
    r"""The request for
    [ListBackups][google.bigtable.admin.v2.BigtableTableAdmin.ListBackups].

    Attributes:
        parent (str):
            Required. The cluster to list backups from. Values are of
            the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}``.
            Use ``{cluster} = '-'`` to list backups for all clusters in
            an instance, e.g.,
            ``projects/{project}/instances/{instance}/clusters/-``.
        filter (str):
            A filter expression that filters backups listed in the
            response. The expression must specify the field name, a
            comparison operator, and the value that you want to use for
            filtering. The value must be a string, a number, or a
            boolean. The comparison operator must be <, >, <=, >=, !=,
            =, or :. Colon ':' represents a HAS operator which is
            roughly synonymous with equality. Filter rules are case
            insensitive.

            The fields eligible for filtering are:

            -  ``name``
            -  ``source_table``
            -  ``state``
            -  ``start_time`` (and values are of the format
               YYYY-MM-DDTHH:MM:SSZ)
            -  ``end_time`` (and values are of the format
               YYYY-MM-DDTHH:MM:SSZ)
            -  ``expire_time`` (and values are of the format
               YYYY-MM-DDTHH:MM:SSZ)
            -  ``size_bytes``

            To filter on multiple expressions, provide each separate
            expression within parentheses. By default, each expression
            is an AND expression. However, you can include AND, OR, and
            NOT expressions explicitly.

            Some examples of using filters are:

            -  ``name:"exact"`` --> The backup's name is the string
               "exact".
            -  ``name:howl`` --> The backup's name contains the string
               "howl".
            -  ``source_table:prod`` --> The source_table's name
               contains the string "prod".
            -  ``state:CREATING`` --> The backup is pending creation.
            -  ``state:READY`` --> The backup is fully created and ready
               for use.
            -  ``(name:howl) AND (start_time < \"2018-03-28T14:50:00Z\")``
               --> The backup name contains the string "howl" and
               start_time of the backup is before 2018-03-28T14:50:00Z.
            -  ``size_bytes > 10000000000`` --> The backup's size is
               greater than 10GB
        order_by (str):
            An expression for specifying the sort order of the results
            of the request. The string value should specify one or more
            fields in [Backup][google.bigtable.admin.v2.Backup]. The
            full syntax is described at https://aip.dev/132#ordering.

            Fields supported are: \* name \* source_table \* expire_time
            \* start_time \* end_time \* size_bytes \* state

            For example, "start_time". The default sorting order is
            ascending. To specify descending order for the field, a
            suffix " desc" should be appended to the field name. For
            example, "start_time desc". Redundant space characters in
            the syntax are insigificant.

            If order_by is empty, results will be sorted by
            ``start_time`` in descending order starting from the most
            recently created backup.
        page_size (int):
            Number of backups to be returned in the
            response. If 0 or less, defaults to the server's
            maximum allowed page size.
        page_token (str):
            If non-empty, ``page_token`` should contain a
            [next_page_token][google.bigtable.admin.v2.ListBackupsResponse.next_page_token]
            from a previous
            [ListBackupsResponse][google.bigtable.admin.v2.ListBackupsResponse]
            to the same ``parent`` and with the same ``filter``.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    filter = proto.Field(
        proto.STRING,
        number=2,
    )
    order_by = proto.Field(
        proto.STRING,
        number=3,
    )
    page_size = proto.Field(
        proto.INT32,
        number=4,
    )
    page_token = proto.Field(
        proto.STRING,
        number=5,
    )


class ListBackupsResponse(proto.Message):
    r"""The response for
    [ListBackups][google.bigtable.admin.v2.BigtableTableAdmin.ListBackups].

    Attributes:
        backups (Sequence[google.cloud.bigtable_admin_v2.types.Backup]):
            The list of matching backups.
        next_page_token (str):
            ``next_page_token`` can be sent in a subsequent
            [ListBackups][google.bigtable.admin.v2.BigtableTableAdmin.ListBackups]
            call to fetch more of the matching backups.
    """

    @property
    def raw_page(self):
        return self

    backups = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gba_table.Backup,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
