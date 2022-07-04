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

from google.cloud.gke_multicloud_v1.types import common_resources
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.gkemulticloud.v1",
    manifest={
        "AzureCluster",
        "AzureClusterNetworking",
        "AzureControlPlane",
        "ReplicaPlacement",
        "AzureProxyConfig",
        "AzureDatabaseEncryption",
        "AzureConfigEncryption",
        "AzureDiskTemplate",
        "AzureClient",
        "AzureAuthorization",
        "AzureClusterUser",
        "AzureNodePool",
        "AzureNodeConfig",
        "AzureNodePoolAutoscaling",
        "AzureServerConfig",
        "AzureK8sVersionInfo",
        "AzureSshConfig",
        "AzureClusterResources",
    },
)


class AzureCluster(proto.Message):
    r"""An Anthos cluster running on Azure.

    Attributes:
        name (str):
            The name of this resource.

            Cluster names are formatted as
            ``projects/<project-number>/locations/<region>/azureClusters/<cluster-id>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on GCP resource names.
        description (str):
            Optional. A human readable description of
            this cluster. Cannot be longer than 255 UTF-8
            encoded bytes.
        azure_region (str):
            Required. The Azure region where the cluster runs.

            Each Google Cloud region supports a subset of nearby Azure
            regions. You can call
            [GetAzureServerConfig][google.cloud.gkemulticloud.v1.AzureClusters.GetAzureServerConfig]
            to list all supported Azure regions within a given Google
            Cloud region.
        resource_group_id (str):
            Required. The ARM ID of the resource group where the cluster
            resources are deployed. For example:
            ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>``
        azure_client (str):
            Required. Name of the
            [AzureClient][google.cloud.gkemulticloud.v1.AzureClient]
            that contains authentication configuration for how the
            Anthos Multi-Cloud API connects to Azure APIs.

            The ``AzureClient`` resource must reside on the same GCP
            project and region as the ``AzureCluster``.

            ``AzureClient`` names are formatted as
            ``projects/<project-number>/locations/<region>/azureClients/<client-id>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud resource names.
        networking (google.cloud.gke_multicloud_v1.types.AzureClusterNetworking):
            Required. Cluster-wide networking
            configuration.
        control_plane (google.cloud.gke_multicloud_v1.types.AzureControlPlane):
            Required. Configuration related to the
            cluster control plane.
        authorization (google.cloud.gke_multicloud_v1.types.AzureAuthorization):
            Required. Configuration related to the
            cluster RBAC settings.
        state (google.cloud.gke_multicloud_v1.types.AzureCluster.State):
            Output only. The current state of the
            cluster.
        endpoint (str):
            Output only. The endpoint of the cluster's
            API server.
        uid (str):
            Output only. A globally unique identifier for
            the cluster.
        reconciling (bool):
            Output only. If set, there are currently
            changes in flight to the cluster.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this cluster
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this cluster
            was last updated.
        etag (str):
            Allows clients to perform consistent
            read-modify-writes through optimistic
            concurrency control.
            Can be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
        annotations (Mapping[str, str]):
            Optional. Annotations on the cluster.

            This field has the same restrictions as Kubernetes
            annotations. The total size of all keys and values combined
            is limited to 256k. Keys can have 2 segments: prefix
            (optional) and name (required), separated by a slash (/).
            Prefix must be a DNS subdomain. Name must be 63 characters
            or less, begin and end with alphanumerics, with dashes (-),
            underscores (_), dots (.), and alphanumerics between.
        workload_identity_config (google.cloud.gke_multicloud_v1.types.WorkloadIdentityConfig):
            Output only. Workload Identity settings.
        cluster_ca_certificate (str):
            Output only. PEM encoded x509 certificate of
            the cluster root of trust.
        fleet (google.cloud.gke_multicloud_v1.types.Fleet):
            Optional. Fleet configuration.
        managed_resources (google.cloud.gke_multicloud_v1.types.AzureClusterResources):
            Output only. Mananged Azure resources for
            this cluster.
        logging_config (google.cloud.gke_multicloud_v1.types.LoggingConfig):
            Optional. Logging configuration for this
            cluster.
    """

    class State(proto.Enum):
        r"""The lifecycle state of the cluster."""
        STATE_UNSPECIFIED = 0
        PROVISIONING = 1
        RUNNING = 2
        RECONCILING = 3
        STOPPING = 4
        ERROR = 5
        DEGRADED = 6

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    description = proto.Field(
        proto.STRING,
        number=2,
    )
    azure_region = proto.Field(
        proto.STRING,
        number=3,
    )
    resource_group_id = proto.Field(
        proto.STRING,
        number=17,
    )
    azure_client = proto.Field(
        proto.STRING,
        number=16,
    )
    networking = proto.Field(
        proto.MESSAGE,
        number=4,
        message="AzureClusterNetworking",
    )
    control_plane = proto.Field(
        proto.MESSAGE,
        number=5,
        message="AzureControlPlane",
    )
    authorization = proto.Field(
        proto.MESSAGE,
        number=6,
        message="AzureAuthorization",
    )
    state = proto.Field(
        proto.ENUM,
        number=7,
        enum=State,
    )
    endpoint = proto.Field(
        proto.STRING,
        number=8,
    )
    uid = proto.Field(
        proto.STRING,
        number=9,
    )
    reconciling = proto.Field(
        proto.BOOL,
        number=10,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=11,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=12,
        message=timestamp_pb2.Timestamp,
    )
    etag = proto.Field(
        proto.STRING,
        number=13,
    )
    annotations = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=14,
    )
    workload_identity_config = proto.Field(
        proto.MESSAGE,
        number=18,
        message=common_resources.WorkloadIdentityConfig,
    )
    cluster_ca_certificate = proto.Field(
        proto.STRING,
        number=19,
    )
    fleet = proto.Field(
        proto.MESSAGE,
        number=20,
        message=common_resources.Fleet,
    )
    managed_resources = proto.Field(
        proto.MESSAGE,
        number=21,
        message="AzureClusterResources",
    )
    logging_config = proto.Field(
        proto.MESSAGE,
        number=23,
        message=common_resources.LoggingConfig,
    )


