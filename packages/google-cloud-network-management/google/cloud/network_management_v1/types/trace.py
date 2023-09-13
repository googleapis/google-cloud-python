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

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.networkmanagement.v1",
    manifest={
        "LoadBalancerType",
        "Trace",
        "Step",
        "InstanceInfo",
        "NetworkInfo",
        "FirewallInfo",
        "RouteInfo",
        "GoogleServiceInfo",
        "ForwardingRuleInfo",
        "LoadBalancerInfo",
        "LoadBalancerBackend",
        "VpnGatewayInfo",
        "VpnTunnelInfo",
        "EndpointInfo",
        "DeliverInfo",
        "ForwardInfo",
        "AbortInfo",
        "DropInfo",
        "GKEMasterInfo",
        "CloudSQLInstanceInfo",
        "CloudFunctionInfo",
        "CloudRunRevisionInfo",
        "AppEngineVersionInfo",
        "VpcConnectorInfo",
    },
)


class LoadBalancerType(proto.Enum):
    r"""Type of a load balancer. For more information, see `Summary of
    Google Cloud load
    balancers <https://cloud.google.com/load-balancing/docs/load-balancing-overview#summary-of-google-cloud-load-balancers>`__.

    Values:
        LOAD_BALANCER_TYPE_UNSPECIFIED (0):
            Forwarding rule points to a different target
            than a load balancer or a load balancer type is
            unknown.
        HTTPS_ADVANCED_LOAD_BALANCER (1):
            Global external HTTP(S) load balancer.
        HTTPS_LOAD_BALANCER (2):
            Global external HTTP(S) load balancer
            (classic)
        REGIONAL_HTTPS_LOAD_BALANCER (3):
            Regional external HTTP(S) load balancer.
        INTERNAL_HTTPS_LOAD_BALANCER (4):
            Internal HTTP(S) load balancer.
        SSL_PROXY_LOAD_BALANCER (5):
            External SSL proxy load balancer.
        TCP_PROXY_LOAD_BALANCER (6):
            External TCP proxy load balancer.
        INTERNAL_TCP_PROXY_LOAD_BALANCER (7):
            Internal regional TCP proxy load balancer.
        NETWORK_LOAD_BALANCER (8):
            External TCP/UDP Network load balancer.
        LEGACY_NETWORK_LOAD_BALANCER (9):
            Target-pool based external TCP/UDP Network
            load balancer.
        TCP_UDP_INTERNAL_LOAD_BALANCER (10):
            Internal TCP/UDP load balancer.
    """
    LOAD_BALANCER_TYPE_UNSPECIFIED = 0
    HTTPS_ADVANCED_LOAD_BALANCER = 1
    HTTPS_LOAD_BALANCER = 2
    REGIONAL_HTTPS_LOAD_BALANCER = 3
    INTERNAL_HTTPS_LOAD_BALANCER = 4
    SSL_PROXY_LOAD_BALANCER = 5
    TCP_PROXY_LOAD_BALANCER = 6
    INTERNAL_TCP_PROXY_LOAD_BALANCER = 7
    NETWORK_LOAD_BALANCER = 8
    LEGACY_NETWORK_LOAD_BALANCER = 9
    TCP_UDP_INTERNAL_LOAD_BALANCER = 10


class Trace(proto.Message):
    r"""Trace represents one simulated packet forwarding path.

    -  Each trace contains multiple ordered steps.
    -  Each step is in a particular state with associated configuration.
    -  State is categorized as final or non-final states.
    -  Each final state has a reason associated.
    -  Each trace must end with a final state (the last step).

    ::

         |---------------------Trace----------------------|
         Step1(State) Step2(State) ---  StepN(State(final))

    Attributes:
        endpoint_info (google.cloud.network_management_v1.types.EndpointInfo):
            Derived from the source and destination endpoints definition
            specified by user request, and validated by the data plane
            model. If there are multiple traces starting from different
            source locations, then the endpoint_info may be different
            between traces.
        steps (MutableSequence[google.cloud.network_management_v1.types.Step]):
            A trace of a test contains multiple steps
            from the initial state to the final state
            (delivered, dropped, forwarded, or aborted).

            The steps are ordered by the processing sequence
            within the simulated network state machine. It
            is critical to preserve the order of the steps
            and avoid reordering or sorting them.
    """

    endpoint_info: "EndpointInfo" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="EndpointInfo",
    )
    steps: MutableSequence["Step"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Step",
    )


