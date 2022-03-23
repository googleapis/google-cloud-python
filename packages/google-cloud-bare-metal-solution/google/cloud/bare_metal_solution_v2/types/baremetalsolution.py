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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.baremetalsolution.v2",
    manifest={
        "Volume",
        "ListVolumesRequest",
        "ListVolumesResponse",
        "GetVolumeRequest",
        "Lun",
        "Network",
        "VRF",
        "ListNetworksRequest",
        "ListNetworksResponse",
        "GetNetworkRequest",
        "GetSnapshotSchedulePolicyRequest",
        "Instance",
        "ListInstancesRequest",
        "ListInstancesResponse",
        "GetInstanceRequest",
        "ResetInstanceRequest",
        "ResetInstanceResponse",
        "GetVolumeSnapshotRequest",
        "ListVolumeSnapshotsRequest",
        "ListVolumeSnapshotsResponse",
        "DeleteVolumeSnapshotRequest",
        "OperationMetadata",
        "VolumeSnapshot",
        "SnapshotSchedulePolicy",
        "ListSnapshotSchedulePoliciesRequest",
        "ListSnapshotSchedulePoliciesResponse",
        "CreateSnapshotSchedulePolicyRequest",
        "UpdateSnapshotSchedulePolicyRequest",
        "DeleteSnapshotSchedulePolicyRequest",
        "UpdateVolumeRequest",
        "GetLunRequest",
        "ListLunsRequest",
        "ListLunsResponse",
        "CreateVolumeSnapshotRequest",
        "RestoreVolumeSnapshotRequest",
    },
)


class Volume(proto.Message):
    r"""A storage volume.

    Attributes:
        name (str):
            Output only. The resource name of this ``Volume``. Resource
            names are schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. Format:
            ``projects/{project}/locations/{location}/volumes/{volume}``
        storage_type (google.cloud.bare_metal_solution_v2.types.Volume.StorageType):
            The storage type for this volume.
        state (google.cloud.bare_metal_solution_v2.types.Volume.State):
            The state of this storage volume.
        requested_size_gib (int):
            The requested size of this storage volume, in
            GiB.
        current_size_gib (int):
            The current size of this storage volume, in
            GiB, including space reserved for snapshots.
            This size might be different than the requested
            size if the storage volume has been configured
            with auto grow or auto shrink.
        auto_grown_size_gib (int):
            The size, in GiB, that this storage volume
            has expanded as a result of an auto grow policy.
            In the absence of auto-grow, the value is 0.
        remaining_space_gib (int):
            The space remaining in the storage volume for
            new LUNs, in GiB, excluding space reserved for
            snapshots.
        snapshot_reservation_detail (google.cloud.bare_metal_solution_v2.types.Volume.SnapshotReservationDetail):
            Details about snapshot space reservation and
            usage on the storage volume.
        snapshot_auto_delete_behavior (google.cloud.bare_metal_solution_v2.types.Volume.SnapshotAutoDeleteBehavior):
            The behavior to use when snapshot reserved
            space is full.
        snapshot_schedule_policy (str):
            The name of the snapshot schedule policy in
            use for this volume, if any.
    """

    class StorageType(proto.Enum):
        r"""The storage type for a volume."""
        STORAGE_TYPE_UNSPECIFIED = 0
        SSD = 1
        HDD = 2

    class State(proto.Enum):
        r"""The possible states for a storage volume."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        DELETING = 3

    class SnapshotAutoDeleteBehavior(proto.Enum):
        r"""The kinds of auto delete behavior to use when snapshot
        reserved space is full.
        """
        SNAPSHOT_AUTO_DELETE_BEHAVIOR_UNSPECIFIED = 0
        DISABLED = 1
        OLDEST_FIRST = 2
        NEWEST_FIRST = 3

    class SnapshotReservationDetail(proto.Message):
        r"""Details about snapshot space reservation and usage on the
        storage volume.

        Attributes:
            reserved_space_gib (int):
                The space on this storage volume reserved for
                snapshots, shown in GiB.
            reserved_space_used_percent (int):
                The percent of snapshot space on this storage
                volume actually being used by the snapshot
                copies. This value might be higher than 100% if
                the snapshot copies have overflowed into the
                data portion of the storage volume.
            reserved_space_remaining_gib (int):
                The amount, in GiB, of available space in
                this storage volume's reserved snapshot space.
        """

        reserved_space_gib = proto.Field(proto.INT64, number=1,)
        reserved_space_used_percent = proto.Field(proto.INT32, number=2,)
        reserved_space_remaining_gib = proto.Field(proto.INT64, number=3,)

    name = proto.Field(proto.STRING, number=1,)
    storage_type = proto.Field(proto.ENUM, number=2, enum=StorageType,)
    state = proto.Field(proto.ENUM, number=3, enum=State,)
    requested_size_gib = proto.Field(proto.INT64, number=4,)
    current_size_gib = proto.Field(proto.INT64, number=5,)
    auto_grown_size_gib = proto.Field(proto.INT64, number=6,)
    remaining_space_gib = proto.Field(proto.INT64, number=7,)
    snapshot_reservation_detail = proto.Field(
        proto.MESSAGE, number=8, message=SnapshotReservationDetail,
    )
    snapshot_auto_delete_behavior = proto.Field(
        proto.ENUM, number=9, enum=SnapshotAutoDeleteBehavior,
    )
    snapshot_schedule_policy = proto.Field(proto.STRING, number=10,)


class ListVolumesRequest(proto.Message):
    r"""Message for requesting a list of storage volumes.

    Attributes:
        parent (str):
            Required. Parent value for
            ListVolumesRequest.
        page_size (int):
            Requested page size. The server might return
            fewer items than requested. If unspecified,
            server will pick an appropriate default.
        page_token (str):
            A token identifying a page of results from
            the server.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListVolumesResponse(proto.Message):
    r"""Response message containing the list of storage volumes.

    Attributes:
        volumes (Sequence[google.cloud.bare_metal_solution_v2.types.Volume]):
            The list of storage volumes.
        next_page_token (str):
            A token identifying a page of results from
            the server.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    volumes = proto.RepeatedField(proto.MESSAGE, number=1, message="Volume",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetVolumeRequest(proto.Message):
    r"""Message for requesting storage volume information.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name = proto.Field(proto.STRING, number=1,)


