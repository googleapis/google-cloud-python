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
    package="google.cloud.networkconnectivity.v1",
    manifest={
        "State",
        "LocationFeature",
        "Hub",
        "RoutingVPC",
        "Spoke",
        "ListHubsRequest",
        "ListHubsResponse",
        "GetHubRequest",
        "CreateHubRequest",
        "UpdateHubRequest",
        "DeleteHubRequest",
        "ListSpokesRequest",
        "ListSpokesResponse",
        "GetSpokeRequest",
        "CreateSpokeRequest",
        "UpdateSpokeRequest",
        "DeleteSpokeRequest",
        "LinkedVpnTunnels",
        "LinkedInterconnectAttachments",
        "LinkedRouterApplianceInstances",
        "RouterApplianceInstance",
        "LocationMetadata",
    },
)


class State(proto.Enum):
    r"""The State enum represents the lifecycle stage of a Network
    Connectivity Center resource.
    """
    STATE_UNSPECIFIED = 0
    CREATING = 1
    ACTIVE = 2
    DELETING = 3


class LocationFeature(proto.Enum):
    r"""Supported features for a location"""
    LOCATION_FEATURE_UNSPECIFIED = 0
    SITE_TO_CLOUD_SPOKES = 1
    SITE_TO_SITE_SPOKES = 2


class Hub(proto.Message):
    r"""A hub is a collection of spokes. A single hub can contain
    spokes from multiple regions. However, if any of a hub's spokes
    use the data transfer feature, the resources associated with
    those spokes must all reside in the same VPC network. Spokes
    that do not use data transfer can be associated with any VPC
    network in your project.

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
        labels (Sequence[google.cloud.networkconnectivity_v1.types.Hub.LabelsEntry]):
            Optional labels in key:value format. For more information
            about labels, see `Requirements for
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
        routing_vpcs (Sequence[google.cloud.networkconnectivity_v1.types.RoutingVPC]):
            The VPC networks associated with this hub's
            spokes.
            This field is read-only. Network Connectivity
            Center automatically populates it based on the
            set of spokes attached to the hub.
    """

    name = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=4,)
    description = proto.Field(proto.STRING, number=5,)
    unique_id = proto.Field(proto.STRING, number=8,)
    state = proto.Field(proto.ENUM, number=9, enum="State",)
    routing_vpcs = proto.RepeatedField(proto.MESSAGE, number=10, message="RoutingVPC",)


