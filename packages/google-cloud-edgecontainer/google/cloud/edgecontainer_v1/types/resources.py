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
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.edgecontainer.v1",
    manifest={
        "KmsKeyState",
        "Cluster",
        "ClusterNetworking",
        "Fleet",
        "ClusterUser",
        "Authorization",
        "NodePool",
        "Machine",
        "VpnConnection",
        "LocationMetadata",
        "ZoneMetadata",
        "Quota",
        "MaintenancePolicy",
        "MaintenanceWindow",
        "RecurringTimeWindow",
        "TimeWindow",
    },
)


class KmsKeyState(proto.Enum):
    r"""Represents the accessibility state of a customer-managed KMS
    key used for CMEK integration.

    Values:
        KMS_KEY_STATE_UNSPECIFIED (0):
            Unspecified.
        KMS_KEY_STATE_KEY_AVAILABLE (1):
            The key is available for use, and dependent
            resources should be accessible.
        KMS_KEY_STATE_KEY_UNAVAILABLE (2):
            The key is unavailable for an unspecified
            reason. Dependent resources may be inaccessible.
    """
    KMS_KEY_STATE_UNSPECIFIED = 0
    KMS_KEY_STATE_KEY_AVAILABLE = 1
    KMS_KEY_STATE_KEY_UNAVAILABLE = 2


