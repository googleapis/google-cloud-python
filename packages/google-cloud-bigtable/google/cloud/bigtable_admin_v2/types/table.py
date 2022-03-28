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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.bigtable.admin.v2",
    manifest={
        "RestoreSourceType",
        "RestoreInfo",
        "Table",
        "ColumnFamily",
        "GcRule",
        "EncryptionInfo",
        "Snapshot",
        "Backup",
        "BackupInfo",
    },
)


class RestoreSourceType(proto.Enum):
    r"""Indicates the type of the restore source."""
    RESTORE_SOURCE_TYPE_UNSPECIFIED = 0
    BACKUP = 1


class RestoreInfo(proto.Message):
    r"""Information about a table restore.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        source_type (google.cloud.bigtable_admin_v2.types.RestoreSourceType):
            The type of the restore source.
        backup_info (google.cloud.bigtable_admin_v2.types.BackupInfo):
            Information about the backup used to restore
            the table. The backup may no longer exist.

            This field is a member of `oneof`_ ``source_info``.
    """

    source_type = proto.Field(
        proto.ENUM,
        number=1,
        enum="RestoreSourceType",
    )
    backup_info = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="source_info",
        message="BackupInfo",
    )


class Table(proto.Message):
    r"""A collection of user data indexed by row, column, and
    timestamp. Each table is served using the resources of its
    parent cluster.

    Attributes:
        name (str):
            The unique name of the table. Values are of the form
            ``projects/{project}/instances/{instance}/tables/[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.
            Views: ``NAME_ONLY``, ``SCHEMA_VIEW``, ``REPLICATION_VIEW``,
            ``FULL``
        cluster_states (Sequence[google.cloud.bigtable_admin_v2.types.Table.ClusterStatesEntry]):
            Output only. Map from cluster ID to per-cluster table state.
            If it could not be determined whether or not the table has
            data in a particular cluster (for example, if its zone is
            unavailable), then there will be an entry for the cluster
            with UNKNOWN ``replication_status``. Views:
            ``REPLICATION_VIEW``, ``ENCRYPTION_VIEW``, ``FULL``
        column_families (Sequence[google.cloud.bigtable_admin_v2.types.Table.ColumnFamiliesEntry]):
            (``CreationOnly``) The column families configured for this
            table, mapped by column family ID. Views: ``SCHEMA_VIEW``,
            ``FULL``
        granularity (google.cloud.bigtable_admin_v2.types.Table.TimestampGranularity):
            (``CreationOnly``) The granularity (i.e. ``MILLIS``) at
            which timestamps are stored in this table. Timestamps not
            matching the granularity will be rejected. If unspecified at
            creation time, the value will be set to ``MILLIS``. Views:
            ``SCHEMA_VIEW``, ``FULL``.
        restore_info (google.cloud.bigtable_admin_v2.types.RestoreInfo):
            Output only. If this table was restored from
            another data source (e.g. a backup), this field
            will be populated with information about the
            restore.
    """

    class TimestampGranularity(proto.Enum):
        r"""Possible timestamp granularities to use when keeping multiple
        versions of data in a table.
        """
        TIMESTAMP_GRANULARITY_UNSPECIFIED = 0
        MILLIS = 1

    class View(proto.Enum):
        r"""Defines a view over a table's fields."""
        VIEW_UNSPECIFIED = 0
        NAME_ONLY = 1
        SCHEMA_VIEW = 2
        REPLICATION_VIEW = 3
        ENCRYPTION_VIEW = 5
        FULL = 4

    class ClusterState(proto.Message):
        r"""The state of a table's data in a particular cluster.

        Attributes:
            replication_state (google.cloud.bigtable_admin_v2.types.Table.ClusterState.ReplicationState):
                Output only. The state of replication for the
                table in this cluster.
            encryption_info (Sequence[google.cloud.bigtable_admin_v2.types.EncryptionInfo]):
                Output only. The encryption information for
                the table in this cluster. If the encryption key
                protecting this resource is customer managed,
                then its version can be rotated in Cloud Key
                Management Service (Cloud KMS). The primary
                version of the key and its status will be
                reflected here when changes propagate from Cloud
                KMS.
        """

        class ReplicationState(proto.Enum):
            r"""Table replication states."""
            STATE_NOT_KNOWN = 0
            INITIALIZING = 1
            PLANNED_MAINTENANCE = 2
            UNPLANNED_MAINTENANCE = 3
            READY = 4
            READY_OPTIMIZING = 5

        replication_state = proto.Field(
            proto.ENUM,
            number=1,
            enum="Table.ClusterState.ReplicationState",
        )
        encryption_info = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="EncryptionInfo",
        )

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    cluster_states = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=2,
        message=ClusterState,
    )
    column_families = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=3,
        message="ColumnFamily",
    )
    granularity = proto.Field(
        proto.ENUM,
        number=4,
        enum=TimestampGranularity,
    )
    restore_info = proto.Field(
        proto.MESSAGE,
        number=6,
        message="RestoreInfo",
    )


