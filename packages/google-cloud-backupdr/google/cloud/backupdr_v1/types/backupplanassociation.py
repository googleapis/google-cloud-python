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
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.backupdr.v1",
    manifest={
        "BackupPlanAssociation",
        "RuleConfigInfo",
        "CreateBackupPlanAssociationRequest",
        "ListBackupPlanAssociationsRequest",
        "ListBackupPlanAssociationsResponse",
        "GetBackupPlanAssociationRequest",
        "DeleteBackupPlanAssociationRequest",
        "TriggerBackupRequest",
    },
)


class BackupPlanAssociation(proto.Message):
    r"""A BackupPlanAssociation represents a single
    BackupPlanAssociation which contains details like workload,
    backup plan etc

    Attributes:
        name (str):
            Output only. Identifier. The resource name of
            BackupPlanAssociation in below format Format :

            projects/{project}/locations/{location}/backupPlanAssociations/{backupPlanAssociationId}
        resource_type (str):
            Required. Immutable. Resource type of
            workload on which backupplan is applied
        resource (str):
            Required. Immutable. Resource name of
            workload on which backupplan is applied
        backup_plan (str):
            Required. Resource name of backup plan which
            needs to be applied on workload. Format:

            projects/{project}/locations/{location}/backupPlans/{backupPlanId}
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the instance was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the instance was
            updated.
        state (google.cloud.backupdr_v1.types.BackupPlanAssociation.State):
            Output only. The BackupPlanAssociation
            resource state.
        rules_config_info (MutableSequence[google.cloud.backupdr_v1.types.RuleConfigInfo]):
            Output only. The config info related to
            backup rules.
        data_source (str):
            Output only. Resource name of data source
            which will be used as storage location for
            backups taken. Format :

            projects/{project}/locations/{location}/backupVaults/{backupvault}/dataSources/{datasource}
    """

    class State(proto.Enum):
        r"""Enum for State of BackupPlan Association

        Values:
            STATE_UNSPECIFIED (0):
                State not set.
            CREATING (1):
                The resource is being created.
            ACTIVE (2):
                The resource has been created and is fully
                usable.
            DELETING (3):
                The resource is being deleted.
            INACTIVE (4):
                The resource has been created but is not
                usable.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        DELETING = 3
        INACTIVE = 4

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    resource_type: str = proto.Field(
        proto.STRING,
        number=2,
    )
    resource: str = proto.Field(
        proto.STRING,
        number=3,
    )
    backup_plan: str = proto.Field(
        proto.STRING,
        number=4,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=7,
        enum=State,
    )
    rules_config_info: MutableSequence["RuleConfigInfo"] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="RuleConfigInfo",
    )
    data_source: str = proto.Field(
        proto.STRING,
        number=9,
    )


class RuleConfigInfo(proto.Message):
    r"""Message for rules config info.

    Attributes:
        rule_id (str):
            Output only. Backup Rule id fetched from
            backup plan.
        last_backup_state (google.cloud.backupdr_v1.types.RuleConfigInfo.LastBackupState):
            Output only. The last backup state for rule.
        last_backup_error (google.rpc.status_pb2.Status):
            Output only. google.rpc.Status object to
            store the last backup error.
        last_successful_backup_consistency_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The point in time when the last
            successful backup was captured from the source.
    """

    class LastBackupState(proto.Enum):
        r"""Enum for LastBackupState

        Values:
            LAST_BACKUP_STATE_UNSPECIFIED (0):
                State not set.
            FIRST_BACKUP_PENDING (1):
                The first backup is pending.
            PERMISSION_DENIED (2):
                The most recent backup could not be
                run/failed because of the lack of permissions.
            SUCCEEDED (3):
                The last backup operation succeeded.
            FAILED (4):
                The last backup operation failed.
        """
        LAST_BACKUP_STATE_UNSPECIFIED = 0
        FIRST_BACKUP_PENDING = 1
        PERMISSION_DENIED = 2
        SUCCEEDED = 3
        FAILED = 4

    rule_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    last_backup_state: LastBackupState = proto.Field(
        proto.ENUM,
        number=3,
        enum=LastBackupState,
    )
    last_backup_error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=4,
        message=status_pb2.Status,
    )
    last_successful_backup_consistency_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )


class CreateBackupPlanAssociationRequest(proto.Message):
    r"""Request message for creating a backup plan.

    Attributes:
        parent (str):
            Required. The backup plan association project and location
            in the format
            ``projects/{project_id}/locations/{location}``. In Cloud
            BackupDR locations map to GCP regions, for example
            **us-central1**.
        backup_plan_association_id (str):
            Required. The name of the backup plan
            association to create. The name must be unique
            for the specified project and location.
        backup_plan_association (google.cloud.backupdr_v1.types.BackupPlanAssociation):
            Required. The resource being created
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    backup_plan_association_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    backup_plan_association: "BackupPlanAssociation" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="BackupPlanAssociation",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListBackupPlanAssociationsRequest(proto.Message):
    r"""Request message for List BackupPlanAssociation

    Attributes:
        parent (str):
            Required. The project and location for which to retrieve
            backup Plan Associations information, in the format
            ``projects/{project_id}/locations/{location}``. In Cloud
            BackupDR, locations map to GCP regions, for example
            **us-central1**. To retrieve backup plan associations for
            all locations, use "-" for the ``{location}`` value.
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
        filter (str):
            Optional. Filtering results
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListBackupPlanAssociationsResponse(proto.Message):
    r"""Response message for List BackupPlanAssociation

    Attributes:
        backup_plan_associations (MutableSequence[google.cloud.backupdr_v1.types.BackupPlanAssociation]):
            The list of Backup Plan Associations in the project for the
            specified location.

            If the ``{location}`` value in the request is "-", the
            response contains a list of instances from all locations. In
            case any location is unreachable, the response will only
            return backup plan associations in reachable locations and
            the 'unreachable' field will be populated with a list of
            unreachable locations.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    backup_plan_associations: MutableSequence[
        "BackupPlanAssociation"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="BackupPlanAssociation",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetBackupPlanAssociationRequest(proto.Message):
    r"""Request message for getting a BackupPlanAssociation resource.

    Attributes:
        name (str):
            Required. Name of the backup plan association resource, in
            the format
            ``projects/{project}/locations/{location}/backupPlanAssociations/{backupPlanAssociationId}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteBackupPlanAssociationRequest(proto.Message):
    r"""Request message for deleting a backup plan association.

    Attributes:
        name (str):
            Required. Name of the backup plan association resource, in
            the format
            ``projects/{project}/locations/{location}/backupPlanAssociations/{backupPlanAssociationId}``
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class TriggerBackupRequest(proto.Message):
    r"""Request message for triggering a backup.

    Attributes:
        name (str):
            Required. Name of the backup plan association resource, in
            the format
            ``projects/{project}/locations/{location}/backupPlanAssociations/{backupPlanAssociationId}``
        rule_id (str):
            Required. backup rule_id for which a backup needs to be
            triggered.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    rule_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