class Cluster(proto.Message):
    r"""A Google Distributed Cloud Edge Kubernetes cluster.

    Attributes:
        name (str):
            Required. The resource name of the cluster.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the cluster was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the cluster was
            last updated.
        labels (MutableMapping[str, str]):
            Labels associated with this resource.
        fleet (google.cloud.edgecontainer_v1.types.Fleet):
            Optional. Fleet configuration.
        networking (google.cloud.edgecontainer_v1.types.ClusterNetworking):
            Required. Cluster-wide networking
            configuration.
        authorization (google.cloud.edgecontainer_v1.types.Authorization):
            Required. Immutable. RBAC policy that will be
            applied and managed by GEC.
        default_max_pods_per_node (int):
            Optional. The default maximum number of pods
            per node used if a maximum value is not
            specified explicitly for a node pool in this
            cluster. If unspecified, the Kubernetes default
            value will be used.
        endpoint (str):
            Output only. The IP address of the Kubernetes
            API server.
        cluster_ca_certificate (str):
            Output only. The PEM-encoded public
            certificate of the cluster's CA.
        maintenance_policy (google.cloud.edgecontainer_v1.types.MaintenancePolicy):
            Optional. Cluster-wide maintenance policy
            configuration.
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
    fleet: "Fleet" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="Fleet",
    )
    networking: "ClusterNetworking" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="ClusterNetworking",
    )
    authorization: "Authorization" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="Authorization",
    )
    default_max_pods_per_node: int = proto.Field(
        proto.INT32,
        number=8,
    )
    endpoint: str = proto.Field(
        proto.STRING,
        number=6,
    )
    cluster_ca_certificate: str = proto.Field(
        proto.STRING,
        number=10,
    )
    maintenance_policy: "MaintenancePolicy" = proto.Field(
        proto.MESSAGE,
        number=12,
        message="MaintenancePolicy",
    )


class ClusterNetworking(proto.Message):
    r"""Cluster-wide networking configuration.

    Attributes:
        cluster_ipv4_cidr_blocks (MutableSequence[str]):
            Required. All pods in the cluster are
            assigned an RFC1918 IPv4 address from these
            blocks. Only a single block is supported. This
            field cannot be changed after creation.
        services_ipv4_cidr_blocks (MutableSequence[str]):
            Required. All services in the cluster are
            assigned an RFC1918 IPv4 address from these
            blocks. Only a single block is supported. This
            field cannot be changed after creation.
    """

    cluster_ipv4_cidr_blocks: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    services_ipv4_cidr_blocks: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class Fleet(proto.Message):
    r"""Fleet related configuration.
    Fleets are a Google Cloud concept for logically organizing
    clusters, letting you use and manage multi-cluster capabilities
    and apply consistent policies across your systems.

    Attributes:
        project (str):
            Required. The name of the Fleet host project where this
            cluster will be registered.

            Project names are formatted as
            ``projects/<project-number>``.
        membership (str):
            Output only. The name of the managed Hub Membership resource
            associated to this cluster.

            Membership names are formatted as
            ``projects/<project-number>/locations/global/membership/<cluster-id>``.
    """

    project: str = proto.Field(
        proto.STRING,
        number=1,
    )
    membership: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ClusterUser(proto.Message):
    r"""A user principal for an RBAC policy.

    Attributes:
        username (str):
            Required. An active Google username.
    """

    username: str = proto.Field(
        proto.STRING,
        number=1,
    )


class Authorization(proto.Message):
    r"""RBAC policy that will be applied and managed by GEC.

    Attributes:
        admin_users (google.cloud.edgecontainer_v1.types.ClusterUser):
            Required. User that will be granted the
            cluster-admin role on the cluster, providing
            full access to the cluster. Currently, this is a
            singular field, but will be expanded to allow
            multiple admins in the future.
    """

    admin_users: "ClusterUser" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ClusterUser",
    )


class NodePool(proto.Message):
    r"""A set of Kubernetes nodes in a cluster with common
    configuration and specification.

    Attributes:
        name (str):
            Required. The resource name of the node pool.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the node pool was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the node pool was
            last updated.
        labels (MutableMapping[str, str]):
            Labels associated with this resource.
        node_location (str):
            Name of the Google Distributed Cloud Edge zone where this
            node pool will be created. For example:
            ``us-central1-edge-customer-a``.
        node_count (int):
            Required. The number of nodes in the pool.
        machine_filter (str):
            Only machines matching this filter will be allowed to join
            the node pool. The filtering language accepts strings like
            "name=", and is documented in more detail in
            `AIP-160 <https://google.aip.dev/160>`__.
        local_disk_encryption (google.cloud.edgecontainer_v1.types.NodePool.LocalDiskEncryption):
            Optional. Local disk encryption options. This
            field is only used when enabling CMEK support.
    """

    class LocalDiskEncryption(proto.Message):
        r"""Configuration for CMEK support for edge machine local disk
        encryption.

        Attributes:
            kms_key (str):
                Immutable. The Cloud KMS CryptoKey e.g.
                projects/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{cryptoKey}
                to use for protecting node local disks. If not
                specified, a Google-managed key will be used
                instead.
            kms_key_active_version (str):
                Output only. The Cloud KMS CryptoKeyVersion currently in use
                for protecting node local disks. Only applicable if kms_key
                is set.
            kms_key_state (google.cloud.edgecontainer_v1.types.KmsKeyState):
                Output only. Availability of the Cloud KMS CryptoKey. If not
                ``KEY_AVAILABLE``, then nodes may go offline as they cannot
                access their local data. This can be caused by a lack of
                permissions to use the key, or if the key is disabled or
                deleted.
            kms_status (google.rpc.status_pb2.Status):
                Output only. Error status returned by Cloud KMS when using
                this key. This field may be populated only if
                ``kms_key_state`` is not ``KMS_KEY_STATE_KEY_AVAILABLE``. If
                populated, this field contains the error status reported by
                Cloud KMS.
        """

        kms_key: str = proto.Field(
            proto.STRING,
            number=1,
        )
        kms_key_active_version: str = proto.Field(
            proto.STRING,
            number=2,
        )
        kms_key_state: "KmsKeyState" = proto.Field(
            proto.ENUM,
            number=3,
            enum="KmsKeyState",
        )
        kms_status: status_pb2.Status = proto.Field(
            proto.MESSAGE,
            number=4,
            message=status_pb2.Status,
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
    node_location: str = proto.Field(
        proto.STRING,
        number=8,
    )
    node_count: int = proto.Field(
        proto.INT32,
        number=6,
    )
    machine_filter: str = proto.Field(
        proto.STRING,
        number=7,
    )
    local_disk_encryption: LocalDiskEncryption = proto.Field(
        proto.MESSAGE,
        number=9,
        message=LocalDiskEncryption,
    )


class Machine(proto.Message):
    r"""A Google Distributed Cloud Edge machine capable of acting as
    a Kubernetes node.

    Attributes:
        name (str):
            Required. The resource name of the machine.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the node pool was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the node pool was
            last updated.
        labels (MutableMapping[str, str]):
            Labels associated with this resource.
        hosted_node (str):
            Canonical resource name of the node that this machine is
            responsible for hosting e.g.
            projects/{project}/locations/{location}/clusters/{cluster_id}/nodePools/{pool_id}/{node},
            Or empty if the machine is not assigned to assume the role
            of a node.
        zone (str):
            The Google Distributed Cloud Edge zone of
            this machine.
        disabled (bool):
            Output only. Whether the machine is disabled.
            If disabled, the machine is unable to enter
            service.
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
    hosted_node: str = proto.Field(
        proto.STRING,
        number=5,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=6,
    )
    disabled: bool = proto.Field(
        proto.BOOL,
        number=8,
    )


