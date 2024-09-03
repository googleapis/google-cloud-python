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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.rpc import code_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.container.v1",
    manifest={
        "PrivateIPv6GoogleAccess",
        "UpgradeResourceType",
        "DatapathProvider",
        "NodePoolUpdateStrategy",
        "StackType",
        "IPv6AccessType",
        "InTransitEncryptionConfig",
        "LinuxNodeConfig",
        "WindowsNodeConfig",
        "NodeKubeletConfig",
        "NodeConfig",
        "AdvancedMachineFeatures",
        "NodeNetworkConfig",
        "AdditionalNodeNetworkConfig",
        "AdditionalPodNetworkConfig",
        "ShieldedInstanceConfig",
        "SandboxConfig",
        "GcfsConfig",
        "ReservationAffinity",
        "SoleTenantConfig",
        "ContainerdConfig",
        "NodeTaint",
        "NodeTaints",
        "NodeLabels",
        "ResourceLabels",
        "NetworkTags",
        "MasterAuth",
        "ClientCertificateConfig",
        "AddonsConfig",
        "HttpLoadBalancing",
        "HorizontalPodAutoscaling",
        "KubernetesDashboard",
        "NetworkPolicyConfig",
        "DnsCacheConfig",
        "PrivateClusterMasterGlobalAccessConfig",
        "PrivateClusterConfig",
        "AuthenticatorGroupsConfig",
        "CloudRunConfig",
        "ConfigConnectorConfig",
        "GcePersistentDiskCsiDriverConfig",
        "GcpFilestoreCsiDriverConfig",
        "GcsFuseCsiDriverConfig",
        "RayOperatorConfig",
        "GkeBackupAgentConfig",
        "StatefulHAConfig",
        "MasterAuthorizedNetworksConfig",
        "LegacyAbac",
        "NetworkPolicy",
        "BinaryAuthorization",
        "PodCIDROverprovisionConfig",
        "IPAllocationPolicy",
        "Cluster",
        "K8sBetaAPIConfig",
        "SecurityPostureConfig",
        "NodePoolAutoConfig",
        "NodePoolDefaults",
        "NodeConfigDefaults",
        "ClusterUpdate",
        "AdditionalPodRangesConfig",
        "RangeInfo",
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
        "BlueGreenSettings",
        "NodePool",
        "NodeManagement",
        "BestEffortProvisioning",
        "AutoUpgradeOptions",
        "MaintenancePolicy",
        "MaintenanceWindow",
        "TimeWindow",
        "MaintenanceExclusionOptions",
        "RecurringTimeWindow",
        "DailyMaintenanceWindow",
        "SetNodePoolManagementRequest",
        "SetNodePoolSizeRequest",
        "CompleteNodePoolUpgradeRequest",
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
        "GPUSharingConfig",
        "GPUDriverInstallationConfig",
        "WorkloadMetadataConfig",
        "SetNetworkPolicyRequest",
        "SetMaintenancePolicyRequest",
        "StatusCondition",
        "NetworkConfig",
        "GatewayAPIConfig",
        "ServiceExternalIPsConfig",
        "GetOpenIDConfigRequest",
        "GetOpenIDConfigResponse",
        "GetJSONWebKeysRequest",
        "Jwk",
        "GetJSONWebKeysResponse",
        "CheckAutopilotCompatibilityRequest",
        "AutopilotCompatibilityIssue",
        "CheckAutopilotCompatibilityResponse",
        "ReleaseChannel",
        "CostManagementConfig",
        "IntraNodeVisibilityConfig",
        "ILBSubsettingConfig",
        "DNSConfig",
        "MaxPodsConstraint",
        "WorkloadIdentityConfig",
        "IdentityServiceConfig",
        "MeshCertificates",
        "DatabaseEncryption",
        "ListUsableSubnetworksRequest",
        "ListUsableSubnetworksResponse",
        "UsableSubnetworkSecondaryRange",
        "UsableSubnetwork",
        "ResourceUsageExportConfig",
        "VerticalPodAutoscaling",
        "DefaultSnatStatus",
        "ShieldedNodes",
        "VirtualNIC",
        "FastSocket",
        "NotificationConfig",
        "ConfidentialNodes",
        "UpgradeEvent",
        "UpgradeAvailableEvent",
        "SecurityBulletinEvent",
        "Autopilot",
        "WorkloadPolicyConfig",
        "LoggingConfig",
        "LoggingComponentConfig",
        "RayClusterLoggingConfig",
        "MonitoringConfig",
        "AdvancedDatapathObservabilityConfig",
        "RayClusterMonitoringConfig",
        "NodePoolLoggingConfig",
        "LoggingVariantConfig",
        "MonitoringComponentConfig",
        "ManagedPrometheusConfig",
        "Fleet",
        "LocalNvmeSsdBlockConfig",
        "EphemeralStorageLocalSsdConfig",
        "ResourceManagerTags",
        "EnterpriseConfig",
        "SecondaryBootDisk",
        "SecondaryBootDiskUpdateStrategy",
    },
)


class PrivateIPv6GoogleAccess(proto.Enum):
    r"""PrivateIPv6GoogleAccess controls whether and how the pods can
    communicate with Google Services through gRPC over IPv6.

    Values:
        PRIVATE_IPV6_GOOGLE_ACCESS_UNSPECIFIED (0):
            Default value. Same as DISABLED
        PRIVATE_IPV6_GOOGLE_ACCESS_DISABLED (1):
            No private access to or from Google Services
        PRIVATE_IPV6_GOOGLE_ACCESS_TO_GOOGLE (2):
            Enables private IPv6 access to Google
            Services from GKE
        PRIVATE_IPV6_GOOGLE_ACCESS_BIDIRECTIONAL (3):
            Enables private IPv6 access to and from
            Google Services
    """
    PRIVATE_IPV6_GOOGLE_ACCESS_UNSPECIFIED = 0
    PRIVATE_IPV6_GOOGLE_ACCESS_DISABLED = 1
    PRIVATE_IPV6_GOOGLE_ACCESS_TO_GOOGLE = 2
    PRIVATE_IPV6_GOOGLE_ACCESS_BIDIRECTIONAL = 3


class UpgradeResourceType(proto.Enum):
    r"""UpgradeResourceType is the resource type that is upgrading.
    It is used in upgrade notifications.

    Values:
        UPGRADE_RESOURCE_TYPE_UNSPECIFIED (0):
            Default value. This shouldn't be used.
        MASTER (1):
            Master / control plane
        NODE_POOL (2):
            Node pool
    """
    UPGRADE_RESOURCE_TYPE_UNSPECIFIED = 0
    MASTER = 1
    NODE_POOL = 2


class DatapathProvider(proto.Enum):
    r"""The datapath provider selects the implementation of the
    Kubernetes networking model for service resolution and network
    policy enforcement.

    Values:
        DATAPATH_PROVIDER_UNSPECIFIED (0):
            Default value.
        LEGACY_DATAPATH (1):
            Use the IPTables implementation based on
            kube-proxy.
        ADVANCED_DATAPATH (2):
            Use the eBPF based GKE Dataplane V2 with additional
            features. See the `GKE Dataplane V2
            documentation <https://cloud.google.com/kubernetes-engine/docs/how-to/dataplane-v2>`__
            for more.
    """
    DATAPATH_PROVIDER_UNSPECIFIED = 0
    LEGACY_DATAPATH = 1
    ADVANCED_DATAPATH = 2


class NodePoolUpdateStrategy(proto.Enum):
    r"""Strategy used for node pool update.

    Values:
        NODE_POOL_UPDATE_STRATEGY_UNSPECIFIED (0):
            Default value if unset. GKE internally
            defaults the update strategy to SURGE for
            unspecified strategies.
        BLUE_GREEN (2):
            blue-green upgrade.
        SURGE (3):
            SURGE is the traditional way of upgrade a node pool.
            max_surge and max_unavailable determines the level of
            upgrade parallelism.
    """
    NODE_POOL_UPDATE_STRATEGY_UNSPECIFIED = 0
    BLUE_GREEN = 2
    SURGE = 3


class StackType(proto.Enum):
    r"""Possible values for IP stack type

    Values:
        STACK_TYPE_UNSPECIFIED (0):
            Default value, will be defaulted as IPV4 only
        IPV4 (1):
            Cluster is IPV4 only
        IPV4_IPV6 (2):
            Cluster can use both IPv4 and IPv6
    """
    STACK_TYPE_UNSPECIFIED = 0
    IPV4 = 1
    IPV4_IPV6 = 2


class IPv6AccessType(proto.Enum):
    r"""Possible values for IPv6 access type

    Values:
        IPV6_ACCESS_TYPE_UNSPECIFIED (0):
            Default value, will be defaulted as type
            external.
        INTERNAL (1):
            Access type internal (all v6 addresses are
            internal IPs)
        EXTERNAL (2):
            Access type external (all v6 addresses are
            external IPs)
    """
    IPV6_ACCESS_TYPE_UNSPECIFIED = 0
    INTERNAL = 1
    EXTERNAL = 2


class InTransitEncryptionConfig(proto.Enum):
    r"""Options for in-transit encryption.

    Values:
        IN_TRANSIT_ENCRYPTION_CONFIG_UNSPECIFIED (0):
            Unspecified, will be inferred as default -
            IN_TRANSIT_ENCRYPTION_UNSPECIFIED.
        IN_TRANSIT_ENCRYPTION_DISABLED (1):
            In-transit encryption is disabled.
        IN_TRANSIT_ENCRYPTION_INTER_NODE_TRANSPARENT (2):
            Data in-transit is encrypted using inter-node
            transparent encryption.
    """
    IN_TRANSIT_ENCRYPTION_CONFIG_UNSPECIFIED = 0
    IN_TRANSIT_ENCRYPTION_DISABLED = 1
    IN_TRANSIT_ENCRYPTION_INTER_NODE_TRANSPARENT = 2


class LinuxNodeConfig(proto.Message):
    r"""Parameters that can be configured on Linux nodes.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        sysctls (MutableMapping[str, str]):
            The Linux kernel parameters to be applied to the nodes and
            all pods running on the nodes.

            The following parameters are supported.

            net.core.busy_poll net.core.busy_read
            net.core.netdev_max_backlog net.core.rmem_max
            net.core.wmem_default net.core.wmem_max net.core.optmem_max
            net.core.somaxconn net.ipv4.tcp_rmem net.ipv4.tcp_wmem
            net.ipv4.tcp_tw_reuse
        cgroup_mode (google.cloud.container_v1.types.LinuxNodeConfig.CgroupMode):
            cgroup_mode specifies the cgroup mode to be used on the
            node.
        hugepages (google.cloud.container_v1.types.LinuxNodeConfig.HugepagesConfig):
            Optional. Amounts for 2M and 1G hugepages

            This field is a member of `oneof`_ ``_hugepages``.
    """

    class CgroupMode(proto.Enum):
        r"""Possible cgroup modes that can be used.

        Values:
            CGROUP_MODE_UNSPECIFIED (0):
                CGROUP_MODE_UNSPECIFIED is when unspecified cgroup
                configuration is used. The default for the GKE node OS image
                will be used.
            CGROUP_MODE_V1 (1):
                CGROUP_MODE_V1 specifies to use cgroupv1 for the cgroup
                configuration on the node image.
            CGROUP_MODE_V2 (2):
                CGROUP_MODE_V2 specifies to use cgroupv2 for the cgroup
                configuration on the node image.
        """
        CGROUP_MODE_UNSPECIFIED = 0
        CGROUP_MODE_V1 = 1
        CGROUP_MODE_V2 = 2

    class HugepagesConfig(proto.Message):
        r"""Hugepages amount in both 2m and 1g size

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            hugepage_size2m (int):
                Optional. Amount of 2M hugepages

                This field is a member of `oneof`_ ``_hugepage_size2m``.
            hugepage_size1g (int):
                Optional. Amount of 1G hugepages

                This field is a member of `oneof`_ ``_hugepage_size1g``.
        """

        hugepage_size2m: int = proto.Field(
            proto.INT32,
            number=1,
            optional=True,
        )
        hugepage_size1g: int = proto.Field(
            proto.INT32,
            number=2,
            optional=True,
        )

    sysctls: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )
    cgroup_mode: CgroupMode = proto.Field(
        proto.ENUM,
        number=2,
        enum=CgroupMode,
    )
    hugepages: HugepagesConfig = proto.Field(
        proto.MESSAGE,
        number=3,
        optional=True,
        message=HugepagesConfig,
    )


class WindowsNodeConfig(proto.Message):
    r"""Parameters that can be configured on Windows nodes.
    Windows Node Config that define the parameters that will be used
    to configure the Windows node pool settings

    Attributes:
        os_version (google.cloud.container_v1.types.WindowsNodeConfig.OSVersion):
            OSVersion specifies the Windows node config
            to be used on the node
    """

    class OSVersion(proto.Enum):
        r"""Possible OS version that can be used.

        Values:
            OS_VERSION_UNSPECIFIED (0):
                When OSVersion is not specified
            OS_VERSION_LTSC2019 (1):
                LTSC2019 specifies to use LTSC2019 as the
                Windows Servercore Base Image
            OS_VERSION_LTSC2022 (2):
                LTSC2022 specifies to use LTSC2022 as the
                Windows Servercore Base Image
        """
        OS_VERSION_UNSPECIFIED = 0
        OS_VERSION_LTSC2019 = 1
        OS_VERSION_LTSC2022 = 2

    os_version: OSVersion = proto.Field(
        proto.ENUM,
        number=1,
        enum=OSVersion,
    )


class NodeKubeletConfig(proto.Message):
    r"""Node kubelet configs.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        cpu_manager_policy (str):
            Control the CPU management policy on the node. See
            https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/

            The following values are allowed.

            -  "none": the default, which represents the existing
               scheduling behavior.
            -  "static": allows pods with certain resource
               characteristics to be granted increased CPU affinity and
               exclusivity on the node. The default value is 'none' if
               unspecified.
        cpu_cfs_quota (google.protobuf.wrappers_pb2.BoolValue):
            Enable CPU CFS quota enforcement for
            containers that specify CPU limits.
            This option is enabled by default which makes
            kubelet use CFS quota
            (https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt)
            to enforce container CPU limits. Otherwise, CPU
            limits will not be enforced at all.

            Disable this option to mitigate CPU throttling
            problems while still having your pods to be in
            Guaranteed QoS class by specifying the CPU
            limits.

            The default value is 'true' if unspecified.
        cpu_cfs_quota_period (str):
            Set the CPU CFS quota period value 'cpu.cfs_period_us'.

            The string must be a sequence of decimal numbers, each with
            optional fraction and a unit suffix, such as "300ms". Valid
            time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
            The value must be a positive duration.
        pod_pids_limit (int):
            Set the Pod PID limits. See
            https://kubernetes.io/docs/concepts/policy/pid-limiting/#pod-pid-limits

            Controls the maximum number of processes allowed
            to run in a pod. The value must be greater than
            or equal to 1024 and less than 4194304.
        insecure_kubelet_readonly_port_enabled (bool):
            Enable or disable Kubelet read only port.

            This field is a member of `oneof`_ ``_insecure_kubelet_readonly_port_enabled``.
    """

    cpu_manager_policy: str = proto.Field(
        proto.STRING,
        number=1,
    )
    cpu_cfs_quota: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.BoolValue,
    )
    cpu_cfs_quota_period: str = proto.Field(
        proto.STRING,
        number=3,
    )
    pod_pids_limit: int = proto.Field(
        proto.INT64,
        number=4,
    )
    insecure_kubelet_readonly_port_enabled: bool = proto.Field(
        proto.BOOL,
        number=7,
        optional=True,
    )


class NodeConfig(proto.Message):
    r"""Parameters that describe the nodes in a cluster.

    GKE Autopilot clusters do not recognize parameters in
    ``NodeConfig``. Use
    [AutoprovisioningNodePoolDefaults][google.container.v1.AutoprovisioningNodePoolDefaults]
    instead.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        machine_type (str):
            The name of a Google Compute Engine `machine
            type <https://cloud.google.com/compute/docs/machine-types>`__

            If unspecified, the default machine type is ``e2-medium``.
        disk_size_gb (int):
            Size of the disk attached to each node,
            specified in GB. The smallest allowed disk size
            is 10GB.

            If unspecified, the default disk size is 100GB.
        oauth_scopes (MutableSequence[str]):
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
            be used by the node VMs. Specify the email
            address of the Service Account; otherwise, if no
            Service Account is specified, the "default"
            service account is used.
        metadata (MutableMapping[str, str]):
            The metadata key/value pairs assigned to instances in the
            cluster.

            Keys must conform to the regexp ``[a-zA-Z0-9-_]+`` and be
            less than 128 bytes in length. These are reflected as part
            of a URL in the metadata server. Additionally, to avoid
            ambiguity, keys must not conflict with any other metadata
            keys for the project or be one of the reserved keys:

            -  "cluster-location"
            -  "cluster-name"
            -  "cluster-uid"
            -  "configure-sh"
            -  "containerd-configure-sh"
            -  "enable-os-login"
            -  "gci-ensure-gke-docker"
            -  "gci-metrics-enabled"
            -  "gci-update-strategy"
            -  "instance-template"
            -  "kube-env"
            -  "startup-script"
            -  "user-data"
            -  "disable-address-manager"
            -  "windows-startup-script-ps1"
            -  "common-psm1"
            -  "k8s-node-setup-psm1"
            -  "install-ssh-psm1"
            -  "user-profile-psm1"

            Values are free-form strings, and only have meaning as
            interpreted by the image running in the instance. The only
            restriction placed on them is that each value's size must be
            less than or equal to 32 KB.

            The total size of all keys and values must be less than 512
            KB.
        image_type (str):
            The image type to use for this node. Note
            that for a given image type, the latest version
            of it will be used. Please see
            https://cloud.google.com/kubernetes-engine/docs/concepts/node-images
            for available image types.
        labels (MutableMapping[str, str]):
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

            https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
        local_ssd_count (int):
            The number of local SSD disks to be attached
            to the node.
            The limit for this value is dependent upon the
            maximum number of disks available on a machine
            per zone. See:

            https://cloud.google.com/compute/docs/disks/local-ssd
            for more information.
        tags (MutableSequence[str]):
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
            for more information about preemptible VM
            instances.
        accelerators (MutableSequence[google.cloud.container_v1.types.AcceleratorConfig]):
            A list of hardware accelerators to be
            attached to each node. See
            https://cloud.google.com/compute/docs/gpus for
            more information about support for GPUs.
        disk_type (str):
            Type of the disk attached to each node (e.g.
            'pd-standard', 'pd-ssd' or 'pd-balanced')

            If unspecified, the default disk type is
            'pd-standard'
        min_cpu_platform (str):
            Minimum CPU platform to be used by this instance. The
            instance may be scheduled on the specified or newer CPU
            platform. Applicable values are the friendly names of CPU
            platforms, such as ``minCpuPlatform: "Intel Haswell"`` or
            ``minCpuPlatform: "Intel Sandy Bridge"``. For more
            information, read `how to specify min CPU
            platform <https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform>`__
        workload_metadata_config (google.cloud.container_v1.types.WorkloadMetadataConfig):
            The workload metadata configuration for this
            node.
        taints (MutableSequence[google.cloud.container_v1.types.NodeTaint]):
            List of kubernetes taints to be applied to
            each node.
            For more information, including usage and the
            valid values, see:

            https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
        sandbox_config (google.cloud.container_v1.types.SandboxConfig):
            Sandbox configuration for this node.
        node_group (str):
            Setting this field will assign instances of this pool to run
            on the specified node group. This is useful for running
            workloads on `sole tenant
            nodes <https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes>`__.
        reservation_affinity (google.cloud.container_v1.types.ReservationAffinity):
            The optional reservation affinity. Setting this field will
            apply the specified `Zonal Compute
            Reservation <https://cloud.google.com/compute/docs/instances/reserving-zonal-resources>`__
            to this node pool.
        shielded_instance_config (google.cloud.container_v1.types.ShieldedInstanceConfig):
            Shielded Instance options.
        linux_node_config (google.cloud.container_v1.types.LinuxNodeConfig):
            Parameters that can be configured on Linux
            nodes.
        kubelet_config (google.cloud.container_v1.types.NodeKubeletConfig):
            Node kubelet configs.
        boot_disk_kms_key (str):
            The Customer Managed Encryption Key used to encrypt the boot
            disk attached to each node in the node pool. This should be
            of the form
            projects/[KEY_PROJECT_ID]/locations/[LOCATION]/keyRings/[RING_NAME]/cryptoKeys/[KEY_NAME].
            For more information about protecting resources with Cloud
            KMS Keys please see:
            https://cloud.google.com/compute/docs/disks/customer-managed-encryption
        gcfs_config (google.cloud.container_v1.types.GcfsConfig):
            Google Container File System (image
            streaming) configs.
        advanced_machine_features (google.cloud.container_v1.types.AdvancedMachineFeatures):
            Advanced features for the Compute Engine VM.
        gvnic (google.cloud.container_v1.types.VirtualNIC):
            Enable or disable gvnic in the node pool.
        spot (bool):
            Spot flag for enabling Spot VM, which is a
            rebrand of the existing preemptible flag.
        confidential_nodes (google.cloud.container_v1.types.ConfidentialNodes):
            Confidential nodes config.
            All the nodes in the node pool will be
            Confidential VM once enabled.
        fast_socket (google.cloud.container_v1.types.FastSocket):
            Enable or disable NCCL fast socket for the
            node pool.

            This field is a member of `oneof`_ ``_fast_socket``.
        resource_labels (MutableMapping[str, str]):
            The resource labels for the node pool to use
            to annotate any related Google Compute Engine
            resources.
        logging_config (google.cloud.container_v1.types.NodePoolLoggingConfig):
            Logging configuration.
        windows_node_config (google.cloud.container_v1.types.WindowsNodeConfig):
            Parameters that can be configured on Windows
            nodes.
        local_nvme_ssd_block_config (google.cloud.container_v1.types.LocalNvmeSsdBlockConfig):
            Parameters for using raw-block Local NVMe
            SSDs.
        ephemeral_storage_local_ssd_config (google.cloud.container_v1.types.EphemeralStorageLocalSsdConfig):
            Parameters for the node ephemeral storage
            using Local SSDs. If unspecified, ephemeral
            storage is backed by the boot disk.
        sole_tenant_config (google.cloud.container_v1.types.SoleTenantConfig):
            Parameters for node pools to be backed by
            shared sole tenant node groups.
        containerd_config (google.cloud.container_v1.types.ContainerdConfig):
            Parameters for containerd customization.
        resource_manager_tags (google.cloud.container_v1.types.ResourceManagerTags):
            A map of resource manager tag keys and values
            to be attached to the nodes.
        enable_confidential_storage (bool):
            Optional. Reserved for future use.
        secondary_boot_disks (MutableSequence[google.cloud.container_v1.types.SecondaryBootDisk]):
            List of secondary boot disks attached to the
            nodes.
        secondary_boot_disk_update_strategy (google.cloud.container_v1.types.SecondaryBootDiskUpdateStrategy):
            Secondary boot disk update strategy.

            This field is a member of `oneof`_ ``_secondary_boot_disk_update_strategy``.
    """

    machine_type: str = proto.Field(
        proto.STRING,
        number=1,
    )
    disk_size_gb: int = proto.Field(
        proto.INT32,
        number=2,
    )
    oauth_scopes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    service_account: str = proto.Field(
        proto.STRING,
        number=9,
    )
    metadata: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    image_type: str = proto.Field(
        proto.STRING,
        number=5,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    local_ssd_count: int = proto.Field(
        proto.INT32,
        number=7,
    )
    tags: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=8,
    )
    preemptible: bool = proto.Field(
        proto.BOOL,
        number=10,
    )
    accelerators: MutableSequence["AcceleratorConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=11,
        message="AcceleratorConfig",
    )
    disk_type: str = proto.Field(
        proto.STRING,
        number=12,
    )
    min_cpu_platform: str = proto.Field(
        proto.STRING,
        number=13,
    )
    workload_metadata_config: "WorkloadMetadataConfig" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="WorkloadMetadataConfig",
    )
    taints: MutableSequence["NodeTaint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=15,
        message="NodeTaint",
    )
    sandbox_config: "SandboxConfig" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="SandboxConfig",
    )
    node_group: str = proto.Field(
        proto.STRING,
        number=18,
    )
    reservation_affinity: "ReservationAffinity" = proto.Field(
        proto.MESSAGE,
        number=19,
        message="ReservationAffinity",
    )
    shielded_instance_config: "ShieldedInstanceConfig" = proto.Field(
        proto.MESSAGE,
        number=20,
        message="ShieldedInstanceConfig",
    )
    linux_node_config: "LinuxNodeConfig" = proto.Field(
        proto.MESSAGE,
        number=21,
        message="LinuxNodeConfig",
    )
    kubelet_config: "NodeKubeletConfig" = proto.Field(
        proto.MESSAGE,
        number=22,
        message="NodeKubeletConfig",
    )
    boot_disk_kms_key: str = proto.Field(
        proto.STRING,
        number=23,
    )
    gcfs_config: "GcfsConfig" = proto.Field(
        proto.MESSAGE,
        number=25,
        message="GcfsConfig",
    )
    advanced_machine_features: "AdvancedMachineFeatures" = proto.Field(
        proto.MESSAGE,
        number=26,
        message="AdvancedMachineFeatures",
    )
    gvnic: "VirtualNIC" = proto.Field(
        proto.MESSAGE,
        number=29,
        message="VirtualNIC",
    )
    spot: bool = proto.Field(
        proto.BOOL,
        number=32,
    )
    confidential_nodes: "ConfidentialNodes" = proto.Field(
        proto.MESSAGE,
        number=35,
        message="ConfidentialNodes",
    )
    fast_socket: "FastSocket" = proto.Field(
        proto.MESSAGE,
        number=36,
        optional=True,
        message="FastSocket",
    )
    resource_labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=37,
    )
    logging_config: "NodePoolLoggingConfig" = proto.Field(
        proto.MESSAGE,
        number=38,
        message="NodePoolLoggingConfig",
    )
    windows_node_config: "WindowsNodeConfig" = proto.Field(
        proto.MESSAGE,
        number=39,
        message="WindowsNodeConfig",
    )
    local_nvme_ssd_block_config: "LocalNvmeSsdBlockConfig" = proto.Field(
        proto.MESSAGE,
        number=40,
        message="LocalNvmeSsdBlockConfig",
    )
    ephemeral_storage_local_ssd_config: "EphemeralStorageLocalSsdConfig" = proto.Field(
        proto.MESSAGE,
        number=41,
        message="EphemeralStorageLocalSsdConfig",
    )
    sole_tenant_config: "SoleTenantConfig" = proto.Field(
        proto.MESSAGE,
        number=42,
        message="SoleTenantConfig",
    )
    containerd_config: "ContainerdConfig" = proto.Field(
        proto.MESSAGE,
        number=43,
        message="ContainerdConfig",
    )
    resource_manager_tags: "ResourceManagerTags" = proto.Field(
        proto.MESSAGE,
        number=45,
        message="ResourceManagerTags",
    )
    enable_confidential_storage: bool = proto.Field(
        proto.BOOL,
        number=46,
    )
    secondary_boot_disks: MutableSequence["SecondaryBootDisk"] = proto.RepeatedField(
        proto.MESSAGE,
        number=48,
        message="SecondaryBootDisk",
    )
    secondary_boot_disk_update_strategy: "SecondaryBootDiskUpdateStrategy" = (
        proto.Field(
            proto.MESSAGE,
            number=50,
            optional=True,
            message="SecondaryBootDiskUpdateStrategy",
        )
    )


class AdvancedMachineFeatures(proto.Message):
    r"""Specifies options for controlling advanced machine features.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        threads_per_core (int):
            The number of threads per physical core. To
            disable simultaneous multithreading (SMT) set
            this to 1. If unset, the maximum number of
            threads supported per core by the underlying
            processor is assumed.

            This field is a member of `oneof`_ ``_threads_per_core``.
        enable_nested_virtualization (bool):
            Whether or not to enable nested
            virtualization (defaults to false).

            This field is a member of `oneof`_ ``_enable_nested_virtualization``.
    """

    threads_per_core: int = proto.Field(
        proto.INT64,
        number=1,
        optional=True,
    )
    enable_nested_virtualization: bool = proto.Field(
        proto.BOOL,
        number=2,
        optional=True,
    )


