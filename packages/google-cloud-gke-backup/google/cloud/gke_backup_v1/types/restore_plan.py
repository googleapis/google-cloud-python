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

from google.cloud.gke_backup_v1.types import restore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.gkebackup.v1",
    manifest={
        "RestorePlan",
    },
)


class RestorePlan(proto.Message):
    r"""The configuration of a potential series of Restore operations
    to be performed against Backups belong to a particular
    BackupPlan. Next id: 11

    Attributes:
        name (str):
            Output only. The full name of the RestorePlan resource.
            Format: ``projects/*/locations/*/restorePlans/*``.
        uid (str):
            Output only. Server generated global unique identifier of
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__
            format.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this
            RestorePlan resource was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this
            RestorePlan resource was last updated.
        description (str):
            User specified descriptive string for this
            RestorePlan.
        backup_plan (str):
            Required. Immutable. A reference to the
            [BackupPlan][google.cloud.gkebackup.v1.BackupPlan] from
            which Backups may be used as the source for Restores created
            via this RestorePlan. Format:
            ``projects/*/locations/*/backupPlans/*``.
        cluster (str):
            Required. Immutable. The target cluster into which Restores
            created via this RestorePlan will restore data. NOTE: the
            cluster's region must be the same as the RestorePlan. Valid
            formats:

            -  ``projects/*/locations/*/clusters/*``
            -  ``projects/*/zones/*/clusters/*``
        restore_config (google.cloud.gke_backup_v1.types.RestoreConfig):
            Required. Configuration of Restores created
            via this RestorePlan.
        labels (Mapping[str, str]):
            A set of custom labels supplied by user.
        etag (str):
            Output only. ``etag`` is used for optimistic concurrency
            control as a way to help prevent simultaneous updates of a
            restore from overwriting each other. It is strongly
            suggested that systems make use of the ``etag`` in the
            read-modify-write cycle to perform restore updates in order
            to avoid race conditions: An ``etag`` is returned in the
            response to ``GetRestorePlan``, and systems are expected to
            put that etag in the request to ``UpdateRestorePlan`` or
            ``DeleteRestorePlan`` to ensure that their change will be
            applied to the same version of the resource.
    """

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
    backup_plan = proto.Field(
        proto.STRING,
        number=6,
    )
    cluster = proto.Field(
        proto.STRING,
        number=7,
    )
    restore_config = proto.Field(
        proto.MESSAGE,
        number=8,
        message=restore.RestoreConfig,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    etag = proto.Field(
        proto.STRING,
        number=10,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