class ColumnFamily(proto.Message):
    r"""A set of columns within a table which share a common
    configuration.

    Attributes:
        gc_rule (google.cloud.bigtable_admin_v2.types.GcRule):
            Garbage collection rule specified as a
            protobuf. Must serialize to at most 500 bytes.
            NOTE: Garbage collection executes
            opportunistically in the background, and so it's
            possible for reads to return a cell even if it
            matches the active GC expression for its family.
    """

    gc_rule = proto.Field(
        proto.MESSAGE,
        number=1,
        message="GcRule",
    )


class GcRule(proto.Message):
    r"""Rule for determining which cells to delete during garbage
    collection.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        max_num_versions (int):
            Delete all cells in a column except the most
            recent N.

            This field is a member of `oneof`_ ``rule``.
        max_age (google.protobuf.duration_pb2.Duration):
            Delete cells in a column older than the given
            age. Values must be at least one millisecond,
            and will be truncated to microsecond
            granularity.

            This field is a member of `oneof`_ ``rule``.
        intersection (google.cloud.bigtable_admin_v2.types.GcRule.Intersection):
            Delete cells that would be deleted by every
            nested rule.

            This field is a member of `oneof`_ ``rule``.
        union (google.cloud.bigtable_admin_v2.types.GcRule.Union):
            Delete cells that would be deleted by any
            nested rule.

            This field is a member of `oneof`_ ``rule``.
    """

    class Intersection(proto.Message):
        r"""A GcRule which deletes cells matching all of the given rules.

        Attributes:
            rules (Sequence[google.cloud.bigtable_admin_v2.types.GcRule]):
                Only delete cells which would be deleted by every element of
                ``rules``.
        """

        rules = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="GcRule",
        )

    class Union(proto.Message):
        r"""A GcRule which deletes cells matching any of the given rules.

        Attributes:
            rules (Sequence[google.cloud.bigtable_admin_v2.types.GcRule]):
                Delete cells which would be deleted by any element of
                ``rules``.
        """

        rules = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="GcRule",
        )

    max_num_versions = proto.Field(
        proto.INT32,
        number=1,
        oneof="rule",
    )
    max_age = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="rule",
        message=duration_pb2.Duration,
    )
    intersection = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="rule",
        message=Intersection,
    )
    union = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="rule",
        message=Union,
    )


class EncryptionInfo(proto.Message):
    r"""Encryption information for a given resource.
    If this resource is protected with customer managed encryption,
    the in-use Cloud Key Management Service (Cloud KMS) key version
    is specified along with its status.

    Attributes:
        encryption_type (google.cloud.bigtable_admin_v2.types.EncryptionInfo.EncryptionType):
            Output only. The type of encryption used to
            protect this resource.
        encryption_status (google.rpc.status_pb2.Status):
            Output only. The status of encrypt/decrypt
            calls on underlying data for this resource.
            Regardless of status, the existing data is
            always encrypted at rest.
        kms_key_version (str):
            Output only. The version of the Cloud KMS key
            specified in the parent cluster that is in use
            for the data underlying this table.
    """

    class EncryptionType(proto.Enum):
        r"""Possible encryption types for a resource."""
        ENCRYPTION_TYPE_UNSPECIFIED = 0
        GOOGLE_DEFAULT_ENCRYPTION = 1
        CUSTOMER_MANAGED_ENCRYPTION = 2

    encryption_type = proto.Field(
        proto.ENUM,
        number=3,
        enum=EncryptionType,
    )
    encryption_status = proto.Field(
        proto.MESSAGE,
        number=4,
        message=status_pb2.Status,
    )
    kms_key_version = proto.Field(
        proto.STRING,
        number=2,
    )