class NodeNetworkConfig(proto.Message):
    r"""Parameters for node pool-level network config.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        create_pod_range (bool):
            Input only. Whether to create a new range for pod IPs in
            this node pool. Defaults are provided for ``pod_range`` and
            ``pod_ipv4_cidr_block`` if they are not specified.

            If neither ``create_pod_range`` or ``pod_range`` are
            specified, the cluster-level default
            (``ip_allocation_policy.cluster_ipv4_cidr_block``) is used.

            Only applicable if ``ip_allocation_policy.use_ip_aliases``
            is true.

            This field cannot be changed after the node pool has been
            created.
        pod_range (str):
            The ID of the secondary range for pod IPs. If
            ``create_pod_range`` is true, this ID is used for the new
            range. If ``create_pod_range`` is false, uses an existing
            secondary range with this ID.

            Only applicable if ``ip_allocation_policy.use_ip_aliases``
            is true.

            This field cannot be changed after the node pool has been
            created.
        pod_ipv4_cidr_block (str):
            The IP address range for pod IPs in this node pool.

            Only applicable if ``create_pod_range`` is true.

            Set to blank to have a range chosen with the default size.

            Set to /netmask (e.g. ``/14``) to have a range chosen with a
            specific netmask.

            Set to a
            `CIDR <https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``10.96.0.0/14``) to pick a specific range to
            use.

            Only applicable if ``ip_allocation_policy.use_ip_aliases``
            is true.

            This field cannot be changed after the node pool has been
            created.
        enable_private_nodes (bool):
            Whether nodes have internal IP addresses only. If
            enable_private_nodes is not specified, then the value is
            derived from
            [cluster.privateClusterConfig.enablePrivateNodes][google.container.v1beta1.PrivateClusterConfig.enablePrivateNodes]

            This field is a member of `oneof`_ ``_enable_private_nodes``.
        network_performance_config (google.cloud.container_v1.types.NodeNetworkConfig.NetworkPerformanceConfig):
            Network bandwidth tier configuration.

            This field is a member of `oneof`_ ``_network_performance_config``.
        pod_cidr_overprovision_config (google.cloud.container_v1.types.PodCIDROverprovisionConfig):
            [PRIVATE FIELD] Pod CIDR size overprovisioning config for
            the nodepool.

            Pod CIDR size per node depends on max_pods_per_node. By
            default, the value of max_pods_per_node is rounded off to
            next power of 2 and we then double that to get the size of
            pod CIDR block per node. Example: max_pods_per_node of 30
            would result in 64 IPs (/26).

            This config can disable the doubling of IPs (we still round
            off to next power of 2) Example: max_pods_per_node of 30
            will result in 32 IPs (/27) when overprovisioning is
            disabled.
        additional_node_network_configs (MutableSequence[google.cloud.container_v1.types.AdditionalNodeNetworkConfig]):
            We specify the additional node networks for
            this node pool using this list. Each node
            network corresponds to an additional interface
        additional_pod_network_configs (MutableSequence[google.cloud.container_v1.types.AdditionalPodNetworkConfig]):
            We specify the additional pod networks for
            this node pool using this list. Each pod network
            corresponds to an additional alias IP range for
            the node
        pod_ipv4_range_utilization (float):
            Output only. The utilization of the IPv4 range for the pod.
            The ratio is Usage/[Total number of IPs in the secondary
            range], Usage=numNodes\ *numZones*\ podIPsPerNode.
    """

    class NetworkPerformanceConfig(proto.Message):
        r"""Configuration of all network bandwidth tiers

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            total_egress_bandwidth_tier (google.cloud.container_v1.types.NodeNetworkConfig.NetworkPerformanceConfig.Tier):
                Specifies the total network bandwidth tier
                for the NodePool.

                This field is a member of `oneof`_ ``_total_egress_bandwidth_tier``.
        """

        class Tier(proto.Enum):
            r"""Node network tier

            Values:
                TIER_UNSPECIFIED (0):
                    Default value
                TIER_1 (1):
                    Higher bandwidth, actual values based on VM
                    size.
            """
            TIER_UNSPECIFIED = 0
            TIER_1 = 1

        total_egress_bandwidth_tier: "NodeNetworkConfig.NetworkPerformanceConfig.Tier" = proto.Field(
            proto.ENUM,
            number=1,
            optional=True,
            enum="NodeNetworkConfig.NetworkPerformanceConfig.Tier",
        )

    create_pod_range: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    pod_range: str = proto.Field(
        proto.STRING,
        number=5,
    )
    pod_ipv4_cidr_block: str = proto.Field(
        proto.STRING,
        number=6,
    )
    enable_private_nodes: bool = proto.Field(
        proto.BOOL,
        number=9,
        optional=True,
    )
    network_performance_config: NetworkPerformanceConfig = proto.Field(
        proto.MESSAGE,
        number=11,
        optional=True,
        message=NetworkPerformanceConfig,
    )
    pod_cidr_overprovision_config: "PodCIDROverprovisionConfig" = proto.Field(
        proto.MESSAGE,
        number=13,
        message="PodCIDROverprovisionConfig",
    )
    additional_node_network_configs: MutableSequence[
        "AdditionalNodeNetworkConfig"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message="AdditionalNodeNetworkConfig",
    )
    additional_pod_network_configs: MutableSequence[
        "AdditionalPodNetworkConfig"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=15,
        message="AdditionalPodNetworkConfig",
    )
    pod_ipv4_range_utilization: float = proto.Field(
        proto.DOUBLE,
        number=16,
    )


class AdditionalNodeNetworkConfig(proto.Message):
    r"""AdditionalNodeNetworkConfig is the configuration for
    additional node networks within the NodeNetworkConfig message

    Attributes:
        network (str):
            Name of the VPC where the additional
            interface belongs
        subnetwork (str):
            Name of the subnetwork where the additional
            interface belongs
    """

    network: str = proto.Field(
        proto.STRING,
        number=1,
    )
    subnetwork: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AdditionalPodNetworkConfig(proto.Message):
    r"""AdditionalPodNetworkConfig is the configuration for
    additional pod networks within the NodeNetworkConfig message


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        subnetwork (str):
            Name of the subnetwork where the additional
            pod network belongs.
        secondary_pod_range (str):
            The name of the secondary range on the subnet
            which provides IP address for this pod range.
        max_pods_per_node (google.cloud.container_v1.types.MaxPodsConstraint):
            The maximum number of pods per node which use
            this pod network.

            This field is a member of `oneof`_ ``_max_pods_per_node``.
    """

    subnetwork: str = proto.Field(
        proto.STRING,
        number=1,
    )
    secondary_pod_range: str = proto.Field(
        proto.STRING,
        number=2,
    )
    max_pods_per_node: "MaxPodsConstraint" = proto.Field(
        proto.MESSAGE,
        number=3,
        optional=True,
        message="MaxPodsConstraint",
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

    enable_secure_boot: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    enable_integrity_monitoring: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class SandboxConfig(proto.Message):
    r"""SandboxConfig contains configurations of the sandbox to use
    for the node.

    Attributes:
        type_ (google.cloud.container_v1.types.SandboxConfig.Type):
            Type of the sandbox to use for the node.
    """

    class Type(proto.Enum):
        r"""Possible types of sandboxes.

        Values:
            UNSPECIFIED (0):
                Default value. This should not be used.
            GVISOR (1):
                Run sandbox using gvisor.
        """
        UNSPECIFIED = 0
        GVISOR = 1

    type_: Type = proto.Field(
        proto.ENUM,
        number=2,
        enum=Type,
    )


class GcfsConfig(proto.Message):
    r"""GcfsConfig contains configurations of Google Container File
    System (image streaming).

    Attributes:
        enabled (bool):
            Whether to use GCFS.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class ReservationAffinity(proto.Message):
    r"""`ReservationAffinity <https://cloud.google.com/compute/docs/instances/reserving-zonal-resources>`__
    is the configuration of desired reservation which instances could
    take capacity from.

    Attributes:
        consume_reservation_type (google.cloud.container_v1.types.ReservationAffinity.Type):
            Corresponds to the type of reservation
            consumption.
        key (str):
            Corresponds to the label key of a reservation resource. To
            target a SPECIFIC_RESERVATION by name, specify
            "compute.googleapis.com/reservation-name" as the key and
            specify the name of your reservation as its value.
        values (MutableSequence[str]):
            Corresponds to the label value(s) of
            reservation resource(s).
    """

    class Type(proto.Enum):
        r"""Indicates whether to consume capacity from a reservation or
        not.

        Values:
            UNSPECIFIED (0):
                Default value. This should not be used.
            NO_RESERVATION (1):
                Do not consume from any reserved capacity.
            ANY_RESERVATION (2):
                Consume any reservation available.
            SPECIFIC_RESERVATION (3):
                Must consume from a specific reservation.
                Must specify key value fields for specifying the
                reservations.
        """
        UNSPECIFIED = 0
        NO_RESERVATION = 1
        ANY_RESERVATION = 2
        SPECIFIC_RESERVATION = 3

    consume_reservation_type: Type = proto.Field(
        proto.ENUM,
        number=1,
        enum=Type,
    )
    key: str = proto.Field(
        proto.STRING,
        number=2,
    )
    values: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class SoleTenantConfig(proto.Message):
    r"""SoleTenantConfig contains the NodeAffinities to specify what
    shared sole tenant node groups should back the node pool.

    Attributes:
        node_affinities (MutableSequence[google.cloud.container_v1.types.SoleTenantConfig.NodeAffinity]):
            NodeAffinities used to match to a shared sole
            tenant node group.
    """

    class NodeAffinity(proto.Message):
        r"""Specifies the NodeAffinity key, values, and affinity operator
        according to `shared sole tenant node group
        affinities <https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes#node_affinity_and_anti-affinity>`__.

        Attributes:
            key (str):
                Key for NodeAffinity.
            operator (google.cloud.container_v1.types.SoleTenantConfig.NodeAffinity.Operator):
                Operator for NodeAffinity.
            values (MutableSequence[str]):
                Values for NodeAffinity.
        """

        class Operator(proto.Enum):
            r"""Operator allows user to specify affinity or anti-affinity for
            the given key values.

            Values:
                OPERATOR_UNSPECIFIED (0):
                    Invalid or unspecified affinity operator.
                IN (1):
                    Affinity operator.
                NOT_IN (2):
                    Anti-affinity operator.
            """
            OPERATOR_UNSPECIFIED = 0
            IN = 1
            NOT_IN = 2

        key: str = proto.Field(
            proto.STRING,
            number=1,
        )
        operator: "SoleTenantConfig.NodeAffinity.Operator" = proto.Field(
            proto.ENUM,
            number=2,
            enum="SoleTenantConfig.NodeAffinity.Operator",
        )
        values: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=3,
        )

    node_affinities: MutableSequence[NodeAffinity] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=NodeAffinity,
    )


class ContainerdConfig(proto.Message):
    r"""ContainerdConfig contains configuration to customize
    containerd.

    Attributes:
        private_registry_access_config (google.cloud.container_v1.types.ContainerdConfig.PrivateRegistryAccessConfig):
            PrivateRegistryAccessConfig is used to
            configure access configuration for private
            container registries.
    """

    class PrivateRegistryAccessConfig(proto.Message):
        r"""PrivateRegistryAccessConfig contains access configuration for
        private container registries.

        Attributes:
            enabled (bool):
                Private registry access is enabled.
            certificate_authority_domain_config (MutableSequence[google.cloud.container_v1.types.ContainerdConfig.PrivateRegistryAccessConfig.CertificateAuthorityDomainConfig]):
                Private registry access configuration.
        """

        class CertificateAuthorityDomainConfig(proto.Message):
            r"""CertificateAuthorityDomainConfig configures one or more fully
            qualified domain names (FQDN) to a specific certificate.


            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                fqdns (MutableSequence[str]):
                    List of fully qualified domain names (FQDN).
                    Specifying port is supported.
                    Wilcards are NOT supported.
                    Examples:

                    - my.customdomain.com
                    - 10.0.1.2:5000
                gcp_secret_manager_certificate_config (google.cloud.container_v1.types.ContainerdConfig.PrivateRegistryAccessConfig.CertificateAuthorityDomainConfig.GCPSecretManagerCertificateConfig):
                    Google Secret Manager (GCP) certificate
                    configuration.

                    This field is a member of `oneof`_ ``certificate_config``.
            """

            class GCPSecretManagerCertificateConfig(proto.Message):
                r"""GCPSecretManagerCertificateConfig configures a secret from `Google
                Secret Manager <https://cloud.google.com/secret-manager>`__.

                Attributes:
                    secret_uri (str):
                        Secret URI, in the form
                        "projects/$PROJECT_ID/secrets/$SECRET_NAME/versions/$VERSION".
                        Version can be fixed (e.g. "2") or "latest".
                """

                secret_uri: str = proto.Field(
                    proto.STRING,
                    number=1,
                )

            fqdns: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=1,
            )
            gcp_secret_manager_certificate_config: "ContainerdConfig.PrivateRegistryAccessConfig.CertificateAuthorityDomainConfig.GCPSecretManagerCertificateConfig" = proto.Field(
                proto.MESSAGE,
                number=2,
                oneof="certificate_config",
                message="ContainerdConfig.PrivateRegistryAccessConfig.CertificateAuthorityDomainConfig.GCPSecretManagerCertificateConfig",
            )

        enabled: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        certificate_authority_domain_config: MutableSequence[
            "ContainerdConfig.PrivateRegistryAccessConfig.CertificateAuthorityDomainConfig"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="ContainerdConfig.PrivateRegistryAccessConfig.CertificateAuthorityDomainConfig",
        )

    private_registry_access_config: PrivateRegistryAccessConfig = proto.Field(
        proto.MESSAGE,
        number=1,
        message=PrivateRegistryAccessConfig,
    )


class NodeTaint(proto.Message):
    r"""Kubernetes taint is composed of three fields: key, value, and
    effect. Effect can only be one of three types: NoSchedule,
    PreferNoSchedule or NoExecute.

    See
    `here <https://kubernetes.io/docs/concepts/configuration/taint-and-toleration>`__
    for more information, including usage and the valid values.

    Attributes:
        key (str):
            Key for taint.
        value (str):
            Value for taint.
        effect (google.cloud.container_v1.types.NodeTaint.Effect):
            Effect for taint.
    """

    class Effect(proto.Enum):
        r"""Possible values for Effect in taint.

        Values:
            EFFECT_UNSPECIFIED (0):
                Not set
            NO_SCHEDULE (1):
                NoSchedule
            PREFER_NO_SCHEDULE (2):
                PreferNoSchedule
            NO_EXECUTE (3):
                NoExecute
        """
        EFFECT_UNSPECIFIED = 0
        NO_SCHEDULE = 1
        PREFER_NO_SCHEDULE = 2
        NO_EXECUTE = 3

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value: str = proto.Field(
        proto.STRING,
        number=2,
    )
    effect: Effect = proto.Field(
        proto.ENUM,
        number=3,
        enum=Effect,
    )


class NodeTaints(proto.Message):
    r"""Collection of Kubernetes `node
    taints <https://kubernetes.io/docs/concepts/configuration/taint-and-toleration>`__.

    Attributes:
        taints (MutableSequence[google.cloud.container_v1.types.NodeTaint]):
            List of node taints.
    """

    taints: MutableSequence["NodeTaint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="NodeTaint",
    )


class NodeLabels(proto.Message):
    r"""Collection of node-level `Kubernetes
    labels <https://kubernetes.io/docs/concepts/overview/working-with-objects/labels>`__.

    Attributes:
        labels (MutableMapping[str, str]):
            Map of node label keys and node label values.
    """

    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )


class ResourceLabels(proto.Message):
    r"""Collection of `GCP
    labels <https://cloud.google.com/resource-manager/docs/creating-managing-labels>`__.

    Attributes:
        labels (MutableMapping[str, str]):
            Map of node label keys and node label values.
    """

    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )


class NetworkTags(proto.Message):
    r"""Collection of Compute Engine network tags that can be applied
    to a node's underlying VM instance.

    Attributes:
        tags (MutableSequence[str]):
            List of network tags.
    """

    tags: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


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

            Warning: basic authentication is deprecated, and
            will be removed in GKE control plane versions
            1.19 and newer. For a list of recommended
            authentication methods, see:

            https://cloud.google.com/kubernetes-engine/docs/how-to/api-server-authentication
        password (str):
            The password to use for HTTP basic
            authentication to the master endpoint. Because
            the master endpoint is open to the Internet, you
            should create a strong password.  If a password
            is provided for cluster creation, username must
            be non-empty.

            Warning: basic authentication is deprecated, and
            will be removed in GKE control plane versions
            1.19 and newer. For a list of recommended
            authentication methods, see:

            https://cloud.google.com/kubernetes-engine/docs/how-to/api-server-authentication
        client_certificate_config (google.cloud.container_v1.types.ClientCertificateConfig):
            Configuration for client certificate
            authentication on the cluster. For clusters
            before v1.12, if no configuration is specified,
            a client certificate is issued.
        cluster_ca_certificate (str):
            Output only. Base64-encoded public
            certificate that is the root of trust for the
            cluster.
        client_certificate (str):
            Output only. Base64-encoded public
            certificate used by clients to authenticate to
            the cluster endpoint.
        client_key (str):
            Output only. Base64-encoded private key used
            by clients to authenticate to the cluster
            endpoint.
    """

    username: str = proto.Field(
        proto.STRING,
        number=1,
    )
    password: str = proto.Field(
        proto.STRING,
        number=2,
    )
    client_certificate_config: "ClientCertificateConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="ClientCertificateConfig",
    )
    cluster_ca_certificate: str = proto.Field(
        proto.STRING,
        number=100,
    )
    client_certificate: str = proto.Field(
        proto.STRING,
        number=101,
    )
    client_key: str = proto.Field(
        proto.STRING,
        number=102,
    )