class Step(proto.Message):
    r"""A simulated forwarding path is composed of multiple steps.
    Each step has a well-defined state and an associated
    configuration.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        description (str):
            A description of the step. Usually this is a
            summary of the state.
        state (google.cloud.network_management_v1.types.Step.State):
            Each step is in one of the pre-defined
            states.
        causes_drop (bool):
            This is a step that leads to the final state
            Drop.
        project_id (str):
            Project ID that contains the configuration
            this step is validating.
        instance (google.cloud.network_management_v1.types.InstanceInfo):
            Display information of a Compute Engine
            instance.

            This field is a member of `oneof`_ ``step_info``.
        firewall (google.cloud.network_management_v1.types.FirewallInfo):
            Display information of a Compute Engine
            firewall rule.

            This field is a member of `oneof`_ ``step_info``.
        route (google.cloud.network_management_v1.types.RouteInfo):
            Display information of a Compute Engine
            route.

            This field is a member of `oneof`_ ``step_info``.
        endpoint (google.cloud.network_management_v1.types.EndpointInfo):
            Display information of the source and
            destination under analysis. The endpoint
            information in an intermediate state may differ
            with the initial input, as it might be modified
            by state like NAT, or Connection Proxy.

            This field is a member of `oneof`_ ``step_info``.
        google_service (google.cloud.network_management_v1.types.GoogleServiceInfo):
            Display information of a Google service

            This field is a member of `oneof`_ ``step_info``.
        forwarding_rule (google.cloud.network_management_v1.types.ForwardingRuleInfo):
            Display information of a Compute Engine
            forwarding rule.

            This field is a member of `oneof`_ ``step_info``.
        vpn_gateway (google.cloud.network_management_v1.types.VpnGatewayInfo):
            Display information of a Compute Engine VPN
            gateway.

            This field is a member of `oneof`_ ``step_info``.
        vpn_tunnel (google.cloud.network_management_v1.types.VpnTunnelInfo):
            Display information of a Compute Engine VPN
            tunnel.

            This field is a member of `oneof`_ ``step_info``.
        vpc_connector (google.cloud.network_management_v1.types.VpcConnectorInfo):
            Display information of a VPC connector.

            This field is a member of `oneof`_ ``step_info``.
        deliver (google.cloud.network_management_v1.types.DeliverInfo):
            Display information of the final state
            "deliver" and reason.

            This field is a member of `oneof`_ ``step_info``.
        forward (google.cloud.network_management_v1.types.ForwardInfo):
            Display information of the final state
            "forward" and reason.

            This field is a member of `oneof`_ ``step_info``.
        abort (google.cloud.network_management_v1.types.AbortInfo):
            Display information of the final state
            "abort" and reason.

            This field is a member of `oneof`_ ``step_info``.
        drop (google.cloud.network_management_v1.types.DropInfo):
            Display information of the final state "drop"
            and reason.

            This field is a member of `oneof`_ ``step_info``.
        load_balancer (google.cloud.network_management_v1.types.LoadBalancerInfo):
            Display information of the load balancers.

            This field is a member of `oneof`_ ``step_info``.
        network (google.cloud.network_management_v1.types.NetworkInfo):
            Display information of a Google Cloud
            network.

            This field is a member of `oneof`_ ``step_info``.
        gke_master (google.cloud.network_management_v1.types.GKEMasterInfo):
            Display information of a Google Kubernetes
            Engine cluster master.

            This field is a member of `oneof`_ ``step_info``.
        cloud_sql_instance (google.cloud.network_management_v1.types.CloudSQLInstanceInfo):
            Display information of a Cloud SQL instance.

            This field is a member of `oneof`_ ``step_info``.
        cloud_function (google.cloud.network_management_v1.types.CloudFunctionInfo):
            Display information of a Cloud Function.

            This field is a member of `oneof`_ ``step_info``.
        app_engine_version (google.cloud.network_management_v1.types.AppEngineVersionInfo):
            Display information of an App Engine service
            version.

            This field is a member of `oneof`_ ``step_info``.
        cloud_run_revision (google.cloud.network_management_v1.types.CloudRunRevisionInfo):
            Display information of a Cloud Run revision.

            This field is a member of `oneof`_ ``step_info``.
    """

    class State(proto.Enum):
        r"""Type of states that are defined in the network state machine.
        Each step in the packet trace is in a specific state.

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified state.
            START_FROM_INSTANCE (1):
                Initial state: packet originating from a
                Compute Engine instance. An InstanceInfo is
                populated with starting instance information.
            START_FROM_INTERNET (2):
                Initial state: packet originating from the
                internet. The endpoint information is populated.
            START_FROM_GOOGLE_SERVICE (27):
                Initial state: packet originating from a
                Google service. Some Google services, such as
                health check probers or Identity Aware Proxy use
                special routes, outside VPC routing
                configuration to reach Compute Engine Instances.
            START_FROM_PRIVATE_NETWORK (3):
                Initial state: packet originating from a VPC
                or on-premises network with internal source IP.
                If the source is a VPC network visible to the
                user, a NetworkInfo is populated with details of
                the network.
            START_FROM_GKE_MASTER (21):
                Initial state: packet originating from a
                Google Kubernetes Engine cluster master. A
                GKEMasterInfo is populated with starting
                instance information.
            START_FROM_CLOUD_SQL_INSTANCE (22):
                Initial state: packet originating from a
                Cloud SQL instance. A CloudSQLInstanceInfo is
                populated with starting instance information.
            START_FROM_CLOUD_FUNCTION (23):
                Initial state: packet originating from a
                Cloud Function. A CloudFunctionInfo is populated
                with starting function information.
            START_FROM_APP_ENGINE_VERSION (25):
                Initial state: packet originating from an App
                Engine service version. An AppEngineVersionInfo
                is populated with starting version information.
            START_FROM_CLOUD_RUN_REVISION (26):
                Initial state: packet originating from a
                Cloud Run revision. A CloudRunRevisionInfo is
                populated with starting revision information.
            APPLY_INGRESS_FIREWALL_RULE (4):
                Config checking state: verify ingress
                firewall rule.
            APPLY_EGRESS_FIREWALL_RULE (5):
                Config checking state: verify egress firewall
                rule.
            APPLY_ROUTE (6):
                Config checking state: verify route.
            APPLY_FORWARDING_RULE (7):
                Config checking state: match forwarding rule.
            SPOOFING_APPROVED (8):
                Config checking state: packet sent or
                received under foreign IP address and allowed.
            ARRIVE_AT_INSTANCE (9):
                Forwarding state: arriving at a Compute
                Engine instance.
            ARRIVE_AT_INTERNAL_LOAD_BALANCER (10):
                Forwarding state: arriving at a Compute
                Engine internal load balancer.
            ARRIVE_AT_EXTERNAL_LOAD_BALANCER (11):
                Forwarding state: arriving at a Compute
                Engine external load balancer.
            ARRIVE_AT_VPN_GATEWAY (12):
                Forwarding state: arriving at a Cloud VPN
                gateway.
            ARRIVE_AT_VPN_TUNNEL (13):
                Forwarding state: arriving at a Cloud VPN
                tunnel.
            ARRIVE_AT_VPC_CONNECTOR (24):
                Forwarding state: arriving at a VPC
                connector.
            NAT (14):
                Transition state: packet header translated.
            PROXY_CONNECTION (15):
                Transition state: original connection is
                terminated and a new proxied connection is
                initiated.
            DELIVER (16):
                Final state: packet could be delivered.
            DROP (17):
                Final state: packet could be dropped.
            FORWARD (18):
                Final state: packet could be forwarded to a
                network with an unknown configuration.
            ABORT (19):
                Final state: analysis is aborted.
            VIEWER_PERMISSION_MISSING (20):
                Special state: viewer of the test result does
                not have permission to see the configuration in
                this step.
        """
        STATE_UNSPECIFIED = 0
        START_FROM_INSTANCE = 1
        START_FROM_INTERNET = 2
        START_FROM_GOOGLE_SERVICE = 27
        START_FROM_PRIVATE_NETWORK = 3
        START_FROM_GKE_MASTER = 21
        START_FROM_CLOUD_SQL_INSTANCE = 22
        START_FROM_CLOUD_FUNCTION = 23
        START_FROM_APP_ENGINE_VERSION = 25
        START_FROM_CLOUD_RUN_REVISION = 26
        APPLY_INGRESS_FIREWALL_RULE = 4
        APPLY_EGRESS_FIREWALL_RULE = 5
        APPLY_ROUTE = 6
        APPLY_FORWARDING_RULE = 7
        SPOOFING_APPROVED = 8
        ARRIVE_AT_INSTANCE = 9
        ARRIVE_AT_INTERNAL_LOAD_BALANCER = 10
        ARRIVE_AT_EXTERNAL_LOAD_BALANCER = 11
        ARRIVE_AT_VPN_GATEWAY = 12
        ARRIVE_AT_VPN_TUNNEL = 13
        ARRIVE_AT_VPC_CONNECTOR = 24
        NAT = 14
        PROXY_CONNECTION = 15
        DELIVER = 16
        DROP = 17
        FORWARD = 18
        ABORT = 19
        VIEWER_PERMISSION_MISSING = 20

    description: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )
    causes_drop: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    project_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    instance: "InstanceInfo" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="step_info",
        message="InstanceInfo",
    )
    firewall: "FirewallInfo" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="step_info",
        message="FirewallInfo",
    )
    route: "RouteInfo" = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="step_info",
        message="RouteInfo",
    )
    endpoint: "EndpointInfo" = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="step_info",
        message="EndpointInfo",
    )
    google_service: "GoogleServiceInfo" = proto.Field(
        proto.MESSAGE,
        number=24,
        oneof="step_info",
        message="GoogleServiceInfo",
    )
    forwarding_rule: "ForwardingRuleInfo" = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="step_info",
        message="ForwardingRuleInfo",
    )
    vpn_gateway: "VpnGatewayInfo" = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="step_info",
        message="VpnGatewayInfo",
    )
    vpn_tunnel: "VpnTunnelInfo" = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="step_info",
        message="VpnTunnelInfo",
    )
    vpc_connector: "VpcConnectorInfo" = proto.Field(
        proto.MESSAGE,
        number=21,
        oneof="step_info",
        message="VpcConnectorInfo",
    )
    deliver: "DeliverInfo" = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="step_info",
        message="DeliverInfo",
    )
    forward: "ForwardInfo" = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof="step_info",
        message="ForwardInfo",
    )
    abort: "AbortInfo" = proto.Field(
        proto.MESSAGE,
        number=14,
        oneof="step_info",
        message="AbortInfo",
    )
    drop: "DropInfo" = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="step_info",
        message="DropInfo",
    )
    load_balancer: "LoadBalancerInfo" = proto.Field(
        proto.MESSAGE,
        number=16,
        oneof="step_info",
        message="LoadBalancerInfo",
    )
    network: "NetworkInfo" = proto.Field(
        proto.MESSAGE,
        number=17,
        oneof="step_info",
        message="NetworkInfo",
    )
    gke_master: "GKEMasterInfo" = proto.Field(
        proto.MESSAGE,
        number=18,
        oneof="step_info",
        message="GKEMasterInfo",
    )
    cloud_sql_instance: "CloudSQLInstanceInfo" = proto.Field(
        proto.MESSAGE,
        number=19,
        oneof="step_info",
        message="CloudSQLInstanceInfo",
    )
    cloud_function: "CloudFunctionInfo" = proto.Field(
        proto.MESSAGE,
        number=20,
        oneof="step_info",
        message="CloudFunctionInfo",
    )
    app_engine_version: "AppEngineVersionInfo" = proto.Field(
        proto.MESSAGE,
        number=22,
        oneof="step_info",
        message="AppEngineVersionInfo",
    )
    cloud_run_revision: "CloudRunRevisionInfo" = proto.Field(
        proto.MESSAGE,
        number=23,
        oneof="step_info",
        message="CloudRunRevisionInfo",
    )