class Lun(proto.Message):
    r"""A storage volume logical unit number (LUN).

    Attributes:
        name (str):
            Output only. The name of the LUN.
        state (google.cloud.bare_metal_solution_v2.types.Lun.State):
            The state of this storage volume.
        size_gb (int):
            The size of this LUN, in gigabytes.
        multiprotocol_type (google.cloud.bare_metal_solution_v2.types.Lun.MultiprotocolType):
            The LUN multiprotocol type ensures the
            characteristics of the LUN are optimized for
            each operating system.
        storage_volume (str):
            Display the storage volume for this LUN.
        shareable (bool):
            Display if this LUN can be shared between
            multiple physical servers.
        boot_lun (bool):
            Display if this LUN is a boot LUN.
        storage_type (google.cloud.bare_metal_solution_v2.types.Lun.StorageType):
            The storage type for this LUN.
        wwid (str):
            The WWID for this LUN.
    """

    class State(proto.Enum):
        r"""The possible states for the LUN."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        UPDATING = 2
        READY = 3
        DELETING = 4

    class MultiprotocolType(proto.Enum):
        r"""Display the operating systems present for the LUN
        multiprotocol type.
        """
        MULTIPROTOCOL_TYPE_UNSPECIFIED = 0
        LINUX = 1

    class StorageType(proto.Enum):
        r"""The storage types for a LUN."""
        STORAGE_TYPE_UNSPECIFIED = 0
        SSD = 1
        HDD = 2

    name = proto.Field(proto.STRING, number=1,)
    state = proto.Field(proto.ENUM, number=2, enum=State,)
    size_gb = proto.Field(proto.INT64, number=3,)
    multiprotocol_type = proto.Field(proto.ENUM, number=4, enum=MultiprotocolType,)
    storage_volume = proto.Field(proto.STRING, number=5,)
    shareable = proto.Field(proto.BOOL, number=6,)
    boot_lun = proto.Field(proto.BOOL, number=7,)
    storage_type = proto.Field(proto.ENUM, number=8, enum=StorageType,)
    wwid = proto.Field(proto.STRING, number=9,)


class Network(proto.Message):
    r"""A Network.

    Attributes:
        name (str):
            Output only. The resource name of this ``Network``. Resource
            names are schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. Format:
            ``projects/{project}/locations/{location}/networks/{network}``
            This field will contain the same value as field "network",
            which will soon be deprecated. Please use this field to
            reference the name of the network resource.
        network (str):
            Name of the network.
        type_ (google.cloud.bare_metal_solution_v2.types.Network.Type):
            The type of this network.
        ip_address (str):
            IP address configured.
        mac_address (Sequence[str]):
            List of physical interfaces.
        state (google.cloud.bare_metal_solution_v2.types.Network.State):
            The Network state.
        vlan_id (str):
            The vlan id of the Network.
        cidr (str):
            The cidr of the Network.
        vrf (google.cloud.bare_metal_solution_v2.types.VRF):
            The vrf for the Network.
    """

    class Type(proto.Enum):
        r"""Network type."""
        TYPE_UNSPECIFIED = 0
        CLIENT = 1
        PRIVATE = 2

    class State(proto.Enum):
        r"""The possible states for this Network."""
        STATE_UNSPECIFIED = 0
        PROVISIONING = 1
        PROVISIONED = 2

    name = proto.Field(proto.STRING, number=5,)
    network = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.ENUM, number=2, enum=Type,)
    ip_address = proto.Field(proto.STRING, number=3,)
    mac_address = proto.RepeatedField(proto.STRING, number=4,)
    state = proto.Field(proto.ENUM, number=6, enum=State,)
    vlan_id = proto.Field(proto.STRING, number=7,)
    cidr = proto.Field(proto.STRING, number=8,)
    vrf = proto.Field(proto.MESSAGE, number=9, message="VRF",)


class VRF(proto.Message):
    r"""A network VRF.

    Attributes:
        name (str):
            The name of the VRF.
        state (google.cloud.bare_metal_solution_v2.types.VRF.State):
            The possible state of VRF.
        qos_policy (google.cloud.bare_metal_solution_v2.types.VRF.QosPolicy):
            The QOS policy applied to this VRF.
        vlan_attachments (Sequence[google.cloud.bare_metal_solution_v2.types.VRF.VlanAttachment]):
            The list of VLAN attachments for the VRF.
    """

    class State(proto.Enum):
        r"""The possible states for this VRF."""
        STATE_UNSPECIFIED = 0
        PROVISIONING = 1
        PROVISIONED = 2

    class QosPolicy(proto.Message):
        r"""QOS policy parameters.

        Attributes:
            bandwidth_gbps (float):
                The bandwidth permitted by the QOS policy, in
                gbps.
        """

        bandwidth_gbps = proto.Field(proto.DOUBLE, number=1,)

    class VlanAttachment(proto.Message):
        r"""VLAN attachment details.

        Attributes:
            peer_vlan_id (int):
                The peer vlan ID of the attachment.
            peer_ip (str):
                The peer IP of the attachment.
            router_ip (str):
                The router IP of the attachment.
        """

        peer_vlan_id = proto.Field(proto.INT64, number=1,)
        peer_ip = proto.Field(proto.STRING, number=2,)
        router_ip = proto.Field(proto.STRING, number=3,)

    name = proto.Field(proto.STRING, number=1,)
    state = proto.Field(proto.ENUM, number=5, enum=State,)
    qos_policy = proto.Field(proto.MESSAGE, number=6, message=QosPolicy,)
    vlan_attachments = proto.RepeatedField(
        proto.MESSAGE, number=7, message=VlanAttachment,
    )


class ListNetworksRequest(proto.Message):
    r"""Message for requesting a list of networks.

    Attributes:
        parent (str):
            Required. Parent value for
            ListNetworksRequest.
        page_size (int):
            Requested page size. The server might return
            fewer items than requested. If unspecified,
            server will pick an appropriate default.
        page_token (str):
            A token identifying a page of results from
            the server.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListNetworksResponse(proto.Message):
    r"""Response message containing the list of networks.

    Attributes:
        networks (Sequence[google.cloud.bare_metal_solution_v2.types.Network]):
            The list of networks.
        next_page_token (str):
            A token identifying a page of results from
            the server.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    networks = proto.RepeatedField(proto.MESSAGE, number=1, message="Network",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetNetworkRequest(proto.Message):
    r"""Message for requesting network information.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name = proto.Field(proto.STRING, number=1,)