class ClientCertificateConfig(proto.Message):
    r"""Configuration for client certificates on the cluster.

    Attributes:
        issue_client_certificate (bool):
            Issue a client certificate.
    """

    issue_client_certificate: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class AddonsConfig(proto.Message):
    r"""Configuration for the addons that can be automatically spun
    up in the cluster, enabling additional functionality.

    Attributes:
        http_load_balancing (google.cloud.container_v1.types.HttpLoadBalancing):
            Configuration for the HTTP (L7) load
            balancing controller addon, which makes it easy
            to set up HTTP load balancers for services in a
            cluster.
        horizontal_pod_autoscaling (google.cloud.container_v1.types.HorizontalPodAutoscaling):
            Configuration for the horizontal pod
            autoscaling feature, which increases or
            decreases the number of replica pods a
            replication controller has based on the resource
            usage of the existing pods.
        kubernetes_dashboard (google.cloud.container_v1.types.KubernetesDashboard):
            Configuration for the Kubernetes Dashboard.
            This addon is deprecated, and will be disabled
            in 1.15. It is recommended to use the Cloud
            Console to manage and monitor your Kubernetes
            clusters, workloads and applications. For more
            information, see:

            https://cloud.google.com/kubernetes-engine/docs/concepts/dashboards
        network_policy_config (google.cloud.container_v1.types.NetworkPolicyConfig):
            Configuration for NetworkPolicy. This only
            tracks whether the addon is enabled or not on
            the Master, it does not track whether network
            policy is enabled for the nodes.
        cloud_run_config (google.cloud.container_v1.types.CloudRunConfig):
            Configuration for the Cloud Run addon, which
            allows the user to use a managed Knative
            service.
        dns_cache_config (google.cloud.container_v1.types.DnsCacheConfig):
            Configuration for NodeLocalDNS, a dns cache
            running on cluster nodes
        config_connector_config (google.cloud.container_v1.types.ConfigConnectorConfig):
            Configuration for the ConfigConnector add-on,
            a Kubernetes extension to manage hosted GCP
            services through the Kubernetes API
        gce_persistent_disk_csi_driver_config (google.cloud.container_v1.types.GcePersistentDiskCsiDriverConfig):
            Configuration for the Compute Engine
            Persistent Disk CSI driver.
        gcp_filestore_csi_driver_config (google.cloud.container_v1.types.GcpFilestoreCsiDriverConfig):
            Configuration for the GCP Filestore CSI
            driver.
        gke_backup_agent_config (google.cloud.container_v1.types.GkeBackupAgentConfig):
            Configuration for the Backup for GKE agent
            addon.
        gcs_fuse_csi_driver_config (google.cloud.container_v1.types.GcsFuseCsiDriverConfig):
            Configuration for the Cloud Storage Fuse CSI
            driver.
        stateful_ha_config (google.cloud.container_v1.types.StatefulHAConfig):
            Optional. Configuration for the StatefulHA
            add-on.
        ray_operator_config (google.cloud.container_v1.types.RayOperatorConfig):
            Optional. Configuration for Ray Operator
            addon.
    """

    http_load_balancing: "HttpLoadBalancing" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="HttpLoadBalancing",
    )
    horizontal_pod_autoscaling: "HorizontalPodAutoscaling" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="HorizontalPodAutoscaling",
    )
    kubernetes_dashboard: "KubernetesDashboard" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="KubernetesDashboard",
    )
    network_policy_config: "NetworkPolicyConfig" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="NetworkPolicyConfig",
    )
    cloud_run_config: "CloudRunConfig" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="CloudRunConfig",
    )
    dns_cache_config: "DnsCacheConfig" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="DnsCacheConfig",
    )
    config_connector_config: "ConfigConnectorConfig" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="ConfigConnectorConfig",
    )
    gce_persistent_disk_csi_driver_config: "GcePersistentDiskCsiDriverConfig" = (
        proto.Field(
            proto.MESSAGE,
            number=11,
            message="GcePersistentDiskCsiDriverConfig",
        )
    )
    gcp_filestore_csi_driver_config: "GcpFilestoreCsiDriverConfig" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="GcpFilestoreCsiDriverConfig",
    )
    gke_backup_agent_config: "GkeBackupAgentConfig" = proto.Field(
        proto.MESSAGE,
        number=16,
        message="GkeBackupAgentConfig",
    )
    gcs_fuse_csi_driver_config: "GcsFuseCsiDriverConfig" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="GcsFuseCsiDriverConfig",
    )
    stateful_ha_config: "StatefulHAConfig" = proto.Field(
        proto.MESSAGE,
        number=18,
        message="StatefulHAConfig",
    )
    ray_operator_config: "RayOperatorConfig" = proto.Field(
        proto.MESSAGE,
        number=21,
        message="RayOperatorConfig",
    )


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

    disabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class HorizontalPodAutoscaling(proto.Message):
    r"""Configuration options for the horizontal pod autoscaling
    feature, which increases or decreases the number of replica pods
    a replication controller has based on the resource usage of the
    existing pods.

    Attributes:
        disabled (bool):
            Whether the Horizontal Pod Autoscaling
            feature is enabled in the cluster. When enabled,
            it ensures that metrics are collected into
            Stackdriver Monitoring.
    """

    disabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class KubernetesDashboard(proto.Message):
    r"""Configuration for the Kubernetes Dashboard.

    Attributes:
        disabled (bool):
            Whether the Kubernetes Dashboard is enabled
            for this cluster.
    """

    disabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class NetworkPolicyConfig(proto.Message):
    r"""Configuration for NetworkPolicy. This only tracks whether the
    addon is enabled or not on the Master, it does not track whether
    network policy is enabled for the nodes.

    Attributes:
        disabled (bool):
            Whether NetworkPolicy is enabled for this
            cluster.
    """

    disabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class DnsCacheConfig(proto.Message):
    r"""Configuration for NodeLocal DNSCache

    Attributes:
        enabled (bool):
            Whether NodeLocal DNSCache is enabled for
            this cluster.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class PrivateClusterMasterGlobalAccessConfig(proto.Message):
    r"""Configuration for controlling master global access settings.

    Attributes:
        enabled (bool):
            Whenever master is accessible globally or
            not.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


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
        peering_name (str):
            Output only. The peering name in the customer
            VPC used by this cluster.
        master_global_access_config (google.cloud.container_v1.types.PrivateClusterMasterGlobalAccessConfig):
            Controls master global access settings.
        private_endpoint_subnetwork (str):
            Subnet to provision the master's private endpoint during
            cluster creation. Specified in
            projects/\ */regions/*/subnetworks/\* format.
    """

    enable_private_nodes: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    enable_private_endpoint: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    master_ipv4_cidr_block: str = proto.Field(
        proto.STRING,
        number=3,
    )
    private_endpoint: str = proto.Field(
        proto.STRING,
        number=4,
    )
    public_endpoint: str = proto.Field(
        proto.STRING,
        number=5,
    )
    peering_name: str = proto.Field(
        proto.STRING,
        number=7,
    )
    master_global_access_config: "PrivateClusterMasterGlobalAccessConfig" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="PrivateClusterMasterGlobalAccessConfig",
    )
    private_endpoint_subnetwork: str = proto.Field(
        proto.STRING,
        number=10,
    )


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

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    security_group: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CloudRunConfig(proto.Message):
    r"""Configuration options for the Cloud Run feature.

    Attributes:
        disabled (bool):
            Whether Cloud Run addon is enabled for this
            cluster.
        load_balancer_type (google.cloud.container_v1.types.CloudRunConfig.LoadBalancerType):
            Which load balancer type is installed for
            Cloud Run.
    """

    class LoadBalancerType(proto.Enum):
        r"""Load balancer type of ingress service of Cloud Run.

        Values:
            LOAD_BALANCER_TYPE_UNSPECIFIED (0):
                Load balancer type for Cloud Run is
                unspecified.
            LOAD_BALANCER_TYPE_EXTERNAL (1):
                Install external load balancer for Cloud Run.
            LOAD_BALANCER_TYPE_INTERNAL (2):
                Install internal load balancer for Cloud Run.
        """
        LOAD_BALANCER_TYPE_UNSPECIFIED = 0
        LOAD_BALANCER_TYPE_EXTERNAL = 1
        LOAD_BALANCER_TYPE_INTERNAL = 2

    disabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    load_balancer_type: LoadBalancerType = proto.Field(
        proto.ENUM,
        number=3,
        enum=LoadBalancerType,
    )


class ConfigConnectorConfig(proto.Message):
    r"""Configuration options for the Config Connector add-on.

    Attributes:
        enabled (bool):
            Whether Cloud Connector is enabled for this
            cluster.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class GcePersistentDiskCsiDriverConfig(proto.Message):
    r"""Configuration for the Compute Engine PD CSI driver.

    Attributes:
        enabled (bool):
            Whether the Compute Engine PD CSI driver is
            enabled for this cluster.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class GcpFilestoreCsiDriverConfig(proto.Message):
    r"""Configuration for the GCP Filestore CSI driver.

    Attributes:
        enabled (bool):
            Whether the GCP Filestore CSI driver is
            enabled for this cluster.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class GcsFuseCsiDriverConfig(proto.Message):
    r"""Configuration for the Cloud Storage Fuse CSI driver.

    Attributes:
        enabled (bool):
            Whether the Cloud Storage Fuse CSI driver is
            enabled for this cluster.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class RayOperatorConfig(proto.Message):
    r"""Configuration options for the Ray Operator add-on.

    Attributes:
        enabled (bool):
            Whether the Ray Operator addon is enabled for
            this cluster.
        ray_cluster_logging_config (google.cloud.container_v1.types.RayClusterLoggingConfig):
            Optional. Logging configuration for Ray
            clusters.
        ray_cluster_monitoring_config (google.cloud.container_v1.types.RayClusterMonitoringConfig):
            Optional. Monitoring configuration for Ray
            clusters.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    ray_cluster_logging_config: "RayClusterLoggingConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="RayClusterLoggingConfig",
    )
    ray_cluster_monitoring_config: "RayClusterMonitoringConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="RayClusterMonitoringConfig",
    )


class GkeBackupAgentConfig(proto.Message):
    r"""Configuration for the Backup for GKE Agent.

    Attributes:
        enabled (bool):
            Whether the Backup for GKE agent is enabled
            for this cluster.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class StatefulHAConfig(proto.Message):
    r"""Configuration for the Stateful HA add-on.

    Attributes:
        enabled (bool):
            Whether the Stateful HA add-on is enabled for
            this cluster.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class MasterAuthorizedNetworksConfig(proto.Message):
    r"""Configuration options for the master authorized networks
    feature. Enabled master authorized networks will disallow all
    external traffic to access Kubernetes master through HTTPS
    except traffic from the given CIDR blocks, Google Compute Engine
    Public IPs and Google Prod IPs.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        enabled (bool):
            Whether or not master authorized networks is
            enabled.
        cidr_blocks (MutableSequence[google.cloud.container_v1.types.MasterAuthorizedNetworksConfig.CidrBlock]):
            cidr_blocks define up to 50 external networks that could
            access Kubernetes master through HTTPS.
        gcp_public_cidrs_access_enabled (bool):
            Whether master is accessbile via Google
            Compute Engine Public IP addresses.

            This field is a member of `oneof`_ ``_gcp_public_cidrs_access_enabled``.
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

        display_name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        cidr_block: str = proto.Field(
            proto.STRING,
            number=2,
        )

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    cidr_blocks: MutableSequence[CidrBlock] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=CidrBlock,
    )
    gcp_public_cidrs_access_enabled: bool = proto.Field(
        proto.BOOL,
        number=3,
        optional=True,
    )


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

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class NetworkPolicy(proto.Message):
    r"""Configuration options for the NetworkPolicy feature.
    https://kubernetes.io/docs/concepts/services-networking/networkpolicies/

    Attributes:
        provider (google.cloud.container_v1.types.NetworkPolicy.Provider):
            The selected network policy provider.
        enabled (bool):
            Whether network policy is enabled on the
            cluster.
    """

    class Provider(proto.Enum):
        r"""Allowed Network Policy providers.

        Values:
            PROVIDER_UNSPECIFIED (0):
                Not set
            CALICO (1):
                Tigera (Calico Felix).
        """
        PROVIDER_UNSPECIFIED = 0
        CALICO = 1

    provider: Provider = proto.Field(
        proto.ENUM,
        number=1,
        enum=Provider,
    )
    enabled: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class BinaryAuthorization(proto.Message):
    r"""Configuration for Binary Authorization.

    Attributes:
        enabled (bool):
            This field is deprecated. Leave this unset and instead
            configure BinaryAuthorization using evaluation_mode. If
            evaluation_mode is set to anything other than
            EVALUATION_MODE_UNSPECIFIED, this field is ignored.
        evaluation_mode (google.cloud.container_v1.types.BinaryAuthorization.EvaluationMode):
            Mode of operation for binauthz policy
            evaluation. If unspecified, defaults to
            DISABLED.
    """

    class EvaluationMode(proto.Enum):
        r"""Binary Authorization mode of operation.

        Values:
            EVALUATION_MODE_UNSPECIFIED (0):
                Default value
            DISABLED (1):
                Disable BinaryAuthorization
            PROJECT_SINGLETON_POLICY_ENFORCE (2):
                Enforce Kubernetes admission requests with
                BinaryAuthorization using the project's
                singleton policy. This is equivalent to setting
                the enabled boolean to true.
        """
        EVALUATION_MODE_UNSPECIFIED = 0
        DISABLED = 1
        PROJECT_SINGLETON_POLICY_ENFORCE = 2

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    evaluation_mode: EvaluationMode = proto.Field(
        proto.ENUM,
        number=2,
        enum=EvaluationMode,
    )


class PodCIDROverprovisionConfig(proto.Message):
    r"""[PRIVATE FIELD] Config for pod CIDR size overprovisioning.

    Attributes:
        disable (bool):
            Whether Pod CIDR overprovisioning is
            disabled. Note: Pod CIDR overprovisioning is
            enabled by default.
    """

    disable: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class IPAllocationPolicy(proto.Message):
    r"""Configuration for controlling how IPs are allocated in the
    cluster.

    Attributes:
        use_ip_aliases (bool):
            Whether alias IPs will be used for pod IPs in the cluster.
            This is used in conjunction with use_routes. It cannot be
            true if use_routes is true. If both use_ip_aliases and
            use_routes are false, then the server picks the default IP
            allocation mode
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

            This field is only applicable with use_ip_aliases is true
            and create_subnetwork is false.
        services_secondary_range_name (str):
            The name of the secondary range to be used as for the
            services CIDR block. The secondary range will be used for
            service ClusterIPs. This must be an existing secondary range
            associated with the cluster subnetwork.

            This field is only applicable with use_ip_aliases is true
            and create_subnetwork is false.
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
        use_routes (bool):
            Whether routes will be used for pod IPs in the cluster. This
            is used in conjunction with use_ip_aliases. It cannot be
            true if use_ip_aliases is true. If both use_ip_aliases and
            use_routes are false, then the server picks the default IP
            allocation mode
        stack_type (google.cloud.container_v1.types.StackType):
            The IP stack type of the cluster
        ipv6_access_type (google.cloud.container_v1.types.IPv6AccessType):
            The ipv6 access type (internal or external) when
            create_subnetwork is true
        pod_cidr_overprovision_config (google.cloud.container_v1.types.PodCIDROverprovisionConfig):
            [PRIVATE FIELD] Pod CIDR size overprovisioning config for
            the cluster.

            Pod CIDR size per node depends on max_pods_per_node. By
            default, the value of max_pods_per_node is doubled and then
            rounded off to next power of 2 to get the size of pod CIDR
            block per node. Example: max_pods_per_node of 30 would
            result in 64 IPs (/26).

            This config can disable the doubling of IPs (we still round
            off to next power of 2) Example: max_pods_per_node of 30
            will result in 32 IPs (/27) when overprovisioning is
            disabled.
        subnet_ipv6_cidr_block (str):
            Output only. The subnet's IPv6 CIDR block
            used by nodes and pods.
        services_ipv6_cidr_block (str):
            Output only. The services IPv6 CIDR block for
            the cluster.
        additional_pod_ranges_config (google.cloud.container_v1.types.AdditionalPodRangesConfig):
            Output only. The additional pod ranges that
            are added to the cluster. These pod ranges can
            be used by new node pools to allocate pod IPs
            automatically. Once the range is removed it will
            not show up in IPAllocationPolicy.
        default_pod_ipv4_range_utilization (float):
            Output only. The utilization of the cluster default IPv4
            range for the pod. The ratio is Usage/[Total number of IPs
            in the secondary range],
            Usage=numNodes\ *numZones*\ podIPsPerNode.
    """

    use_ip_aliases: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    create_subnetwork: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    subnetwork_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    cluster_ipv4_cidr: str = proto.Field(
        proto.STRING,
        number=4,
    )
    node_ipv4_cidr: str = proto.Field(
        proto.STRING,
        number=5,
    )
    services_ipv4_cidr: str = proto.Field(
        proto.STRING,
        number=6,
    )
    cluster_secondary_range_name: str = proto.Field(
        proto.STRING,
        number=7,
    )
    services_secondary_range_name: str = proto.Field(
        proto.STRING,
        number=8,
    )
    cluster_ipv4_cidr_block: str = proto.Field(
        proto.STRING,
        number=9,
    )
    node_ipv4_cidr_block: str = proto.Field(
        proto.STRING,
        number=10,
    )
    services_ipv4_cidr_block: str = proto.Field(
        proto.STRING,
        number=11,
    )
    tpu_ipv4_cidr_block: str = proto.Field(
        proto.STRING,
        number=13,
    )
    use_routes: bool = proto.Field(
        proto.BOOL,
        number=15,
    )
    stack_type: "StackType" = proto.Field(
        proto.ENUM,
        number=16,
        enum="StackType",
    )
    ipv6_access_type: "IPv6AccessType" = proto.Field(
        proto.ENUM,
        number=17,
        enum="IPv6AccessType",
    )
    pod_cidr_overprovision_config: "PodCIDROverprovisionConfig" = proto.Field(
        proto.MESSAGE,
        number=21,
        message="PodCIDROverprovisionConfig",
    )
    subnet_ipv6_cidr_block: str = proto.Field(
        proto.STRING,
        number=22,
    )
    services_ipv6_cidr_block: str = proto.Field(
        proto.STRING,
        number=23,
    )
    additional_pod_ranges_config: "AdditionalPodRangesConfig" = proto.Field(
        proto.MESSAGE,
        number=24,
        message="AdditionalPodRangesConfig",
    )
    default_pod_ipv4_range_utilization: float = proto.Field(
        proto.DOUBLE,
        number=25,
    )


class Cluster(proto.Message):
    r"""A Google Kubernetes Engine cluster.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

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
        node_config (google.cloud.container_v1.types.NodeConfig):
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
        master_auth (google.cloud.container_v1.types.MasterAuth):
            The authentication information for accessing the master
            endpoint. If unspecified, the defaults are used: For
            clusters before v1.12, if master_auth is unspecified,
            ``username`` will be set to "admin", a random password will
            be generated, and a client certificate will be issued.
        logging_service (str):
            The logging service the cluster should use to write logs.
            Currently available options:

            -  ``logging.googleapis.com/kubernetes`` - The Cloud Logging
               service with a Kubernetes-native resource model
            -  ``logging.googleapis.com`` - The legacy Cloud Logging
               service (no longer available as of GKE 1.15).
            -  ``none`` - no logs will be exported from the cluster.

            If left as an empty
            string,\ ``logging.googleapis.com/kubernetes`` will be used
            for GKE 1.14+ or ``logging.googleapis.com`` for earlier
            versions.
        monitoring_service (str):
            The monitoring service the cluster should use to write
            metrics. Currently available options:

            -  "monitoring.googleapis.com/kubernetes" - The Cloud
               Monitoring service with a Kubernetes-native resource
               model
            -  ``monitoring.googleapis.com`` - The legacy Cloud
               Monitoring service (no longer available as of GKE 1.15).
            -  ``none`` - No metrics will be exported from the cluster.

            If left as an empty
            string,\ ``monitoring.googleapis.com/kubernetes`` will be
            used for GKE 1.14+ or ``monitoring.googleapis.com`` for
            earlier versions.
        network (str):
            The name of the Google Compute Engine
            `network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`__
            to which the cluster is connected. If left unspecified, the
            ``default`` network will be used.
        cluster_ipv4_cidr (str):
            The IP address range of the container pods in this cluster,
            in
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``10.96.0.0/14``). Leave blank to have one
            automatically chosen or specify a ``/14`` block in
            ``10.0.0.0/8``.
        addons_config (google.cloud.container_v1.types.AddonsConfig):
            Configurations for the various addons
            available to run in the cluster.
        subnetwork (str):
            The name of the Google Compute Engine
            `subnetwork <https://cloud.google.com/compute/docs/subnetworks>`__
            to which the cluster is connected.
        node_pools (MutableSequence[google.cloud.container_v1.types.NodePool]):
            The node pools associated with this cluster. This field
            should not be set if "node_config" or "initial_node_count"
            are specified.
        locations (MutableSequence[str]):
            The list of Google Compute Engine
            `zones <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster's nodes should be located.

            This field provides a default value if
            `NodePool.Locations <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.FIELDS.locations>`__
            are not specified during node pool creation.

            Warning: changing cluster locations will update the
            `NodePool.Locations <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.FIELDS.locations>`__
            of all node pools and will result in nodes being added
            and/or removed.
        enable_kubernetes_alpha (bool):
            Kubernetes alpha features are enabled on this
            cluster. This includes alpha API groups (e.g.
            v1alpha1) and features that may not be
            production ready in the kubernetes version of
            the master and nodes. The cluster has no SLA for
            uptime and master/node upgrades are disabled.
            Alpha enabled clusters are automatically deleted
            thirty days after creation.
        resource_labels (MutableMapping[str, str]):
            The resource labels for the cluster to use to
            annotate any related Google Compute Engine
            resources.
        label_fingerprint (str):
            The fingerprint of the set of labels for this
            cluster.
        legacy_abac (google.cloud.container_v1.types.LegacyAbac):
            Configuration for the legacy ABAC
            authorization mode.
        network_policy (google.cloud.container_v1.types.NetworkPolicy):
            Configuration options for the NetworkPolicy
            feature.
        ip_allocation_policy (google.cloud.container_v1.types.IPAllocationPolicy):
            Configuration for cluster IP allocation.
        master_authorized_networks_config (google.cloud.container_v1.types.MasterAuthorizedNetworksConfig):
            The configuration options for master
            authorized networks feature.
        maintenance_policy (google.cloud.container_v1.types.MaintenancePolicy):
            Configure the maintenance policy for this
            cluster.
        binary_authorization (google.cloud.container_v1.types.BinaryAuthorization):
            Configuration for Binary Authorization.
        autoscaling (google.cloud.container_v1.types.ClusterAutoscaling):
            Cluster-level autoscaling configuration.
        network_config (google.cloud.container_v1.types.NetworkConfig):
            Configuration for cluster networking.
        default_max_pods_constraint (google.cloud.container_v1.types.MaxPodsConstraint):
            The default constraint on the maximum number
            of pods that can be run simultaneously on a node
            in the node pool of this cluster. Only honored
            if cluster created with IP Alias support.
        resource_usage_export_config (google.cloud.container_v1.types.ResourceUsageExportConfig):
            Configuration for exporting resource usages.
            Resource usage export is disabled when this
            config is unspecified.
        authenticator_groups_config (google.cloud.container_v1.types.AuthenticatorGroupsConfig):
            Configuration controlling RBAC group
            membership information.
        private_cluster_config (google.cloud.container_v1.types.PrivateClusterConfig):
            Configuration for private cluster.
        database_encryption (google.cloud.container_v1.types.DatabaseEncryption):
            Configuration of etcd encryption.
        vertical_pod_autoscaling (google.cloud.container_v1.types.VerticalPodAutoscaling):
            Cluster-level Vertical Pod Autoscaling
            configuration.
        shielded_nodes (google.cloud.container_v1.types.ShieldedNodes):
            Shielded Nodes configuration.
        release_channel (google.cloud.container_v1.types.ReleaseChannel):
            Release channel configuration. If left
            unspecified on cluster creation and a version is
            specified, the cluster is enrolled in the most
            mature release channel where the version is
            available (first checking STABLE, then REGULAR,
            and finally RAPID). Otherwise, if no release
            channel configuration and no version is
            specified, the cluster is enrolled in the
            REGULAR channel with its default version.
        workload_identity_config (google.cloud.container_v1.types.WorkloadIdentityConfig):
            Configuration for the use of Kubernetes
            Service Accounts in GCP IAM policies.
        mesh_certificates (google.cloud.container_v1.types.MeshCertificates):
            Configuration for issuance of mTLS keys and
            certificates to Kubernetes pods.
        cost_management_config (google.cloud.container_v1.types.CostManagementConfig):
            Configuration for the fine-grained cost
            management feature.
        notification_config (google.cloud.container_v1.types.NotificationConfig):
            Notification configuration of the cluster.
        confidential_nodes (google.cloud.container_v1.types.ConfidentialNodes):
            Configuration of Confidential Nodes.
            All the nodes in the cluster will be
            Confidential VM once enabled.
        identity_service_config (google.cloud.container_v1.types.IdentityServiceConfig):
            Configuration for Identity Service component.
        self_link (str):
            Output only. Server-defined URL for the
            resource.
        zone (str):
            Output only. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field is deprecated, use
            location instead.
        endpoint (str):
            Output only. The IP address of this cluster's master
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
              version
            - "1.X": picks the highest valid patch+gke.N
              patch in the 1.X version
            - "1.X.Y": picks the highest valid gke.N patch
              in the 1.X.Y version
            - "1.X.Y-gke.N": picks an explicit Kubernetes
              version
            - "","-": picks the default Kubernetes version
        current_master_version (str):
            Output only. The current software version of
            the master endpoint.
        current_node_version (str):
            Output only. Deprecated, use
            `NodePools.version <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools>`__
            instead. The current version of the node software
            components. If they are currently at multiple versions
            because they're in the process of being upgraded, this
            reflects the minimum version of all nodes.
        create_time (str):
            Output only. The time the cluster was created, in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        status (google.cloud.container_v1.types.Cluster.Status):
            Output only. The current status of this
            cluster.
        status_message (str):
            Output only. Deprecated. Use conditions
            instead. Additional information about the
            current status of this cluster, if available.
        node_ipv4_cidr_size (int):
            Output only. The size of the address space on each node for
            hosting containers. This is provisioned from within the
            ``container_ipv4_cidr`` range. This field will only be set
            when cluster is in route-based network mode.
        services_ipv4_cidr (str):
            Output only. The IP address range of the Kubernetes services
            in this cluster, in
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``1.2.3.4/29``). Service addresses are
            typically put in the last ``/16`` from the container CIDR.
        instance_group_urls (MutableSequence[str]):
            Output only. Deprecated. Use node_pools.instance_group_urls.
        current_node_count (int):
            Output only. The number of nodes currently in
            the cluster. Deprecated. Call Kubernetes API
            directly to retrieve node information.
        expire_time (str):
            Output only. The time the cluster will be automatically
            deleted in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        location (str):
            Output only. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`__
            or
            `region <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`__
            in which the cluster resides.
        enable_tpu (bool):
            Enable the ability to use Cloud TPUs in this
            cluster.
        tpu_ipv4_cidr_block (str):
            Output only. The IP address range of the Cloud TPUs in this
            cluster, in
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``1.2.3.4/29``).
        conditions (MutableSequence[google.cloud.container_v1.types.StatusCondition]):
            Which conditions caused the current cluster
            state.
        autopilot (google.cloud.container_v1.types.Autopilot):
            Autopilot configuration for the cluster.
        id (str):
            Output only. Unique id for the cluster.
        node_pool_defaults (google.cloud.container_v1.types.NodePoolDefaults):
            Default NodePool settings for the entire
            cluster. These settings are overridden if
            specified on the specific NodePool object.

            This field is a member of `oneof`_ ``_node_pool_defaults``.
        logging_config (google.cloud.container_v1.types.LoggingConfig):
            Logging configuration for the cluster.
        monitoring_config (google.cloud.container_v1.types.MonitoringConfig):
            Monitoring configuration for the cluster.
        node_pool_auto_config (google.cloud.container_v1.types.NodePoolAutoConfig):
            Node pool configs that apply to all
            auto-provisioned node pools in autopilot
            clusters and node auto-provisioning enabled
            clusters.
        etag (str):
            This checksum is computed by the server based
            on the value of cluster fields, and may be sent
            on update requests to ensure the client has an
            up-to-date value before proceeding.
        fleet (google.cloud.container_v1.types.Fleet):
            Fleet information for the cluster.
        security_posture_config (google.cloud.container_v1.types.SecurityPostureConfig):
            Enable/Disable Security Posture API features
            for the cluster.
        enable_k8s_beta_apis (google.cloud.container_v1.types.K8sBetaAPIConfig):
            Beta APIs Config
        enterprise_config (google.cloud.container_v1.types.EnterpriseConfig):
            GKE Enterprise Configuration.
        satisfies_pzs (bool):
            Output only. Reserved for future use.

            This field is a member of `oneof`_ ``_satisfies_pzs``.
        satisfies_pzi (bool):
            Output only. Reserved for future use.

            This field is a member of `oneof`_ ``_satisfies_pzi``.
    """

    class Status(proto.Enum):
        r"""The current status of the cluster.

        Values:
            STATUS_UNSPECIFIED (0):
                Not set.
            PROVISIONING (1):
                The PROVISIONING state indicates the cluster
                is being created.
            RUNNING (2):
                The RUNNING state indicates the cluster has
                been created and is fully usable.
            RECONCILING (3):
                The RECONCILING state indicates that some work is actively
                being done on the cluster, such as upgrading the master or
                node software. Details can be found in the ``statusMessage``
                field.
            STOPPING (4):
                The STOPPING state indicates the cluster is
                being deleted.
            ERROR (5):
                The ERROR state indicates the cluster is unusable. It will
                be automatically deleted. Details can be found in the
                ``statusMessage`` field.
            DEGRADED (6):
                The DEGRADED state indicates the cluster requires user
                action to restore full functionality. Details can be found
                in the ``statusMessage`` field.
        """
        STATUS_UNSPECIFIED = 0
        PROVISIONING = 1
        RUNNING = 2
        RECONCILING = 3
        STOPPING = 4
        ERROR = 5
        DEGRADED = 6

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    initial_node_count: int = proto.Field(
        proto.INT32,
        number=3,
    )
    node_config: "NodeConfig" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="NodeConfig",
    )
    master_auth: "MasterAuth" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="MasterAuth",
    )
    logging_service: str = proto.Field(
        proto.STRING,
        number=6,
    )
    monitoring_service: str = proto.Field(
        proto.STRING,
        number=7,
    )
    network: str = proto.Field(
        proto.STRING,
        number=8,
    )
    cluster_ipv4_cidr: str = proto.Field(
        proto.STRING,
        number=9,
    )
    addons_config: "AddonsConfig" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="AddonsConfig",
    )
    subnetwork: str = proto.Field(
        proto.STRING,
        number=11,
    )
    node_pools: MutableSequence["NodePool"] = proto.RepeatedField(
        proto.MESSAGE,
        number=12,
        message="NodePool",
    )
    locations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=13,
    )
    enable_kubernetes_alpha: bool = proto.Field(
        proto.BOOL,
        number=14,
    )
    resource_labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=15,
    )
    label_fingerprint: str = proto.Field(
        proto.STRING,
        number=16,
    )
    legacy_abac: "LegacyAbac" = proto.Field(
        proto.MESSAGE,
        number=18,
        message="LegacyAbac",
    )
    network_policy: "NetworkPolicy" = proto.Field(
        proto.MESSAGE,
        number=19,
        message="NetworkPolicy",
    )
    ip_allocation_policy: "IPAllocationPolicy" = proto.Field(
        proto.MESSAGE,
        number=20,
        message="IPAllocationPolicy",
    )
    master_authorized_networks_config: "MasterAuthorizedNetworksConfig" = proto.Field(
        proto.MESSAGE,
        number=22,
        message="MasterAuthorizedNetworksConfig",
    )
    maintenance_policy: "MaintenancePolicy" = proto.Field(
        proto.MESSAGE,
        number=23,
        message="MaintenancePolicy",
    )
    binary_authorization: "BinaryAuthorization" = proto.Field(
        proto.MESSAGE,
        number=24,
        message="BinaryAuthorization",
    )
    autoscaling: "ClusterAutoscaling" = proto.Field(
        proto.MESSAGE,
        number=26,
        message="ClusterAutoscaling",
    )
    network_config: "NetworkConfig" = proto.Field(
        proto.MESSAGE,
        number=27,
        message="NetworkConfig",
    )
    default_max_pods_constraint: "MaxPodsConstraint" = proto.Field(
        proto.MESSAGE,
        number=30,
        message="MaxPodsConstraint",
    )
    resource_usage_export_config: "ResourceUsageExportConfig" = proto.Field(
        proto.MESSAGE,
        number=33,
        message="ResourceUsageExportConfig",
    )
    authenticator_groups_config: "AuthenticatorGroupsConfig" = proto.Field(
        proto.MESSAGE,
        number=34,
        message="AuthenticatorGroupsConfig",
    )
    private_cluster_config: "PrivateClusterConfig" = proto.Field(
        proto.MESSAGE,
        number=37,
        message="PrivateClusterConfig",
    )
    database_encryption: "DatabaseEncryption" = proto.Field(
        proto.MESSAGE,
        number=38,
        message="DatabaseEncryption",
    )
    vertical_pod_autoscaling: "VerticalPodAutoscaling" = proto.Field(
        proto.MESSAGE,
        number=39,
        message="VerticalPodAutoscaling",
    )
    shielded_nodes: "ShieldedNodes" = proto.Field(
        proto.MESSAGE,
        number=40,
        message="ShieldedNodes",
    )
    release_channel: "ReleaseChannel" = proto.Field(
        proto.MESSAGE,
        number=41,
        message="ReleaseChannel",
    )
    workload_identity_config: "WorkloadIdentityConfig" = proto.Field(
        proto.MESSAGE,
        number=43,
        message="WorkloadIdentityConfig",
    )
    mesh_certificates: "MeshCertificates" = proto.Field(
        proto.MESSAGE,
        number=67,
        message="MeshCertificates",
    )
    cost_management_config: "CostManagementConfig" = proto.Field(
        proto.MESSAGE,
        number=45,
        message="CostManagementConfig",
    )
    notification_config: "NotificationConfig" = proto.Field(
        proto.MESSAGE,
        number=49,
        message="NotificationConfig",
    )
    confidential_nodes: "ConfidentialNodes" = proto.Field(
        proto.MESSAGE,
        number=50,
        message="ConfidentialNodes",
    )
    identity_service_config: "IdentityServiceConfig" = proto.Field(
        proto.MESSAGE,
        number=54,
        message="IdentityServiceConfig",
    )
    self_link: str = proto.Field(
        proto.STRING,
        number=100,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=101,
    )
    endpoint: str = proto.Field(
        proto.STRING,
        number=102,
    )
    initial_cluster_version: str = proto.Field(
        proto.STRING,
        number=103,
    )
    current_master_version: str = proto.Field(
        proto.STRING,
        number=104,
    )
    current_node_version: str = proto.Field(
        proto.STRING,
        number=105,
    )
    create_time: str = proto.Field(
        proto.STRING,
        number=106,
    )
    status: Status = proto.Field(
        proto.ENUM,
        number=107,
        enum=Status,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=108,
    )
    node_ipv4_cidr_size: int = proto.Field(
        proto.INT32,
        number=109,
    )
    services_ipv4_cidr: str = proto.Field(
        proto.STRING,
        number=110,
    )
    instance_group_urls: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=111,
    )
    current_node_count: int = proto.Field(
        proto.INT32,
        number=112,
    )
    expire_time: str = proto.Field(
        proto.STRING,
        number=113,
    )
    location: str = proto.Field(
        proto.STRING,
        number=114,
    )
    enable_tpu: bool = proto.Field(
        proto.BOOL,
        number=115,
    )
    tpu_ipv4_cidr_block: str = proto.Field(
        proto.STRING,
        number=116,
    )
    conditions: MutableSequence["StatusCondition"] = proto.RepeatedField(
        proto.MESSAGE,
        number=118,
        message="StatusCondition",
    )
    autopilot: "Autopilot" = proto.Field(
        proto.MESSAGE,
        number=128,
        message="Autopilot",
    )
    id: str = proto.Field(
        proto.STRING,
        number=129,
    )
    node_pool_defaults: "NodePoolDefaults" = proto.Field(
        proto.MESSAGE,
        number=131,
        optional=True,
        message="NodePoolDefaults",
    )
    logging_config: "LoggingConfig" = proto.Field(
        proto.MESSAGE,
        number=132,
        message="LoggingConfig",
    )
    monitoring_config: "MonitoringConfig" = proto.Field(
        proto.MESSAGE,
        number=133,
        message="MonitoringConfig",
    )
    node_pool_auto_config: "NodePoolAutoConfig" = proto.Field(
        proto.MESSAGE,
        number=136,
        message="NodePoolAutoConfig",
    )
    etag: str = proto.Field(
        proto.STRING,
        number=139,
    )
    fleet: "Fleet" = proto.Field(
        proto.MESSAGE,
        number=140,
        message="Fleet",
    )
    security_posture_config: "SecurityPostureConfig" = proto.Field(
        proto.MESSAGE,
        number=145,
        message="SecurityPostureConfig",
    )
    enable_k8s_beta_apis: "K8sBetaAPIConfig" = proto.Field(
        proto.MESSAGE,
        number=143,
        message="K8sBetaAPIConfig",
    )
    enterprise_config: "EnterpriseConfig" = proto.Field(
        proto.MESSAGE,
        number=149,
        message="EnterpriseConfig",
    )
    satisfies_pzs: bool = proto.Field(
        proto.BOOL,
        number=152,
        optional=True,
    )
    satisfies_pzi: bool = proto.Field(
        proto.BOOL,
        number=153,
        optional=True,
    )


class K8sBetaAPIConfig(proto.Message):
    r"""K8sBetaAPIConfig , configuration for beta APIs

    Attributes:
        enabled_apis (MutableSequence[str]):
            Enabled k8s beta APIs.
    """

    enabled_apis: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class SecurityPostureConfig(proto.Message):
    r"""SecurityPostureConfig defines the flags needed to
    enable/disable features for the Security Posture API.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        mode (google.cloud.container_v1.types.SecurityPostureConfig.Mode):
            Sets which mode to use for Security Posture
            features.

            This field is a member of `oneof`_ ``_mode``.
        vulnerability_mode (google.cloud.container_v1.types.SecurityPostureConfig.VulnerabilityMode):
            Sets which mode to use for vulnerability
            scanning.

            This field is a member of `oneof`_ ``_vulnerability_mode``.
    """

    class Mode(proto.Enum):
        r"""Mode defines enablement mode for GKE Security posture
        features.

        Values:
            MODE_UNSPECIFIED (0):
                Default value not specified.
            DISABLED (1):
                Disables Security Posture features on the
                cluster.
            BASIC (2):
                Applies Security Posture features on the
                cluster.
            ENTERPRISE (3):
                Applies the Security Posture off cluster
                Enterprise level features.
        """
        MODE_UNSPECIFIED = 0
        DISABLED = 1
        BASIC = 2
        ENTERPRISE = 3

    class VulnerabilityMode(proto.Enum):
        r"""VulnerabilityMode defines enablement mode for vulnerability
        scanning.

        Values:
            VULNERABILITY_MODE_UNSPECIFIED (0):
                Default value not specified.
            VULNERABILITY_DISABLED (1):
                Disables vulnerability scanning on the
                cluster.
            VULNERABILITY_BASIC (2):
                Applies basic vulnerability scanning on the
                cluster.
            VULNERABILITY_ENTERPRISE (3):
                Applies the Security Posture's vulnerability
                on cluster Enterprise level features.
        """
        VULNERABILITY_MODE_UNSPECIFIED = 0
        VULNERABILITY_DISABLED = 1
        VULNERABILITY_BASIC = 2
        VULNERABILITY_ENTERPRISE = 3

    mode: Mode = proto.Field(
        proto.ENUM,
        number=1,
        optional=True,
        enum=Mode,
    )
    vulnerability_mode: VulnerabilityMode = proto.Field(
        proto.ENUM,
        number=2,
        optional=True,
        enum=VulnerabilityMode,
    )


class NodePoolAutoConfig(proto.Message):
    r"""Node pool configs that apply to all auto-provisioned node
    pools in autopilot clusters and node auto-provisioning enabled
    clusters.

    Attributes:
        network_tags (google.cloud.container_v1.types.NetworkTags):
            The list of instance tags applied to all
            nodes. Tags are used to identify valid sources
            or targets for network firewalls and are
            specified by the client during cluster creation.
            Each tag within the list must comply with
            RFC1035.
        resource_manager_tags (google.cloud.container_v1.types.ResourceManagerTags):
            Resource manager tag keys and values to be
            attached to the nodes for managing Compute
            Engine firewalls using Network Firewall
            Policies.
        node_kubelet_config (google.cloud.container_v1.types.NodeKubeletConfig):
            NodeKubeletConfig controls the defaults for autoprovisioned
            node-pools.

            Currently only ``insecure_kubelet_readonly_port_enabled``
            can be set here.
    """

    network_tags: "NetworkTags" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="NetworkTags",
    )
    resource_manager_tags: "ResourceManagerTags" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ResourceManagerTags",
    )
    node_kubelet_config: "NodeKubeletConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="NodeKubeletConfig",
    )


class NodePoolDefaults(proto.Message):
    r"""Subset of Nodepool message that has defaults.

    Attributes:
        node_config_defaults (google.cloud.container_v1.types.NodeConfigDefaults):
            Subset of NodeConfig message that has
            defaults.
    """

    node_config_defaults: "NodeConfigDefaults" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="NodeConfigDefaults",
    )


class NodeConfigDefaults(proto.Message):
    r"""Subset of NodeConfig message that has defaults.

    Attributes:
        gcfs_config (google.cloud.container_v1.types.GcfsConfig):
            GCFS (Google Container File System, also
            known as Riptide) options.
        logging_config (google.cloud.container_v1.types.NodePoolLoggingConfig):
            Logging configuration for node pools.
        containerd_config (google.cloud.container_v1.types.ContainerdConfig):
            Parameters for containerd customization.
        node_kubelet_config (google.cloud.container_v1.types.NodeKubeletConfig):
            NodeKubeletConfig controls the defaults for new node-pools.

            Currently only ``insecure_kubelet_readonly_port_enabled``
            can be set here.
    """

    gcfs_config: "GcfsConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="GcfsConfig",
    )
    logging_config: "NodePoolLoggingConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="NodePoolLoggingConfig",
    )
    containerd_config: "ContainerdConfig" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="ContainerdConfig",
    )
    node_kubelet_config: "NodeKubeletConfig" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="NodeKubeletConfig",
    )


class ClusterUpdate(proto.Message):
    r"""ClusterUpdate describes an update to the cluster. Exactly one
    update can be applied to a cluster with each request, so at most
    one field can be provided.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        desired_node_version (str):
            The Kubernetes version to change the nodes to
            (typically an upgrade).

            Users may specify either explicit versions
            offered by Kubernetes Engine or version aliases,
            which have the following behavior:

            - "latest": picks the highest valid Kubernetes
              version
            - "1.X": picks the highest valid patch+gke.N
              patch in the 1.X version
            - "1.X.Y": picks the highest valid gke.N patch
              in the 1.X.Y version
            - "1.X.Y-gke.N": picks an explicit Kubernetes
              version
            - "-": picks the Kubernetes master version
        desired_monitoring_service (str):
            The monitoring service the cluster should use to write
            metrics. Currently available options:

            -  "monitoring.googleapis.com/kubernetes" - The Cloud
               Monitoring service with a Kubernetes-native resource
               model
            -  ``monitoring.googleapis.com`` - The legacy Cloud
               Monitoring service (no longer available as of GKE 1.15).
            -  ``none`` - No metrics will be exported from the cluster.

            If left as an empty
            string,\ ``monitoring.googleapis.com/kubernetes`` will be
            used for GKE 1.14+ or ``monitoring.googleapis.com`` for
            earlier versions.
        desired_addons_config (google.cloud.container_v1.types.AddonsConfig):
            Configurations for the various addons
            available to run in the cluster.
        desired_node_pool_id (str):
            The node pool to be upgraded. This field is mandatory if
            "desired_node_version", "desired_image_family" or
            "desired_node_pool_autoscaling" is specified and there is
            more than one node pool on the cluster.
        desired_image_type (str):
            The desired image type for the node pool. NOTE: Set the
            "desired_node_pool" field as well.
        desired_database_encryption (google.cloud.container_v1.types.DatabaseEncryption):
            Configuration of etcd encryption.
        desired_workload_identity_config (google.cloud.container_v1.types.WorkloadIdentityConfig):
            Configuration for Workload Identity.
        desired_mesh_certificates (google.cloud.container_v1.types.MeshCertificates):
            Configuration for issuance of mTLS keys and
            certificates to Kubernetes pods.
        desired_shielded_nodes (google.cloud.container_v1.types.ShieldedNodes):
            Configuration for Shielded Nodes.
        desired_cost_management_config (google.cloud.container_v1.types.CostManagementConfig):
            The desired configuration for the
            fine-grained cost management feature.
        desired_dns_config (google.cloud.container_v1.types.DNSConfig):
            DNSConfig contains clusterDNS config for this
            cluster.
        desired_node_pool_autoscaling (google.cloud.container_v1.types.NodePoolAutoscaling):
            Autoscaler configuration for the node pool specified in
            desired_node_pool_id. If there is only one pool in the
            cluster and desired_node_pool_id is not provided then the
            change applies to that single node pool.
        desired_locations (MutableSequence[str]):
            The desired list of Google Compute Engine
            `zones <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster's nodes should be located.

            This list must always include the cluster's primary zone.

            Warning: changing cluster locations will update the
            locations of all node pools and will result in nodes being
            added and/or removed.
        desired_master_authorized_networks_config (google.cloud.container_v1.types.MasterAuthorizedNetworksConfig):
            The desired configuration options for master
            authorized networks feature.
        desired_cluster_autoscaling (google.cloud.container_v1.types.ClusterAutoscaling):
            Cluster-level autoscaling configuration.
        desired_binary_authorization (google.cloud.container_v1.types.BinaryAuthorization):
            The desired configuration options for the
            Binary Authorization feature.
        desired_logging_service (str):
            The logging service the cluster should use to write logs.
            Currently available options:

            -  ``logging.googleapis.com/kubernetes`` - The Cloud Logging
               service with a Kubernetes-native resource model
            -  ``logging.googleapis.com`` - The legacy Cloud Logging
               service (no longer available as of GKE 1.15).
            -  ``none`` - no logs will be exported from the cluster.

            If left as an empty
            string,\ ``logging.googleapis.com/kubernetes`` will be used
            for GKE 1.14+ or ``logging.googleapis.com`` for earlier
            versions.
        desired_resource_usage_export_config (google.cloud.container_v1.types.ResourceUsageExportConfig):
            The desired configuration for exporting
            resource usage.
        desired_vertical_pod_autoscaling (google.cloud.container_v1.types.VerticalPodAutoscaling):
            Cluster-level Vertical Pod Autoscaling
            configuration.
        desired_private_cluster_config (google.cloud.container_v1.types.PrivateClusterConfig):
            The desired private cluster configuration.
            master_global_access_config is the only field that can be
            changed via this field. See also
            [ClusterUpdate.desired_enable_private_endpoint][google.container.v1.ClusterUpdate.desired_enable_private_endpoint]
            for modifying other fields within
            [PrivateClusterConfig][google.container.v1.PrivateClusterConfig].
        desired_intra_node_visibility_config (google.cloud.container_v1.types.IntraNodeVisibilityConfig):
            The desired config of Intra-node visibility.
        desired_default_snat_status (google.cloud.container_v1.types.DefaultSnatStatus):
            The desired status of whether to disable
            default sNAT for this cluster.
        desired_release_channel (google.cloud.container_v1.types.ReleaseChannel):
            The desired release channel configuration.
        desired_l4ilb_subsetting_config (google.cloud.container_v1.types.ILBSubsettingConfig):
            The desired L4 Internal Load Balancer
            Subsetting configuration.
        desired_datapath_provider (google.cloud.container_v1.types.DatapathProvider):
            The desired datapath provider for the
            cluster.
        desired_private_ipv6_google_access (google.cloud.container_v1.types.PrivateIPv6GoogleAccess):
            The desired state of IPv6 connectivity to
            Google Services.
        desired_notification_config (google.cloud.container_v1.types.NotificationConfig):
            The desired notification configuration.
        desired_authenticator_groups_config (google.cloud.container_v1.types.AuthenticatorGroupsConfig):
            The desired authenticator groups config for
            the cluster.
        desired_logging_config (google.cloud.container_v1.types.LoggingConfig):
            The desired logging configuration.
        desired_monitoring_config (google.cloud.container_v1.types.MonitoringConfig):
            The desired monitoring configuration.
        desired_identity_service_config (google.cloud.container_v1.types.IdentityServiceConfig):
            The desired Identity Service component
            configuration.
        desired_service_external_ips_config (google.cloud.container_v1.types.ServiceExternalIPsConfig):
            ServiceExternalIPsConfig specifies the config
            for the use of Services with ExternalIPs field.
        desired_enable_private_endpoint (bool):
            Enable/Disable private endpoint for the
            cluster's master.

            This field is a member of `oneof`_ ``_desired_enable_private_endpoint``.
        desired_master_version (str):
            The Kubernetes version to change the master
            to.
            Users may specify either explicit versions
            offered by Kubernetes Engine or version aliases,
            which have the following behavior:

            - "latest": picks the highest valid Kubernetes
              version
            - "1.X": picks the highest valid patch+gke.N
              patch in the 1.X version
            - "1.X.Y": picks the highest valid gke.N patch
              in the 1.X.Y version
            - "1.X.Y-gke.N": picks an explicit Kubernetes
              version
            - "-": picks the default Kubernetes version
        desired_gcfs_config (google.cloud.container_v1.types.GcfsConfig):
            The desired GCFS config for the cluster
        desired_node_pool_auto_config_network_tags (google.cloud.container_v1.types.NetworkTags):
            The desired network tags that apply to all
            auto-provisioned node pools in autopilot
            clusters and node auto-provisioning enabled
            clusters.
        desired_gateway_api_config (google.cloud.container_v1.types.GatewayAPIConfig):
            The desired config of Gateway API on this
            cluster.
        etag (str):
            The current etag of the cluster.
            If an etag is provided and does not match the
            current etag of the cluster, update will be
            blocked and an ABORTED error will be returned.
        desired_node_pool_logging_config (google.cloud.container_v1.types.NodePoolLoggingConfig):
            The desired node pool logging configuration
            defaults for the cluster.
        desired_fleet (google.cloud.container_v1.types.Fleet):
            The desired fleet configuration for the
            cluster.
        desired_stack_type (google.cloud.container_v1.types.StackType):
            The desired stack type of the cluster.
            If a stack type is provided and does not match
            the current stack type of the cluster, update
            will attempt to change the stack type to the new
            type.
        additional_pod_ranges_config (google.cloud.container_v1.types.AdditionalPodRangesConfig):
            The additional pod ranges to be added to the
            cluster. These pod ranges can be used by node
            pools to allocate pod IPs.
        removed_additional_pod_ranges_config (google.cloud.container_v1.types.AdditionalPodRangesConfig):
            The additional pod ranges that are to be removed from the
            cluster. The pod ranges specified here must have been
            specified earlier in the 'additional_pod_ranges_config'
            argument.
        enable_k8s_beta_apis (google.cloud.container_v1.types.K8sBetaAPIConfig):
            Kubernetes open source beta apis enabled on
            the cluster. Only beta apis
        desired_security_posture_config (google.cloud.container_v1.types.SecurityPostureConfig):
            Enable/Disable Security Posture API features
            for the cluster.
        desired_network_performance_config (google.cloud.container_v1.types.NetworkConfig.ClusterNetworkPerformanceConfig):
            The desired network performance config.
        desired_enable_fqdn_network_policy (bool):
            Enable/Disable FQDN Network Policy for the
            cluster.

            This field is a member of `oneof`_ ``_desired_enable_fqdn_network_policy``.
        desired_autopilot_workload_policy_config (google.cloud.container_v1.types.WorkloadPolicyConfig):
            The desired workload policy configuration for
            the autopilot cluster.
        desired_k8s_beta_apis (google.cloud.container_v1.types.K8sBetaAPIConfig):
            Desired Beta APIs to be enabled for cluster.
        desired_containerd_config (google.cloud.container_v1.types.ContainerdConfig):
            The desired containerd config for the
            cluster.
        desired_enable_multi_networking (bool):
            Enable/Disable Multi-Networking for the
            cluster

            This field is a member of `oneof`_ ``_desired_enable_multi_networking``.
        desired_node_pool_auto_config_resource_manager_tags (google.cloud.container_v1.types.ResourceManagerTags):
            The desired resource manager tags that apply
            to all auto-provisioned node pools in autopilot
            clusters and node auto-provisioning enabled
            clusters.
        desired_in_transit_encryption_config (google.cloud.container_v1.types.InTransitEncryptionConfig):
            Specify the details of in-transit encryption.

            This field is a member of `oneof`_ ``_desired_in_transit_encryption_config``.
        desired_enable_cilium_clusterwide_network_policy (bool):
            Enable/Disable Cilium Clusterwide Network
            Policy for the cluster.

            This field is a member of `oneof`_ ``_desired_enable_cilium_clusterwide_network_policy``.
        desired_node_kubelet_config (google.cloud.container_v1.types.NodeKubeletConfig):
            The desired node kubelet config for the
            cluster.
        desired_node_pool_auto_config_kubelet_config (google.cloud.container_v1.types.NodeKubeletConfig):
            The desired node kubelet config for all
            auto-provisioned node pools in autopilot
            clusters and node auto-provisioning enabled
            clusters.
    """

    desired_node_version: str = proto.Field(
        proto.STRING,
        number=4,
    )
    desired_monitoring_service: str = proto.Field(
        proto.STRING,
        number=5,
    )
    desired_addons_config: "AddonsConfig" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="AddonsConfig",
    )
    desired_node_pool_id: str = proto.Field(
        proto.STRING,
        number=7,
    )
    desired_image_type: str = proto.Field(
        proto.STRING,
        number=8,
    )
    desired_database_encryption: "DatabaseEncryption" = proto.Field(
        proto.MESSAGE,
        number=46,
        message="DatabaseEncryption",
    )
    desired_workload_identity_config: "WorkloadIdentityConfig" = proto.Field(
        proto.MESSAGE,
        number=47,
        message="WorkloadIdentityConfig",
    )
    desired_mesh_certificates: "MeshCertificates" = proto.Field(
        proto.MESSAGE,
        number=67,
        message="MeshCertificates",
    )
    desired_shielded_nodes: "ShieldedNodes" = proto.Field(
        proto.MESSAGE,
        number=48,
        message="ShieldedNodes",
    )
    desired_cost_management_config: "CostManagementConfig" = proto.Field(
        proto.MESSAGE,
        number=49,
        message="CostManagementConfig",
    )
    desired_dns_config: "DNSConfig" = proto.Field(
        proto.MESSAGE,
        number=53,
        message="DNSConfig",
    )
    desired_node_pool_autoscaling: "NodePoolAutoscaling" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="NodePoolAutoscaling",
    )
    desired_locations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=10,
    )
    desired_master_authorized_networks_config: "MasterAuthorizedNetworksConfig" = (
        proto.Field(
            proto.MESSAGE,
            number=12,
            message="MasterAuthorizedNetworksConfig",
        )
    )
    desired_cluster_autoscaling: "ClusterAutoscaling" = proto.Field(
        proto.MESSAGE,
        number=15,
        message="ClusterAutoscaling",
    )
    desired_binary_authorization: "BinaryAuthorization" = proto.Field(
        proto.MESSAGE,
        number=16,
        message="BinaryAuthorization",
    )
    desired_logging_service: str = proto.Field(
        proto.STRING,
        number=19,
    )
    desired_resource_usage_export_config: "ResourceUsageExportConfig" = proto.Field(
        proto.MESSAGE,
        number=21,
        message="ResourceUsageExportConfig",
    )
    desired_vertical_pod_autoscaling: "VerticalPodAutoscaling" = proto.Field(
        proto.MESSAGE,
        number=22,
        message="VerticalPodAutoscaling",
    )
    desired_private_cluster_config: "PrivateClusterConfig" = proto.Field(
        proto.MESSAGE,
        number=25,
        message="PrivateClusterConfig",
    )
    desired_intra_node_visibility_config: "IntraNodeVisibilityConfig" = proto.Field(
        proto.MESSAGE,
        number=26,
        message="IntraNodeVisibilityConfig",
    )
    desired_default_snat_status: "DefaultSnatStatus" = proto.Field(
        proto.MESSAGE,
        number=28,
        message="DefaultSnatStatus",
    )
    desired_release_channel: "ReleaseChannel" = proto.Field(
        proto.MESSAGE,
        number=31,
        message="ReleaseChannel",
    )
    desired_l4ilb_subsetting_config: "ILBSubsettingConfig" = proto.Field(
        proto.MESSAGE,
        number=39,
        message="ILBSubsettingConfig",
    )
    desired_datapath_provider: "DatapathProvider" = proto.Field(
        proto.ENUM,
        number=50,
        enum="DatapathProvider",
    )
    desired_private_ipv6_google_access: "PrivateIPv6GoogleAccess" = proto.Field(
        proto.ENUM,
        number=51,
        enum="PrivateIPv6GoogleAccess",
    )
    desired_notification_config: "NotificationConfig" = proto.Field(
        proto.MESSAGE,
        number=55,
        message="NotificationConfig",
    )
    desired_authenticator_groups_config: "AuthenticatorGroupsConfig" = proto.Field(
        proto.MESSAGE,
        number=63,
        message="AuthenticatorGroupsConfig",
    )
    desired_logging_config: "LoggingConfig" = proto.Field(
        proto.MESSAGE,
        number=64,
        message="LoggingConfig",
    )
    desired_monitoring_config: "MonitoringConfig" = proto.Field(
        proto.MESSAGE,
        number=65,
        message="MonitoringConfig",
    )
    desired_identity_service_config: "IdentityServiceConfig" = proto.Field(
        proto.MESSAGE,
        number=66,
        message="IdentityServiceConfig",
    )
    desired_service_external_ips_config: "ServiceExternalIPsConfig" = proto.Field(
        proto.MESSAGE,
        number=60,
        message="ServiceExternalIPsConfig",
    )
    desired_enable_private_endpoint: bool = proto.Field(
        proto.BOOL,
        number=71,
        optional=True,
    )
    desired_master_version: str = proto.Field(
        proto.STRING,
        number=100,
    )
    desired_gcfs_config: "GcfsConfig" = proto.Field(
        proto.MESSAGE,
        number=109,
        message="GcfsConfig",
    )
    desired_node_pool_auto_config_network_tags: "NetworkTags" = proto.Field(
        proto.MESSAGE,
        number=110,
        message="NetworkTags",
    )
    desired_gateway_api_config: "GatewayAPIConfig" = proto.Field(
        proto.MESSAGE,
        number=114,
        message="GatewayAPIConfig",
    )
    etag: str = proto.Field(
        proto.STRING,
        number=115,
    )
    desired_node_pool_logging_config: "NodePoolLoggingConfig" = proto.Field(
        proto.MESSAGE,
        number=116,
        message="NodePoolLoggingConfig",
    )
    desired_fleet: "Fleet" = proto.Field(
        proto.MESSAGE,
        number=117,
        message="Fleet",
    )
    desired_stack_type: "StackType" = proto.Field(
        proto.ENUM,
        number=119,
        enum="StackType",
    )
    additional_pod_ranges_config: "AdditionalPodRangesConfig" = proto.Field(
        proto.MESSAGE,
        number=120,
        message="AdditionalPodRangesConfig",
    )
    removed_additional_pod_ranges_config: "AdditionalPodRangesConfig" = proto.Field(
        proto.MESSAGE,
        number=121,
        message="AdditionalPodRangesConfig",
    )
    enable_k8s_beta_apis: "K8sBetaAPIConfig" = proto.Field(
        proto.MESSAGE,
        number=122,
        message="K8sBetaAPIConfig",
    )
    desired_security_posture_config: "SecurityPostureConfig" = proto.Field(
        proto.MESSAGE,
        number=124,
        message="SecurityPostureConfig",
    )
    desired_network_performance_config: "NetworkConfig.ClusterNetworkPerformanceConfig" = proto.Field(
        proto.MESSAGE,
        number=125,
        message="NetworkConfig.ClusterNetworkPerformanceConfig",
    )
    desired_enable_fqdn_network_policy: bool = proto.Field(
        proto.BOOL,
        number=126,
        optional=True,
    )
    desired_autopilot_workload_policy_config: "WorkloadPolicyConfig" = proto.Field(
        proto.MESSAGE,
        number=128,
        message="WorkloadPolicyConfig",
    )
    desired_k8s_beta_apis: "K8sBetaAPIConfig" = proto.Field(
        proto.MESSAGE,
        number=131,
        message="K8sBetaAPIConfig",
    )
    desired_containerd_config: "ContainerdConfig" = proto.Field(
        proto.MESSAGE,
        number=134,
        message="ContainerdConfig",
    )
    desired_enable_multi_networking: bool = proto.Field(
        proto.BOOL,
        number=135,
        optional=True,
    )
    desired_node_pool_auto_config_resource_manager_tags: "ResourceManagerTags" = (
        proto.Field(
            proto.MESSAGE,
            number=136,
            message="ResourceManagerTags",
        )
    )
    desired_in_transit_encryption_config: "InTransitEncryptionConfig" = proto.Field(
        proto.ENUM,
        number=137,
        optional=True,
        enum="InTransitEncryptionConfig",
    )
    desired_enable_cilium_clusterwide_network_policy: bool = proto.Field(
        proto.BOOL,
        number=138,
        optional=True,
    )
    desired_node_kubelet_config: "NodeKubeletConfig" = proto.Field(
        proto.MESSAGE,
        number=141,
        message="NodeKubeletConfig",
    )
    desired_node_pool_auto_config_kubelet_config: "NodeKubeletConfig" = proto.Field(
        proto.MESSAGE,
        number=142,
        message="NodeKubeletConfig",
    )


class AdditionalPodRangesConfig(proto.Message):
    r"""AdditionalPodRangesConfig is the configuration for additional
    pod secondary ranges supporting the ClusterUpdate message.

    Attributes:
        pod_range_names (MutableSequence[str]):
            Name for pod secondary ipv4 range which has
            the actual range defined ahead.
        pod_range_info (MutableSequence[google.cloud.container_v1.types.RangeInfo]):
            Output only. Information for additional pod
            range.
    """

    pod_range_names: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    pod_range_info: MutableSequence["RangeInfo"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="RangeInfo",
    )


class RangeInfo(proto.Message):
    r"""RangeInfo contains the range name and the range utilization
    by this cluster.

    Attributes:
        range_name (str):
            Output only. Name of a range.
        utilization (float):
            Output only. The utilization of the range.
    """

    range_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    utilization: float = proto.Field(
        proto.DOUBLE,
        number=2,
    )


class Operation(proto.Message):
    r"""This operation resource represents operations that may have
    happened or are happening on the cluster. All fields are output
    only.

    Attributes:
        name (str):
            Output only. The server-assigned ID for the
            operation.
        zone (str):
            Output only. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the operation is taking place. This field is
            deprecated, use location instead.
        operation_type (google.cloud.container_v1.types.Operation.Type):
            Output only. The operation type.
        status (google.cloud.container_v1.types.Operation.Status):
            Output only. The current status of the
            operation.
        detail (str):
            Output only. Detailed operation progress, if
            available.
        status_message (str):
            Output only. If an error has occurred, a
            textual description of the error. Deprecated.
            Use the field error instead.
        self_link (str):
            Output only. Server-defined URI for the operation. Example:
            ``https://container.googleapis.com/v1alpha1/projects/123/locations/us-central1/operations/operation-123``.
        target_link (str):
            Output only. Server-defined URI for the target of the
            operation. The format of this is a URI to the resource being
            modified (such as a cluster, node pool, or node). For node
            pool repairs, there may be multiple nodes being repaired,
            but only one will be the target.

            Examples:

            -

            ``https://container.googleapis.com/v1/projects/123/locations/us-central1/clusters/my-cluster``

            ``https://container.googleapis.com/v1/projects/123/zones/us-central1-c/clusters/my-cluster/nodePools/my-np``

            ``https://container.googleapis.com/v1/projects/123/zones/us-central1-c/clusters/my-cluster/nodePools/my-np/node/my-node``
        location (str):
            Output only. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`__
            or
            `region <https://cloud.google.com/compute/docs/regions-zones/regions-zones#available>`__
            in which the cluster resides.
        start_time (str):
            Output only. The time the operation started, in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        end_time (str):
            Output only. The time the operation completed, in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        progress (google.cloud.container_v1.types.OperationProgress):
            Output only. Progress information for an
            operation.
        cluster_conditions (MutableSequence[google.cloud.container_v1.types.StatusCondition]):
            Which conditions caused the current cluster
            state. Deprecated. Use field error instead.
        nodepool_conditions (MutableSequence[google.cloud.container_v1.types.StatusCondition]):
            Which conditions caused the current node pool
            state. Deprecated. Use field error instead.
        error (google.rpc.status_pb2.Status):
            The error result of the operation in case of
            failure.
    """

    class Status(proto.Enum):
        r"""Current status of the operation.

        Values:
            STATUS_UNSPECIFIED (0):
                Not set.
            PENDING (1):
                The operation has been created.
            RUNNING (2):
                The operation is currently running.
            DONE (3):
                The operation is done, either cancelled or
                completed.
            ABORTING (4):
                The operation is aborting.
        """
        STATUS_UNSPECIFIED = 0
        PENDING = 1
        RUNNING = 2
        DONE = 3
        ABORTING = 4

    class Type(proto.Enum):
        r"""Operation type categorizes the operation.

        Values:
            TYPE_UNSPECIFIED (0):
                Not set.
            CREATE_CLUSTER (1):
                The cluster is being created. The cluster should be assumed
                to be unusable until the operation finishes.

                In the event of the operation failing, the cluster will
                enter the [ERROR state][Cluster.Status.ERROR] and eventually
                be deleted.
            DELETE_CLUSTER (2):
                The cluster is being deleted. The cluster should be assumed
                to be unusable as soon as this operation starts.

                In the event of the operation failing, the cluster will
                enter the [ERROR state][Cluster.Status.ERROR] and the
                deletion will be automatically retried until completed.
            UPGRADE_MASTER (3):
                The [cluster
                version][google.container.v1.ClusterUpdate.desired_master_version]
                is being updated. Note that this includes "upgrades" to the
                same version, which are simply a recreation. This also
                includes
                `auto-upgrades <https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-upgrades#upgrading_automatically>`__.
                For more details, see `documentation on cluster
                upgrades <https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-upgrades#cluster_upgrades>`__.
            UPGRADE_NODES (4):
                A node pool is being updated. Despite calling this an
                "upgrade", this includes most forms of updates to node
                pools. This also includes
                `auto-upgrades <https://cloud.google.com/kubernetes-engine/docs/how-to/node-auto-upgrades>`__.

                This operation sets the
                [progress][google.container.v1.Operation.progress] field and
                may be
                [canceled][google.container.v1.ClusterManager.CancelOperation].

                The upgrade strategy depends on `node pool
                configuration <https://cloud.google.com/kubernetes-engine/docs/concepts/node-pool-upgrade-strategies>`__.
                The nodes are generally still usable during this operation.
            REPAIR_CLUSTER (5):
                A problem has been detected with the control plane and is
                being repaired. This operation type is initiated by GKE. For
                more details, see `documentation on
                repairs <https://cloud.google.com/kubernetes-engine/docs/concepts/maintenance-windows-and-exclusions#repairs>`__.
            UPDATE_CLUSTER (6):
                The cluster is being updated. This is a broad category of
                operations and includes operations that only change metadata
                as well as those that must recreate the entire cluster. If
                the control plane must be recreated, this will cause
                temporary downtime for zonal clusters.

                Some features require recreating the nodes as well. Those
                will be recreated as separate operations and the update may
                not be completely functional until the node pools
                recreations finish. Node recreations will generally follow
                `maintenance
                policies <https://cloud.google.com/kubernetes-engine/docs/concepts/maintenance-windows-and-exclusions>`__.

                Some GKE-initiated operations use this type. This includes
                certain types of auto-upgrades and incident mitigations.
            CREATE_NODE_POOL (7):
                A node pool is being created. The node pool should be
                assumed to be unusable until this operation finishes. In the
                event of an error, the node pool may be partially created.

                If enabled, `node
                autoprovisioning <https://cloud.google.com/kubernetes-engine/docs/how-to/node-auto-provisioning>`__
                may have automatically initiated such operations.
            DELETE_NODE_POOL (8):
                The node pool is being deleted. The node pool
                should be assumed to be unusable as soon as this
                operation starts.
            SET_NODE_POOL_MANAGEMENT (9):
                The node pool's
                [manamagent][google.container.v1.NodePool.management] field
                is being updated. These operations only update metadata and
                may be concurrent with most other operations.
            AUTO_REPAIR_NODES (10):
                A problem has been detected with nodes and `they are being
                repaired <https://cloud.google.com/kubernetes-engine/docs/how-to/node-auto-repair>`__.
                This operation type is initiated by GKE, typically
                automatically. This operation may be concurrent with other
                operations and there may be multiple repairs occurring on
                the same node pool.
            AUTO_UPGRADE_NODES (11):
                Unused. Automatic node upgrade uses
                [UPGRADE_NODES][google.container.v1.Operation.Type.UPGRADE_NODES].
            SET_LABELS (12):
                Unused. Updating labels uses
                [UPDATE_CLUSTER][google.container.v1.Operation.Type.UPDATE_CLUSTER].
            SET_MASTER_AUTH (13):
                Unused. Updating master auth uses
                [UPDATE_CLUSTER][google.container.v1.Operation.Type.UPDATE_CLUSTER].
            SET_NODE_POOL_SIZE (14):
                The node pool is being resized. With the
                exception of resizing to or from size zero, the
                node pool is generally usable during this
                operation.
            SET_NETWORK_POLICY (15):
                Unused. Updating network policy uses
                [UPDATE_CLUSTER][google.container.v1.Operation.Type.UPDATE_CLUSTER].
            SET_MAINTENANCE_POLICY (16):
                Unused. Updating maintenance policy uses
                [UPDATE_CLUSTER][google.container.v1.Operation.Type.UPDATE_CLUSTER].
            RESIZE_CLUSTER (18):
                The control plane is being resized. This operation type is
                initiated by GKE. These operations are often performed
                preemptively to ensure that the control plane has sufficient
                resources and is not typically an indication of issues. For
                more details, see `documentation on
                resizes <https://cloud.google.com/kubernetes-engine/docs/concepts/maintenance-windows-and-exclusions#repairs>`__.
            FLEET_FEATURE_UPGRADE (19):
                Fleet features of GKE Enterprise are being
                upgraded. The cluster should be assumed to be
                blocked for other upgrades until the operation
                finishes.
        """
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
        RESIZE_CLUSTER = 18
        FLEET_FEATURE_UPGRADE = 19

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    operation_type: Type = proto.Field(
        proto.ENUM,
        number=3,
        enum=Type,
    )
    status: Status = proto.Field(
        proto.ENUM,
        number=4,
        enum=Status,
    )
    detail: str = proto.Field(
        proto.STRING,
        number=8,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    self_link: str = proto.Field(
        proto.STRING,
        number=6,
    )
    target_link: str = proto.Field(
        proto.STRING,
        number=7,
    )
    location: str = proto.Field(
        proto.STRING,
        number=9,
    )
    start_time: str = proto.Field(
        proto.STRING,
        number=10,
    )
    end_time: str = proto.Field(
        proto.STRING,
        number=11,
    )
    progress: "OperationProgress" = proto.Field(
        proto.MESSAGE,
        number=12,
        message="OperationProgress",
    )
    cluster_conditions: MutableSequence["StatusCondition"] = proto.RepeatedField(
        proto.MESSAGE,
        number=13,
        message="StatusCondition",
    )
    nodepool_conditions: MutableSequence["StatusCondition"] = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message="StatusCondition",
    )
    error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=15,
        message=status_pb2.Status,
    )


class OperationProgress(proto.Message):
    r"""Information about operation (or operation stage) progress.

    Attributes:
        name (str):
            A non-parameterized string describing an
            operation stage. Unset for single-stage
            operations.
        status (google.cloud.container_v1.types.Operation.Status):
            Status of an operation stage.
            Unset for single-stage operations.
        metrics (MutableSequence[google.cloud.container_v1.types.OperationProgress.Metric]):
            Progress metric bundle, for example: metrics: [{name: "nodes
            done", int_value: 15}, {name: "nodes total", int_value: 32}]
            or metrics: [{name: "progress", double_value: 0.56}, {name:
            "progress scale", double_value: 1.0}]
        stages (MutableSequence[google.cloud.container_v1.types.OperationProgress]):
            Substages of an operation or a stage.
    """

    class Metric(proto.Message):
        r"""Progress metric is (string, int|float|string) pair.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            name (str):
                Required. Metric name, e.g., "nodes total",
                "percent done".
            int_value (int):
                For metrics with integer value.

                This field is a member of `oneof`_ ``value``.
            double_value (float):
                For metrics with floating point value.

                This field is a member of `oneof`_ ``value``.
            string_value (str):
                For metrics with custom values (ratios,
                visual progress, etc.).

                This field is a member of `oneof`_ ``value``.
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        int_value: int = proto.Field(
            proto.INT64,
            number=2,
            oneof="value",
        )
        double_value: float = proto.Field(
            proto.DOUBLE,
            number=3,
            oneof="value",
        )
        string_value: str = proto.Field(
            proto.STRING,
            number=4,
            oneof="value",
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    status: "Operation.Status" = proto.Field(
        proto.ENUM,
        number=2,
        enum="Operation.Status",
    )
    metrics: MutableSequence[Metric] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=Metric,
    )
    stages: MutableSequence["OperationProgress"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="OperationProgress",
    )


class CreateClusterRequest(proto.Message):
    r"""CreateClusterRequest creates a cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the parent
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the parent field.
        cluster (google.cloud.container_v1.types.Cluster):
            Required. A `cluster
            resource <https://cloud.google.com/container-engine/reference/rest/v1/projects.locations.clusters>`__
        parent (str):
            The parent (project and location) where the cluster will be
            created. Specified in the format ``projects/*/locations/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster: "Cluster" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Cluster",
    )
    parent: str = proto.Field(
        proto.STRING,
        number=5,
    )