class InstanceInfo(proto.Message):
    r"""For display only. Metadata associated with a Compute Engine
    instance.

    Attributes:
        display_name (str):
            Name of a Compute Engine instance.
        uri (str):
            URI of a Compute Engine instance.
        interface (str):
            Name of the network interface of a Compute
            Engine instance.
        network_uri (str):
            URI of a Compute Engine network.
        internal_ip (str):
            Internal IP address of the network interface.
        external_ip (str):
            External IP address of the network interface.
        network_tags (MutableSequence[str]):
            Network tags configured on the instance.
        service_account (str):
            Service account authorized for the instance.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    interface: str = proto.Field(
        proto.STRING,
        number=3,
    )
    network_uri: str = proto.Field(
        proto.STRING,
        number=4,
    )
    internal_ip: str = proto.Field(
        proto.STRING,
        number=5,
    )
    external_ip: str = proto.Field(
        proto.STRING,
        number=6,
    )
    network_tags: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    service_account: str = proto.Field(
        proto.STRING,
        number=8,
    )


class NetworkInfo(proto.Message):
    r"""For display only. Metadata associated with a Compute Engine
    network.

    Attributes:
        display_name (str):
            Name of a Compute Engine network.
        uri (str):
            URI of a Compute Engine network.
        matched_ip_range (str):
            The IP range that matches the test.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    matched_ip_range: str = proto.Field(
        proto.STRING,
        number=4,
    )


class FirewallInfo(proto.Message):
    r"""For display only. Metadata associated with a VPC firewall
    rule, an implied VPC firewall rule, or a hierarchical firewall
    policy rule.

    Attributes:
        display_name (str):
            The display name of the VPC firewall rule.
            This field is not applicable to hierarchical
            firewall policy rules.
        uri (str):
            The URI of the VPC firewall rule. This field
            is not applicable to implied firewall rules or
            hierarchical firewall policy rules.
        direction (str):
            Possible values: INGRESS, EGRESS
        action (str):
            Possible values: ALLOW, DENY
        priority (int):
            The priority of the firewall rule.
        network_uri (str):
            The URI of the VPC network that the firewall
            rule is associated with. This field is not
            applicable to hierarchical firewall policy
            rules.
        target_tags (MutableSequence[str]):
            The target tags defined by the VPC firewall
            rule. This field is not applicable to
            hierarchical firewall policy rules.
        target_service_accounts (MutableSequence[str]):
            The target service accounts specified by the
            firewall rule.
        policy (str):
            The hierarchical firewall policy that this
            rule is associated with. This field is not
            applicable to VPC firewall rules.
        firewall_rule_type (google.cloud.network_management_v1.types.FirewallInfo.FirewallRuleType):
            The firewall rule's type.
    """

    class FirewallRuleType(proto.Enum):
        r"""The firewall rule's type.

        Values:
            FIREWALL_RULE_TYPE_UNSPECIFIED (0):
                Unspecified type.
            HIERARCHICAL_FIREWALL_POLICY_RULE (1):
                Hierarchical firewall policy rule. For details, see
                `Hierarchical firewall policies
                overview <https://cloud.google.com/vpc/docs/firewall-policies>`__.
            VPC_FIREWALL_RULE (2):
                VPC firewall rule. For details, see `VPC firewall rules
                overview <https://cloud.google.com/vpc/docs/firewalls>`__.
            IMPLIED_VPC_FIREWALL_RULE (3):
                Implied VPC firewall rule. For details, see `Implied
                rules <https://cloud.google.com/vpc/docs/firewalls#default_firewall_rules>`__.
            SERVERLESS_VPC_ACCESS_MANAGED_FIREWALL_RULE (4):
                Implicit firewall rules that are managed by serverless VPC
                access to allow ingress access. They are not visible in the
                Google Cloud console. For details, see `VPC connector's
                implicit
                rules <https://cloud.google.com/functions/docs/networking/connecting-vpc#restrict-access>`__.
            NETWORK_FIREWALL_POLICY_RULE (5):
                Global network firewall policy rule. For details, see
                `Network firewall
                policies <https://cloud.google.com/vpc/docs/network-firewall-policies>`__.
            NETWORK_REGIONAL_FIREWALL_POLICY_RULE (6):
                Regional network firewall policy rule. For details, see
                `Regional network firewall
                policies <https://cloud.google.com/firewall/docs/regional-firewall-policies>`__.
        """
        FIREWALL_RULE_TYPE_UNSPECIFIED = 0
        HIERARCHICAL_FIREWALL_POLICY_RULE = 1
        VPC_FIREWALL_RULE = 2
        IMPLIED_VPC_FIREWALL_RULE = 3
        SERVERLESS_VPC_ACCESS_MANAGED_FIREWALL_RULE = 4
        NETWORK_FIREWALL_POLICY_RULE = 5
        NETWORK_REGIONAL_FIREWALL_POLICY_RULE = 6

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    direction: str = proto.Field(
        proto.STRING,
        number=3,
    )
    action: str = proto.Field(
        proto.STRING,
        number=4,
    )
    priority: int = proto.Field(
        proto.INT32,
        number=5,
    )
    network_uri: str = proto.Field(
        proto.STRING,
        number=6,
    )
    target_tags: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    target_service_accounts: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=8,
    )
    policy: str = proto.Field(
        proto.STRING,
        number=9,
    )
    firewall_rule_type: FirewallRuleType = proto.Field(
        proto.ENUM,
        number=10,
        enum=FirewallRuleType,
    )


