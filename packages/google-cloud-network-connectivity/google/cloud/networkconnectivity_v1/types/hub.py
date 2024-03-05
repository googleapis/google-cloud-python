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
    package="google.cloud.networkconnectivity.v1",
    manifest={
        "LocationFeature",
        "RouteType",
        "State",
        "SpokeType",
        "Hub",
        "RoutingVPC",
        "Spoke",
        "RouteTable",
        "Route",
        "Group",
        "ListHubsRequest",
        "ListHubsResponse",
        "GetHubRequest",
        "CreateHubRequest",
        "UpdateHubRequest",
        "DeleteHubRequest",
        "ListHubSpokesRequest",
        "ListHubSpokesResponse",
        "ListSpokesRequest",
        "ListSpokesResponse",
        "GetSpokeRequest",
        "CreateSpokeRequest",
        "UpdateSpokeRequest",
        "DeleteSpokeRequest",
        "AcceptHubSpokeRequest",
        "AcceptHubSpokeResponse",
        "RejectHubSpokeRequest",
        "RejectHubSpokeResponse",
        "GetRouteTableRequest",
        "GetRouteRequest",
        "ListRoutesRequest",
        "ListRoutesResponse",
        "ListRouteTablesRequest",
        "ListRouteTablesResponse",
        "ListGroupsRequest",
        "ListGroupsResponse",
        "LinkedVpnTunnels",
        "LinkedInterconnectAttachments",
        "LinkedRouterApplianceInstances",
        "LinkedVpcNetwork",
        "RouterApplianceInstance",
        "LocationMetadata",
        "NextHopVpcNetwork",
        "SpokeSummary",
        "GetGroupRequest",
    },
)


class LocationFeature(proto.Enum):
    r"""Supported features for a location

    Values:
        LOCATION_FEATURE_UNSPECIFIED (0):
            No publicly supported feature in this
            location
        SITE_TO_CLOUD_SPOKES (1):
            Site-to-cloud spokes are supported in this
            location
        SITE_TO_SITE_SPOKES (2):
            Site-to-site spokes are supported in this
            location
    """
    LOCATION_FEATURE_UNSPECIFIED = 0
    SITE_TO_CLOUD_SPOKES = 1
    SITE_TO_SITE_SPOKES = 2


class RouteType(proto.Enum):
    r"""The route's type

    Values:
        ROUTE_TYPE_UNSPECIFIED (0):
            No route type information specified
        VPC_PRIMARY_SUBNET (1):
            The route leads to a destination within the
            primary address range of the VPC network's
            subnet.
        VPC_SECONDARY_SUBNET (2):
            The route leads to a destination within the
            secondary address range of the VPC network's
            subnet.
    """
    ROUTE_TYPE_UNSPECIFIED = 0
    VPC_PRIMARY_SUBNET = 1
    VPC_SECONDARY_SUBNET = 2


class State(proto.Enum):
    r"""The State enum represents the lifecycle stage of a Network
    Connectivity Center resource.

    Values:
        STATE_UNSPECIFIED (0):
            No state information available
        CREATING (1):
            The resource's create operation is in
            progress.
        ACTIVE (2):
            The resource is active
        DELETING (3):
            The resource's delete operation is in
            progress.
        ACCEPTING (8):
            The resource's accept operation is in
            progress.
        REJECTING (9):
            The resource's reject operation is in
            progress.
        UPDATING (6):
            The resource's update operation is in
            progress.
        INACTIVE (7):
            The resource is inactive.
        OBSOLETE (10):
            The hub associated with this spoke resource
            has been deleted. This state applies to spoke
            resources only.
    """
    STATE_UNSPECIFIED = 0
    CREATING = 1
    ACTIVE = 2
    DELETING = 3
    ACCEPTING = 8
    REJECTING = 9
    UPDATING = 6
    INACTIVE = 7
    OBSOLETE = 10


class SpokeType(proto.Enum):
    r"""The SpokeType enum represents the type of spoke. The type
    reflects the kind of resource that a spoke is associated with.

    Values:
        SPOKE_TYPE_UNSPECIFIED (0):
            Unspecified spoke type.
        VPN_TUNNEL (1):
            Spokes associated with VPN tunnels.
        INTERCONNECT_ATTACHMENT (2):
            Spokes associated with VLAN attachments.
        ROUTER_APPLIANCE (3):
            Spokes associated with router appliance
            instances.
        VPC_NETWORK (4):
            Spokes associated with VPC networks.
    """
    SPOKE_TYPE_UNSPECIFIED = 0
    VPN_TUNNEL = 1
    INTERCONNECT_ATTACHMENT = 2
    ROUTER_APPLIANCE = 3
    VPC_NETWORK = 4


