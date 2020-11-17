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


from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.container.v1beta1",
    manifest={
        "NodeConfig",
        "ShieldedInstanceConfig",
        "NodeTaint",
        "MasterAuth",
        "ClientCertificateConfig",
        "AddonsConfig",
        "HttpLoadBalancing",
        "HorizontalPodAutoscaling",
        "KubernetesDashboard",
        "NetworkPolicyConfig",
        "PrivateClusterConfig",
        "IstioConfig",
        "CloudRunConfig",
        "MasterAuthorizedNetworksConfig",
        "LegacyAbac",
        "NetworkPolicy",
        "IPAllocationPolicy",
        "BinaryAuthorization",
        "PodSecurityPolicyConfig",
        "AuthenticatorGroupsConfig",
        "Cluster",
        "ClusterUpdate",
        "Operation",
        "OperationProgress",
        "CreateClusterRequest",
        "GetClusterRequest",
        "UpdateClusterRequest",
        "UpdateNodePoolRequest",
        "SetNodePoolAutoscalingRequest",
        "SetLoggingServiceRequest",
        "SetMonitoringServiceRequest",
        "SetAddonsConfigRequest",
        "SetLocationsRequest",
        "UpdateMasterRequest",
        "SetMasterAuthRequest",
        "DeleteClusterRequest",
        "ListClustersRequest",
        "ListClustersResponse",
        "GetOperationRequest",
        "ListOperationsRequest",
        "CancelOperationRequest",
        "ListOperationsResponse",
        "GetServerConfigRequest",
        "ServerConfig",
        "CreateNodePoolRequest",
        "DeleteNodePoolRequest",
        "ListNodePoolsRequest",
        "GetNodePoolRequest",
        "NodePool",
        "NodeManagement",
        "AutoUpgradeOptions",
        "MaintenancePolicy",
        "MaintenanceWindow",
        "TimeWindow",
        "RecurringTimeWindow",
        "DailyMaintenanceWindow",
        "SetNodePoolManagementRequest",
        "SetNodePoolSizeRequest",
        "RollbackNodePoolUpgradeRequest",
        "ListNodePoolsResponse",
        "ClusterAutoscaling",
        "AutoprovisioningNodePoolDefaults",
        "ResourceLimit",
        "NodePoolAutoscaling",
        "SetLabelsRequest",
        "SetLegacyAbacRequest",
        "StartIPRotationRequest",
        "CompleteIPRotationRequest",
        "AcceleratorConfig",
        "WorkloadMetadataConfig",
        "SetNetworkPolicyRequest",
        "SetMaintenancePolicyRequest",
        "ListLocationsRequest",
        "ListLocationsResponse",
        "Location",
        "StatusCondition",
        "NetworkConfig",
        "ListUsableSubnetworksRequest",
        "ListUsableSubnetworksResponse",
        "UsableSubnetworkSecondaryRange",
        "UsableSubnetwork",
        "VerticalPodAutoscaling",
        "IntraNodeVisibilityConfig",
        "MaxPodsConstraint",
        "DatabaseEncryption",
        "ResourceUsageExportConfig",
    },
)


class NodeConfig(proto.Message):
    r"""Parameters that describe the nodes in a cluster.

    Attributes:
        machine_type (str):
            The name of a Google Compute Engine `machine
            type <https://cloud.google.com/compute/docs/machine-types>`__
            (e.g. ``n1-standard-1``).

            If unspecified, the default machine type is
            ``n1-standard-1``.
        disk_size_gb (int):
            Size of the disk attached to each node,
            specified in GB. The smallest allowed disk size
            is 10GB.
            If unspecified, the default disk size is 100GB.
        oauth_scopes (Sequence[str]):
            The set of Google API scopes to be made available on all of
            the node VMs under the "default" service account.

            The following scopes are recommended, but not required, and
            by default are not included:

            -  ``https://www.googleapis.com/auth/compute`` is required
               for mounting persistent storage on your nodes.
            -  ``https://www.googleapis.com/auth/devstorage.read_only``
               is required for communicating with **gcr.io** (the
               `Google Container
               Registry <https://cloud.google.com/container-registry/>`__).

            If unspecified, no scopes are added, unless Cloud Logging or
            Cloud Monitoring are enabled, in which case their required
            scopes will be added.
        service_account (str):
            The Google Cloud Platform Service Account to
            be used by the node VMs. If no Service Account
            is specified, the "default" service account is
            used.
        metadata (Sequence[~.cluster_service.NodeConfig.MetadataEntry]):
            The metadata key/value pairs assigned to instances in the
            cluster.

            Keys must conform to the regexp [a-zA-Z0-9-_]+ and be less
            than 128 bytes in length. These are reflected as part of a
            URL in the metadata server. Additionally, to avoid
            ambiguity, keys must not conflict with any other metadata
            keys for the project or be one of the reserved keys:
            "cluster-location" "cluster-name" "cluster-uid"
            "configure-sh" "containerd-configure-sh" "enable-oslogin"
            "gci-ensure-gke-docker" "gci-metrics-enabled"
            "gci-update-strategy" "instance-template" "kube-env"
            "startup-script" "user-data" "disable-address-manager"
            "windows-startup-script-ps1" "common-psm1"
            "k8s-node-setup-psm1" "install-ssh-psm1" "user-profile-psm1"
            "serial-port-logging-enable" Values are free-form strings,
            and only have meaning as interpreted by the image running in
            the instance. The only restriction placed on them is that
            each value's size must be less than or equal to 32 KB.

            The total size of all keys and values must be less than 512
            KB.
        image_type (str):
            The image type to use for this node. Note
            that for a given image type, the latest version
            of it will be used.
        labels (Sequence[~.cluster_service.NodeConfig.LabelsEntry]):
            The map of Kubernetes labels (key/value
            pairs) to be applied to each node. These will
            added in addition to any default label(s) that
            Kubernetes may apply to the node.
            In case of conflict in label keys, the applied
            set may differ depending on the Kubernetes
            version -- it's best to assume the behavior is
            undefined and conflicts should be avoided.
            For more information, including usage and the
            valid values, see:
            https://kubernetes.io/docs/concepts/overview/working-
            with-objects/labels/
        local_ssd_count (int):
            The number of local SSD disks to be attached
            to the node.
            The limit for this value is dependent upon the
            maximum number of disks available on a machine
            per zone. See:
            https://cloud.google.com/compute/docs/disks/local-
            ssd for more information.
        tags (Sequence[str]):
            The list of instance tags applied to all
            nodes. Tags are used to identify valid sources
            or targets for network firewalls and are
            specified by the client during cluster or node
            pool creation. Each tag within the list must
            comply with RFC1035.
        preemptible (bool):
            Whether the nodes are created as preemptible
            VM instances. See:
            https://cloud.google.com/compute/docs/instances/preemptible
            for more inforamtion about preemptible VM
            instances.
        accelerators (Sequence[~.cluster_service.AcceleratorConfig]):
            A list of hardware accelerators to be
            attached to each node. See
            https://cloud.google.com/compute/docs/gpus for
            more information about support for GPUs.
        disk_type (str):
            Type of the disk attached to each node (e.g.
            'pd-standard' or 'pd-ssd')
            If unspecified, the default disk type is 'pd-
            standard'
        min_cpu_platform (str):
            Minimum CPU platform to be used by this instance. The
            instance may be scheduled on the specified or newer CPU
            platform. Applicable values are the friendly names of CPU
            platforms, such as minCpuPlatform: "Intel Haswell" or
            minCpuPlatform: "Intel Sandy Bridge". For more information,
            read `how to specify min CPU
            platform <https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform>`__
            To unset the min cpu platform field pass "automatic" as
            field value.
        workload_metadata_config (~.cluster_service.WorkloadMetadataConfig):
            The workload metadata configuration for this
            node.
        taints (Sequence[~.cluster_service.NodeTaint]):
            List of kubernetes taints to be applied to
            each node.
            For more information, including usage and the
            valid values, see:
            https://kubernetes.io/docs/concepts/configuration/taint-
            and-toleration/
        shielded_instance_config (~.cluster_service.ShieldedInstanceConfig):
            Shielded Instance options.
    """

    machine_type = proto.Field(proto.STRING, number=1)

    disk_size_gb = proto.Field(proto.INT32, number=2)

    oauth_scopes = proto.RepeatedField(proto.STRING, number=3)

    service_account = proto.Field(proto.STRING, number=9)

    metadata = proto.MapField(proto.STRING, proto.STRING, number=4)

    image_type = proto.Field(proto.STRING, number=5)

    labels = proto.MapField(proto.STRING, proto.STRING, number=6)

    local_ssd_count = proto.Field(proto.INT32, number=7)

    tags = proto.RepeatedField(proto.STRING, number=8)

    preemptible = proto.Field(proto.BOOL, number=10)

    accelerators = proto.RepeatedField(
        proto.MESSAGE, number=11, message="AcceleratorConfig",
    )

    disk_type = proto.Field(proto.STRING, number=12)

    min_cpu_platform = proto.Field(proto.STRING, number=13)

    workload_metadata_config = proto.Field(
        proto.MESSAGE, number=14, message="WorkloadMetadataConfig",
    )

    taints = proto.RepeatedField(proto.MESSAGE, number=15, message="NodeTaint",)

    shielded_instance_config = proto.Field(
        proto.MESSAGE, number=20, message="ShieldedInstanceConfig",
    )


class ShieldedInstanceConfig(proto.Message):
    r"""A set of Shielded Instance options.

    Attributes:
        enable_secure_boot (bool):
            Defines whether the instance has Secure Boot
            enabled.
            Secure Boot helps ensure that the system only
            runs authentic software by verifying the digital
            signature of all boot components, and halting
            the boot process if signature verification
            fails.
        enable_integrity_monitoring (bool):
            Defines whether the instance has integrity
            monitoring enabled.
            Enables monitoring and attestation of the boot
            integrity of the instance. The attestation is
            performed against the integrity policy baseline.
            This baseline is initially derived from the
            implicitly trusted boot image when the instance
            is created.
    """

    enable_secure_boot = proto.Field(proto.BOOL, number=1)

    enable_integrity_monitoring = proto.Field(proto.BOOL, number=2)


class NodeTaint(proto.Message):
    r"""Kubernetes taint is comprised of three fields: key, value,
    and effect. Effect can only be one of three types:  NoSchedule,
    PreferNoSchedule or NoExecute.
    For more information, including usage and the valid values, see:
    https://kubernetes.io/docs/concepts/configuration/taint-and-
    toleration/

    Attributes:
        key (str):
            Key for taint.
        value (str):
            Value for taint.
        effect (~.cluster_service.NodeTaint.Effect):
            Effect for taint.
    """

    class Effect(proto.Enum):
        r"""Possible values for Effect in taint."""
        EFFECT_UNSPECIFIED = 0
        NO_SCHEDULE = 1
        PREFER_NO_SCHEDULE = 2
        NO_EXECUTE = 3

    key = proto.Field(proto.STRING, number=1)

    value = proto.Field(proto.STRING, number=2)

    effect = proto.Field(proto.ENUM, number=3, enum=Effect,)


class MasterAuth(proto.Message):
    r"""The authentication information for accessing the master
    endpoint. Authentication can be done using HTTP basic auth or
    using client certificates.

    Attributes:
        username (str):
            The username to use for HTTP basic
            authentication to the master endpoint. For
            clusters v1.6.0 and later, basic authentication
            can be disabled by leaving username unspecified
            (or setting it to the empty string).
        password (str):
            The password to use for HTTP basic
            authentication to the master endpoint. Because
            the master endpoint is open to the Internet, you
            should create a strong password.  If a password
            is provided for cluster creation, username must
            be non-empty.
        client_certificate_config (~.cluster_service.ClientCertificateConfig):
            Configuration for client certificate
            authentication on the cluster. For clusters
            before v1.12, if no configuration is specified,
            a client certificate is issued.
        cluster_ca_certificate (str):
            [Output only] Base64-encoded public certificate that is the
            root of trust for the cluster.
        client_certificate (str):
            [Output only] Base64-encoded public certificate used by
            clients to authenticate to the cluster endpoint.
        client_key (str):
            [Output only] Base64-encoded private key used by clients to
            authenticate to the cluster endpoint.
    """

    username = proto.Field(proto.STRING, number=1)

    password = proto.Field(proto.STRING, number=2)

    client_certificate_config = proto.Field(
        proto.MESSAGE, number=3, message="ClientCertificateConfig",
    )

    cluster_ca_certificate = proto.Field(proto.STRING, number=100)

    client_certificate = proto.Field(proto.STRING, number=101)

    client_key = proto.Field(proto.STRING, number=102)