class RouteInfo(proto.Message):
    r"""For display only. Metadata associated with a Compute Engine
    route.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        route_type (google.cloud.network_management_v1.types.RouteInfo.RouteType):
            Type of route.
        next_hop_type (google.cloud.network_management_v1.types.RouteInfo.NextHopType):
            Type of next hop.
        route_scope (google.cloud.network_management_v1.types.RouteInfo.RouteScope):
            Indicates where route is applicable.
        display_name (str):
            Name of a route.
        uri (str):
            URI of a route.
            Dynamic, peering static and peering dynamic
            routes do not have an URI. Advertised route from
            Google Cloud VPC to on-premises network also
            does not have an URI.
        dest_ip_range (str):
            Destination IP range of the route.
        next_hop (str):
            Next hop of the route.
        network_uri (str):
            URI of a Compute Engine network. NETWORK
            routes only.
        priority (int):
            Priority of the route.
        instance_tags (MutableSequence[str]):
            Instance tags of the route.
        src_ip_range (str):
            Source IP address range of the route. Policy
            based routes only.
        dest_port_ranges (MutableSequence[str]):
            Destination port ranges of the route. Policy
            based routes only.
        src_port_ranges (MutableSequence[str]):
            Source port ranges of the route. Policy based
            routes only.
        protocols (MutableSequence[str]):
            Protocols of the route. Policy based routes
            only.
        ncc_hub_uri (str):
            URI of a NCC Hub. NCC_HUB routes only.

            This field is a member of `oneof`_ ``_ncc_hub_uri``.
        ncc_spoke_uri (str):
            URI of a NCC Spoke. NCC_HUB routes only.

            This field is a member of `oneof`_ ``_ncc_spoke_uri``.
    """

    class RouteType(proto.Enum):
        r"""Type of route:

        Values:
            ROUTE_TYPE_UNSPECIFIED (0):
                Unspecified type. Default value.
            SUBNET (1):
                Route is a subnet route automatically created
                by the system.
            STATIC (2):
                Static route created by the user, including
                the default route to the internet.
            DYNAMIC (3):
                Dynamic route exchanged between BGP peers.
            PEERING_SUBNET (4):
                A subnet route received from peering network.
            PEERING_STATIC (5):
                A static route received from peering network.
            PEERING_DYNAMIC (6):
                A dynamic route received from peering
                network.
            POLICY_BASED (7):
                Policy based route.
        """
        ROUTE_TYPE_UNSPECIFIED = 0
        SUBNET = 1
        STATIC = 2
        DYNAMIC = 3
        PEERING_SUBNET = 4
        PEERING_STATIC = 5
        PEERING_DYNAMIC = 6
        POLICY_BASED = 7

    class NextHopType(proto.Enum):
        r"""Type of next hop:

        Values:
            NEXT_HOP_TYPE_UNSPECIFIED (0):
                Unspecified type. Default value.
            NEXT_HOP_IP (1):
                Next hop is an IP address.
            NEXT_HOP_INSTANCE (2):
                Next hop is a Compute Engine instance.
            NEXT_HOP_NETWORK (3):
                Next hop is a VPC network gateway.
            NEXT_HOP_PEERING (4):
                Next hop is a peering VPC.
            NEXT_HOP_INTERCONNECT (5):
                Next hop is an interconnect.
            NEXT_HOP_VPN_TUNNEL (6):
                Next hop is a VPN tunnel.
            NEXT_HOP_VPN_GATEWAY (7):
                Next hop is a VPN gateway. This scenario only
                happens when tracing connectivity from an
                on-premises network to Google Cloud through a
                VPN. The analysis simulates a packet departing
                from the on-premises network through a VPN
                tunnel and arriving at a Cloud VPN gateway.
            NEXT_HOP_INTERNET_GATEWAY (8):
                Next hop is an internet gateway.
            NEXT_HOP_BLACKHOLE (9):
                Next hop is blackhole; that is, the next hop
                either does not exist or is not running.
            NEXT_HOP_ILB (10):
                Next hop is the forwarding rule of an
                Internal Load Balancer.
            NEXT_HOP_ROUTER_APPLIANCE (11):
                Next hop is a `router appliance
                instance <https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/ra-overview>`__.
            NEXT_HOP_NCC_HUB (12):
                Next hop is an NCC hub.
        """
        NEXT_HOP_TYPE_UNSPECIFIED = 0
        NEXT_HOP_IP = 1
        NEXT_HOP_INSTANCE = 2
        NEXT_HOP_NETWORK = 3
        NEXT_HOP_PEERING = 4
        NEXT_HOP_INTERCONNECT = 5
        NEXT_HOP_VPN_TUNNEL = 6
        NEXT_HOP_VPN_GATEWAY = 7
        NEXT_HOP_INTERNET_GATEWAY = 8
        NEXT_HOP_BLACKHOLE = 9
        NEXT_HOP_ILB = 10
        NEXT_HOP_ROUTER_APPLIANCE = 11
        NEXT_HOP_NCC_HUB = 12

    class RouteScope(proto.Enum):
        r"""Indicates where routes are applicable.

        Values:
            ROUTE_SCOPE_UNSPECIFIED (0):
                Unspecified scope. Default value.
            NETWORK (1):
                Route is applicable to packets in Network.
            NCC_HUB (2):
                Route is applicable to packets using NCC
                Hub's routing table.
        """
        ROUTE_SCOPE_UNSPECIFIED = 0
        NETWORK = 1
        NCC_HUB = 2

    route_type: RouteType = proto.Field(
        proto.ENUM,
        number=8,
        enum=RouteType,
    )
    next_hop_type: NextHopType = proto.Field(
        proto.ENUM,
        number=9,
        enum=NextHopType,
    )
    route_scope: RouteScope = proto.Field(
        proto.ENUM,
        number=14,
        enum=RouteScope,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    dest_ip_range: str = proto.Field(
        proto.STRING,
        number=3,
    )
    next_hop: str = proto.Field(
        proto.STRING,
        number=4,
    )
    network_uri: str = proto.Field(
        proto.STRING,
        number=5,
    )
    priority: int = proto.Field(
        proto.INT32,
        number=6,
    )
    instance_tags: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    src_ip_range: str = proto.Field(
        proto.STRING,
        number=10,
    )
    dest_port_ranges: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=11,
    )
    src_port_ranges: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=12,
    )
    protocols: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=13,
    )
    ncc_hub_uri: str = proto.Field(
        proto.STRING,
        number=15,
        optional=True,
    )
    ncc_spoke_uri: str = proto.Field(
        proto.STRING,
        number=16,
        optional=True,
    )


class GoogleServiceInfo(proto.Message):
    r"""For display only. Details of a Google Service sending packets to a
    VPC network. Although the source IP might be a publicly routable
    address, some Google Services use special routes within Google
    production infrastructure to reach Compute Engine Instances.
    https://cloud.google.com/vpc/docs/routes#special_return_paths

    Attributes:
        source_ip (str):
            Source IP address.
        google_service_type (google.cloud.network_management_v1.types.GoogleServiceInfo.GoogleServiceType):
            Recognized type of a Google Service.
    """

    class GoogleServiceType(proto.Enum):
        r"""Recognized type of a Google Service.

        Values:
            GOOGLE_SERVICE_TYPE_UNSPECIFIED (0):
                Unspecified Google Service. Includes most of
                Google APIs and services.
            IAP (1):
                Identity aware proxy.
                https://cloud.google.com/iap/docs/using-tcp-forwarding
            GFE_PROXY_OR_HEALTH_CHECK_PROBER (2):
                One of two services sharing IP ranges:

                -  Load Balancer proxy
                -  Centralized Health Check prober
                   https://cloud.google.com/load-balancing/docs/firewall-rules
            CLOUD_DNS (3):
                Connectivity from Cloud DNS to forwarding
                targets or alternate name servers that use
                private routing.
                https://cloud.google.com/dns/docs/zones/forwarding-zones#firewall-rules
                https://cloud.google.com/dns/docs/policies#firewall-rules
        """
        GOOGLE_SERVICE_TYPE_UNSPECIFIED = 0
        IAP = 1
        GFE_PROXY_OR_HEALTH_CHECK_PROBER = 2
        CLOUD_DNS = 3

    source_ip: str = proto.Field(
        proto.STRING,
        number=1,
    )
    google_service_type: GoogleServiceType = proto.Field(
        proto.ENUM,
        number=2,
        enum=GoogleServiceType,
    )