class Hub(proto.Message):
    r"""A Network Connectivity Center hub is a global management
    resource to which you attach spokes. A single hub can contain
    spokes from multiple regions. However, if any of a hub's spokes
    use the site-to-site data transfer feature, the resources
    associated with those spokes must all be in the same VPC
    network. Spokes that do not use site-to-site data transfer can
    be associated with any VPC network in your project.

    Attributes:
        name (str):
            Immutable. The name of the hub. Hub names must be unique.
            They use the following form:
            ``projects/{project_number}/locations/global/hubs/{hub_id}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the hub was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the hub was last
            updated.
        labels (MutableMapping[str, str]):
            Optional labels in key-value pair format. For more
            information about labels, see `Requirements for
            labels <https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements>`__.
        description (str):
            An optional description of the hub.
        unique_id (str):
            Output only. The Google-generated UUID for the hub. This
            value is unique across all hub resources. If a hub is
            deleted and another with the same name is created, the new
            hub is assigned a different unique_id.
        state (google.cloud.networkconnectivity_v1.types.State):
            Output only. The current lifecycle state of
            this hub.
        routing_vpcs (MutableSequence[google.cloud.networkconnectivity_v1.types.RoutingVPC]):
            The VPC networks associated with this hub's
            spokes.
            This field is read-only. Network Connectivity
            Center automatically populates it based on the
            set of spokes attached to the hub.
        route_tables (MutableSequence[str]):
            Output only. The route tables that belong to this hub. They
            use the following form:
            ``projects/{project_number}/locations/global/hubs/{hub_id}/routeTables/{route_table_id}``

            This field is read-only. Network Connectivity Center
            automatically populates it based on the route tables nested
            under the hub.
        spoke_summary (google.cloud.networkconnectivity_v1.types.SpokeSummary):
            Output only. A summary of the spokes
            associated with a hub. The summary includes a
            count of spokes according to type and according
            to state. If any spokes are inactive, the
            summary also lists the reasons they are
            inactive, including a count for each reason.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    unique_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    state: "State" = proto.Field(
        proto.ENUM,
        number=9,
        enum="State",
    )
    routing_vpcs: MutableSequence["RoutingVPC"] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message="RoutingVPC",
    )
    route_tables: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=11,
    )
    spoke_summary: "SpokeSummary" = proto.Field(
        proto.MESSAGE,
        number=12,
        message="SpokeSummary",
    )


class RoutingVPC(proto.Message):
    r"""RoutingVPC contains information about the VPC networks
    associated with the spokes of a Network Connectivity Center hub.

    Attributes:
        uri (str):
            The URI of the VPC network.
        required_for_new_site_to_site_data_transfer_spokes (bool):
            Output only. If true, indicates that this VPC network is
            currently associated with spokes that use the data transfer
            feature (spokes where the site_to_site_data_transfer field
            is set to true). If you create new spokes that use data
            transfer, they must be associated with this VPC network. At
            most, one VPC network will have this field set to true.
    """

    uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    required_for_new_site_to_site_data_transfer_spokes: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class Spoke(proto.Message):
    r"""A Network Connectivity Center spoke represents one or more network
    connectivity resources.

    When you create a spoke, you associate it with a hub. You must also
    identify a value for exactly one of the following fields:

    -  linked_vpn_tunnels
    -  linked_interconnect_attachments
    -  linked_router_appliance_instances
    -  linked_vpc_network

    Attributes:
        name (str):
            Immutable. The name of the spoke. Spoke names must be
            unique. They use the following form:
            ``projects/{project_number}/locations/{region}/spokes/{spoke_id}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the spoke was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the spoke was last
            updated.
        labels (MutableMapping[str, str]):
            Optional labels in key-value pair format. For more
            information about labels, see `Requirements for
            labels <https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements>`__.
        description (str):
            An optional description of the spoke.
        hub (str):
            Immutable. The name of the hub that this
            spoke is attached to.
        group (str):
            Optional. The name of the group that this
            spoke is associated with.
        linked_vpn_tunnels (google.cloud.networkconnectivity_v1.types.LinkedVpnTunnels):
            VPN tunnels that are associated with the
            spoke.
        linked_interconnect_attachments (google.cloud.networkconnectivity_v1.types.LinkedInterconnectAttachments):
            VLAN attachments that are associated with the
            spoke.
        linked_router_appliance_instances (google.cloud.networkconnectivity_v1.types.LinkedRouterApplianceInstances):
            Router appliance instances that are
            associated with the spoke.
        linked_vpc_network (google.cloud.networkconnectivity_v1.types.LinkedVpcNetwork):
            Optional. VPC network that is associated with
            the spoke.
        unique_id (str):
            Output only. The Google-generated UUID for the spoke. This
            value is unique across all spoke resources. If a spoke is
            deleted and another with the same name is created, the new
            spoke is assigned a different ``unique_id``.
        state (google.cloud.networkconnectivity_v1.types.State):
            Output only. The current lifecycle state of
            this spoke.
        reasons (MutableSequence[google.cloud.networkconnectivity_v1.types.Spoke.StateReason]):
            Output only. The reasons for current state of the spoke.
            Only present when the spoke is in the ``INACTIVE`` state.
        spoke_type (google.cloud.networkconnectivity_v1.types.SpokeType):
            Output only. The type of resource associated
            with the spoke.
    """

    class StateReason(proto.Message):
        r"""The reason a spoke is inactive.

        Attributes:
            code (google.cloud.networkconnectivity_v1.types.Spoke.StateReason.Code):
                The code associated with this reason.
            message (str):
                Human-readable details about this reason.
            user_details (str):
                Additional information provided by the user
                in the RejectSpoke call.
        """

        class Code(proto.Enum):
            r"""The Code enum represents the various reasons a state can be
            ``INACTIVE``.

            Values:
                CODE_UNSPECIFIED (0):
                    No information available.
                PENDING_REVIEW (1):
                    The proposed spoke is pending review.
                REJECTED (2):
                    The proposed spoke has been rejected by the
                    hub administrator.
                PAUSED (3):
                    The spoke has been deactivated internally.
                FAILED (4):
                    Network Connectivity Center encountered
                    errors while accepting the spoke.
            """
            CODE_UNSPECIFIED = 0
            PENDING_REVIEW = 1
            REJECTED = 2
            PAUSED = 3
            FAILED = 4

        code: "Spoke.StateReason.Code" = proto.Field(
            proto.ENUM,
            number=1,
            enum="Spoke.StateReason.Code",
        )
        message: str = proto.Field(
            proto.STRING,
            number=2,
        )
        user_details: str = proto.Field(
            proto.STRING,
            number=3,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    hub: str = proto.Field(
        proto.STRING,
        number=6,
    )
    group: str = proto.Field(
        proto.STRING,
        number=23,
    )
    linked_vpn_tunnels: "LinkedVpnTunnels" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="LinkedVpnTunnels",
    )
    linked_interconnect_attachments: "LinkedInterconnectAttachments" = proto.Field(
        proto.MESSAGE,
        number=18,
        message="LinkedInterconnectAttachments",
    )
    linked_router_appliance_instances: "LinkedRouterApplianceInstances" = proto.Field(
        proto.MESSAGE,
        number=19,
        message="LinkedRouterApplianceInstances",
    )
    linked_vpc_network: "LinkedVpcNetwork" = proto.Field(
        proto.MESSAGE,
        number=20,
        message="LinkedVpcNetwork",
    )
    unique_id: str = proto.Field(
        proto.STRING,
        number=11,
    )
    state: "State" = proto.Field(
        proto.ENUM,
        number=15,
        enum="State",
    )
    reasons: MutableSequence[StateReason] = proto.RepeatedField(
        proto.MESSAGE,
        number=21,
        message=StateReason,
    )
    spoke_type: "SpokeType" = proto.Field(
        proto.ENUM,
        number=22,
        enum="SpokeType",
    )


class RouteTable(proto.Message):
    r"""

    Attributes:
        name (str):
            Immutable. The name of the route table. Route table names
            must be unique. They use the following form:
            ``projects/{project_number}/locations/global/hubs/{hub}/routeTables/{route_table_id}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the route table was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the route table was
            last updated.
        labels (MutableMapping[str, str]):
            Optional labels in key-value pair format. For more
            information about labels, see `Requirements for
            labels <https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements>`__.
        description (str):
            An optional description of the route table.
        uid (str):
            Output only. The Google-generated UUID for the route table.
            This value is unique across all route table resources. If a
            route table is deleted and another with the same name is
            created, the new route table is assigned a different
            ``uid``.
        state (google.cloud.networkconnectivity_v1.types.State):
            Output only. The current lifecycle state of
            this route table.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=6,
    )
    state: "State" = proto.Field(
        proto.ENUM,
        number=7,
        enum="State",
    )


