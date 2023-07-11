# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.vmwareengine.v1",
    manifest={
        "NetworkConfig",
        "NodeTypeConfig",
        "PrivateCloud",
        "Cluster",
        "Subnet",
        "NodeType",
        "Credentials",
        "HcxActivationKey",
        "Hcx",
        "Nsx",
        "Vcenter",
        "PeeringRoute",
        "NetworkPolicy",
        "VmwareEngineNetwork",
        "PrivateConnection",
    },
)


class NetworkConfig(proto.Message):
    r"""Network configuration in the consumer project
    with which the peering has to be done.

    Attributes:
        management_cidr (str):
            Required. Management CIDR used by VMware
            management appliances.
        vmware_engine_network (str):
            Optional. The relative resource name of the VMware Engine
            network attached to the private cloud. Specify the name in
            the following form:
            ``projects/{project}/locations/{location}/vmwareEngineNetworks/{vmware_engine_network_id}``
            where ``{project}`` can either be a project number or a
            project ID.
        vmware_engine_network_canonical (str):
            Output only. The canonical name of the VMware Engine network
            in the form:
            ``projects/{project_number}/locations/{location}/vmwareEngineNetworks/{vmware_engine_network_id}``
        management_ip_address_layout_version (int):
            Output only. The IP address layout version of the management
            IP address range. Possible versions include:

            -  ``managementIpAddressLayoutVersion=1``: Indicates the
               legacy IP address layout used by some existing private
               clouds. This is no longer supported for new private
               clouds as it does not support all features.
            -  ``managementIpAddressLayoutVersion=2``: Indicates the
               latest IP address layout used by all newly created
               private clouds. This version supports all current
               features.
    """

    management_cidr: str = proto.Field(
        proto.STRING,
        number=4,
    )
    vmware_engine_network: str = proto.Field(
        proto.STRING,
        number=5,
    )
    vmware_engine_network_canonical: str = proto.Field(
        proto.STRING,
        number=6,
    )
    management_ip_address_layout_version: int = proto.Field(
        proto.INT32,
        number=8,
    )


class NodeTypeConfig(proto.Message):
    r"""Information about the type and number of nodes associated
    with the cluster.

    Attributes:
        node_count (int):
            Required. The number of nodes of this type in
            the cluster
        custom_core_count (int):
            Optional. Customized number of cores available to each node
            of the type. This number must always be one of
            ``nodeType.availableCustomCoreCounts``. If zero is provided
            max value from ``nodeType.availableCustomCoreCounts`` will
            be used.
    """

    node_count: int = proto.Field(
        proto.INT32,
        number=1,
    )
    custom_core_count: int = proto.Field(
        proto.INT32,
        number=2,
    )


