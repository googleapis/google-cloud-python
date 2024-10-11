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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import dayofweek_pb2  # type: ignore
from google.type import timeofday_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.alloydb.v1alpha",
    manifest={
        "InstanceView",
        "ClusterView",
        "DatabaseVersion",
        "UserPassword",
        "MigrationSource",
        "EncryptionConfig",
        "EncryptionInfo",
        "SslConfig",
        "AutomatedBackupPolicy",
        "ContinuousBackupConfig",
        "ContinuousBackupInfo",
        "BackupSource",
        "ContinuousBackupSource",
        "Cluster",
        "Instance",
        "ConnectionInfo",
        "Backup",
        "SupportedDatabaseFlag",
        "User",
        "Database",
    },
)


class InstanceView(proto.Enum):
    r"""View on Instance. Pass this enum to rpcs that returns an
    Instance message to control which subsets of fields to get.

    Values:
        INSTANCE_VIEW_UNSPECIFIED (0):
            INSTANCE_VIEW_UNSPECIFIED Not specified, equivalent to
            BASIC.
        INSTANCE_VIEW_BASIC (1):
            BASIC server responses for a primary or read
            instance include all the relevant instance
            details, excluding the details of each node in
            the instance. The default value.
        INSTANCE_VIEW_FULL (2):
            FULL response is equivalent to BASIC for
            primary instance (for now). For read pool
            instance, this includes details of each node in
            the pool.
    """
    INSTANCE_VIEW_UNSPECIFIED = 0
    INSTANCE_VIEW_BASIC = 1
    INSTANCE_VIEW_FULL = 2


class ClusterView(proto.Enum):
    r"""View on Cluster. Pass this enum to rpcs that returns a
    cluster message to control which subsets of fields to get.

    Values:
        CLUSTER_VIEW_UNSPECIFIED (0):
            CLUSTER_VIEW_UNSPECIFIED Not specified, equivalent to BASIC.
        CLUSTER_VIEW_BASIC (1):
            BASIC server responses include all the
            relevant cluster details, excluding
            Cluster.ContinuousBackupInfo.EarliestRestorableTime
            and other view-specific fields. The default
            value.
        CLUSTER_VIEW_CONTINUOUS_BACKUP (2):
            CONTINUOUS_BACKUP response returns all the fields from BASIC
            plus the earliest restorable time if continuous backups are
            enabled. May increase latency.
    """
    CLUSTER_VIEW_UNSPECIFIED = 0
    CLUSTER_VIEW_BASIC = 1
    CLUSTER_VIEW_CONTINUOUS_BACKUP = 2


class DatabaseVersion(proto.Enum):
    r"""The supported database engine versions.

    Values:
        DATABASE_VERSION_UNSPECIFIED (0):
            This is an unknown database version.
        POSTGRES_13 (1):
            DEPRECATED - The database version is Postgres
            13.
        POSTGRES_14 (2):
            The database version is Postgres 14.
        POSTGRES_15 (3):
            The database version is Postgres 15.
    """
    DATABASE_VERSION_UNSPECIFIED = 0
    POSTGRES_13 = 1
    POSTGRES_14 = 2
    POSTGRES_15 = 3


class UserPassword(proto.Message):
    r"""The username/password for a database user. Used for
    specifying initial users at cluster creation time.

    Attributes:
        user (str):
            The database username.
        password (str):
            The initial password for the user.
    """

    user: str = proto.Field(
        proto.STRING,
        number=1,
    )
    password: str = proto.Field(
        proto.STRING,
        number=2,
    )


class MigrationSource(proto.Message):
    r"""Subset of the source instance configuration that is available
    when reading the cluster resource.

    Attributes:
        host_port (str):
            Output only. The host and port of the
            on-premises instance in host:port format
        reference_id (str):
            Output only. Place holder for the external
            source identifier(e.g DMS job name) that created
            the cluster.
        source_type (google.cloud.alloydb_v1alpha.types.MigrationSource.MigrationSourceType):
            Output only. Type of migration source.
    """

    class MigrationSourceType(proto.Enum):
        r"""Denote the type of migration source that created this
        cluster.

        Values:
            MIGRATION_SOURCE_TYPE_UNSPECIFIED (0):
                Migration source is unknown.
            DMS (1):
                DMS source means the cluster was created via
                DMS migration job.
        """
        MIGRATION_SOURCE_TYPE_UNSPECIFIED = 0
        DMS = 1

    host_port: str = proto.Field(
        proto.STRING,
        number=1,
    )
    reference_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    source_type: MigrationSourceType = proto.Field(
        proto.ENUM,
        number=3,
        enum=MigrationSourceType,
    )


class EncryptionConfig(proto.Message):
    r"""EncryptionConfig describes the encryption config of a cluster
    or a backup that is encrypted with a CMEK (customer-managed
    encryption key).

    Attributes:
        kms_key_name (str):
            The fully-qualified resource name of the KMS key. Each Cloud
            KMS key is regionalized and has the following format:
            projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]
    """

    kms_key_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class EncryptionInfo(proto.Message):
    r"""EncryptionInfo describes the encryption information of a
    cluster or a backup.

    Attributes:
        encryption_type (google.cloud.alloydb_v1alpha.types.EncryptionInfo.Type):
            Output only. Type of encryption.
        kms_key_versions (MutableSequence[str]):
            Output only. Cloud KMS key versions that are
            being used to protect the database or the
            backup.
    """

    class Type(proto.Enum):
        r"""Possible encryption types.

        Values:
            TYPE_UNSPECIFIED (0):
                Encryption type not specified. Defaults to
                GOOGLE_DEFAULT_ENCRYPTION.
            GOOGLE_DEFAULT_ENCRYPTION (1):
                The data is encrypted at rest with a key that
                is fully managed by Google. No key version will
                be populated. This is the default state.
            CUSTOMER_MANAGED_ENCRYPTION (2):
                The data is encrypted at rest with a key that
                is managed by the customer. KMS key versions
                will be populated.
        """
        TYPE_UNSPECIFIED = 0
        GOOGLE_DEFAULT_ENCRYPTION = 1
        CUSTOMER_MANAGED_ENCRYPTION = 2

    encryption_type: Type = proto.Field(
        proto.ENUM,
        number=1,
        enum=Type,
    )
    kms_key_versions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class SslConfig(proto.Message):
    r"""SSL configuration.

    Attributes:
        ssl_mode (google.cloud.alloydb_v1alpha.types.SslConfig.SslMode):
            Optional. SSL mode. Specifies client-server
            SSL/TLS connection behavior.
        ca_source (google.cloud.alloydb_v1alpha.types.SslConfig.CaSource):
            Optional. Certificate Authority (CA) source. Only
            CA_SOURCE_MANAGED is supported currently, and is the default
            value.
    """

    class SslMode(proto.Enum):
        r"""SSL mode options.

        Values:
            SSL_MODE_UNSPECIFIED (0):
                SSL mode not specified. Defaults to ENCRYPTED_ONLY.
            SSL_MODE_ALLOW (1):
                SSL connections are optional. CA verification
                not enforced.
            SSL_MODE_REQUIRE (2):
                SSL connections are required. CA verification
                not enforced. Clients may use locally
                self-signed certificates (default psql client
                behavior).
            SSL_MODE_VERIFY_CA (3):
                SSL connections are required. CA verification
                enforced. Clients must have certificates signed
                by a Cluster CA, e.g. via
                GenerateClientCertificate.
            ALLOW_UNENCRYPTED_AND_ENCRYPTED (4):
                SSL connections are optional. CA verification
                not enforced.
            ENCRYPTED_ONLY (5):
                SSL connections are required. CA verification
                not enforced.
        """
        SSL_MODE_UNSPECIFIED = 0
        SSL_MODE_ALLOW = 1
        SSL_MODE_REQUIRE = 2
        SSL_MODE_VERIFY_CA = 3
        ALLOW_UNENCRYPTED_AND_ENCRYPTED = 4
        ENCRYPTED_ONLY = 5

    class CaSource(proto.Enum):
        r"""Certificate Authority (CA) source for SSL/TLS certificates.

        Values:
            CA_SOURCE_UNSPECIFIED (0):
                Certificate Authority (CA) source not specified. Defaults to
                CA_SOURCE_MANAGED.
            CA_SOURCE_MANAGED (1):
                Certificate Authority (CA) managed by the
                AlloyDB Cluster.
        """
        CA_SOURCE_UNSPECIFIED = 0
        CA_SOURCE_MANAGED = 1

    ssl_mode: SslMode = proto.Field(
        proto.ENUM,
        number=1,
        enum=SslMode,
    )
    ca_source: CaSource = proto.Field(
        proto.ENUM,
        number=2,
        enum=CaSource,
    )