class GetClusterRequest(proto.Message):
    r"""GetClusterRequest gets the settings of a cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            retrieve. This field has been deprecated and
            replaced by the name field.
        name (str):
            The name (project, location, cluster) of the cluster to
            retrieve. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    name: str = proto.Field(
        proto.STRING,
        number=5,
    )


class UpdateClusterRequest(proto.Message):
    r"""UpdateClusterRequest updates the settings of a cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            upgrade. This field has been deprecated and
            replaced by the name field.
        update (google.cloud.container_v1.types.ClusterUpdate):
            Required. A description of the update.
        name (str):
            The name (project, location, cluster) of the cluster to
            update. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    update: "ClusterUpdate" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="ClusterUpdate",
    )
    name: str = proto.Field(
        proto.STRING,
        number=5,
    )


class UpdateNodePoolRequest(proto.Message):
    r"""UpdateNodePoolRequests update a node pool's image and/or
    version.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            upgrade. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Deprecated. The name of the node pool to
            upgrade. This field has been deprecated and
            replaced by the name field.
        node_version (str):
            Required. The Kubernetes version to change
            the nodes to (typically an upgrade).

            Users may specify either explicit versions
            offered by Kubernetes Engine or version aliases,
            which have the following behavior:

            - "latest": picks the highest valid Kubernetes
              version
            - "1.X": picks the highest valid patch+gke.N
              patch in the 1.X version
            - "1.X.Y": picks the highest valid gke.N patch
              in the 1.X.Y version
            - "1.X.Y-gke.N": picks an explicit Kubernetes
              version
            - "-": picks the Kubernetes master version
        image_type (str):
            Required. The desired image type for the node
            pool. Please see
            https://cloud.google.com/kubernetes-engine/docs/concepts/node-images
            for available image types.
        name (str):
            The name (project, location, cluster, node pool) of the node
            pool to update. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
        locations (MutableSequence[str]):
            The desired list of Google Compute Engine
            `zones <https://cloud.google.com/compute/docs/zones#available>`__
            in which the node pool's nodes should be located. Changing
            the locations for a node pool will result in nodes being
            either created or removed from the node pool, depending on
            whether locations are being added or removed.
        workload_metadata_config (google.cloud.container_v1.types.WorkloadMetadataConfig):
            The desired workload metadata config for the
            node pool.
        upgrade_settings (google.cloud.container_v1.types.NodePool.UpgradeSettings):
            Upgrade settings control disruption and speed
            of the upgrade.
        tags (google.cloud.container_v1.types.NetworkTags):
            The desired network tags to be applied to all nodes in the
            node pool. If this field is not present, the tags will not
            be changed. Otherwise, the existing network tags will be
            *replaced* with the provided tags.
        taints (google.cloud.container_v1.types.NodeTaints):
            The desired node taints to be applied to all nodes in the
            node pool. If this field is not present, the taints will not
            be changed. Otherwise, the existing node taints will be
            *replaced* with the provided taints.
        labels (google.cloud.container_v1.types.NodeLabels):
            The desired node labels to be applied to all nodes in the
            node pool. If this field is not present, the labels will not
            be changed. Otherwise, the existing node labels will be
            *replaced* with the provided labels.
        linux_node_config (google.cloud.container_v1.types.LinuxNodeConfig):
            Parameters that can be configured on Linux
            nodes.
        kubelet_config (google.cloud.container_v1.types.NodeKubeletConfig):
            Node kubelet configs.
        node_network_config (google.cloud.container_v1.types.NodeNetworkConfig):
            Node network config.
        gcfs_config (google.cloud.container_v1.types.GcfsConfig):
            GCFS config.
        confidential_nodes (google.cloud.container_v1.types.ConfidentialNodes):
            Confidential nodes config.
            All the nodes in the node pool will be
            Confidential VM once enabled.
        gvnic (google.cloud.container_v1.types.VirtualNIC):
            Enable or disable gvnic on the node pool.
        etag (str):
            The current etag of the node pool.
            If an etag is provided and does not match the
            current etag of the node pool, update will be
            blocked and an ABORTED error will be returned.
        fast_socket (google.cloud.container_v1.types.FastSocket):
            Enable or disable NCCL fast socket for the
            node pool.
        logging_config (google.cloud.container_v1.types.NodePoolLoggingConfig):
            Logging configuration.
        resource_labels (google.cloud.container_v1.types.ResourceLabels):
            The resource labels for the node pool to use
            to annotate any related Google Compute Engine
            resources.
        windows_node_config (google.cloud.container_v1.types.WindowsNodeConfig):
            Parameters that can be configured on Windows
            nodes.
        accelerators (MutableSequence[google.cloud.container_v1.types.AcceleratorConfig]):
            A list of hardware accelerators to be
            attached to each node. See
            https://cloud.google.com/compute/docs/gpus for
            more information about support for GPUs.
        machine_type (str):
            Optional. The desired `Google Compute Engine machine
            type <https://cloud.google.com/compute/docs/machine-types>`__
            for nodes in the node pool. Initiates an upgrade operation
            that migrates the nodes in the node pool to the specified
            machine type.
        disk_type (str):
            Optional. The desired disk type (e.g.
            'pd-standard', 'pd-ssd' or 'pd-balanced') for
            nodes in the node pool. Initiates an upgrade
            operation that migrates the nodes in the node
            pool to the specified disk type.
        disk_size_gb (int):
            Optional. The desired disk size for nodes in
            the node pool specified in GB. The smallest
            allowed disk size is 10GB. Initiates an upgrade
            operation that migrates the nodes in the node
            pool to the specified disk size.
        resource_manager_tags (google.cloud.container_v1.types.ResourceManagerTags):
            Desired resource manager tag keys and values
            to be attached to the nodes for managing Compute
            Engine firewalls using Network Firewall
            Policies. Existing tags will be replaced with
            new values.
        containerd_config (google.cloud.container_v1.types.ContainerdConfig):
            The desired containerd config for nodes in
            the node pool. Initiates an upgrade operation
            that recreates the nodes with the new config.
        queued_provisioning (google.cloud.container_v1.types.NodePool.QueuedProvisioning):
            Specifies the configuration of queued
            provisioning.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    node_pool_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    node_version: str = proto.Field(
        proto.STRING,
        number=5,
    )
    image_type: str = proto.Field(
        proto.STRING,
        number=6,
    )
    name: str = proto.Field(
        proto.STRING,
        number=8,
    )
    locations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=13,
    )
    workload_metadata_config: "WorkloadMetadataConfig" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="WorkloadMetadataConfig",
    )
    upgrade_settings: "NodePool.UpgradeSettings" = proto.Field(
        proto.MESSAGE,
        number=15,
        message="NodePool.UpgradeSettings",
    )
    tags: "NetworkTags" = proto.Field(
        proto.MESSAGE,
        number=16,
        message="NetworkTags",
    )
    taints: "NodeTaints" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="NodeTaints",
    )
    labels: "NodeLabels" = proto.Field(
        proto.MESSAGE,
        number=18,
        message="NodeLabels",
    )
    linux_node_config: "LinuxNodeConfig" = proto.Field(
        proto.MESSAGE,
        number=19,
        message="LinuxNodeConfig",
    )
    kubelet_config: "NodeKubeletConfig" = proto.Field(
        proto.MESSAGE,
        number=20,
        message="NodeKubeletConfig",
    )
    node_network_config: "NodeNetworkConfig" = proto.Field(
        proto.MESSAGE,
        number=21,
        message="NodeNetworkConfig",
    )
    gcfs_config: "GcfsConfig" = proto.Field(
        proto.MESSAGE,
        number=22,
        message="GcfsConfig",
    )
    confidential_nodes: "ConfidentialNodes" = proto.Field(
        proto.MESSAGE,
        number=23,
        message="ConfidentialNodes",
    )
    gvnic: "VirtualNIC" = proto.Field(
        proto.MESSAGE,
        number=29,
        message="VirtualNIC",
    )
    etag: str = proto.Field(
        proto.STRING,
        number=30,
    )
    fast_socket: "FastSocket" = proto.Field(
        proto.MESSAGE,
        number=31,
        message="FastSocket",
    )
    logging_config: "NodePoolLoggingConfig" = proto.Field(
        proto.MESSAGE,
        number=32,
        message="NodePoolLoggingConfig",
    )
    resource_labels: "ResourceLabels" = proto.Field(
        proto.MESSAGE,
        number=33,
        message="ResourceLabels",
    )
    windows_node_config: "WindowsNodeConfig" = proto.Field(
        proto.MESSAGE,
        number=34,
        message="WindowsNodeConfig",
    )
    accelerators: MutableSequence["AcceleratorConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=35,
        message="AcceleratorConfig",
    )
    machine_type: str = proto.Field(
        proto.STRING,
        number=36,
    )
    disk_type: str = proto.Field(
        proto.STRING,
        number=37,
    )
    disk_size_gb: int = proto.Field(
        proto.INT64,
        number=38,
    )
    resource_manager_tags: "ResourceManagerTags" = proto.Field(
        proto.MESSAGE,
        number=39,
        message="ResourceManagerTags",
    )
    containerd_config: "ContainerdConfig" = proto.Field(
        proto.MESSAGE,
        number=40,
        message="ContainerdConfig",
    )
    queued_provisioning: "NodePool.QueuedProvisioning" = proto.Field(
        proto.MESSAGE,
        number=42,
        message="NodePool.QueuedProvisioning",
    )


class SetNodePoolAutoscalingRequest(proto.Message):
    r"""SetNodePoolAutoscalingRequest sets the autoscaler settings of
    a node pool.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            upgrade. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Deprecated. The name of the node pool to
            upgrade. This field has been deprecated and
            replaced by the name field.
        autoscaling (google.cloud.container_v1.types.NodePoolAutoscaling):
            Required. Autoscaling configuration for the
            node pool.
        name (str):
            The name (project, location, cluster, node pool) of the node
            pool to set autoscaler settings. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    node_pool_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    autoscaling: "NodePoolAutoscaling" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="NodePoolAutoscaling",
    )
    name: str = proto.Field(
        proto.STRING,
        number=6,
    )