class ClientCertificateConfig(proto.Message):
    r"""Configuration for client certificates on the cluster.

    Attributes:
        issue_client_certificate (bool):
            Issue a client certificate.
    """

    issue_client_certificate = proto.Field(proto.BOOL, number=1)


class AddonsConfig(proto.Message):
    r"""Configuration for the addons that can be automatically spun
    up in the cluster, enabling additional functionality.

    Attributes:
        http_load_balancing (~.cluster_service.HttpLoadBalancing):
            Configuration for the HTTP (L7) load
            balancing controller addon, which makes it easy
            to set up HTTP load balancers for services in a
            cluster.
        horizontal_pod_autoscaling (~.cluster_service.HorizontalPodAutoscaling):
            Configuration for the horizontal pod
            autoscaling feature, which increases or
            decreases the number of replica pods a
            replication controller has based on the resource
            usage of the existing pods.
        kubernetes_dashboard (~.cluster_service.KubernetesDashboard):
            Configuration for the Kubernetes Dashboard.
            This addon is deprecated, and will be disabled
            in 1.15. It is recommended to use the Cloud
            Console to manage and monitor your Kubernetes
            clusters, workloads and applications. For more
            information, see:
            https://cloud.google.com/kubernetes-
            engine/docs/concepts/dashboards
        network_policy_config (~.cluster_service.NetworkPolicyConfig):
            Configuration for NetworkPolicy. This only
            tracks whether the addon is enabled or not on
            the Master, it does not track whether network
            policy is enabled for the nodes.
        istio_config (~.cluster_service.IstioConfig):
            Configuration for Istio, an open platform to
            connect, manage, and secure microservices.
        cloud_run_config (~.cluster_service.CloudRunConfig):
            Configuration for the Cloud Run addon. The ``IstioConfig``
            addon must be enabled in order to enable Cloud Run addon.
            This option can only be enabled at cluster creation time.
    """

    http_load_balancing = proto.Field(
        proto.MESSAGE, number=1, message="HttpLoadBalancing",
    )

    horizontal_pod_autoscaling = proto.Field(
        proto.MESSAGE, number=2, message="HorizontalPodAutoscaling",
    )

    kubernetes_dashboard = proto.Field(
        proto.MESSAGE, number=3, message="KubernetesDashboard",
    )

    network_policy_config = proto.Field(
        proto.MESSAGE, number=4, message="NetworkPolicyConfig",
    )

    istio_config = proto.Field(proto.MESSAGE, number=5, message="IstioConfig",)

    cloud_run_config = proto.Field(proto.MESSAGE, number=7, message="CloudRunConfig",)


class HttpLoadBalancing(proto.Message):
    r"""Configuration options for the HTTP (L7) load balancing
    controller addon, which makes it easy to set up HTTP load
    balancers for services in a cluster.

    Attributes:
        disabled (bool):
            Whether the HTTP Load Balancing controller is
            enabled in the cluster. When enabled, it runs a
            small pod in the cluster that manages the load
            balancers.
    """

    disabled = proto.Field(proto.BOOL, number=1)


class HorizontalPodAutoscaling(proto.Message):
    r"""Configuration options for the horizontal pod autoscaling
    feature, which increases or decreases the number of replica pods
    a replication controller has based on the resource usage of the
    existing pods.

    Attributes:
        disabled (bool):
            Whether the Horizontal Pod Autoscaling
            feature is enabled in the cluster. When enabled,
            it ensures that a Heapster pod is running in the
            cluster, which is also used by the Cloud
            Monitoring service.
    """

    disabled = proto.Field(proto.BOOL, number=1)


class KubernetesDashboard(proto.Message):
    r"""Configuration for the Kubernetes Dashboard.

    Attributes:
        disabled (bool):
            Whether the Kubernetes Dashboard is enabled
            for this cluster.
    """

    disabled = proto.Field(proto.BOOL, number=1)


class NetworkPolicyConfig(proto.Message):
    r"""Configuration for NetworkPolicy. This only tracks whether the
    addon is enabled or not on the Master, it does not track whether
    network policy is enabled for the nodes.

    Attributes:
        disabled (bool):
            Whether NetworkPolicy is enabled for this
            cluster.
    """

    disabled = proto.Field(proto.BOOL, number=1)


class PrivateClusterConfig(proto.Message):
    r"""Configuration options for private clusters.

    Attributes:
        enable_private_nodes (bool):
            Whether nodes have internal IP addresses
            only. If enabled, all nodes are given only RFC
            1918 private addresses and communicate with the
            master via private networking.
        enable_private_endpoint (bool):
            Whether the master's internal IP address is
            used as the cluster endpoint.
        master_ipv4_cidr_block (str):
            The IP range in CIDR notation to use for the
            hosted master network. This range will be used
            for assigning internal IP addresses to the
            master or set of masters, as well as the ILB
            VIP. This range must not overlap with any other
            ranges in use within the cluster's network.
        private_endpoint (str):
            Output only. The internal IP address of this
            cluster's master endpoint.
        public_endpoint (str):
            Output only. The external IP address of this
            cluster's master endpoint.
    """

    enable_private_nodes = proto.Field(proto.BOOL, number=1)

    enable_private_endpoint = proto.Field(proto.BOOL, number=2)

    master_ipv4_cidr_block = proto.Field(proto.STRING, number=3)

    private_endpoint = proto.Field(proto.STRING, number=4)

    public_endpoint = proto.Field(proto.STRING, number=5)


class IstioConfig(proto.Message):
    r"""Configuration options for Istio addon.

    Attributes:
        disabled (bool):
            Whether Istio is enabled for this cluster.
        auth (~.cluster_service.IstioConfig.IstioAuthMode):
            The specified Istio auth mode, either none,
            or mutual TLS.
    """

    class IstioAuthMode(proto.Enum):
        r"""Istio auth mode,
        https://istio.io/docs/concepts/security/mutual-tls.html
        """
        AUTH_NONE = 0
        AUTH_MUTUAL_TLS = 1

    disabled = proto.Field(proto.BOOL, number=1)

    auth = proto.Field(proto.ENUM, number=2, enum=IstioAuthMode,)


class CloudRunConfig(proto.Message):
    r"""Configuration options for the Cloud Run feature.

    Attributes:
        disabled (bool):
            Whether Cloud Run addon is enabled for this
            cluster.
    """

    disabled = proto.Field(proto.BOOL, number=1)


class MasterAuthorizedNetworksConfig(proto.Message):
    r"""Configuration options for the master authorized networks
    feature. Enabled master authorized networks will disallow all
    external traffic to access Kubernetes master through HTTPS
    except traffic from the given CIDR blocks, Google Compute Engine
    Public IPs and Google Prod IPs.

    Attributes:
        enabled (bool):
            Whether or not master authorized networks is
            enabled.
        cidr_blocks (Sequence[~.cluster_service.MasterAuthorizedNetworksConfig.CidrBlock]):
            cidr_blocks define up to 10 external networks that could
            access Kubernetes master through HTTPS.
    """

    class CidrBlock(proto.Message):
        r"""CidrBlock contains an optional name and one CIDR block.

        Attributes:
            display_name (str):
                display_name is an optional field for users to identify CIDR
                blocks.
            cidr_block (str):
                cidr_block must be specified in CIDR notation.
        """

        display_name = proto.Field(proto.STRING, number=1)

        cidr_block = proto.Field(proto.STRING, number=2)

    enabled = proto.Field(proto.BOOL, number=1)

    cidr_blocks = proto.RepeatedField(proto.MESSAGE, number=2, message=CidrBlock,)


class LegacyAbac(proto.Message):
    r"""Configuration for the legacy Attribute Based Access Control
    authorization mode.

    Attributes:
        enabled (bool):
            Whether the ABAC authorizer is enabled for
            this cluster. When enabled, identities in the
            system, including service accounts, nodes, and
            controllers, will have statically granted
            permissions beyond those provided by the RBAC
            configuration or IAM.
    """

    enabled = proto.Field(proto.BOOL, number=1)


class NetworkPolicy(proto.Message):
    r"""Configuration options for the NetworkPolicy feature.
    https://kubernetes.io/docs/concepts/services-
    networking/networkpolicies/

    Attributes:
        provider (~.cluster_service.NetworkPolicy.Provider):
            The selected network policy provider.
        enabled (bool):
            Whether network policy is enabled on the
            cluster.
    """

    class Provider(proto.Enum):
        r"""Allowed Network Policy providers."""
        PROVIDER_UNSPECIFIED = 0
        CALICO = 1

    provider = proto.Field(proto.ENUM, number=1, enum=Provider,)

    enabled = proto.Field(proto.BOOL, number=2)


class IPAllocationPolicy(proto.Message):
    r"""Configuration for controlling how IPs are allocated in the
    cluster.

    Attributes:
        use_ip_aliases (bool):
            Whether alias IPs will be used for pod IPs in
            the cluster.
        create_subnetwork (bool):
            Whether a new subnetwork will be created automatically for
            the cluster.

            This field is only applicable when ``use_ip_aliases`` is
            true.
        subnetwork_name (str):
            A custom subnetwork name to be used if ``create_subnetwork``
            is true. If this field is empty, then an automatic name will
            be chosen for the new subnetwork.
        cluster_ipv4_cidr (str):
            This field is deprecated, use cluster_ipv4_cidr_block.
        node_ipv4_cidr (str):
            This field is deprecated, use node_ipv4_cidr_block.
        services_ipv4_cidr (str):
            This field is deprecated, use services_ipv4_cidr_block.
        cluster_secondary_range_name (str):
            The name of the secondary range to be used for the cluster
            CIDR block. The secondary range will be used for pod IP
            addresses. This must be an existing secondary range
            associated with the cluster subnetwork.

            This field is only applicable with use_ip_aliases and
            create_subnetwork is false.
        services_secondary_range_name (str):
            The name of the secondary range to be used as for the
            services CIDR block. The secondary range will be used for
            service ClusterIPs. This must be an existing secondary range
            associated with the cluster subnetwork.

            This field is only applicable with use_ip_aliases and
            create_subnetwork is false.
        cluster_ipv4_cidr_block (str):
            The IP address range for the cluster pod IPs. If this field
            is set, then ``cluster.cluster_ipv4_cidr`` must be left
            blank.

            This field is only applicable when ``use_ip_aliases`` is
            true.

            Set to blank to have a range chosen with the default size.

            Set to /netmask (e.g. ``/14``) to have a range chosen with a
            specific netmask.

            Set to a
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``10.96.0.0/14``) from the RFC-1918 private
            networks (e.g. ``10.0.0.0/8``, ``172.16.0.0/12``,
            ``192.168.0.0/16``) to pick a specific range to use.
        node_ipv4_cidr_block (str):
            The IP address range of the instance IPs in this cluster.

            This is applicable only if ``create_subnetwork`` is true.

            Set to blank to have a range chosen with the default size.

            Set to /netmask (e.g. ``/14``) to have a range chosen with a
            specific netmask.

            Set to a
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``10.96.0.0/14``) from the RFC-1918 private
            networks (e.g. ``10.0.0.0/8``, ``172.16.0.0/12``,
            ``192.168.0.0/16``) to pick a specific range to use.
        services_ipv4_cidr_block (str):
            The IP address range of the services IPs in this cluster. If
            blank, a range will be automatically chosen with the default
            size.

            This field is only applicable when ``use_ip_aliases`` is
            true.

            Set to blank to have a range chosen with the default size.

            Set to /netmask (e.g. ``/14``) to have a range chosen with a
            specific netmask.

            Set to a
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``10.96.0.0/14``) from the RFC-1918 private
            networks (e.g. ``10.0.0.0/8``, ``172.16.0.0/12``,
            ``192.168.0.0/16``) to pick a specific range to use.
        allow_route_overlap (bool):
            If true, allow allocation of cluster CIDR ranges that
            overlap with certain kinds of network routes. By default we
            do not allow cluster CIDR ranges to intersect with any user
            declared routes. With allow_route_overlap == true, we allow
            overlapping with CIDR ranges that are larger than the
            cluster CIDR range.

            If this field is set to true, then cluster and services
            CIDRs must be fully-specified (e.g. ``10.96.0.0/14``, but
            not ``/14``), which means:

            1) When ``use_ip_aliases`` is true,
               ``cluster_ipv4_cidr_block`` and
               ``services_ipv4_cidr_block`` must be fully-specified.
            2) When ``use_ip_aliases`` is false,
               ``cluster.cluster_ipv4_cidr`` muse be fully-specified.
        tpu_ipv4_cidr_block (str):
            The IP address range of the Cloud TPUs in this cluster. If
            unspecified, a range will be automatically chosen with the
            default size.

            This field is only applicable when ``use_ip_aliases`` is
            true.

            If unspecified, the range will use the default size.

            Set to /netmask (e.g. ``/14``) to have a range chosen with a
            specific netmask.

            Set to a
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``10.96.0.0/14``) from the RFC-1918 private
            networks (e.g. ``10.0.0.0/8``, ``172.16.0.0/12``,
            ``192.168.0.0/16``) to pick a specific range to use.
    """

    use_ip_aliases = proto.Field(proto.BOOL, number=1)

    create_subnetwork = proto.Field(proto.BOOL, number=2)

    subnetwork_name = proto.Field(proto.STRING, number=3)

    cluster_ipv4_cidr = proto.Field(proto.STRING, number=4)

    node_ipv4_cidr = proto.Field(proto.STRING, number=5)

    services_ipv4_cidr = proto.Field(proto.STRING, number=6)

    cluster_secondary_range_name = proto.Field(proto.STRING, number=7)

    services_secondary_range_name = proto.Field(proto.STRING, number=8)

    cluster_ipv4_cidr_block = proto.Field(proto.STRING, number=9)

    node_ipv4_cidr_block = proto.Field(proto.STRING, number=10)

    services_ipv4_cidr_block = proto.Field(proto.STRING, number=11)

    allow_route_overlap = proto.Field(proto.BOOL, number=12)

    tpu_ipv4_cidr_block = proto.Field(proto.STRING, number=13)


