# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
    package="google.cloud.memcache.v1beta2",
    manifest={
        "MemcacheVersion",
        "Instance",
        "ListInstancesRequest",
        "ListInstancesResponse",
        "GetInstanceRequest",
        "CreateInstanceRequest",
        "UpdateInstanceRequest",
        "DeleteInstanceRequest",
        "ApplyParametersRequest",
        "UpdateParametersRequest",
        "ApplySoftwareUpdateRequest",
        "MemcacheParameters",
        "OperationMetadata",
        "LocationMetadata",
        "ZoneMetadata",
    },
)


class MemcacheVersion(proto.Enum):
    r"""Memcached versions supported by our service."""
    MEMCACHE_VERSION_UNSPECIFIED = 0
    MEMCACHE_1_5 = 1


class Instance(proto.Message):
    r"""A Memorystore for Memcached instance
    Attributes:
        name (str):
            Required. Unique name of the resource in this scope
            including project and location using the form:
            ``projects/{project_id}/locations/{location_id}/instances/{instance_id}``

            Note: Memcached instances are managed and addressed at the
            regional level so ``location_id`` here refers to a Google
            Cloud region; however, users may choose which zones
            Memcached nodes should be provisioned in within an instance.
            Refer to
            [zones][google.cloud.memcache.v1beta2.Instance.zones] field
            for more details.
        display_name (str):
            User provided name for the instance, which is
            only used for display purposes. Cannot be more
            than 80 characters.
        labels (Sequence[google.cloud.memcache_v1beta2.types.Instance.LabelsEntry]):
            Resource labels to represent user-provided
            metadata. Refer to cloud documentation on labels
            for more details.
            https://cloud.google.com/compute/docs/labeling-
            resources
        authorized_network (str):
            The full name of the Google Compute Engine
            `network <https://cloud.google.com/vpc/docs/vpc>`__ to which
            the instance is connected. If left unspecified, the
            ``default`` network will be used.
        zones (Sequence[str]):
            Zones in which Memcached nodes should be
            provisioned. Memcached nodes will be equally
            distributed across these zones. If not provided,
            the service will by default create nodes in all
            zones in the region for the instance.
        node_count (int):
            Required. Number of nodes in the Memcached
            instance.
        node_config (google.cloud.memcache_v1beta2.types.Instance.NodeConfig):
            Required. Configuration for Memcached nodes.
        memcache_version (google.cloud.memcache_v1beta2.types.MemcacheVersion):
            The major version of Memcached software. If not provided,
            latest supported version will be used. Currently the latest
            supported major version is ``MEMCACHE_1_5``. The minor
            version will be automatically determined by our system based
            on the latest supported minor version.
        parameters (google.cloud.memcache_v1beta2.types.MemcacheParameters):
            Optional: User defined parameters to apply to
            the memcached process on each node.
        memcache_nodes (Sequence[google.cloud.memcache_v1beta2.types.Instance.Node]):
            Output only. List of Memcached nodes. Refer to
            [Node][google.cloud.memcache.v1beta2.Instance.Node] message
            for more details.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the instance was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the instance was
            updated.
        state (google.cloud.memcache_v1beta2.types.Instance.State):
            Output only. The state of this Memcached
            instance.
        memcache_full_version (str):
            Output only. The full version of memcached
            server running on this instance. System
            automatically determines the full memcached
            version for an instance based on the input
            MemcacheVersion.
            The full version format will be
            "memcached-1.5.16".
        instance_messages (Sequence[google.cloud.memcache_v1beta2.types.Instance.InstanceMessage]):
            List of messages that describe the current
            state of the Memcached instance.
        discovery_endpoint (str):
            Output only. Endpoint for the Discovery API.
        update_available (bool):
            Output only. Returns true if there is an
            update waiting to be applied
    """

    class State(proto.Enum):
        r"""Different states of a Memcached instance."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        DELETING = 4
        PERFORMING_MAINTENANCE = 5

    class NodeConfig(proto.Message):
        r"""Configuration for a Memcached Node.
        Attributes:
            cpu_count (int):
                Required. Number of cpus per Memcached node.
            memory_size_mb (int):
                Required. Memory size in MiB for each
                Memcached node.
        """

        cpu_count = proto.Field(proto.INT32, number=1,)
        memory_size_mb = proto.Field(proto.INT32, number=2,)

    class Node(proto.Message):
        r"""
        Attributes:
            node_id (str):
                Output only. Identifier of the Memcached
                node. The node id does not include project or
                location like the Memcached instance name.
            zone (str):
                Output only. Location (GCP Zone) for the
                Memcached node.
            state (google.cloud.memcache_v1beta2.types.Instance.Node.State):
                Output only. Current state of the Memcached
                node.
            host (str):
                Output only. Hostname or IP address of the
                Memcached node used by the clients to connect to
                the Memcached server on this node.
            port (int):
                Output only. The port number of the Memcached
                server on this node.
            parameters (google.cloud.memcache_v1beta2.types.MemcacheParameters):
                User defined parameters currently applied to
                the node.
            update_available (bool):
                Output only. Returns true if there is an
                update waiting to be applied
        """

        class State(proto.Enum):
            r"""Different states of a Memcached node."""
            STATE_UNSPECIFIED = 0
            CREATING = 1
            READY = 2
            DELETING = 3
            UPDATING = 4

        node_id = proto.Field(proto.STRING, number=1,)
        zone = proto.Field(proto.STRING, number=2,)
        state = proto.Field(proto.ENUM, number=3, enum="Instance.Node.State",)
        host = proto.Field(proto.STRING, number=4,)
        port = proto.Field(proto.INT32, number=5,)
        parameters = proto.Field(proto.MESSAGE, number=6, message="MemcacheParameters",)
        update_available = proto.Field(proto.BOOL, number=7,)

    class InstanceMessage(proto.Message):
        r"""
        Attributes:
            code (google.cloud.memcache_v1beta2.types.Instance.InstanceMessage.Code):
                A code that correspond to one type of user-
                acing message.
            message (str):
                Message on memcached instance which will be
                exposed to users.
        """

        class Code(proto.Enum):
            r""""""
            CODE_UNSPECIFIED = 0
            ZONE_DISTRIBUTION_UNBALANCED = 1

        code = proto.Field(proto.ENUM, number=1, enum="Instance.InstanceMessage.Code",)
        message = proto.Field(proto.STRING, number=2,)

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=3,)
    authorized_network = proto.Field(proto.STRING, number=4,)
    zones = proto.RepeatedField(proto.STRING, number=5,)
    node_count = proto.Field(proto.INT32, number=6,)
    node_config = proto.Field(proto.MESSAGE, number=7, message=NodeConfig,)
    memcache_version = proto.Field(proto.ENUM, number=9, enum="MemcacheVersion",)
    parameters = proto.Field(proto.MESSAGE, number=11, message="MemcacheParameters",)
    memcache_nodes = proto.RepeatedField(proto.MESSAGE, number=12, message=Node,)
    create_time = proto.Field(
        proto.MESSAGE, number=13, message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE, number=14, message=timestamp_pb2.Timestamp,
    )
    state = proto.Field(proto.ENUM, number=15, enum=State,)
    memcache_full_version = proto.Field(proto.STRING, number=18,)
    instance_messages = proto.RepeatedField(
        proto.MESSAGE, number=19, message=InstanceMessage,
    )
    discovery_endpoint = proto.Field(proto.STRING, number=20,)
    update_available = proto.Field(proto.BOOL, number=21,)


class ListInstancesRequest(proto.Message):
    r"""Request for
    [ListInstances][google.cloud.memcache.v1beta2.CloudMemcache.ListInstances].

    Attributes:
        parent (str):
            Required. The resource name of the instance location using
            the form: ``projects/{project_id}/locations/{location_id}``
            where ``location_id`` refers to a GCP region
        page_size (int):
            The maximum number of items to return.

            If not specified, a default value of 1000 will be used by
            the service. Regardless of the ``page_size`` value, the
            response may include a partial list and a caller should only
            rely on response's
            [``next_page_token``][google.cloud.memcache.v1beta2.ListInstancesResponse.next_page_token]
            to determine if there are more instances left to be queried.
        page_token (str):
            The ``next_page_token`` value returned from a previous List
            request, if any.
        filter (str):
            List filter. For example, exclude all Memcached instances
            with name as my-instance by specifying
            ``"name != my-instance"``.
        order_by (str):
            Sort results. Supported values are "name",
            "name desc" or "" (unsorted).
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListInstancesResponse(proto.Message):
    r"""Response for
    [ListInstances][google.cloud.memcache.v1beta2.CloudMemcache.ListInstances].

    Attributes:
        resources (Sequence[google.cloud.memcache_v1beta2.types.Instance]):
            A list of Memcached instances in the project in the
            specified location, or across all locations.

            If the ``location_id`` in the parent field of the request is
            "-", all regions available to the project are queried, and
            the results aggregated.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    resources = proto.RepeatedField(proto.MESSAGE, number=1, message="Instance",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetInstanceRequest(proto.Message):
    r"""Request for
    [GetInstance][google.cloud.memcache.v1beta2.CloudMemcache.GetInstance].

    Attributes:
        name (str):
            Required. Memcached instance resource name in the format:
            ``projects/{project_id}/locations/{location_id}/instances/{instance_id}``
            where ``location_id`` refers to a GCP region
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateInstanceRequest(proto.Message):
    r"""Request for
    [CreateInstance][google.cloud.memcache.v1beta2.CloudMemcache.CreateInstance].

    Attributes:
        parent (str):
            Required. The resource name of the instance location using
            the form: ``projects/{project_id}/locations/{location_id}``
            where ``location_id`` refers to a GCP region
        instance_id (str):
            Required. The logical name of the Memcached instance in the
            user project with the following restrictions:

            -  Must contain only lowercase letters, numbers, and
               hyphens.
            -  Must start with a letter.
            -  Must be between 1-40 characters.
            -  Must end with a number or a letter.
            -  Must be unique within the user project / location.

            If any of the above are not met, the API raises an invalid
            argument error.
        resource (google.cloud.memcache_v1beta2.types.Instance):
            Required. A Memcached [Instance] resource
    """

    parent = proto.Field(proto.STRING, number=1,)
    instance_id = proto.Field(proto.STRING, number=2,)
    resource = proto.Field(proto.MESSAGE, number=3, message="Instance",)