class ForwardingRuleInfo(proto.Message):
    r"""For display only. Metadata associated with a Compute Engine
    forwarding rule.

    Attributes:
        display_name (str):
            Name of a Compute Engine forwarding rule.
        uri (str):
            URI of a Compute Engine forwarding rule.
        matched_protocol (str):
            Protocol defined in the forwarding rule that
            matches the test.
        matched_port_range (str):
            Port range defined in the forwarding rule
            that matches the test.
        vip (str):
            VIP of the forwarding rule.
        target (str):
            Target type of the forwarding rule.
        network_uri (str):
            Network URI. Only valid for Internal Load
            Balancer.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    matched_protocol: str = proto.Field(
        proto.STRING,
        number=3,
    )
    matched_port_range: str = proto.Field(
        proto.STRING,
        number=6,
    )
    vip: str = proto.Field(
        proto.STRING,
        number=4,
    )
    target: str = proto.Field(
        proto.STRING,
        number=5,
    )
    network_uri: str = proto.Field(
        proto.STRING,
        number=7,
    )


class LoadBalancerInfo(proto.Message):
    r"""For display only. Metadata associated with a load balancer.

    Attributes:
        load_balancer_type (google.cloud.network_management_v1.types.LoadBalancerInfo.LoadBalancerType):
            Type of the load balancer.
        health_check_uri (str):
            URI of the health check for the load
            balancer.
        backends (MutableSequence[google.cloud.network_management_v1.types.LoadBalancerBackend]):
            Information for the loadbalancer backends.
        backend_type (google.cloud.network_management_v1.types.LoadBalancerInfo.BackendType):
            Type of load balancer's backend
            configuration.
        backend_uri (str):
            Backend configuration URI.
    """

    class LoadBalancerType(proto.Enum):
        r"""The type definition for a load balancer:

        Values:
            LOAD_BALANCER_TYPE_UNSPECIFIED (0):
                Type is unspecified.
            INTERNAL_TCP_UDP (1):
                Internal TCP/UDP load balancer.
            NETWORK_TCP_UDP (2):
                Network TCP/UDP load balancer.
            HTTP_PROXY (3):
                HTTP(S) proxy load balancer.
            TCP_PROXY (4):
                TCP proxy load balancer.
            SSL_PROXY (5):
                SSL proxy load balancer.
        """
        LOAD_BALANCER_TYPE_UNSPECIFIED = 0
        INTERNAL_TCP_UDP = 1
        NETWORK_TCP_UDP = 2
        HTTP_PROXY = 3
        TCP_PROXY = 4
        SSL_PROXY = 5

    class BackendType(proto.Enum):
        r"""The type definition for a load balancer backend
        configuration:

        Values:
            BACKEND_TYPE_UNSPECIFIED (0):
                Type is unspecified.
            BACKEND_SERVICE (1):
                Backend Service as the load balancer's
                backend.
            TARGET_POOL (2):
                Target Pool as the load balancer's backend.
            TARGET_INSTANCE (3):
                Target Instance as the load balancer's
                backend.
        """
        BACKEND_TYPE_UNSPECIFIED = 0
        BACKEND_SERVICE = 1
        TARGET_POOL = 2
        TARGET_INSTANCE = 3

    load_balancer_type: LoadBalancerType = proto.Field(
        proto.ENUM,
        number=1,
        enum=LoadBalancerType,
    )
    health_check_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    backends: MutableSequence["LoadBalancerBackend"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="LoadBalancerBackend",
    )
    backend_type: BackendType = proto.Field(
        proto.ENUM,
        number=4,
        enum=BackendType,
    )
    backend_uri: str = proto.Field(
        proto.STRING,
        number=5,
    )


class LoadBalancerBackend(proto.Message):
    r"""For display only. Metadata associated with a specific load
    balancer backend.

    Attributes:
        display_name (str):
            Name of a Compute Engine instance or network
            endpoint.
        uri (str):
            URI of a Compute Engine instance or network
            endpoint.
        health_check_firewall_state (google.cloud.network_management_v1.types.LoadBalancerBackend.HealthCheckFirewallState):
            State of the health check firewall
            configuration.
        health_check_allowing_firewall_rules (MutableSequence[str]):
            A list of firewall rule URIs allowing probes
            from health check IP ranges.
        health_check_blocking_firewall_rules (MutableSequence[str]):
            A list of firewall rule URIs blocking probes
            from health check IP ranges.
    """

    class HealthCheckFirewallState(proto.Enum):
        r"""State of a health check firewall configuration:

        Values:
            HEALTH_CHECK_FIREWALL_STATE_UNSPECIFIED (0):
                State is unspecified. Default state if not
                populated.
            CONFIGURED (1):
                There are configured firewall rules to allow
                health check probes to the backend.
            MISCONFIGURED (2):
                There are firewall rules configured to allow
                partial health check ranges or block all health
                check ranges. If a health check probe is sent
                from denied IP ranges, the health check to the
                backend will fail. Then, the backend will be
                marked unhealthy and will not receive traffic
                sent to the load balancer.
        """
        HEALTH_CHECK_FIREWALL_STATE_UNSPECIFIED = 0
        CONFIGURED = 1
        MISCONFIGURED = 2

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    health_check_firewall_state: HealthCheckFirewallState = proto.Field(
        proto.ENUM,
        number=3,
        enum=HealthCheckFirewallState,
    )
    health_check_allowing_firewall_rules: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    health_check_blocking_firewall_rules: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )


class VpnGatewayInfo(proto.Message):
    r"""For display only. Metadata associated with a Compute Engine
    VPN gateway.

    Attributes:
        display_name (str):
            Name of a VPN gateway.
        uri (str):
            URI of a VPN gateway.
        network_uri (str):
            URI of a Compute Engine network where the VPN
            gateway is configured.
        ip_address (str):
            IP address of the VPN gateway.
        vpn_tunnel_uri (str):
            A VPN tunnel that is associated with this VPN
            gateway. There may be multiple VPN tunnels
            configured on a VPN gateway, and only the one
            relevant to the test is displayed.
        region (str):
            Name of a Google Cloud region where this VPN
            gateway is configured.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    network_uri: str = proto.Field(
        proto.STRING,
        number=3,
    )
    ip_address: str = proto.Field(
        proto.STRING,
        number=4,
    )
    vpn_tunnel_uri: str = proto.Field(
        proto.STRING,
        number=5,
    )
    region: str = proto.Field(
        proto.STRING,
        number=6,
    )


class VpnTunnelInfo(proto.Message):
    r"""For display only. Metadata associated with a Compute Engine
    VPN tunnel.

    Attributes:
        display_name (str):
            Name of a VPN tunnel.
        uri (str):
            URI of a VPN tunnel.
        source_gateway (str):
            URI of the VPN gateway at local end of the
            tunnel.
        remote_gateway (str):
            URI of a VPN gateway at remote end of the
            tunnel.
        remote_gateway_ip (str):
            Remote VPN gateway's IP address.
        source_gateway_ip (str):
            Local VPN gateway's IP address.
        network_uri (str):
            URI of a Compute Engine network where the VPN
            tunnel is configured.
        region (str):
            Name of a Google Cloud region where this VPN
            tunnel is configured.
        routing_type (google.cloud.network_management_v1.types.VpnTunnelInfo.RoutingType):
            Type of the routing policy.
    """

    class RoutingType(proto.Enum):
        r"""Types of VPN routing policy. For details, refer to `Networks and
        Tunnel
        routing <https://cloud.google.com/network-connectivity/docs/vpn/concepts/choosing-networks-routing/>`__.

        Values:
            ROUTING_TYPE_UNSPECIFIED (0):
                Unspecified type. Default value.
            ROUTE_BASED (1):
                Route based VPN.
            POLICY_BASED (2):
                Policy based routing.
            DYNAMIC (3):
                Dynamic (BGP) routing.
        """
        ROUTING_TYPE_UNSPECIFIED = 0
        ROUTE_BASED = 1
        POLICY_BASED = 2
        DYNAMIC = 3

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    source_gateway: str = proto.Field(
        proto.STRING,
        number=3,
    )
    remote_gateway: str = proto.Field(
        proto.STRING,
        number=4,
    )
    remote_gateway_ip: str = proto.Field(
        proto.STRING,
        number=5,
    )
    source_gateway_ip: str = proto.Field(
        proto.STRING,
        number=6,
    )
    network_uri: str = proto.Field(
        proto.STRING,
        number=7,
    )
    region: str = proto.Field(
        proto.STRING,
        number=8,
    )
    routing_type: RoutingType = proto.Field(
        proto.ENUM,
        number=9,
        enum=RoutingType,
    )