class BinaryAuthorization(proto.Message):
    r"""Configuration for Binary Authorization.

    Attributes:
        enabled (bool):
            Enable Binary Authorization for this cluster.
            If enabled, all container images will be
            validated by Google Binauthz.
    """

    enabled = proto.Field(proto.BOOL, number=1)


class PodSecurityPolicyConfig(proto.Message):
    r"""Configuration for the PodSecurityPolicy feature.

    Attributes:
        enabled (bool):
            Enable the PodSecurityPolicy controller for
            this cluster. If enabled, pods must be valid
            under a PodSecurityPolicy to be created.
    """

    enabled = proto.Field(proto.BOOL, number=1)


class AuthenticatorGroupsConfig(proto.Message):
    r"""Configuration for returning group information from
    authenticators.

    Attributes:
        enabled (bool):
            Whether this cluster should return group
            membership lookups during authentication using a
            group of security groups.
        security_group (str):
            The name of the security group-of-groups to
            be used. Only relevant if enabled = true.
    """

    enabled = proto.Field(proto.BOOL, number=1)

    security_group = proto.Field(proto.STRING, number=2)


class Cluster(proto.Message):
    r"""A Google Kubernetes Engine cluster.

    Attributes:
        name (str):
            The name of this cluster. The name must be unique within
            this project and location (e.g. zone or region), and can be
            up to 40 characters with the following restrictions:

            -  Lowercase letters, numbers, and hyphens only.
            -  Must start with a letter.
            -  Must end with a number or a letter.
        description (str):
            An optional description of this cluster.
        initial_node_count (int):
            The number of nodes to create in this cluster. You must
            ensure that your Compute Engine `resource
            quota <https://cloud.google.com/compute/quotas>`__ is
            sufficient for this number of instances. You must also have
            available firewall and routes quota. For requests, this
            field should only be used in lieu of a "node_pool" object,
            since this configuration (along with the "node_config") will
            be used to create a "NodePool" object with an auto-generated
            name. Do not use this and a node_pool at the same time.

            This field is deprecated, use node_pool.initial_node_count
            instead.
        node_config (~.cluster_service.NodeConfig):
            Parameters used in creating the cluster's nodes. For
            requests, this field should only be used in lieu of a
            "node_pool" object, since this configuration (along with the
            "initial_node_count") will be used to create a "NodePool"
            object with an auto-generated name. Do not use this and a
            node_pool at the same time. For responses, this field will
            be populated with the node configuration of the first node
            pool. (For configuration of each node pool, see
            ``node_pool.config``)

            If unspecified, the defaults are used. This field is
            deprecated, use node_pool.config instead.
        master_auth (~.cluster_service.MasterAuth):
            The authentication information for accessing the master
            endpoint. If unspecified, the defaults are used: For
            clusters before v1.12, if master_auth is unspecified,
            ``username`` will be set to "admin", a random password will
            be generated, and a client certificate will be issued.
        logging_service (str):
            The logging service the cluster should use to write logs.
            Currently available options:

            -  ``logging.googleapis.com`` - the Google Cloud Logging
               service.
            -  ``none`` - no logs will be exported from the cluster.
            -  if left as an empty string,\ ``logging.googleapis.com``
               will be used.
        monitoring_service (str):
            The monitoring service the cluster should use to write
            metrics. Currently available options:

            -  ``monitoring.googleapis.com`` - the Google Cloud
               Monitoring service.
            -  ``none`` - no metrics will be exported from the cluster.
            -  if left as an empty string, ``monitoring.googleapis.com``
               will be used.
        network (str):
            The name of the Google Compute Engine
            `network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`__
            to which the cluster is connected. If left unspecified, the
            ``default`` network will be used. On output this shows the
            network ID instead of the name.
        cluster_ipv4_cidr (str):
            The IP address range of the container pods in this cluster,
            in
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``10.96.0.0/14``). Leave blank to have one
            automatically chosen or specify a ``/14`` block in
            ``10.0.0.0/8``.
        addons_config (~.cluster_service.AddonsConfig):
            Configurations for the various addons
            available to run in the cluster.
        subnetwork (str):
            The name of the Google Compute Engine
            `subnetwork <https://cloud.google.com/compute/docs/subnetworks>`__
            to which the cluster is connected. On output this shows the
            subnetwork ID instead of the name.
        node_pools (Sequence[~.cluster_service.NodePool]):
            The node pools associated with this cluster. This field
            should not be set if "node_config" or "initial_node_count"
            are specified.
        locations (Sequence[str]):
            The list of Google Compute Engine
            `zones <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster's nodes should be located.
        enable_kubernetes_alpha (bool):
            Kubernetes alpha features are enabled on this
            cluster. This includes alpha API groups (e.g.
            v1beta1) and features that may not be production
            ready in the kubernetes version of the master
            and nodes. The cluster has no SLA for uptime and
            master/node upgrades are disabled. Alpha enabled
            clusters are automatically deleted thirty days
            after creation.
        resource_labels (Sequence[~.cluster_service.Cluster.ResourceLabelsEntry]):
            The resource labels for the cluster to use to
            annotate any related Google Compute Engine
            resources.
        label_fingerprint (str):
            The fingerprint of the set of labels for this
            cluster.
        legacy_abac (~.cluster_service.LegacyAbac):
            Configuration for the legacy ABAC
            authorization mode.
        network_policy (~.cluster_service.NetworkPolicy):
            Configuration options for the NetworkPolicy
            feature.
        ip_allocation_policy (~.cluster_service.IPAllocationPolicy):
            Configuration for cluster IP allocation.
        master_authorized_networks_config (~.cluster_service.MasterAuthorizedNetworksConfig):
            The configuration options for master
            authorized networks feature.
        maintenance_policy (~.cluster_service.MaintenancePolicy):
            Configure the maintenance policy for this
            cluster.
        binary_authorization (~.cluster_service.BinaryAuthorization):
            Configuration for Binary Authorization.
        pod_security_policy_config (~.cluster_service.PodSecurityPolicyConfig):
            Configuration for the PodSecurityPolicy
            feature.
        autoscaling (~.cluster_service.ClusterAutoscaling):
            Cluster-level autoscaling configuration.
        network_config (~.cluster_service.NetworkConfig):
            Configuration for cluster networking.
        private_cluster (bool):
            If this is a private cluster setup. Private clusters are
            clusters that, by default have no external IP addresses on
            the nodes and where nodes and the master communicate over
            private IP addresses. This field is deprecated, use
            private_cluster_config.enable_private_nodes instead.
        master_ipv4_cidr_block (str):
            The IP prefix in CIDR notation to use for the hosted master
            network. This prefix will be used for assigning private IP
            addresses to the master or set of masters, as well as the
            ILB VIP. This field is deprecated, use
            private_cluster_config.master_ipv4_cidr_block instead.
        default_max_pods_constraint (~.cluster_service.MaxPodsConstraint):
            The default constraint on the maximum number
            of pods that can be run simultaneously on a node
            in the node pool of this cluster. Only honored
            if cluster created with IP Alias support.
        resource_usage_export_config (~.cluster_service.ResourceUsageExportConfig):
            Configuration for exporting resource usages.
            Resource usage export is disabled when this
            config unspecified.
        authenticator_groups_config (~.cluster_service.AuthenticatorGroupsConfig):
            Configuration controlling RBAC group
            membership information.
        private_cluster_config (~.cluster_service.PrivateClusterConfig):
            Configuration for private cluster.
        vertical_pod_autoscaling (~.cluster_service.VerticalPodAutoscaling):
            Cluster-level Vertical Pod Autoscaling
            configuration.
        self_link (str):
            [Output only] Server-defined URL for the resource.
        zone (str):
            [Output only] The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field is deprecated, use
            location instead.
        endpoint (str):
            [Output only] The IP address of this cluster's master
            endpoint. The endpoint can be accessed from the internet at
            ``https://username:password@endpoint/``.

            See the ``masterAuth`` property of this resource for
            username and password information.
        initial_cluster_version (str):
            The initial Kubernetes version for this
            cluster.  Valid versions are those found in
            validMasterVersions returned by getServerConfig.
            The version can be upgraded over time; such
            upgrades are reflected in currentMasterVersion
            and currentNodeVersion.

            Users may specify either explicit versions
            offered by Kubernetes Engine or version aliases,
            which have the following behavior:
            - "latest": picks the highest valid Kubernetes
            version - "1.X": picks the highest valid
            patch+gke.N patch in the 1.X version - "1.X.Y":
            picks the highest valid gke.N patch in the 1.X.Y
            version - "1.X.Y-gke.N": picks an explicit
            Kubernetes version - "","-": picks the default
            Kubernetes version
        current_master_version (str):
            [Output only] The current software version of the master
            endpoint.
        current_node_version (str):
            [Output only] Deprecated, use
            `NodePool.version <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1beta1/projects.locations.clusters.nodePools>`__
            instead. The current version of the node software
            components. If they are currently at multiple versions
            because they're in the process of being upgraded, this
            reflects the minimum version of all nodes.
        create_time (str):
            [Output only] The time the cluster was created, in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        status (~.cluster_service.Cluster.Status):
            [Output only] The current status of this cluster.
        status_message (str):
            [Output only] Additional information about the current
            status of this cluster, if available.
        node_ipv4_cidr_size (int):
            [Output only] The size of the address space on each node for
            hosting containers. This is provisioned from within the
            ``container_ipv4_cidr`` range. This field will only be set
            when cluster is in route-based network mode.
        services_ipv4_cidr (str):
            [Output only] The IP address range of the Kubernetes
            services in this cluster, in
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``1.2.3.4/29``). Service addresses are
            typically put in the last ``/16`` from the container CIDR.
        instance_group_urls (Sequence[str]):
            Deprecated. Use node_pools.instance_group_urls.
        current_node_count (int):
            [Output only] The number of nodes currently in the cluster.
            Deprecated. Call Kubernetes API directly to retrieve node
            information.
        expire_time (str):
            [Output only] The time the cluster will be automatically
            deleted in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        location (str):
            [Output only] The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`__
            or
            `region <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`__
            in which the cluster resides.
        enable_tpu (bool):
            Enable the ability to use Cloud TPUs in this
            cluster.
        tpu_ipv4_cidr_block (str):
            [Output only] The IP address range of the Cloud TPUs in this
            cluster, in
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``1.2.3.4/29``).
        database_encryption (~.cluster_service.DatabaseEncryption):
            Configuration of etcd encryption.
        conditions (Sequence[~.cluster_service.StatusCondition]):
            Which conditions caused the current cluster
            state.
    """

    class Status(proto.Enum):
        r"""The current status of the cluster."""
        STATUS_UNSPECIFIED = 0
        PROVISIONING = 1
        RUNNING = 2
        RECONCILING = 3
        STOPPING = 4
        ERROR = 5
        DEGRADED = 6

    name = proto.Field(proto.STRING, number=1)

    description = proto.Field(proto.STRING, number=2)

    initial_node_count = proto.Field(proto.INT32, number=3)

    node_config = proto.Field(proto.MESSAGE, number=4, message="NodeConfig",)

    master_auth = proto.Field(proto.MESSAGE, number=5, message="MasterAuth",)

    logging_service = proto.Field(proto.STRING, number=6)

    monitoring_service = proto.Field(proto.STRING, number=7)

    network = proto.Field(proto.STRING, number=8)

    cluster_ipv4_cidr = proto.Field(proto.STRING, number=9)

    addons_config = proto.Field(proto.MESSAGE, number=10, message="AddonsConfig",)

    subnetwork = proto.Field(proto.STRING, number=11)

    node_pools = proto.RepeatedField(proto.MESSAGE, number=12, message="NodePool",)

    locations = proto.RepeatedField(proto.STRING, number=13)

    enable_kubernetes_alpha = proto.Field(proto.BOOL, number=14)

    resource_labels = proto.MapField(proto.STRING, proto.STRING, number=15)

    label_fingerprint = proto.Field(proto.STRING, number=16)

    legacy_abac = proto.Field(proto.MESSAGE, number=18, message="LegacyAbac",)

    network_policy = proto.Field(proto.MESSAGE, number=19, message="NetworkPolicy",)

    ip_allocation_policy = proto.Field(
        proto.MESSAGE, number=20, message="IPAllocationPolicy",
    )

    master_authorized_networks_config = proto.Field(
        proto.MESSAGE, number=22, message="MasterAuthorizedNetworksConfig",
    )

    maintenance_policy = proto.Field(
        proto.MESSAGE, number=23, message="MaintenancePolicy",
    )

    binary_authorization = proto.Field(
        proto.MESSAGE, number=24, message="BinaryAuthorization",
    )

    pod_security_policy_config = proto.Field(
        proto.MESSAGE, number=25, message="PodSecurityPolicyConfig",
    )

    autoscaling = proto.Field(proto.MESSAGE, number=26, message="ClusterAutoscaling",)

    network_config = proto.Field(proto.MESSAGE, number=27, message="NetworkConfig",)

    private_cluster = proto.Field(proto.BOOL, number=28)

    master_ipv4_cidr_block = proto.Field(proto.STRING, number=29)

    default_max_pods_constraint = proto.Field(
        proto.MESSAGE, number=30, message="MaxPodsConstraint",
    )

    resource_usage_export_config = proto.Field(
        proto.MESSAGE, number=33, message="ResourceUsageExportConfig",
    )

    authenticator_groups_config = proto.Field(
        proto.MESSAGE, number=34, message="AuthenticatorGroupsConfig",
    )

    private_cluster_config = proto.Field(
        proto.MESSAGE, number=37, message="PrivateClusterConfig",
    )

    vertical_pod_autoscaling = proto.Field(
        proto.MESSAGE, number=39, message="VerticalPodAutoscaling",
    )

    self_link = proto.Field(proto.STRING, number=100)

    zone = proto.Field(proto.STRING, number=101)

    endpoint = proto.Field(proto.STRING, number=102)

    initial_cluster_version = proto.Field(proto.STRING, number=103)

    current_master_version = proto.Field(proto.STRING, number=104)

    current_node_version = proto.Field(proto.STRING, number=105)

    create_time = proto.Field(proto.STRING, number=106)

    status = proto.Field(proto.ENUM, number=107, enum=Status,)

    status_message = proto.Field(proto.STRING, number=108)

    node_ipv4_cidr_size = proto.Field(proto.INT32, number=109)

    services_ipv4_cidr = proto.Field(proto.STRING, number=110)

    instance_group_urls = proto.RepeatedField(proto.STRING, number=111)

    current_node_count = proto.Field(proto.INT32, number=112)

    expire_time = proto.Field(proto.STRING, number=113)

    location = proto.Field(proto.STRING, number=114)

    enable_tpu = proto.Field(proto.BOOL, number=115)

    tpu_ipv4_cidr_block = proto.Field(proto.STRING, number=116)

    database_encryption = proto.Field(
        proto.MESSAGE, number=38, message="DatabaseEncryption",
    )

    conditions = proto.RepeatedField(
        proto.MESSAGE, number=118, message="StatusCondition",
    )


