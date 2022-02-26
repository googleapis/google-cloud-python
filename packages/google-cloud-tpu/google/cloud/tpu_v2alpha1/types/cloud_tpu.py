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
    package="google.cloud.tpu.v2alpha1",
    manifest={
        "GuestAttributes",
        "GuestAttributesValue",
        "GuestAttributesEntry",
        "AttachedDisk",
        "SchedulingConfig",
        "NetworkEndpoint",
        "AccessConfig",
        "NetworkConfig",
        "ServiceAccount",
        "Node",
        "ListNodesRequest",
        "ListNodesResponse",
        "GetNodeRequest",
        "CreateNodeRequest",
        "DeleteNodeRequest",
        "StopNodeRequest",
        "StartNodeRequest",
        "UpdateNodeRequest",
        "ServiceIdentity",
        "GenerateServiceIdentityRequest",
        "GenerateServiceIdentityResponse",
        "AcceleratorType",
        "GetAcceleratorTypeRequest",
        "ListAcceleratorTypesRequest",
        "ListAcceleratorTypesResponse",
        "OperationMetadata",
        "RuntimeVersion",
        "GetRuntimeVersionRequest",
        "ListRuntimeVersionsRequest",
        "ListRuntimeVersionsResponse",
        "Symptom",
        "GetGuestAttributesRequest",
        "GetGuestAttributesResponse",
    },
)


class GuestAttributes(proto.Message):
    r"""A guest attributes.

    Attributes:
        query_path (str):
            The path to be queried. This can be the
            default namespace ('/') or a nested namespace
            ('/\<namespace\>/') or a specified key
            ('/\<namespace\>/\<key\>')
        query_value (google.cloud.tpu_v2alpha1.types.GuestAttributesValue):
            The value of the requested queried path.
    """

    query_path = proto.Field(proto.STRING, number=1,)
    query_value = proto.Field(proto.MESSAGE, number=2, message="GuestAttributesValue",)


class GuestAttributesValue(proto.Message):
    r"""Array of guest attribute namespace/key/value tuples.

    Attributes:
        items (Sequence[google.cloud.tpu_v2alpha1.types.GuestAttributesEntry]):
            The list of guest attributes entries.
    """

    items = proto.RepeatedField(
        proto.MESSAGE, number=1, message="GuestAttributesEntry",
    )


class GuestAttributesEntry(proto.Message):
    r"""A guest attributes namespace/key/value entry.

    Attributes:
        namespace (str):
            Namespace for the guest attribute entry.
        key (str):
            Key for the guest attribute entry.
        value (str):
            Value for the guest attribute entry.
    """

    namespace = proto.Field(proto.STRING, number=1,)
    key = proto.Field(proto.STRING, number=2,)
    value = proto.Field(proto.STRING, number=3,)


class AttachedDisk(proto.Message):
    r"""A node-attached disk resource.
    Next ID: 8;

    Attributes:
        source_disk (str):
            Specifies the full path to an existing disk.
            For example:
            "projects/my-project/zones/us-central1-c/disks/my-disk".
        mode (google.cloud.tpu_v2alpha1.types.AttachedDisk.DiskMode):
            The mode in which to attach this disk. If not specified, the
            default is READ_WRITE mode. Only applicable to data_disks.
    """

    class DiskMode(proto.Enum):
        r"""The different mode of the attached disk."""
        DISK_MODE_UNSPECIFIED = 0
        READ_WRITE = 1
        READ_ONLY = 2

    source_disk = proto.Field(proto.STRING, number=3,)
    mode = proto.Field(proto.ENUM, number=4, enum=DiskMode,)


class SchedulingConfig(proto.Message):
    r"""Sets the scheduling options for this node.

    Attributes:
        preemptible (bool):
            Defines whether the node is preemptible.
        reserved (bool):
            Whether the node is created under a
            reservation.
    """

    preemptible = proto.Field(proto.BOOL, number=1,)
    reserved = proto.Field(proto.BOOL, number=2,)