class VpnConnection(proto.Message):
    r"""A VPN connection .

    Attributes:
        name (str):
            Required. The resource name of VPN connection
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the VPN connection
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the VPN connection
            was last updated.
        labels (MutableMapping[str, str]):
            Labels associated with this resource.
        nat_gateway_ip (str):
            NAT gateway IP, or WAN IP address. If a
            customer has multiple NAT IPs, the customer
            needs to configure NAT such that only one
            external IP maps to the GMEC Anthos cluster.
            This is empty if NAT is not used.
        bgp_routing_mode (google.cloud.edgecontainer_v1.types.VpnConnection.BgpRoutingMode):
            Dynamic routing mode of the VPC network, ``regional`` or
            ``global``.
        cluster (str):
            The canonical Cluster name to connect to. It
            is in the form of
            projects/{project}/locations/{location}/clusters/{cluster}.
        vpc (str):
            The network ID of VPC to connect to.
        vpc_project (google.cloud.edgecontainer_v1.types.VpnConnection.VpcProject):
            Optional. Project detail of the VPC network.
            Required if VPC is in a different project than
            the cluster project.
        enable_high_availability (bool):
            Whether this VPN connection has HA enabled on
            cluster side. If enabled, when creating VPN
            connection we will attempt to use 2 ANG floating
            IPs.
        details (google.cloud.edgecontainer_v1.types.VpnConnection.Details):
            Output only. The created connection details.
    """

    class BgpRoutingMode(proto.Enum):
        r"""Routing mode.

        Values:
            BGP_ROUTING_MODE_UNSPECIFIED (0):
                Unknown.
            REGIONAL (1):
                Regional mode.
            GLOBAL (2):
                Global mode.
        """
        BGP_ROUTING_MODE_UNSPECIFIED = 0
        REGIONAL = 1
        GLOBAL = 2

    class VpcProject(proto.Message):
        r"""Project detail of the VPC network.

        Attributes:
            project_id (str):
                The project of the VPC to connect to. If not
                specified, it is the same as the cluster
                project.
            service_account (str):
                Optional. The service account in the VPC project configured
                by user. It is used to create/delete Cloud Router and Cloud
                HA VPNs for VPN connection. If this SA is changed
                during/after a VPN connection is created, you need to remove
                the Cloud Router and Cloud VPN resources in \|project_id|.
                It is in the form of
                service-{project_number}@gcp-sa-edgecontainer.iam.gserviceaccount.com.
        """

        project_id: str = proto.Field(
            proto.STRING,
            number=1,
        )
        service_account: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class Details(proto.Message):
        r"""The created connection details.

        Attributes:
            state (google.cloud.edgecontainer_v1.types.VpnConnection.Details.State):
                The state of this connection.
            error (str):
                The error message. This is only populated
                when state=ERROR.
            cloud_router (google.cloud.edgecontainer_v1.types.VpnConnection.Details.CloudRouter):
                The Cloud Router info.
            cloud_vpns (MutableSequence[google.cloud.edgecontainer_v1.types.VpnConnection.Details.CloudVpn]):
                Each connection has multiple Cloud VPN
                gateways.
        """

        class State(proto.Enum):
            r"""The current connection state.

            Values:
                STATE_UNSPECIFIED (0):
                    Unknown.
                STATE_CONNECTED (1):
                    Connected.
                STATE_CONNECTING (2):
                    Still connecting.
                STATE_ERROR (3):
                    Error occurred.
            """
            STATE_UNSPECIFIED = 0
            STATE_CONNECTED = 1
            STATE_CONNECTING = 2
            STATE_ERROR = 3

        class CloudRouter(proto.Message):
            r"""The Cloud Router info.

            Attributes:
                name (str):
                    The created Cloud Router name.
            """

            name: str = proto.Field(
                proto.STRING,
                number=1,
            )

        class CloudVpn(proto.Message):
            r"""The Cloud VPN info.

            Attributes:
                gateway (str):
                    The created Cloud VPN gateway name.
            """

            gateway: str = proto.Field(
                proto.STRING,
                number=1,
            )

        state: "VpnConnection.Details.State" = proto.Field(
            proto.ENUM,
            number=1,
            enum="VpnConnection.Details.State",
        )
        error: str = proto.Field(
            proto.STRING,
            number=2,
        )
        cloud_router: "VpnConnection.Details.CloudRouter" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="VpnConnection.Details.CloudRouter",
        )
        cloud_vpns: MutableSequence[
            "VpnConnection.Details.CloudVpn"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=4,
            message="VpnConnection.Details.CloudVpn",
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
    nat_gateway_ip: str = proto.Field(
        proto.STRING,
        number=5,
    )
    bgp_routing_mode: BgpRoutingMode = proto.Field(
        proto.ENUM,
        number=6,
        enum=BgpRoutingMode,
    )
    cluster: str = proto.Field(
        proto.STRING,
        number=7,
    )
    vpc: str = proto.Field(
        proto.STRING,
        number=8,
    )
    vpc_project: VpcProject = proto.Field(
        proto.MESSAGE,
        number=11,
        message=VpcProject,
    )
    enable_high_availability: bool = proto.Field(
        proto.BOOL,
        number=9,
    )
    details: Details = proto.Field(
        proto.MESSAGE,
        number=10,
        message=Details,
    )


class LocationMetadata(proto.Message):
    r"""Metadata for a given
    [google.cloud.location.Location][google.cloud.location.Location].

    Attributes:
        available_zones (MutableMapping[str, google.cloud.edgecontainer_v1.types.ZoneMetadata]):
            The set of available Google Distributed Cloud
            Edge zones in the location. The map is keyed by
            the lowercase ID of each zone.
    """

    available_zones: MutableMapping[str, "ZoneMetadata"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=1,
        message="ZoneMetadata",
    )


class ZoneMetadata(proto.Message):
    r"""A Google Distributed Cloud Edge zone where edge machines are
    located.

    Attributes:
        quota (MutableSequence[google.cloud.edgecontainer_v1.types.Quota]):
            Quota for resources in this zone.
    """

    quota: MutableSequence["Quota"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Quota",
    )


class Quota(proto.Message):
    r"""Represents quota for Edge Container resources.

    Attributes:
        metric (str):
            Name of the quota metric.
        limit (float):
            Quota limit for this metric.
        usage (float):
            Current usage of this metric.
    """

    metric: str = proto.Field(
        proto.STRING,
        number=1,
    )
    limit: float = proto.Field(
        proto.DOUBLE,
        number=2,
    )
    usage: float = proto.Field(
        proto.DOUBLE,
        number=3,
    )


class MaintenancePolicy(proto.Message):
    r"""Maintenance policy configuration.

    Attributes:
        window (google.cloud.edgecontainer_v1.types.MaintenanceWindow):
            Specifies the maintenance window in which
            maintenance may be performed.
    """

    window: "MaintenanceWindow" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="MaintenanceWindow",
    )


class MaintenanceWindow(proto.Message):
    r"""Maintenance window configuration

    Attributes:
        recurring_window (google.cloud.edgecontainer_v1.types.RecurringTimeWindow):
            Configuration of a recurring maintenance
            window.
    """

    recurring_window: "RecurringTimeWindow" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="RecurringTimeWindow",
    )


class RecurringTimeWindow(proto.Message):
    r"""Represents an arbitrary window of time that recurs.

    Attributes:
        window (google.cloud.edgecontainer_v1.types.TimeWindow):
            The window of the first recurrence.
        recurrence (str):
            An RRULE
            (https://tools.ietf.org/html/rfc5545#section-3.8.5.3)
            for how this window recurs. They go on for the
            span of time between the start and end time.
    """

    window: "TimeWindow" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="TimeWindow",
    )
    recurrence: str = proto.Field(
        proto.STRING,
        number=2,
    )


class TimeWindow(proto.Message):
    r"""Represents an arbitrary window of time.

    Attributes:
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The time that the window first starts.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time that the window ends. The end time
            must take place after the start time.
    """

    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