class ClusterUpdate(proto.Message):
    r"""ClusterUpdate describes an update to the cluster. Exactly one
    update can be applied to a cluster with each request, so at most
    one field can be provided.

    Attributes:
        desired_node_version (str):
            The Kubernetes version to change the nodes to
            (typically an upgrade).

            Users may specify either explicit versions
            offered by Kubernetes Engine or version aliases,
            which have the following behavior:
            - "latest": picks the highest valid Kubernetes
            version - "1.X": picks the highest valid
            patch+gke.N patch in the 1.X version - "1.X.Y":
            picks the highest valid gke.N patch in the 1.X.Y
            version - "1.X.Y-gke.N": picks an explicit
            Kubernetes version - "-": picks the Kubernetes
            master version
        desired_monitoring_service (str):
            The monitoring service the cluster should use to write
            metrics. Currently available options:

            -  "monitoring.googleapis.com/kubernetes" - the Google Cloud
               Monitoring service with Kubernetes-native resource model
            -  "monitoring.googleapis.com" - the Google Cloud Monitoring
               service
            -  "none" - no metrics will be exported from the cluster
        desired_addons_config (~.cluster_service.AddonsConfig):
            Configurations for the various addons
            available to run in the cluster.
        desired_node_pool_id (str):
            The node pool to be upgraded. This field is mandatory if
            "desired_node_version", "desired_image_family",
            "desired_node_pool_autoscaling", or
            "desired_workload_metadata_config" is specified and there is
            more than one node pool on the cluster.
        desired_image_type (str):
            The desired image type for the node pool. NOTE: Set the
            "desired_node_pool" field as well.
        desired_node_pool_autoscaling (~.cluster_service.NodePoolAutoscaling):
            Autoscaler configuration for the node pool specified in
            desired_node_pool_id. If there is only one pool in the
            cluster and desired_node_pool_id is not provided then the
            change applies to that single node pool.
        desired_locations (Sequence[str]):
            The desired list of Google Compute Engine
            `zones <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster's nodes should be located. Changing the
            locations a cluster is in will result in nodes being either
            created or removed from the cluster, depending on whether
            locations are being added or removed.

            This list must always include the cluster's primary zone.
        desired_master_authorized_networks_config (~.cluster_service.MasterAuthorizedNetworksConfig):
            The desired configuration options for master
            authorized networks feature.
        desired_pod_security_policy_config (~.cluster_service.PodSecurityPolicyConfig):
            The desired configuration options for the
            PodSecurityPolicy feature.
        desired_cluster_autoscaling (~.cluster_service.ClusterAutoscaling):
            Cluster-level autoscaling configuration.
        desired_binary_authorization (~.cluster_service.BinaryAuthorization):
            The desired configuration options for the
            Binary Authorization feature.
        desired_logging_service (str):
            The logging service the cluster should use to write metrics.
            Currently available options:

            -  "logging.googleapis.com/kubernetes" - the Google Cloud
               Logging service with Kubernetes-native resource model
            -  "logging.googleapis.com" - the Google Cloud Logging
               service
            -  "none" - no logs will be exported from the cluster
        desired_resource_usage_export_config (~.cluster_service.ResourceUsageExportConfig):
            The desired configuration for exporting
            resource usage.
        desired_vertical_pod_autoscaling (~.cluster_service.VerticalPodAutoscaling):
            Cluster-level Vertical Pod Autoscaling
            configuration.
        desired_intra_node_visibility_config (~.cluster_service.IntraNodeVisibilityConfig):
            The desired config of Intra-node visibility.
        desired_master_version (str):
            The Kubernetes version to change the master
            to. The only valid value is the latest supported
            version.
            Users may specify either explicit versions
            offered by Kubernetes Engine or version aliases,
            which have the following behavior:
            - "latest": picks the highest valid Kubernetes
            version - "1.X": picks the highest valid
            patch+gke.N patch in the 1.X version - "1.X.Y":
            picks the highest valid gke.N patch in the 1.X.Y
            version - "1.X.Y-gke.N": picks an explicit
            Kubernetes version - "-": picks the default
            Kubernetes version
    """

    desired_node_version = proto.Field(proto.STRING, number=4)

    desired_monitoring_service = proto.Field(proto.STRING, number=5)

    desired_addons_config = proto.Field(
        proto.MESSAGE, number=6, message="AddonsConfig",
    )

    desired_node_pool_id = proto.Field(proto.STRING, number=7)

    desired_image_type = proto.Field(proto.STRING, number=8)

    desired_node_pool_autoscaling = proto.Field(
        proto.MESSAGE, number=9, message="NodePoolAutoscaling",
    )

    desired_locations = proto.RepeatedField(proto.STRING, number=10)

    desired_master_authorized_networks_config = proto.Field(
        proto.MESSAGE, number=12, message="MasterAuthorizedNetworksConfig",
    )

    desired_pod_security_policy_config = proto.Field(
        proto.MESSAGE, number=14, message="PodSecurityPolicyConfig",
    )

    desired_cluster_autoscaling = proto.Field(
        proto.MESSAGE, number=15, message="ClusterAutoscaling",
    )

    desired_binary_authorization = proto.Field(
        proto.MESSAGE, number=16, message="BinaryAuthorization",
    )

    desired_logging_service = proto.Field(proto.STRING, number=19)

    desired_resource_usage_export_config = proto.Field(
        proto.MESSAGE, number=21, message="ResourceUsageExportConfig",
    )

    desired_vertical_pod_autoscaling = proto.Field(
        proto.MESSAGE, number=22, message="VerticalPodAutoscaling",
    )

    desired_intra_node_visibility_config = proto.Field(
        proto.MESSAGE, number=26, message="IntraNodeVisibilityConfig",
    )

    desired_master_version = proto.Field(proto.STRING, number=100)