class NetworkEndpoint(proto.Message):
    r"""A network endpoint over which a TPU worker can be reached.

    Attributes:
        ip_address (str):
            The internal IP address of this network
            endpoint.
        port (int):
            The port of this network endpoint.
        access_config (google.cloud.tpu_v2alpha1.types.AccessConfig):
            The access config for the TPU worker.
    """

    ip_address = proto.Field(proto.STRING, number=1,)
    port = proto.Field(proto.INT32, number=2,)
    access_config = proto.Field(proto.MESSAGE, number=5, message="AccessConfig",)


class AccessConfig(proto.Message):
    r"""An access config attached to the TPU worker.

    Attributes:
        external_ip (str):
            Output only. An external IP address
            associated with the TPU worker.
    """

    external_ip = proto.Field(proto.STRING, number=1,)


class NetworkConfig(proto.Message):
    r"""Network related configurations.

    Attributes:
        network (str):
            The name of the network for the TPU node. It
            must be a preexisting Google Compute Engine
            network. If none is provided, "default" will be
            used.
        subnetwork (str):
            The name of the subnetwork for the TPU node.
            It must be a preexisting Google Compute Engine
            subnetwork. If none is provided, "default" will
            be used.
        enable_external_ips (bool):
            Indicates that external IP addresses would be
            associated with the TPU workers. If set to
            false, the specified subnetwork or network
            should have Private Google Access enabled.
    """

    network = proto.Field(proto.STRING, number=1,)
    subnetwork = proto.Field(proto.STRING, number=2,)
    enable_external_ips = proto.Field(proto.BOOL, number=3,)


class ServiceAccount(proto.Message):
    r"""A service account.

    Attributes:
        email (str):
            Email address of the service account. If
            empty, default Compute service account will be
            used.
        scope (Sequence[str]):
            The list of scopes to be made available for
            this service account. If empty, access to all
            Cloud APIs will be allowed.
    """

    email = proto.Field(proto.STRING, number=1,)
    scope = proto.RepeatedField(proto.STRING, number=2,)


