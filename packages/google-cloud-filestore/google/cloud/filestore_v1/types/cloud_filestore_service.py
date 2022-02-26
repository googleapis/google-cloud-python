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
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.filestore.v1",
    manifest={
        "NetworkConfig",
        "FileShareConfig",
        "NfsExportOptions",
        "Instance",
        "CreateInstanceRequest",
        "GetInstanceRequest",
        "UpdateInstanceRequest",
        "RestoreInstanceRequest",
        "DeleteInstanceRequest",
        "ListInstancesRequest",
        "ListInstancesResponse",
        "Backup",
        "CreateBackupRequest",
        "DeleteBackupRequest",
        "UpdateBackupRequest",
        "GetBackupRequest",
        "ListBackupsRequest",
        "ListBackupsResponse",
    },
)


class NetworkConfig(proto.Message):
    r"""Network configuration for the instance.

    Attributes:
        network (str):
            The name of the Google Compute Engine `VPC
            network <https://cloud.google.com/vpc/docs/vpc>`__ to which
            the instance is connected.
        modes (Sequence[google.cloud.filestore_v1.types.NetworkConfig.AddressMode]):
            Internet protocol versions for which the instance has IP
            addresses assigned. For this version, only MODE_IPV4 is
            supported.
        reserved_ip_range (str):
            A /29 CIDR block in one of the `internal IP address
            ranges <https://www.arin.net/reference/research/statistics/address_filters/>`__
            that identifies the range of IP addresses reserved for this
            instance. For example, 10.0.0.0/29 or 192.168.0.0/29. The
            range you specify can't overlap with either existing subnets
            or assigned IP address ranges for other Cloud Filestore
            instances in the selected VPC network.
        ip_addresses (Sequence[str]):
            Output only. IPv4 addresses in the format IPv4 addresses in
            the format ``{octet1}.{octet2}.{octet3}.{octet4}`` or IPv6
            addresses in the format
            ``{block1}:{block2}:{block3}:{block4}:{block5}:{block6}:{block7}:{block8}``.
    """

    class AddressMode(proto.Enum):
        r"""Internet protocol versions supported by Cloud Filestore."""
        ADDRESS_MODE_UNSPECIFIED = 0
        MODE_IPV4 = 1

    network = proto.Field(proto.STRING, number=1,)
    modes = proto.RepeatedField(proto.ENUM, number=3, enum=AddressMode,)
    reserved_ip_range = proto.Field(proto.STRING, number=4,)
    ip_addresses = proto.RepeatedField(proto.STRING, number=5,)


class FileShareConfig(proto.Message):
    r"""File share configuration for the instance.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            The name of the file share (must be 16
            characters or less).
        capacity_gb (int):
            File share capacity in gigabytes (GB).
            Cloud Filestore defines 1 GB as 1024^3 bytes.
        source_backup (str):
            The resource name of the backup, in the format
            ``projects/{project_number}/locations/{location_id}/backups/{backup_id}``,
            that this file share has been restored from.

            This field is a member of `oneof`_ ``source``.
        nfs_export_options (Sequence[google.cloud.filestore_v1.types.NfsExportOptions]):
            Nfs Export Options.
            There is a limit of 10 export options per file
            share.
    """

    name = proto.Field(proto.STRING, number=1,)
    capacity_gb = proto.Field(proto.INT64, number=2,)
    source_backup = proto.Field(proto.STRING, number=8, oneof="source",)
    nfs_export_options = proto.RepeatedField(
        proto.MESSAGE, number=7, message="NfsExportOptions",
    )