class Route(proto.Message):
    r"""A route defines a path from VM instances within a spoke to a
    specific destination resource. Only VPC spokes have routes.

    Attributes:
        name (str):
            Immutable. The name of the route. Route names must be
            unique. Route names use the following form:
            ``projects/{project_number}/locations/global/hubs/{hub}/routeTables/{route_table_id}/routes/{route_id}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the route was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the route was last
            updated.
        ip_cidr_range (str):
            The destination IP address range.
        type_ (google.cloud.networkconnectivity_v1.types.RouteType):
            Output only. The route's type. Its type is
            determined by the properties of its IP address
            range.
        next_hop_vpc_network (google.cloud.networkconnectivity_v1.types.NextHopVpcNetwork):
            Immutable. The destination VPC network for
            packets on this route.
        labels (MutableMapping[str, str]):
            Optional labels in key-value pair format. For more
            information about labels, see `Requirements for
            labels <https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements>`__.
        description (str):
            An optional description of the route.
        uid (str):
            Output only. The Google-generated UUID for the route. This
            value is unique across all Network Connectivity Center route
            resources. If a route is deleted and another with the same
            name is created, the new route is assigned a different
            ``uid``.
        state (google.cloud.networkconnectivity_v1.types.State):
            Output only. The current lifecycle state of
            the route.
        spoke (str):
            Immutable. The spoke that this route leads
            to. Example:
            projects/12345/locations/global/spokes/SPOKE
        location (str):
            Output only. The location of the route.
            Uses the following form:
            "projects/{project}/locations/{location}"
            Example: projects/1234/locations/us-central1
    """

    name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    ip_cidr_range: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: "RouteType" = proto.Field(
        proto.ENUM,
        number=10,
        enum="RouteType",
    )
    next_hop_vpc_network: "NextHopVpcNetwork" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="NextHopVpcNetwork",
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    description: str = proto.Field(
        proto.STRING,
        number=7,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=8,
    )
    state: "State" = proto.Field(
        proto.ENUM,
        number=9,
        enum="State",
    )
    spoke: str = proto.Field(
        proto.STRING,
        number=11,
    )
    location: str = proto.Field(
        proto.STRING,
        number=12,
    )