class Snapshot(proto.Message):
    r"""A snapshot of a table at a particular time. A snapshot can be
    used as a checkpoint for data restoration or a data source for a
    new table.
    Note: This is a private alpha release of Cloud Bigtable
    snapshots. This feature is not currently available to most Cloud
    Bigtable customers. This feature might be changed in
    backward-incompatible ways and is not recommended for production
    use. It is not subject to any SLA or deprecation policy.

    Attributes:
        name (str):
            Output only. The unique name of the snapshot. Values are of
            the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/{snapshot}``.
        source_table (google.cloud.bigtable_admin_v2.types.Table):
            Output only. The source table at the time the
            snapshot was taken.
        data_size_bytes (int):
            Output only. The size of the data in the
            source table at the time the snapshot was taken.
            In some cases, this value may be computed
            asynchronously via a background process and a
            placeholder of 0 will be used in the meantime.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the snapshot is
            created.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the snapshot will
            be deleted. The maximum amount of time a
            snapshot can stay active is 365 days. If 'ttl'
            is not specified, the default maximum of 365
            days will be used.
        state (google.cloud.bigtable_admin_v2.types.Snapshot.State):
            Output only. The current state of the
            snapshot.
        description (str):
            Output only. Description of the snapshot.
    """

    class State(proto.Enum):
        r"""Possible states of a snapshot."""
        STATE_NOT_KNOWN = 0
        READY = 1
        CREATING = 2

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    source_table = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Table",
    )
    data_size_bytes = proto.Field(
        proto.INT64,
        number=3,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    delete_time = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    state = proto.Field(
        proto.ENUM,
        number=6,
        enum=State,
    )
    description = proto.Field(
        proto.STRING,
        number=7,
    )


class Backup(proto.Message):
    r"""A backup of a Cloud Bigtable table.

    Attributes:
        name (str):
            Output only. A globally unique identifier for the backup
            which cannot be changed. Values are of the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}/ backups/[_a-zA-Z0-9][-_.a-zA-Z0-9]*``
            The final segment of the name must be between 1 and 50
            characters in length.

            The backup is stored in the cluster identified by the prefix
            of the backup name of the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}``.
        source_table (str):
            Required. Immutable. Name of the table from which this
            backup was created. This needs to be in the same instance as
            the backup. Values are of the form
            ``projects/{project}/instances/{instance}/tables/{source_table}``.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. The expiration time of the backup, with
            microseconds granularity that must be at least 6 hours and
            at most 30 days from the time the request is received. Once
            the ``expire_time`` has passed, Cloud Bigtable will delete
            the backup and free the resources used by the backup.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. ``start_time`` is the time that the backup was
            started (i.e. approximately the time the
            [CreateBackup][google.bigtable.admin.v2.BigtableTableAdmin.CreateBackup]
            request is received). The row data in this backup will be no
            older than this timestamp.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. ``end_time`` is the time that the backup was
            finished. The row data in the backup will be no newer than
            this timestamp.
        size_bytes (int):
            Output only. Size of the backup in bytes.
        state (google.cloud.bigtable_admin_v2.types.Backup.State):
            Output only. The current state of the backup.
        encryption_info (google.cloud.bigtable_admin_v2.types.EncryptionInfo):
            Output only. The encryption information for
            the backup.
    """

    class State(proto.Enum):
        r"""Indicates the current state of the backup."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    source_table = proto.Field(
        proto.STRING,
        number=2,
    )
    expire_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    start_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    size_bytes = proto.Field(
        proto.INT64,
        number=6,
    )
    state = proto.Field(
        proto.ENUM,
        number=7,
        enum=State,
    )
    encryption_info = proto.Field(
        proto.MESSAGE,
        number=9,
        message="EncryptionInfo",
    )


class BackupInfo(proto.Message):
    r"""Information about a backup.

    Attributes:
        backup (str):
            Output only. Name of the backup.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time that the backup was
            started. Row data in the backup will be no older
            than this timestamp.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. This time that the backup was
            finished. Row data in the backup will be no
            newer than this timestamp.
        source_table (str):
            Output only. Name of the table the backup was
            created from.
    """

    backup = proto.Field(
        proto.STRING,
        number=1,
    )
    start_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    source_table = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