class AzureClusterNetworking(proto.Message):
    r"""ClusterNetworking contains cluster-wide networking
    configuration.

    Attributes:
        virtual_network_id (str):
            Required. The Azure Resource Manager (ARM) ID of the VNet
            associated with your cluster.

            All components in the cluster (i.e. control plane and node
            pools) run on a single VNet.

            Example:
            ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-id>/providers/Microsoft.Network/virtualNetworks/<vnet-id>``

            This field cannot be changed after creation.
        pod_address_cidr_blocks (Sequence[str]):
            Required. The IP address range of the pods in this cluster,
            in CIDR notation (e.g. ``10.96.0.0/14``).

            All pods in the cluster get assigned a unique IPv4 address
            from these ranges. Only a single range is supported.

            This field cannot be changed after creation.
        service_address_cidr_blocks (Sequence[str]):
            Required. The IP address range for services in this cluster,
            in CIDR notation (e.g. ``10.96.0.0/14``).

            All services in the cluster get assigned a unique IPv4
            address from these ranges. Only a single range is supported.

            This field cannot be changed after creating a cluster.
        service_load_balancer_subnet_id (str):
            Optional. The ARM ID of the subnet where Kubernetes private
            service type load balancers are deployed. When unspecified,
            it defaults to AzureControlPlane.subnet_id.

            Example:
            "/subscriptions/d00494d6-6f3c-4280-bbb2-899e163d1d30/resourceGroups/anthos_cluster_gkeust4/providers/Microsoft.Network/virtualNetworks/gke-vnet-gkeust4/subnets/subnetid456".
    """

    virtual_network_id = proto.Field(
        proto.STRING,
        number=1,
    )
    pod_address_cidr_blocks = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    service_address_cidr_blocks = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    service_load_balancer_subnet_id = proto.Field(
        proto.STRING,
        number=5,
    )