class EndpointInfo(proto.Message):
    r"""For display only. The specification of the endpoints for the
    test. EndpointInfo is derived from source and destination
    Endpoint and validated by the backend data plane model.

    Attributes:
        source_ip (str):
            Source IP address.
        destination_ip (str):
            Destination IP address.
        protocol (str):
            IP protocol in string format, for example:
            "TCP", "UDP", "ICMP".
        source_port (int):
            Source port. Only valid when protocol is TCP
            or UDP.
        destination_port (int):
            Destination port. Only valid when protocol is
            TCP or UDP.
        source_network_uri (str):
            URI of the network where this packet
            originates from.
        destination_network_uri (str):
            URI of the network where this packet is sent
            to.
        source_agent_uri (str):
            URI of the source telemetry agent this packet
            originates from.
    """

    source_ip: str = proto.Field(
        proto.STRING,
        number=1,
    )
    destination_ip: str = proto.Field(
        proto.STRING,
        number=2,
    )
    protocol: str = proto.Field(
        proto.STRING,
        number=3,
    )
    source_port: int = proto.Field(
        proto.INT32,
        number=4,
    )
    destination_port: int = proto.Field(
        proto.INT32,
        number=5,
    )
    source_network_uri: str = proto.Field(
        proto.STRING,
        number=6,
    )
    destination_network_uri: str = proto.Field(
        proto.STRING,
        number=7,
    )
    source_agent_uri: str = proto.Field(
        proto.STRING,
        number=8,
    )


