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

from google.cloud.netapp_v1.types import common

__protobuf__ = proto.module(
    package="google.cloud.netapp.v1",
    manifest={
        "GetStoragePoolRequest",
        "ListStoragePoolsRequest",
        "ListStoragePoolsResponse",
        "CreateStoragePoolRequest",
        "UpdateStoragePoolRequest",
        "DeleteStoragePoolRequest",
        "StoragePool",
    },
)


class GetStoragePoolRequest(proto.Message):
    r"""GetStoragePoolRequest gets a Storage Pool.

    Attributes:
        name (str):
            Required. Name of the storage pool
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListStoragePoolsRequest(proto.Message):
    r"""ListStoragePoolsRequest lists Storage Pools.

    Attributes:
        parent (str):
            Required. Parent value
        page_size (int):
            Optional. The maximum number of items to
            return.
        page_token (str):
            Optional. The next_page_token value to use if there are
            additional results to retrieve for this list request.
        order_by (str):
            Optional. Sort results. Supported values are
            "name", "name desc" or "" (unsorted).
        filter (str):
            Optional. List filter.
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


class ListStoragePoolsResponse(proto.Message):
    r"""ListStoragePoolsResponse is the response to a
    ListStoragePoolsRequest.

    Attributes:
        storage_pools (MutableSequence[google.cloud.netapp_v1.types.StoragePool]):
            The list of StoragePools
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    storage_pools: MutableSequence["StoragePool"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="StoragePool",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class CreateStoragePoolRequest(proto.Message):
    r"""CreateStoragePoolRequest creates a Storage Pool.

    Attributes:
        parent (str):
            Required. Value for parent.
        storage_pool_id (str):
            Required. Id of the requesting storage pool If
            auto-generating Id server-side, remove this field and id
            from the method_signature of Create RPC
        storage_pool (google.cloud.netapp_v1.types.StoragePool):
            Required. The required parameters to create a
            new storage pool.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    storage_pool_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    storage_pool: "StoragePool" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="StoragePool",
    )


class UpdateStoragePoolRequest(proto.Message):
    r"""UpdateStoragePoolRequest updates a Storage Pool.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the StoragePool resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If the user does not provide a mask
            then all fields will be overwritten.
        storage_pool (google.cloud.netapp_v1.types.StoragePool):
            Required. The pool being updated
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    storage_pool: "StoragePool" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="StoragePool",
    )


class DeleteStoragePoolRequest(proto.Message):
    r"""DeleteStoragePoolRequest deletes a Storage Pool.

    Attributes:
        name (str):
            Required. Name of the storage pool
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class StoragePool(proto.Message):
    r"""StoragePool is a container for volumes with a service level
    and capacity. Volumes can be created in a pool of sufficient
    available capacity. StoragePool capacity is what you are billed
    for.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Identifier. Name of the storage pool
        service_level (google.cloud.netapp_v1.types.ServiceLevel):
            Required. Service level of the storage pool
        capacity_gib (int):
            Required. Capacity in GIB of the pool
        volume_capacity_gib (int):
            Output only. Allocated size of all volumes in
            GIB in the storage pool
        volume_count (int):
            Output only. Volume count of the storage pool
        state (google.cloud.netapp_v1.types.StoragePool.State):
            Output only. State of the storage pool
        state_details (str):
            Output only. State details of the storage
            pool
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Create time of the storage pool
        description (str):
            Optional. Description of the storage pool
        labels (MutableMapping[str, str]):
            Optional. Labels as key value pairs
        network (str):
            Required. VPC Network name.
            Format:
            projects/{project}/global/networks/{network}
        active_directory (str):
            Optional. Specifies the Active Directory to
            be used for creating a SMB volume.
        kms_config (str):
            Optional. Specifies the KMS config to be used
            for volume encryption.
        ldap_enabled (bool):
            Optional. Flag indicating if the pool is NFS
            LDAP enabled or not.
        psa_range (str):
            Optional. This field is not implemented. The
            values provided in this field are ignored.
        encryption_type (google.cloud.netapp_v1.types.EncryptionType):
            Output only. Specifies the current pool
            encryption key source.
        global_access_allowed (bool):
            Deprecated. Used to allow SO pool to access
            AD or DNS server from other regions.

            This field is a member of `oneof`_ ``_global_access_allowed``.
    """

    class State(proto.Enum):
        r"""The Storage Pool States

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified Storage Pool State
            READY (1):
                Storage Pool State is Ready
            CREATING (2):
                Storage Pool State is Creating
            DELETING (3):
                Storage Pool State is Deleting
            UPDATING (4):
                Storage Pool State is Updating
            RESTORING (5):
                Storage Pool State is Restoring
            DISABLED (6):
                Storage Pool State is Disabled
            ERROR (7):
                Storage Pool State is Error
        """
        STATE_UNSPECIFIED = 0
        READY = 1
        CREATING = 2
        DELETING = 3
        UPDATING = 4
        RESTORING = 5
        DISABLED = 6
        ERROR = 7

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    service_level: common.ServiceLevel = proto.Field(
        proto.ENUM,
        number=2,
        enum=common.ServiceLevel,
    )
    capacity_gib: int = proto.Field(
        proto.INT64,
        number=3,
    )
    volume_capacity_gib: int = proto.Field(
        proto.INT64,
        number=4,
    )
    volume_count: int = proto.Field(
        proto.INT32,
        number=5,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=6,
        enum=State,
    )
    state_details: str = proto.Field(
        proto.STRING,
        number=7,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    description: str = proto.Field(
        proto.STRING,
        number=9,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=10,
    )
    network: str = proto.Field(
        proto.STRING,
        number=11,
    )
    active_directory: str = proto.Field(
        proto.STRING,
        number=12,
    )
    kms_config: str = proto.Field(
        proto.STRING,
        number=13,
    )
    ldap_enabled: bool = proto.Field(
        proto.BOOL,
        number=14,
    )
    psa_range: str = proto.Field(
        proto.STRING,
        number=15,
    )
    encryption_type: common.EncryptionType = proto.Field(
        proto.ENUM,
        number=16,
        enum=common.EncryptionType,
    )
    global_access_allowed: bool = proto.Field(
        proto.BOOL,
        number=17,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
