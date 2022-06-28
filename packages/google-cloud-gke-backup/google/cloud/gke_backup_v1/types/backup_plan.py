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

from google.cloud.gke_backup_v1.types import common
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.gkebackup.v1",
    manifest={
        "BackupPlan",
    },
)


class BackupPlan(proto.Message):
    r"""Defines the configuration and scheduling for a "line" of
    Backups.

    Attributes:
        name (str):
            Output only. The full name of the BackupPlan resource.
            Format: projects/\ */locations/*/backupPlans/\*
        uid (str):
            Output only. Server generated global unique identifier of
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__
            format.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this
            BackupPlan resource was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this
            BackupPlan resource was last updated.
        description (str):
            User specified descriptive string for this
            BackupPlan.
        cluster (str):
            Required. Immutable. The source cluster from which Backups
            will be created via this BackupPlan. Valid formats:

            -  projects/\ */locations/*/clusters/\*
            -  projects/\ */zones/*/clusters/\*
        retention_policy (google.cloud.gke_backup_v1.types.BackupPlan.RetentionPolicy):
            RetentionPolicy governs lifecycle of Backups
            created under this plan.
        labels (Mapping[str, str]):
            A set of custom labels supplied by user.
        backup_schedule (google.cloud.gke_backup_v1.types.BackupPlan.Schedule):
            Defines a schedule for automatic Backup
            creation via this BackupPlan.
        etag (str):
            Output only. ``etag`` is used for optimistic concurrency
            control as a way to help prevent simultaneous updates of a
            backup plan from overwriting each other. It is strongly
            suggested that systems make use of the 'etag' in the
            read-modify-write cycle to perform BackupPlan updates in
            order to avoid race conditions: An ``etag`` is returned in
            the response to ``GetBackupPlan``, and systems are expected
            to put that etag in the request to ``UpdateBackupPlan`` or
            ``DeleteBackupPlan`` to ensure that their change will be
            applied to the same version of the resource.
        deactivated (bool):
            This flag indicates whether this BackupPlan
            has been deactivated. Setting this field to True
            locks the BackupPlan such that no further
            updates will be allowed (except deletes),
            including the deactivated field itself. It also
            prevents any new Backups from being created via
            this BackupPlan (including scheduled Backups).

            Default: False
        backup_config (google.cloud.gke_backup_v1.types.BackupPlan.BackupConfig):
            Defines the configuration of Backups created
            via this BackupPlan.
        protected_pod_count (int):
            Output only. The number of Kubernetes Pods
            backed up in the last successful Backup created
            via this BackupPlan.
    """

    class RetentionPolicy(proto.Message):
        r"""RetentionPolicy defines a Backup retention policy for a
        BackupPlan.

        Attributes:
            backup_delete_lock_days (int):
                Minimum age for Backups created via this BackupPlan (in
                days). This field MUST be an integer value between 0-90
                (inclusive). A Backup created under this BackupPlan will NOT
                be deletable until it reaches Backup's (create_time +
                backup_delete_lock_days). Updating this field of a
                BackupPlan does NOT affect existing Backups under it.
                Backups created AFTER a successful update will inherit the
                new value.

                Default: 0 (no delete blocking)
            backup_retain_days (int):
                The default maximum age of a Backup created via this
                BackupPlan. This field MUST be an integer value >= 0. If
                specified, a Backup created under this BackupPlan will be
                automatically deleted after its age reaches (create_time +
                backup_retain_days). If not specified, Backups created under
                this BackupPlan will NOT be subject to automatic deletion.
                Updating this field does NOT affect existing Backups under
                it. Backups created AFTER a successful update will
                automatically pick up the new value. NOTE:
                backup_retain_days must be >=
                [backup_delete_lock_days][google.cloud.gkebackup.v1.BackupPlan.RetentionPolicy.backup_delete_lock_days].

                Default: 0 (no automatic deletion)
            locked (bool):
                This flag denotes whether the retention policy of this
                BackupPlan is locked. If set to True, no further update is
                allowed on this policy, including the ``locked`` field
                itself.

                Default: False
        """

        backup_delete_lock_days = proto.Field(
            proto.INT32,
            number=1,
        )
        backup_retain_days = proto.Field(
            proto.INT32,
            number=2,
        )
        locked = proto.Field(
            proto.BOOL,
            number=3,
        )

    class Schedule(proto.Message):
        r"""Schedule defines scheduling parameters for automatically
        creating Backups via this BackupPlan.

        Attributes:
            cron_schedule (str):
                A standard `cron <https://wikipedia.com/wiki/cron>`__ string
                that defines a repeating schedule for creating Backups via
                this BackupPlan.

                Default (empty): no automatic backup creation will occur.
            paused (bool):
                This flag denotes whether automatic Backup
                creation is paused for this BackupPlan.

                Default: False
        """

        cron_schedule = proto.Field(
            proto.STRING,
            number=1,
        )
        paused = proto.Field(
            proto.BOOL,
            number=2,
        )

    class BackupConfig(proto.Message):
        r"""BackupConfig defines the configuration of Backups created via
        this BackupPlan.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            all_namespaces (bool):
                If True, include all namespaced resources

                This field is a member of `oneof`_ ``backup_scope``.
            selected_namespaces (google.cloud.gke_backup_v1.types.Namespaces):
                If set, include just the resources in the
                listed namespaces.

                This field is a member of `oneof`_ ``backup_scope``.
            selected_applications (google.cloud.gke_backup_v1.types.NamespacedNames):
                If set, include just the resources referenced
                by the listed ProtectedApplications.

                This field is a member of `oneof`_ ``backup_scope``.
            include_volume_data (bool):
                This flag specifies whether volume data
                should be backed up when PVCs are included in
                the scope of a Backup.
                Default: False
            include_secrets (bool):
                This flag specifies whether Kubernetes Secret
                resources should be included when they fall into
                the scope of Backups.
                Default: False
            encryption_key (google.cloud.gke_backup_v1.types.EncryptionKey):
                This defines a customer managed encryption
                key that will be used to encrypt the "config"
                portion (the Kubernetes resources) of Backups
                created via this plan.

                Default (empty): Config backup artifacts will
                not be encrypted.
        """

        all_namespaces = proto.Field(
            proto.BOOL,
            number=1,
            oneof="backup_scope",
        )
        selected_namespaces = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="backup_scope",
            message=common.Namespaces,
        )
        selected_applications = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="backup_scope",
            message=common.NamespacedNames,
        )
        include_volume_data = proto.Field(
            proto.BOOL,
            number=4,
        )
        include_secrets = proto.Field(
            proto.BOOL,
            number=5,
        )
        encryption_key = proto.Field(
            proto.MESSAGE,
            number=6,
            message=common.EncryptionKey,
        )

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    uid = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    description = proto.Field(
        proto.STRING,
        number=5,
    )
    cluster = proto.Field(
        proto.STRING,
        number=6,
    )
    retention_policy = proto.Field(
        proto.MESSAGE,
        number=7,
        message=RetentionPolicy,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=8,
    )
    backup_schedule = proto.Field(
        proto.MESSAGE,
        number=9,
        message=Schedule,
    )
    etag = proto.Field(
        proto.STRING,
        number=10,
    )
    deactivated = proto.Field(
        proto.BOOL,
        number=11,
    )
    backup_config = proto.Field(
        proto.MESSAGE,
        number=12,
        message=BackupConfig,
    )
    protected_pod_count = proto.Field(
        proto.INT32,
        number=13,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