class DeliverInfo(proto.Message):
    r"""Details of the final state "deliver" and associated resource.

    Attributes:
        target (google.cloud.network_management_v1.types.DeliverInfo.Target):
            Target type where the packet is delivered to.
        resource_uri (str):
            URI of the resource that the packet is
            delivered to.
    """

    class Target(proto.Enum):
        r"""Deliver target types:

        Values:
            TARGET_UNSPECIFIED (0):
                Target not specified.
            INSTANCE (1):
                Target is a Compute Engine instance.
            INTERNET (2):
                Target is the internet.
            GOOGLE_API (3):
                Target is a Google API.
            GKE_MASTER (4):
                Target is a Google Kubernetes Engine cluster
                master.
            CLOUD_SQL_INSTANCE (5):
                Target is a Cloud SQL instance.
            PSC_PUBLISHED_SERVICE (6):
                Target is a published service that uses `Private Service
                Connect <https://cloud.google.com/vpc/docs/configure-private-service-connect-services>`__.
            PSC_GOOGLE_API (7):
                Target is all Google APIs that use `Private Service
                Connect <https://cloud.google.com/vpc/docs/configure-private-service-connect-apis>`__.
            PSC_VPC_SC (8):
                Target is a VPC-SC that uses `Private Service
                Connect <https://cloud.google.com/vpc/docs/configure-private-service-connect-apis>`__.
            SERVERLESS_NEG (9):
                Target is a serverless network endpoint
                group.
        """
        TARGET_UNSPECIFIED = 0
        INSTANCE = 1
        INTERNET = 2
        GOOGLE_API = 3
        GKE_MASTER = 4
        CLOUD_SQL_INSTANCE = 5
        PSC_PUBLISHED_SERVICE = 6
        PSC_GOOGLE_API = 7
        PSC_VPC_SC = 8
        SERVERLESS_NEG = 9

    target: Target = proto.Field(
        proto.ENUM,
        number=1,
        enum=Target,
    )
    resource_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ForwardInfo(proto.Message):
    r"""Details of the final state "forward" and associated resource.

    Attributes:
        target (google.cloud.network_management_v1.types.ForwardInfo.Target):
            Target type where this packet is forwarded
            to.
        resource_uri (str):
            URI of the resource that the packet is
            forwarded to.
    """

    class Target(proto.Enum):
        r"""Forward target types.

        Values:
            TARGET_UNSPECIFIED (0):
                Target not specified.
            PEERING_VPC (1):
                Forwarded to a VPC peering network.
            VPN_GATEWAY (2):
                Forwarded to a Cloud VPN gateway.
            INTERCONNECT (3):
                Forwarded to a Cloud Interconnect connection.
            GKE_MASTER (4):
                Forwarded to a Google Kubernetes Engine
                Container cluster master.
            IMPORTED_CUSTOM_ROUTE_NEXT_HOP (5):
                Forwarded to the next hop of a custom route
                imported from a peering VPC.
            CLOUD_SQL_INSTANCE (6):
                Forwarded to a Cloud SQL instance.
            ANOTHER_PROJECT (7):
                Forwarded to a VPC network in another
                project.
            NCC_HUB (8):
                Forwarded to an NCC Hub.
        """
        TARGET_UNSPECIFIED = 0
        PEERING_VPC = 1
        VPN_GATEWAY = 2
        INTERCONNECT = 3
        GKE_MASTER = 4
        IMPORTED_CUSTOM_ROUTE_NEXT_HOP = 5
        CLOUD_SQL_INSTANCE = 6
        ANOTHER_PROJECT = 7
        NCC_HUB = 8

    target: Target = proto.Field(
        proto.ENUM,
        number=1,
        enum=Target,
    )
    resource_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AbortInfo(proto.Message):
    r"""Details of the final state "abort" and associated resource.

    Attributes:
        cause (google.cloud.network_management_v1.types.AbortInfo.Cause):
            Causes that the analysis is aborted.
        resource_uri (str):
            URI of the resource that caused the abort.
        projects_missing_permission (MutableSequence[str]):
            List of project IDs that the user has specified in the
            request but does not have permission to access network
            configs. Analysis is aborted in this case with the
            PERMISSION_DENIED cause.
    """

    class Cause(proto.Enum):
        r"""Abort cause types:

        Values:
            CAUSE_UNSPECIFIED (0):
                Cause is unspecified.
            UNKNOWN_NETWORK (1):
                Aborted due to unknown network.
                The reachability analysis cannot proceed because
                the user does not have access to the host
                project's network configurations, including
                firewall rules and routes. This happens when the
                project is a service project and the endpoints
                being traced are in the host project's network.
            UNKNOWN_IP (2):
                Aborted because the IP address(es) are
                unknown.
            UNKNOWN_PROJECT (3):
                Aborted because no project information can be
                derived from the test input.
            PERMISSION_DENIED (4):
                Aborted because the user lacks the permission
                to access all or part of the network
                configurations required to run the test.
            NO_SOURCE_LOCATION (5):
                Aborted because no valid source endpoint is
                derived from the input test request.
            INVALID_ARGUMENT (6):
                Aborted because the source and/or destination
                endpoint specified in the test are invalid. The
                possible reasons that an endpoint is invalid
                include: malformed IP address; nonexistent
                instance or network URI; IP address not in the
                range of specified network URI; and instance not
                owning the network interface in the specified
                network.
            NO_EXTERNAL_IP (7):
                Aborted because traffic is sent from a public
                IP to an instance without an external IP.
            UNINTENDED_DESTINATION (8):
                Aborted because none of the traces matches
                destination information specified in the input
                test request.
            TRACE_TOO_LONG (9):
                Aborted because the number of steps in the
                trace exceeding a certain limit which may be
                caused by routing loop.
            INTERNAL_ERROR (10):
                Aborted due to internal server error.
            SOURCE_ENDPOINT_NOT_FOUND (11):
                Aborted because the source endpoint could not
                be found.
            MISMATCHED_SOURCE_NETWORK (12):
                Aborted because the source network does not
                match the source endpoint.
            DESTINATION_ENDPOINT_NOT_FOUND (13):
                Aborted because the destination endpoint
                could not be found.
            MISMATCHED_DESTINATION_NETWORK (14):
                Aborted because the destination network does
                not match the destination endpoint.
            UNSUPPORTED (15):
                Aborted because the test scenario is not
                supported.
            MISMATCHED_IP_VERSION (16):
                Aborted because the source and destination
                resources have no common IP version.
            GKE_KONNECTIVITY_PROXY_UNSUPPORTED (17):
                Aborted because the connection between the
                control plane and the node of the source cluster
                is initiated by the node and managed by the
                Konnectivity proxy.
            RESOURCE_CONFIG_NOT_FOUND (18):
                Aborted because expected resource
                configuration was missing.
            GOOGLE_MANAGED_SERVICE_AMBIGUOUS_PSC_ENDPOINT (19):
                Aborted because a PSC endpoint selection for
                the Google-managed service is ambiguous (several
                PSC endpoints satisfy test input).
            SOURCE_PSC_CLOUD_SQL_UNSUPPORTED (20):
                Aborted because tests with a PSC-based Cloud
                SQL instance as a source are not supported.
            SOURCE_FORWARDING_RULE_UNSUPPORTED (21):
                Aborted because tests with a forwarding rule
                as a source are not supported.
        """
        CAUSE_UNSPECIFIED = 0
        UNKNOWN_NETWORK = 1
        UNKNOWN_IP = 2
        UNKNOWN_PROJECT = 3
        PERMISSION_DENIED = 4
        NO_SOURCE_LOCATION = 5
        INVALID_ARGUMENT = 6
        NO_EXTERNAL_IP = 7
        UNINTENDED_DESTINATION = 8
        TRACE_TOO_LONG = 9
        INTERNAL_ERROR = 10
        SOURCE_ENDPOINT_NOT_FOUND = 11
        MISMATCHED_SOURCE_NETWORK = 12
        DESTINATION_ENDPOINT_NOT_FOUND = 13
        MISMATCHED_DESTINATION_NETWORK = 14
        UNSUPPORTED = 15
        MISMATCHED_IP_VERSION = 16
        GKE_KONNECTIVITY_PROXY_UNSUPPORTED = 17
        RESOURCE_CONFIG_NOT_FOUND = 18
        GOOGLE_MANAGED_SERVICE_AMBIGUOUS_PSC_ENDPOINT = 19
        SOURCE_PSC_CLOUD_SQL_UNSUPPORTED = 20
        SOURCE_FORWARDING_RULE_UNSUPPORTED = 21

    cause: Cause = proto.Field(
        proto.ENUM,
        number=1,
        enum=Cause,
    )
    resource_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    projects_missing_permission: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class DropInfo(proto.Message):
    r"""Details of the final state "drop" and associated resource.

    Attributes:
        cause (google.cloud.network_management_v1.types.DropInfo.Cause):
            Cause that the packet is dropped.
        resource_uri (str):
            URI of the resource that caused the drop.
    """

    class Cause(proto.Enum):
        r"""Drop cause types:

        Values:
            CAUSE_UNSPECIFIED (0):
                Cause is unspecified.
            UNKNOWN_EXTERNAL_ADDRESS (1):
                Destination external address cannot be
                resolved to a known target. If the address is
                used in a Google Cloud project, provide the
                project ID as test input.
            FOREIGN_IP_DISALLOWED (2):
                A Compute Engine instance can only send or receive a packet
                with a foreign IP address if ip_forward is enabled.
            FIREWALL_RULE (3):
                Dropped due to a firewall rule, unless
                allowed due to connection tracking.
            NO_ROUTE (4):
                Dropped due to no routes.
            ROUTE_BLACKHOLE (5):
                Dropped due to invalid route. Route's next
                hop is a blackhole.
            ROUTE_WRONG_NETWORK (6):
                Packet is sent to a wrong (unintended)
                network. Example: you trace a packet from
                VM1:Network1 to VM2:Network2, however, the route
                configured in Network1 sends the packet destined
                for VM2's IP addresss to Network3.
            PRIVATE_TRAFFIC_TO_INTERNET (7):
                Packet with internal destination address sent
                to the internet gateway.
            PRIVATE_GOOGLE_ACCESS_DISALLOWED (8):
                Instance with only an internal IP address
                tries to access Google API and services, but
                private Google access is not enabled.
            NO_EXTERNAL_ADDRESS (9):
                Instance with only an internal IP address
                tries to access external hosts, but Cloud NAT is
                not enabled in the subnet, unless special
                configurations on a VM allow this connection.
            UNKNOWN_INTERNAL_ADDRESS (10):
                Destination internal address cannot be
                resolved to a known target. If this is a shared
                VPC scenario, verify if the service project ID
                is provided as test input. Otherwise, verify if
                the IP address is being used in the project.
            FORWARDING_RULE_MISMATCH (11):
                Forwarding rule's protocol and ports do not
                match the packet header.
            FORWARDING_RULE_REGION_MISMATCH (25):
                Packet could be dropped because it was sent
                from a different region to a regional forwarding
                without global access.
            FORWARDING_RULE_NO_INSTANCES (12):
                Forwarding rule does not have backends
                configured.
            FIREWALL_BLOCKING_LOAD_BALANCER_BACKEND_HEALTH_CHECK (13):
                Firewalls block the health check probes to the backends and
                cause the backends to be unavailable for traffic from the
                load balancer. For more details, see `Health check firewall
                rules <https://cloud.google.com/load-balancing/docs/health-checks#firewall_rules>`__.
            INSTANCE_NOT_RUNNING (14):
                Packet is sent from or to a Compute Engine
                instance that is not in a running state.
            GKE_CLUSTER_NOT_RUNNING (27):
                Packet sent from or to a GKE cluster that is
                not in running state.
            CLOUD_SQL_INSTANCE_NOT_RUNNING (28):
                Packet sent from or to a Cloud SQL instance
                that is not in running state.
            TRAFFIC_TYPE_BLOCKED (15):
                The type of traffic is blocked and the user cannot configure
                a firewall rule to enable it. See `Always blocked
                traffic <https://cloud.google.com/vpc/docs/firewalls#blockedtraffic>`__
                for more details.
            GKE_MASTER_UNAUTHORIZED_ACCESS (16):
                Access to Google Kubernetes Engine cluster master's endpoint
                is not authorized. See `Access to the cluster
                endpoints <https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters#access_to_the_cluster_endpoints>`__
                for more details.
            CLOUD_SQL_INSTANCE_UNAUTHORIZED_ACCESS (17):
                Access to the Cloud SQL instance endpoint is not authorized.
                See `Authorizing with authorized
                networks <https://cloud.google.com/sql/docs/mysql/authorize-networks>`__
                for more details.
            DROPPED_INSIDE_GKE_SERVICE (18):
                Packet was dropped inside Google Kubernetes
                Engine Service.
            DROPPED_INSIDE_CLOUD_SQL_SERVICE (19):
                Packet was dropped inside Cloud SQL Service.
            GOOGLE_MANAGED_SERVICE_NO_PEERING (20):
                Packet was dropped because there is no
                peering between the originating network and the
                Google Managed Services Network.
            GOOGLE_MANAGED_SERVICE_NO_PSC_ENDPOINT (38):
                Packet was dropped because the Google-managed
                service uses Private Service Connect (PSC), but
                the PSC endpoint is not found in the project.
            GKE_PSC_ENDPOINT_MISSING (36):
                Packet was dropped because the GKE cluster
                uses Private Service Connect (PSC), but the PSC
                endpoint is not found in the project.
            CLOUD_SQL_INSTANCE_NO_IP_ADDRESS (21):
                Packet was dropped because the Cloud SQL
                instance has neither a private nor a public IP
                address.
            GKE_CONTROL_PLANE_REGION_MISMATCH (30):
                Packet was dropped because a GKE cluster
                private endpoint is unreachable from a region
                different from the cluster's region.
            PUBLIC_GKE_CONTROL_PLANE_TO_PRIVATE_DESTINATION (31):
                Packet sent from a public GKE cluster control
                plane to a private IP address.
            GKE_CONTROL_PLANE_NO_ROUTE (32):
                Packet was dropped because there is no route
                from a GKE cluster control plane to a
                destination network.
            CLOUD_SQL_INSTANCE_NOT_CONFIGURED_FOR_EXTERNAL_TRAFFIC (33):
                Packet sent from a Cloud SQL instance to an
                external IP address is not allowed. The Cloud
                SQL instance is not configured to send packets
                to external IP addresses.
            PUBLIC_CLOUD_SQL_INSTANCE_TO_PRIVATE_DESTINATION (34):
                Packet sent from a Cloud SQL instance with
                only a public IP address to a private IP
                address.
            CLOUD_SQL_INSTANCE_NO_ROUTE (35):
                Packet was dropped because there is no route
                from a Cloud SQL instance to a destination
                network.
            CLOUD_FUNCTION_NOT_ACTIVE (22):
                Packet could be dropped because the Cloud
                Function is not in an active status.
            VPC_CONNECTOR_NOT_SET (23):
                Packet could be dropped because no VPC
                connector is set.
            VPC_CONNECTOR_NOT_RUNNING (24):
                Packet could be dropped because the VPC
                connector is not in a running state.
            PSC_CONNECTION_NOT_ACCEPTED (26):
                The Private Service Connect endpoint is in a
                project that is not approved to connect to the
                service.
            CLOUD_RUN_REVISION_NOT_READY (29):
                Packet sent from a Cloud Run revision that is
                not ready.
            DROPPED_INSIDE_PSC_SERVICE_PRODUCER (37):
                Packet was dropped inside Private Service
                Connect service producer.
            LOAD_BALANCER_HAS_NO_PROXY_SUBNET (39):
                Packet sent to a load balancer, which
                requires a proxy-only subnet and the subnet is
                not found.
        """
        CAUSE_UNSPECIFIED = 0
        UNKNOWN_EXTERNAL_ADDRESS = 1
        FOREIGN_IP_DISALLOWED = 2
        FIREWALL_RULE = 3
        NO_ROUTE = 4
        ROUTE_BLACKHOLE = 5
        ROUTE_WRONG_NETWORK = 6
        PRIVATE_TRAFFIC_TO_INTERNET = 7
        PRIVATE_GOOGLE_ACCESS_DISALLOWED = 8
        NO_EXTERNAL_ADDRESS = 9
        UNKNOWN_INTERNAL_ADDRESS = 10
        FORWARDING_RULE_MISMATCH = 11
        FORWARDING_RULE_REGION_MISMATCH = 25
        FORWARDING_RULE_NO_INSTANCES = 12
        FIREWALL_BLOCKING_LOAD_BALANCER_BACKEND_HEALTH_CHECK = 13
        INSTANCE_NOT_RUNNING = 14
        GKE_CLUSTER_NOT_RUNNING = 27
        CLOUD_SQL_INSTANCE_NOT_RUNNING = 28
        TRAFFIC_TYPE_BLOCKED = 15
        GKE_MASTER_UNAUTHORIZED_ACCESS = 16
        CLOUD_SQL_INSTANCE_UNAUTHORIZED_ACCESS = 17
        DROPPED_INSIDE_GKE_SERVICE = 18
        DROPPED_INSIDE_CLOUD_SQL_SERVICE = 19
        GOOGLE_MANAGED_SERVICE_NO_PEERING = 20
        GOOGLE_MANAGED_SERVICE_NO_PSC_ENDPOINT = 38
        GKE_PSC_ENDPOINT_MISSING = 36
        CLOUD_SQL_INSTANCE_NO_IP_ADDRESS = 21
        GKE_CONTROL_PLANE_REGION_MISMATCH = 30
        PUBLIC_GKE_CONTROL_PLANE_TO_PRIVATE_DESTINATION = 31
        GKE_CONTROL_PLANE_NO_ROUTE = 32
        CLOUD_SQL_INSTANCE_NOT_CONFIGURED_FOR_EXTERNAL_TRAFFIC = 33
        PUBLIC_CLOUD_SQL_INSTANCE_TO_PRIVATE_DESTINATION = 34
        CLOUD_SQL_INSTANCE_NO_ROUTE = 35
        CLOUD_FUNCTION_NOT_ACTIVE = 22
        VPC_CONNECTOR_NOT_SET = 23
        VPC_CONNECTOR_NOT_RUNNING = 24
        PSC_CONNECTION_NOT_ACCEPTED = 26
        CLOUD_RUN_REVISION_NOT_READY = 29
        DROPPED_INSIDE_PSC_SERVICE_PRODUCER = 37
        LOAD_BALANCER_HAS_NO_PROXY_SUBNET = 39

    cause: Cause = proto.Field(
        proto.ENUM,
        number=1,
        enum=Cause,
    )
    resource_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GKEMasterInfo(proto.Message):
    r"""For display only. Metadata associated with a Google
    Kubernetes Engine (GKE) cluster master.

    Attributes:
        cluster_uri (str):
            URI of a GKE cluster.
        cluster_network_uri (str):
            URI of a GKE cluster network.
        internal_ip (str):
            Internal IP address of a GKE cluster master.
        external_ip (str):
            External IP address of a GKE cluster master.
    """

    cluster_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_network_uri: str = proto.Field(
        proto.STRING,
        number=4,
    )
    internal_ip: str = proto.Field(
        proto.STRING,
        number=5,
    )
    external_ip: str = proto.Field(
        proto.STRING,
        number=6,
    )