class GetSnapshotSchedulePolicyRequest(proto.Message):
    r"""Message for requesting snapshot schedule policy information.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name = proto.Field(proto.STRING, number=1,)


class Instance(proto.Message):
    r"""A server.

    Attributes:
        name (str):
            Output only. The resource name of this ``Instance``.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. Format:
            ``projects/{project}/locations/{location}/instances/{instance}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Create a time stamp.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Update a time stamp.
        machine_type (str):
            The server type. `Available server
            types <https://cloud.google.com/bare-metal/docs/bms-planning#server_configurations>`__
        state (google.cloud.bare_metal_solution_v2.types.Instance.State):
            The state of the server.
        hyperthreading_enabled (bool):
            True if you enable hyperthreading for the
            server, otherwise false. The default value is
            false.
        labels (Sequence[google.cloud.bare_metal_solution_v2.types.Instance.LabelsEntry]):
            Labels as key value pairs.
        luns (Sequence[google.cloud.bare_metal_solution_v2.types.Lun]):
            List of LUNs associated with this server.
        networks (Sequence[google.cloud.bare_metal_solution_v2.types.Network]):
            List of networks associated with this server.
        interactive_serial_console_enabled (bool):
            True if the interactive serial console
            feature is enabled for the instance, false
            otherwise. The default value is false.
    """

    class State(proto.Enum):
        r"""The possible states for this server."""
        STATE_UNSPECIFIED = 0
        PROVISIONING = 1
        RUNNING = 2
        DELETED = 3

    name = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    machine_type = proto.Field(proto.STRING, number=4,)
    state = proto.Field(proto.ENUM, number=5, enum=State,)
    hyperthreading_enabled = proto.Field(proto.BOOL, number=6,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=7,)
    luns = proto.RepeatedField(proto.MESSAGE, number=8, message="Lun",)
    networks = proto.RepeatedField(proto.MESSAGE, number=9, message="Network",)
    interactive_serial_console_enabled = proto.Field(proto.BOOL, number=10,)


class ListInstancesRequest(proto.Message):
    r"""Message for requesting the list of servers.

    Attributes:
        parent (str):
            Required. Parent value for
            ListInstancesRequest.
        page_size (int):
            Requested page size. Server may return fewer
            items than requested. If unspecified, the server
            will pick an appropriate default.
        page_token (str):
            A token identifying a page of results from
            the server.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListInstancesResponse(proto.Message):
    r"""Response message for the list of servers.

    Attributes:
        instances (Sequence[google.cloud.bare_metal_solution_v2.types.Instance]):
            The list of servers.
        next_page_token (str):
            A token identifying a page of results from
            the server.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    instances = proto.RepeatedField(proto.MESSAGE, number=1, message="Instance",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetInstanceRequest(proto.Message):
    r"""Message for requesting server information.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name = proto.Field(proto.STRING, number=1,)