class RoutingVPC(proto.Message):
    r"""RoutingVPC contains information about the VPC networks that
    are associated with a hub's spokes.

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

    uri = proto.Field(proto.STRING, number=1,)
    required_for_new_site_to_site_data_transfer_spokes = proto.Field(
        proto.BOOL, number=2,
    )


class Spoke(proto.Message):
    r"""A spoke represents a connection between your Google Cloud network
    resources and a non-Google-Cloud network.

    When you create a spoke, you associate it with a hub. You must also
    identify a value for exactly one of the following fields:

    -  linked_vpn_tunnels
    -  linked_interconnect_attachments
    -  linked_router_appliance_instances

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
        labels (Sequence[google.cloud.networkconnectivity_v1.types.Spoke.LabelsEntry]):
            Optional labels in key:value format. For more information
            about labels, see `Requirements for
            labels <https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements>`__.
        description (str):
            An optional description of the spoke.
        hub (str):
            Immutable. The name of the hub that this
            spoke is attached to.
        linked_vpn_tunnels (google.cloud.networkconnectivity_v1.types.LinkedVpnTunnels):
            VPN tunnels that are associated with the
            spoke.
        linked_interconnect_attachments (google.cloud.networkconnectivity_v1.types.LinkedInterconnectAttachments):
            VLAN attachments that are associated with the
            spoke.
        linked_router_appliance_instances (google.cloud.networkconnectivity_v1.types.LinkedRouterApplianceInstances):
            Router appliance instances that are
            associated with the spoke.
        unique_id (str):
            Output only. The Google-generated UUID for the spoke. This
            value is unique across all spoke resources. If a spoke is
            deleted and another with the same name is created, the new
            spoke is assigned a different unique_id.
        state (google.cloud.networkconnectivity_v1.types.State):
            Output only. The current lifecycle state of
            this spoke.
    """

    name = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=4,)
    description = proto.Field(proto.STRING, number=5,)
    hub = proto.Field(proto.STRING, number=6,)
    linked_vpn_tunnels = proto.Field(
        proto.MESSAGE, number=17, message="LinkedVpnTunnels",
    )
    linked_interconnect_attachments = proto.Field(
        proto.MESSAGE, number=18, message="LinkedInterconnectAttachments",
    )
    linked_router_appliance_instances = proto.Field(
        proto.MESSAGE, number=19, message="LinkedRouterApplianceInstances",
    )
    unique_id = proto.Field(proto.STRING, number=11,)
    state = proto.Field(proto.ENUM, number=15, enum="State",)


class ListHubsRequest(proto.Message):
    r"""Request for
    [HubService.ListHubs][google.cloud.networkconnectivity.v1.HubService.ListHubs]
    method.

    Attributes:
        parent (str):
            Required. The parent resource's name.
        page_size (int):
            The maximum number of results per page that
            should be returned.
        page_token (str):
            The page token.
        filter (str):
            An expression that filters the results listed
            in the response.
        order_by (str):
            Sort the results by a certain order.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListHubsResponse(proto.Message):
    r"""Response for
    [HubService.ListHubs][google.cloud.networkconnectivity.v1.HubService.ListHubs]
    method.

    Attributes:
        hubs (Sequence[google.cloud.networkconnectivity_v1.types.Hub]):
            The requested hubs.
        next_page_token (str):
            The next pagination token in the List response. It should be
            used as page_token for the following request. An empty value
            means no more result.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    hubs = proto.RepeatedField(proto.MESSAGE, number=1, message="Hub",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetHubRequest(proto.Message):
    r"""Request for
    [HubService.GetHub][google.cloud.networkconnectivity.v1.HubService.GetHub]
    method.

    Attributes:
        name (str):
            Required. The name of the hub resource to
            get.
    """

    name = proto.Field(proto.STRING, number=1,)


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
            Optional. A unique request ID (optional). If
            you specify this ID, you can use it in cases
            when you need to retry your request. When you
            need to retry, this ID lets the server know that
            it can ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes after the first request.

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

    parent = proto.Field(proto.STRING, number=1,)
    hub_id = proto.Field(proto.STRING, number=2,)
    hub = proto.Field(proto.MESSAGE, number=3, message="Hub",)
    request_id = proto.Field(proto.STRING, number=4,)


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
            Optional. A unique request ID (optional). If
            you specify this ID, you can use it in cases
            when you need to retry your request. When you
            need to retry, this ID lets the server know that
            it can ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes after the first request.

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

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    hub = proto.Field(proto.MESSAGE, number=2, message="Hub",)
    request_id = proto.Field(proto.STRING, number=3,)


class DeleteHubRequest(proto.Message):
    r"""The request for
    [HubService.DeleteHub][google.cloud.networkconnectivity.v1.HubService.DeleteHub].

    Attributes:
        name (str):
            Required. The name of the hub to delete.
        request_id (str):
            Optional. A unique request ID (optional). If
            you specify this ID, you can use it in cases
            when you need to retry your request. When you
            need to retry, this ID lets the server know that
            it can ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes after the first request.

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

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class ListSpokesRequest(proto.Message):
    r"""The request for
    [HubService.ListSpokes][google.cloud.networkconnectivity.v1.HubService.ListSpokes].

    Attributes:
        parent (str):
            Required. The parent resource.
        page_size (int):
            The maximum number of results per page that
            should be returned.
        page_token (str):
            The page token.
        filter (str):
            An expression that filters the results listed
            in the response.
        order_by (str):
            Sort the results by a certain order.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListSpokesResponse(proto.Message):
    r"""The response for
    [HubService.ListSpokes][google.cloud.networkconnectivity.v1.HubService.ListSpokes].

    Attributes:
        spokes (Sequence[google.cloud.networkconnectivity_v1.types.Spoke]):
            The requested spokes.
        next_page_token (str):
            The next pagination token in the List response. It should be
            used as page_token for the following request. An empty value
            means no more result.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    spokes = proto.RepeatedField(proto.MESSAGE, number=1, message="Spoke",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetSpokeRequest(proto.Message):
    r"""The request for
    [HubService.GetSpoke][google.cloud.networkconnectivity.v1.HubService.GetSpoke].

    Attributes:
        name (str):
            Required. The name of the spoke resource.
    """

    name = proto.Field(proto.STRING, number=1,)


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
            Optional. A unique request ID (optional). If
            you specify this ID, you can use it in cases
            when you need to retry your request. When you
            need to retry, this ID lets the server know that
            it can ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes after the first request.

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

    parent = proto.Field(proto.STRING, number=1,)
    spoke_id = proto.Field(proto.STRING, number=2,)
    spoke = proto.Field(proto.MESSAGE, number=3, message="Spoke",)
    request_id = proto.Field(proto.STRING, number=4,)


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
            Optional. A unique request ID (optional). If
            you specify this ID, you can use it in cases
            when you need to retry your request. When you
            need to retry, this ID lets the server know that
            it can ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes after the first request.

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

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    spoke = proto.Field(proto.MESSAGE, number=2, message="Spoke",)
    request_id = proto.Field(proto.STRING, number=3,)


class DeleteSpokeRequest(proto.Message):
    r"""The request for
    [HubService.DeleteSpoke][google.cloud.networkconnectivity.v1.HubService.DeleteSpoke].

    Attributes:
        name (str):
            Required. The name of the spoke to delete.
        request_id (str):
            Optional. A unique request ID (optional). If
            you specify this ID, you can use it in cases
            when you need to retry your request. When you
            need to retry, this ID lets the server know that
            it can ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes after the first request.

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

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class LinkedVpnTunnels(proto.Message):
    r"""A collection of Cloud VPN tunnel resources. These resources
    should be redundant HA VPN tunnels that all advertise the same
    prefixes to Google Cloud. Alternatively, in a passive/active
    configuration, all tunnels should be capable of advertising the
    same prefixes.

    Attributes:
        uris (Sequence[str]):
            The URIs of linked VPN tunnel resources.
        site_to_site_data_transfer (bool):
            A value that controls whether site-to-site data transfer is
            enabled for these resources. Data transfer is available only
            in `supported
            locations <https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/locations>`__.
    """

    uris = proto.RepeatedField(proto.STRING, number=1,)
    site_to_site_data_transfer = proto.Field(proto.BOOL, number=2,)


class LinkedInterconnectAttachments(proto.Message):
    r"""A collection of VLAN attachment resources. These resources
    should be redundant attachments that all advertise the same
    prefixes to Google Cloud. Alternatively, in active/passive
    configurations, all attachments should be capable of advertising
    the same prefixes.

    Attributes:
        uris (Sequence[str]):
            The URIs of linked interconnect attachment
            resources
        site_to_site_data_transfer (bool):
            A value that controls whether site-to-site data transfer is
            enabled for these resources. Data transfer is available only
            in `supported
            locations <https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/locations>`__.
    """

    uris = proto.RepeatedField(proto.STRING, number=1,)
    site_to_site_data_transfer = proto.Field(proto.BOOL, number=2,)


class LinkedRouterApplianceInstances(proto.Message):
    r"""A collection of router appliance instances. If you configure
    multiple router appliance instances to receive data from the
    same set of sites outside of Google Cloud, we recommend that you
    associate those instances with the same spoke.

    Attributes:
        instances (Sequence[google.cloud.networkconnectivity_v1.types.RouterApplianceInstance]):
            The list of router appliance instances.
        site_to_site_data_transfer (bool):
            A value that controls whether site-to-site data transfer is
            enabled for these resources. Data transfer is available only
            in `supported
            locations <https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/locations>`__.
    """

    instances = proto.RepeatedField(
        proto.MESSAGE, number=1, message="RouterApplianceInstance",
    )
    site_to_site_data_transfer = proto.Field(proto.BOOL, number=2,)


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

    virtual_machine = proto.Field(proto.STRING, number=1,)
    ip_address = proto.Field(proto.STRING, number=3,)


class LocationMetadata(proto.Message):
    r"""Metadata about locations

    Attributes:
        location_features (Sequence[google.cloud.networkconnectivity_v1.types.LocationFeature]):
            List of supported features
    """

    location_features = proto.RepeatedField(
        proto.ENUM, number=1, enum="LocationFeature",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