class CloudSQLInstanceInfo(proto.Message):
    r"""For display only. Metadata associated with a Cloud SQL
    instance.

    Attributes:
        display_name (str):
            Name of a Cloud SQL instance.
        uri (str):
            URI of a Cloud SQL instance.
        network_uri (str):
            URI of a Cloud SQL instance network or empty
            string if the instance does not have one.
        internal_ip (str):
            Internal IP address of a Cloud SQL instance.
        external_ip (str):
            External IP address of a Cloud SQL instance.
        region (str):
            Region in which the Cloud SQL instance is
            running.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    network_uri: str = proto.Field(
        proto.STRING,
        number=4,
    )
    internal_ip: str = proto.Field(
        proto.STRING,
        number=5,
    )
    external_ip: str = proto.Field(
        proto.STRING,
        number=6,
    )
    region: str = proto.Field(
        proto.STRING,
        number=7,
    )


class CloudFunctionInfo(proto.Message):
    r"""For display only. Metadata associated with a Cloud Function.

    Attributes:
        display_name (str):
            Name of a Cloud Function.
        uri (str):
            URI of a Cloud Function.
        location (str):
            Location in which the Cloud Function is
            deployed.
        version_id (int):
            Latest successfully deployed version id of
            the Cloud Function.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    location: str = proto.Field(
        proto.STRING,
        number=3,
    )
    version_id: int = proto.Field(
        proto.INT64,
        number=4,
    )


class CloudRunRevisionInfo(proto.Message):
    r"""For display only. Metadata associated with a Cloud Run
    revision.

    Attributes:
        display_name (str):
            Name of a Cloud Run revision.
        uri (str):
            URI of a Cloud Run revision.
        location (str):
            Location in which this revision is deployed.
        service_uri (str):
            URI of Cloud Run service this revision
            belongs to.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    location: str = proto.Field(
        proto.STRING,
        number=4,
    )
    service_uri: str = proto.Field(
        proto.STRING,
        number=5,
    )


class AppEngineVersionInfo(proto.Message):
    r"""For display only. Metadata associated with an App Engine
    version.

    Attributes:
        display_name (str):
            Name of an App Engine version.
        uri (str):
            URI of an App Engine version.
        runtime (str):
            Runtime of the App Engine version.
        environment (str):
            App Engine execution environment for a
            version.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    runtime: str = proto.Field(
        proto.STRING,
        number=3,
    )
    environment: str = proto.Field(
        proto.STRING,
        number=4,
    )


class VpcConnectorInfo(proto.Message):
    r"""For display only. Metadata associated with a VPC connector.

    Attributes:
        display_name (str):
            Name of a VPC connector.
        uri (str):
            URI of a VPC connector.
        location (str):
            Location in which the VPC connector is
            deployed.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    location: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
