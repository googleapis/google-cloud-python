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
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.edgecontainer_v1.types import resources

__protobuf__ = proto.module(
    package="google.cloud.edgecontainer.v1",
    manifest={
        "OperationMetadata",
        "ListClustersRequest",
        "ListClustersResponse",
        "GetClusterRequest",
        "CreateClusterRequest",
        "UpdateClusterRequest",
        "DeleteClusterRequest",
        "GenerateAccessTokenRequest",
        "GenerateAccessTokenResponse",
        "ListNodePoolsRequest",
        "ListNodePoolsResponse",
        "GetNodePoolRequest",
        "CreateNodePoolRequest",
        "UpdateNodePoolRequest",
        "DeleteNodePoolRequest",
        "ListMachinesRequest",
        "ListMachinesResponse",
        "GetMachineRequest",
        "ListVpnConnectionsRequest",
        "ListVpnConnectionsResponse",
        "GetVpnConnectionRequest",
        "CreateVpnConnectionRequest",
        "DeleteVpnConnectionRequest",
    },
)


class OperationMetadata(proto.Message):
    r"""Long-running operation metadata for Edge Container API
    methods.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation was created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation finished running.
        target (str):
            Server-defined resource path for the target
            of the operation.
        verb (str):
            The verb executed by the operation.
        status_message (str):
            Human-readable status of the operation, if
            any.
        requested_cancellation (bool):
            Identifies whether the user has requested cancellation of
            the operation. Operations that have successfully been
            cancelled have [Operation.error][] value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            API version used to start the operation.
    """

    create_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target = proto.Field(
        proto.STRING,
        number=3,
    )
    verb = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version = proto.Field(
        proto.STRING,
        number=7,
    )


class ListClustersRequest(proto.Message):
    r"""Lists clusters in a location.

    Attributes:
        parent (str):
            Required. The parent location, which owns
            this collection of clusters.
        page_size (int):
            The maximum number of resources to list.
        page_token (str):
            A page token received from previous list
            request. A page token received from previous
            list request.
        filter (str):
            Only resources matching this filter will be
            listed.
        order_by (str):
            Specifies the order in which resources will
            be listed.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    filter = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by = proto.Field(
        proto.STRING,
        number=5,
    )


class ListClustersResponse(proto.Message):
    r"""List of clusters in a location.

    Attributes:
        clusters (Sequence[google.cloud.edgecontainer_v1.types.Cluster]):
            Clusters in the location.
        next_page_token (str):
            A token to retrieve next page of results.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    clusters = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.Cluster,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetClusterRequest(proto.Message):
    r"""Gets a cluster.

    Attributes:
        name (str):
            Required. The resource name of the cluster.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateClusterRequest(proto.Message):
    r"""Creates a cluster.

    Attributes:
        parent (str):
            Required. The parent location where this
            cluster will be created.
        cluster_id (str):
            Required. A client-specified unique
            identifier for the cluster.
        cluster (google.cloud.edgecontainer_v1.types.Cluster):
            Required. The cluster to create.
        request_id (str):
            A unique identifier for this request. Restricted to 36 ASCII
            characters. A random UUID is recommended. This request is
            only idempotent if ``request_id`` is provided.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    cluster_id = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster = proto.Field(
        proto.MESSAGE,
        number=3,
        message=resources.Cluster,
    )
    request_id = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateClusterRequest(proto.Message):
    r"""Updates a cluster.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Field mask is used to specify the fields to be overwritten
            in the Cluster resource by the update. The fields specified
            in the update_mask are relative to the resource, not the
            full request. A field will be overwritten if it is in the
            mask. If the user does not provide a mask then all fields
            will be overwritten.
        cluster (google.cloud.edgecontainer_v1.types.Cluster):
            The updated cluster.
        request_id (str):
            A unique identifier for this request. Restricted to 36 ASCII
            characters. A random UUID is recommended. This request is
            only idempotent if ``request_id`` is provided.
    """

    update_mask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    cluster = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.Cluster,
    )
    request_id = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteClusterRequest(proto.Message):
    r"""Deletes a cluster.

    Attributes:
        name (str):
            Required. The resource name of the cluster.
        request_id (str):
            A unique identifier for this request. Restricted to 36 ASCII
            characters. A random UUID is recommended. This request is
            only idempotent if ``request_id`` is provided.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id = proto.Field(
        proto.STRING,
        number=2,
    )


class GenerateAccessTokenRequest(proto.Message):
    r"""Generates an access token for a cluster.

    Attributes:
        cluster (str):
            Required. The resource name of the cluster.
    """

    cluster = proto.Field(
        proto.STRING,
        number=1,
    )


class GenerateAccessTokenResponse(proto.Message):
    r"""An access token for a cluster.

    Attributes:
        access_token (str):
            Output only. Access token to authenticate to
            k8s api-server.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp at which the token
            will expire.
    """

    access_token = proto.Field(
        proto.STRING,
        number=1,
    )
    expire_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class ListNodePoolsRequest(proto.Message):
    r"""Lists node pools in a cluster.

    Attributes:
        parent (str):
            Required. The parent cluster, which owns this
            collection of node pools.
        page_size (int):
            The maximum number of resources to list.
        page_token (str):
            A page token received from previous list
            request.
        filter (str):
            Only resources matching this filter will be
            listed.
        order_by (str):
            Specifies the order in which resources will
            be listed.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    filter = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by = proto.Field(
        proto.STRING,
        number=5,
    )