class Group(proto.Message):
    r"""A group represents a subset of spokes attached to a hub.

    Attributes:
        name (str):
            Immutable. The name of the group. Group names must be
            unique. They use the following form:
            ``projects/{project_number}/locations/global/hubs/{hub}/groups/{group_id}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the group was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the group was last
            updated.
        labels (MutableMapping[str, str]):
            Optional. Labels in key-value pair format. For more
            information about labels, see `Requirements for
            labels <https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements>`__.
        description (str):
            Optional. The description of the group.
        uid (str):
            Output only. The Google-generated UUID for the group. This
            value is unique across all group resources. If a group is
            deleted and another with the same name is created, the new
            route table is assigned a different unique_id.
        state (google.cloud.networkconnectivity_v1.types.State):
            Output only. The current lifecycle state of
            this group.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=6,
    )
    state: "State" = proto.Field(
        proto.ENUM,
        number=7,
        enum="State",
    )


class ListHubsRequest(proto.Message):
    r"""Request for
    [HubService.ListHubs][google.cloud.networkconnectivity.v1.HubService.ListHubs]
    method.

    Attributes:
        parent (str):
            Required. The parent resource's name.
        page_size (int):
            The maximum number of results per page to
            return.
        page_token (str):
            The page token.
        filter (str):
            An expression that filters the list of
            results.
        order_by (str):
            Sort the results by a certain order.
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