class NfsExportOptions(proto.Message):
    r"""NFS export options specifications.

    Attributes:
        ip_ranges (Sequence[str]):
            List of either an IPv4 addresses in the format
            ``{octet1}.{octet2}.{octet3}.{octet4}`` or CIDR ranges in
            the format
            ``{octet1}.{octet2}.{octet3}.{octet4}/{mask size}`` which
            may mount the file share. Overlapping IP ranges are not
            allowed, both within and across NfsExportOptions. An error
            will be returned. The limit is 64 IP ranges/addresses for
            each FileShareConfig among all NfsExportOptions.
        access_mode (google.cloud.filestore_v1.types.NfsExportOptions.AccessMode):
            Either READ_ONLY, for allowing only read requests on the
            exported directory, or READ_WRITE, for allowing both read
            and write requests. The default is READ_WRITE.
        squash_mode (google.cloud.filestore_v1.types.NfsExportOptions.SquashMode):
            Either NO_ROOT_SQUASH, for allowing root access on the
            exported directory, or ROOT_SQUASH, for not allowing root
            access. The default is NO_ROOT_SQUASH.
        anon_uid (int):
            An integer representing the anonymous user id with a default
            value of 65534. Anon_uid may only be set with squash_mode of
            ROOT_SQUASH. An error will be returned if this field is
            specified for other squash_mode settings.
        anon_gid (int):
            An integer representing the anonymous group id with a
            default value of 65534. Anon_gid may only be set with
            squash_mode of ROOT_SQUASH. An error will be returned if
            this field is specified for other squash_mode settings.
    """

    class AccessMode(proto.Enum):
        r"""The access mode."""
        ACCESS_MODE_UNSPECIFIED = 0
        READ_ONLY = 1
        READ_WRITE = 2

    class SquashMode(proto.Enum):
        r"""The squash mode."""
        SQUASH_MODE_UNSPECIFIED = 0
        NO_ROOT_SQUASH = 1
        ROOT_SQUASH = 2

    ip_ranges = proto.RepeatedField(proto.STRING, number=1,)
    access_mode = proto.Field(proto.ENUM, number=2, enum=AccessMode,)
    squash_mode = proto.Field(proto.ENUM, number=3, enum=SquashMode,)
    anon_uid = proto.Field(proto.INT64, number=4,)
    anon_gid = proto.Field(proto.INT64, number=5,)