class AzureControlPlane(proto.Message):
    r"""AzureControlPlane represents the control plane
    configurations.

    Attributes:
        version (str):
            Required. The Kubernetes version to run on control plane
            replicas (e.g. ``1.19.10-gke.1000``).

            You can list all supported versions on a given Google Cloud
            region by calling
            [GetAzureServerConfig][google.cloud.gkemulticloud.v1.AzureClusters.GetAzureServerConfig].
        subnet_id (str):
            Optional. The ARM ID of the default subnet for the control
            plane. The control plane VMs are deployed in this subnet,
            unless ``AzureControlPlane.replica_placements`` is
            specified. This subnet will also be used as default for
            ``AzureControlPlane.endpoint_subnet_id`` if
            ``AzureControlPlane.endpoint_subnet_id`` is not specified.
            Similarly it will be used as default for
            ``AzureClusterNetworking.service_load_balancer_subnet_id``.

            Example:
            ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-id>/providers/Microsoft.Network/virtualNetworks/<vnet-id>/subnets/default``.
        vm_size (str):
            Optional. The Azure VM size name. Example:
            ``Standard_DS2_v2``.

            For available VM sizes, see
            https://docs.microsoft.com/en-us/azure/virtual-machines/vm-naming-conventions.

            When unspecified, it defaults to ``Standard_DS2_v2``.
        ssh_config (google.cloud.gke_multicloud_v1.types.AzureSshConfig):
            Required. SSH configuration for how to access
            the underlying control plane machines.
        root_volume (google.cloud.gke_multicloud_v1.types.AzureDiskTemplate):
            Optional. Configuration related to the root
            volume provisioned for each control plane
            replica.
            When unspecified, it defaults to 32-GiB Azure
            Disk.
        main_volume (google.cloud.gke_multicloud_v1.types.AzureDiskTemplate):
            Optional. Configuration related to the main
            volume provisioned for each control plane
            replica. The main volume is in charge of storing
            all of the cluster's etcd state.
            When unspecified, it defaults to a 8-GiB Azure
            Disk.
        database_encryption (google.cloud.gke_multicloud_v1.types.AzureDatabaseEncryption):
            Optional. Configuration related to
            application-layer secrets encryption.
        proxy_config (google.cloud.gke_multicloud_v1.types.AzureProxyConfig):
            Optional. Proxy configuration for outbound
            HTTP(S) traffic.
        config_encryption (google.cloud.gke_multicloud_v1.types.AzureConfigEncryption):
            Optional. Configuration related to vm config
            encryption.
        tags (Mapping[str, str]):
            Optional. A set of tags to apply to all
            underlying control plane Azure resources.
        replica_placements (Sequence[google.cloud.gke_multicloud_v1.types.ReplicaPlacement]):
            Optional. Configuration for where to place the control plane
            replicas.

            Up to three replica placement instances can be specified. If
            replica_placements is set, the replica placement instances
            will be applied to the three control plane replicas as
            evenly as possible.
        endpoint_subnet_id (str):
            Optional. The ARM ID of the subnet where the control plane
            load balancer is deployed. When unspecified, it defaults to
            AzureControlPlane.subnet_id.

            Example:
            "/subscriptions/d00494d6-6f3c-4280-bbb2-899e163d1d30/resourceGroups/anthos_cluster_gkeust4/providers/Microsoft.Network/virtualNetworks/gke-vnet-gkeust4/subnets/subnetid123".
    """

    version = proto.Field(
        proto.STRING,
        number=1,
    )
    subnet_id = proto.Field(
        proto.STRING,
        number=2,
    )
    vm_size = proto.Field(
        proto.STRING,
        number=3,
    )
    ssh_config = proto.Field(
        proto.MESSAGE,
        number=11,
        message="AzureSshConfig",
    )
    root_volume = proto.Field(
        proto.MESSAGE,
        number=4,
        message="AzureDiskTemplate",
    )
    main_volume = proto.Field(
        proto.MESSAGE,
        number=5,
        message="AzureDiskTemplate",
    )
    database_encryption = proto.Field(
        proto.MESSAGE,
        number=10,
        message="AzureDatabaseEncryption",
    )
    proxy_config = proto.Field(
        proto.MESSAGE,
        number=12,
        message="AzureProxyConfig",
    )
    config_encryption = proto.Field(
        proto.MESSAGE,
        number=14,
        message="AzureConfigEncryption",
    )
    tags = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    replica_placements = proto.RepeatedField(
        proto.MESSAGE,
        number=13,
        message="ReplicaPlacement",
    )
    endpoint_subnet_id = proto.Field(
        proto.STRING,
        number=15,
    )