class Node(proto.Message):
    r"""A TPU instance.

    Attributes:
        name (str):
            Output only. Immutable. The name of the TPU.
        description (str):
            The user-supplied description of the TPU.
            Maximum of 512 characters.
        accelerator_type (str):
            Required. The type of hardware accelerators
            associated with this node.
        state (google.cloud.tpu_v2alpha1.types.Node.State):
            Output only. The current state for the TPU
            Node.
        health_description (str):
            Output only. If this field is populated, it
            contains a description of why the TPU Node is
            unhealthy.
        runtime_version (str):
            Required. The runtime version running in the
            Node.
        network_config (google.cloud.tpu_v2alpha1.types.NetworkConfig):
            Network configurations for the TPU node.
        cidr_block (str):
            The CIDR block that the TPU node will use
            when selecting an IP address. This CIDR block
            must be a /29 block; the Compute Engine networks
            API forbids a smaller block, and using a larger
            block would be wasteful (a node can only consume
            one IP address). Errors will occur if the CIDR
            block has already been used for a currently
            existing TPU node, the CIDR block conflicts with
            any subnetworks in the user's provided network,
            or the provided network is peered with another
            network that is using that CIDR block.
        service_account (google.cloud.tpu_v2alpha1.types.ServiceAccount):
            The Google Cloud Platform Service Account to
            be used by the TPU node VMs. If None is
            specified, the default compute service account
            will be used.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the node was
            created.
        scheduling_config (google.cloud.tpu_v2alpha1.types.SchedulingConfig):
            The scheduling options for this node.
        network_endpoints (Sequence[google.cloud.tpu_v2alpha1.types.NetworkEndpoint]):
            Output only. The network endpoints where TPU
            workers can be accessed and sent work. It is
            recommended that runtime clients of the node
            reach out to the 0th entry in this map first.
        health (google.cloud.tpu_v2alpha1.types.Node.Health):
            The health status of the TPU node.
        labels (Sequence[google.cloud.tpu_v2alpha1.types.Node.LabelsEntry]):
            Resource labels to represent user-provided
            metadata.
        metadata (Sequence[google.cloud.tpu_v2alpha1.types.Node.MetadataEntry]):
            Custom metadata to apply to the TPU Node.
            Can set startup-script and shutdown-script
        tags (Sequence[str]):
            Tags to apply to the TPU Node. Tags are used
            to identify valid sources or targets for network
            firewalls.
        id (int):
            Output only. The unique identifier for the
            TPU Node.
        data_disks (Sequence[google.cloud.tpu_v2alpha1.types.AttachedDisk]):
            The additional data disks for the Node.
        api_version (google.cloud.tpu_v2alpha1.types.Node.ApiVersion):
            Output only. The API version that created
            this Node.
        symptoms (Sequence[google.cloud.tpu_v2alpha1.types.Symptom]):
            Output only. The Symptoms that have occurred
            to the TPU Node.
    """

    class State(proto.Enum):
        r"""Represents the different states of a TPU node during its
        lifecycle.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        RESTARTING = 3
        REIMAGING = 4
        DELETING = 5
        REPAIRING = 6
        STOPPED = 8
        STOPPING = 9
        STARTING = 10
        PREEMPTED = 11
        TERMINATED = 12
        HIDING = 13
        HIDDEN = 14
        UNHIDING = 15

    class Health(proto.Enum):
        r"""Health defines the status of a TPU node as reported by
        Health Monitor.
        """
        HEALTH_UNSPECIFIED = 0
        HEALTHY = 1
        TIMEOUT = 3
        UNHEALTHY_TENSORFLOW = 4
        UNHEALTHY_MAINTENANCE = 5

    class ApiVersion(proto.Enum):
        r"""TPU API Version."""
        API_VERSION_UNSPECIFIED = 0
        V1_ALPHA1 = 1
        V1 = 2
        V2_ALPHA1 = 3

    name = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=3,)
    accelerator_type = proto.Field(proto.STRING, number=5,)
    state = proto.Field(proto.ENUM, number=9, enum=State,)
    health_description = proto.Field(proto.STRING, number=10,)
    runtime_version = proto.Field(proto.STRING, number=11,)
    network_config = proto.Field(proto.MESSAGE, number=36, message="NetworkConfig",)
    cidr_block = proto.Field(proto.STRING, number=13,)
    service_account = proto.Field(proto.MESSAGE, number=37, message="ServiceAccount",)
    create_time = proto.Field(
        proto.MESSAGE, number=16, message=timestamp_pb2.Timestamp,
    )
    scheduling_config = proto.Field(
        proto.MESSAGE, number=17, message="SchedulingConfig",
    )
    network_endpoints = proto.RepeatedField(
        proto.MESSAGE, number=21, message="NetworkEndpoint",
    )
    health = proto.Field(proto.ENUM, number=22, enum=Health,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=24,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=34,)
    tags = proto.RepeatedField(proto.STRING, number=40,)
    id = proto.Field(proto.INT64, number=33,)
    data_disks = proto.RepeatedField(proto.MESSAGE, number=41, message="AttachedDisk",)
    api_version = proto.Field(proto.ENUM, number=38, enum=ApiVersion,)
    symptoms = proto.RepeatedField(proto.MESSAGE, number=39, message="Symptom",)


class ListNodesRequest(proto.Message):
    r"""Request for [ListNodes][google.cloud.tpu.v2alpha1.Tpu.ListNodes].

    Attributes:
        parent (str):
            Required. The parent resource name.
        page_size (int):
            The maximum number of items to return.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListNodesResponse(proto.Message):
    r"""Response for [ListNodes][google.cloud.tpu.v2alpha1.Tpu.ListNodes].

    Attributes:
        nodes (Sequence[google.cloud.tpu_v2alpha1.types.Node]):
            The listed nodes.
        next_page_token (str):
            The next page token or empty if none.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    nodes = proto.RepeatedField(proto.MESSAGE, number=1, message="Node",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetNodeRequest(proto.Message):
    r"""Request for [GetNode][google.cloud.tpu.v2alpha1.Tpu.GetNode].

    Attributes:
        name (str):
            Required. The resource name.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateNodeRequest(proto.Message):
    r"""Request for [CreateNode][google.cloud.tpu.v2alpha1.Tpu.CreateNode].

    Attributes:
        parent (str):
            Required. The parent resource name.
        node_id (str):
            The unqualified resource name.
        node (google.cloud.tpu_v2alpha1.types.Node):
            Required. The node.
    """

    parent = proto.Field(proto.STRING, number=1,)
    node_id = proto.Field(proto.STRING, number=2,)
    node = proto.Field(proto.MESSAGE, number=3, message="Node",)