class Operation(proto.Message):
    r"""This operation resource represents operations that may have
    happened or are happening on the cluster. All fields are output
    only.

    Attributes:
        name (str):
            The server-assigned ID for the operation.
        zone (str):
            The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the operation is taking place. This field is
            deprecated, use location instead.
        operation_type (~.cluster_service.Operation.Type):
            The operation type.
        status (~.cluster_service.Operation.Status):
            The current status of the operation.
        detail (str):
            Detailed operation progress, if available.
        status_message (str):
            If an error has occurred, a textual
            description of the error.
        self_link (str):
            Server-defined URL for the resource.
        target_link (str):
            Server-defined URL for the target of the
            operation.
        location (str):
            [Output only] The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`__
            or
            `region <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`__
            in which the cluster resides.
        start_time (str):
            [Output only] The time the operation started, in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        end_time (str):
            [Output only] The time the operation completed, in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        progress (~.cluster_service.OperationProgress):
            [Output only] Progress information for an operation.
        cluster_conditions (Sequence[~.cluster_service.StatusCondition]):
            Which conditions caused the current cluster
            state.
        nodepool_conditions (Sequence[~.cluster_service.StatusCondition]):
            Which conditions caused the current node pool
            state.
    """

    class Status(proto.Enum):
        r"""Current status of the operation."""
        STATUS_UNSPECIFIED = 0
        PENDING = 1
        RUNNING = 2
        DONE = 3
        ABORTING = 4

    class Type(proto.Enum):
        r"""Operation type."""
        TYPE_UNSPECIFIED = 0
        CREATE_CLUSTER = 1
        DELETE_CLUSTER = 2
        UPGRADE_MASTER = 3
        UPGRADE_NODES = 4
        REPAIR_CLUSTER = 5
        UPDATE_CLUSTER = 6
        CREATE_NODE_POOL = 7
        DELETE_NODE_POOL = 8
        SET_NODE_POOL_MANAGEMENT = 9
        AUTO_REPAIR_NODES = 10
        AUTO_UPGRADE_NODES = 11
        SET_LABELS = 12
        SET_MASTER_AUTH = 13
        SET_NODE_POOL_SIZE = 14
        SET_NETWORK_POLICY = 15
        SET_MAINTENANCE_POLICY = 16

    name = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    operation_type = proto.Field(proto.ENUM, number=3, enum=Type,)

    status = proto.Field(proto.ENUM, number=4, enum=Status,)

    detail = proto.Field(proto.STRING, number=8)

    status_message = proto.Field(proto.STRING, number=5)

    self_link = proto.Field(proto.STRING, number=6)

    target_link = proto.Field(proto.STRING, number=7)

    location = proto.Field(proto.STRING, number=9)

    start_time = proto.Field(proto.STRING, number=10)

    end_time = proto.Field(proto.STRING, number=11)

    progress = proto.Field(proto.MESSAGE, number=12, message="OperationProgress",)

    cluster_conditions = proto.RepeatedField(
        proto.MESSAGE, number=13, message="StatusCondition",
    )

    nodepool_conditions = proto.RepeatedField(
        proto.MESSAGE, number=14, message="StatusCondition",
    )


class OperationProgress(proto.Message):
    r"""Information about operation (or operation stage) progress.

    Attributes:
        name (str):
            A non-parameterized string describing an
            operation stage. Unset for single-stage
            operations.
        status (~.cluster_service.Operation.Status):
            Status of an operation stage.
            Unset for single-stage operations.
        metrics (Sequence[~.cluster_service.OperationProgress.Metric]):
            Progress metric bundle, for example: metrics: [{name: "nodes
            done", int_value: 15}, {name: "nodes total", int_value: 32}]
            or metrics: [{name: "progress", double_value: 0.56}, {name:
            "progress scale", double_value: 1.0}]
        stages (Sequence[~.cluster_service.OperationProgress]):
            Substages of an operation or a stage.
    """

    class Metric(proto.Message):
        r"""Progress metric is (string, int|float|string) pair.

        Attributes:
            name (str):
                Metric name, required.
                e.g., "nodes total", "percent done".
            int_value (int):
                For metrics with integer value.
            double_value (float):
                For metrics with floating point value.
            string_value (str):
                For metrics with custom values (ratios,
                visual progress, etc.).
        """

        name = proto.Field(proto.STRING, number=1)

        int_value = proto.Field(proto.INT64, number=2, oneof="value")

        double_value = proto.Field(proto.DOUBLE, number=3, oneof="value")

        string_value = proto.Field(proto.STRING, number=4, oneof="value")

    name = proto.Field(proto.STRING, number=1)

    status = proto.Field(proto.ENUM, number=2, enum="Operation.Status",)

    metrics = proto.RepeatedField(proto.MESSAGE, number=3, message=Metric,)

    stages = proto.RepeatedField(proto.MESSAGE, number=4, message="OperationProgress",)


class CreateClusterRequest(proto.Message):
    r"""CreateClusterRequest creates a cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the parent
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the parent field.
        cluster (~.cluster_service.Cluster):
            Required. A `cluster
            resource <https://cloud.google.com/container-engine/reference/rest/v1beta1/projects.zones.clusters>`__
        parent (str):
            The parent (project and location) where the cluster will be
            created. Specified in the format ``projects/*/locations/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster = proto.Field(proto.MESSAGE, number=3, message="Cluster",)

    parent = proto.Field(proto.STRING, number=5)


class GetClusterRequest(proto.Message):
    r"""GetClusterRequest gets the settings of a cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to retrieve. This field has been deprecated and
            replaced by the name field.
        name (str):
            The name (project, location, cluster) of the cluster to
            retrieve. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    name = proto.Field(proto.STRING, number=5)


class UpdateClusterRequest(proto.Message):
    r"""UpdateClusterRequest updates the settings of a cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to upgrade. This field has been deprecated and
            replaced by the name field.
        update (~.cluster_service.ClusterUpdate):
            Required. A description of the update.
        name (str):
            The name (project, location, cluster) of the cluster to
            update. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    update = proto.Field(proto.MESSAGE, number=4, message="ClusterUpdate",)

    name = proto.Field(proto.STRING, number=5)


class UpdateNodePoolRequest(proto.Message):
    r"""SetNodePoolVersionRequest updates the version of a node pool.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to upgrade. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Required. Deprecated. The name of the node
            pool to upgrade. This field has been deprecated
            and replaced by the name field.
        node_version (str):
            Required. The Kubernetes version to change
            the nodes to (typically an upgrade).

            Users may specify either explicit versions
            offered by Kubernetes Engine or version aliases,
            which have the following behavior:
            - "latest": picks the highest valid Kubernetes
            version - "1.X": picks the highest valid
            patch+gke.N patch in the 1.X version - "1.X.Y":
            picks the highest valid gke.N patch in the 1.X.Y
            version - "1.X.Y-gke.N": picks an explicit
            Kubernetes version - "-": picks the Kubernetes
            master version
        image_type (str):
            Required. The desired image type for the node
            pool.
        workload_metadata_config (~.cluster_service.WorkloadMetadataConfig):
            The desired image type for the node pool.
        name (str):
            The name (project, location, cluster, node pool) of the node
            pool to update. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    node_pool_id = proto.Field(proto.STRING, number=4)

    node_version = proto.Field(proto.STRING, number=5)

    image_type = proto.Field(proto.STRING, number=6)

    workload_metadata_config = proto.Field(
        proto.MESSAGE, number=14, message="WorkloadMetadataConfig",
    )

    name = proto.Field(proto.STRING, number=8)


class SetNodePoolAutoscalingRequest(proto.Message):
    r"""SetNodePoolAutoscalingRequest sets the autoscaler settings of
    a node pool.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to upgrade. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Required. Deprecated. The name of the node
            pool to upgrade. This field has been deprecated
            and replaced by the name field.
        autoscaling (~.cluster_service.NodePoolAutoscaling):
            Required. Autoscaling configuration for the
            node pool.
        name (str):
            The name (project, location, cluster, node pool) of the node
            pool to set autoscaler settings. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    node_pool_id = proto.Field(proto.STRING, number=4)

    autoscaling = proto.Field(proto.MESSAGE, number=5, message="NodePoolAutoscaling",)

    name = proto.Field(proto.STRING, number=6)


class SetLoggingServiceRequest(proto.Message):
    r"""SetLoggingServiceRequest sets the logging service of a
    cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to upgrade. This field has been deprecated and
            replaced by the name field.
        logging_service (str):
            Required. The logging service the cluster should use to
            write metrics. Currently available options:

            -  "logging.googleapis.com" - the Google Cloud Logging
               service
            -  "none" - no metrics will be exported from the cluster
        name (str):
            The name (project, location, cluster) of the cluster to set
            logging. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    logging_service = proto.Field(proto.STRING, number=4)

    name = proto.Field(proto.STRING, number=5)


class SetMonitoringServiceRequest(proto.Message):
    r"""SetMonitoringServiceRequest sets the monitoring service of a
    cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to upgrade. This field has been deprecated and
            replaced by the name field.
        monitoring_service (str):
            Required. The monitoring service the cluster should use to
            write metrics. Currently available options:

            -  "monitoring.googleapis.com" - the Google Cloud Monitoring
               service
            -  "none" - no metrics will be exported from the cluster
        name (str):
            The name (project, location, cluster) of the cluster to set
            monitoring. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    monitoring_service = proto.Field(proto.STRING, number=4)

    name = proto.Field(proto.STRING, number=6)


class SetAddonsConfigRequest(proto.Message):
    r"""SetAddonsRequest sets the addons associated with the cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to upgrade. This field has been deprecated and
            replaced by the name field.
        addons_config (~.cluster_service.AddonsConfig):
            Required. The desired configurations for the
            various addons available to run in the cluster.
        name (str):
            The name (project, location, cluster) of the cluster to set
            addons. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    addons_config = proto.Field(proto.MESSAGE, number=4, message="AddonsConfig",)

    name = proto.Field(proto.STRING, number=6)


class SetLocationsRequest(proto.Message):
    r"""SetLocationsRequest sets the locations of the cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to upgrade. This field has been deprecated and
            replaced by the name field.
        locations (Sequence[str]):
            Required. The desired list of Google Compute Engine
            `zones <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster's nodes should be located. Changing the
            locations a cluster is in will result in nodes being either
            created or removed from the cluster, depending on whether
            locations are being added or removed.

            This list must always include the cluster's primary zone.
        name (str):
            The name (project, location, cluster) of the cluster to set
            locations. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    locations = proto.RepeatedField(proto.STRING, number=4)

    name = proto.Field(proto.STRING, number=6)


class UpdateMasterRequest(proto.Message):
    r"""UpdateMasterRequest updates the master of the cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to upgrade. This field has been deprecated and
            replaced by the name field.
        master_version (str):
            Required. The Kubernetes version to change
            the master to.
            Users may specify either explicit versions
            offered by Kubernetes Engine or version aliases,
            which have the following behavior:
            - "latest": picks the highest valid Kubernetes
            version - "1.X": picks the highest valid
            patch+gke.N patch in the 1.X version - "1.X.Y":
            picks the highest valid gke.N patch in the 1.X.Y
            version - "1.X.Y-gke.N": picks an explicit
            Kubernetes version - "-": picks the default
            Kubernetes version
        name (str):
            The name (project, location, cluster) of the cluster to
            update. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    master_version = proto.Field(proto.STRING, number=4)

    name = proto.Field(proto.STRING, number=7)


class SetMasterAuthRequest(proto.Message):
    r"""SetMasterAuthRequest updates the admin password of a cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to upgrade. This field has been deprecated and
            replaced by the name field.
        action (~.cluster_service.SetMasterAuthRequest.Action):
            Required. The exact form of action to be
            taken on the master auth.
        update (~.cluster_service.MasterAuth):
            Required. A description of the update.
        name (str):
            The name (project, location, cluster) of the cluster to set
            auth. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    class Action(proto.Enum):
        r"""Operation type: what type update to perform."""
        UNKNOWN = 0
        SET_PASSWORD = 1
        GENERATE_PASSWORD = 2
        SET_USERNAME = 3

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    action = proto.Field(proto.ENUM, number=4, enum=Action,)

    update = proto.Field(proto.MESSAGE, number=5, message="MasterAuth",)

    name = proto.Field(proto.STRING, number=7)


class DeleteClusterRequest(proto.Message):
    r"""DeleteClusterRequest deletes a cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to delete. This field has been deprecated and
            replaced by the name field.
        name (str):
            The name (project, location, cluster) of the cluster to
            delete. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    name = proto.Field(proto.STRING, number=4)