class ReplicaPlacement(proto.Message):
    r"""Configuration for the placement of a control plane replica.

    Attributes:
        subnet_id (str):
            Required. For a given replica, the ARM ID of
            the subnet where the control plane VM is
            deployed. Make sure it's a subnet under the
            virtual network in the cluster configuration.
        azure_availability_zone (str):
            Required. For a given replica, the Azure
            availability zone where to provision the control
            plane VM and the ETCD disk.
    """

    subnet_id = proto.Field(
        proto.STRING,
        number=1,
    )
    azure_availability_zone = proto.Field(
        proto.STRING,
        number=2,
    )


class AzureProxyConfig(proto.Message):
    r"""Details of a proxy config stored in Azure Key Vault.

    Attributes:
        resource_group_id (str):
            The ARM ID the of the resource group containing proxy
            keyvault.

            Resource group ids are formatted as
            ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>``.
        secret_id (str):
            The URL the of the proxy setting secret with its version.

            Secret ids are formatted as
            ``https://<key-vault-name>.vault.azure.net/secrets/<secret-name>/<secret-version>``.
    """

    resource_group_id = proto.Field(
        proto.STRING,
        number=1,
    )
    secret_id = proto.Field(
        proto.STRING,
        number=2,
    )


class AzureDatabaseEncryption(proto.Message):
    r"""Configuration related to application-layer secrets
    encryption.
    Anthos clusters on Azure encrypts your Kubernetes data at rest
    in etcd using Azure Key Vault.

    Attributes:
        key_id (str):
            Required. The ARM ID of the Azure Key Vault key to encrypt /
            decrypt data.

            For example:
            ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-id>/providers/Microsoft.KeyVault/vaults/<key-vault-id>/keys/<key-name>``
            Encryption will always take the latest version of the key
            and hence specific version is not supported.
    """

    key_id = proto.Field(
        proto.STRING,
        number=3,
    )


class AzureConfigEncryption(proto.Message):
    r"""Configuration related to config data encryption.
    Azure VM bootstrap secret is envelope encrypted with the
    provided key vault key.

    Attributes:
        key_id (str):
            Required. The ARM ID of the Azure Key Vault key to encrypt /
            decrypt config data.

            For example:
            ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-id>/providers/Microsoft.KeyVault/vaults/<key-vault-id>/keys/<key-name>``
        public_key (str):
            Optional. RSA key of the Azure Key Vault
            public key to use for encrypting the data.
            This key must be formatted as a PEM-encoded
            SubjectPublicKeyInfo (RFC 5280) in ASN.1 DER
            form. The string must be comprised of a single
            PEM block of type "PUBLIC KEY".
    """

    key_id = proto.Field(
        proto.STRING,
        number=2,
    )
    public_key = proto.Field(
        proto.STRING,
        number=3,
    )


class AzureDiskTemplate(proto.Message):
    r"""Configuration for Azure Disks.

    Attributes:
        size_gib (int):
            Optional. The size of the disk, in GiBs.
            When unspecified, a default value is provided.
            See the specific reference in the parent
            resource.
    """

    size_gib = proto.Field(
        proto.INT32,
        number=1,
    )