class SetLoggingServiceRequest(proto.Message):
    r"""SetLoggingServiceRequest sets the logging service of a
    cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            upgrade. This field has been deprecated and
            replaced by the name field.
        logging_service (str):
            Required. The logging service the cluster should use to
            write logs. Currently available options:

            -  ``logging.googleapis.com/kubernetes`` - The Cloud Logging
               service with a Kubernetes-native resource model
            -  ``logging.googleapis.com`` - The legacy Cloud Logging
               service (no longer available as of GKE 1.15).
            -  ``none`` - no logs will be exported from the cluster.

            If left as an empty
            string,\ ``logging.googleapis.com/kubernetes`` will be used
            for GKE 1.14+ or ``logging.googleapis.com`` for earlier
            versions.
        name (str):
            The name (project, location, cluster) of the cluster to set
            logging. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    logging_service: str = proto.Field(
        proto.STRING,
        number=4,
    )
    name: str = proto.Field(
        proto.STRING,
        number=5,
    )


class SetMonitoringServiceRequest(proto.Message):
    r"""SetMonitoringServiceRequest sets the monitoring service of a
    cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            upgrade. This field has been deprecated and
            replaced by the name field.
        monitoring_service (str):
            Required. The monitoring service the cluster should use to
            write metrics. Currently available options:

            -  "monitoring.googleapis.com/kubernetes" - The Cloud
               Monitoring service with a Kubernetes-native resource
               model
            -  ``monitoring.googleapis.com`` - The legacy Cloud
               Monitoring service (no longer available as of GKE 1.15).
            -  ``none`` - No metrics will be exported from the cluster.

            If left as an empty
            string,\ ``monitoring.googleapis.com/kubernetes`` will be
            used for GKE 1.14+ or ``monitoring.googleapis.com`` for
            earlier versions.
        name (str):
            The name (project, location, cluster) of the cluster to set
            monitoring. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    monitoring_service: str = proto.Field(
        proto.STRING,
        number=4,
    )
    name: str = proto.Field(
        proto.STRING,
        number=6,
    )


class SetAddonsConfigRequest(proto.Message):
    r"""SetAddonsConfigRequest sets the addons associated with the
    cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            upgrade. This field has been deprecated and
            replaced by the name field.
        addons_config (google.cloud.container_v1.types.AddonsConfig):
            Required. The desired configurations for the
            various addons available to run in the cluster.
        name (str):
            The name (project, location, cluster) of the cluster to set
            addons. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    addons_config: "AddonsConfig" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="AddonsConfig",
    )
    name: str = proto.Field(
        proto.STRING,
        number=6,
    )


class SetLocationsRequest(proto.Message):
    r"""SetLocationsRequest sets the locations of the cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            upgrade. This field has been deprecated and
            replaced by the name field.
        locations (MutableSequence[str]):
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

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    locations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    name: str = proto.Field(
        proto.STRING,
        number=6,
    )


class UpdateMasterRequest(proto.Message):
    r"""UpdateMasterRequest updates the master of the cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            upgrade. This field has been deprecated and
            replaced by the name field.
        master_version (str):
            Required. The Kubernetes version to change
            the master to.
            Users may specify either explicit versions
            offered by Kubernetes Engine or version aliases,
            which have the following behavior:

            - "latest": picks the highest valid Kubernetes
              version
            - "1.X": picks the highest valid patch+gke.N
              patch in the 1.X version
            - "1.X.Y": picks the highest valid gke.N patch
              in the 1.X.Y version
            - "1.X.Y-gke.N": picks an explicit Kubernetes
              version
            - "-": picks the default Kubernetes version
        name (str):
            The name (project, location, cluster) of the cluster to
            update. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    master_version: str = proto.Field(
        proto.STRING,
        number=4,
    )
    name: str = proto.Field(
        proto.STRING,
        number=7,
    )


class SetMasterAuthRequest(proto.Message):
    r"""SetMasterAuthRequest updates the admin password of a cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            upgrade. This field has been deprecated and
            replaced by the name field.
        action (google.cloud.container_v1.types.SetMasterAuthRequest.Action):
            Required. The exact form of action to be
            taken on the master auth.
        update (google.cloud.container_v1.types.MasterAuth):
            Required. A description of the update.
        name (str):
            The name (project, location, cluster) of the cluster to set
            auth. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    class Action(proto.Enum):
        r"""Operation type: what type update to perform.

        Values:
            UNKNOWN (0):
                Operation is unknown and will error out.
            SET_PASSWORD (1):
                Set the password to a user generated value.
            GENERATE_PASSWORD (2):
                Generate a new password and set it to that.
            SET_USERNAME (3):
                Set the username.  If an empty username is
                provided, basic authentication is disabled for
                the cluster.  If a non-empty username is
                provided, basic authentication is enabled, with
                either a provided password or a generated one.
        """
        UNKNOWN = 0
        SET_PASSWORD = 1
        GENERATE_PASSWORD = 2
        SET_USERNAME = 3

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    action: Action = proto.Field(
        proto.ENUM,
        number=4,
        enum=Action,
    )
    update: "MasterAuth" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="MasterAuth",
    )
    name: str = proto.Field(
        proto.STRING,
        number=7,
    )


class DeleteClusterRequest(proto.Message):
    r"""DeleteClusterRequest deletes a cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            delete. This field has been deprecated and
            replaced by the name field.
        name (str):
            The name (project, location, cluster) of the cluster to
            delete. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    name: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListClustersRequest(proto.Message):
    r"""ListClustersRequest lists clusters.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the parent
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides, or "-" for all zones. This
            field has been deprecated and replaced by the parent field.
        parent (str):
            The parent (project and location) where the clusters will be
            listed. Specified in the format ``projects/*/locations/*``.
            Location "-" matches all zones and all regions.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    parent: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListClustersResponse(proto.Message):
    r"""ListClustersResponse is the result of ListClustersRequest.

    Attributes:
        clusters (MutableSequence[google.cloud.container_v1.types.Cluster]):
            A list of clusters in the project in the
            specified zone, or across all ones.
        missing_zones (MutableSequence[str]):
            If any zones are listed here, the list of
            clusters returned may be missing those zones.
    """

    clusters: MutableSequence["Cluster"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Cluster",
    )
    missing_zones: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class GetOperationRequest(proto.Message):
    r"""GetOperationRequest gets a single operation.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        operation_id (str):
            Deprecated. The server-assigned ``name`` of the operation.
            This field has been deprecated and replaced by the name
            field.
        name (str):
            The name (project, location, operation id) of the operation
            to get. Specified in the format
            ``projects/*/locations/*/operations/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    operation_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    name: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListOperationsRequest(proto.Message):
    r"""ListOperationsRequest lists operations.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the parent
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            to return operations for, or ``-`` for all zones. This field
            has been deprecated and replaced by the parent field.
        parent (str):
            The parent (project and location) where the operations will
            be listed. Specified in the format
            ``projects/*/locations/*``. Location "-" matches all zones
            and all regions.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    parent: str = proto.Field(
        proto.STRING,
        number=4,
    )


class CancelOperationRequest(proto.Message):
    r"""CancelOperationRequest cancels a single operation.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the operation resides. This field has been
            deprecated and replaced by the name field.
        operation_id (str):
            Deprecated. The server-assigned ``name`` of the operation.
            This field has been deprecated and replaced by the name
            field.
        name (str):
            The name (project, location, operation id) of the operation
            to cancel. Specified in the format
            ``projects/*/locations/*/operations/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    operation_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    name: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListOperationsResponse(proto.Message):
    r"""ListOperationsResponse is the result of
    ListOperationsRequest.

    Attributes:
        operations (MutableSequence[google.cloud.container_v1.types.Operation]):
            A list of operations in the project in the
            specified zone.
        missing_zones (MutableSequence[str]):
            If any zones are listed here, the list of
            operations returned may be missing the
            operations from those zones.
    """

    operations: MutableSequence["Operation"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Operation",
    )
    missing_zones: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class GetServerConfigRequest(proto.Message):
    r"""Gets the current Kubernetes Engine service configuration.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            to return operations for. This field has been deprecated and
            replaced by the name field.
        name (str):
            The name (project and location) of the server config to get,
            specified in the format ``projects/*/locations/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    name: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ServerConfig(proto.Message):
    r"""Kubernetes Engine service configuration.

    Attributes:
        default_cluster_version (str):
            Version of Kubernetes the service deploys by
            default.
        valid_node_versions (MutableSequence[str]):
            List of valid node upgrade target versions,
            in descending order.
        default_image_type (str):
            Default image type.
        valid_image_types (MutableSequence[str]):
            List of valid image types.
        valid_master_versions (MutableSequence[str]):
            List of valid master versions, in descending
            order.
        channels (MutableSequence[google.cloud.container_v1.types.ServerConfig.ReleaseChannelConfig]):
            List of release channel configurations.
    """

    class ReleaseChannelConfig(proto.Message):
        r"""ReleaseChannelConfig exposes configuration for a release
        channel.

        Attributes:
            channel (google.cloud.container_v1.types.ReleaseChannel.Channel):
                The release channel this configuration
                applies to.
            default_version (str):
                The default version for newly created
                clusters on the channel.
            valid_versions (MutableSequence[str]):
                List of valid versions for the channel.
        """

        channel: "ReleaseChannel.Channel" = proto.Field(
            proto.ENUM,
            number=1,
            enum="ReleaseChannel.Channel",
        )
        default_version: str = proto.Field(
            proto.STRING,
            number=2,
        )
        valid_versions: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=4,
        )

    default_cluster_version: str = proto.Field(
        proto.STRING,
        number=1,
    )
    valid_node_versions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    default_image_type: str = proto.Field(
        proto.STRING,
        number=4,
    )
    valid_image_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    valid_master_versions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    channels: MutableSequence[ReleaseChannelConfig] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message=ReleaseChannelConfig,
    )


class CreateNodePoolRequest(proto.Message):
    r"""CreateNodePoolRequest creates a node pool for a cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the parent
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the parent field.
        cluster_id (str):
            Deprecated. The name of the cluster.
            This field has been deprecated and replaced by
            the parent field.
        node_pool (google.cloud.container_v1.types.NodePool):
            Required. The node pool to create.
        parent (str):
            The parent (project, location, cluster name) where the node
            pool will be created. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    node_pool: "NodePool" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="NodePool",
    )
    parent: str = proto.Field(
        proto.STRING,
        number=6,
    )


class DeleteNodePoolRequest(proto.Message):
    r"""DeleteNodePoolRequest deletes a node pool for a cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster.
            This field has been deprecated and replaced by
            the name field.
        node_pool_id (str):
            Deprecated. The name of the node pool to
            delete. This field has been deprecated and
            replaced by the name field.
        name (str):
            The name (project, location, cluster, node pool id) of the
            node pool to delete. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    node_pool_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    name: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ListNodePoolsRequest(proto.Message):
    r"""ListNodePoolsRequest lists the node pool(s) for a cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the parent
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the parent field.
        cluster_id (str):
            Deprecated. The name of the cluster.
            This field has been deprecated and replaced by
            the parent field.
        parent (str):
            The parent (project, location, cluster name) where the node
            pools will be listed. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    parent: str = proto.Field(
        proto.STRING,
        number=5,
    )


class GetNodePoolRequest(proto.Message):
    r"""GetNodePoolRequest retrieves a node pool for a cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster.
            This field has been deprecated and replaced by
            the name field.
        node_pool_id (str):
            Deprecated. The name of the node pool.
            This field has been deprecated and replaced by
            the name field.
        name (str):
            The name (project, location, cluster, node pool id) of the
            node pool to get. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    node_pool_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    name: str = proto.Field(
        proto.STRING,
        number=6,
    )


