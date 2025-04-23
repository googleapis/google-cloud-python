# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.gkebackup.v1",
    manifest={
        "BackupPlanBinding",
    },
)


class BackupPlanBinding(proto.Message):
    r"""A BackupPlanBinding binds a BackupPlan with a BackupChannel.
    This resource is created automatically when a BackupPlan is
    created using a BackupChannel. This also serves as a holder for
    cross-project fields that need to be displayed in the current
    project.

    Attributes:
        name (str):
            Identifier. The fully qualified name of the
            BackupPlanBinding.
            ``projects/*/locations/*/backupChannels/*/backupPlanBindings/*``
        uid (str):
            Output only. Server generated global unique identifier of
            `UUID4 <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this binding
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this binding
            was created.
        backup_plan (str):
            Output only. Immutable. The fully qualified name of the
            BackupPlan bound with the parent BackupChannel.
            ``projects/*/locations/*/backupPlans/{backup_plan}``
        cluster (str):
            Output only. Immutable. The fully qualified name of the
            cluster that is being backed up Valid formats:

            -  ``projects/*/locations/*/clusters/*``
            -  ``projects/*/zones/*/clusters/*``
        backup_plan_details (google.cloud.gke_backup_v1.types.BackupPlanBinding.BackupPlanDetails):
            Output only. Contains details about the
            backup plan/backup.
        etag (str):
            Output only. ``etag`` is used for optimistic concurrency
            control as a way to help prevent simultaneous updates of a
            BackupPlanBinding from overwriting each other. It is
            strongly suggested that systems make use of the 'etag' in
            the read-modify-write cycle to perform BackupPlanBinding
            updates in order to avoid race conditions: An ``etag`` is
            returned in the response to ``GetBackupPlanBinding``, and
            systems are expected to put that etag in the request to
            ``UpdateBackupPlanBinding`` or ``DeleteBackupPlanBinding``
            to ensure that their change will be applied to the same
            version of the resource.
    """

    class BackupPlanDetails(proto.Message):
        r"""Contains metadata about the backup plan/backup.

        Attributes:
            protected_pod_count (int):
                Output only. The number of Kubernetes Pods
                backed up in the last successful Backup created
                via this BackupPlan.
            state (google.cloud.gke_backup_v1.types.BackupPlanBinding.BackupPlanDetails.State):
                Output only. State of the BackupPlan.
            last_successful_backup_time (google.protobuf.timestamp_pb2.Timestamp):
                Output only. Completion time of the last successful Backup.
                This is sourced from a successful Backup's complete_time
                field.
            next_scheduled_backup_time (google.protobuf.timestamp_pb2.Timestamp):
                Output only. Start time of next scheduled backup under this
                BackupPlan by either cron_schedule or rpo config. This is
                sourced from BackupPlan.
            rpo_risk_level (int):
                Output only. A number that represents the
                current risk level of this BackupPlan from RPO
                perspective with 1 being no risk and 5 being
                highest risk.
            last_successful_backup (str):
                Output only. The fully qualified name of the last successful
                Backup created under this BackupPlan.
                ``projects/*/locations/*/backupPlans/*/backups/*``
        """

        class State(proto.Enum):
            r"""State

            Values:
                STATE_UNSPECIFIED (0):
                    Default first value for Enums.
                CLUSTER_PENDING (1):
                    Waiting for cluster state to be RUNNING.
                PROVISIONING (2):
                    The BackupPlan is in the process of being
                    created.
                READY (3):
                    The BackupPlan has successfully been created
                    and is ready for Backups.
                FAILED (4):
                    BackupPlan creation has failed.
                DEACTIVATED (5):
                    The BackupPlan has been deactivated.
                DELETING (6):
                    The BackupPlan is in the process of being
                    deleted.
            """
            STATE_UNSPECIFIED = 0
            CLUSTER_PENDING = 1
            PROVISIONING = 2
            READY = 3
            FAILED = 4
            DEACTIVATED = 5
            DELETING = 6

        protected_pod_count: int = proto.Field(
            proto.INT32,
            number=1,
        )
        state: "BackupPlanBinding.BackupPlanDetails.State" = proto.Field(
            proto.ENUM,
            number=2,
            enum="BackupPlanBinding.BackupPlanDetails.State",
        )
        last_successful_backup_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=3,
            message=timestamp_pb2.Timestamp,
        )
        next_scheduled_backup_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=4,
            message=timestamp_pb2.Timestamp,
        )
        rpo_risk_level: int = proto.Field(
            proto.INT32,
            number=5,
        )
        last_successful_backup: str = proto.Field(
            proto.STRING,
            number=6,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    backup_plan: str = proto.Field(
        proto.STRING,
        number=5,
    )
    cluster: str = proto.Field(
        proto.STRING,
        number=6,
    )
    backup_plan_details: BackupPlanDetails = proto.Field(
        proto.MESSAGE,
        number=7,
        message=BackupPlanDetails,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=8,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