class AzureClient(proto.Message):
    r"""``AzureClient`` resources hold client authentication information
    needed by the Anthos Multi-Cloud API to manage Azure resources on
    your Azure subscription.

    When an [AzureCluster][google.cloud.gkemulticloud.v1.AzureCluster]
    is created, an ``AzureClient`` resource needs to be provided and all
    operations on Azure resources associated to that cluster will
    authenticate to Azure services using the given client.

    ``AzureClient`` resources are immutable and cannot be modified upon
    creation.

    Each ``AzureClient`` resource is bound to a single Azure Active
    Directory Application and tenant.

    Attributes:
        name (str):
            The name of this resource.

            ``AzureClient`` resource names are formatted as
            ``projects/<project-number>/locations/<region>/azureClients/<client-id>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud resource names.
        tenant_id (str):
            Required. The Azure Active Directory Tenant
            ID.
        application_id (str):
            Required. The Azure Active Directory
            Application ID.
        annotations (Mapping[str, str]):
            Optional. Annotations on the resource.

            This field has the same restrictions as Kubernetes
            annotations. The total size of all keys and values combined
            is limited to 256k. Keys can have 2 segments: prefix
            (optional) and name (required), separated by a slash (/).
            Prefix must be a DNS subdomain. Name must be 63 characters
            or less, begin and end with alphanumerics, with dashes (-),
            underscores (_), dots (.), and alphanumerics between.
        pem_certificate (str):
            Output only. The PEM encoded x509
            certificate.
        uid (str):
            Output only. A globally unique identifier for
            the client.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this resource
            was created.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    tenant_id = proto.Field(
        proto.STRING,
        number=2,
    )
    application_id = proto.Field(
        proto.STRING,
        number=3,
    )
    annotations = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=8,
    )
    pem_certificate = proto.Field(
        proto.STRING,
        number=7,
    )
    uid = proto.Field(
        proto.STRING,
        number=5,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )


class AzureAuthorization(proto.Message):
    r"""Configuration related to the cluster RBAC settings.

    Attributes:
        admin_users (Sequence[google.cloud.gke_multicloud_v1.types.AzureClusterUser]):
            Required. Users that can perform operations as a cluster
            admin. A managed ClusterRoleBinding will be created to grant
            the ``cluster-admin`` ClusterRole to the users. Up to ten
            admin users can be provided.

            For more info on RBAC, see
            https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles
    """

    admin_users = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AzureClusterUser",
    )


class AzureClusterUser(proto.Message):
    r"""Identities of a user-type subject for Azure clusters.

    Attributes:
        username (str):
            Required. The name of the user, e.g.
            ``my-gcp-id@gmail.com``.
    """

    username = proto.Field(
        proto.STRING,
        number=1,
    )


class AzureNodePool(proto.Message):
    r"""An Anthos node pool running on Azure.

    Attributes:
        name (str):
            The name of this resource.

            Node pool names are formatted as
            ``projects/<project-number>/locations/<region>/azureClusters/<cluster-id>/azureNodePools/<node-pool-id>``.

            For more details on Google Cloud resource names, see
            `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
        version (str):
            Required. The Kubernetes version (e.g. ``1.19.10-gke.1000``)
            running on this node pool.
        config (google.cloud.gke_multicloud_v1.types.AzureNodeConfig):
            Required. The node configuration of the node
            pool.
        subnet_id (str):
            Required. The ARM ID of the subnet where the
            node pool VMs run. Make sure it's a subnet under
            the virtual network in the cluster
            configuration.
        autoscaling (google.cloud.gke_multicloud_v1.types.AzureNodePoolAutoscaling):
            Required. Autoscaler configuration for this
            node pool.
        state (google.cloud.gke_multicloud_v1.types.AzureNodePool.State):
            Output only. The current state of the node
            pool.
        uid (str):
            Output only. A globally unique identifier for
            the node pool.
        reconciling (bool):
            Output only. If set, there are currently
            pending changes to the node pool.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this node pool
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this node pool
            was last updated.
        etag (str):
            Allows clients to perform consistent
            read-modify-writes through optimistic
            concurrency control.
            Can be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
        annotations (Mapping[str, str]):
            Optional. Annotations on the node pool.

            This field has the same restrictions as Kubernetes
            annotations. The total size of all keys and values combined
            is limited to 256k. Keys can have 2 segments: prefix
            (optional) and name (required), separated by a slash (/).
            Prefix must be a DNS subdomain. Name must be 63 characters
            or less, begin and end with alphanumerics, with dashes (-),
            underscores (_), dots (.), and alphanumerics between.
        max_pods_constraint (google.cloud.gke_multicloud_v1.types.MaxPodsConstraint):
            Required. The constraint on the maximum
            number of pods that can be run simultaneously on
            a node in the node pool.
        azure_availability_zone (str):
            Optional. The Azure availability zone of the nodes in this
            nodepool.

            When unspecified, it defaults to ``1``.
    """

    class State(proto.Enum):
        r"""The lifecycle state of the node pool."""
        STATE_UNSPECIFIED = 0
        PROVISIONING = 1
        RUNNING = 2
        RECONCILING = 3
        STOPPING = 4
        ERROR = 5
        DEGRADED = 6

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    version = proto.Field(
        proto.STRING,
        number=2,
    )
    config = proto.Field(
        proto.MESSAGE,
        number=22,
        message="AzureNodeConfig",
    )
    subnet_id = proto.Field(
        proto.STRING,
        number=3,
    )
    autoscaling = proto.Field(
        proto.MESSAGE,
        number=4,
        message="AzureNodePoolAutoscaling",
    )
    state = proto.Field(
        proto.ENUM,
        number=6,
        enum=State,
    )
    uid = proto.Field(
        proto.STRING,
        number=8,
    )
    reconciling = proto.Field(
        proto.BOOL,
        number=9,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=11,
        message=timestamp_pb2.Timestamp,
    )
    etag = proto.Field(
        proto.STRING,
        number=12,
    )
    annotations = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=13,
    )
    max_pods_constraint = proto.Field(
        proto.MESSAGE,
        number=21,
        message=common_resources.MaxPodsConstraint,
    )
    azure_availability_zone = proto.Field(
        proto.STRING,
        number=23,
    )


class AzureNodeConfig(proto.Message):
    r"""Parameters that describe the configuration of all node
    machines on a given node pool.

    Attributes:
        vm_size (str):
            Optional. The Azure VM size name. Example:
            ``Standard_DS2_v2``.

            See `Supported VM
            sizes </anthos/clusters/docs/azure/reference/supported-vms>`__
            for options.

            When unspecified, it defaults to ``Standard_DS2_v2``.
        root_volume (google.cloud.gke_multicloud_v1.types.AzureDiskTemplate):
            Optional. Configuration related to the root
            volume provisioned for each node pool machine.
            When unspecified, it defaults to a 32-GiB Azure
            Disk.
        tags (Mapping[str, str]):
            Optional. A set of tags to apply to all underlying Azure
            resources for this node pool. This currently only includes
            Virtual Machine Scale Sets.

            Specify at most 50 pairs containing alphanumerics, spaces,
            and symbols (.+-=_:@/). Keys can be up to 127 Unicode
            characters. Values can be up to 255 Unicode characters.
        image_type (str):
            Optional. The OS image type to use on node pool instances.
            Can have a value of ``ubuntu``, or ``windows`` if the
            cluster enables the Windows node pool preview feature.

            When unspecified, it defaults to ``ubuntu``.
        ssh_config (google.cloud.gke_multicloud_v1.types.AzureSshConfig):
            Required. SSH configuration for how to access
            the node pool machines.
        proxy_config (google.cloud.gke_multicloud_v1.types.AzureProxyConfig):
            Optional. Proxy configuration for outbound
            HTTP(S) traffic.
        config_encryption (google.cloud.gke_multicloud_v1.types.AzureConfigEncryption):
            Optional. Configuration related to vm config
            encryption.
        taints (Sequence[google.cloud.gke_multicloud_v1.types.NodeTaint]):
            Optional. The initial taints assigned to
            nodes of this node pool.
        labels (Mapping[str, str]):
            Optional. The initial labels assigned to
            nodes of this node pool. An object containing a
            list of "key": value pairs. Example: { "name":
            "wrench", "mass": "1.3kg", "count": "3" }.
    """

    vm_size = proto.Field(
        proto.STRING,
        number=1,
    )
    root_volume = proto.Field(
        proto.MESSAGE,
        number=2,
        message="AzureDiskTemplate",
    )
    tags = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )
    image_type = proto.Field(
        proto.STRING,
        number=8,
    )
    ssh_config = proto.Field(
        proto.MESSAGE,
        number=7,
        message="AzureSshConfig",
    )
    proxy_config = proto.Field(
        proto.MESSAGE,
        number=9,
        message="AzureProxyConfig",
    )
    config_encryption = proto.Field(
        proto.MESSAGE,
        number=12,
        message="AzureConfigEncryption",
    )
    taints = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message=common_resources.NodeTaint,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=11,
    )


class AzureNodePoolAutoscaling(proto.Message):
    r"""Configuration related to Kubernetes cluster autoscaler.
    The Kubernetes cluster autoscaler will automatically adjust the
    size of the node pool based on the cluster load.

    Attributes:
        min_node_count (int):
            Required. Minimum number of nodes in the node pool. Must be
            greater than or equal to 1 and less than or equal to
            max_node_count.
        max_node_count (int):
            Required. Maximum number of nodes in the node pool. Must be
            greater than or equal to min_node_count and less than or
            equal to 50.
    """

    min_node_count = proto.Field(
        proto.INT32,
        number=1,
    )
    max_node_count = proto.Field(
        proto.INT32,
        number=2,
    )


class AzureServerConfig(proto.Message):
    r"""AzureServerConfig contains information about a Google Cloud
    location, such as supported Azure regions and Kubernetes
    versions.

    Attributes:
        name (str):
            The ``AzureServerConfig`` resource name.

            ``AzureServerConfig`` names are formatted as
            ``projects/<project-number>/locations/<region>/azureServerConfig``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on GCP resource names.
        valid_versions (Sequence[google.cloud.gke_multicloud_v1.types.AzureK8sVersionInfo]):
            List of valid Kubernetes versions.
        supported_azure_regions (Sequence[str]):
            The list of supported Azure regions.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    valid_versions = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="AzureK8sVersionInfo",
    )
    supported_azure_regions = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class AzureK8sVersionInfo(proto.Message):
    r"""Information about a supported Kubernetes version.

    Attributes:
        version (str):
            A supported Kubernetes version (for example,
            ``1.19.10-gke.1000``)
    """

    version = proto.Field(
        proto.STRING,
        number=1,
    )


class AzureSshConfig(proto.Message):
    r"""SSH configuration for Azure resources.

    Attributes:
        authorized_key (str):
            Required. The SSH public key data for VMs managed by Anthos.
            This accepts the authorized_keys file format used in OpenSSH
            according to the sshd(8) manual page.
    """

    authorized_key = proto.Field(
        proto.STRING,
        number=1,
    )


class AzureClusterResources(proto.Message):
    r"""Managed Azure resources for the cluster.
    The values could change and be empty, depending on the state of
    the cluster.

    Attributes:
        network_security_group_id (str):
            Output only. The ARM ID of the cluster
            network security group.
        control_plane_application_security_group_id (str):
            Output only. The ARM ID of the control plane
            application security group.
    """

    network_security_group_id = proto.Field(
        proto.STRING,
        number=1,
    )
    control_plane_application_security_group_id = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