class UpdateInstanceRequest(proto.Message):
    r"""Request for
    [UpdateInstance][google.cloud.memcache.v1beta2.CloudMemcache.UpdateInstance].

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update.

            -  ``displayName``
        resource (google.cloud.memcache_v1beta2.types.Instance):
            Required. A Memcached [Instance] resource. Only fields
            specified in update_mask are updated.
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    resource = proto.Field(proto.MESSAGE, number=2, message="Instance",)


class DeleteInstanceRequest(proto.Message):
    r"""Request for
    [DeleteInstance][google.cloud.memcache.v1beta2.CloudMemcache.DeleteInstance].

    Attributes:
        name (str):
            Required. Memcached instance resource name in the format:
            ``projects/{project_id}/locations/{location_id}/instances/{instance_id}``
            where ``location_id`` refers to a GCP region
    """

    name = proto.Field(proto.STRING, number=1,)


class ApplyParametersRequest(proto.Message):
    r"""Request for
    [ApplyParameters][google.cloud.memcache.v1beta2.CloudMemcache.ApplyParameters].

    Attributes:
        name (str):
            Required. Resource name of the Memcached
            instance for which parameter group updates
            should be applied.
        node_ids (Sequence[str]):
            Nodes to which the instance-level parameter
            group is applied.
        apply_all (bool):
            Whether to apply instance-level parameter group to all
            nodes. If set to true, users are restricted from specifying
            individual nodes, and ``ApplyParameters`` updates all nodes
            within the instance.
    """

    name = proto.Field(proto.STRING, number=1,)
    node_ids = proto.RepeatedField(proto.STRING, number=2,)
    apply_all = proto.Field(proto.BOOL, number=3,)


class UpdateParametersRequest(proto.Message):
    r"""Request for
    [UpdateParameters][google.cloud.memcache.v1beta2.CloudMemcache.UpdateParameters].

    Attributes:
        name (str):
            Required. Resource name of the Memcached
            instance for which the parameters should be
            updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update.
        parameters (google.cloud.memcache_v1beta2.types.MemcacheParameters):
            The parameters to apply to the instance.
    """

    name = proto.Field(proto.STRING, number=1,)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )
    parameters = proto.Field(proto.MESSAGE, number=3, message="MemcacheParameters",)


class ApplySoftwareUpdateRequest(proto.Message):
    r"""Request for
    [ApplySoftwareUpdate][google.cloud.memcache.v1beta2.CloudMemcache.ApplySoftwareUpdate].

    Attributes:
        instance (str):
            Required. Resource name of the Memcached
            instance for which software update should be
            applied.
        node_ids (Sequence[str]):
            Nodes to which we should apply the update to.
            Note all the selected nodes are updated in
            parallel.
        apply_all (bool):
            Whether to apply the update to all nodes. If
            set to true, will explicitly restrict users from
            specifying any nodes, and apply software update
            to all nodes (where applicable) within the
            instance.
    """

    instance = proto.Field(proto.STRING, number=1,)
    node_ids = proto.RepeatedField(proto.STRING, number=2,)
    apply_all = proto.Field(proto.BOOL, number=3,)


class MemcacheParameters(proto.Message):
    r"""The unique ID associated with this set of parameters. Users
    can use this id to determine if the parameters associated with
    the instance differ from the parameters associated with the
    nodes. A discrepancy between parameter ids can inform users that
    they may need to take action to apply parameters on nodes.

    Attributes:
        id (str):
            Output only.
        params (Sequence[google.cloud.memcache_v1beta2.types.MemcacheParameters.ParamsEntry]):
            User defined set of parameters to use in the
            memcached process.
    """

    id = proto.Field(proto.STRING, number=1,)
    params = proto.MapField(proto.STRING, proto.STRING, number=3,)


class OperationMetadata(proto.Message):
    r"""Represents the metadata of a long-running operation.
    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_detail (str):
            Output only. Human-readable status of the
            operation, if any.
        cancel_requested (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have
            successfully been cancelled have [Operation.error][] value
            with a [google.rpc.Status.code][google.rpc.Status.code] of
            1, corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    target = proto.Field(proto.STRING, number=3,)
    verb = proto.Field(proto.STRING, number=4,)
    status_detail = proto.Field(proto.STRING, number=5,)
    cancel_requested = proto.Field(proto.BOOL, number=6,)
    api_version = proto.Field(proto.STRING, number=7,)


class LocationMetadata(proto.Message):
    r"""Metadata for the given
    [google.cloud.location.Location][google.cloud.location.Location].

    Attributes:
        available_zones (Sequence[google.cloud.memcache_v1beta2.types.LocationMetadata.AvailableZonesEntry]):
            Output only. The set of available zones in the location. The
            map is keyed by the lowercase ID of each zone, as defined by
            GCE. These keys can be specified in the ``zones`` field when
            creating a Memcached instance.
    """

    available_zones = proto.MapField(
        proto.STRING, proto.MESSAGE, number=1, message="ZoneMetadata",
    )


class ZoneMetadata(proto.Message):
    r"""    """


__all__ = tuple(sorted(__protobuf__.manifest))