class PrivateCloud(proto.Message):
    r"""Represents a private cloud resource. Private clouds are zonal
    resources.

    Attributes:
        name (str):
            Output only. The resource name of this private cloud.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-central1-a/privateClouds/my-cloud``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of this resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update time of this
            resource.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the resource was
            scheduled for deletion.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the resource will be
            irreversibly deleted.
        state (google.cloud.vmwareengine_v1.types.PrivateCloud.State):
            Output only. State of the resource. New
            values may be added to this enum when
            appropriate.
        network_config (google.cloud.vmwareengine_v1.types.NetworkConfig):
            Required. Network configuration of the
            private cloud.
        management_cluster (google.cloud.vmwareengine_v1.types.PrivateCloud.ManagementCluster):
            Required. Input only. The management cluster for this
            private cloud. This field is required during creation of the
            private cloud to provide details for the default cluster.

            The following fields can't be changed after private cloud
            creation: ``ManagementCluster.clusterId``,
            ``ManagementCluster.nodeTypeId``.
        description (str):
            User-provided description for this private
            cloud.
        hcx (google.cloud.vmwareengine_v1.types.Hcx):
            Output only. HCX appliance.
        nsx (google.cloud.vmwareengine_v1.types.Nsx):
            Output only. NSX appliance.
        vcenter (google.cloud.vmwareengine_v1.types.Vcenter):
            Output only. Vcenter appliance.
        uid (str):
            Output only. System-generated unique
            identifier for the resource.
        type_ (google.cloud.vmwareengine_v1.types.PrivateCloud.Type):
            Optional. Type of the private cloud. Defaults
            to STANDARD.
    """

    class State(proto.Enum):
        r"""Enum State defines possible states of private clouds.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value should never be
                used.
            ACTIVE (1):
                The private cloud is ready.
            CREATING (2):
                The private cloud is being created.
            UPDATING (3):
                The private cloud is being updated.
            FAILED (5):
                The private cloud is in failed state.
            DELETED (6):
                The private cloud is scheduled for deletion.
                The deletion process can be cancelled by using
                the corresponding undelete method.
            PURGING (7):
                The private cloud is irreversibly deleted and
                is being removed from the system.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2
        UPDATING = 3
        FAILED = 5
        DELETED = 6
        PURGING = 7

    class Type(proto.Enum):
        r"""Enum Type defines private cloud type.

        Values:
            STANDARD (0):
                Standard private is a zonal resource, with 3+
                nodes. Default type.
            TIME_LIMITED (1):
                Time limited private cloud is a zonal
                resource, can have only 1 node and has limited
                life span. Will be deleted after defined period
                of time, can be converted into standard private
                cloud by expanding it up to 3 or more nodes.
        """
        STANDARD = 0
        TIME_LIMITED = 1

    class ManagementCluster(proto.Message):
        r"""Management cluster configuration.

        Attributes:
            cluster_id (str):
                Required. The user-provided identifier of the new
                ``Cluster``. The identifier must meet the following
                requirements:

                -  Only contains 1-63 alphanumeric characters and hyphens
                -  Begins with an alphabetical character
                -  Ends with a non-hyphen character
                -  Not formatted as a UUID
                -  Complies with `RFC
                   1034 <https://datatracker.ietf.org/doc/html/rfc1034>`__
                   (section 3.5)
            node_type_configs (MutableMapping[str, google.cloud.vmwareengine_v1.types.NodeTypeConfig]):
                Required. The map of cluster node types in this cluster,
                where the key is canonical identifier of the node type
                (corresponds to the ``NodeType``).
        """

        cluster_id: str = proto.Field(
            proto.STRING,
            number=1,
        )
        node_type_configs: MutableMapping[str, "NodeTypeConfig"] = proto.MapField(
            proto.STRING,
            proto.MESSAGE,
            number=7,
            message="NodeTypeConfig",
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
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    expire_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=8,
        enum=State,
    )
    network_config: "NetworkConfig" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="NetworkConfig",
    )
    management_cluster: ManagementCluster = proto.Field(
        proto.MESSAGE,
        number=10,
        message=ManagementCluster,
    )
    description: str = proto.Field(
        proto.STRING,
        number=11,
    )
    hcx: "Hcx" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="Hcx",
    )
    nsx: "Nsx" = proto.Field(
        proto.MESSAGE,
        number=18,
        message="Nsx",
    )
    vcenter: "Vcenter" = proto.Field(
        proto.MESSAGE,
        number=19,
        message="Vcenter",
    )
    uid: str = proto.Field(
        proto.STRING,
        number=20,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=22,
        enum=Type,
    )


class Cluster(proto.Message):
    r"""A cluster in a private cloud.

    Attributes:
        name (str):
            Output only. The resource name of this cluster. Resource
            names are schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-central1-a/privateClouds/my-cloud/clusters/my-cluster``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of this resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update time of this
            resource.
        state (google.cloud.vmwareengine_v1.types.Cluster.State):
            Output only. State of the resource.
        management (bool):
            Output only. True if the cluster is a
            management cluster; false otherwise. There can
            only be one management cluster in a private
            cloud and it has to be the first one.
        uid (str):
            Output only. System-generated unique
            identifier for the resource.
        node_type_configs (MutableMapping[str, google.cloud.vmwareengine_v1.types.NodeTypeConfig]):
            Required. The map of cluster node types in this cluster,
            where the key is canonical identifier of the node type
            (corresponds to the ``NodeType``).
    """

    class State(proto.Enum):
        r"""Enum State defines possible states of private cloud clusters.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value should never be
                used.
            ACTIVE (1):
                The Cluster is operational and can be used by
                the user.
            CREATING (2):
                The Cluster is being deployed.
            UPDATING (3):
                Adding or removing of a node to the cluster,
                any other cluster specific updates.
            DELETING (4):
                The Cluster is being deleted.
            REPAIRING (5):
                The Cluster is undergoing maintenance, for
                example: a failed node is
                getting replaced.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2
        UPDATING = 3
        DELETING = 4
        REPAIRING = 5

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
    state: State = proto.Field(
        proto.ENUM,
        number=6,
        enum=State,
    )
    management: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=14,
    )
    node_type_configs: MutableMapping[str, "NodeTypeConfig"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=16,
        message="NodeTypeConfig",
    )