class AutomatedBackupPolicy(proto.Message):
    r"""Message describing the user-specified automated backup
    policy.
    All fields in the automated backup policy are optional. Defaults
    for each field are provided if they are not set.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        weekly_schedule (google.cloud.alloydb_v1alpha.types.AutomatedBackupPolicy.WeeklySchedule):
            Weekly schedule for the Backup.

            This field is a member of `oneof`_ ``schedule``.
        time_based_retention (google.cloud.alloydb_v1alpha.types.AutomatedBackupPolicy.TimeBasedRetention):
            Time-based Backup retention policy.

            This field is a member of `oneof`_ ``retention``.
        quantity_based_retention (google.cloud.alloydb_v1alpha.types.AutomatedBackupPolicy.QuantityBasedRetention):
            Quantity-based Backup retention policy to
            retain recent backups.

            This field is a member of `oneof`_ ``retention``.
        enabled (bool):
            Whether automated automated backups are
            enabled. If not set, defaults to true.

            This field is a member of `oneof`_ ``_enabled``.
        backup_window (google.protobuf.duration_pb2.Duration):
            The length of the time window during which a
            backup can be taken. If a backup does not
            succeed within this time window, it will be
            canceled and considered failed.

            The backup window must be at least 5 minutes
            long. There is no upper bound on the window. If
            not set, it defaults to 1 hour.
        encryption_config (google.cloud.alloydb_v1alpha.types.EncryptionConfig):
            Optional. The encryption config can be
            specified to encrypt the backups with a
            customer-managed encryption key (CMEK). When
            this field is not specified, the backup will
            then use default encryption scheme to protect
            the user data.
        location (str):
            The location where the backup will be stored.
            Currently, the only supported option is to store
            the backup in the same region as the cluster.

            If empty, defaults to the region of the cluster.
        labels (MutableMapping[str, str]):
            Labels to apply to backups created using this
            configuration.
    """

    class WeeklySchedule(proto.Message):
        r"""A weekly schedule starts a backup at prescribed start times within a
        day, for the specified days of the week.

        The weekly schedule message is flexible and can be used to create
        many types of schedules. For example, to have a daily backup that
        starts at 22:00, configure the ``start_times`` field to have one
        element "22:00" and the ``days_of_week`` field to have all seven
        days of the week.

        Attributes:
            start_times (MutableSequence[google.type.timeofday_pb2.TimeOfDay]):
                The times during the day to start a backup.
                The start times are assumed to be in UTC and to
                be an exact hour (e.g., 04:00:00).

                If no start times are provided, a single fixed
                start time is chosen arbitrarily.
            days_of_week (MutableSequence[google.type.dayofweek_pb2.DayOfWeek]):
                The days of the week to perform a backup.

                If this field is left empty, the default of
                every day of the week is used.
        """

        start_times: MutableSequence[timeofday_pb2.TimeOfDay] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=timeofday_pb2.TimeOfDay,
        )
        days_of_week: MutableSequence[dayofweek_pb2.DayOfWeek] = proto.RepeatedField(
            proto.ENUM,
            number=2,
            enum=dayofweek_pb2.DayOfWeek,
        )

    class TimeBasedRetention(proto.Message):
        r"""A time based retention policy specifies that all backups
        within a certain time period should be retained.

        Attributes:
            retention_period (google.protobuf.duration_pb2.Duration):
                The retention period.
        """

        retention_period: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=1,
            message=duration_pb2.Duration,
        )

    class QuantityBasedRetention(proto.Message):
        r"""A quantity based policy specifies that a certain number of
        the most recent successful backups should be retained.

        Attributes:
            count (int):
                The number of backups to retain.
        """

        count: int = proto.Field(
            proto.INT32,
            number=1,
        )

    weekly_schedule: WeeklySchedule = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="schedule",
        message=WeeklySchedule,
    )
    time_based_retention: TimeBasedRetention = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="retention",
        message=TimeBasedRetention,
    )
    quantity_based_retention: QuantityBasedRetention = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="retention",
        message=QuantityBasedRetention,
    )
    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )
    backup_window: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=3,
        message=duration_pb2.Duration,
    )
    encryption_config: "EncryptionConfig" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="EncryptionConfig",
    )
    location: str = proto.Field(
        proto.STRING,
        number=6,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )


