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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.netapp.v1",
    manifest={
        "BackupVault",
        "GetBackupVaultRequest",
        "ListBackupVaultsRequest",
        "ListBackupVaultsResponse",
        "CreateBackupVaultRequest",
        "DeleteBackupVaultRequest",
        "UpdateBackupVaultRequest",
    },
)


class BackupVault(proto.Message):
    r"""A NetApp BackupVault.

    Attributes:
        name (str):
            Identifier. The resource name of the backup vault. Format:
            ``projects/{project_id}/locations/{location}/backupVaults/{backup_vault_id}``.
        state (google.cloud.netapp_v1.types.BackupVault.State):
            Output only. The backup vault state.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Create time of the backup vault.
        description (str):
            Description of the backup vault.
        labels (MutableMapping[str, str]):
            Resource labels to represent user provided
            metadata.
    """

    class State(proto.Enum):
        r"""The Backup Vault States

        Values:
            STATE_UNSPECIFIED (0):
                State not set.
            CREATING (1):
                BackupVault is being created.
            READY (2):
                BackupVault is available for use.
            DELETING (3):
                BackupVault is being deleted.
            ERROR (4):
                BackupVault is not valid and cannot be used.
            UPDATING (5):
                BackupVault is being updated.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        DELETING = 3
        ERROR = 4
        UPDATING = 5

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )


class GetBackupVaultRequest(proto.Message):
    r"""GetBackupVaultRequest gets the state of a backupVault.

    Attributes:
        name (str):
            Required. The backupVault resource name, in the format
            ``projects/{project_id}/locations/{location}/backupVaults/{backup_vault_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListBackupVaultsRequest(proto.Message):
    r"""ListBackupVaultsRequest lists backupVaults.

    Attributes:
        parent (str):
            Required. The location for which to retrieve backupVault
            information, in the format
            ``projects/{project_id}/locations/{location}``.
        page_size (int):
            The maximum number of items to return.
        page_token (str):
            The next_page_token value to use if there are additional
            results to retrieve for this list request.
        order_by (str):
            Sort results. Supported values are "name",
            "name desc" or "" (unsorted).
        filter (str):
            List filter.
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
    order_by: str = proto.Field(
        proto.STRING,
        number=4,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListBackupVaultsResponse(proto.Message):
    r"""ListBackupVaultsResponse is the result of
    ListBackupVaultsRequest.

    Attributes:
        backup_vaults (MutableSequence[google.cloud.netapp_v1.types.BackupVault]):
            A list of backupVaults in the project for the
            specified location.
        next_page_token (str):
            The token you can use to retrieve the next
            page of results. Not returned if there are no
            more results in the list.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    backup_vaults: MutableSequence["BackupVault"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="BackupVault",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class CreateBackupVaultRequest(proto.Message):
    r"""CreateBackupVaultRequest creates a backup vault.

    Attributes:
        parent (str):
            Required. The location to create the backup vaults, in the
            format ``projects/{project_id}/locations/{location}``
        backup_vault_id (str):
            Required. The ID to use for the backupVault. The ID must be
            unique within the specified location. The max supported
            length is 63 characters. This value must start with a
            lowercase letter followed by up to 62 lowercase letters,
            numbers, or hyphens, and cannot end with a hyphen. Values
            that do not match this pattern will trigger an
            INVALID_ARGUMENT error.
        backup_vault (google.cloud.netapp_v1.types.BackupVault):
            Required. A backupVault resource
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    backup_vault_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    backup_vault: "BackupVault" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="BackupVault",
    )


class DeleteBackupVaultRequest(proto.Message):
    r"""DeleteBackupVaultRequest deletes a backupVault.

    Attributes:
        name (str):
            Required. The backupVault resource name, in the format
            ``projects/{project_id}/locations/{location}/backupVaults/{backup_vault_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateBackupVaultRequest(proto.Message):
    r"""UpdateBackupVaultRequest updates description and/or labels
    for a backupVault.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the Backup resource to be updated. The fields
            specified in the update_mask are relative to the resource,
            not the full request. A field will be overwritten if it is
            in the mask. If the user does not provide a mask then all
            fields will be overwritten.
        backup_vault (google.cloud.netapp_v1.types.BackupVault):
            Required. The backupVault being updated
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    backup_vault: "BackupVault" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="BackupVault",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