class ListNodePoolsResponse(proto.Message):
    r"""List of node pools in a cluster.

    Attributes:
        node_pools (Sequence[google.cloud.edgecontainer_v1.types.NodePool]):
            Node pools in the cluster.
        next_page_token (str):
            A token to retrieve next page of results.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    node_pools = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.NodePool,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetNodePoolRequest(proto.Message):
    r"""Gets a node pool.

    Attributes:
        name (str):
            Required. The resource name of the node pool.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateNodePoolRequest(proto.Message):
    r"""Creates a node pool.

    Attributes:
        parent (str):
            Required. The parent cluster where this node
            pool will be created.
        node_pool_id (str):
            Required. A client-specified unique
            identifier for the node pool.
        node_pool (google.cloud.edgecontainer_v1.types.NodePool):
            Required. The node pool to create.
        request_id (str):
            A unique identifier for this request. Restricted to 36 ASCII
            characters. A random UUID is recommended. This request is
            only idempotent if ``request_id`` is provided.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    node_pool_id = proto.Field(
        proto.STRING,
        number=2,
    )
    node_pool = proto.Field(
        proto.MESSAGE,
        number=3,
        message=resources.NodePool,
    )
    request_id = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateNodePoolRequest(proto.Message):
    r"""Updates a node pool.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Field mask is used to specify the fields to be overwritten
            in the NodePool resource by the update. The fields specified
            in the update_mask are relative to the resource, not the
            full request. A field will be overwritten if it is in the
            mask. If the user does not provide a mask then all fields
            will be overwritten.
        node_pool (google.cloud.edgecontainer_v1.types.NodePool):
            The updated node pool.
        request_id (str):
            A unique identifier for this request. Restricted to 36 ASCII
            characters. A random UUID is recommended. This request is
            only idempotent if ``request_id`` is provided.
    """

    update_mask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    node_pool = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.NodePool,
    )
    request_id = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteNodePoolRequest(proto.Message):
    r"""Deletes a node pool.

    Attributes:
        name (str):
            Required. The resource name of the node pool.
        request_id (str):
            A unique identifier for this request. Restricted to 36 ASCII
            characters. A random UUID is recommended. This request is
            only idempotent if ``request_id`` is provided.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id = proto.Field(
        proto.STRING,
        number=2,
    )


class ListMachinesRequest(proto.Message):
    r"""Lists machines in a site.

    Attributes:
        parent (str):
            Required. The parent site, which owns this
            collection of machines.
        page_size (int):
            The maximum number of resources to list.
        page_token (str):
            A page token received from previous list
            request.
        filter (str):
            Only resources matching this filter will be
            listed.
        order_by (str):
            Specifies the order in which resources will
            be listed.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    filter = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by = proto.Field(
        proto.STRING,
        number=5,
    )


class ListMachinesResponse(proto.Message):
    r"""List of machines in a site.

    Attributes:
        machines (Sequence[google.cloud.edgecontainer_v1.types.Machine]):
            Machines in the site.
        next_page_token (str):
            A token to retrieve next page of results.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    machines = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.Machine,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetMachineRequest(proto.Message):
    r"""Gets a machine.

    Attributes:
        name (str):
            Required. The resource name of the machine.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListVpnConnectionsRequest(proto.Message):
    r"""Lists VPN connections.

    Attributes:
        parent (str):
            Required. The parent location, which owns
            this collection of VPN connections.
        page_size (int):
            The maximum number of resources to list.
        page_token (str):
            A page token received from previous list
            request.
        filter (str):
            Only resources matching this filter will be
            listed.
        order_by (str):
            Specifies the order in which resources will
            be listed.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    filter = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by = proto.Field(
        proto.STRING,
        number=5,
    )


class ListVpnConnectionsResponse(proto.Message):
    r"""List of VPN connections in a location.

    Attributes:
        vpn_connections (Sequence[google.cloud.edgecontainer_v1.types.VpnConnection]):
            VpnConnections in the location.
        next_page_token (str):
            A token to retrieve next page of results.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    vpn_connections = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.VpnConnection,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetVpnConnectionRequest(proto.Message):
    r"""Gets a VPN connection.

    Attributes:
        name (str):
            Required. The resource name of the vpn
            connection.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateVpnConnectionRequest(proto.Message):
    r"""Creates a VPN connection.

    Attributes:
        parent (str):
            Required. The parent location where this vpn
            connection will be created.
        vpn_connection_id (str):
            Required. The VPN connection identifier.
        vpn_connection (google.cloud.edgecontainer_v1.types.VpnConnection):
            Required. The VPN connection to create.
        request_id (str):
            A unique identifier for this request. Restricted to 36 ASCII
            characters. A random UUID is recommended. This request is
            only idempotent if ``request_id`` is provided.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    vpn_connection_id = proto.Field(
        proto.STRING,
        number=2,
    )
    vpn_connection = proto.Field(
        proto.MESSAGE,
        number=3,
        message=resources.VpnConnection,
    )
    request_id = proto.Field(
        proto.STRING,
        number=4,
    )


class DeleteVpnConnectionRequest(proto.Message):
    r"""Deletes a vpn connection.

    Attributes:
        name (str):
            Required. The resource name of the vpn
            connection.
        request_id (str):
            A unique identifier for this request. Restricted to 36 ASCII
            characters. A random UUID is recommended. This request is
            only idempotent if ``request_id`` is provided.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