class Instance(proto.Message):
    r"""A Cloud Filestore instance.

    Attributes:
        name (str):
            Output only. The resource name of the instance, in the
            format
            ``projects/{project}/locations/{location}/instances/{instance}``.
        description (str):
            The description of the instance (2048
            characters or less).
        state (google.cloud.filestore_v1.types.Instance.State):
            Output only. The instance state.
        status_message (str):
            Output only. Additional information about the
            instance state, if available.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the instance was
            created.
        tier (google.cloud.filestore_v1.types.Instance.Tier):
            The service tier of the instance.
        labels (Sequence[google.cloud.filestore_v1.types.Instance.LabelsEntry]):
            Resource labels to represent user provided
            metadata.
        file_shares (Sequence[google.cloud.filestore_v1.types.FileShareConfig]):
            File system shares on the instance.
            For this version, only a single file share is
            supported.
        networks (Sequence[google.cloud.filestore_v1.types.NetworkConfig]):
            VPC networks to which the instance is
            connected. For this version, only a single
            network is supported.
        etag (str):
            Server-specified ETag for the instance
            resource to prevent simultaneous updates from
            overwriting each other.
        satisfies_pzs (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Reserved for future use.
    """

    class State(proto.Enum):
        r"""The instance state."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        REPAIRING = 3
        DELETING = 4
        ERROR = 6
        RESTORING = 7

    class Tier(proto.Enum):
        r"""Available service tiers."""
        TIER_UNSPECIFIED = 0
        STANDARD = 1
        PREMIUM = 2
        BASIC_HDD = 3
        BASIC_SSD = 4
        HIGH_SCALE_SSD = 5

    name = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    state = proto.Field(proto.ENUM, number=5, enum=State,)
    status_message = proto.Field(proto.STRING, number=6,)
    create_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    tier = proto.Field(proto.ENUM, number=8, enum=Tier,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=9,)
    file_shares = proto.RepeatedField(
        proto.MESSAGE, number=10, message="FileShareConfig",
    )
    networks = proto.RepeatedField(proto.MESSAGE, number=11, message="NetworkConfig",)
    etag = proto.Field(proto.STRING, number=12,)
    satisfies_pzs = proto.Field(
        proto.MESSAGE, number=13, message=wrappers_pb2.BoolValue,
    )


class CreateInstanceRequest(proto.Message):
    r"""CreateInstanceRequest creates an instance.

    Attributes:
        parent (str):
            Required. The instance's project and location, in the format
            ``projects/{project_id}/locations/{location}``. In Cloud
            Filestore, locations map to GCP zones, for example
            **us-west1-b**.
        instance_id (str):
            Required. The name of the instance to create.
            The name must be unique for the specified
            project and location.
        instance (google.cloud.filestore_v1.types.Instance):
            Required. An [instance
            resource][google.cloud.filestore.v1.Instance]
    """

    parent = proto.Field(proto.STRING, number=1,)
    instance_id = proto.Field(proto.STRING, number=2,)
    instance = proto.Field(proto.MESSAGE, number=3, message="Instance",)


class GetInstanceRequest(proto.Message):
    r"""GetInstanceRequest gets the state of an instance.

    Attributes:
        name (str):
            Required. The instance resource name, in the format
            ``projects/{project_id}/locations/{location}/instances/{instance_id}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateInstanceRequest(proto.Message):
    r"""UpdateInstanceRequest updates the settings of an instance.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Mask of fields to update. At least one path must be supplied
            in this field. The elements of the repeated paths field may
            only include these fields:

            -  "description"
            -  "file_shares"
            -  "labels".
        instance (google.cloud.filestore_v1.types.Instance):
            Only fields specified in update_mask are updated.
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    instance = proto.Field(proto.MESSAGE, number=2, message="Instance",)


class RestoreInstanceRequest(proto.Message):
    r"""RestoreInstanceRequest restores an existing instances's file
    share from a backup.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. The resource name of the instance, in the format
            ``projects/{project_number}/locations/{location_id}/instances/{instance_id}``.
        file_share (str):
            Required. Name of the file share in the Cloud
            Filestore instance that the backup is being
            restored to.
        source_backup (str):
            The resource name of the backup, in the format
            ``projects/{project_number}/locations/{location_id}/backups/{backup_id}``.

            This field is a member of `oneof`_ ``source``.
    """

    name = proto.Field(proto.STRING, number=1,)
    file_share = proto.Field(proto.STRING, number=2,)
    source_backup = proto.Field(proto.STRING, number=3, oneof="source",)


class DeleteInstanceRequest(proto.Message):
    r"""DeleteInstanceRequest deletes an instance.

    Attributes:
        name (str):
            Required. The instance resource name, in the format
            ``projects/{project_id}/locations/{location}/instances/{instance_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class ListInstancesRequest(proto.Message):
    r"""ListInstancesRequest lists instances.

    Attributes:
        parent (str):
            Required. The project and location for which to retrieve
            instance information, in the format
            ``projects/{project_id}/locations/{location}``. In Cloud
            Filestore, locations map to GCP zones, for example
            **us-west1-b**. To retrieve instance information for all
            locations, use "-" for the ``{location}`` value.
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

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    order_by = proto.Field(proto.STRING, number=4,)
    filter = proto.Field(proto.STRING, number=5,)


class ListInstancesResponse(proto.Message):
    r"""ListInstancesResponse is the result of ListInstancesRequest.

    Attributes:
        instances (Sequence[google.cloud.filestore_v1.types.Instance]):
            A list of instances in the project for the specified
            location.

            If the ``{location}`` value in the request is "-", the
            response contains a list of instances from all locations. If
            any location is unreachable, the response will only return
            instances in reachable locations and the "unreachable" field
            will be populated with a list of unreachable locations.
        next_page_token (str):
            The token you can use to retrieve the next
            page of results. Not returned if there are no
            more results in the list.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    instances = proto.RepeatedField(proto.MESSAGE, number=1, message="Instance",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class Backup(proto.Message):
    r"""A Cloud Filestore backup.

    Attributes:
        name (str):
            Output only. The resource name of the backup, in the format
            ``projects/{project_number}/locations/{location_id}/backups/{backup_id}``.
        description (str):
            A description of the backup with 2048
            characters or less. Requests with longer
            descriptions will be rejected.
        state (google.cloud.filestore_v1.types.Backup.State):
            Output only. The backup state.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the backup was
            created.
        labels (Sequence[google.cloud.filestore_v1.types.Backup.LabelsEntry]):
            Resource labels to represent user provided
            metadata.
        capacity_gb (int):
            Output only. Capacity of the source file
            share when the backup was created.
        storage_bytes (int):
            Output only. The size of the storage used by
            the backup. As backups share storage, this
            number is expected to change with backup
            creation/deletion.
        source_instance (str):
            The resource name of the source Cloud Filestore instance, in
            the format
            ``projects/{project_number}/locations/{location_id}/instances/{instance_id}``,
            used to create this backup.
        source_file_share (str):
            Name of the file share in the source Cloud
            Filestore instance that the backup is created
            from.
        source_instance_tier (google.cloud.filestore_v1.types.Instance.Tier):
            Output only. The service tier of the source
            Cloud Filestore instance that this backup is
            created from.
        download_bytes (int):
            Output only. Amount of bytes that will be
            downloaded if the backup is restored. This may
            be different than storage bytes, since
            sequential backups of the same disk will share
            storage.
        satisfies_pzs (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Reserved for future use.
    """

    class State(proto.Enum):
        r"""The backup state."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        FINALIZING = 2
        READY = 3
        DELETING = 4

    name = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    state = proto.Field(proto.ENUM, number=3, enum=State,)
    create_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=5,)
    capacity_gb = proto.Field(proto.INT64, number=6,)
    storage_bytes = proto.Field(proto.INT64, number=7,)
    source_instance = proto.Field(proto.STRING, number=8,)
    source_file_share = proto.Field(proto.STRING, number=9,)
    source_instance_tier = proto.Field(proto.ENUM, number=10, enum="Instance.Tier",)
    download_bytes = proto.Field(proto.INT64, number=11,)
    satisfies_pzs = proto.Field(
        proto.MESSAGE, number=12, message=wrappers_pb2.BoolValue,
    )


class CreateBackupRequest(proto.Message):
    r"""CreateBackupRequest creates a backup.

    Attributes:
        parent (str):
            Required. The backup's project and location, in the format
            ``projects/{project_number}/locations/{location}``. In Cloud
            Filestore, backup locations map to GCP regions, for example
            **us-west1**.
        backup (google.cloud.filestore_v1.types.Backup):
            Required. A [backup
            resource][google.cloud.filestore.v1.Backup]
        backup_id (str):
            Required. The ID to use for the backup. The ID must be
            unique within the specified project and location.

            This value must start with a lowercase letter followed by up
            to 62 lowercase letters, numbers, or hyphens, and cannot end
            with a hyphen. Values that do not match this pattern will
            trigger an INVALID_ARGUMENT error.
    """

    parent = proto.Field(proto.STRING, number=1,)
    backup = proto.Field(proto.MESSAGE, number=2, message="Backup",)
    backup_id = proto.Field(proto.STRING, number=3,)


class DeleteBackupRequest(proto.Message):
    r"""DeleteBackupRequest deletes a backup.

    Attributes:
        name (str):
            Required. The backup resource name, in the format
            ``projects/{project_number}/locations/{location}/backups/{backup_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateBackupRequest(proto.Message):
    r"""UpdateBackupRequest updates description and/or labels for a
    backup.

    Attributes:
        backup (google.cloud.filestore_v1.types.Backup):
            Required. A [backup
            resource][google.cloud.filestore.v1.Backup]
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update.  At least
            one path must be supplied in this field.
    """

    backup = proto.Field(proto.MESSAGE, number=1, message="Backup",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class GetBackupRequest(proto.Message):
    r"""GetBackupRequest gets the state of a backup.

    Attributes:
        name (str):
            Required. The backup resource name, in the format
            ``projects/{project_number}/locations/{location}/backups/{backup_id}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListBackupsRequest(proto.Message):
    r"""ListBackupsRequest lists backups.

    Attributes:
        parent (str):
            Required. The project and location for which to retrieve
            backup information, in the format
            ``projects/{project_number}/locations/{location}``. In Cloud
            Filestore, backup locations map to GCP regions, for example
            **us-west1**. To retrieve backup information for all
            locations, use "-" for the ``{location}`` value.
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

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    order_by = proto.Field(proto.STRING, number=4,)
    filter = proto.Field(proto.STRING, number=5,)


class ListBackupsResponse(proto.Message):
    r"""ListBackupsResponse is the result of ListBackupsRequest.

    Attributes:
        backups (Sequence[google.cloud.filestore_v1.types.Backup]):
            A list of backups in the project for the specified location.

            If the ``{location}`` value in the request is "-", the
            response contains a list of backups from all locations. If
            any location is unreachable, the response will only return
            backups in reachable locations and the "unreachable" field
            will be populated with a list of unreachable locations.
        next_page_token (str):
            The token you can use to retrieve the next
            page of results. Not returned if there are no
            more results in the list.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    backups = proto.RepeatedField(proto.MESSAGE, number=1, message="Backup",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


__all__ = tuple(sorted(__protobuf__.manifest))