class BlueGreenSettings(proto.Message):
    r"""Settings for blue-green upgrade.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        standard_rollout_policy (google.cloud.container_v1.types.BlueGreenSettings.StandardRolloutPolicy):
            Standard policy for the blue-green upgrade.

            This field is a member of `oneof`_ ``rollout_policy``.
        node_pool_soak_duration (google.protobuf.duration_pb2.Duration):
            Time needed after draining entire blue pool.
            After this period, blue pool will be cleaned up.

            This field is a member of `oneof`_ ``_node_pool_soak_duration``.
    """

    class StandardRolloutPolicy(proto.Message):
        r"""Standard rollout policy is the default policy for blue-green.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            batch_percentage (float):
                Percentage of the blue pool nodes to drain in a batch. The
                range of this field should be (0.0, 1.0].

                This field is a member of `oneof`_ ``update_batch_size``.
            batch_node_count (int):
                Number of blue nodes to drain in a batch.

                This field is a member of `oneof`_ ``update_batch_size``.
            batch_soak_duration (google.protobuf.duration_pb2.Duration):
                Soak time after each batch gets drained.
                Default to zero.

                This field is a member of `oneof`_ ``_batch_soak_duration``.
        """

        batch_percentage: float = proto.Field(
            proto.FLOAT,
            number=1,
            oneof="update_batch_size",
        )
        batch_node_count: int = proto.Field(
            proto.INT32,
            number=2,
            oneof="update_batch_size",
        )
        batch_soak_duration: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=3,
            optional=True,
            message=duration_pb2.Duration,
        )

    standard_rollout_policy: StandardRolloutPolicy = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="rollout_policy",
        message=StandardRolloutPolicy,
    )
    node_pool_soak_duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=2,
        optional=True,
        message=duration_pb2.Duration,
    )


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
        config (google.cloud.container_v1.types.NodeConfig):
            The node configuration of the pool.
        initial_node_count (int):
            The initial node count for the pool. You must ensure that
            your Compute Engine `resource
            quota <https://cloud.google.com/compute/quotas>`__ is
            sufficient for this number of instances. You must also have
            available firewall and routes quota.
        locations (MutableSequence[str]):
            The list of Google Compute Engine
            `zones <https://cloud.google.com/compute/docs/zones#available>`__
            in which the NodePool's nodes should be located.

            If this value is unspecified during node pool creation, the
            `Cluster.Locations <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters#Cluster.FIELDS.locations>`__
            value will be used, instead.

            Warning: changing node pool locations will result in nodes
            being added and/or removed.
        network_config (google.cloud.container_v1.types.NodeNetworkConfig):
            Networking configuration for this NodePool.
            If specified, it overrides the cluster-level
            defaults.
        self_link (str):
            Output only. Server-defined URL for the
            resource.
        version (str):
            The version of Kubernetes running on this NodePool's nodes.
            If unspecified, it defaults as described
            `here <https://cloud.google.com/kubernetes-engine/versioning#specifying_node_version>`__.
        instance_group_urls (MutableSequence[str]):
            Output only. The resource URLs of the `managed instance
            groups <https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances>`__
            associated with this node pool. During the node pool
            blue-green upgrade operation, the URLs contain both blue and
            green resources.
        status (google.cloud.container_v1.types.NodePool.Status):
            Output only. The status of the nodes in this
            pool instance.
        status_message (str):
            Output only. Deprecated. Use conditions
            instead. Additional information about the
            current status of this node pool instance, if
            available.
        autoscaling (google.cloud.container_v1.types.NodePoolAutoscaling):
            Autoscaler configuration for this NodePool.
            Autoscaler is enabled only if a valid
            configuration is present.
        management (google.cloud.container_v1.types.NodeManagement):
            NodeManagement configuration for this
            NodePool.
        max_pods_constraint (google.cloud.container_v1.types.MaxPodsConstraint):
            The constraint on the maximum number of pods
            that can be run simultaneously on a node in the
            node pool.
        conditions (MutableSequence[google.cloud.container_v1.types.StatusCondition]):
            Which conditions caused the current node pool
            state.
        pod_ipv4_cidr_size (int):
            Output only. The pod CIDR block size per node
            in this node pool.
        upgrade_settings (google.cloud.container_v1.types.NodePool.UpgradeSettings):
            Upgrade settings control disruption and speed
            of the upgrade.
        placement_policy (google.cloud.container_v1.types.NodePool.PlacementPolicy):
            Specifies the node placement policy.
        update_info (google.cloud.container_v1.types.NodePool.UpdateInfo):
            Output only. Update info contains relevant
            information during a node pool update.
        etag (str):
            This checksum is computed by the server based
            on the value of node pool fields, and may be
            sent on update requests to ensure the client has
            an up-to-date value before proceeding.
        queued_provisioning (google.cloud.container_v1.types.NodePool.QueuedProvisioning):
            Specifies the configuration of queued
            provisioning.
        best_effort_provisioning (google.cloud.container_v1.types.BestEffortProvisioning):
            Enable best effort provisioning for nodes
    """

    class Status(proto.Enum):
        r"""The current status of the node pool instance.

        Values:
            STATUS_UNSPECIFIED (0):
                Not set.
            PROVISIONING (1):
                The PROVISIONING state indicates the node
                pool is being created.
            RUNNING (2):
                The RUNNING state indicates the node pool has
                been created and is fully usable.
            RUNNING_WITH_ERROR (3):
                The RUNNING_WITH_ERROR state indicates the node pool has
                been created and is partially usable. Some error state has
                occurred and some functionality may be impaired. Customer
                may need to reissue a request or trigger a new update.
            RECONCILING (4):
                The RECONCILING state indicates that some work is actively
                being done on the node pool, such as upgrading node
                software. Details can be found in the ``statusMessage``
                field.
            STOPPING (5):
                The STOPPING state indicates the node pool is
                being deleted.
            ERROR (6):
                The ERROR state indicates the node pool may be unusable.
                Details can be found in the ``statusMessage`` field.
        """
        STATUS_UNSPECIFIED = 0
        PROVISIONING = 1
        RUNNING = 2
        RUNNING_WITH_ERROR = 3
        RECONCILING = 4
        STOPPING = 5
        ERROR = 6

    class UpgradeSettings(proto.Message):
        r"""These upgrade settings control the level of parallelism and the
        level of disruption caused by an upgrade.

        maxUnavailable controls the number of nodes that can be
        simultaneously unavailable.

        maxSurge controls the number of additional nodes that can be added
        to the node pool temporarily for the time of the upgrade to increase
        the number of available nodes.

        (maxUnavailable + maxSurge) determines the level of parallelism (how
        many nodes are being upgraded at the same time).

        Note: upgrades inevitably introduce some disruption since workloads
        need to be moved from old nodes to new, upgraded ones. Even if
        maxUnavailable=0, this holds true. (Disruption stays within the
        limits of PodDisruptionBudget, if it is configured.)

        Consider a hypothetical node pool with 5 nodes having maxSurge=2,
        maxUnavailable=1. This means the upgrade process upgrades 3 nodes
        simultaneously. It creates 2 additional (upgraded) nodes, then it
        brings down 3 old (not yet upgraded) nodes at the same time. This
        ensures that there are always at least 4 nodes available.

        These upgrade settings configure the upgrade strategy for the node
        pool. Use strategy to switch between the strategies applied to the
        node pool.

        If the strategy is ROLLING, use max_surge and max_unavailable to
        control the level of parallelism and the level of disruption caused
        by upgrade.

        1. maxSurge controls the number of additional nodes that can be
           added to the node pool temporarily for the time of the upgrade to
           increase the number of available nodes.
        2. maxUnavailable controls the number of nodes that can be
           simultaneously unavailable.
        3. (maxUnavailable + maxSurge) determines the level of parallelism
           (how many nodes are being upgraded at the same time).

        If the strategy is BLUE_GREEN, use blue_green_settings to configure
        the blue-green upgrade related settings.

        1. standard_rollout_policy is the default policy. The policy is used
           to control the way blue pool gets drained. The draining is
           executed in the batch mode. The batch size could be specified as
           either percentage of the node pool size or the number of nodes.
           batch_soak_duration is the soak time after each batch gets
           drained.
        2. node_pool_soak_duration is the soak time after all blue nodes are
           drained. After this period, the blue pool nodes will be deleted.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            max_surge (int):
                The maximum number of nodes that can be
                created beyond the current size of the node pool
                during the upgrade process.
            max_unavailable (int):
                The maximum number of nodes that can be
                simultaneously unavailable during the upgrade
                process. A node is considered available if its
                status is Ready.
            strategy (google.cloud.container_v1.types.NodePoolUpdateStrategy):
                Update strategy of the node pool.

                This field is a member of `oneof`_ ``_strategy``.
            blue_green_settings (google.cloud.container_v1.types.BlueGreenSettings):
                Settings for blue-green upgrade strategy.

                This field is a member of `oneof`_ ``_blue_green_settings``.
        """

        max_surge: int = proto.Field(
            proto.INT32,
            number=1,
        )
        max_unavailable: int = proto.Field(
            proto.INT32,
            number=2,
        )
        strategy: "NodePoolUpdateStrategy" = proto.Field(
            proto.ENUM,
            number=3,
            optional=True,
            enum="NodePoolUpdateStrategy",
        )
        blue_green_settings: "BlueGreenSettings" = proto.Field(
            proto.MESSAGE,
            number=4,
            optional=True,
            message="BlueGreenSettings",
        )

    class UpdateInfo(proto.Message):
        r"""UpdateInfo contains resource (instance groups, etc), status
        and other intermediate information relevant to a node pool
        upgrade.

        Attributes:
            blue_green_info (google.cloud.container_v1.types.NodePool.UpdateInfo.BlueGreenInfo):
                Information of a blue-green upgrade.
        """

        class BlueGreenInfo(proto.Message):
            r"""Information relevant to blue-green upgrade.

            Attributes:
                phase (google.cloud.container_v1.types.NodePool.UpdateInfo.BlueGreenInfo.Phase):
                    Current blue-green upgrade phase.
                blue_instance_group_urls (MutableSequence[str]):
                    The resource URLs of the [managed instance groups]
                    (/compute/docs/instance-groups/creating-groups-of-managed-instances)
                    associated with blue pool.
                green_instance_group_urls (MutableSequence[str]):
                    The resource URLs of the [managed instance groups]
                    (/compute/docs/instance-groups/creating-groups-of-managed-instances)
                    associated with green pool.
                blue_pool_deletion_start_time (str):
                    Time to start deleting blue pool to complete blue-green
                    upgrade, in
                    `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
                    format.
                green_pool_version (str):
                    Version of green pool.
            """

            class Phase(proto.Enum):
                r"""Phase represents the different stages blue-green upgrade is
                running in.

                Values:
                    PHASE_UNSPECIFIED (0):
                        Unspecified phase.
                    UPDATE_STARTED (1):
                        blue-green upgrade has been initiated.
                    CREATING_GREEN_POOL (2):
                        Start creating green pool nodes.
                    CORDONING_BLUE_POOL (3):
                        Start cordoning blue pool nodes.
                    DRAINING_BLUE_POOL (4):
                        Start draining blue pool nodes.
                    NODE_POOL_SOAKING (5):
                        Start soaking time after draining entire blue
                        pool.
                    DELETING_BLUE_POOL (6):
                        Start deleting blue nodes.
                    ROLLBACK_STARTED (7):
                        Rollback has been initiated.
                """
                PHASE_UNSPECIFIED = 0
                UPDATE_STARTED = 1
                CREATING_GREEN_POOL = 2
                CORDONING_BLUE_POOL = 3
                DRAINING_BLUE_POOL = 4
                NODE_POOL_SOAKING = 5
                DELETING_BLUE_POOL = 6
                ROLLBACK_STARTED = 7

            phase: "NodePool.UpdateInfo.BlueGreenInfo.Phase" = proto.Field(
                proto.ENUM,
                number=1,
                enum="NodePool.UpdateInfo.BlueGreenInfo.Phase",
            )
            blue_instance_group_urls: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=2,
            )
            green_instance_group_urls: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=3,
            )
            blue_pool_deletion_start_time: str = proto.Field(
                proto.STRING,
                number=4,
            )
            green_pool_version: str = proto.Field(
                proto.STRING,
                number=5,
            )

        blue_green_info: "NodePool.UpdateInfo.BlueGreenInfo" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="NodePool.UpdateInfo.BlueGreenInfo",
        )

    class PlacementPolicy(proto.Message):
        r"""PlacementPolicy defines the placement policy used by the node
        pool.

        Attributes:
            type_ (google.cloud.container_v1.types.NodePool.PlacementPolicy.Type):
                The type of placement.
            tpu_topology (str):
                Optional. TPU placement topology for pod slice node pool.
                https://cloud.google.com/tpu/docs/types-topologies#tpu_topologies
            policy_name (str):
                If set, refers to the name of a custom
                resource policy supplied by the user. The
                resource policy must be in the same project and
                region as the node pool. If not found,
                InvalidArgument error is returned.
        """

        class Type(proto.Enum):
            r"""Type defines the type of placement policy.

            Values:
                TYPE_UNSPECIFIED (0):
                    TYPE_UNSPECIFIED specifies no requirements on nodes
                    placement.
                COMPACT (1):
                    COMPACT specifies node placement in the same
                    availability domain to ensure low communication
                    latency.
            """
            TYPE_UNSPECIFIED = 0
            COMPACT = 1

        type_: "NodePool.PlacementPolicy.Type" = proto.Field(
            proto.ENUM,
            number=1,
            enum="NodePool.PlacementPolicy.Type",
        )
        tpu_topology: str = proto.Field(
            proto.STRING,
            number=2,
        )
        policy_name: str = proto.Field(
            proto.STRING,
            number=3,
        )

    class QueuedProvisioning(proto.Message):
        r"""QueuedProvisioning defines the queued provisioning used by
        the node pool.

        Attributes:
            enabled (bool):
                Denotes that this nodepool is QRM specific,
                meaning nodes can be only obtained through
                queuing via the Cluster Autoscaler
                ProvisioningRequest API.
        """

        enabled: bool = proto.Field(
            proto.BOOL,
            number=1,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    config: "NodeConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="NodeConfig",
    )
    initial_node_count: int = proto.Field(
        proto.INT32,
        number=3,
    )
    locations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=13,
    )
    network_config: "NodeNetworkConfig" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="NodeNetworkConfig",
    )
    self_link: str = proto.Field(
        proto.STRING,
        number=100,
    )
    version: str = proto.Field(
        proto.STRING,
        number=101,
    )
    instance_group_urls: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=102,
    )
    status: Status = proto.Field(
        proto.ENUM,
        number=103,
        enum=Status,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=104,
    )
    autoscaling: "NodePoolAutoscaling" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="NodePoolAutoscaling",
    )
    management: "NodeManagement" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="NodeManagement",
    )
    max_pods_constraint: "MaxPodsConstraint" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="MaxPodsConstraint",
    )
    conditions: MutableSequence["StatusCondition"] = proto.RepeatedField(
        proto.MESSAGE,
        number=105,
        message="StatusCondition",
    )
    pod_ipv4_cidr_size: int = proto.Field(
        proto.INT32,
        number=7,
    )
    upgrade_settings: UpgradeSettings = proto.Field(
        proto.MESSAGE,
        number=107,
        message=UpgradeSettings,
    )
    placement_policy: PlacementPolicy = proto.Field(
        proto.MESSAGE,
        number=108,
        message=PlacementPolicy,
    )
    update_info: UpdateInfo = proto.Field(
        proto.MESSAGE,
        number=109,
        message=UpdateInfo,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=110,
    )
    queued_provisioning: QueuedProvisioning = proto.Field(
        proto.MESSAGE,
        number=112,
        message=QueuedProvisioning,
    )
    best_effort_provisioning: "BestEffortProvisioning" = proto.Field(
        proto.MESSAGE,
        number=113,
        message="BestEffortProvisioning",
    )


class NodeManagement(proto.Message):
    r"""NodeManagement defines the set of node management services
    turned on for the node pool.

    Attributes:
        auto_upgrade (bool):
            A flag that specifies whether node
            auto-upgrade is enabled for the node pool. If
            enabled, node auto-upgrade helps keep the nodes
            in your node pool up to date with the latest
            release version of Kubernetes.
        auto_repair (bool):
            A flag that specifies whether the node
            auto-repair is enabled for the node pool. If
            enabled, the nodes in this node pool will be
            monitored and, if they fail health checks too
            many times, an automatic repair action will be
            triggered.
        upgrade_options (google.cloud.container_v1.types.AutoUpgradeOptions):
            Specifies the Auto Upgrade knobs for the node
            pool.
    """

    auto_upgrade: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    auto_repair: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    upgrade_options: "AutoUpgradeOptions" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="AutoUpgradeOptions",
    )


class BestEffortProvisioning(proto.Message):
    r"""Best effort provisioning.

    Attributes:
        enabled (bool):
            When this is enabled, cluster/node pool
            creations will ignore non-fatal errors like
            stockout to best provision as many nodes as
            possible right now and eventually bring up all
            target number of nodes
        min_provision_nodes (int):
            Minimum number of nodes to be provisioned to
            be considered as succeeded, and the rest of
            nodes will be provisioned gradually and
            eventually when stockout issue has been
            resolved.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    min_provision_nodes: int = proto.Field(
        proto.INT32,
        number=2,
    )


class AutoUpgradeOptions(proto.Message):
    r"""AutoUpgradeOptions defines the set of options for the user to
    control how the Auto Upgrades will proceed.

    Attributes:
        auto_upgrade_start_time (str):
            Output only. This field is set when upgrades are about to
            commence with the approximate start time for the upgrades,
            in `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        description (str):
            Output only. This field is set when upgrades
            are about to commence with the description of
            the upgrade.
    """

    auto_upgrade_start_time: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )


class MaintenancePolicy(proto.Message):
    r"""MaintenancePolicy defines the maintenance policy to be used
    for the cluster.

    Attributes:
        window (google.cloud.container_v1.types.MaintenanceWindow):
            Specifies the maintenance window in which
            maintenance may be performed.
        resource_version (str):
            A hash identifying the version of this policy, so that
            updates to fields of the policy won't accidentally undo
            intermediate changes (and so that users of the API unaware
            of some fields won't accidentally remove other fields). Make
            a ``get()`` request to the cluster to get the current
            resource version and include it with requests to set the
            policy.
    """

    window: "MaintenanceWindow" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="MaintenanceWindow",
    )
    resource_version: str = proto.Field(
        proto.STRING,
        number=3,
    )


class MaintenanceWindow(proto.Message):
    r"""MaintenanceWindow defines the maintenance window to be used
    for the cluster.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        daily_maintenance_window (google.cloud.container_v1.types.DailyMaintenanceWindow):
            DailyMaintenanceWindow specifies a daily
            maintenance operation window.

            This field is a member of `oneof`_ ``policy``.
        recurring_window (google.cloud.container_v1.types.RecurringTimeWindow):
            RecurringWindow specifies some number of
            recurring time periods for maintenance to occur.
            The time windows may be overlapping. If no
            maintenance windows are set, maintenance can
            occur at any time.

            This field is a member of `oneof`_ ``policy``.
        maintenance_exclusions (MutableMapping[str, google.cloud.container_v1.types.TimeWindow]):
            Exceptions to maintenance window.
            Non-emergency maintenance should not occur in
            these windows.
    """

    daily_maintenance_window: "DailyMaintenanceWindow" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="policy",
        message="DailyMaintenanceWindow",
    )
    recurring_window: "RecurringTimeWindow" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="policy",
        message="RecurringTimeWindow",
    )
    maintenance_exclusions: MutableMapping[str, "TimeWindow"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=4,
        message="TimeWindow",
    )


class TimeWindow(proto.Message):
    r"""Represents an arbitrary window of time.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        maintenance_exclusion_options (google.cloud.container_v1.types.MaintenanceExclusionOptions):
            MaintenanceExclusionOptions provides
            maintenance exclusion related options.

            This field is a member of `oneof`_ ``options``.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The time that the window first starts.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time that the window ends. The end time
            should take place after the start time.
    """

    maintenance_exclusion_options: "MaintenanceExclusionOptions" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="options",
        message="MaintenanceExclusionOptions",
    )
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


class MaintenanceExclusionOptions(proto.Message):
    r"""Represents the Maintenance exclusion option.

    Attributes:
        scope (google.cloud.container_v1.types.MaintenanceExclusionOptions.Scope):
            Scope specifies the upgrade scope which
            upgrades are blocked by the exclusion.
    """

    class Scope(proto.Enum):
        r"""Scope of exclusion.

        Values:
            NO_UPGRADES (0):
                NO_UPGRADES excludes all upgrades, including patch upgrades
                and minor upgrades across control planes and nodes. This is
                the default exclusion behavior.
            NO_MINOR_UPGRADES (1):
                NO_MINOR_UPGRADES excludes all minor upgrades for the
                cluster, only patches are allowed.
            NO_MINOR_OR_NODE_UPGRADES (2):
                NO_MINOR_OR_NODE_UPGRADES excludes all minor upgrades for
                the cluster, and also exclude all node pool upgrades. Only
                control plane patches are allowed.
        """
        NO_UPGRADES = 0
        NO_MINOR_UPGRADES = 1
        NO_MINOR_OR_NODE_UPGRADES = 2

    scope: Scope = proto.Field(
        proto.ENUM,
        number=1,
        enum=Scope,
    )


class RecurringTimeWindow(proto.Message):
    r"""Represents an arbitrary window of time that recurs.

    Attributes:
        window (google.cloud.container_v1.types.TimeWindow):
            The window of the first recurrence.
        recurrence (str):
            An RRULE
            (https://tools.ietf.org/html/rfc5545#section-3.8.5.3) for
            how this window reccurs. They go on for the span of time
            between the start and end time.

            For example, to have something repeat every weekday, you'd
            use: ``FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR``

            To repeat some window daily (equivalent to the
            DailyMaintenanceWindow): ``FREQ=DAILY``

            For the first weekend of every month:
            ``FREQ=MONTHLY;BYSETPOS=1;BYDAY=SA,SU``

            This specifies how frequently the window starts. Eg, if you
            wanted to have a 9-5 UTC-4 window every weekday, you'd use
            something like:

            ::

               start time = 2019-01-01T09:00:00-0400
               end time = 2019-01-01T17:00:00-0400
               recurrence = FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR

            Windows can span multiple days. Eg, to make the window
            encompass every weekend from midnight Saturday till the last
            minute of Sunday UTC:

            ::

               start time = 2019-01-05T00:00:00Z
               end time = 2019-01-07T23:59:00Z
               recurrence = FREQ=WEEKLY;BYDAY=SA

            Note the start and end time's specific dates are largely
            arbitrary except to specify duration of the window and when
            it first starts. The FREQ values of HOURLY, MINUTELY, and
            SECONDLY are not supported.
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


class DailyMaintenanceWindow(proto.Message):
    r"""Time window specified for daily maintenance operations.

    Attributes:
        start_time (str):
            Time within the maintenance window to start the maintenance
            operations. Time format should be in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ format
            "HH:MM", where HH : [00-23] and MM : [00-59] GMT.
        duration (str):
            Output only. Duration of the time window, automatically
            chosen to be smallest possible in the given scenario.
            Duration will be in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ format
            "PTnHnMnS".
    """

    start_time: str = proto.Field(
        proto.STRING,
        number=2,
    )
    duration: str = proto.Field(
        proto.STRING,
        number=3,
    )


class SetNodePoolManagementRequest(proto.Message):
    r"""SetNodePoolManagementRequest sets the node management
    properties of a node pool.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            update. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Deprecated. The name of the node pool to
            update. This field has been deprecated and
            replaced by the name field.
        management (google.cloud.container_v1.types.NodeManagement):
            Required. NodeManagement configuration for
            the node pool.
        name (str):
            The name (project, location, cluster, node pool id) of the
            node pool to set management properties. Specified in the
            format ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    node_pool_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    management: "NodeManagement" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="NodeManagement",
    )
    name: str = proto.Field(
        proto.STRING,
        number=7,
    )


class SetNodePoolSizeRequest(proto.Message):
    r"""SetNodePoolSizeRequest sets the size of a node pool.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            update. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Deprecated. The name of the node pool to
            update. This field has been deprecated and
            replaced by the name field.
        node_count (int):
            Required. The desired node count for the
            pool.
        name (str):
            The name (project, location, cluster, node pool id) of the
            node pool to set size. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    node_pool_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    node_count: int = proto.Field(
        proto.INT32,
        number=5,
    )
    name: str = proto.Field(
        proto.STRING,
        number=7,
    )


class CompleteNodePoolUpgradeRequest(proto.Message):
    r"""CompleteNodePoolUpgradeRequest sets the name of target node
    pool to complete upgrade.

    Attributes:
        name (str):
            The name (project, location, cluster, node pool id) of the
            node pool to complete upgrade. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class RollbackNodePoolUpgradeRequest(proto.Message):
    r"""RollbackNodePoolUpgradeRequest rollbacks the previously
    Aborted or Failed NodePool upgrade. This will be an no-op if the
    last upgrade successfully completed.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            rollback. This field has been deprecated and
            replaced by the name field.
        node_pool_id (str):
            Deprecated. The name of the node pool to
            rollback. This field has been deprecated and
            replaced by the name field.
        name (str):
            The name (project, location, cluster, node pool id) of the
            node poll to rollback upgrade. Specified in the format
            ``projects/*/locations/*/clusters/*/nodePools/*``.
        respect_pdb (bool):
            Option for rollback to ignore the
            PodDisruptionBudget. Default value is false.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    node_pool_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    respect_pdb: bool = proto.Field(
        proto.BOOL,
        number=7,
    )


class ListNodePoolsResponse(proto.Message):
    r"""ListNodePoolsResponse is the result of ListNodePoolsRequest.

    Attributes:
        node_pools (MutableSequence[google.cloud.container_v1.types.NodePool]):
            A list of node pools for a cluster.
    """

    node_pools: MutableSequence["NodePool"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="NodePool",
    )


class ClusterAutoscaling(proto.Message):
    r"""ClusterAutoscaling contains global, per-cluster information
    required by Cluster Autoscaler to automatically adjust the size
    of the cluster and create/delete
    node pools based on the current needs.

    Attributes:
        enable_node_autoprovisioning (bool):
            Enables automatic node pool creation and
            deletion.
        resource_limits (MutableSequence[google.cloud.container_v1.types.ResourceLimit]):
            Contains global constraints regarding minimum
            and maximum amount of resources in the cluster.
        autoscaling_profile (google.cloud.container_v1.types.ClusterAutoscaling.AutoscalingProfile):
            Defines autoscaling behaviour.
        autoprovisioning_node_pool_defaults (google.cloud.container_v1.types.AutoprovisioningNodePoolDefaults):
            AutoprovisioningNodePoolDefaults contains
            defaults for a node pool created by NAP.
        autoprovisioning_locations (MutableSequence[str]):
            The list of Google Compute Engine
            `zones <https://cloud.google.com/compute/docs/zones#available>`__
            in which the NodePool's nodes can be created by NAP.
    """

    class AutoscalingProfile(proto.Enum):
        r"""Defines possible options for autoscaling_profile field.

        Values:
            PROFILE_UNSPECIFIED (0):
                No change to autoscaling configuration.
            OPTIMIZE_UTILIZATION (1):
                Prioritize optimizing utilization of
                resources.
            BALANCED (2):
                Use default (balanced) autoscaling
                configuration.
        """
        PROFILE_UNSPECIFIED = 0
        OPTIMIZE_UTILIZATION = 1
        BALANCED = 2

    enable_node_autoprovisioning: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    resource_limits: MutableSequence["ResourceLimit"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="ResourceLimit",
    )
    autoscaling_profile: AutoscalingProfile = proto.Field(
        proto.ENUM,
        number=3,
        enum=AutoscalingProfile,
    )
    autoprovisioning_node_pool_defaults: "AutoprovisioningNodePoolDefaults" = (
        proto.Field(
            proto.MESSAGE,
            number=4,
            message="AutoprovisioningNodePoolDefaults",
        )
    )
    autoprovisioning_locations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )


class AutoprovisioningNodePoolDefaults(proto.Message):
    r"""AutoprovisioningNodePoolDefaults contains defaults for a node
    pool created by NAP.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        oauth_scopes (MutableSequence[str]):
            Scopes that are used by NAP when creating
            node pools.
        service_account (str):
            The Google Cloud Platform Service Account to
            be used by the node VMs.
        upgrade_settings (google.cloud.container_v1.types.NodePool.UpgradeSettings):
            Specifies the upgrade settings for NAP
            created node pools
        management (google.cloud.container_v1.types.NodeManagement):
            Specifies the node management options for NAP
            created node-pools.
        min_cpu_platform (str):
            Deprecated. Minimum CPU platform to be used for NAP created
            node pools. The instance may be scheduled on the specified
            or newer CPU platform. Applicable values are the friendly
            names of CPU platforms, such as minCpuPlatform: Intel
            Haswell or minCpuPlatform: Intel Sandy Bridge. For more
            information, read `how to specify min CPU
            platform <https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform>`__.
            This field is deprecated, min_cpu_platform should be
            specified using
            ``cloud.google.com/requested-min-cpu-platform`` label
            selector on the pod. To unset the min cpu platform field
            pass "automatic" as field value.
        disk_size_gb (int):
            Size of the disk attached to each node,
            specified in GB. The smallest allowed disk size
            is 10GB.

            If unspecified, the default disk size is 100GB.
        disk_type (str):
            Type of the disk attached to each node (e.g.
            'pd-standard', 'pd-ssd' or 'pd-balanced')

            If unspecified, the default disk type is
            'pd-standard'
        shielded_instance_config (google.cloud.container_v1.types.ShieldedInstanceConfig):
            Shielded Instance options.
        boot_disk_kms_key (str):
            The Customer Managed Encryption Key used to encrypt the boot
            disk attached to each node in the node pool. This should be
            of the form
            projects/[KEY_PROJECT_ID]/locations/[LOCATION]/keyRings/[RING_NAME]/cryptoKeys/[KEY_NAME].
            For more information about protecting resources with Cloud
            KMS Keys please see:
            https://cloud.google.com/compute/docs/disks/customer-managed-encryption
        image_type (str):
            The image type to use for NAP created node.
            Please see
            https://cloud.google.com/kubernetes-engine/docs/concepts/node-images
            for available image types.
        insecure_kubelet_readonly_port_enabled (bool):
            Enable or disable Kubelet read only port.

            This field is a member of `oneof`_ ``_insecure_kubelet_readonly_port_enabled``.
    """

    oauth_scopes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    service_account: str = proto.Field(
        proto.STRING,
        number=2,
    )
    upgrade_settings: "NodePool.UpgradeSettings" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="NodePool.UpgradeSettings",
    )
    management: "NodeManagement" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="NodeManagement",
    )
    min_cpu_platform: str = proto.Field(
        proto.STRING,
        number=5,
    )
    disk_size_gb: int = proto.Field(
        proto.INT32,
        number=6,
    )
    disk_type: str = proto.Field(
        proto.STRING,
        number=7,
    )
    shielded_instance_config: "ShieldedInstanceConfig" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="ShieldedInstanceConfig",
    )
    boot_disk_kms_key: str = proto.Field(
        proto.STRING,
        number=9,
    )
    image_type: str = proto.Field(
        proto.STRING,
        number=10,
    )
    insecure_kubelet_readonly_port_enabled: bool = proto.Field(
        proto.BOOL,
        number=13,
        optional=True,
    )


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

    resource_type: str = proto.Field(
        proto.STRING,
        number=1,
    )
    minimum: int = proto.Field(
        proto.INT64,
        number=2,
    )
    maximum: int = proto.Field(
        proto.INT64,
        number=3,
    )


class NodePoolAutoscaling(proto.Message):
    r"""NodePoolAutoscaling contains information required by cluster
    autoscaler to adjust the size of the node pool to the current
    cluster usage.

    Attributes:
        enabled (bool):
            Is autoscaling enabled for this node pool.
        min_node_count (int):
            Minimum number of nodes for one location in the NodePool.
            Must be >= 1 and <= max_node_count.
        max_node_count (int):
            Maximum number of nodes for one location in the NodePool.
            Must be >= min_node_count. There has to be enough quota to
            scale up the cluster.
        autoprovisioned (bool):
            Can this node pool be deleted automatically.
        location_policy (google.cloud.container_v1.types.NodePoolAutoscaling.LocationPolicy):
            Location policy used when scaling up a
            nodepool.
        total_min_node_count (int):
            Minimum number of nodes in the node pool. Must be greater
            than 1 less than total_max_node_count. The
            total_*_node_count fields are mutually exclusive with the
            \*_node_count fields.
        total_max_node_count (int):
            Maximum number of nodes in the node pool. Must be greater
            than total_min_node_count. There has to be enough quota to
            scale up the cluster. The total_*_node_count fields are
            mutually exclusive with the \*_node_count fields.
    """

    class LocationPolicy(proto.Enum):
        r"""Location policy specifies how zones are picked when scaling
        up the nodepool.

        Values:
            LOCATION_POLICY_UNSPECIFIED (0):
                Not set.
            BALANCED (1):
                BALANCED is a best effort policy that aims to
                balance the sizes of different zones.
            ANY (2):
                ANY policy picks zones that have the highest
                capacity available.
        """
        LOCATION_POLICY_UNSPECIFIED = 0
        BALANCED = 1
        ANY = 2

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    min_node_count: int = proto.Field(
        proto.INT32,
        number=2,
    )
    max_node_count: int = proto.Field(
        proto.INT32,
        number=3,
    )
    autoprovisioned: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    location_policy: LocationPolicy = proto.Field(
        proto.ENUM,
        number=5,
        enum=LocationPolicy,
    )
    total_min_node_count: int = proto.Field(
        proto.INT32,
        number=6,
    )
    total_max_node_count: int = proto.Field(
        proto.INT32,
        number=7,
    )


class SetLabelsRequest(proto.Message):
    r"""SetLabelsRequest sets the Google Cloud Platform labels on a
    Google Container Engine cluster, which will in turn set them for
    Google Compute Engine resources used by that cluster

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster.
            This field has been deprecated and replaced by
            the name field.
        resource_labels (MutableMapping[str, str]):
            Required. The labels to set for that cluster.
        label_fingerprint (str):
            Required. The fingerprint of the previous set of labels for
            this resource, used to detect conflicts. The fingerprint is
            initially generated by Kubernetes Engine and changes after
            every request to modify or update labels. You must always
            provide an up-to-date fingerprint hash when updating or
            changing labels. Make a ``get()`` request to the resource to
            get the latest fingerprint.
        name (str):
            The name (project, location, cluster name) of the cluster to
            set labels. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    resource_labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    label_fingerprint: str = proto.Field(
        proto.STRING,
        number=5,
    )
    name: str = proto.Field(
        proto.STRING,
        number=7,
    )


class SetLegacyAbacRequest(proto.Message):
    r"""SetLegacyAbacRequest enables or disables the ABAC
    authorization mechanism for a cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster to
            update. This field has been deprecated and
            replaced by the name field.
        enabled (bool):
            Required. Whether ABAC authorization will be
            enabled in the cluster.
        name (str):
            The name (project, location, cluster name) of the cluster to
            set legacy abac. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    enabled: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    name: str = proto.Field(
        proto.STRING,
        number=6,
    )


class StartIPRotationRequest(proto.Message):
    r"""StartIPRotationRequest creates a new IP for the cluster and
    then performs a node upgrade on each node pool to point to the
    new IP.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster.
            This field has been deprecated and replaced by
            the name field.
        name (str):
            The name (project, location, cluster name) of the cluster to
            start IP rotation. Specified in the format
            ``projects/*/locations/*/clusters/*``.
        rotate_credentials (bool):
            Whether to rotate credentials during IP
            rotation.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    rotate_credentials: bool = proto.Field(
        proto.BOOL,
        number=7,
    )


class CompleteIPRotationRequest(proto.Message):
    r"""CompleteIPRotationRequest moves the cluster master back into
    single-IP mode.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster.
            This field has been deprecated and replaced by
            the name field.
        name (str):
            The name (project, location, cluster name) of the cluster to
            complete IP rotation. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    name: str = proto.Field(
        proto.STRING,
        number=7,
    )


class AcceleratorConfig(proto.Message):
    r"""AcceleratorConfig represents a Hardware Accelerator request.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        accelerator_count (int):
            The number of the accelerator cards exposed
            to an instance.
        accelerator_type (str):
            The accelerator type resource name. List of supported
            accelerators
            `here <https://cloud.google.com/compute/docs/gpus>`__
        gpu_partition_size (str):
            Size of partitions to create on the GPU. Valid values are
            described in the NVIDIA `mig user
            guide <https://docs.nvidia.com/datacenter/tesla/mig-user-guide/#partitioning>`__.
        gpu_sharing_config (google.cloud.container_v1.types.GPUSharingConfig):
            The configuration for GPU sharing options.

            This field is a member of `oneof`_ ``_gpu_sharing_config``.
        gpu_driver_installation_config (google.cloud.container_v1.types.GPUDriverInstallationConfig):
            The configuration for auto installation of
            GPU driver.

            This field is a member of `oneof`_ ``_gpu_driver_installation_config``.
    """

    accelerator_count: int = proto.Field(
        proto.INT64,
        number=1,
    )
    accelerator_type: str = proto.Field(
        proto.STRING,
        number=2,
    )
    gpu_partition_size: str = proto.Field(
        proto.STRING,
        number=3,
    )
    gpu_sharing_config: "GPUSharingConfig" = proto.Field(
        proto.MESSAGE,
        number=5,
        optional=True,
        message="GPUSharingConfig",
    )
    gpu_driver_installation_config: "GPUDriverInstallationConfig" = proto.Field(
        proto.MESSAGE,
        number=6,
        optional=True,
        message="GPUDriverInstallationConfig",
    )


class GPUSharingConfig(proto.Message):
    r"""GPUSharingConfig represents the GPU sharing configuration for
    Hardware Accelerators.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        max_shared_clients_per_gpu (int):
            The max number of containers that can share a
            physical GPU.
        gpu_sharing_strategy (google.cloud.container_v1.types.GPUSharingConfig.GPUSharingStrategy):
            The type of GPU sharing strategy to enable on
            the GPU node.

            This field is a member of `oneof`_ ``_gpu_sharing_strategy``.
    """

    class GPUSharingStrategy(proto.Enum):
        r"""The type of GPU sharing strategy currently provided.

        Values:
            GPU_SHARING_STRATEGY_UNSPECIFIED (0):
                Default value.
            TIME_SHARING (1):
                GPUs are time-shared between containers.
            MPS (2):
                GPUs are shared between containers with
                NVIDIA MPS.
        """
        GPU_SHARING_STRATEGY_UNSPECIFIED = 0
        TIME_SHARING = 1
        MPS = 2

    max_shared_clients_per_gpu: int = proto.Field(
        proto.INT64,
        number=1,
    )
    gpu_sharing_strategy: GPUSharingStrategy = proto.Field(
        proto.ENUM,
        number=2,
        optional=True,
        enum=GPUSharingStrategy,
    )


class GPUDriverInstallationConfig(proto.Message):
    r"""GPUDriverInstallationConfig specifies the version of GPU
    driver to be auto installed.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gpu_driver_version (google.cloud.container_v1.types.GPUDriverInstallationConfig.GPUDriverVersion):
            Mode for how the GPU driver is installed.

            This field is a member of `oneof`_ ``_gpu_driver_version``.
    """

    class GPUDriverVersion(proto.Enum):
        r"""The GPU driver version to install.

        Values:
            GPU_DRIVER_VERSION_UNSPECIFIED (0):
                Default value is to not install any GPU
                driver.
            INSTALLATION_DISABLED (1):
                Disable GPU driver auto installation and
                needs manual installation
            DEFAULT (2):
                "Default" GPU driver in COS and Ubuntu.
            LATEST (3):
                "Latest" GPU driver in COS.
        """
        GPU_DRIVER_VERSION_UNSPECIFIED = 0
        INSTALLATION_DISABLED = 1
        DEFAULT = 2
        LATEST = 3

    gpu_driver_version: GPUDriverVersion = proto.Field(
        proto.ENUM,
        number=1,
        optional=True,
        enum=GPUDriverVersion,
    )


class WorkloadMetadataConfig(proto.Message):
    r"""WorkloadMetadataConfig defines the metadata configuration to
    expose to workloads on the node pool.

    Attributes:
        mode (google.cloud.container_v1.types.WorkloadMetadataConfig.Mode):
            Mode is the configuration for how to expose
            metadata to workloads running on the node pool.
    """

    class Mode(proto.Enum):
        r"""Mode is the configuration for how to expose metadata to
        workloads running on the node.

        Values:
            MODE_UNSPECIFIED (0):
                Not set.
            GCE_METADATA (1):
                Expose all Compute Engine metadata to pods.
            GKE_METADATA (2):
                Run the GKE Metadata Server on this node. The
                GKE Metadata Server exposes a metadata API to
                workloads that is compatible with the V1 Compute
                Metadata APIs exposed by the Compute Engine and
                App Engine Metadata Servers. This feature can
                only be enabled if Workload Identity is enabled
                at the cluster level.
        """
        MODE_UNSPECIFIED = 0
        GCE_METADATA = 1
        GKE_METADATA = 2

    mode: Mode = proto.Field(
        proto.ENUM,
        number=2,
        enum=Mode,
    )


class SetNetworkPolicyRequest(proto.Message):
    r"""SetNetworkPolicyRequest enables/disables network policy for a
    cluster.

    Attributes:
        project_id (str):
            Deprecated. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
            This field has been deprecated and replaced by the name
            field.
        zone (str):
            Deprecated. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides. This field has been deprecated
            and replaced by the name field.
        cluster_id (str):
            Deprecated. The name of the cluster.
            This field has been deprecated and replaced by
            the name field.
        network_policy (google.cloud.container_v1.types.NetworkPolicy):
            Required. Configuration options for the
            NetworkPolicy feature.
        name (str):
            The name (project, location, cluster name) of the cluster to
            set networking policy. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    network_policy: "NetworkPolicy" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="NetworkPolicy",
    )
    name: str = proto.Field(
        proto.STRING,
        number=6,
    )


class SetMaintenancePolicyRequest(proto.Message):
    r"""SetMaintenancePolicyRequest sets the maintenance policy for a
    cluster.

    Attributes:
        project_id (str):
            Required. The Google Developers Console `project ID or
            project
            number <https://cloud.google.com/resource-manager/docs/creating-managing-projects>`__.
        zone (str):
            Required. The name of the Google Compute Engine
            `zone <https://cloud.google.com/compute/docs/zones#available>`__
            in which the cluster resides.
        cluster_id (str):
            Required. The name of the cluster to update.
        maintenance_policy (google.cloud.container_v1.types.MaintenancePolicy):
            Required. The maintenance policy to be set
            for the cluster. An empty field clears the
            existing maintenance policy.
        name (str):
            The name (project, location, cluster name) of the cluster to
            set maintenance policy. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    maintenance_policy: "MaintenancePolicy" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="MaintenancePolicy",
    )
    name: str = proto.Field(
        proto.STRING,
        number=5,
    )


class StatusCondition(proto.Message):
    r"""StatusCondition describes why a cluster or a node pool has a
    certain status (e.g., ERROR or DEGRADED).

    Attributes:
        code (google.cloud.container_v1.types.StatusCondition.Code):
            Machine-friendly representation of the condition Deprecated.
            Use canonical_code instead.
        message (str):
            Human-friendly representation of the
            condition
        canonical_code (google.rpc.code_pb2.Code):
            Canonical code of the condition.
    """

    class Code(proto.Enum):
        r"""Code for each condition

        Values:
            UNKNOWN (0):
                UNKNOWN indicates a generic condition.
            GCE_STOCKOUT (1):
                GCE_STOCKOUT indicates that Google Compute Engine resources
                are temporarily unavailable.
            GKE_SERVICE_ACCOUNT_DELETED (2):
                GKE_SERVICE_ACCOUNT_DELETED indicates that the user deleted
                their robot service account.
            GCE_QUOTA_EXCEEDED (3):
                Google Compute Engine quota was exceeded.
            SET_BY_OPERATOR (4):
                Cluster state was manually changed by an SRE
                due to a system logic error.
            CLOUD_KMS_KEY_ERROR (7):
                Unable to perform an encrypt operation
                against the CloudKMS key used for etcd level
                encryption.
            CA_EXPIRING (9):
                Cluster CA is expiring soon.
        """
        UNKNOWN = 0
        GCE_STOCKOUT = 1
        GKE_SERVICE_ACCOUNT_DELETED = 2
        GCE_QUOTA_EXCEEDED = 3
        SET_BY_OPERATOR = 4
        CLOUD_KMS_KEY_ERROR = 7
        CA_EXPIRING = 9

    code: Code = proto.Field(
        proto.ENUM,
        number=1,
        enum=Code,
    )
    message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    canonical_code: code_pb2.Code = proto.Field(
        proto.ENUM,
        number=3,
        enum=code_pb2.Code,
    )


class NetworkConfig(proto.Message):
    r"""NetworkConfig reports the relative names of network &
    subnetwork.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        network (str):
            Output only. The relative name of the Google Compute Engine
            [network]`google.container.v1.NetworkConfig.network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`__
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
        default_snat_status (google.cloud.container_v1.types.DefaultSnatStatus):
            Whether the cluster disables default in-node sNAT rules.
            In-node sNAT rules will be disabled when default_snat_status
            is disabled. When disabled is set to false, default IP
            masquerade rules will be applied to the nodes to prevent
            sNAT on cluster internal traffic.
        enable_l4ilb_subsetting (bool):
            Whether L4ILB Subsetting is enabled for this
            cluster.
        datapath_provider (google.cloud.container_v1.types.DatapathProvider):
            The desired datapath provider for this
            cluster. By default, uses the IPTables-based
            kube-proxy implementation.
        private_ipv6_google_access (google.cloud.container_v1.types.PrivateIPv6GoogleAccess):
            The desired state of IPv6 connectivity to
            Google Services. By default, no private IPv6
            access to or from Google Services (all access
            will be via IPv4)
        dns_config (google.cloud.container_v1.types.DNSConfig):
            DNSConfig contains clusterDNS config for this
            cluster.
        service_external_ips_config (google.cloud.container_v1.types.ServiceExternalIPsConfig):
            ServiceExternalIPsConfig specifies if
            services with externalIPs field are blocked or
            not.
        gateway_api_config (google.cloud.container_v1.types.GatewayAPIConfig):
            GatewayAPIConfig contains the desired config
            of Gateway API on this cluster.
        enable_multi_networking (bool):
            Whether multi-networking is enabled for this
            cluster.
        network_performance_config (google.cloud.container_v1.types.NetworkConfig.ClusterNetworkPerformanceConfig):
            Network bandwidth tier configuration.
        enable_fqdn_network_policy (bool):
            Whether FQDN Network Policy is enabled on
            this cluster.

            This field is a member of `oneof`_ ``_enable_fqdn_network_policy``.
        in_transit_encryption_config (google.cloud.container_v1.types.InTransitEncryptionConfig):
            Specify the details of in-transit encryption.
            Now named inter-node transparent encryption.

            This field is a member of `oneof`_ ``_in_transit_encryption_config``.
        enable_cilium_clusterwide_network_policy (bool):
            Whether CiliumClusterwideNetworkPolicy is
            enabled on this cluster.

            This field is a member of `oneof`_ ``_enable_cilium_clusterwide_network_policy``.
    """

    class ClusterNetworkPerformanceConfig(proto.Message):
        r"""Configuration of network bandwidth tiers

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            total_egress_bandwidth_tier (google.cloud.container_v1.types.NetworkConfig.ClusterNetworkPerformanceConfig.Tier):
                Specifies the total network bandwidth tier
                for NodePools in the cluster.

                This field is a member of `oneof`_ ``_total_egress_bandwidth_tier``.
        """

        class Tier(proto.Enum):
            r"""Node network tier

            Values:
                TIER_UNSPECIFIED (0):
                    Default value
                TIER_1 (1):
                    Higher bandwidth, actual values based on VM
                    size.
            """
            TIER_UNSPECIFIED = 0
            TIER_1 = 1

        total_egress_bandwidth_tier: "NetworkConfig.ClusterNetworkPerformanceConfig.Tier" = proto.Field(
            proto.ENUM,
            number=1,
            optional=True,
            enum="NetworkConfig.ClusterNetworkPerformanceConfig.Tier",
        )

    network: str = proto.Field(
        proto.STRING,
        number=1,
    )
    subnetwork: str = proto.Field(
        proto.STRING,
        number=2,
    )
    enable_intra_node_visibility: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    default_snat_status: "DefaultSnatStatus" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="DefaultSnatStatus",
    )
    enable_l4ilb_subsetting: bool = proto.Field(
        proto.BOOL,
        number=10,
    )
    datapath_provider: "DatapathProvider" = proto.Field(
        proto.ENUM,
        number=11,
        enum="DatapathProvider",
    )
    private_ipv6_google_access: "PrivateIPv6GoogleAccess" = proto.Field(
        proto.ENUM,
        number=12,
        enum="PrivateIPv6GoogleAccess",
    )
    dns_config: "DNSConfig" = proto.Field(
        proto.MESSAGE,
        number=13,
        message="DNSConfig",
    )
    service_external_ips_config: "ServiceExternalIPsConfig" = proto.Field(
        proto.MESSAGE,
        number=15,
        message="ServiceExternalIPsConfig",
    )
    gateway_api_config: "GatewayAPIConfig" = proto.Field(
        proto.MESSAGE,
        number=16,
        message="GatewayAPIConfig",
    )
    enable_multi_networking: bool = proto.Field(
        proto.BOOL,
        number=17,
    )
    network_performance_config: ClusterNetworkPerformanceConfig = proto.Field(
        proto.MESSAGE,
        number=18,
        message=ClusterNetworkPerformanceConfig,
    )
    enable_fqdn_network_policy: bool = proto.Field(
        proto.BOOL,
        number=19,
        optional=True,
    )
    in_transit_encryption_config: "InTransitEncryptionConfig" = proto.Field(
        proto.ENUM,
        number=20,
        optional=True,
        enum="InTransitEncryptionConfig",
    )
    enable_cilium_clusterwide_network_policy: bool = proto.Field(
        proto.BOOL,
        number=21,
        optional=True,
    )


class GatewayAPIConfig(proto.Message):
    r"""GatewayAPIConfig contains the desired config of Gateway API
    on this cluster.

    Attributes:
        channel (google.cloud.container_v1.types.GatewayAPIConfig.Channel):
            The Gateway API release channel to use for
            Gateway API.
    """

    class Channel(proto.Enum):
        r"""Channel describes if/how Gateway API should be installed and
        implemented in a cluster.

        Values:
            CHANNEL_UNSPECIFIED (0):
                Default value.
            CHANNEL_DISABLED (1):
                Gateway API support is disabled
            CHANNEL_EXPERIMENTAL (3):
                Deprecated: use CHANNEL_STANDARD instead. Gateway API
                support is enabled, experimental CRDs are installed
            CHANNEL_STANDARD (4):
                Gateway API support is enabled, standard CRDs
                are installed
        """
        CHANNEL_UNSPECIFIED = 0
        CHANNEL_DISABLED = 1
        CHANNEL_EXPERIMENTAL = 3
        CHANNEL_STANDARD = 4

    channel: Channel = proto.Field(
        proto.ENUM,
        number=1,
        enum=Channel,
    )


class ServiceExternalIPsConfig(proto.Message):
    r"""Config to block services with externalIPs field.

    Attributes:
        enabled (bool):
            Whether Services with ExternalIPs field are
            allowed or not.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class GetOpenIDConfigRequest(proto.Message):
    r"""GetOpenIDConfigRequest gets the OIDC discovery document for
    the cluster. See the OpenID Connect Discovery 1.0 specification
    for details.

    Attributes:
        parent (str):
            The cluster (project, location, cluster name) to get the
            discovery document for. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetOpenIDConfigResponse(proto.Message):
    r"""GetOpenIDConfigResponse is an OIDC discovery document for the
    cluster. See the OpenID Connect Discovery 1.0 specification for
    details.

    Attributes:
        issuer (str):
            OIDC Issuer.
        jwks_uri (str):
            JSON Web Key uri.
        response_types_supported (MutableSequence[str]):
            Supported response types.
        subject_types_supported (MutableSequence[str]):
            Supported subject types.
        id_token_signing_alg_values_supported (MutableSequence[str]):
            supported ID Token signing Algorithms.
        claims_supported (MutableSequence[str]):
            Supported claims.
        grant_types (MutableSequence[str]):
            Supported grant types.
    """

    issuer: str = proto.Field(
        proto.STRING,
        number=1,
    )
    jwks_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    response_types_supported: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    subject_types_supported: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    id_token_signing_alg_values_supported: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    claims_supported: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    grant_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )


class GetJSONWebKeysRequest(proto.Message):
    r"""GetJSONWebKeysRequest gets the public component of the keys used by
    the cluster to sign token requests. This will be the jwks_uri for
    the discover document returned by getOpenIDConfig. See the OpenID
    Connect Discovery 1.0 specification for details.

    Attributes:
        parent (str):
            The cluster (project, location, cluster name) to get keys
            for. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class Jwk(proto.Message):
    r"""Jwk is a JSON Web Key as specified in RFC 7517

    Attributes:
        kty (str):
            Key Type.
        alg (str):
            Algorithm.
        use (str):
            Permitted uses for the public keys.
        kid (str):
            Key ID.
        n (str):
            Used for RSA keys.
        e (str):
            Used for RSA keys.
        x (str):
            Used for ECDSA keys.
        y (str):
            Used for ECDSA keys.
        crv (str):
            Used for ECDSA keys.
    """

    kty: str = proto.Field(
        proto.STRING,
        number=1,
    )
    alg: str = proto.Field(
        proto.STRING,
        number=2,
    )
    use: str = proto.Field(
        proto.STRING,
        number=3,
    )
    kid: str = proto.Field(
        proto.STRING,
        number=4,
    )
    n: str = proto.Field(
        proto.STRING,
        number=5,
    )
    e: str = proto.Field(
        proto.STRING,
        number=6,
    )
    x: str = proto.Field(
        proto.STRING,
        number=7,
    )
    y: str = proto.Field(
        proto.STRING,
        number=8,
    )
    crv: str = proto.Field(
        proto.STRING,
        number=9,
    )


class GetJSONWebKeysResponse(proto.Message):
    r"""GetJSONWebKeysResponse is a valid JSON Web Key Set as
    specififed in rfc 7517

    Attributes:
        keys (MutableSequence[google.cloud.container_v1.types.Jwk]):
            The public component of the keys used by the
            cluster to sign token requests.
    """

    keys: MutableSequence["Jwk"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Jwk",
    )


class CheckAutopilotCompatibilityRequest(proto.Message):
    r"""CheckAutopilotCompatibilityRequest requests getting the
    blockers for the given operation in the cluster.

    Attributes:
        name (str):
            The name (project, location, cluster) of the cluster to
            retrieve. Specified in the format
            ``projects/*/locations/*/clusters/*``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AutopilotCompatibilityIssue(proto.Message):
    r"""AutopilotCompatibilityIssue contains information about a
    specific compatibility issue with Autopilot mode.

    Attributes:
        last_observation (google.protobuf.timestamp_pb2.Timestamp):
            The last time when this issue was observed.
        constraint_type (str):
            The constraint type of the issue.
        incompatibility_type (google.cloud.container_v1.types.AutopilotCompatibilityIssue.IssueType):
            The incompatibility type of this issue.
        subjects (MutableSequence[str]):
            The name of the resources which are subject
            to this issue.
        documentation_url (str):
            A URL to a public documnetation, which
            addresses resolving this issue.
        description (str):
            The description of the issue.
    """

    class IssueType(proto.Enum):
        r"""The type of the reported issue.

        Values:
            UNSPECIFIED (0):
                Default value, should not be used.
            INCOMPATIBILITY (1):
                Indicates that the issue is a known
                incompatibility between the cluster and
                Autopilot mode.
            ADDITIONAL_CONFIG_REQUIRED (2):
                Indicates the issue is an incompatibility if
                customers take no further action to resolve.
            PASSED_WITH_OPTIONAL_CONFIG (3):
                Indicates the issue is not an
                incompatibility, but depending on the workloads
                business logic, there is a potential that they
                won't work on Autopilot.
        """
        UNSPECIFIED = 0
        INCOMPATIBILITY = 1
        ADDITIONAL_CONFIG_REQUIRED = 2
        PASSED_WITH_OPTIONAL_CONFIG = 3

    last_observation: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    constraint_type: str = proto.Field(
        proto.STRING,
        number=2,
    )
    incompatibility_type: IssueType = proto.Field(
        proto.ENUM,
        number=3,
        enum=IssueType,
    )
    subjects: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    documentation_url: str = proto.Field(
        proto.STRING,
        number=5,
    )
    description: str = proto.Field(
        proto.STRING,
        number=6,
    )


class CheckAutopilotCompatibilityResponse(proto.Message):
    r"""CheckAutopilotCompatibilityResponse has a list of
    compatibility issues.

    Attributes:
        issues (MutableSequence[google.cloud.container_v1.types.AutopilotCompatibilityIssue]):
            The list of issues for the given operation.
        summary (str):
            The summary of the autopilot compatibility
            response.
    """

    issues: MutableSequence["AutopilotCompatibilityIssue"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AutopilotCompatibilityIssue",
    )
    summary: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ReleaseChannel(proto.Message):
    r"""ReleaseChannel indicates which release channel a cluster is
    subscribed to. Release channels are arranged in order of risk.

    When a cluster is subscribed to a release channel, Google
    maintains both the master version and the node version. Node
    auto-upgrade defaults to true and cannot be disabled.

    Attributes:
        channel (google.cloud.container_v1.types.ReleaseChannel.Channel):
            channel specifies which release channel the
            cluster is subscribed to.
    """

    class Channel(proto.Enum):
        r"""Possible values for 'channel'.

        Values:
            UNSPECIFIED (0):
                No channel specified.
            RAPID (1):
                RAPID channel is offered on an early access
                basis for customers who want to test new
                releases.

                WARNING: Versions available in the RAPID Channel
                may be subject to unresolved issues with no
                known workaround and are not subject to any
                SLAs.
            REGULAR (2):
                Clusters subscribed to REGULAR receive
                versions that are considered GA quality. REGULAR
                is intended for production users who want to
                take advantage of new features.
            STABLE (3):
                Clusters subscribed to STABLE receive
                versions that are known to be stable and
                reliable in production.
            EXTENDED (4):
                Clusters subscribed to EXTENDED receive
                extended support and availability for versions
                which are known to be stable and reliable in
                production.
        """
        UNSPECIFIED = 0
        RAPID = 1
        REGULAR = 2
        STABLE = 3
        EXTENDED = 4

    channel: Channel = proto.Field(
        proto.ENUM,
        number=1,
        enum=Channel,
    )


class CostManagementConfig(proto.Message):
    r"""Configuration for fine-grained cost management feature.

    Attributes:
        enabled (bool):
            Whether the feature is enabled or not.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class IntraNodeVisibilityConfig(proto.Message):
    r"""IntraNodeVisibilityConfig contains the desired config of the
    intra-node visibility on this cluster.

    Attributes:
        enabled (bool):
            Enables intra node visibility for this
            cluster.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class ILBSubsettingConfig(proto.Message):
    r"""ILBSubsettingConfig contains the desired config of L4
    Internal LoadBalancer subsetting on this cluster.

    Attributes:
        enabled (bool):
            Enables l4 ILB subsetting for this cluster.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class DNSConfig(proto.Message):
    r"""DNSConfig contains the desired set of options for configuring
    clusterDNS.

    Attributes:
        cluster_dns (google.cloud.container_v1.types.DNSConfig.Provider):
            cluster_dns indicates which in-cluster DNS provider should
            be used.
        cluster_dns_scope (google.cloud.container_v1.types.DNSConfig.DNSScope):
            cluster_dns_scope indicates the scope of access to cluster
            DNS records.
        cluster_dns_domain (str):
            cluster_dns_domain is the suffix used for all cluster
            service records.
        additive_vpc_scope_dns_domain (str):
            Optional. The domain used in Additive VPC
            scope.
    """

    class Provider(proto.Enum):
        r"""Provider lists the various in-cluster DNS providers.

        Values:
            PROVIDER_UNSPECIFIED (0):
                Default value
            PLATFORM_DEFAULT (1):
                Use GKE default DNS provider(kube-dns) for
                DNS resolution.
            CLOUD_DNS (2):
                Use CloudDNS for DNS resolution.
            KUBE_DNS (3):
                Use KubeDNS for DNS resolution.
        """
        PROVIDER_UNSPECIFIED = 0
        PLATFORM_DEFAULT = 1
        CLOUD_DNS = 2
        KUBE_DNS = 3

    class DNSScope(proto.Enum):
        r"""DNSScope lists the various scopes of access to cluster DNS
        records.

        Values:
            DNS_SCOPE_UNSPECIFIED (0):
                Default value, will be inferred as cluster
                scope.
            CLUSTER_SCOPE (1):
                DNS records are accessible from within the
                cluster.
            VPC_SCOPE (2):
                DNS records are accessible from within the
                VPC.
        """
        DNS_SCOPE_UNSPECIFIED = 0
        CLUSTER_SCOPE = 1
        VPC_SCOPE = 2

    cluster_dns: Provider = proto.Field(
        proto.ENUM,
        number=1,
        enum=Provider,
    )
    cluster_dns_scope: DNSScope = proto.Field(
        proto.ENUM,
        number=2,
        enum=DNSScope,
    )
    cluster_dns_domain: str = proto.Field(
        proto.STRING,
        number=3,
    )
    additive_vpc_scope_dns_domain: str = proto.Field(
        proto.STRING,
        number=5,
    )


class MaxPodsConstraint(proto.Message):
    r"""Constraints applied to pods.

    Attributes:
        max_pods_per_node (int):
            Constraint enforced on the max num of pods
            per node.
    """

    max_pods_per_node: int = proto.Field(
        proto.INT64,
        number=1,
    )


class WorkloadIdentityConfig(proto.Message):
    r"""Configuration for the use of Kubernetes Service Accounts in
    GCP IAM policies.

    Attributes:
        workload_pool (str):
            The workload pool to attach all Kubernetes
            service accounts to.
    """

    workload_pool: str = proto.Field(
        proto.STRING,
        number=2,
    )


class IdentityServiceConfig(proto.Message):
    r"""IdentityServiceConfig is configuration for Identity Service
    which allows customers to use external identity providers with
    the K8S API

    Attributes:
        enabled (bool):
            Whether to enable the Identity Service
            component
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class MeshCertificates(proto.Message):
    r"""Configuration for issuance of mTLS keys and certificates to
    Kubernetes pods.

    Attributes:
        enable_certificates (google.protobuf.wrappers_pb2.BoolValue):
            enable_certificates controls issuance of workload mTLS
            certificates.

            If set, the GKE Workload Identity Certificates controller
            and node agent will be deployed in the cluster, which can
            then be configured by creating a WorkloadCertificateConfig
            Custom Resource.

            Requires Workload Identity
            ([workload_pool][google.container.v1.WorkloadIdentityConfig.workload_pool]
            must be non-empty).
    """

    enable_certificates: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=1,
        message=wrappers_pb2.BoolValue,
    )


class DatabaseEncryption(proto.Message):
    r"""Configuration of etcd encryption.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        key_name (str):
            Name of CloudKMS key to use for the
            encryption of secrets in etcd. Ex.
            projects/my-project/locations/global/keyRings/my-ring/cryptoKeys/my-key
        state (google.cloud.container_v1.types.DatabaseEncryption.State):
            The desired state of etcd encryption.
        current_state (google.cloud.container_v1.types.DatabaseEncryption.CurrentState):
            Output only. The current state of etcd
            encryption.

            This field is a member of `oneof`_ ``_current_state``.
        decryption_keys (MutableSequence[str]):
            Output only. Keys in use by the cluster for decrypting
            existing objects, in addition to the key in ``key_name``.

            Each item is a CloudKMS key resource.
        last_operation_errors (MutableSequence[google.cloud.container_v1.types.DatabaseEncryption.OperationError]):
            Output only. Records errors seen during
            DatabaseEncryption update operations.
    """

    class State(proto.Enum):
        r"""State of etcd encryption.

        Values:
            UNKNOWN (0):
                Should never be set
            ENCRYPTED (1):
                Secrets in etcd are encrypted.
            DECRYPTED (2):
                Secrets in etcd are stored in plain text (at
                etcd level) - this is unrelated to Compute
                Engine level full disk encryption.
        """
        UNKNOWN = 0
        ENCRYPTED = 1
        DECRYPTED = 2

    class CurrentState(proto.Enum):
        r"""Current State of etcd encryption.

        Values:
            CURRENT_STATE_UNSPECIFIED (0):
                Should never be set
            CURRENT_STATE_ENCRYPTED (7):
                Secrets in etcd are encrypted.
            CURRENT_STATE_DECRYPTED (2):
                Secrets in etcd are stored in plain text (at
                etcd level) - this is unrelated to Compute
                Engine level full disk encryption.
            CURRENT_STATE_ENCRYPTION_PENDING (3):
                Encryption (or re-encryption with a different
                CloudKMS key) of Secrets is in progress.
            CURRENT_STATE_ENCRYPTION_ERROR (4):
                Encryption (or re-encryption with a different
                CloudKMS key) of Secrets in etcd encountered an
                error.
            CURRENT_STATE_DECRYPTION_PENDING (5):
                De-crypting Secrets to plain text in etcd is
                in progress.
            CURRENT_STATE_DECRYPTION_ERROR (6):
                De-crypting Secrets to plain text in etcd
                encountered an error.
        """
        CURRENT_STATE_UNSPECIFIED = 0
        CURRENT_STATE_ENCRYPTED = 7
        CURRENT_STATE_DECRYPTED = 2
        CURRENT_STATE_ENCRYPTION_PENDING = 3
        CURRENT_STATE_ENCRYPTION_ERROR = 4
        CURRENT_STATE_DECRYPTION_PENDING = 5
        CURRENT_STATE_DECRYPTION_ERROR = 6

    class OperationError(proto.Message):
        r"""OperationError records errors seen from CloudKMS keys
        encountered during updates to DatabaseEncryption configuration.

        Attributes:
            key_name (str):
                CloudKMS key resource that had the error.
            error_message (str):
                Description of the error seen during the
                operation.
            timestamp (google.protobuf.timestamp_pb2.Timestamp):
                Time when the CloudKMS error was seen.
        """

        key_name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        error_message: str = proto.Field(
            proto.STRING,
            number=2,
        )
        timestamp: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=3,
            message=timestamp_pb2.Timestamp,
        )

    key_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )
    current_state: CurrentState = proto.Field(
        proto.ENUM,
        number=3,
        optional=True,
        enum=CurrentState,
    )
    decryption_keys: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    last_operation_errors: MutableSequence[OperationError] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=OperationError,
    )


class ListUsableSubnetworksRequest(proto.Message):
    r"""ListUsableSubnetworksRequest requests the list of usable
    subnetworks available to a user for creating clusters.

    Attributes:
        parent (str):
            The parent project where subnetworks are usable. Specified
            in the format ``projects/*``.
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

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
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


class ListUsableSubnetworksResponse(proto.Message):
    r"""ListUsableSubnetworksResponse is the response of
    ListUsableSubnetworksRequest.

    Attributes:
        subnetworks (MutableSequence[google.cloud.container_v1.types.UsableSubnetwork]):
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

    subnetworks: MutableSequence["UsableSubnetwork"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="UsableSubnetwork",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


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
        status (google.cloud.container_v1.types.UsableSubnetworkSecondaryRange.Status):
            This field is to determine the status of the
            secondary range programmably.
    """

    class Status(proto.Enum):
        r"""Status shows the current usage of a secondary IP range.

        Values:
            UNKNOWN (0):
                UNKNOWN is the zero value of the Status enum.
                It's not a valid status.
            UNUSED (1):
                UNUSED denotes that this range is unclaimed
                by any cluster.
            IN_USE_SERVICE (2):
                IN_USE_SERVICE denotes that this range is claimed by
                cluster(s) for services. User-managed services range can be
                shared between clusters within the same subnetwork.
            IN_USE_SHAREABLE_POD (3):
                IN_USE_SHAREABLE_POD denotes this range was created by the
                network admin and is currently claimed by a cluster for
                pods. It can only be used by other clusters as a pod range.
            IN_USE_MANAGED_POD (4):
                IN_USE_MANAGED_POD denotes this range was created by GKE and
                is claimed for pods. It cannot be used for other clusters.
        """
        UNKNOWN = 0
        UNUSED = 1
        IN_USE_SERVICE = 2
        IN_USE_SHAREABLE_POD = 3
        IN_USE_MANAGED_POD = 4

    range_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ip_cidr_range: str = proto.Field(
        proto.STRING,
        number=2,
    )
    status: Status = proto.Field(
        proto.ENUM,
        number=3,
        enum=Status,
    )


class UsableSubnetwork(proto.Message):
    r"""UsableSubnetwork resource returns the subnetwork name, its
    associated network and the primary CIDR range.

    Attributes:
        subnetwork (str):
            Subnetwork Name.
            Example:
            projects/my-project/regions/us-central1/subnetworks/my-subnet
        network (str):
            Network Name.
            Example:
            projects/my-project/global/networks/my-network
        ip_cidr_range (str):
            The range of internal addresses that are
            owned by this subnetwork.
        secondary_ip_ranges (MutableSequence[google.cloud.container_v1.types.UsableSubnetworkSecondaryRange]):
            Secondary IP ranges.
        status_message (str):
            A human readable status message representing the reasons for
            cases where the caller cannot use the secondary ranges under
            the subnet. For example if the secondary_ip_ranges is empty
            due to a permission issue, an insufficient permission
            message will be given by status_message.
    """

    subnetwork: str = proto.Field(
        proto.STRING,
        number=1,
    )
    network: str = proto.Field(
        proto.STRING,
        number=2,
    )
    ip_cidr_range: str = proto.Field(
        proto.STRING,
        number=3,
    )
    secondary_ip_ranges: MutableSequence[
        "UsableSubnetworkSecondaryRange"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="UsableSubnetworkSecondaryRange",
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ResourceUsageExportConfig(proto.Message):
    r"""Configuration for exporting cluster resource usages.

    Attributes:
        bigquery_destination (google.cloud.container_v1.types.ResourceUsageExportConfig.BigQueryDestination):
            Configuration to use BigQuery as usage export
            destination.
        enable_network_egress_metering (bool):
            Whether to enable network egress metering for
            this cluster. If enabled, a daemonset will be
            created in the cluster to meter network egress
            traffic.
        consumption_metering_config (google.cloud.container_v1.types.ResourceUsageExportConfig.ConsumptionMeteringConfig):
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

        dataset_id: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class ConsumptionMeteringConfig(proto.Message):
        r"""Parameters for controlling consumption metering.

        Attributes:
            enabled (bool):
                Whether to enable consumption metering for
                this cluster. If enabled, a second BigQuery
                table will be created to hold resource
                consumption records.
        """

        enabled: bool = proto.Field(
            proto.BOOL,
            number=1,
        )

    bigquery_destination: BigQueryDestination = proto.Field(
        proto.MESSAGE,
        number=1,
        message=BigQueryDestination,
    )
    enable_network_egress_metering: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    consumption_metering_config: ConsumptionMeteringConfig = proto.Field(
        proto.MESSAGE,
        number=3,
        message=ConsumptionMeteringConfig,
    )


class VerticalPodAutoscaling(proto.Message):
    r"""VerticalPodAutoscaling contains global, per-cluster
    information required by Vertical Pod Autoscaler to automatically
    adjust the resources of pods controlled by it.

    Attributes:
        enabled (bool):
            Enables vertical pod autoscaling.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class DefaultSnatStatus(proto.Message):
    r"""DefaultSnatStatus contains the desired state of whether
    default sNAT should be disabled on the cluster.

    Attributes:
        disabled (bool):
            Disables cluster default sNAT rules.
    """

    disabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class ShieldedNodes(proto.Message):
    r"""Configuration of Shielded Nodes feature.

    Attributes:
        enabled (bool):
            Whether Shielded Nodes features are enabled
            on all nodes in this cluster.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class VirtualNIC(proto.Message):
    r"""Configuration of gVNIC feature.

    Attributes:
        enabled (bool):
            Whether gVNIC features are enabled in the
            node pool.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class FastSocket(proto.Message):
    r"""Configuration of Fast Socket feature.

    Attributes:
        enabled (bool):
            Whether Fast Socket features are enabled in
            the node pool.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class NotificationConfig(proto.Message):
    r"""NotificationConfig is the configuration of notifications.

    Attributes:
        pubsub (google.cloud.container_v1.types.NotificationConfig.PubSub):
            Notification config for Pub/Sub.
    """

    class EventType(proto.Enum):
        r"""Types of notifications currently supported. Can be used to
        filter what notifications are sent.

        Values:
            EVENT_TYPE_UNSPECIFIED (0):
                Not set, will be ignored.
            UPGRADE_AVAILABLE_EVENT (1):
                Corresponds with UpgradeAvailableEvent.
            UPGRADE_EVENT (2):
                Corresponds with UpgradeEvent.
            SECURITY_BULLETIN_EVENT (3):
                Corresponds with SecurityBulletinEvent.
        """
        EVENT_TYPE_UNSPECIFIED = 0
        UPGRADE_AVAILABLE_EVENT = 1
        UPGRADE_EVENT = 2
        SECURITY_BULLETIN_EVENT = 3

    class PubSub(proto.Message):
        r"""Pub/Sub specific notification config.

        Attributes:
            enabled (bool):
                Enable notifications for Pub/Sub.
            topic (str):
                The desired Pub/Sub topic to which notifications will be
                sent by GKE. Format is
                ``projects/{project}/topics/{topic}``.
            filter (google.cloud.container_v1.types.NotificationConfig.Filter):
                Allows filtering to one or more specific
                event types. If no filter is specified, or if a
                filter is specified with no event types, all
                event types will be sent
        """

        enabled: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        topic: str = proto.Field(
            proto.STRING,
            number=2,
        )
        filter: "NotificationConfig.Filter" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="NotificationConfig.Filter",
        )

    class Filter(proto.Message):
        r"""Allows filtering to one or more specific event types. If
        event types are present, those and only those event types will
        be transmitted to the cluster. Other types will be skipped. If
        no filter is specified, or no event types are present, all event
        types will be sent

        Attributes:
            event_type (MutableSequence[google.cloud.container_v1.types.NotificationConfig.EventType]):
                Event types to allowlist.
        """

        event_type: MutableSequence[
            "NotificationConfig.EventType"
        ] = proto.RepeatedField(
            proto.ENUM,
            number=1,
            enum="NotificationConfig.EventType",
        )

    pubsub: PubSub = proto.Field(
        proto.MESSAGE,
        number=1,
        message=PubSub,
    )


class ConfidentialNodes(proto.Message):
    r"""ConfidentialNodes is configuration for the confidential nodes
    feature, which makes nodes run on confidential VMs.

    Attributes:
        enabled (bool):
            Whether Confidential Nodes feature is
            enabled.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class UpgradeEvent(proto.Message):
    r"""UpgradeEvent is a notification sent to customers by the
    cluster server when a resource is upgrading.

    Attributes:
        resource_type (google.cloud.container_v1.types.UpgradeResourceType):
            The resource type that is upgrading.
        operation (str):
            The operation associated with this upgrade.
        operation_start_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the operation was started.
        current_version (str):
            The current version before the upgrade.
        target_version (str):
            The target version for the upgrade.
        resource (str):
            Optional relative path to the resource. For
            example in node pool upgrades, the relative path
            of the node pool.
    """

    resource_type: "UpgradeResourceType" = proto.Field(
        proto.ENUM,
        number=1,
        enum="UpgradeResourceType",
    )
    operation: str = proto.Field(
        proto.STRING,
        number=2,
    )
    operation_start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    current_version: str = proto.Field(
        proto.STRING,
        number=4,
    )
    target_version: str = proto.Field(
        proto.STRING,
        number=5,
    )
    resource: str = proto.Field(
        proto.STRING,
        number=6,
    )


class UpgradeAvailableEvent(proto.Message):
    r"""UpgradeAvailableEvent is a notification sent to customers
    when a new available version is released.

    Attributes:
        version (str):
            The release version available for upgrade.
        resource_type (google.cloud.container_v1.types.UpgradeResourceType):
            The resource type of the release version.
        release_channel (google.cloud.container_v1.types.ReleaseChannel):
            The release channel of the version. If empty,
            it means a non-channel release.
        resource (str):
            Optional relative path to the resource. For
            example, the relative path of the node pool.
    """

    version: str = proto.Field(
        proto.STRING,
        number=1,
    )
    resource_type: "UpgradeResourceType" = proto.Field(
        proto.ENUM,
        number=2,
        enum="UpgradeResourceType",
    )
    release_channel: "ReleaseChannel" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="ReleaseChannel",
    )
    resource: str = proto.Field(
        proto.STRING,
        number=4,
    )


class SecurityBulletinEvent(proto.Message):
    r"""SecurityBulletinEvent is a notification sent to customers
    when a security bulletin has been posted that they are
    vulnerable to.

    Attributes:
        resource_type_affected (str):
            The resource type (node/control plane) that
            has the vulnerability. Multiple notifications (1
            notification per resource type) will be sent for
            a vulnerability that affects > 1 resource type.
        bulletin_id (str):
            The ID of the bulletin corresponding to the
            vulnerability.
        cve_ids (MutableSequence[str]):
            The CVEs associated with this bulletin.
        severity (str):
            The severity of this bulletin as it relates
            to GKE.
        bulletin_uri (str):
            The URI link to the bulletin on the website
            for more information.
        brief_description (str):
            A brief description of the bulletin. See the bulletin
            pointed to by the bulletin_uri field for an expanded
            description.
        affected_supported_minors (MutableSequence[str]):
            The GKE minor versions affected by this
            vulnerability.
        patched_versions (MutableSequence[str]):
            The GKE versions where this vulnerability is
            patched.
        suggested_upgrade_target (str):
            This represents a version selected from the patched_versions
            field that the cluster receiving this notification should
            most likely want to upgrade to based on its current version.
            Note that if this notification is being received by a given
            cluster, it means that this version is currently available
            as an upgrade target in that cluster's location.
        manual_steps_required (bool):
            If this field is specified, it means there
            are manual steps that the user must take to make
            their clusters safe.
    """

    resource_type_affected: str = proto.Field(
        proto.STRING,
        number=1,
    )
    bulletin_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cve_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    severity: str = proto.Field(
        proto.STRING,
        number=4,
    )
    bulletin_uri: str = proto.Field(
        proto.STRING,
        number=5,
    )
    brief_description: str = proto.Field(
        proto.STRING,
        number=6,
    )
    affected_supported_minors: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    patched_versions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=8,
    )
    suggested_upgrade_target: str = proto.Field(
        proto.STRING,
        number=9,
    )
    manual_steps_required: bool = proto.Field(
        proto.BOOL,
        number=10,
    )


class Autopilot(proto.Message):
    r"""Autopilot is the configuration for Autopilot settings on the
    cluster.

    Attributes:
        enabled (bool):
            Enable Autopilot
        workload_policy_config (google.cloud.container_v1.types.WorkloadPolicyConfig):
            Workload policy configuration for Autopilot.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    workload_policy_config: "WorkloadPolicyConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="WorkloadPolicyConfig",
    )


class WorkloadPolicyConfig(proto.Message):
    r"""WorkloadPolicyConfig is the configuration of workload policy
    for autopilot clusters.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        allow_net_admin (bool):
            If true, workloads can use NET_ADMIN capability.

            This field is a member of `oneof`_ ``_allow_net_admin``.
    """

    allow_net_admin: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )


class LoggingConfig(proto.Message):
    r"""LoggingConfig is cluster logging configuration.

    Attributes:
        component_config (google.cloud.container_v1.types.LoggingComponentConfig):
            Logging components configuration
    """

    component_config: "LoggingComponentConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="LoggingComponentConfig",
    )


class LoggingComponentConfig(proto.Message):
    r"""LoggingComponentConfig is cluster logging component
    configuration.

    Attributes:
        enable_components (MutableSequence[google.cloud.container_v1.types.LoggingComponentConfig.Component]):
            Select components to collect logs. An empty
            set would disable all logging.
    """

    class Component(proto.Enum):
        r"""GKE components exposing logs

        Values:
            COMPONENT_UNSPECIFIED (0):
                Default value. This shouldn't be used.
            SYSTEM_COMPONENTS (1):
                system components
            WORKLOADS (2):
                workloads
            APISERVER (3):
                kube-apiserver
            SCHEDULER (4):
                kube-scheduler
            CONTROLLER_MANAGER (5):
                kube-controller-manager
        """
        COMPONENT_UNSPECIFIED = 0
        SYSTEM_COMPONENTS = 1
        WORKLOADS = 2
        APISERVER = 3
        SCHEDULER = 4
        CONTROLLER_MANAGER = 5

    enable_components: MutableSequence[Component] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum=Component,
    )


class RayClusterLoggingConfig(proto.Message):
    r"""RayClusterLoggingConfig specifies configuration of Ray
    logging.

    Attributes:
        enabled (bool):
            Enable log collection for Ray clusters.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class MonitoringConfig(proto.Message):
    r"""MonitoringConfig is cluster monitoring configuration.

    Attributes:
        component_config (google.cloud.container_v1.types.MonitoringComponentConfig):
            Monitoring components configuration
        managed_prometheus_config (google.cloud.container_v1.types.ManagedPrometheusConfig):
            Enable Google Cloud Managed Service for
            Prometheus in the cluster.
        advanced_datapath_observability_config (google.cloud.container_v1.types.AdvancedDatapathObservabilityConfig):
            Configuration of Advanced Datapath
            Observability features.
    """

    component_config: "MonitoringComponentConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="MonitoringComponentConfig",
    )
    managed_prometheus_config: "ManagedPrometheusConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ManagedPrometheusConfig",
    )
    advanced_datapath_observability_config: "AdvancedDatapathObservabilityConfig" = (
        proto.Field(
            proto.MESSAGE,
            number=3,
            message="AdvancedDatapathObservabilityConfig",
        )
    )


class AdvancedDatapathObservabilityConfig(proto.Message):
    r"""AdvancedDatapathObservabilityConfig specifies configuration
    of observability features of advanced datapath.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        enable_metrics (bool):
            Expose flow metrics on nodes
        relay_mode (google.cloud.container_v1.types.AdvancedDatapathObservabilityConfig.RelayMode):
            Method used to make Relay available
        enable_relay (bool):
            Enable Relay component

            This field is a member of `oneof`_ ``_enable_relay``.
    """

    class RelayMode(proto.Enum):
        r"""Supported Relay modes

        Values:
            RELAY_MODE_UNSPECIFIED (0):
                Default value. This shouldn't be used.
            DISABLED (1):
                disabled
            INTERNAL_VPC_LB (3):
                exposed via internal load balancer
            EXTERNAL_LB (4):
                exposed via external load balancer
        """
        RELAY_MODE_UNSPECIFIED = 0
        DISABLED = 1
        INTERNAL_VPC_LB = 3
        EXTERNAL_LB = 4

    enable_metrics: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    relay_mode: RelayMode = proto.Field(
        proto.ENUM,
        number=2,
        enum=RelayMode,
    )
    enable_relay: bool = proto.Field(
        proto.BOOL,
        number=3,
        optional=True,
    )


class RayClusterMonitoringConfig(proto.Message):
    r"""RayClusterMonitoringConfig specifies monitoring configuration
    for Ray clusters.

    Attributes:
        enabled (bool):
            Enable metrics collection for Ray clusters.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class NodePoolLoggingConfig(proto.Message):
    r"""NodePoolLoggingConfig specifies logging configuration for
    nodepools.

    Attributes:
        variant_config (google.cloud.container_v1.types.LoggingVariantConfig):
            Logging variant configuration.
    """

    variant_config: "LoggingVariantConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="LoggingVariantConfig",
    )


class LoggingVariantConfig(proto.Message):
    r"""LoggingVariantConfig specifies the behaviour of the logging
    component.

    Attributes:
        variant (google.cloud.container_v1.types.LoggingVariantConfig.Variant):
            Logging variant deployed on nodes.
    """

    class Variant(proto.Enum):
        r"""Logging component variants.

        Values:
            VARIANT_UNSPECIFIED (0):
                Default value. This shouldn't be used.
            DEFAULT (1):
                default logging variant.
            MAX_THROUGHPUT (2):
                maximum logging throughput variant.
        """
        VARIANT_UNSPECIFIED = 0
        DEFAULT = 1
        MAX_THROUGHPUT = 2

    variant: Variant = proto.Field(
        proto.ENUM,
        number=1,
        enum=Variant,
    )


class MonitoringComponentConfig(proto.Message):
    r"""MonitoringComponentConfig is cluster monitoring component
    configuration.

    Attributes:
        enable_components (MutableSequence[google.cloud.container_v1.types.MonitoringComponentConfig.Component]):
            Select components to collect metrics. An
            empty set would disable all monitoring.
    """

    class Component(proto.Enum):
        r"""GKE components exposing metrics

        Values:
            COMPONENT_UNSPECIFIED (0):
                Default value. This shouldn't be used.
            SYSTEM_COMPONENTS (1):
                system components
            APISERVER (3):
                kube-apiserver
            SCHEDULER (4):
                kube-scheduler
            CONTROLLER_MANAGER (5):
                kube-controller-manager
            STORAGE (7):
                Storage
            HPA (8):
                Horizontal Pod Autoscaling
            POD (9):
                Pod
            DAEMONSET (10):
                DaemonSet
            DEPLOYMENT (11):
                Deployment
            STATEFULSET (12):
                Statefulset
            CADVISOR (13):
                CADVISOR
            KUBELET (14):
                KUBELET
            DCGM (15):
                NVIDIA Data Center GPU Manager (DCGM)
        """
        COMPONENT_UNSPECIFIED = 0
        SYSTEM_COMPONENTS = 1
        APISERVER = 3
        SCHEDULER = 4
        CONTROLLER_MANAGER = 5
        STORAGE = 7
        HPA = 8
        POD = 9
        DAEMONSET = 10
        DEPLOYMENT = 11
        STATEFULSET = 12
        CADVISOR = 13
        KUBELET = 14
        DCGM = 15

    enable_components: MutableSequence[Component] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum=Component,
    )


class ManagedPrometheusConfig(proto.Message):
    r"""ManagedPrometheusConfig defines the configuration for
    Google Cloud Managed Service for Prometheus.

    Attributes:
        enabled (bool):
            Enable Managed Collection.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class Fleet(proto.Message):
    r"""Fleet is the fleet configuration for the cluster.

    Attributes:
        project (str):
            The Fleet host project(project ID or project
            number) where this cluster will be registered
            to. This field cannot be changed after the
            cluster has been registered.
        membership (str):
            Output only. The full resource name of the registered fleet
            membership of the cluster, in the format
            ``//gkehub.googleapis.com/projects/*/locations/*/memberships/*``.
        pre_registered (bool):
            Output only. Whether the cluster has been
            registered through the fleet API.
    """

    project: str = proto.Field(
        proto.STRING,
        number=1,
    )
    membership: str = proto.Field(
        proto.STRING,
        number=2,
    )
    pre_registered: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class LocalNvmeSsdBlockConfig(proto.Message):
    r"""LocalNvmeSsdBlockConfig contains configuration for using
    raw-block local NVMe SSDs

    Attributes:
        local_ssd_count (int):
            Number of local NVMe SSDs to use. The limit for this value
            is dependent upon the maximum number of disk available on a
            machine per zone. See:
            https://cloud.google.com/compute/docs/disks/local-ssd for
            more information.

            A zero (or unset) value has different meanings depending on
            machine type being used:

            1. For pre-Gen3 machines, which support flexible numbers of
               local ssds, zero (or unset) means to disable using local
               SSDs as ephemeral storage.
            2. For Gen3 machines which dictate a specific number of
               local ssds, zero (or unset) means to use the default
               number of local ssds that goes with that machine type.
               For example, for a c3-standard-8-lssd machine, 2 local
               ssds would be provisioned. For c3-standard-8 (which
               doesn't support local ssds), 0 will be provisioned. See
               https://cloud.google.com/compute/docs/disks/local-ssd#choose_number_local_ssds
               for more info.
    """

    local_ssd_count: int = proto.Field(
        proto.INT32,
        number=1,
    )


class EphemeralStorageLocalSsdConfig(proto.Message):
    r"""EphemeralStorageLocalSsdConfig contains configuration for the
    node ephemeral storage using Local SSDs.

    Attributes:
        local_ssd_count (int):
            Number of local SSDs to use to back ephemeral storage. Uses
            NVMe interfaces.

            A zero (or unset) value has different meanings depending on
            machine type being used:

            1. For pre-Gen3 machines, which support flexible numbers of
               local ssds, zero (or unset) means to disable using local
               SSDs as ephemeral storage. The limit for this value is
               dependent upon the maximum number of disk available on a
               machine per zone. See:
               https://cloud.google.com/compute/docs/disks/local-ssd for
               more information.
            2. For Gen3 machines which dictate a specific number of
               local ssds, zero (or unset) means to use the default
               number of local ssds that goes with that machine type.
               For example, for a c3-standard-8-lssd machine, 2 local
               ssds would be provisioned. For c3-standard-8 (which
               doesn't support local ssds), 0 will be provisioned. See
               https://cloud.google.com/compute/docs/disks/local-ssd#choose_number_local_ssds
               for more info.
    """

    local_ssd_count: int = proto.Field(
        proto.INT32,
        number=1,
    )


class ResourceManagerTags(proto.Message):
    r"""A map of resource manager tag keys and values to be attached
    to the nodes for managing Compute Engine firewalls using Network
    Firewall Policies. Tags must be according to specifications in
    https://cloud.google.com/vpc/docs/tags-firewalls-overview#specifications.
    A maximum of 5 tag key-value pairs can be specified. Existing
    tags will be replaced with new values.

    Attributes:
        tags (MutableMapping[str, str]):
            TagKeyValue must be in one of the following formats
            ([KEY]=[VALUE])

            1. ``tagKeys/{tag_key_id}=tagValues/{tag_value_id}``
            2. ``{org_id}/{tag_key_name}={tag_value_name}``
            3. ``{project_id}/{tag_key_name}={tag_value_name}``
    """

    tags: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )


class EnterpriseConfig(proto.Message):
    r"""EnterpriseConfig is the cluster enterprise configuration.

    Attributes:
        cluster_tier (google.cloud.container_v1.types.EnterpriseConfig.ClusterTier):
            Output only. cluster_tier specifies the premium tier of the
            cluster.
    """

    class ClusterTier(proto.Enum):
        r"""Premium tiers for GKE Cluster.

        Values:
            CLUSTER_TIER_UNSPECIFIED (0):
                CLUSTER_TIER_UNSPECIFIED is when cluster_tier is not set.
            STANDARD (1):
                STANDARD indicates a standard GKE cluster.
            ENTERPRISE (2):
                ENTERPRISE indicates a GKE Enterprise
                cluster.
        """
        CLUSTER_TIER_UNSPECIFIED = 0
        STANDARD = 1
        ENTERPRISE = 2

    cluster_tier: ClusterTier = proto.Field(
        proto.ENUM,
        number=1,
        enum=ClusterTier,
    )


class SecondaryBootDisk(proto.Message):
    r"""SecondaryBootDisk represents a persistent disk attached to a
    node with special configurations based on its mode.

    Attributes:
        mode (google.cloud.container_v1.types.SecondaryBootDisk.Mode):
            Disk mode (container image cache, etc.)
        disk_image (str):
            Fully-qualified resource ID for an existing
            disk image.
    """

    class Mode(proto.Enum):
        r"""Mode specifies how the secondary boot disk will be used.
        This triggers mode-specified logic in the control plane.

        Values:
            MODE_UNSPECIFIED (0):
                MODE_UNSPECIFIED is when mode is not set.
            CONTAINER_IMAGE_CACHE (1):
                CONTAINER_IMAGE_CACHE is for using the secondary boot disk
                as a container image cache.
        """
        MODE_UNSPECIFIED = 0
        CONTAINER_IMAGE_CACHE = 1

    mode: Mode = proto.Field(
        proto.ENUM,
        number=1,
        enum=Mode,
    )
    disk_image: str = proto.Field(
        proto.STRING,
        number=2,
    )


class SecondaryBootDiskUpdateStrategy(proto.Message):
    r"""SecondaryBootDiskUpdateStrategy is a placeholder which will
    be extended in the future to define different options for
    updating secondary boot disks.

    """


__all__ = tuple(sorted(__protobuf__.manifest))
