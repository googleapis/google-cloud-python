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
        "VolumeBackup",
        "VolumeRestore",
    },
)


class VolumeBackup(proto.Message):
    r"""Represents the backup of a specific persistent volume as a
    component of a Backup - both the record of the operation and a
    pointer to the underlying storage-specific artifacts.
    Next id: 14

    Attributes:
        name (str):
            Output only. The full name of the VolumeBackup resource.
            Format:
            ``projects/*/locations/*/backupPlans/*/backups/*/volumeBackups/*``.
        uid (str):
            Output only. Server generated global unique identifier of
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__
            format.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this
            VolumeBackup resource was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this
            VolumeBackup resource was last updated.
        source_pvc (google.cloud.gke_backup_v1.types.NamespacedName):
            Output only. A reference to the source
            Kubernetes PVC from which this VolumeBackup was
            created.
        volume_backup_handle (str):
            Output only. A storage system-specific opaque
            handle to the underlying volume backup.
        format_ (google.cloud.gke_backup_v1.types.VolumeBackup.VolumeBackupFormat):
            Output only. The format used for the volume
            backup.
        storage_bytes (int):
            Output only. The aggregate size of the
            underlying artifacts associated with this
            VolumeBackup in the backup storage. This may
            change over time when multiple backups of the
            same volume share the same backup storage
            location. In particular, this is likely to
            increase in size when the immediately preceding
            backup of the same volume is deleted.
        disk_size_bytes (int):
            Output only. The minimum size of the disk to
            which this VolumeBackup can be restored.
        complete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the
            associated underlying volume backup operation
            completed.
        state (google.cloud.gke_backup_v1.types.VolumeBackup.State):
            Output only. The current state of this
            VolumeBackup.
        state_message (str):
            Output only. A human readable message
            explaining why the VolumeBackup is in its
            current state.
        etag (str):
            Output only. ``etag`` is used for optimistic concurrency
            control as a way to help prevent simultaneous updates of a
            volume backup from overwriting each other. It is strongly
            suggested that systems make use of the ``etag`` in the
            read-modify-write cycle to perform volume backup updates in
            order to avoid race conditions.
    """

    class VolumeBackupFormat(proto.Enum):
        r"""Identifies the format used for the volume backup."""
        VOLUME_BACKUP_FORMAT_UNSPECIFIED = 0
        GCE_PERSISTENT_DISK = 1

    class State(proto.Enum):
        r"""The current state of a VolumeBackup"""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        SNAPSHOTTING = 2
        UPLOADING = 3
        SUCCEEDED = 4
        FAILED = 5
        DELETING = 6

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
    source_pvc = proto.Field(
        proto.MESSAGE,
        number=5,
        message=common.NamespacedName,
    )
    volume_backup_handle = proto.Field(
        proto.STRING,
        number=6,
    )
    format_ = proto.Field(
        proto.ENUM,
        number=7,
        enum=VolumeBackupFormat,
    )
    storage_bytes = proto.Field(
        proto.INT64,
        number=8,
    )
    disk_size_bytes = proto.Field(
        proto.INT64,
        number=9,
    )
    complete_time = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    state = proto.Field(
        proto.ENUM,
        number=11,
        enum=State,
    )
    state_message = proto.Field(
        proto.STRING,
        number=12,
    )
    etag = proto.Field(
        proto.STRING,
        number=13,
    )


class VolumeRestore(proto.Message):
    r"""Represents the operation of restoring a volume from a
    VolumeBackup. Next id: 13

    Attributes:
        name (str):
            Output only. Full name of the VolumeRestore resource.
            Format:
            ``projects/*/locations/*/restorePlans/*/restores/*/volumeRestores/*``.
        uid (str):
            Output only. Server generated global unique identifier of
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__
            format.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this
            VolumeRestore resource was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this
            VolumeRestore resource was last updated.
        volume_backup (str):
            Output only. The full name of the VolumeBackup from which
            the volume will be restored. Format:
            ``projects/*/locations/*/backupPlans/*/backups/*/volumeBackups/*``.
        target_pvc (google.cloud.gke_backup_v1.types.NamespacedName):
            Output only. The reference to the target
            Kubernetes PVC to be restored.
        volume_handle (str):
            Output only. A storage system-specific opaque
            handler to the underlying volume created for the
            target PVC from the volume backup.
        volume_type (google.cloud.gke_backup_v1.types.VolumeRestore.VolumeType):
            Output only. The type of volume provisioned
        complete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the
            associated underlying volume restoration
            completed.
        state (google.cloud.gke_backup_v1.types.VolumeRestore.State):
            Output only. The current state of this
            VolumeRestore.
        state_message (str):
            Output only. A human readable message
            explaining why the VolumeRestore is in its
            current state.
        etag (str):
            Output only. ``etag`` is used for optimistic concurrency
            control as a way to help prevent simultaneous updates of a
            volume restore from overwriting each other. It is strongly
            suggested that systems make use of the ``etag`` in the
            read-modify-write cycle to perform volume restore updates in
            order to avoid race conditions.
    """

    class VolumeType(proto.Enum):
        r"""Supported volume types."""
        VOLUME_TYPE_UNSPECIFIED = 0
        GCE_PERSISTENT_DISK = 1

    class State(proto.Enum):
        r"""The current state of a VolumeRestore"""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        RESTORING = 2
        SUCCEEDED = 3
        FAILED = 4
        DELETING = 5

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
    volume_backup = proto.Field(
        proto.STRING,
        number=5,
    )
    target_pvc = proto.Field(
        proto.MESSAGE,
        number=6,
        message=common.NamespacedName,
    )
    volume_handle = proto.Field(
        proto.STRING,
        number=7,
    )
    volume_type = proto.Field(
        proto.ENUM,
        number=8,
        enum=VolumeType,
    )
    complete_time = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    state = proto.Field(
        proto.ENUM,
        number=10,
        enum=State,
    )
    state_message = proto.Field(
        proto.STRING,
        number=11,
    )
    etag = proto.Field(
        proto.STRING,
        number=12,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