class ContinuousBackupConfig(proto.Message):
    r"""ContinuousBackupConfig describes the continuous backups
    recovery configurations of a cluster.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        enabled (bool):
            Whether ContinuousBackup is enabled.

            This field is a member of `oneof`_ ``_enabled``.
        recovery_window_days (int):
            The number of days that are eligible to
            restore from using PITR. To support the entire
            recovery window, backups and logs are retained
            for one day more than the recovery window. If
            not set, defaults to 14 days.
        encryption_config (google.cloud.alloydb_v1alpha.types.EncryptionConfig):
            The encryption config can be specified to
            encrypt the backups with a customer-managed
            encryption key (CMEK). When this field is not
            specified, the backup will then use default
            encryption scheme to protect the user data.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )
    recovery_window_days: int = proto.Field(
        proto.INT32,
        number=4,
    )
    encryption_config: "EncryptionConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="EncryptionConfig",
    )


class ContinuousBackupInfo(proto.Message):
    r"""ContinuousBackupInfo describes the continuous backup
    properties of a cluster.

    Attributes:
        encryption_info (google.cloud.alloydb_v1alpha.types.EncryptionInfo):
            Output only. The encryption information for
            the WALs and backups required for
            ContinuousBackup.
        enabled_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. When ContinuousBackup was most
            recently enabled. Set to null if
            ContinuousBackup is not enabled.
        schedule (MutableSequence[google.type.dayofweek_pb2.DayOfWeek]):
            Output only. Days of the week on which a
            continuous backup is taken. Output only field.
            Ignored if passed into the request.
        earliest_restorable_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The earliest restorable time
            that can be restored to. Output only field.
    """

    encryption_info: "EncryptionInfo" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="EncryptionInfo",
    )
    enabled_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    schedule: MutableSequence[dayofweek_pb2.DayOfWeek] = proto.RepeatedField(
        proto.ENUM,
        number=3,
        enum=dayofweek_pb2.DayOfWeek,
    )
    earliest_restorable_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )


class BackupSource(proto.Message):
    r"""Message describing a BackupSource.

    Attributes:
        backup_uid (str):
            Output only. The system-generated UID of the
            backup which was used to create this resource.
            The UID is generated when the backup is created,
            and it is retained until the backup is deleted.
        backup_name (str):
            Required. The name of the backup resource with the format:

            -  projects/{project}/locations/{region}/backups/{backup_id}
    """

    backup_uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    backup_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ContinuousBackupSource(proto.Message):
    r"""Message describing a ContinuousBackupSource.

    Attributes:
        cluster (str):
            Required. The source cluster from which to
            restore. This cluster must have continuous
            backup enabled for this operation to succeed.
            For the required format, see the comment on the
            Cluster.name field.
        point_in_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. The point in time to restore to.
    """

    cluster: str = proto.Field(
        proto.STRING,
        number=1,
    )
    point_in_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class Cluster(proto.Message):
    r"""A cluster is a collection of regional AlloyDB resources. It
    can include a primary instance and one or more read pool
    instances. All cluster resources share a storage layer, which
    scales as needed.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        backup_source (google.cloud.alloydb_v1alpha.types.BackupSource):
            Output only. Cluster created from backup.

            This field is a member of `oneof`_ ``source``.
        migration_source (google.cloud.alloydb_v1alpha.types.MigrationSource):
            Output only. Cluster created via DMS
            migration.

            This field is a member of `oneof`_ ``source``.
        name (str):
            Output only. The name of the cluster resource with the
            format:

            -  projects/{project}/locations/{region}/clusters/{cluster_id}
               where the cluster ID segment should satisfy the regex
               expression ``[a-z0-9-]+``. For more details see
               https://google.aip.dev/122. The prefix of the cluster
               resource name is the name of the parent resource:
            -  projects/{project}/locations/{region}
        display_name (str):
            User-settable and human-readable display name
            for the Cluster.
        uid (str):
            Output only. The system-generated UID of the
            resource. The UID is assigned when the resource
            is created, and it is retained until it is
            deleted.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Create time stamp
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Update time stamp
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Delete time stamp
        labels (MutableMapping[str, str]):
            Labels as key value pairs
        state (google.cloud.alloydb_v1alpha.types.Cluster.State):
            Output only. The current serving state of the
            cluster.
        cluster_type (google.cloud.alloydb_v1alpha.types.Cluster.ClusterType):
            Output only. The type of the cluster. This is an output-only
            field and it's populated at the Cluster creation time or the
            Cluster promotion time. The cluster type is determined by
            which RPC was used to create the cluster (i.e.
            ``CreateCluster`` vs. ``CreateSecondaryCluster``
        database_version (google.cloud.alloydb_v1alpha.types.DatabaseVersion):
            Optional. The database engine major version.
            This is an optional field and it is populated at
            the Cluster creation time. If a database version
            is not supplied at cluster creation time, then a
            default database version will be used.
        network_config (google.cloud.alloydb_v1alpha.types.Cluster.NetworkConfig):

        network (str):
            Required. The resource link for the VPC network in which
            cluster resources are created and from which they are
            accessible via Private IP. The network must belong to the
            same project as the cluster. It is specified in the form:
            "projects/{project}/global/networks/{network_id}". This is
            required to create a cluster. Deprecated, use
            network_config.network instead.
        etag (str):
            For Resource freshness validation
            (https://google.aip.dev/154)
        annotations (MutableMapping[str, str]):
            Annotations to allow client tools to store
            small amount of arbitrary data. This is distinct
            from labels. https://google.aip.dev/128
        reconciling (bool):
            Output only. Reconciling
            (https://google.aip.dev/128#reconciliation). Set
            to true if the current state of Cluster does not
            match the user's intended state, and the service
            is actively updating the resource to reconcile
            them. This can happen due to user-triggered
            updates or system actions like failover or
            maintenance.
        initial_user (google.cloud.alloydb_v1alpha.types.UserPassword):
            Input only. Initial user to setup during cluster creation.
            Required. If used in ``RestoreCluster`` this is ignored.
        automated_backup_policy (google.cloud.alloydb_v1alpha.types.AutomatedBackupPolicy):
            The automated backup policy for this cluster.

            If no policy is provided then the default policy
            will be used. If backups are supported for the
            cluster, the default policy takes one backup a
            day, has a backup window of 1 hour, and retains
            backups for 14 days. For more information on the
            defaults, consult the documentation for the
            message type.
        ssl_config (google.cloud.alloydb_v1alpha.types.SslConfig):
            SSL configuration for this AlloyDB cluster.
        encryption_config (google.cloud.alloydb_v1alpha.types.EncryptionConfig):
            Optional. The encryption config can be
            specified to encrypt the data disks and other
            persistent data resources of a cluster with a
            customer-managed encryption key (CMEK). When
            this field is not specified, the cluster will
            then use default encryption scheme to protect
            the user data.
        encryption_info (google.cloud.alloydb_v1alpha.types.EncryptionInfo):
            Output only. The encryption information for
            the cluster.
        continuous_backup_config (google.cloud.alloydb_v1alpha.types.ContinuousBackupConfig):
            Optional. Continuous backup configuration for
            this cluster.
        continuous_backup_info (google.cloud.alloydb_v1alpha.types.ContinuousBackupInfo):
            Output only. Continuous backup properties for
            this cluster.
        secondary_config (google.cloud.alloydb_v1alpha.types.Cluster.SecondaryConfig):
            Cross Region replication config specific to
            SECONDARY cluster.
        primary_config (google.cloud.alloydb_v1alpha.types.Cluster.PrimaryConfig):
            Output only. Cross Region replication config
            specific to PRIMARY cluster.
        satisfies_pzi (bool):
            Output only. Reserved for future use.
        satisfies_pzs (bool):
            Output only. Reserved for future use.
        psc_config (google.cloud.alloydb_v1alpha.types.Cluster.PscConfig):
            Optional. The configuration for Private
            Service Connect (PSC) for the cluster.
    """

    class State(proto.Enum):
        r"""Cluster State

        Values:
            STATE_UNSPECIFIED (0):
                The state of the cluster is unknown.
            READY (1):
                The cluster is active and running.
            STOPPED (2):
                The cluster is stopped. All instances in the
                cluster are stopped. Customers can start a
                stopped cluster at any point and all their
                instances will come back to life with same names
                and IP resources. In this state, customer pays
                for storage.
                Associated backups could also be present in a
                stopped cluster.
            EMPTY (3):
                The cluster is empty and has no associated
                resources. All instances, associated storage and
                backups have been deleted.
            CREATING (4):
                The cluster is being created.
            DELETING (5):
                The cluster is being deleted.
            FAILED (6):
                The creation of the cluster failed.
            BOOTSTRAPPING (7):
                The cluster is bootstrapping with data from
                some other source. Direct mutations to the
                cluster (e.g. adding read pool) are not allowed.
            MAINTENANCE (8):
                The cluster is under maintenance. AlloyDB
                regularly performs maintenance and upgrades on
                customer clusters. Updates on the cluster are
                not allowed while the cluster is in this state.
            PROMOTING (9):
                The cluster is being promoted.
        """
        STATE_UNSPECIFIED = 0
        READY = 1
        STOPPED = 2
        EMPTY = 3
        CREATING = 4
        DELETING = 5
        FAILED = 6
        BOOTSTRAPPING = 7
        MAINTENANCE = 8
        PROMOTING = 9

    class ClusterType(proto.Enum):
        r"""Type of Cluster

        Values:
            CLUSTER_TYPE_UNSPECIFIED (0):
                The type of the cluster is unknown.
            PRIMARY (1):
                Primary cluster that support read and write
                operations.
            SECONDARY (2):
                Secondary cluster that is replicating from
                another region. This only supports read.
        """
        CLUSTER_TYPE_UNSPECIFIED = 0
        PRIMARY = 1
        SECONDARY = 2

    class NetworkConfig(proto.Message):
        r"""Metadata related to network configuration.

        Attributes:
            network (str):
                Optional. The resource link for the VPC network in which
                cluster resources are created and from which they are
                accessible via Private IP. The network must belong to the
                same project as the cluster. It is specified in the form:
                "projects/{project_number}/global/networks/{network_id}".
                This is required to create a cluster.
            allocated_ip_range (str):
                Optional. Name of the allocated IP range for the private IP
                AlloyDB cluster, for example:
                "google-managed-services-default". If set, the instance IPs
                for this cluster will be created in the allocated range. The
                range name must comply with RFC 1035. Specifically, the name
                must be 1-63 characters long and match the regular
                expression ``[a-z]([-a-z0-9]*[a-z0-9])?``. Field name is
                intended to be consistent with Cloud SQL.
        """

        network: str = proto.Field(
            proto.STRING,
            number=1,
        )
        allocated_ip_range: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class SecondaryConfig(proto.Message):
        r"""Configuration information for the secondary cluster. This
        should be set if and only if the cluster is of type SECONDARY.

        Attributes:
            primary_cluster_name (str):
                The name of the primary cluster name with the format:

                -  projects/{project}/locations/{region}/clusters/{cluster_id}
        """

        primary_cluster_name: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class PrimaryConfig(proto.Message):
        r"""Configuration for the primary cluster. It has the list of
        clusters that are replicating from this cluster. This should be
        set if and only if the cluster is of type PRIMARY.

        Attributes:
            secondary_cluster_names (MutableSequence[str]):
                Output only. Names of the clusters that are
                replicating from this cluster.
        """

        secondary_cluster_names: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    class PscConfig(proto.Message):
        r"""PscConfig contains PSC related configuration at a cluster
        level.

        Attributes:
            psc_enabled (bool):
                Optional. Create an instance that allows
                connections from Private Service Connect
                endpoints to the instance.
        """

        psc_enabled: bool = proto.Field(
            proto.BOOL,
            number=1,
        )

    backup_source: "BackupSource" = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="source",
        message="BackupSource",
    )
    migration_source: "MigrationSource" = proto.Field(
        proto.MESSAGE,
        number=16,
        oneof="source",
        message="MigrationSource",
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=8,
        enum=State,
    )
    cluster_type: ClusterType = proto.Field(
        proto.ENUM,
        number=24,
        enum=ClusterType,
    )
    database_version: "DatabaseVersion" = proto.Field(
        proto.ENUM,
        number=9,
        enum="DatabaseVersion",
    )
    network_config: NetworkConfig = proto.Field(
        proto.MESSAGE,
        number=29,
        message=NetworkConfig,
    )
    network: str = proto.Field(
        proto.STRING,
        number=10,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=11,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=12,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=13,
    )
    initial_user: "UserPassword" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="UserPassword",
    )
    automated_backup_policy: "AutomatedBackupPolicy" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="AutomatedBackupPolicy",
    )
    ssl_config: "SslConfig" = proto.Field(
        proto.MESSAGE,
        number=18,
        message="SslConfig",
    )
    encryption_config: "EncryptionConfig" = proto.Field(
        proto.MESSAGE,
        number=19,
        message="EncryptionConfig",
    )
    encryption_info: "EncryptionInfo" = proto.Field(
        proto.MESSAGE,
        number=20,
        message="EncryptionInfo",
    )
    continuous_backup_config: "ContinuousBackupConfig" = proto.Field(
        proto.MESSAGE,
        number=27,
        message="ContinuousBackupConfig",
    )
    continuous_backup_info: "ContinuousBackupInfo" = proto.Field(
        proto.MESSAGE,
        number=28,
        message="ContinuousBackupInfo",
    )
    secondary_config: SecondaryConfig = proto.Field(
        proto.MESSAGE,
        number=22,
        message=SecondaryConfig,
    )
    primary_config: PrimaryConfig = proto.Field(
        proto.MESSAGE,
        number=23,
        message=PrimaryConfig,
    )
    satisfies_pzi: bool = proto.Field(
        proto.BOOL,
        number=33,
    )
    satisfies_pzs: bool = proto.Field(
        proto.BOOL,
        number=30,
    )
    psc_config: PscConfig = proto.Field(
        proto.MESSAGE,
        number=31,
        message=PscConfig,
    )


class Instance(proto.Message):
    r"""An Instance is a computing unit that an end customer can
    connect to. It's the main unit of computing resources in
    AlloyDB.

    Attributes:
        name (str):
            Output only. The name of the instance resource with the
            format:

            -  projects/{project}/locations/{region}/clusters/{cluster_id}/instances/{instance_id}
               where the cluster and instance ID segments should satisfy
               the regex expression ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``,
               e.g. 1-63 characters of lowercase letters, numbers, and
               dashes, starting with a letter, and ending with a letter
               or number. For more details see
               https://google.aip.dev/122. The prefix of the instance
               resource name is the name of the parent resource:
            -  projects/{project}/locations/{region}/clusters/{cluster_id}
        display_name (str):
            User-settable and human-readable display name
            for the Instance.
        uid (str):
            Output only. The system-generated UID of the
            resource. The UID is assigned when the resource
            is created, and it is retained until it is
            deleted.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Create time stamp
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Update time stamp
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Delete time stamp
        labels (MutableMapping[str, str]):
            Labels as key value pairs
        state (google.cloud.alloydb_v1alpha.types.Instance.State):
            Output only. The current serving state of the
            instance.
        instance_type (google.cloud.alloydb_v1alpha.types.Instance.InstanceType):
            Required. The type of the instance. Specified
            at creation time.
        machine_config (google.cloud.alloydb_v1alpha.types.Instance.MachineConfig):
            Configurations for the machines that host the
            underlying database engine.
        availability_type (google.cloud.alloydb_v1alpha.types.Instance.AvailabilityType):
            Availability type of an Instance. If empty, defaults to
            REGIONAL for primary instances. For read pools,
            availability_type is always UNSPECIFIED. Instances in the
            read pools are evenly distributed across available zones
            within the region (i.e. read pools with more than one node
            will have a node in at least two zones).
        gce_zone (str):
            The Compute Engine zone that the instance
            should serve from, per
            https://cloud.google.com/compute/docs/regions-zones
            This can ONLY be specified for ZONAL instances.
            If present for a REGIONAL instance, an error
            will be thrown. If this is absent for a ZONAL
            instance, instance is created in a random zone
            with available capacity.
        database_flags (MutableMapping[str, str]):
            Database flags. Set at instance level.

            -  They are copied from primary instance on read instance
               creation.
            -  Read instances can set new or override existing flags
               that are relevant for reads, e.g. for enabling columnar
               cache on a read instance. Flags set on read instance may
               or may not be present on primary.

            This is a list of "key": "value" pairs. "key": The name of
            the flag. These flags are passed at instance setup time, so
            include both server options and system variables for
            Postgres. Flags are specified with underscores, not hyphens.
            "value": The value of the flag. Booleans are set to **on**
            for true and **off** for false. This field must be omitted
            if the flag doesn't take a value.
        writable_node (google.cloud.alloydb_v1alpha.types.Instance.Node):
            Output only. This is set for the read-write
            VM of the PRIMARY instance only.
        nodes (MutableSequence[google.cloud.alloydb_v1alpha.types.Instance.Node]):
            Output only. List of available read-only VMs
            in this instance, including the standby for a
            PRIMARY instance.
        query_insights_config (google.cloud.alloydb_v1alpha.types.Instance.QueryInsightsInstanceConfig):
            Configuration for query insights.
        read_pool_config (google.cloud.alloydb_v1alpha.types.Instance.ReadPoolConfig):
            Read pool instance configuration. This is required if the
            value of instanceType is READ_POOL.
        ip_address (str):
            Output only. The IP address for the Instance.
            This is the connection endpoint for an end-user
            application.
        public_ip_address (str):
            Output only. The public IP addresses for the Instance. This
            is available ONLY when enable_public_ip is set. This is the
            connection endpoint for an end-user application.
        reconciling (bool):
            Output only. Reconciling
            (https://google.aip.dev/128#reconciliation). Set
            to true if the current state of Instance does
            not match the user's intended state, and the
            service is actively updating the resource to
            reconcile them. This can happen due to
            user-triggered updates or system actions like
            failover or maintenance.
        etag (str):
            For Resource freshness validation
            (https://google.aip.dev/154)
        annotations (MutableMapping[str, str]):
            Annotations to allow client tools to store
            small amount of arbitrary data. This is distinct
            from labels. https://google.aip.dev/128
        update_policy (google.cloud.alloydb_v1alpha.types.Instance.UpdatePolicy):
            Update policy that will be applied during
            instance update. This field is not persisted
            when you update the instance. To use a
            non-default update policy, you must
            specify explicitly specify the value in each
            update request.
        client_connection_config (google.cloud.alloydb_v1alpha.types.Instance.ClientConnectionConfig):
            Optional. Client connection specific
            configurations
        satisfies_pzi (bool):
            Output only. Reserved for future use.
        satisfies_pzs (bool):
            Output only. Reserved for future use.
        psc_instance_config (google.cloud.alloydb_v1alpha.types.Instance.PscInstanceConfig):
            Optional. The configuration for Private
            Service Connect (PSC) for the instance.
        network_config (google.cloud.alloydb_v1alpha.types.Instance.InstanceNetworkConfig):
            Optional. Instance level network
            configuration.
    """

    class State(proto.Enum):
        r"""Instance State

        Values:
            STATE_UNSPECIFIED (0):
                The state of the instance is unknown.
            READY (1):
                The instance is active and running.
            STOPPED (2):
                The instance is stopped. Instance name and IP
                resources are preserved.
            CREATING (3):
                The instance is being created.
            DELETING (4):
                The instance is being deleted.
            MAINTENANCE (5):
                The instance is down for maintenance.
            FAILED (6):
                The creation of the instance failed or a
                fatal error occurred during an operation on the
                instance. Note: Instances in this state would
                tried to be auto-repaired. And Customers should
                be able to restart, update or delete these
                instances.
            BOOTSTRAPPING (8):
                Index 7 is used in the producer apis for ROLLED_BACK state.
                Keeping that index unused in case that state also needs to
                exposed via consumer apis in future. The instance has been
                configured to sync data from some other source.
            PROMOTING (9):
                The instance is being promoted.
        """
        STATE_UNSPECIFIED = 0
        READY = 1
        STOPPED = 2
        CREATING = 3
        DELETING = 4
        MAINTENANCE = 5
        FAILED = 6
        BOOTSTRAPPING = 8
        PROMOTING = 9

    class InstanceType(proto.Enum):
        r"""Type of an Instance

        Values:
            INSTANCE_TYPE_UNSPECIFIED (0):
                The type of the instance is unknown.
            PRIMARY (1):
                PRIMARY instances support read and write
                operations.
            READ_POOL (2):
                READ POOL instances support read operations only. Each read
                pool instance consists of one or more homogeneous nodes.

                -  Read pool of size 1 can only have zonal availability.
                -  Read pools with node count of 2 or more can have regional
                   availability (nodes are present in 2 or more zones in a
                   region).
            SECONDARY (3):
                SECONDARY instances support read operations
                only. SECONDARY instance is a cross-region read
                replica
        """
        INSTANCE_TYPE_UNSPECIFIED = 0
        PRIMARY = 1
        READ_POOL = 2
        SECONDARY = 3

    class AvailabilityType(proto.Enum):
        r"""The Availability type of an instance. Potential values:

        - ZONAL: The instance serves data from only one zone. Outages in
          that     zone affect instance availability.
        - REGIONAL: The instance can serve data from more than one zone
          in a     region (it is highly available).

        Values:
            AVAILABILITY_TYPE_UNSPECIFIED (0):
                This is an unknown Availability type.
            ZONAL (1):
                Zonal available instance.
            REGIONAL (2):
                Regional (or Highly) available instance.
        """
        AVAILABILITY_TYPE_UNSPECIFIED = 0
        ZONAL = 1
        REGIONAL = 2

    class MachineConfig(proto.Message):
        r"""MachineConfig describes the configuration of a machine.

        Attributes:
            cpu_count (int):
                The number of CPU's in the VM instance.
        """

        cpu_count: int = proto.Field(
            proto.INT32,
            number=1,
        )

    class Node(proto.Message):
        r"""Details of a single node in the instance.
        Nodes in an AlloyDB instance are ephemereal, they can change
        during update, failover, autohealing and resize operations.

        Attributes:
            zone_id (str):
                The Compute Engine zone of the VM e.g.
                "us-central1-b".
            id (str):
                The identifier of the VM e.g.
                "test-read-0601-407e52be-ms3l".
            ip (str):
                The private IP address of the VM e.g.
                "10.57.0.34".
            state (str):
                Determined by state of the compute VM and
                postgres-service health. Compute VM state can
                have values listed in
                https://cloud.google.com/compute/docs/instances/instance-life-cycle
                and postgres-service health can have values:
                HEALTHY and UNHEALTHY.
        """

        zone_id: str = proto.Field(
            proto.STRING,
            number=1,
        )
        id: str = proto.Field(
            proto.STRING,
            number=2,
        )
        ip: str = proto.Field(
            proto.STRING,
            number=3,
        )
        state: str = proto.Field(
            proto.STRING,
            number=4,
        )

    class QueryInsightsInstanceConfig(proto.Message):
        r"""QueryInsights Instance specific configuration.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            record_application_tags (bool):
                Record application tags for an instance.
                This flag is turned "on" by default.

                This field is a member of `oneof`_ ``_record_application_tags``.
            record_client_address (bool):
                Record client address for an instance. Client
                address is PII information. This flag is turned
                "on" by default.

                This field is a member of `oneof`_ ``_record_client_address``.
            query_string_length (int):
                Query string length. The default value is
                1024. Any integer between 256 and 4500 is
                considered valid.
            query_plans_per_minute (int):
                Number of query execution plans captured by
                Insights per minute for all queries combined.
                The default value is 5. Any integer between 0
                and 20 is considered valid.

                This field is a member of `oneof`_ ``_query_plans_per_minute``.
        """

        record_application_tags: bool = proto.Field(
            proto.BOOL,
            number=2,
            optional=True,
        )
        record_client_address: bool = proto.Field(
            proto.BOOL,
            number=3,
            optional=True,
        )
        query_string_length: int = proto.Field(
            proto.UINT32,
            number=4,
        )
        query_plans_per_minute: int = proto.Field(
            proto.UINT32,
            number=5,
            optional=True,
        )

    class ReadPoolConfig(proto.Message):
        r"""Configuration for a read pool instance.

        Attributes:
            node_count (int):
                Read capacity, i.e. number of nodes in a read
                pool instance.
        """

        node_count: int = proto.Field(
            proto.INT32,
            number=1,
        )

    class UpdatePolicy(proto.Message):
        r"""Policy to be used while updating the instance.

        Attributes:
            mode (google.cloud.alloydb_v1alpha.types.Instance.UpdatePolicy.Mode):
                Mode for updating the instance.
        """

        class Mode(proto.Enum):
            r"""Specifies the available modes of update.

            Values:
                MODE_UNSPECIFIED (0):
                    Mode is unknown.
                DEFAULT (1):
                    Least disruptive way to apply the update.
                FORCE_APPLY (2):
                    Performs a forced update when applicable.
                    This will be fast but may incur a downtime.
            """
            MODE_UNSPECIFIED = 0
            DEFAULT = 1
            FORCE_APPLY = 2

        mode: "Instance.UpdatePolicy.Mode" = proto.Field(
            proto.ENUM,
            number=1,
            enum="Instance.UpdatePolicy.Mode",
        )

    class ClientConnectionConfig(proto.Message):
        r"""Client connection configuration

        Attributes:
            require_connectors (bool):
                Optional. Configuration to enforce connectors
                only (ex: AuthProxy) connections to the
                database.
            ssl_config (google.cloud.alloydb_v1alpha.types.SslConfig):
                Optional. SSL config option for this
                instance.
        """

        require_connectors: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        ssl_config: "SslConfig" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="SslConfig",
        )

    class PscInterfaceConfig(proto.Message):
        r"""Configuration for setting up a PSC interface. This
        information needs to be provided by the customer.
        PSC interfaces will be created and added to VMs via SLM (adding
        a network interface will require recreating the VM). For HA
        instances this will be done via LDTM.

        Attributes:
            consumer_endpoint_ips (MutableSequence[str]):
                A list of endpoints in the consumer VPC the
                interface might initiate outbound connections
                to. This list has to be provided when the PSC
                interface is created.
            network_attachment (str):
                The NetworkAttachment resource created in the consumer VPC
                to which the PSC interface will be linked, in the form of:
                "projects/${CONSUMER_PROJECT}/regions/${REGION}/networkAttachments/${NETWORK_ATTACHMENT_NAME}".
                NetworkAttachment has to be provided when the PSC interface
                is created.
        """

        consumer_endpoint_ips: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        network_attachment: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class PscInstanceConfig(proto.Message):
        r"""PscInstanceConfig contains PSC related configuration at an
        instance level.

        Attributes:
            service_attachment_link (str):
                Output only. The service attachment created
                when Private Service Connect (PSC) is enabled
                for the instance. The name of the resource will
                be in the format of
                projects/<alloydb-tenant-project-number>/regions/<region-name>/serviceAttachments/<service-attachment-name>
            allowed_consumer_projects (MutableSequence[str]):
                Optional. List of consumer projects that are
                allowed to create PSC endpoints to
                service-attachments to this instance.
            allowed_consumer_networks (MutableSequence[str]):
                Optional. List of consumer networks that are
                allowed to create PSC endpoints to
                service-attachments to this instance.
            psc_interface_configs (MutableSequence[google.cloud.alloydb_v1alpha.types.Instance.PscInterfaceConfig]):
                Optional. Configurations for setting up PSC
                interfaces attached to the instance which are
                used for outbound connectivity. Only primary
                instances can have PSC interface attached. All
                the VMs created for the primary instance will
                share the same configurations. Currently we only
                support 0 or 1 PSC interface.
            outgoing_service_attachment_links (MutableSequence[str]):
                Optional. List of service attachments that
                this instance has created endpoints to connect
                with. Currently, only a single outgoing service
                attachment is supported per instance.
            psc_enabled (bool):
                Optional. Whether PSC connectivity is enabled
                for this instance. This is populated by
                referencing the value from the parent cluster.
        """

        service_attachment_link: str = proto.Field(
            proto.STRING,
            number=1,
        )
        allowed_consumer_projects: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        allowed_consumer_networks: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=3,
        )
        psc_interface_configs: MutableSequence[
            "Instance.PscInterfaceConfig"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=4,
            message="Instance.PscInterfaceConfig",
        )
        outgoing_service_attachment_links: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=5,
        )
        psc_enabled: bool = proto.Field(
            proto.BOOL,
            number=6,
        )

    class InstanceNetworkConfig(proto.Message):
        r"""Metadata related to instance level network configuration.

        Attributes:
            authorized_external_networks (MutableSequence[google.cloud.alloydb_v1alpha.types.Instance.InstanceNetworkConfig.AuthorizedNetwork]):
                Optional. A list of external network
                authorized to access this instance.
            enable_public_ip (bool):
                Optional. Enabling public ip for the
                instance.
        """

        class AuthorizedNetwork(proto.Message):
            r"""AuthorizedNetwork contains metadata for an authorized
            network.

            Attributes:
                cidr_range (str):
                    CIDR range for one authorzied network of the
                    instance.
            """

            cidr_range: str = proto.Field(
                proto.STRING,
                number=1,
            )

        authorized_external_networks: MutableSequence[
            "Instance.InstanceNetworkConfig.AuthorizedNetwork"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="Instance.InstanceNetworkConfig.AuthorizedNetwork",
        )
        enable_public_ip: bool = proto.Field(
            proto.BOOL,
            number=2,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=8,
        enum=State,
    )
    instance_type: InstanceType = proto.Field(
        proto.ENUM,
        number=9,
        enum=InstanceType,
    )
    machine_config: MachineConfig = proto.Field(
        proto.MESSAGE,
        number=10,
        message=MachineConfig,
    )
    availability_type: AvailabilityType = proto.Field(
        proto.ENUM,
        number=11,
        enum=AvailabilityType,
    )
    gce_zone: str = proto.Field(
        proto.STRING,
        number=12,
    )
    database_flags: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=13,
    )
    writable_node: Node = proto.Field(
        proto.MESSAGE,
        number=19,
        message=Node,
    )
    nodes: MutableSequence[Node] = proto.RepeatedField(
        proto.MESSAGE,
        number=20,
        message=Node,
    )
    query_insights_config: QueryInsightsInstanceConfig = proto.Field(
        proto.MESSAGE,
        number=21,
        message=QueryInsightsInstanceConfig,
    )
    read_pool_config: ReadPoolConfig = proto.Field(
        proto.MESSAGE,
        number=14,
        message=ReadPoolConfig,
    )
    ip_address: str = proto.Field(
        proto.STRING,
        number=15,
    )
    public_ip_address: str = proto.Field(
        proto.STRING,
        number=27,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=16,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=17,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=18,
    )
    update_policy: UpdatePolicy = proto.Field(
        proto.MESSAGE,
        number=22,
        message=UpdatePolicy,
    )
    client_connection_config: ClientConnectionConfig = proto.Field(
        proto.MESSAGE,
        number=23,
        message=ClientConnectionConfig,
    )
    satisfies_pzi: bool = proto.Field(
        proto.BOOL,
        number=30,
    )
    satisfies_pzs: bool = proto.Field(
        proto.BOOL,
        number=24,
    )
    psc_instance_config: PscInstanceConfig = proto.Field(
        proto.MESSAGE,
        number=28,
        message=PscInstanceConfig,
    )
    network_config: InstanceNetworkConfig = proto.Field(
        proto.MESSAGE,
        number=29,
        message=InstanceNetworkConfig,
    )


class ConnectionInfo(proto.Message):
    r"""ConnectionInfo singleton resource.
    https://google.aip.dev/156

    Attributes:
        name (str):
            The name of the ConnectionInfo singleton resource, e.g.:
            projects/{project}/locations/{location}/clusters/\ */instances/*/connectionInfo
            This field currently has no semantic meaning.
        ip_address (str):
            Output only. The private network IP address for the
            Instance. This is the default IP for the instance and is
            always created (even if enable_public_ip is set). This is
            the connection endpoint for an end-user application.
        public_ip_address (str):
            Output only. The public IP addresses for the Instance. This
            is available ONLY when enable_public_ip is set. This is the
            connection endpoint for an end-user application.
        pem_certificate_chain (MutableSequence[str]):
            Output only. The pem-encoded chain that may
            be used to verify the X.509 certificate.
            Expected to be in issuer-to-root order according
            to RFC 5246.
        instance_uid (str):
            Output only. The unique ID of the Instance.
        psc_dns_name (str):
            Output only. The DNS name to use with PSC for
            the Instance.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ip_address: str = proto.Field(
        proto.STRING,
        number=2,
    )
    public_ip_address: str = proto.Field(
        proto.STRING,
        number=5,
    )
    pem_certificate_chain: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    instance_uid: str = proto.Field(
        proto.STRING,
        number=4,
    )
    psc_dns_name: str = proto.Field(
        proto.STRING,
        number=6,
    )


class Backup(proto.Message):
    r"""Message describing Backup object

    Attributes:
        name (str):
            Output only. The name of the backup resource with the
            format:

            -  projects/{project}/locations/{region}/backups/{backup_id}
               where the cluster and backup ID segments should satisfy
               the regex expression ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``,
               e.g. 1-63 characters of lowercase letters, numbers, and
               dashes, starting with a letter, and ending with a letter
               or number. For more details see
               https://google.aip.dev/122. The prefix of the backup
               resource name is the name of the parent resource:
            -  projects/{project}/locations/{region}
        display_name (str):
            User-settable and human-readable display name
            for the Backup.
        uid (str):
            Output only. The system-generated UID of the
            resource. The UID is assigned when the resource
            is created, and it is retained until it is
            deleted.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Create time stamp
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Update time stamp
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Delete time stamp
        labels (MutableMapping[str, str]):
            Labels as key value pairs
        state (google.cloud.alloydb_v1alpha.types.Backup.State):
            Output only. The current state of the backup.
        type_ (google.cloud.alloydb_v1alpha.types.Backup.Type):
            The backup type, which suggests the trigger
            for the backup.
        description (str):
            User-provided description of the backup.
        cluster_uid (str):
            Output only. The system-generated UID of the
            cluster which was used to create this resource.
        cluster_name (str):
            Required. The full resource name of the backup source
            cluster (e.g.,
            projects/{project}/locations/{region}/clusters/{cluster_id}).
        reconciling (bool):
            Output only. Reconciling
            (https://google.aip.dev/128#reconciliation), if
            true, indicates that the service is actively
            updating the resource. This can happen due to
            user-triggered updates or system actions like
            failover or maintenance.
        encryption_config (google.cloud.alloydb_v1alpha.types.EncryptionConfig):
            Optional. The encryption config can be
            specified to encrypt the backup with a
            customer-managed encryption key (CMEK). When
            this field is not specified, the backup will
            then use default encryption scheme to protect
            the user data.
        encryption_info (google.cloud.alloydb_v1alpha.types.EncryptionInfo):
            Output only. The encryption information for
            the backup.
        etag (str):
            For Resource freshness validation
            (https://google.aip.dev/154)
        annotations (MutableMapping[str, str]):
            Annotations to allow client tools to store
            small amount of arbitrary data. This is distinct
            from labels. https://google.aip.dev/128
        size_bytes (int):
            Output only. The size of the backup in bytes.
        expiry_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which after the backup is eligible
            to be garbage collected. It is the duration specified by the
            backup's retention policy, added to the backup's
            create_time.
        expiry_quantity (google.cloud.alloydb_v1alpha.types.Backup.QuantityBasedExpiry):
            Output only. The QuantityBasedExpiry of the
            backup, specified by the backup's retention
            policy. Once the expiry quantity is over
            retention, the backup is eligible to be garbage
            collected.
        satisfies_pzi (bool):
            Output only. Reserved for future use.
        satisfies_pzs (bool):
            Output only. Reserved for future use.
        database_version (google.cloud.alloydb_v1alpha.types.DatabaseVersion):
            Output only. The database engine major
            version of the cluster this backup was created
            from. Any restored cluster created from this
            backup will have the same database version.
    """

    class State(proto.Enum):
        r"""Backup State

        Values:
            STATE_UNSPECIFIED (0):
                The state of the backup is unknown.
            READY (1):
                The backup is ready.
            CREATING (2):
                The backup is creating.
            FAILED (3):
                The backup failed.
            DELETING (4):
                The backup is being deleted.
        """
        STATE_UNSPECIFIED = 0
        READY = 1
        CREATING = 2
        FAILED = 3
        DELETING = 4

    class Type(proto.Enum):
        r"""Backup Type

        Values:
            TYPE_UNSPECIFIED (0):
                Backup Type is unknown.
            ON_DEMAND (1):
                ON_DEMAND backups that were triggered by the customer (e.g.,
                not AUTOMATED).
            AUTOMATED (2):
                AUTOMATED backups triggered by the automated
                backups scheduler pursuant to an automated
                backup policy.
            CONTINUOUS (3):
                CONTINUOUS backups triggered by the automated
                backups scheduler due to a continuous backup
                policy.
        """
        TYPE_UNSPECIFIED = 0
        ON_DEMAND = 1
        AUTOMATED = 2
        CONTINUOUS = 3

    class QuantityBasedExpiry(proto.Message):
        r"""A backup's position in a quantity-based retention queue, of backups
        with the same source cluster and type, with length, retention,
        specified by the backup's retention policy. Once the position is
        greater than the retention, the backup is eligible to be garbage
        collected.

        Example: 5 backups from the same source cluster and type with a
        quantity-based retention of 3 and denoted by backup_id (position,
        retention).

        Safe: backup_5 (1, 3), backup_4, (2, 3), backup_3 (3, 3). Awaiting
        garbage collection: backup_2 (4, 3), backup_1 (5, 3)

        Attributes:
            retention_count (int):
                Output only. The backup's position among its
                backups with the same source cluster and type,
                by descending chronological order create
                time(i.e. newest first).
            total_retention_count (int):
                Output only. The length of the quantity-based
                queue, specified by the backup's retention
                policy.
        """

        retention_count: int = proto.Field(
            proto.INT32,
            number=1,
        )
        total_retention_count: int = proto.Field(
            proto.INT32,
            number=2,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=15,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=7,
        enum=State,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=8,
        enum=Type,
    )
    description: str = proto.Field(
        proto.STRING,
        number=9,
    )
    cluster_uid: str = proto.Field(
        proto.STRING,
        number=18,
    )
    cluster_name: str = proto.Field(
        proto.STRING,
        number=10,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=11,
    )
    encryption_config: "EncryptionConfig" = proto.Field(
        proto.MESSAGE,
        number=12,
        message="EncryptionConfig",
    )
    encryption_info: "EncryptionInfo" = proto.Field(
        proto.MESSAGE,
        number=13,
        message="EncryptionInfo",
    )
    etag: str = proto.Field(
        proto.STRING,
        number=14,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=16,
    )
    size_bytes: int = proto.Field(
        proto.INT64,
        number=17,
    )
    expiry_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=19,
        message=timestamp_pb2.Timestamp,
    )
    expiry_quantity: QuantityBasedExpiry = proto.Field(
        proto.MESSAGE,
        number=20,
        message=QuantityBasedExpiry,
    )
    satisfies_pzi: bool = proto.Field(
        proto.BOOL,
        number=23,
    )
    satisfies_pzs: bool = proto.Field(
        proto.BOOL,
        number=21,
    )
    database_version: "DatabaseVersion" = proto.Field(
        proto.ENUM,
        number=22,
        enum="DatabaseVersion",
    )


class SupportedDatabaseFlag(proto.Message):
    r"""SupportedDatabaseFlag gives general information about a database
    flag, like type and allowed values. This is a static value that is
    defined on the server side, and it cannot be modified by callers. To
    set the Database flags on a particular Instance, a caller should
    modify the Instance.database_flags field.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        string_restrictions (google.cloud.alloydb_v1alpha.types.SupportedDatabaseFlag.StringRestrictions):
            Restriction on STRING type value.

            This field is a member of `oneof`_ ``restrictions``.
        integer_restrictions (google.cloud.alloydb_v1alpha.types.SupportedDatabaseFlag.IntegerRestrictions):
            Restriction on INTEGER type value.

            This field is a member of `oneof`_ ``restrictions``.
        name (str):
            The name of the flag resource, following Google Cloud
            conventions, e.g.:

            -  projects/{project}/locations/{location}/flags/{flag} This
               field currently has no semantic meaning.
        flag_name (str):
            The name of the database flag, e.g. "max_allowed_packets".
            The is a possibly key for the Instance.database_flags map
            field.
        value_type (google.cloud.alloydb_v1alpha.types.SupportedDatabaseFlag.ValueType):

        accepts_multiple_values (bool):
            Whether the database flag accepts multiple
            values. If true, a comma-separated list of
            stringified values may be specified.
        supported_db_versions (MutableSequence[google.cloud.alloydb_v1alpha.types.DatabaseVersion]):
            Major database engine versions for which this
            flag is supported.
        requires_db_restart (bool):
            Whether setting or updating this flag on an
            Instance requires a database restart. If a flag
            that requires database restart is set, the
            backend will automatically restart the database
            (making sure to satisfy any availability SLO's).
    """

    class ValueType(proto.Enum):
        r"""ValueType describes the semantic type of the value that the flag
        accepts. Regardless of the ValueType, the Instance.database_flags
        field accepts the stringified version of the value, i.e. "20" or
        "3.14".

        Values:
            VALUE_TYPE_UNSPECIFIED (0):
                This is an unknown flag type.
            STRING (1):
                String type flag.
            INTEGER (2):
                Integer type flag.
            FLOAT (3):
                Float type flag.
            NONE (4):
                Denotes that the flag does not accept any
                values.
        """
        VALUE_TYPE_UNSPECIFIED = 0
        STRING = 1
        INTEGER = 2
        FLOAT = 3
        NONE = 4

    class StringRestrictions(proto.Message):
        r"""Restrictions on STRING type values

        Attributes:
            allowed_values (MutableSequence[str]):
                The list of allowed values, if bounded. This
                field will be empty if there is a unbounded
                number of allowed values.
        """

        allowed_values: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    class IntegerRestrictions(proto.Message):
        r"""Restrictions on INTEGER type values.

        Attributes:
            min_value (google.protobuf.wrappers_pb2.Int64Value):
                The minimum value that can be specified, if
                applicable.
            max_value (google.protobuf.wrappers_pb2.Int64Value):
                The maximum value that can be specified, if
                applicable.
        """

        min_value: wrappers_pb2.Int64Value = proto.Field(
            proto.MESSAGE,
            number=1,
            message=wrappers_pb2.Int64Value,
        )
        max_value: wrappers_pb2.Int64Value = proto.Field(
            proto.MESSAGE,
            number=2,
            message=wrappers_pb2.Int64Value,
        )

    string_restrictions: StringRestrictions = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="restrictions",
        message=StringRestrictions,
    )
    integer_restrictions: IntegerRestrictions = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="restrictions",
        message=IntegerRestrictions,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    flag_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    value_type: ValueType = proto.Field(
        proto.ENUM,
        number=3,
        enum=ValueType,
    )
    accepts_multiple_values: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    supported_db_versions: MutableSequence["DatabaseVersion"] = proto.RepeatedField(
        proto.ENUM,
        number=5,
        enum="DatabaseVersion",
    )
    requires_db_restart: bool = proto.Field(
        proto.BOOL,
        number=6,
    )


class User(proto.Message):
    r"""Message describing User object.

    Attributes:
        name (str):
            Output only. Name of the resource in the form
            of
            projects/{project}/locations/{location}/cluster/{cluster}/users/{user}.
        password (str):
            Input only. Password for the user.
        database_roles (MutableSequence[str]):
            Optional. List of database roles this user
            has. The database role strings are subject to
            the PostgreSQL naming conventions.
        user_type (google.cloud.alloydb_v1alpha.types.User.UserType):
            Optional. Type of this user.
    """

    class UserType(proto.Enum):
        r"""Enum that details the user type.

        Values:
            USER_TYPE_UNSPECIFIED (0):
                Unspecified user type.
            ALLOYDB_BUILT_IN (1):
                The default user type that authenticates via
                password-based authentication.
            ALLOYDB_IAM_USER (2):
                Database user that can authenticate via
                IAM-Based authentication.
        """
        USER_TYPE_UNSPECIFIED = 0
        ALLOYDB_BUILT_IN = 1
        ALLOYDB_IAM_USER = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    password: str = proto.Field(
        proto.STRING,
        number=2,
    )
    database_roles: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    user_type: UserType = proto.Field(
        proto.ENUM,
        number=5,
        enum=UserType,
    )


class Database(proto.Message):
    r"""Message describing Database object.

    Attributes:
        name (str):
            Identifier. Name of the resource in the form
            of
            projects/{project}/locations/{location}/clusters/{cluster}/databases/{database}.
        charset (str):
            Optional. Charset for the database. This field can contain
            any PostgreSQL supported charset name. Example values
            include "UTF8", "SQL_ASCII", etc.
        collation (str):
            Optional. Collation for the database.
            Name of the custom or native collation for
            postgres. Example values include "C", "POSIX",
            etc
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    charset: str = proto.Field(
        proto.STRING,
        number=2,
    )
    collation: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