class ResetInstanceRequest(proto.Message):
    r"""Message requesting to reset a server.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name = proto.Field(proto.STRING, number=1,)


class ResetInstanceResponse(proto.Message):
    r"""Response message from resetting a server.
    """


class GetVolumeSnapshotRequest(proto.Message):
    r"""Message for requesting storage volume snapshot information.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListVolumeSnapshotsRequest(proto.Message):
    r"""Message for requesting a list of storage volume snapshots.

    Attributes:
        parent (str):
            Required. Parent value for
            ListVolumesRequest.
        page_size (int):
            Requested page size. The server might return
            fewer items than requested. If unspecified,
            server will pick an appropriate default.
        page_token (str):
            A token identifying a page of results from
            the server.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListVolumeSnapshotsResponse(proto.Message):
    r"""Response message containing the list of storage volume
    snapshots.

    Attributes:
        volume_snapshots (Sequence[google.cloud.bare_metal_solution_v2.types.VolumeSnapshot]):
            The list of storage volumes.
        next_page_token (str):
            A token identifying a page of results from
            the server.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    volume_snapshots = proto.RepeatedField(
        proto.MESSAGE, number=1, message="VolumeSnapshot",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class DeleteVolumeSnapshotRequest(proto.Message):
    r"""Message for deleting named Volume snapshot.

    Attributes:
        name (str):
            Required. The name of the snapshot to delete.
    """

    name = proto.Field(proto.STRING, number=1,)


class OperationMetadata(proto.Message):
    r"""Represents the metadata from a long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation was created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation finished running.
        target (str):
            Server-defined resource path for the target
            of the operation.
        verb (str):
            Name of the action executed by the operation.
        status_message (str):
            Human-readable status of the operation, if
            any.
        requested_cancellation (bool):
            Identifies whether the user requested the cancellation of
            the operation. Operations that have been successfully
            cancelled have [Operation.error][] value with a
            [google.rpc.Status.code][] of 1, corresponding to
            ``Code.CANCELLED``.
        api_version (str):
            API version used with the operation.
    """

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    target = proto.Field(proto.STRING, number=3,)
    verb = proto.Field(proto.STRING, number=4,)
    status_message = proto.Field(proto.STRING, number=5,)
    requested_cancellation = proto.Field(proto.BOOL, number=6,)
    api_version = proto.Field(proto.STRING, number=7,)


class VolumeSnapshot(proto.Message):
    r"""Snapshot registered for a given storage volume.

    Attributes:
        name (str):
            Output only. The name of the storage volume
            snapshot.
        description (str):
            The description of the storage volume
            snapshot.
        size_bytes (int):
            The size of the storage volume snapshot, in
            bytes.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. The creation time of the storage
            volume snapshot.
        storage_volume (str):
            The storage volume this snapshot belongs to.
    """

    name = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    size_bytes = proto.Field(proto.INT64, number=3,)
    create_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    storage_volume = proto.Field(proto.STRING, number=5,)


class SnapshotSchedulePolicy(proto.Message):
    r"""A snapshot schedule policy.

    Attributes:
        name (str):
            Output only. The name of the snapshot
            schedule policy.
        description (str):
            The description of the snapshot schedule
            policy.
        schedules (Sequence[google.cloud.bare_metal_solution_v2.types.SnapshotSchedulePolicy.Schedule]):
            The snapshot schedules contained in this
            policy. You can specify a maximum  of 5
            schedules.
    """

    class Schedule(proto.Message):
        r"""A snapshot schedule.

        Attributes:
            crontab_spec (str):
                A crontab-like specification that the
                schedule uses to take snapshots.
            retention_count (int):
                The maximum number of snapshots to retain in
                this schedule.
            prefix (str):
                A list of snapshot names created in this
                schedule.
        """

        crontab_spec = proto.Field(proto.STRING, number=1,)
        retention_count = proto.Field(proto.INT32, number=2,)
        prefix = proto.Field(proto.STRING, number=3,)

    name = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    schedules = proto.RepeatedField(proto.MESSAGE, number=3, message=Schedule,)


class ListSnapshotSchedulePoliciesRequest(proto.Message):
    r"""Message for requesting a list of snapshot schedule policies.

    Attributes:
        parent (str):
            Required. The parent project containing the
            Snapshot Schedule Policies.
        page_size (int):
            The maximum number of items to return.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListSnapshotSchedulePoliciesResponse(proto.Message):
    r"""Response message containing the list of snapshot schedule
    policies.

    Attributes:
        snapshot_schedule_policies (Sequence[google.cloud.bare_metal_solution_v2.types.SnapshotSchedulePolicy]):
            The snapshot schedule policies registered in
            this project.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    snapshot_schedule_policies = proto.RepeatedField(
        proto.MESSAGE, number=1, message="SnapshotSchedulePolicy",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class CreateSnapshotSchedulePolicyRequest(proto.Message):
    r"""Message for creating a snapshot schedule policy in a project.

    Attributes:
        parent (str):
            Required. The parent project and location
            containing the SnapshotSchedulePolicy.
        snapshot_schedule_policy (google.cloud.bare_metal_solution_v2.types.SnapshotSchedulePolicy):
            Required. The SnapshotSchedulePolicy to
            create.
        snapshot_schedule_policy_id (str):
            Required. Snapshot policy ID
    """

    parent = proto.Field(proto.STRING, number=1,)
    snapshot_schedule_policy = proto.Field(
        proto.MESSAGE, number=2, message="SnapshotSchedulePolicy",
    )
    snapshot_schedule_policy_id = proto.Field(proto.STRING, number=3,)


class UpdateSnapshotSchedulePolicyRequest(proto.Message):
    r"""Message for updating a snapshot schedule policy in a project.

    Attributes:
        snapshot_schedule_policy (google.cloud.bare_metal_solution_v2.types.SnapshotSchedulePolicy):
            Required. The snapshot schedule policy to update.

            The ``name`` field is used to identify the snapshot schedule
            policy to update. Format:
            projects/{project}/locations/global/snapshotSchedulePolicies/{policy}
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to update.
    """

    snapshot_schedule_policy = proto.Field(
        proto.MESSAGE, number=1, message="SnapshotSchedulePolicy",
    )
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteSnapshotSchedulePolicyRequest(proto.Message):
    r"""Message for deleting a snapshot schedule policy in a project.

    Attributes:
        name (str):
            Required. The name of the snapshot schedule
            policy to delete.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateVolumeRequest(proto.Message):
    r"""Message for updating a volume.

    Attributes:
        volume (google.cloud.bare_metal_solution_v2.types.Volume):
            Required. The volume to update.

            The ``name`` field is used to identify the volume to update.
            Format:
            projects/{project}/locations/{location}/volumes/{volume}
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to update. The only currently supported
            fields are: ``snapshot_auto_delete_behavior``
            ``snapshot_schedule_policy_name``
    """

    volume = proto.Field(proto.MESSAGE, number=1, message="Volume",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class GetLunRequest(proto.Message):
    r"""Message for requesting storage lun information.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListLunsRequest(proto.Message):
    r"""Message for requesting a list of storage volume luns.

    Attributes:
        parent (str):
            Required. Parent value for ListLunsRequest.
        page_size (int):
            Requested page size. The server might return
            fewer items than requested. If unspecified,
            server will pick an appropriate default.
        page_token (str):
            A token identifying a page of results from
            the server.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListLunsResponse(proto.Message):
    r"""Response message containing the list of storage volume luns.

    Attributes:
        luns (Sequence[google.cloud.bare_metal_solution_v2.types.Lun]):
            The list of luns.
        next_page_token (str):
            A token identifying a page of results from
            the server.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    luns = proto.RepeatedField(proto.MESSAGE, number=1, message="Lun",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class CreateVolumeSnapshotRequest(proto.Message):
    r"""Message for creating a volume snapshot.

    Attributes:
        parent (str):
            Required. The volume to snapshot.
        volume_snapshot (google.cloud.bare_metal_solution_v2.types.VolumeSnapshot):
            Required. The volume snapshot to create. Only
            the description field may be specified.
    """

    parent = proto.Field(proto.STRING, number=1,)
    volume_snapshot = proto.Field(proto.MESSAGE, number=2, message="VolumeSnapshot",)


class RestoreVolumeSnapshotRequest(proto.Message):
    r"""Message for restoring a volume snapshot.

    Attributes:
        volume_snapshot (str):
            Required. Name of the resource.
    """

    volume_snapshot = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