class DeleteNodeRequest(proto.Message):
    r"""Request for [DeleteNode][google.cloud.tpu.v2alpha1.Tpu.DeleteNode].

    Attributes:
        name (str):
            Required. The resource name.
    """

    name = proto.Field(proto.STRING, number=1,)


class StopNodeRequest(proto.Message):
    r"""Request for [StopNode][google.cloud.tpu.v2alpha1.Tpu.StopNode].

    Attributes:
        name (str):
            The resource name.
    """

    name = proto.Field(proto.STRING, number=1,)


class StartNodeRequest(proto.Message):
    r"""Request for [StartNode][google.cloud.tpu.v2alpha1.Tpu.StartNode].

    Attributes:
        name (str):
            The resource name.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateNodeRequest(proto.Message):
    r"""Request for [UpdateNode][google.cloud.tpu.v2alpha1.Tpu.UpdateNode].

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields from [Node][Tpu.Node] to update.
            Supported fields: None.
        node (google.cloud.tpu_v2alpha1.types.Node):
            Required. The node. Only fields specified in update_mask are
            updated.
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    node = proto.Field(proto.MESSAGE, number=2, message="Node",)


class ServiceIdentity(proto.Message):
    r"""The per-product per-project service identity for Cloud TPU
    service.

    Attributes:
        email (str):
            The email address of the service identity.
    """

    email = proto.Field(proto.STRING, number=1,)


class GenerateServiceIdentityRequest(proto.Message):
    r"""Request for
    [GenerateServiceIdentity][google.cloud.tpu.v2alpha1.Tpu.GenerateServiceIdentity].

    Attributes:
        parent (str):
            Required. The parent resource name.
    """

    parent = proto.Field(proto.STRING, number=1,)


class GenerateServiceIdentityResponse(proto.Message):
    r"""Response for
    [GenerateServiceIdentity][google.cloud.tpu.v2alpha1.Tpu.GenerateServiceIdentity].

    Attributes:
        identity (google.cloud.tpu_v2alpha1.types.ServiceIdentity):
            ServiceIdentity that was created or
            retrieved.
    """

    identity = proto.Field(proto.MESSAGE, number=1, message="ServiceIdentity",)


class AcceleratorType(proto.Message):
    r"""A accelerator type that a Node can be configured with.

    Attributes:
        name (str):
            The resource name.
        type_ (str):
            the accelerator type.
    """

    name = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.STRING, number=2,)


class GetAcceleratorTypeRequest(proto.Message):
    r"""Request for
    [GetAcceleratorType][google.cloud.tpu.v2alpha1.Tpu.GetAcceleratorType].

    Attributes:
        name (str):
            Required. The resource name.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListAcceleratorTypesRequest(proto.Message):
    r"""Request for
    [ListAcceleratorTypes][google.cloud.tpu.v2alpha1.Tpu.ListAcceleratorTypes].

    Attributes:
        parent (str):
            Required. The parent resource name.
        page_size (int):
            The maximum number of items to return.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
        filter (str):
            List filter.
        order_by (str):
            Sort results.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=5,)
    order_by = proto.Field(proto.STRING, number=6,)