class ListClustersRequest(proto.Message):
    r"""ListClustersRequest lists clusters.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the parent
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides, or "-" for all zones. This
            field has been deprecated and replaced by the parent field.
        parent (str):
            The parent (project and location) where the clusters will be
            listed. Specified in the format ``projects/*/locations/*``.
            Location "-" matches all zones and all regions.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    parent = proto.Field(proto.STRING, number=4)


class ListClustersResponse(proto.Message):
    r"""ListClustersResponse is the result of ListClustersRequest.

    Attributes:
        clusters (Sequence[~.cluster_service.Cluster]):
            A list of clusters in the project in the
            specified zone, or across all ones.
        missing_zones (Sequence[str]):
            If any zones are listed here, the list of
            clusters returned may be missing those zones.
    """

    clusters = proto.RepeatedField(proto.MESSAGE, number=1, message="Cluster",)

    missing_zones = proto.RepeatedField(proto.STRING, number=2)


class GetOperationRequest(proto.Message):
    r"""GetOperationRequest gets a single operation.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        operation_id (str):
            Required. Deprecated. The server-assigned ``name`` of the
            operation. This field has been deprecated and replaced by
            the name field.
        name (str):
            The name (project, location, operation id) of the operation
            to get. Specified in the format
            ``projects/*/locations/*/operations/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    operation_id = proto.Field(proto.STRING, number=3)

    name = proto.Field(proto.STRING, number=5)


class ListOperationsRequest(proto.Message):
    r"""ListOperationsRequest lists operations.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the parent
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            to return operations for, or ``-`` for all zones. This field
            has been deprecated and replaced by the parent field.
        parent (str):
            The parent (project and location) where the operations will
            be listed. Specified in the format
            ``projects/*/locations/*``. Location "-" matches all zones
            and all regions.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    parent = proto.Field(proto.STRING, number=4)


class CancelOperationRequest(proto.Message):
    r"""CancelOperationRequest cancels a single operation.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the operation resides. This field has been
            deprecated and replaced by the name field.
        operation_id (str):
            Required. Deprecated. The server-assigned ``name`` of the
            operation. This field has been deprecated and replaced by
            the name field.
        name (str):
            The name (project, location, operation id) of the operation
            to cancel. Specified in the format
            ``projects/*/locations/*/operations/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    operation_id = proto.Field(proto.STRING, number=3)

    name = proto.Field(proto.STRING, number=4)


class ListOperationsResponse(proto.Message):
    r"""ListOperationsResponse is the result of
    ListOperationsRequest.

    Attributes:
        operations (Sequence[~.cluster_service.Operation]):
            A list of operations in the project in the
            specified zone.
        missing_zones (Sequence[str]):
            If any zones are listed here, the list of
            operations returned may be missing the
            operations from those zones.
    """

    operations = proto.RepeatedField(proto.MESSAGE, number=1, message="Operation",)

    missing_zones = proto.RepeatedField(proto.STRING, number=2)


class GetServerConfigRequest(proto.Message):
    r"""Gets the current Kubernetes Engine service configuration.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            to return operations for. This field has been deprecated and
            replaced by the name field.
        name (str):
            The name (project and location) of the server config to get,
            specified in the format ``projects/*/locations/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    name = proto.Field(proto.STRING, number=4)


class ServerConfig(proto.Message):
    r"""Kubernetes Engine service configuration.

    Attributes:
        default_cluster_version (str):
            Version of Kubernetes the service deploys by
            default.
        valid_node_versions (Sequence[str]):
            List of valid node upgrade target versions.
        default_image_type (str):
            Default image type.
        valid_image_types (Sequence[str]):
            List of valid image types.
        valid_master_versions (Sequence[str]):
            List of valid master versions.
    """

    default_cluster_version = proto.Field(proto.STRING, number=1)

    valid_node_versions = proto.RepeatedField(proto.STRING, number=3)

    default_image_type = proto.Field(proto.STRING, number=4)

    valid_image_types = proto.RepeatedField(proto.STRING, number=5)

    valid_master_versions = proto.RepeatedField(proto.STRING, number=6)


class CreateNodePoolRequest(proto.Message):
    r"""CreateNodePoolRequest creates a node pool for a cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://developers.google.com/console/help/new/#projectnumber>`__.
            This field has been deprecated and replaced by the parent
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the parent field.
        cluster_id (str):
            Required. Deprecated. The name of the
            cluster. This field has been deprecated and
            replaced by the parent field.
        node_pool (~.cluster_service.NodePool):
            Required. The node pool to create.
        parent (str):
            The parent (project, location, cluster id) where the node
            pool will be created. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    node_pool = proto.Field(proto.MESSAGE, number=4, message="NodePool",)

    parent = proto.Field(proto.STRING, number=6)


class DeleteNodePoolRequest(proto.Message):
    r"""DeleteNodePoolRequest deletes a node pool for a cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://developers.google.com/console/help/new/#projectnumber>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the
            cluster. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Required. Deprecated. The name of the node
            pool to delete. This field has been deprecated
            and replaced by the name field.
        name (str):
            The name (project, location, cluster, node pool id) of the
            node pool to delete. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    node_pool_id = proto.Field(proto.STRING, number=4)

    name = proto.Field(proto.STRING, number=6)


class ListNodePoolsRequest(proto.Message):
    r"""ListNodePoolsRequest lists the node pool(s) for a cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://developers.google.com/console/help/new/#projectnumber>`__.
            This field has been deprecated and replaced by the parent
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the parent field.
        cluster_id (str):
            Required. Deprecated. The name of the
            cluster. This field has been deprecated and
            replaced by the parent field.
        parent (str):
            The parent (project, location, cluster id) where the node
            pools will be listed. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    parent = proto.Field(proto.STRING, number=5)