class Subnet(proto.Message):
    r"""Subnet in a private cloud. Either ``management`` subnets (such as
    vMotion) that are read-only, or ``userDefined``, which can also be
    updated.

    Attributes:
        name (str):
            Output only. The resource name of this subnet. Resource
            names are schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-central1-a/privateClouds/my-cloud/subnets/my-subnet``
        ip_cidr_range (str):
            The IP address range of the subnet in CIDR
            format '10.0.0.0/24'.
        gateway_ip (str):
            The IP address of the gateway of this subnet.
            Must fall within the IP prefix defined above.
        type_ (str):
            Output only. The type of the subnet. For
            example "management" or "userDefined".
        state (google.cloud.vmwareengine_v1.types.Subnet.State):
            Output only. The state of the resource.
    """

    class State(proto.Enum):
        r"""Defines possible states of subnets.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value should never be
                used.
            ACTIVE (1):
                The subnet is ready.
            CREATING (2):
                The subnet is being created.
            UPDATING (3):
                The subnet is being updated.
            DELETING (4):
                The subnet is being deleted.
            RECONCILING (5):
                Changes requested in the last operation are
                being propagated.
            FAILED (6):
                Last operation on the subnet did not succeed.
                Subnet's payload is reverted back to its most
                recent working state.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2
        UPDATING = 3
        DELETING = 4
        RECONCILING = 5
        FAILED = 6

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ip_cidr_range: str = proto.Field(
        proto.STRING,
        number=7,
    )
    gateway_ip: str = proto.Field(
        proto.STRING,
        number=8,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=11,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=13,
        enum=State,
    )


class NodeType(proto.Message):
    r"""Describes node type.

    Attributes:
        name (str):
            Output only. The resource name of this node type. Resource
            names are schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-proj/locations/us-central1-a/nodeTypes/standard-72``
        node_type_id (str):
            Output only. The canonical identifier of the node type
            (corresponds to the ``NodeType``). For example: standard-72.
        display_name (str):
            Output only. The friendly name for this node
            type. For example: ve1-standard-72
        virtual_cpu_count (int):
            Output only. The total number of virtual CPUs
            in a single node.
        total_core_count (int):
            Output only. The total number of CPU cores in
            a single node.
        memory_gb (int):
            Output only. The amount of physical memory
            available, defined in GB.
        disk_size_gb (int):
            Output only. The amount of storage available,
            defined in GB.
        available_custom_core_counts (MutableSequence[int]):
            Output only. List of possible values of
            custom core count.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    node_type_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    virtual_cpu_count: int = proto.Field(
        proto.INT32,
        number=4,
    )
    total_core_count: int = proto.Field(
        proto.INT32,
        number=5,
    )
    memory_gb: int = proto.Field(
        proto.INT32,
        number=7,
    )
    disk_size_gb: int = proto.Field(
        proto.INT32,
        number=8,
    )
    available_custom_core_counts: MutableSequence[int] = proto.RepeatedField(
        proto.INT32,
        number=11,
    )


class Credentials(proto.Message):
    r"""Credentials for a private cloud.

    Attributes:
        username (str):
            Initial username.
        password (str):
            Initial password.
    """

    username: str = proto.Field(
        proto.STRING,
        number=1,
    )
    password: str = proto.Field(
        proto.STRING,
        number=2,
    )