class ListAcceleratorTypesResponse(proto.Message):
    r"""Response for
    [ListAcceleratorTypes][google.cloud.tpu.v2alpha1.Tpu.ListAcceleratorTypes].

    Attributes:
        accelerator_types (Sequence[google.cloud.tpu_v2alpha1.types.AcceleratorType]):
            The listed nodes.
        next_page_token (str):
            The next page token or empty if none.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    accelerator_types = proto.RepeatedField(
        proto.MESSAGE, number=1, message="AcceleratorType",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class OperationMetadata(proto.Message):
    r"""Metadata describing an [Operation][google.longrunning.Operation]

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation was created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation finished running.
        target (str):
            Target of the operation - for example
            projects/project-1/connectivityTests/test-1
        verb (str):
            Name of the verb executed by the operation.
        status_detail (str):
            Human-readable status of the operation, if
            any.
        cancel_requested (bool):
            Specifies if cancellation was requested for
            the operation.
        api_version (str):
            API version.
    """

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    target = proto.Field(proto.STRING, number=3,)
    verb = proto.Field(proto.STRING, number=4,)
    status_detail = proto.Field(proto.STRING, number=5,)
    cancel_requested = proto.Field(proto.BOOL, number=6,)
    api_version = proto.Field(proto.STRING, number=7,)


class RuntimeVersion(proto.Message):
    r"""A runtime version that a Node can be configured with.

    Attributes:
        name (str):
            The resource name.
        version (str):
            The runtime version.
    """

    name = proto.Field(proto.STRING, number=1,)
    version = proto.Field(proto.STRING, number=2,)


class GetRuntimeVersionRequest(proto.Message):
    r"""Request for
    [GetRuntimeVersion][google.cloud.tpu.v2alpha1.Tpu.GetRuntimeVersion].

    Attributes:
        name (str):
            Required. The resource name.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListRuntimeVersionsRequest(proto.Message):
    r"""Request for
    [ListRuntimeVersions][google.cloud.tpu.v2alpha1.Tpu.ListRuntimeVersions].

    Attributes:
        parent (str):
            Required. The parent resource name.
        page_size (int):
            The maximum number of items to return.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
        filter (str):
            List filter.
        order_by (str):
            Sort results.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=5,)
    order_by = proto.Field(proto.STRING, number=6,)


class ListRuntimeVersionsResponse(proto.Message):
    r"""Response for
    [ListRuntimeVersions][google.cloud.tpu.v2alpha1.Tpu.ListRuntimeVersions].

    Attributes:
        runtime_versions (Sequence[google.cloud.tpu_v2alpha1.types.RuntimeVersion]):
            The listed nodes.
        next_page_token (str):
            The next page token or empty if none.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    runtime_versions = proto.RepeatedField(
        proto.MESSAGE, number=1, message="RuntimeVersion",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class Symptom(proto.Message):
    r"""A Symptom instance.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp when the Symptom is created.
        symptom_type (google.cloud.tpu_v2alpha1.types.Symptom.SymptomType):
            Type of the Symptom.
        details (str):
            Detailed information of the current Symptom.
        worker_id (str):
            A string used to uniquely distinguish a
            worker within a TPU node.
    """

    class SymptomType(proto.Enum):
        r"""SymptomType represents the different types of Symptoms that a
        TPU can be at.
        """
        SYMPTOM_TYPE_UNSPECIFIED = 0
        LOW_MEMORY = 1
        OUT_OF_MEMORY = 2
        EXECUTE_TIMED_OUT = 3
        MESH_BUILD_FAIL = 4
        HBM_OUT_OF_MEMORY = 5
        PROJECT_ABUSE = 6

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    symptom_type = proto.Field(proto.ENUM, number=2, enum=SymptomType,)
    details = proto.Field(proto.STRING, number=3,)
    worker_id = proto.Field(proto.STRING, number=4,)


class GetGuestAttributesRequest(proto.Message):
    r"""Request for
    [GetGuestAttributes][google.cloud.tpu.v2alpha1.Tpu.GetGuestAttributes].

    Attributes:
        name (str):
            Required. The resource name.
        query_path (str):
            The guest attributes path to be queried.
        worker_ids (Sequence[str]):
            The 0-based worker ID. If it is empty, all
            workers' GuestAttributes will be returned.
    """

    name = proto.Field(proto.STRING, number=1,)
    query_path = proto.Field(proto.STRING, number=2,)
    worker_ids = proto.RepeatedField(proto.STRING, number=3,)


class GetGuestAttributesResponse(proto.Message):
    r"""Response for
    [GetGuestAttributes][google.cloud.tpu.v2alpha1.Tpu.GetGuestAttributes].

    Attributes:
        guest_attributes (Sequence[google.cloud.tpu_v2alpha1.types.GuestAttributes]):
            The guest attributes for the TPU workers.
    """

    guest_attributes = proto.RepeatedField(
        proto.MESSAGE, number=1, message="GuestAttributes",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
