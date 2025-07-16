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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.lustre.v1",
    manifest={
        "Instance",
        "ListInstancesRequest",
        "ListInstancesResponse",
        "GetInstanceRequest",
        "CreateInstanceRequest",
        "UpdateInstanceRequest",
        "DeleteInstanceRequest",
        "OperationMetadata",
    },
)


class Instance(proto.Message):
    r"""A Managed Lustre instance.

    Attributes:
        name (str):
            Identifier. The name of the instance.
        filesystem (str):
            Required. Immutable. The filesystem name for
            this instance. This name is used by client-side
            tools, including when mounting the instance.
            Must be eight characters or less and can only
            contain letters and numbers.
        capacity_gib (int):
            Required. The storage capacity of the instance in gibibytes
            (GiB). Allowed values are from ``18000`` to ``954000``, in
            increments of 9000.
        network (str):
            Required. Immutable. The full name of the VPC network to
            which the instance is connected. Must be in the format
            ``projects/{project_id}/global/networks/{network_name}``.
        state (google.cloud.lustre_v1.types.Instance.State):
            Output only. The state of the instance.
        mount_point (str):
            Output only. Mount point of the instance in the format
            ``IP_ADDRESS@tcp:/FILESYSTEM``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the instance was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the instance was
            last updated.
        description (str):
            Optional. A user-readable description of the
            instance.
        labels (MutableMapping[str, str]):
            Optional. Labels as key value pairs.
        per_unit_storage_throughput (int):
            Required. The throughput of the instance in
            MB/s/TiB. Valid values are 125, 250, 500, 1000.
        gke_support_enabled (bool):
            Optional. Indicates whether you want to
            enable support for GKE clients. By default, GKE
            clients are not supported. Deprecated. No longer
            required for GKE instance creation.
    """

    class State(proto.Enum):
        r"""The possible states of an instance.

        Values:
            STATE_UNSPECIFIED (0):
                Not set.
            ACTIVE (1):
                The instance is available for use.
            CREATING (2):
                The instance is being created and is not yet
                ready for use.
            DELETING (3):
                The instance is being deleted.
            UPGRADING (4):
                The instance is being upgraded.
            REPAIRING (5):
                The instance is being repaired.
            STOPPED (6):
                The instance is stopped.
            UPDATING (7):
                The instance is being updated.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2
        DELETING = 3
        UPGRADING = 4
        REPAIRING = 5
        STOPPED = 6
        UPDATING = 7

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filesystem: str = proto.Field(
        proto.STRING,
        number=10,
    )
    capacity_gib: int = proto.Field(
        proto.INT64,
        number=2,
    )
    network: str = proto.Field(
        proto.STRING,
        number=3,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    mount_point: str = proto.Field(
        proto.STRING,
        number=5,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    description: str = proto.Field(
        proto.STRING,
        number=8,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    per_unit_storage_throughput: int = proto.Field(
        proto.INT64,
        number=11,
    )
    gke_support_enabled: bool = proto.Field(
        proto.BOOL,
        number=12,
    )


class ListInstancesRequest(proto.Message):
    r"""Message for requesting list of Instances

    Attributes:
        parent (str):
            Required. The project and location for which to retrieve a
            list of instances, in the format
            ``projects/{projectId}/locations/{location}``.

            To retrieve instance information for all locations, use "-"
            as the value of ``{location}``.
        page_size (int):
            Optional. Requested page size. Server might
            return fewer items than requested. If
            unspecified, the server will pick an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
        filter (str):
            Optional. Filtering results.
        order_by (str):
            Optional. Desired order of results.
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
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListInstancesResponse(proto.Message):
    r"""Message for response to listing Instances

    Attributes:
        instances (MutableSequence[google.cloud.lustre_v1.types.Instance]):
            Response from
            [ListInstances][google.cloud.lustre.v1.Lustre.ListInstances].
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Unordered list. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    instances: MutableSequence["Instance"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Instance",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetInstanceRequest(proto.Message):
    r"""Message for getting a Instance

    Attributes:
        name (str):
            Required. The instance resource name, in the format
            ``projects/{projectId}/locations/{location}/instances/{instanceId}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateInstanceRequest(proto.Message):
    r"""Message for creating a Instance

    Attributes:
        parent (str):
            Required. The instance's project and location, in the format
            ``projects/{project}/locations/{location}``. Locations map
            to Google Cloud zones; for example, ``us-west1-b``.
        instance_id (str):
            Required. The name of the Managed Lustre instance.

            -  Must contain only lowercase letters, numbers, and
               hyphens.
            -  Must start with a letter.
            -  Must be between 1-63 characters.
            -  Must end with a number or a letter.
        instance (google.cloud.lustre_v1.types.Instance):
            Required. The resource being created
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

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

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    instance_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    instance: "Instance" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Instance",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateInstanceRequest(proto.Message):
    r"""Message for updating a Instance

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Specifies the fields to be overwritten in the
            instance resource by the update.

            The fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If no mask is provided then all fields
            present in the request are overwritten.
        instance (google.cloud.lustre_v1.types.Instance):
            Required. The resource name of the instance to update, in
            the format
            ``projects/{projectId}/locations/{location}/instances/{instanceId}``.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

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

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    instance: "Instance" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Instance",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteInstanceRequest(proto.Message):
    r"""Message for deleting a Instance

    Attributes:
        name (str):
            Required. The resource name of the instance to delete, in
            the format
            ``projects/{projectId}/locations/{location}/instances/{instanceId}``.
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


class OperationMetadata(proto.Message):
    r"""Represents the metadata of a long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have been
            cancelled successfully have [Operation.error][] value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