class GetNodePoolRequest(proto.Message):
    r"""GetNodePoolRequest retrieves a node pool for a cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://developers.google.com/console/help/new/#projectnumber>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the
            cluster. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Required. Deprecated. The name of the node
            pool. This field has been deprecated and
            replaced by the name field.
        name (str):
            The name (project, location, cluster, node pool id) of the
            node pool to get. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    node_pool_id = proto.Field(proto.STRING, number=4)

    name = proto.Field(proto.STRING, number=6)


class NodePool(proto.Message):
    r"""NodePool contains the name and configuration for a cluster's
    node pool. Node pools are a set of nodes (i.e. VM's), with a
    common configuration and specification, under the control of the
    cluster master. They may have a set of Kubernetes labels applied
    to them, which may be used to reference them during pod
    scheduling. They may also be resized up or down, to accommodate
    the workload.

    Attributes:
        name (str):
            The name of the node pool.
        config (~.cluster_service.NodeConfig):
            The node configuration of the pool.
        initial_node_count (int):
            The initial node count for the pool. You must ensure that
            your Compute Engine `resource
            quota <https://cloud.google.com/compute/quotas>`__ is
            sufficient for this number of instances. You must also have
            available firewall and routes quota.
        self_link (str):
            [Output only] Server-defined URL for the resource.
        version (str):
            The version of the Kubernetes of this node.
        instance_group_urls (Sequence[str]):
            [Output only] The resource URLs of the `managed instance
            groups <https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances>`__
            associated with this node pool.
        status (~.cluster_service.NodePool.Status):
            [Output only] The status of the nodes in this pool instance.
        status_message (str):
            [Output only] Additional information about the current
            status of this node pool instance, if available.
        autoscaling (~.cluster_service.NodePoolAutoscaling):
            Autoscaler configuration for this NodePool.
            Autoscaler is enabled only if a valid
            configuration is present.
        management (~.cluster_service.NodeManagement):
            NodeManagement configuration for this
            NodePool.
        max_pods_constraint (~.cluster_service.MaxPodsConstraint):
            The constraint on the maximum number of pods
            that can be run simultaneously on a node in the
            node pool.
        conditions (Sequence[~.cluster_service.StatusCondition]):
            Which conditions caused the current node pool
            state.
        pod_ipv4_cidr_size (int):
            [Output only] The pod CIDR block size per node in this node
            pool.
    """

    class Status(proto.Enum):
        r"""The current status of the node pool instance."""
        STATUS_UNSPECIFIED = 0
        PROVISIONING = 1
        RUNNING = 2
        RUNNING_WITH_ERROR = 3
        RECONCILING = 4
        STOPPING = 5
        ERROR = 6

    name = proto.Field(proto.STRING, number=1)

    config = proto.Field(proto.MESSAGE, number=2, message="NodeConfig",)

    initial_node_count = proto.Field(proto.INT32, number=3)

    self_link = proto.Field(proto.STRING, number=100)

    version = proto.Field(proto.STRING, number=101)

    instance_group_urls = proto.RepeatedField(proto.STRING, number=102)

    status = proto.Field(proto.ENUM, number=103, enum=Status,)

    status_message = proto.Field(proto.STRING, number=104)

    autoscaling = proto.Field(proto.MESSAGE, number=4, message="NodePoolAutoscaling",)

    management = proto.Field(proto.MESSAGE, number=5, message="NodeManagement",)

    max_pods_constraint = proto.Field(
        proto.MESSAGE, number=6, message="MaxPodsConstraint",
    )

    conditions = proto.RepeatedField(
        proto.MESSAGE, number=105, message="StatusCondition",
    )

    pod_ipv4_cidr_size = proto.Field(proto.INT32, number=7)


class NodeManagement(proto.Message):
    r"""NodeManagement defines the set of node management services
    turned on for the node pool.

    Attributes:
        auto_upgrade (bool):
            Whether the nodes will be automatically
            upgraded.
        auto_repair (bool):
            Whether the nodes will be automatically
            repaired.
        upgrade_options (~.cluster_service.AutoUpgradeOptions):
            Specifies the Auto Upgrade knobs for the node
            pool.
    """

    auto_upgrade = proto.Field(proto.BOOL, number=1)

    auto_repair = proto.Field(proto.BOOL, number=2)

    upgrade_options = proto.Field(
        proto.MESSAGE, number=10, message="AutoUpgradeOptions",
    )


class AutoUpgradeOptions(proto.Message):
    r"""AutoUpgradeOptions defines the set of options for the user to
    control how the Auto Upgrades will proceed.

    Attributes:
        auto_upgrade_start_time (str):
            [Output only] This field is set when upgrades are about to
            commence with the approximate start time for the upgrades,
            in `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        description (str):
            [Output only] This field is set when upgrades are about to
            commence with the description of the upgrade.
    """

    auto_upgrade_start_time = proto.Field(proto.STRING, number=1)

    description = proto.Field(proto.STRING, number=2)


class MaintenancePolicy(proto.Message):
    r"""MaintenancePolicy defines the maintenance policy to be used
    for the cluster.

    Attributes:
        window (~.cluster_service.MaintenanceWindow):
            Specifies the maintenance window in which
            maintenance may be performed.
        resource_version (str):
            A hash identifying the version of this
            policy, so that updates to fields of the policy
            won't accidentally undo intermediate changes
            (and so that users of the API unaware of some
            fields won't accidentally remove other fields).
            Make a <code>get()</code> request to the cluster
            to get the current resource version and include
            it with requests to set the policy.
    """

    window = proto.Field(proto.MESSAGE, number=1, message="MaintenanceWindow",)

    resource_version = proto.Field(proto.STRING, number=3)


class MaintenanceWindow(proto.Message):
    r"""MaintenanceWindow defines the maintenance window to be used
    for the cluster.

    Attributes:
        daily_maintenance_window (~.cluster_service.DailyMaintenanceWindow):
            DailyMaintenanceWindow specifies a daily
            maintenance operation window.
        recurring_window (~.cluster_service.RecurringTimeWindow):
            RecurringWindow specifies some number of
            recurring time periods for maintenance to occur.
            The time windows may be overlapping. If no
            maintenance windows are set, maintenance can
            occur at any time.
        maintenance_exclusions (Sequence[~.cluster_service.MaintenanceWindow.MaintenanceExclusionsEntry]):
            Exceptions to maintenance window. Non-
            mergency maintenance should not occur in these
            windows.
    """

    daily_maintenance_window = proto.Field(
        proto.MESSAGE, number=2, oneof="policy", message="DailyMaintenanceWindow",
    )

    recurring_window = proto.Field(
        proto.MESSAGE, number=3, oneof="policy", message="RecurringTimeWindow",
    )

    maintenance_exclusions = proto.MapField(
        proto.STRING, proto.MESSAGE, number=4, message="TimeWindow",
    )


class TimeWindow(proto.Message):
    r"""Represents an arbitrary window of time.

    Attributes:
        start_time (~.timestamp.Timestamp):
            The time that the window first starts.
        end_time (~.timestamp.Timestamp):
            The time that the window ends. The end time
            should take place after the start time.
    """

    start_time = proto.Field(proto.MESSAGE, number=1, message=timestamp.Timestamp,)

    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)


class RecurringTimeWindow(proto.Message):
    r"""Represents an arbitrary window of time that recurs.

    Attributes:
        window (~.cluster_service.TimeWindow):
            The window of the first recurrence.
        recurrence (str):
            An RRULE
            (https://tools.ietf.org/html/rfc5545#section-3.8.5.3)
            for how this window reccurs. They go on for the
            span of time between the start and end time.

            For example, to have something repeat every
            weekday, you'd use:
            <code>FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR</code> To
            repeat some window daily (equivalent to the
            DailyMaintenanceWindow):
            <code>FREQ=DAILY</code>
            For the first weekend of every month:
            <code>FREQ=MONTHLY;BYSETPOS=1;BYDAY=SA,SU</code>
            This specifies how frequently the window starts.
            Eg, if you wanted to have a 9-5 UTC-4 window
            every weekday, you'd use something like: <code>
              start time = 2019-01-01T09:00:00-0400
              end time = 2019-01-01T17:00:00-0400
              recurrence = FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR
            </code>
            Windows can span multiple days. Eg, to make the
            window encompass every weekend from midnight
            Saturday till the last minute of Sunday UTC:
            <code>
              start time = 2019-01-05T00:00:00Z
              end time = 2019-01-07T23:59:00Z
              recurrence = FREQ=WEEKLY;BYDAY=SA
            </code>
            Note the start and end time's specific dates are
            largely arbitrary except to specify duration of
            the window and when it first starts. The FREQ
            values of HOURLY, MINUTELY, and SECONDLY are not
            supported.
    """

    window = proto.Field(proto.MESSAGE, number=1, message="TimeWindow",)

    recurrence = proto.Field(proto.STRING, number=2)


class DailyMaintenanceWindow(proto.Message):
    r"""Time window specified for daily maintenance operations.

    Attributes:
        start_time (str):
            Time within the maintenance window to start the maintenance
            operations. It must be in format "HH:MM", where HH : [00-23]
            and MM : [00-59] GMT.
        duration (str):
            [Output only] Duration of the time window, automatically
            chosen to be smallest possible in the given scenario.
    """

    start_time = proto.Field(proto.STRING, number=2)

    duration = proto.Field(proto.STRING, number=3)


class SetNodePoolManagementRequest(proto.Message):
    r"""SetNodePoolManagementRequest sets the node management
    properties of a node pool.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to update. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Required. Deprecated. The name of the node
            pool to update. This field has been deprecated
            and replaced by the name field.
        management (~.cluster_service.NodeManagement):
            Required. NodeManagement configuration for
            the node pool.
        name (str):
            The name (project, location, cluster, node pool id) of the
            node pool to set management properties. Specified in the
            format ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    node_pool_id = proto.Field(proto.STRING, number=4)

    management = proto.Field(proto.MESSAGE, number=5, message="NodeManagement",)

    name = proto.Field(proto.STRING, number=7)


class SetNodePoolSizeRequest(proto.Message):
    r"""SetNodePoolSizeRequest sets the size a node
    pool.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to update. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Required. Deprecated. The name of the node
            pool to update. This field has been deprecated
            and replaced by the name field.
        node_count (int):
            Required. The desired node count for the
            pool.
        name (str):
            The name (project, location, cluster, node pool id) of the
            node pool to set size. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    node_pool_id = proto.Field(proto.STRING, number=4)

    node_count = proto.Field(proto.INT32, number=5)

    name = proto.Field(proto.STRING, number=7)


class RollbackNodePoolUpgradeRequest(proto.Message):
    r"""RollbackNodePoolUpgradeRequest rollbacks the previously
    Aborted or Failed NodePool upgrade. This will be an no-op if the
    last upgrade successfully completed.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to rollback. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Required. Deprecated. The name of the node
            pool to rollback. This field has been deprecated
            and replaced by the name field.
        name (str):
            The name (project, location, cluster, node pool id) of the
            node poll to rollback upgrade. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    node_pool_id = proto.Field(proto.STRING, number=4)

    name = proto.Field(proto.STRING, number=6)


class ListNodePoolsResponse(proto.Message):
    r"""ListNodePoolsResponse is the result of ListNodePoolsRequest.

    Attributes:
        node_pools (Sequence[~.cluster_service.NodePool]):
            A list of node pools for a cluster.
    """

    node_pools = proto.RepeatedField(proto.MESSAGE, number=1, message="NodePool",)


class ClusterAutoscaling(proto.Message):
    r"""ClusterAutoscaling contains global, per-cluster information
    required by Cluster Autoscaler to automatically adjust the size
    of the cluster and create/delete
    node pools based on the current needs.

    Attributes:
        enable_node_autoprovisioning (bool):
            Enables automatic node pool creation and
            deletion.
        resource_limits (Sequence[~.cluster_service.ResourceLimit]):
            Contains global constraints regarding minimum
            and maximum amount of resources in the cluster.
        autoprovisioning_node_pool_defaults (~.cluster_service.AutoprovisioningNodePoolDefaults):
            AutoprovisioningNodePoolDefaults contains
            defaults for a node pool created by NAP.
        autoprovisioning_locations (Sequence[str]):
            The list of Google Compute Engine
            `zones <https://cloud.google.com/compute/docs/zones#available>`__
            in which the NodePool's nodes can be created by NAP.
    """

    enable_node_autoprovisioning = proto.Field(proto.BOOL, number=1)

    resource_limits = proto.RepeatedField(
        proto.MESSAGE, number=2, message="ResourceLimit",
    )

    autoprovisioning_node_pool_defaults = proto.Field(
        proto.MESSAGE, number=4, message="AutoprovisioningNodePoolDefaults",
    )

    autoprovisioning_locations = proto.RepeatedField(proto.STRING, number=5)


class AutoprovisioningNodePoolDefaults(proto.Message):
    r"""AutoprovisioningNodePoolDefaults contains defaults for a node
    pool created by NAP.

    Attributes:
        oauth_scopes (Sequence[str]):
            Scopes that are used by NAP when creating node pools. If
            oauth_scopes are specified, service_account should be empty.
        service_account (str):
            The Google Cloud Platform Service Account to be used by the
            node VMs. If service_account is specified, scopes should be
            empty.
    """

    oauth_scopes = proto.RepeatedField(proto.STRING, number=1)

    service_account = proto.Field(proto.STRING, number=2)


class ResourceLimit(proto.Message):
    r"""Contains information about amount of some resource in the
    cluster. For memory, value should be in GB.

    Attributes:
        resource_type (str):
            Resource name "cpu", "memory" or gpu-specific
            string.
        minimum (int):
            Minimum amount of the resource in the
            cluster.
        maximum (int):
            Maximum amount of the resource in the
            cluster.
    """

    resource_type = proto.Field(proto.STRING, number=1)

    minimum = proto.Field(proto.INT64, number=2)

    maximum = proto.Field(proto.INT64, number=3)


class NodePoolAutoscaling(proto.Message):
    r"""NodePoolAutoscaling contains information required by cluster
    autoscaler to adjust the size of the node pool to the current
    cluster usage.

    Attributes:
        enabled (bool):
            Is autoscaling enabled for this node pool.
        min_node_count (int):
            Minimum number of nodes in the NodePool. Must be >= 1 and <=
            max_node_count.
        max_node_count (int):
            Maximum number of nodes in the NodePool. Must be >=
            min_node_count. There has to enough quota to scale up the
            cluster.
        autoprovisioned (bool):
            Can this node pool be deleted automatically.
    """

    enabled = proto.Field(proto.BOOL, number=1)

    min_node_count = proto.Field(proto.INT32, number=2)

    max_node_count = proto.Field(proto.INT32, number=3)

    autoprovisioned = proto.Field(proto.BOOL, number=4)


class SetLabelsRequest(proto.Message):
    r"""SetLabelsRequest sets the Google Cloud Platform labels on a
    Google Container Engine cluster, which will in turn set them for
    Google Compute Engine resources used by that cluster

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://developers.google.com/console/help/new/#projectnumber>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the
            cluster. This field has been deprecated and
            replaced by the name field.
        resource_labels (Sequence[~.cluster_service.SetLabelsRequest.ResourceLabelsEntry]):
            Required. The labels to set for that cluster.
        label_fingerprint (str):
            Required. The fingerprint of the previous set
            of labels for this resource, used to detect
            conflicts. The fingerprint is initially
            generated by Kubernetes Engine and changes after
            every request to modify or update labels. You
            must always provide an up-to-date fingerprint
            hash when updating or changing labels. Make a
            <code>get()</code> request to the resource to
            get the latest fingerprint.
        name (str):
            The name (project, location, cluster id) of the cluster to
            set labels. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    resource_labels = proto.MapField(proto.STRING, proto.STRING, number=4)

    label_fingerprint = proto.Field(proto.STRING, number=5)

    name = proto.Field(proto.STRING, number=7)


class SetLegacyAbacRequest(proto.Message):
    r"""SetLegacyAbacRequest enables or disables the ABAC
    authorization mechanism for a cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://support.google.com/cloud/answer/6158840>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the cluster
            to update. This field has been deprecated and
            replaced by the name field.
        enabled (bool):
            Required. Whether ABAC authorization will be
            enabled in the cluster.
        name (str):
            The name (project, location, cluster id) of the cluster to
            set legacy abac. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    enabled = proto.Field(proto.BOOL, number=4)

    name = proto.Field(proto.STRING, number=6)


class StartIPRotationRequest(proto.Message):
    r"""StartIPRotationRequest creates a new IP for the cluster and
    then performs a node upgrade on each node pool to point to the
    new IP.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://developers.google.com/console/help/new/#projectnumber>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the
            cluster. This field has been deprecated and
            replaced by the name field.
        name (str):
            The name (project, location, cluster id) of the cluster to
            start IP rotation. Specified in the format
            ``projects/*/locations/*/clusters/*``.
        rotate_credentials (bool):
            Whether to rotate credentials during IP
            rotation.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    name = proto.Field(proto.STRING, number=6)

    rotate_credentials = proto.Field(proto.BOOL, number=7)


class CompleteIPRotationRequest(proto.Message):
    r"""CompleteIPRotationRequest moves the cluster master back into
    single-IP mode.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://developers.google.com/console/help/new/#projectnumber>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the
            cluster. This field has been deprecated and
            replaced by the name field.
        name (str):
            The name (project, location, cluster id) of the cluster to
            complete IP rotation. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    name = proto.Field(proto.STRING, number=7)


class AcceleratorConfig(proto.Message):
    r"""AcceleratorConfig represents a Hardware Accelerator request.

    Attributes:
        accelerator_count (int):
            The number of the accelerator cards exposed
            to an instance.
        accelerator_type (str):
            The accelerator type resource name. List of supported
            accelerators
            `here <https://cloud.google.com/compute/docs/gpus>`__
    """

    accelerator_count = proto.Field(proto.INT64, number=1)

    accelerator_type = proto.Field(proto.STRING, number=2)


class WorkloadMetadataConfig(proto.Message):
    r"""WorkloadMetadataConfig defines the metadata configuration to
    expose to workloads on the node pool.

    Attributes:
        node_metadata (~.cluster_service.WorkloadMetadataConfig.NodeMetadata):
            NodeMetadata is the configuration for how to
            expose metadata to the workloads running on the
            node.
    """

    class NodeMetadata(proto.Enum):
        r"""NodeMetadata is the configuration for if and how to expose
        the node metadata to the workload running on the node.
        """
        UNSPECIFIED = 0
        SECURE = 1
        EXPOSE = 2

    node_metadata = proto.Field(proto.ENUM, number=1, enum=NodeMetadata,)


class SetNetworkPolicyRequest(proto.Message):
    r"""SetNetworkPolicyRequest enables/disables network policy for a
    cluster.

    Attributes:
        project_id (str):
            Required. Deprecated. The Google Developers Console `project
            ID or project
            number <https://developers.google.com/console/help/new/#projectnumber>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Required. Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Required. Deprecated. The name of the
            cluster. This field has been deprecated and
            replaced by the name field.
        network_policy (~.cluster_service.NetworkPolicy):
            Required. Configuration options for the
            NetworkPolicy feature.
        name (str):
            The name (project, location, cluster id) of the cluster to
            set networking policy. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    network_policy = proto.Field(proto.MESSAGE, number=4, message="NetworkPolicy",)

    name = proto.Field(proto.STRING, number=6)


class SetMaintenancePolicyRequest(proto.Message):
    r"""SetMaintenancePolicyRequest sets the maintenance policy for a
    cluster.

    Attributes:
        project_id (str):
            Required. The Google Developers Console `project ID or
            project
            number <https://support.google.com/cloud/answer/6158840>`__.
        zone (str):
            Required. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides.
        cluster_id (str):
            Required. The name of the cluster to update.
        maintenance_policy (~.cluster_service.MaintenancePolicy):
            Required. The maintenance policy to be set
            for the cluster. An empty field clears the
            existing maintenance policy.
        name (str):
            The name (project, location, cluster id) of the cluster to
            set maintenance policy. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id = proto.Field(proto.STRING, number=1)

    zone = proto.Field(proto.STRING, number=2)

    cluster_id = proto.Field(proto.STRING, number=3)

    maintenance_policy = proto.Field(
        proto.MESSAGE, number=4, message="MaintenancePolicy",
    )

    name = proto.Field(proto.STRING, number=5)


class ListLocationsRequest(proto.Message):
    r"""ListLocationsRequest is used to request the locations that
    offer GKE.

    Attributes:
        parent (str):
            Required. Contains the name of the resource requested.
            Specified in the format ``projects/*``.
    """

    parent = proto.Field(proto.STRING, number=1)


class ListLocationsResponse(proto.Message):
    r"""ListLocationsResponse returns the list of all GKE locations
    and their recommendation state.

    Attributes:
        locations (Sequence[~.cluster_service.Location]):
            A full list of GKE locations.
        next_page_token (str):
            Only return ListLocationsResponse that occur after the
            page_token. This value should be populated from the
            ListLocationsResponse.next_page_token if that response token
            was set (which happens when listing more Locations than fit
            in a single ListLocationsResponse).
    """

    @property
    def raw_page(self):
        return self

    locations = proto.RepeatedField(proto.MESSAGE, number=1, message="Location",)

    next_page_token = proto.Field(proto.STRING, number=2)


class Location(proto.Message):
    r"""Location returns the location name, and if the location is
    recommended for GKE cluster scheduling.

    Attributes:
        type_ (~.cluster_service.Location.LocationType):
            Contains the type of location this Location
            is for. Regional or Zonal.
        name (str):
            Contains the name of the resource requested. Specified in
            the format ``projects/*/locations/*``.
        recommended (bool):
            Whether the location is recomended for GKE
            cluster scheduling.
    """

    class LocationType(proto.Enum):
        r"""LocationType is the type of GKE location, regional or zonal."""
        LOCATION_TYPE_UNSPECIFIED = 0
        ZONE = 1
        REGION = 2

    type_ = proto.Field(proto.ENUM, number=1, enum=LocationType,)

    name = proto.Field(proto.STRING, number=2)

    recommended = proto.Field(proto.BOOL, number=3)


class StatusCondition(proto.Message):
    r"""StatusCondition describes why a cluster or a node pool has a
    certain status (e.g., ERROR or DEGRADED).

    Attributes:
        code (~.cluster_service.StatusCondition.Code):
            Machine-friendly representation of the
            condition
        message (str):
            Human-friendly representation of the
            condition
    """

    class Code(proto.Enum):
        r"""Code for each condition"""
        UNKNOWN = 0
        GCE_STOCKOUT = 1
        GKE_SERVICE_ACCOUNT_DELETED = 2
        GCE_QUOTA_EXCEEDED = 3
        SET_BY_OPERATOR = 4
        CLOUD_KMS_KEY_ERROR = 7

    code = proto.Field(proto.ENUM, number=1, enum=Code,)

    message = proto.Field(proto.STRING, number=2)


class NetworkConfig(proto.Message):
    r"""NetworkConfig reports the relative names of network &
    subnetwork.

    Attributes:
        network (str):
            Output only. The relative name of the Google Compute Engine
            [network]`google.container.v1beta1.NetworkConfig.network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`__
            to which the cluster is connected. Example:
            projects/my-project/global/networks/my-network
        subnetwork (str):
            Output only. The relative name of the Google Compute Engine
            `subnetwork <https://cloud.google.com/compute/docs/vpc>`__
            to which the cluster is connected. Example:
            projects/my-project/regions/us-central1/subnetworks/my-subnet
        enable_intra_node_visibility (bool):
            Whether Intra-node visibility is enabled for
            this cluster. This makes same node pod to pod
            traffic visible for VPC network.
    """

    network = proto.Field(proto.STRING, number=1)

    subnetwork = proto.Field(proto.STRING, number=2)

    enable_intra_node_visibility = proto.Field(proto.BOOL, number=5)


class ListUsableSubnetworksRequest(proto.Message):
    r"""ListUsableSubnetworksRequest requests the list of usable
    subnetworks. available to a user for creating clusters.

    Attributes:
        parent (str):
            Required. The parent project where subnetworks are usable.
            Specified in the format ``projects/*``.
        filter (str):
            Filtering currently only supports equality on the
            networkProjectId and must be in the form:
            "networkProjectId=[PROJECTID]", where ``networkProjectId``
            is the project which owns the listed subnetworks. This
            defaults to the parent project ID.
        page_size (int):
            The max number of results per page that should be returned.
            If the number of available results is larger than
            ``page_size``, a ``next_page_token`` is returned which can
            be used to get the next page of results in subsequent
            requests. Acceptable values are 0 to 500, inclusive.
            (Default: 500)
        page_token (str):
            Specifies a page token to use. Set this to
            the nextPageToken returned by previous list
            requests to get the next page of results.
    """

    parent = proto.Field(proto.STRING, number=1)

    filter = proto.Field(proto.STRING, number=2)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class ListUsableSubnetworksResponse(proto.Message):
    r"""ListUsableSubnetworksResponse is the response of
    ListUsableSubnetworksRequest.

    Attributes:
        subnetworks (Sequence[~.cluster_service.UsableSubnetwork]):
            A list of usable subnetworks in the specified
            network project.
        next_page_token (str):
            This token allows you to get the next page of results for
            list requests. If the number of results is larger than
            ``page_size``, use the ``next_page_token`` as a value for
            the query parameter ``page_token`` in the next request. The
            value will become empty when there are no more pages.
    """

    @property
    def raw_page(self):
        return self

    subnetworks = proto.RepeatedField(
        proto.MESSAGE, number=1, message="UsableSubnetwork",
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class UsableSubnetworkSecondaryRange(proto.Message):
    r"""Secondary IP range of a usable subnetwork.

    Attributes:
        range_name (str):
            The name associated with this subnetwork
            secondary range, used when adding an alias IP
            range to a VM instance.
        ip_cidr_range (str):
            The range of IP addresses belonging to this
            subnetwork secondary range.
        status (~.cluster_service.UsableSubnetworkSecondaryRange.Status):
            This field is to determine the status of the
            secondary range programmably.
    """

    class Status(proto.Enum):
        r"""Status shows the current usage of a secondary IP range."""
        UNKNOWN = 0
        UNUSED = 1
        IN_USE_SERVICE = 2
        IN_USE_SHAREABLE_POD = 3
        IN_USE_MANAGED_POD = 4

    range_name = proto.Field(proto.STRING, number=1)

    ip_cidr_range = proto.Field(proto.STRING, number=2)

    status = proto.Field(proto.ENUM, number=3, enum=Status,)


class UsableSubnetwork(proto.Message):
    r"""UsableSubnetwork resource returns the subnetwork name, its
    associated network and the primary CIDR range.

    Attributes:
        subnetwork (str):
            Subnetwork Name.
            Example: projects/my-project/regions/us-
            central1/subnetworks/my-subnet
        network (str):
            Network Name.
            Example: projects/my-project/global/networks/my-
            network
        ip_cidr_range (str):
            The range of internal addresses that are
            owned by this subnetwork.
        secondary_ip_ranges (Sequence[~.cluster_service.UsableSubnetworkSecondaryRange]):
            Secondary IP ranges.
        status_message (str):
            A human readable status message representing the reasons for
            cases where the caller cannot use the secondary ranges under
            the subnet. For example if the secondary_ip_ranges is empty
            due to a permission issue, an insufficient permission
            message will be given by status_message.
    """

    subnetwork = proto.Field(proto.STRING, number=1)

    network = proto.Field(proto.STRING, number=2)

    ip_cidr_range = proto.Field(proto.STRING, number=3)

    secondary_ip_ranges = proto.RepeatedField(
        proto.MESSAGE, number=4, message="UsableSubnetworkSecondaryRange",
    )

    status_message = proto.Field(proto.STRING, number=5)


class VerticalPodAutoscaling(proto.Message):
    r"""VerticalPodAutoscaling contains global, per-cluster
    information required by Vertical Pod Autoscaler to automatically
    adjust the resources of pods controlled by it.

    Attributes:
        enabled (bool):
            Enables vertical pod autoscaling.
    """

    enabled = proto.Field(proto.BOOL, number=1)


class IntraNodeVisibilityConfig(proto.Message):
    r"""IntraNodeVisibilityConfig contains the desired config of the
    intra-node visibility on this cluster.

    Attributes:
        enabled (bool):
            Enables intra node visibility for this
            cluster.
    """

    enabled = proto.Field(proto.BOOL, number=1)


class MaxPodsConstraint(proto.Message):
    r"""Constraints applied to pods.

    Attributes:
        max_pods_per_node (int):
            Constraint enforced on the max num of pods
            per node.
    """

    max_pods_per_node = proto.Field(proto.INT64, number=1)


class DatabaseEncryption(proto.Message):
    r"""Configuration of etcd encryption.

    Attributes:
        state (~.cluster_service.DatabaseEncryption.State):
            Denotes the state of etcd encryption.
        key_name (str):
            Name of CloudKMS key to use for the
            encryption of secrets in etcd. Ex. projects/my-
            project/locations/global/keyRings/my-
            ring/cryptoKeys/my-key
    """

    class State(proto.Enum):
        r"""State of etcd encryption."""
        UNKNOWN = 0
        ENCRYPTED = 1
        DECRYPTED = 2

    state = proto.Field(proto.ENUM, number=2, enum=State,)

    key_name = proto.Field(proto.STRING, number=1)


class ResourceUsageExportConfig(proto.Message):
    r"""Configuration for exporting cluster resource usages.

    Attributes:
        bigquery_destination (~.cluster_service.ResourceUsageExportConfig.BigQueryDestination):
            Configuration to use BigQuery as usage export
            destination.
        enable_network_egress_metering (bool):
            Whether to enable network egress metering for
            this cluster. If enabled, a daemonset will be
            created in the cluster to meter network egress
            traffic.
        consumption_metering_config (~.cluster_service.ResourceUsageExportConfig.ConsumptionMeteringConfig):
            Configuration to enable resource consumption
            metering.
    """

    class BigQueryDestination(proto.Message):
        r"""Parameters for using BigQuery as the destination of resource
        usage export.

        Attributes:
            dataset_id (str):
                The ID of a BigQuery Dataset.
        """

        dataset_id = proto.Field(proto.STRING, number=1)

    class ConsumptionMeteringConfig(proto.Message):
        r"""Parameters for controlling consumption metering.

        Attributes:
            enabled (bool):
                Whether to enable consumption metering for
                this cluster. If enabled, a second BigQuery
                table will be created to hold resource
                consumption records.
        """

        enabled = proto.Field(proto.BOOL, number=1)

    bigquery_destination = proto.Field(
        proto.MESSAGE, number=1, message=BigQueryDestination,
    )

    enable_network_egress_metering = proto.Field(proto.BOOL, number=2)

    consumption_metering_config = proto.Field(
        proto.MESSAGE, number=3, message=ConsumptionMeteringConfig,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