class HcxActivationKey(proto.Message):
    r"""HCX activation key. A default key is created during private cloud
    provisioning, but this behavior is subject to change and you should
    always verify active keys. Use
    [VmwareEngine.ListHcxActivationKeys][google.cloud.vmwareengine.v1.VmwareEngine.ListHcxActivationKeys]
    to retrieve existing keys and
    [VmwareEngine.CreateHcxActivationKey][google.cloud.vmwareengine.v1.VmwareEngine.CreateHcxActivationKey]
    to create new ones.

    Attributes:
        name (str):
            Output only. The resource name of this HcxActivationKey.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-central1/privateClouds/my-cloud/hcxActivationKeys/my-key``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of HCX activation
            key.
        state (google.cloud.vmwareengine_v1.types.HcxActivationKey.State):
            Output only. State of HCX activation key.
        activation_key (str):
            Output only. HCX activation key.
        uid (str):
            Output only. System-generated unique
            identifier for the resource.
    """

    class State(proto.Enum):
        r"""State of HCX activation key

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified state.
            AVAILABLE (1):
                State of a newly generated activation key.
            CONSUMED (2):
                State of key when it has been used to
                activate HCX appliance.
            CREATING (3):
                State of key when it is being created.
        """
        STATE_UNSPECIFIED = 0
        AVAILABLE = 1
        CONSUMED = 2
        CREATING = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=3,
        enum=State,
    )
    activation_key: str = proto.Field(
        proto.STRING,
        number=4,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=5,
    )