class ListHubsResponse(proto.Message):
    r"""Response for
    [HubService.ListHubs][google.cloud.networkconnectivity.v1.HubService.ListHubs]
    method.

    Attributes:
        hubs (MutableSequence[google.cloud.networkconnectivity_v1.types.Hub]):
            The requested hubs.
        next_page_token (str):
            The token for the next page of the response. To see more
            results, use this value as the page_token for your next
            request. If this value is empty, there are no more results.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    hubs: MutableSequence["Hub"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Hub",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetHubRequest(proto.Message):
    r"""Request for
    [HubService.GetHub][google.cloud.networkconnectivity.v1.HubService.GetHub]
    method.

    Attributes:
        name (str):
            Required. The name of the hub resource to
            get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateHubRequest(proto.Message):
    r"""Request for
    [HubService.CreateHub][google.cloud.networkconnectivity.v1.HubService.CreateHub]
    method.

    Attributes:
        parent (str):
            Required. The parent resource.
        hub_id (str):
            Required. A unique identifier for the hub.
        hub (google.cloud.networkconnectivity_v1.types.Hub):
            Required. The initial values for a new hub.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server knows to ignore
            the request if it has already been completed.
            The server guarantees that a request doesn't
            result in creation of duplicate commitments for
            at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check to see whether the
            original operation was received. If it was, the
            server ignores the second request. This behavior
            prevents clients from mistakenly creating
            duplicate commitments.

            The request ID must be a valid UUID, with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    hub_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    hub: "Hub" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Hub",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateHubRequest(proto.Message):
    r"""Request for
    [HubService.UpdateHub][google.cloud.networkconnectivity.v1.HubService.UpdateHub]
    method.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. In the case of an update to an existing hub, field
            mask is used to specify the fields to be overwritten. The
            fields specified in the update_mask are relative to the
            resource, not the full request. A field is overwritten if it
            is in the mask. If the user does not provide a mask, then
            all fields are overwritten.
        hub (google.cloud.networkconnectivity_v1.types.Hub):
            Required. The state that the hub should be in
            after the update.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server knows to ignore
            the request if it has already been completed.
            The server guarantees that a request doesn't
            result in creation of duplicate commitments for
            at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check to see whether the
            original operation was received. If it was, the
            server ignores the second request. This behavior
            prevents clients from mistakenly creating
            duplicate commitments.

            The request ID must be a valid UUID, with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    hub: "Hub" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Hub",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteHubRequest(proto.Message):
    r"""The request for
    [HubService.DeleteHub][google.cloud.networkconnectivity.v1.HubService.DeleteHub].

    Attributes:
        name (str):
            Required. The name of the hub to delete.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server knows to ignore
            the request if it has already been completed.
            The server guarantees that a request doesn't
            result in creation of duplicate commitments for
            at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check to see whether the
            original operation was received. If it was, the
            server ignores the second request. This behavior
            prevents clients from mistakenly creating
            duplicate commitments.

            The request ID must be a valid UUID, with the
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


class ListHubSpokesRequest(proto.Message):
    r"""The request for
    [HubService.ListHubSpokes][google.cloud.networkconnectivity.v1.HubService.ListHubSpokes].

    Attributes:
        name (str):
            Required. The name of the hub.
        spoke_locations (MutableSequence[str]):
            A list of locations. Specify one of the following:
            ``[global]``, a single region (for example,
            ``[us-central1]``), or a combination of values (for example,
            ``[global, us-central1, us-west1]``). If the spoke_locations
            field is populated, the list of results includes only spokes
            in the specified location. If the spoke_locations field is
            not populated, the list of results includes spokes in all
            locations.
        page_size (int):
            The maximum number of results to return per
            page.
        page_token (str):
            The page token.
        filter (str):
            An expression that filters the list of
            results.
        order_by (str):
            Sort the results by name or create_time.
        view (google.cloud.networkconnectivity_v1.types.ListHubSpokesRequest.SpokeView):
            The view of the spoke to return.
            The view that you use determines which spoke
            fields are included in the response.
    """

    class SpokeView(proto.Enum):
        r"""Enum that controls which spoke fields are included in the
        response.

        Values:
            SPOKE_VIEW_UNSPECIFIED (0):
                The spoke view is unspecified. When the spoke view is
                unspecified, the API returns the same fields as the
                ``BASIC`` view.
            BASIC (1):
                Includes ``name``, ``create_time``, ``hub``, ``unique_id``,
                ``state``, ``reasons``, and ``spoke_type``. This is the
                default value.
            DETAILED (2):
                Includes all spoke fields except ``labels``. You can use the
                ``DETAILED`` view only when you set the ``spoke_locations``
                field to ``[global]``.
        """
        SPOKE_VIEW_UNSPECIFIED = 0
        BASIC = 1
        DETAILED = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    spoke_locations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=5,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=6,
    )
    view: SpokeView = proto.Field(
        proto.ENUM,
        number=7,
        enum=SpokeView,
    )


class ListHubSpokesResponse(proto.Message):
    r"""The response for
    [HubService.ListHubSpokes][google.cloud.networkconnectivity.v1.HubService.ListHubSpokes].

    Attributes:
        spokes (MutableSequence[google.cloud.networkconnectivity_v1.types.Spoke]):
            The requested spokes. The spoke fields can be partially
            populated based on the ``view`` field in the request
            message.
        next_page_token (str):
            The token for the next page of the response. To see more
            results, use this value as the page_token for your next
            request. If this value is empty, there are no more results.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    spokes: MutableSequence["Spoke"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Spoke",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class ListSpokesRequest(proto.Message):
    r"""The request for
    [HubService.ListSpokes][google.cloud.networkconnectivity.v1.HubService.ListSpokes].

    Attributes:
        parent (str):
            Required. The parent resource.
        page_size (int):
            The maximum number of results to return per
            page.
        page_token (str):
            The page token.
        filter (str):
            An expression that filters the list of
            results.
        order_by (str):
            Sort the results by a certain order.
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


class ListSpokesResponse(proto.Message):
    r"""The response for
    [HubService.ListSpokes][google.cloud.networkconnectivity.v1.HubService.ListSpokes].

    Attributes:
        spokes (MutableSequence[google.cloud.networkconnectivity_v1.types.Spoke]):
            The requested spokes.
        next_page_token (str):
            The token for the next page of the response. To see more
            results, use this value as the page_token for your next
            request. If this value is empty, there are no more results.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    spokes: MutableSequence["Spoke"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Spoke",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetSpokeRequest(proto.Message):
    r"""The request for
    [HubService.GetSpoke][google.cloud.networkconnectivity.v1.HubService.GetSpoke].

    Attributes:
        name (str):
            Required. The name of the spoke resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateSpokeRequest(proto.Message):
    r"""The request for
    [HubService.CreateSpoke][google.cloud.networkconnectivity.v1.HubService.CreateSpoke].

    Attributes:
        parent (str):
            Required. The parent resource.
        spoke_id (str):
            Required. Unique id for the spoke to create.
        spoke (google.cloud.networkconnectivity_v1.types.Spoke):
            Required. The initial values for a new spoke.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server knows to ignore
            the request if it has already been completed.
            The server guarantees that a request doesn't
            result in creation of duplicate commitments for
            at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check to see whether the
            original operation was received. If it was, the
            server ignores the second request. This behavior
            prevents clients from mistakenly creating
            duplicate commitments.

            The request ID must be a valid UUID, with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    spoke_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    spoke: "Spoke" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Spoke",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateSpokeRequest(proto.Message):
    r"""Request for
    [HubService.UpdateSpoke][google.cloud.networkconnectivity.v1.HubService.UpdateSpoke]
    method.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. In the case of an update to an existing spoke,
            field mask is used to specify the fields to be overwritten.
            The fields specified in the update_mask are relative to the
            resource, not the full request. A field is overwritten if it
            is in the mask. If the user does not provide a mask, then
            all fields are overwritten.
        spoke (google.cloud.networkconnectivity_v1.types.Spoke):
            Required. The state that the spoke should be
            in after the update.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server knows to ignore
            the request if it has already been completed.
            The server guarantees that a request doesn't
            result in creation of duplicate commitments for
            at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check to see whether the
            original operation was received. If it was, the
            server ignores the second request. This behavior
            prevents clients from mistakenly creating
            duplicate commitments.

            The request ID must be a valid UUID, with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    spoke: "Spoke" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Spoke",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteSpokeRequest(proto.Message):
    r"""The request for
    [HubService.DeleteSpoke][google.cloud.networkconnectivity.v1.HubService.DeleteSpoke].

    Attributes:
        name (str):
            Required. The name of the spoke to delete.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server knows to ignore
            the request if it has already been completed.
            The server guarantees that a request doesn't
            result in creation of duplicate commitments for
            at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check to see whether the
            original operation was received. If it was, the
            server ignores the second request. This behavior
            prevents clients from mistakenly creating
            duplicate commitments.

            The request ID must be a valid UUID, with the
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


class AcceptHubSpokeRequest(proto.Message):
    r"""The request for
    [HubService.AcceptHubSpoke][google.cloud.networkconnectivity.v1.HubService.AcceptHubSpoke].

    Attributes:
        name (str):
            Required. The name of the hub into which to
            accept the spoke.
        spoke_uri (str):
            Required. The URI of the spoke to accept into
            the hub.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server knows to ignore
            the request if it has already been completed.
            The server guarantees that a request doesn't
            result in creation of duplicate commitments for
            at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check to see whether the
            original operation was received. If it was, the
            server ignores the second request. This behavior
            prevents clients from mistakenly creating
            duplicate commitments.

            The request ID must be a valid UUID, with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    spoke_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class AcceptHubSpokeResponse(proto.Message):
    r"""The response for
    [HubService.AcceptHubSpoke][google.cloud.networkconnectivity.v1.HubService.AcceptHubSpoke].

    Attributes:
        spoke (google.cloud.networkconnectivity_v1.types.Spoke):
            The spoke that was operated on.
    """

    spoke: "Spoke" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Spoke",
    )


class RejectHubSpokeRequest(proto.Message):
    r"""The request for
    [HubService.RejectHubSpoke][google.cloud.networkconnectivity.v1.HubService.RejectHubSpoke].

    Attributes:
        name (str):
            Required. The name of the hub from which to
            reject the spoke.
        spoke_uri (str):
            Required. The URI of the spoke to reject from
            the hub.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server knows to ignore
            the request if it has already been completed.
            The server guarantees that a request doesn't
            result in creation of duplicate commitments for
            at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check to see whether the
            original operation was received. If it was, the
            server ignores the second request. This behavior
            prevents clients from mistakenly creating
            duplicate commitments.

            The request ID must be a valid UUID, with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        details (str):
            Optional. Additional information provided by
            the hub administrator.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    spoke_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    details: str = proto.Field(
        proto.STRING,
        number=4,
    )


class RejectHubSpokeResponse(proto.Message):
    r"""The response for
    [HubService.RejectHubSpoke][google.cloud.networkconnectivity.v1.HubService.RejectHubSpoke].

    Attributes:
        spoke (google.cloud.networkconnectivity_v1.types.Spoke):
            The spoke that was operated on.
    """

    spoke: "Spoke" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Spoke",
    )


class GetRouteTableRequest(proto.Message):
    r"""The request for
    [HubService.GetRouteTable][google.cloud.networkconnectivity.v1.HubService.GetRouteTable].

    Attributes:
        name (str):
            Required. The name of the route table
            resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetRouteRequest(proto.Message):
    r"""The request for
    [HubService.GetRoute][google.cloud.networkconnectivity.v1.HubService.GetRoute].

    Attributes:
        name (str):
            Required. The name of the route resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListRoutesRequest(proto.Message):
    r"""Request for
    [HubService.ListRoutes][google.cloud.networkconnectivity.v1.HubService.ListRoutes]
    method.

    Attributes:
        parent (str):
            Required. The parent resource's name.
        page_size (int):
            The maximum number of results to return per
            page.
        page_token (str):
            The page token.
        filter (str):
            An expression that filters the list of
            results.
        order_by (str):
            Sort the results by a certain order.
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


class ListRoutesResponse(proto.Message):
    r"""Response for
    [HubService.ListRoutes][google.cloud.networkconnectivity.v1.HubService.ListRoutes]
    method.

    Attributes:
        routes (MutableSequence[google.cloud.networkconnectivity_v1.types.Route]):
            The requested routes.
        next_page_token (str):
            The token for the next page of the response. To see more
            results, use this value as the page_token for your next
            request. If this value is empty, there are no more results.
        unreachable (MutableSequence[str]):
            RouteTables that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    routes: MutableSequence["Route"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Route",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class ListRouteTablesRequest(proto.Message):
    r"""Request for
    [HubService.ListRouteTables][google.cloud.networkconnectivity.v1.HubService.ListRouteTables]
    method.

    Attributes:
        parent (str):
            Required. The parent resource's name.
        page_size (int):
            The maximum number of results to return per
            page.
        page_token (str):
            The page token.
        filter (str):
            An expression that filters the list of
            results.
        order_by (str):
            Sort the results by a certain order.
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


class ListRouteTablesResponse(proto.Message):
    r"""Response for
    [HubService.ListRouteTables][google.cloud.networkconnectivity.v1.HubService.ListRouteTables]
    method.

    Attributes:
        route_tables (MutableSequence[google.cloud.networkconnectivity_v1.types.RouteTable]):
            The requested route tables.
        next_page_token (str):
            The token for the next page of the response. To see more
            results, use this value as the page_token for your next
            request. If this value is empty, there are no more results.
        unreachable (MutableSequence[str]):
            Hubs that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    route_tables: MutableSequence["RouteTable"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="RouteTable",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class ListGroupsRequest(proto.Message):
    r"""Request for
    [HubService.ListGroups][google.cloud.networkconnectivity.v1.HubService.ListGroups]
    method.

    Attributes:
        parent (str):
            Required. The parent resource's name.
        page_size (int):
            The maximum number of results to return per
            page.
        page_token (str):
            The page token.
        filter (str):
            An expression that filters the list of
            results.
        order_by (str):
            Sort the results by a certain order.
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


class ListGroupsResponse(proto.Message):
    r"""Response for
    [HubService.ListGroups][google.cloud.networkconnectivity.v1.HubService.ListGroups]
    method.

    Attributes:
        groups (MutableSequence[google.cloud.networkconnectivity_v1.types.Group]):
            The requested groups.
        next_page_token (str):
            The token for the next page of the response. To see more
            results, use this value as the page_token for your next
            request. If this value is empty, there are no more results.
        unreachable (MutableSequence[str]):
            Hubs that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    groups: MutableSequence["Group"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Group",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class LinkedVpnTunnels(proto.Message):
    r"""A collection of Cloud VPN tunnel resources. These resources
    should be redundant HA VPN tunnels that all advertise the same
    prefixes to Google Cloud. Alternatively, in a passive/active
    configuration, all tunnels should be capable of advertising the
    same prefixes.

    Attributes:
        uris (MutableSequence[str]):
            The URIs of linked VPN tunnel resources.
        site_to_site_data_transfer (bool):
            A value that controls whether site-to-site data transfer is
            enabled for these resources. Data transfer is available only
            in `supported
            locations <https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/locations>`__.
        vpc_network (str):
            Output only. The VPC network where these VPN
            tunnels are located.
    """

    uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    site_to_site_data_transfer: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    vpc_network: str = proto.Field(
        proto.STRING,
        number=3,
    )


class LinkedInterconnectAttachments(proto.Message):
    r"""A collection of VLAN attachment resources. These resources
    should be redundant attachments that all advertise the same
    prefixes to Google Cloud. Alternatively, in active/passive
    configurations, all attachments should be capable of advertising
    the same prefixes.

    Attributes:
        uris (MutableSequence[str]):
            The URIs of linked interconnect attachment
            resources
        site_to_site_data_transfer (bool):
            A value that controls whether site-to-site data transfer is
            enabled for these resources. Data transfer is available only
            in `supported
            locations <https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/locations>`__.
        vpc_network (str):
            Output only. The VPC network where these VLAN
            attachments are located.
    """

    uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    site_to_site_data_transfer: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    vpc_network: str = proto.Field(
        proto.STRING,
        number=3,
    )


class LinkedRouterApplianceInstances(proto.Message):
    r"""A collection of router appliance instances. If you configure
    multiple router appliance instances to receive data from the
    same set of sites outside of Google Cloud, we recommend that you
    associate those instances with the same spoke.

    Attributes:
        instances (MutableSequence[google.cloud.networkconnectivity_v1.types.RouterApplianceInstance]):
            The list of router appliance instances.
        site_to_site_data_transfer (bool):
            A value that controls whether site-to-site data transfer is
            enabled for these resources. Data transfer is available only
            in `supported
            locations <https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/locations>`__.
        vpc_network (str):
            Output only. The VPC network where these
            router appliance instances are located.
    """

    instances: MutableSequence["RouterApplianceInstance"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="RouterApplianceInstance",
    )
    site_to_site_data_transfer: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    vpc_network: str = proto.Field(
        proto.STRING,
        number=3,
    )


class LinkedVpcNetwork(proto.Message):
    r"""An existing VPC network.

    Attributes:
        uri (str):
            Required. The URI of the VPC network
            resource.
        exclude_export_ranges (MutableSequence[str]):
            Optional. IP ranges encompassing the subnets
            to be excluded from peering.
    """

    uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    exclude_export_ranges: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class RouterApplianceInstance(proto.Message):
    r"""A router appliance instance is a Compute Engine virtual
    machine (VM) instance that acts as a BGP speaker. A router
    appliance instance is specified by the URI of the VM and the
    internal IP address of one of the VM's network interfaces.

    Attributes:
        virtual_machine (str):
            The URI of the VM.
        ip_address (str):
            The IP address on the VM to use for peering.
    """

    virtual_machine: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ip_address: str = proto.Field(
        proto.STRING,
        number=3,
    )


class LocationMetadata(proto.Message):
    r"""Metadata about locations

    Attributes:
        location_features (MutableSequence[google.cloud.networkconnectivity_v1.types.LocationFeature]):
            List of supported features
    """

    location_features: MutableSequence["LocationFeature"] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum="LocationFeature",
    )


class NextHopVpcNetwork(proto.Message):
    r"""

    Attributes:
        uri (str):
            The URI of the VPC network resource
    """

    uri: str = proto.Field(
        proto.STRING,
        number=1,
    )


class SpokeSummary(proto.Message):
    r"""Summarizes information about the spokes associated with a
    hub. The summary includes a count of spokes according to type
    and according to state. If any spokes are inactive, the summary
    also lists the reasons they are inactive, including a count for
    each reason.

    Attributes:
        spoke_type_counts (MutableSequence[google.cloud.networkconnectivity_v1.types.SpokeSummary.SpokeTypeCount]):
            Output only. Counts the number of spokes of
            each type that are associated with a specific
            hub.
        spoke_state_counts (MutableSequence[google.cloud.networkconnectivity_v1.types.SpokeSummary.SpokeStateCount]):
            Output only. Counts the number of spokes that
            are in each state and associated with a given
            hub.
        spoke_state_reason_counts (MutableSequence[google.cloud.networkconnectivity_v1.types.SpokeSummary.SpokeStateReasonCount]):
            Output only. Counts the number of spokes that
            are inactive for each possible reason and
            associated with a given hub.
    """

    class SpokeTypeCount(proto.Message):
        r"""The number of spokes of a given type that are associated
        with a specific hub. The type indicates what kind of resource is
        associated with the spoke.

        Attributes:
            spoke_type (google.cloud.networkconnectivity_v1.types.SpokeType):
                Output only. The type of the spokes.
            count (int):
                Output only. The total number of spokes of
                this type that are associated with the hub.
        """

        spoke_type: "SpokeType" = proto.Field(
            proto.ENUM,
            number=1,
            enum="SpokeType",
        )
        count: int = proto.Field(
            proto.INT64,
            number=2,
        )

    class SpokeStateCount(proto.Message):
        r"""The number of spokes that are in a particular state
        and associated with a given hub.

        Attributes:
            state (google.cloud.networkconnectivity_v1.types.State):
                Output only. The state of the spokes.
            count (int):
                Output only. The total number of spokes that
                are in this state and associated with a given
                hub.
        """

        state: "State" = proto.Field(
            proto.ENUM,
            number=1,
            enum="State",
        )
        count: int = proto.Field(
            proto.INT64,
            number=2,
        )

    class SpokeStateReasonCount(proto.Message):
        r"""The number of spokes in the hub that are inactive for this
        reason.

        Attributes:
            state_reason_code (google.cloud.networkconnectivity_v1.types.Spoke.StateReason.Code):
                Output only. The reason that a spoke is
                inactive.
            count (int):
                Output only. The total number of spokes that
                are inactive for a particular reason and
                associated with a given hub.
        """

        state_reason_code: "Spoke.StateReason.Code" = proto.Field(
            proto.ENUM,
            number=1,
            enum="Spoke.StateReason.Code",
        )
        count: int = proto.Field(
            proto.INT64,
            number=2,
        )

    spoke_type_counts: MutableSequence[SpokeTypeCount] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=SpokeTypeCount,
    )
    spoke_state_counts: MutableSequence[SpokeStateCount] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=SpokeStateCount,
    )
    spoke_state_reason_counts: MutableSequence[
        SpokeStateReasonCount
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=SpokeStateReasonCount,
    )


class GetGroupRequest(proto.Message):
    r"""The request for
    [HubService.GetGroup][google.cloud.networkconnectivity.v1.HubService.GetGroup].

    Attributes:
        name (str):
            Required. The name of the route table
            resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