class Hcx(proto.Message):
    r"""Details about a HCX Cloud Manager appliance.

    Attributes:
        internal_ip (str):
            Internal IP address of the appliance.
        version (str):
            Version of the appliance.
        state (google.cloud.vmwareengine_v1.types.Hcx.State):
            Output only. The state of the appliance.
        fqdn (str):
            Fully qualified domain name of the appliance.
    """

    class State(proto.Enum):
        r"""State of the appliance

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified appliance state. This is the
                default value.
            ACTIVE (1):
                The appliance is operational and can be used.
            CREATING (2):
                The appliance is being deployed.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2

    internal_ip: str = proto.Field(
        proto.STRING,
        number=2,
    )
    version: str = proto.Field(
        proto.STRING,
        number=4,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    fqdn: str = proto.Field(
        proto.STRING,
        number=6,
    )


class Nsx(proto.Message):
    r"""Details about a NSX Manager appliance.

    Attributes:
        internal_ip (str):
            Internal IP address of the appliance.
        version (str):
            Version of the appliance.
        state (google.cloud.vmwareengine_v1.types.Nsx.State):
            Output only. The state of the appliance.
        fqdn (str):
            Fully qualified domain name of the appliance.
    """

    class State(proto.Enum):
        r"""State of the appliance

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified appliance state. This is the
                default value.
            ACTIVE (1):
                The appliance is operational and can be used.
            CREATING (2):
                The appliance is being deployed.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2

    internal_ip: str = proto.Field(
        proto.STRING,
        number=2,
    )
    version: str = proto.Field(
        proto.STRING,
        number=4,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    fqdn: str = proto.Field(
        proto.STRING,
        number=6,
    )


class Vcenter(proto.Message):
    r"""Details about a vCenter Server management appliance.

    Attributes:
        internal_ip (str):
            Internal IP address of the appliance.
        version (str):
            Version of the appliance.
        state (google.cloud.vmwareengine_v1.types.Vcenter.State):
            Output only. The state of the appliance.
        fqdn (str):
            Fully qualified domain name of the appliance.
    """

    class State(proto.Enum):
        r"""State of the appliance

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified appliance state. This is the
                default value.
            ACTIVE (1):
                The appliance is operational and can be used.
            CREATING (2):
                The appliance is being deployed.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2

    internal_ip: str = proto.Field(
        proto.STRING,
        number=2,
    )
    version: str = proto.Field(
        proto.STRING,
        number=4,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    fqdn: str = proto.Field(
        proto.STRING,
        number=6,
    )


class PeeringRoute(proto.Message):
    r"""Exchanged network peering route.

    Attributes:
        dest_range (str):
            Output only. Destination range of the peering
            route in CIDR notation.
        type_ (google.cloud.vmwareengine_v1.types.PeeringRoute.Type):
            Output only. Type of the route in the peer
            VPC network.
        next_hop_region (str):
            Output only. Region containing the next hop
            of the peering route. This field only applies to
            dynamic routes in the peer VPC network.
        priority (int):
            Output only. The priority of the peering
            route.
        imported (bool):
            Output only. True if the peering route has been imported
            from a peered VPC network; false otherwise. The import
            happens if the field ``NetworkPeering.importCustomRoutes``
            is true for this network,
            ``NetworkPeering.exportCustomRoutes`` is true for the peer
            VPC network, and the import does not result in a route
            conflict.
        direction (google.cloud.vmwareengine_v1.types.PeeringRoute.Direction):
            Output only. Direction of the routes exchanged with the peer
            network, from the VMware Engine network perspective:

            -  Routes of direction ``INCOMING`` are imported from the
               peer network.
            -  Routes of direction ``OUTGOING`` are exported from the
               intranet VPC network of the VMware Engine network.
    """

    class Type(proto.Enum):
        r"""The type of the peering route.

        Values:
            TYPE_UNSPECIFIED (0):
                Unspecified peering route type. This is the
                default value.
            DYNAMIC_PEERING_ROUTE (1):
                Dynamic routes in the peer network.
            STATIC_PEERING_ROUTE (2):
                Static routes in the peer network.
            SUBNET_PEERING_ROUTE (3):
                Created, updated, and removed automatically
                by Google Cloud when subnets are created,
                modified, or deleted in the peer network.
        """
        TYPE_UNSPECIFIED = 0
        DYNAMIC_PEERING_ROUTE = 1
        STATIC_PEERING_ROUTE = 2
        SUBNET_PEERING_ROUTE = 3

    class Direction(proto.Enum):
        r"""The direction of the exchanged routes.

        Values:
            DIRECTION_UNSPECIFIED (0):
                Unspecified exchanged routes direction. This
                is default.
            INCOMING (1):
                Routes imported from the peer network.
            OUTGOING (2):
                Routes exported to the peer network.
        """
        DIRECTION_UNSPECIFIED = 0
        INCOMING = 1
        OUTGOING = 2

    dest_range: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=2,
        enum=Type,
    )
    next_hop_region: str = proto.Field(
        proto.STRING,
        number=3,
    )
    priority: int = proto.Field(
        proto.INT64,
        number=4,
    )
    imported: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    direction: Direction = proto.Field(
        proto.ENUM,
        number=6,
        enum=Direction,
    )


class NetworkPolicy(proto.Message):
    r"""Represents a network policy resource. Network policies are
    regional resources. You can use a network policy to enable or
    disable internet access and external IP access. Network policies
    are associated with a VMware Engine network, which might span
    across regions. For a given region, a network policy applies to
    all private clouds in the VMware Engine network associated with
    the policy.

    Attributes:
        name (str):
            Output only. The resource name of this network policy.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-central1/networkPolicies/my-network-policy``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of this resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update time of this
            resource.
        internet_access (google.cloud.vmwareengine_v1.types.NetworkPolicy.NetworkService):
            Network service that allows VMware workloads
            to access the internet.
        external_ip (google.cloud.vmwareengine_v1.types.NetworkPolicy.NetworkService):
            Network service that allows External IP addresses to be
            assigned to VMware workloads. This service can only be
            enabled when ``internet_access`` is also enabled.
        edge_services_cidr (str):
            Required. IP address range in CIDR notation
            used to create internet access and external IP
            access. An RFC 1918 CIDR block, with a "/26"
            prefix, is required. The range cannot overlap
            with any prefixes either in the consumer VPC
            network or in use by the private clouds attached
            to that VPC network.
        uid (str):
            Output only. System-generated unique
            identifier for the resource.
        vmware_engine_network (str):
            Optional. The relative resource name of the VMware Engine
            network. Specify the name in the following form:
            ``projects/{project}/locations/{location}/vmwareEngineNetworks/{vmware_engine_network_id}``
            where ``{project}`` can either be a project number or a
            project ID.
        description (str):
            Optional. User-provided description for this
            network policy.
        vmware_engine_network_canonical (str):
            Output only. The canonical name of the VMware Engine network
            in the form:
            ``projects/{project_number}/locations/{location}/vmwareEngineNetworks/{vmware_engine_network_id}``
    """

    class NetworkService(proto.Message):
        r"""Represents a network service that is managed by a ``NetworkPolicy``
        resource. A network service provides a way to control an aspect of
        external access to VMware workloads. For example, whether the VMware
        workloads in the private clouds governed by a network policy can
        access or be accessed from the internet.

        Attributes:
            enabled (bool):
                True if the service is enabled; false
                otherwise.
            state (google.cloud.vmwareengine_v1.types.NetworkPolicy.NetworkService.State):
                Output only. State of the service. New values
                may be added to this enum when appropriate.
        """

        class State(proto.Enum):
            r"""Enum State defines possible states of a network policy
            controlled service.

            Values:
                STATE_UNSPECIFIED (0):
                    Unspecified service state. This is the
                    default value.
                UNPROVISIONED (1):
                    Service is not provisioned.
                RECONCILING (2):
                    Service is in the process of being
                    provisioned/deprovisioned.
                ACTIVE (3):
                    Service is active.
            """
            STATE_UNSPECIFIED = 0
            UNPROVISIONED = 1
            RECONCILING = 2
            ACTIVE = 3

        enabled: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        state: "NetworkPolicy.NetworkService.State" = proto.Field(
            proto.ENUM,
            number=2,
            enum="NetworkPolicy.NetworkService.State",
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
    internet_access: NetworkService = proto.Field(
        proto.MESSAGE,
        number=6,
        message=NetworkService,
    )
    external_ip: NetworkService = proto.Field(
        proto.MESSAGE,
        number=7,
        message=NetworkService,
    )
    edge_services_cidr: str = proto.Field(
        proto.STRING,
        number=9,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=10,
    )
    vmware_engine_network: str = proto.Field(
        proto.STRING,
        number=12,
    )
    description: str = proto.Field(
        proto.STRING,
        number=13,
    )
    vmware_engine_network_canonical: str = proto.Field(
        proto.STRING,
        number=14,
    )


class VmwareEngineNetwork(proto.Message):
    r"""VMware Engine network resource that provides connectivity for
    VMware Engine private clouds.

    Attributes:
        name (str):
            Output only. The resource name of the VMware Engine network.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/global/vmwareEngineNetworks/my-network``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of this resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update time of this
            resource.
        description (str):
            User-provided description for this VMware
            Engine network.
        vpc_networks (MutableSequence[google.cloud.vmwareengine_v1.types.VmwareEngineNetwork.VpcNetwork]):
            Output only. VMware Engine service VPC
            networks that provide connectivity from a
            private cloud to customer projects, the
            internet, and other Google Cloud services.
        state (google.cloud.vmwareengine_v1.types.VmwareEngineNetwork.State):
            Output only. State of the VMware Engine
            network.
        type_ (google.cloud.vmwareengine_v1.types.VmwareEngineNetwork.Type):
            Required. VMware Engine network type.
        uid (str):
            Output only. System-generated unique
            identifier for the resource.
        etag (str):
            Checksum that may be sent on update and
            delete requests to ensure that the user-provided
            value is up to date before the server processes
            a request. The server computes checksums based
            on the value of other fields in the request.
    """

    class State(proto.Enum):
        r"""Enum State defines possible states of VMware Engine network.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is omitted.
            CREATING (1):
                The VMware Engine network is being created.
            ACTIVE (2):
                The VMware Engine network is ready.
            UPDATING (3):
                The VMware Engine network is being updated.
            DELETING (4):
                The VMware Engine network is being deleted.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        UPDATING = 3
        DELETING = 4

    class Type(proto.Enum):
        r"""Enum Type defines possible types of VMware Engine network.

        Values:
            TYPE_UNSPECIFIED (0):
                The default value. This value should never be
                used.
            LEGACY (1):
                Network type used by private clouds created in projects
                without a network of type ``STANDARD``. This network type is
                no longer used for new VMware Engine private cloud
                deployments.
        """
        TYPE_UNSPECIFIED = 0
        LEGACY = 1

    class VpcNetwork(proto.Message):
        r"""Represents a VMware Engine VPC network that is managed by a
        VMware Engine network resource.

        Attributes:
            type_ (google.cloud.vmwareengine_v1.types.VmwareEngineNetwork.VpcNetwork.Type):
                Output only. Type of VPC network (INTRANET, INTERNET, or
                GOOGLE_CLOUD)
            network (str):
                Output only. The relative resource name of the service VPC
                network this VMware Engine network is attached to. For
                example: ``projects/123123/global/networks/my-network``
        """

        class Type(proto.Enum):
            r"""Enum Type defines possible types of a VMware Engine network
            controlled service.

            Values:
                TYPE_UNSPECIFIED (0):
                    The default value. This value should never be
                    used.
                INTRANET (1):
                    VPC network that will be peered with a
                    consumer VPC network or the intranet VPC of
                    another VMware Engine network. Access a private
                    cloud through Compute Engine VMs on a peered VPC
                    network or an on-premises resource connected to
                    a peered consumer VPC network.
                INTERNET (2):
                    VPC network used for internet access to and
                    from a private cloud.
                GOOGLE_CLOUD (3):
                    VPC network used for access to Google Cloud
                    services like Cloud Storage.
            """
            TYPE_UNSPECIFIED = 0
            INTRANET = 1
            INTERNET = 2
            GOOGLE_CLOUD = 3

        type_: "VmwareEngineNetwork.VpcNetwork.Type" = proto.Field(
            proto.ENUM,
            number=1,
            enum="VmwareEngineNetwork.VpcNetwork.Type",
        )
        network: str = proto.Field(
            proto.STRING,
            number=2,
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
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    vpc_networks: MutableSequence[VpcNetwork] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message=VpcNetwork,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=7,
        enum=State,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=8,
        enum=Type,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=9,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=10,
    )


class PrivateConnection(proto.Message):
    r"""Private connection resource that provides connectivity for
    VMware Engine private clouds.

    Attributes:
        name (str):
            Output only. The resource name of the private connection.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-central1/privateConnections/my-connection``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of this resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update time of this
            resource.
        description (str):
            Optional. User-provided description for this
            private connection.
        state (google.cloud.vmwareengine_v1.types.PrivateConnection.State):
            Output only. State of the private connection.
        vmware_engine_network (str):
            Required. The relative resource name of Legacy VMware Engine
            network. Specify the name in the following form:
            ``projects/{project}/locations/{location}/vmwareEngineNetworks/{vmware_engine_network_id}``
            where ``{project}``, ``{location}`` will be same as
            specified in private connection resource name and
            ``{vmware_engine_network_id}`` will be in the form of
            ``{location}``-default e.g.
            projects/project/locations/us-central1/vmwareEngineNetworks/us-central1-default.
        vmware_engine_network_canonical (str):
            Output only. The canonical name of the VMware Engine network
            in the form:
            ``projects/{project_number}/locations/{location}/vmwareEngineNetworks/{vmware_engine_network_id}``
        type_ (google.cloud.vmwareengine_v1.types.PrivateConnection.Type):
            Required. Private connection type.
        peering_id (str):
            Output only. VPC network peering id between
            given network VPC and VMwareEngineNetwork.
        routing_mode (google.cloud.vmwareengine_v1.types.PrivateConnection.RoutingMode):
            Optional. Routing Mode. Default value is set to GLOBAL. For
            type = PRIVATE_SERVICE_ACCESS, this field can be set to
            GLOBAL or REGIONAL, for other types only GLOBAL is
            supported.
        uid (str):
            Output only. System-generated unique
            identifier for the resource.
        service_network (str):
            Required. Service network to create private connection.
            Specify the name in the following form:
            ``projects/{project}/global/networks/{network_id}`` For type
            = PRIVATE_SERVICE_ACCESS, this field represents
            servicenetworking VPC, e.g.
            projects/project-tp/global/networks/servicenetworking. For
            type = NETAPP_CLOUD_VOLUME, this field represents NetApp
            service VPC, e.g.
            projects/project-tp/global/networks/netapp-tenant-vpc. For
            type = DELL_POWERSCALE, this field represent Dell service
            VPC, e.g.
            projects/project-tp/global/networks/dell-tenant-vpc. For
            type= THIRD_PARTY_SERVICE, this field could represent a
            consumer VPC or any other producer VPC to which the VMware
            Engine Network needs to be connected, e.g.
            projects/project/global/networks/vpc.
        peering_state (google.cloud.vmwareengine_v1.types.PrivateConnection.PeeringState):
            Output only. Peering state between service
            network and VMware Engine network.
    """

    class State(proto.Enum):
        r"""Enum State defines possible states of private connection.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is omitted.
            CREATING (1):
                The private connection is being created.
            ACTIVE (2):
                The private connection is ready.
            UPDATING (3):
                The private connection is being updated.
            DELETING (4):
                The private connection is being deleted.
            UNPROVISIONED (5):
                The private connection is not provisioned,
                since no private cloud is present for which this
                private connection is needed.
            FAILED (6):
                The private connection is in failed state.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        UPDATING = 3
        DELETING = 4
        UNPROVISIONED = 5
        FAILED = 6

    class Type(proto.Enum):
        r"""Enum Type defines possible types of private connection.

        Values:
            TYPE_UNSPECIFIED (0):
                The default value. This value should never be
                used.
            PRIVATE_SERVICE_ACCESS (1):
                Connection used for establishing `private services
                access <https://cloud.google.com/vpc/docs/private-services-access>`__.
            NETAPP_CLOUD_VOLUMES (2):
                Connection used for connecting to NetApp
                Cloud Volumes.
            DELL_POWERSCALE (3):
                Connection used for connecting to Dell
                PowerScale.
            THIRD_PARTY_SERVICE (4):
                Connection used for connecting to third-party
                services.
        """
        TYPE_UNSPECIFIED = 0
        PRIVATE_SERVICE_ACCESS = 1
        NETAPP_CLOUD_VOLUMES = 2
        DELL_POWERSCALE = 3
        THIRD_PARTY_SERVICE = 4

    class RoutingMode(proto.Enum):
        r"""Possible types for RoutingMode

        Values:
            ROUTING_MODE_UNSPECIFIED (0):
                The default value. This value should never be
                used.
            GLOBAL (1):
                Global Routing Mode
            REGIONAL (2):
                Regional Routing Mode
        """
        ROUTING_MODE_UNSPECIFIED = 0
        GLOBAL = 1
        REGIONAL = 2

    class PeeringState(proto.Enum):
        r"""Enum PeeringState defines the possible states of peering
        between service network and the vpc network peered to service
        network

        Values:
            PEERING_STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                peering state is omitted or unknown.
            PEERING_ACTIVE (1):
                The peering is in active state.
            PEERING_INACTIVE (2):
                The peering is in inactive state.
        """
        PEERING_STATE_UNSPECIFIED = 0
        PEERING_ACTIVE = 1
        PEERING_INACTIVE = 2

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
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    vmware_engine_network: str = proto.Field(
        proto.STRING,
        number=8,
    )
    vmware_engine_network_canonical: str = proto.Field(
        proto.STRING,
        number=9,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=10,
        enum=Type,
    )
    peering_id: str = proto.Field(
        proto.STRING,
        number=12,
    )
    routing_mode: RoutingMode = proto.Field(
        proto.ENUM,
        number=13,
        enum=RoutingMode,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=14,
    )
    service_network: str = proto.Field(
        proto.STRING,
        number=16,
    )
    peering_state: PeeringState = proto.Field(
        proto.ENUM,
        number=17,
        enum=PeeringState,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
