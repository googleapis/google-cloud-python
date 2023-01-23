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
from typing import MutableMapping, MutableSequence

import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dataproc.v1",
    manifest={
        "Component",
        "FailureAction",
        "RuntimeConfig",
        "EnvironmentConfig",
        "ExecutionConfig",
        "SparkHistoryServerConfig",
        "PeripheralsConfig",
        "RuntimeInfo",
        "GkeClusterConfig",
        "KubernetesClusterConfig",
        "KubernetesSoftwareConfig",
        "GkeNodePoolTarget",
        "GkeNodePoolConfig",
    },
)


class Component(proto.Enum):
    r"""Cluster components that can be activated.

    Values:
        COMPONENT_UNSPECIFIED (0):
            Unspecified component. Specifying this will
            cause Cluster creation to fail.
        ANACONDA (5):
            The Anaconda python distribution. The
            Anaconda component is not supported in the
            Dataproc <a
            href="/dataproc/docs/concepts/versioning/dataproc-release-2.0">2.0
            image</a>. The 2.0 image is pre-installed with
            Miniconda.
        DOCKER (13):
            Docker
        DRUID (9):
            The Druid query engine. (alpha)
        FLINK (14):
            Flink
        HBASE (11):
            HBase. (beta)
        HIVE_WEBHCAT (3):
            The Hive Web HCatalog (the REST service for
            accessing HCatalog).
        JUPYTER (1):
            The Jupyter Notebook.
        PRESTO (6):
            The Presto query engine.
        RANGER (12):
            The Ranger service.
        SOLR (10):
            The Solr service.
        ZEPPELIN (4):
            The Zeppelin notebook.
        ZOOKEEPER (8):
            The Zookeeper service.
    """
    COMPONENT_UNSPECIFIED = 0
    ANACONDA = 5
    DOCKER = 13
    DRUID = 9
    FLINK = 14
    HBASE = 11
    HIVE_WEBHCAT = 3
    JUPYTER = 1
    PRESTO = 6
    RANGER = 12
    SOLR = 10
    ZEPPELIN = 4
    ZOOKEEPER = 8


class FailureAction(proto.Enum):
    r"""Actions in response to failure of a resource associated with
    a cluster.

    Values:
        FAILURE_ACTION_UNSPECIFIED (0):
            When FailureAction is unspecified, failure action defaults
            to NO_ACTION.
        NO_ACTION (1):
            Take no action on failure to create a cluster resource.
            NO_ACTION is the default.
        DELETE (2):
            Delete the failed cluster resource.
    """
    FAILURE_ACTION_UNSPECIFIED = 0
    NO_ACTION = 1
    DELETE = 2


class RuntimeConfig(proto.Message):
    r"""Runtime configuration for a workload.

    Attributes:
        version (str):
            Optional. Version of the batch runtime.
        container_image (str):
            Optional. Optional custom container image for
            the job runtime environment. If not specified, a
            default container image will be used.
        properties (MutableMapping[str, str]):
            Optional. A mapping of property names to
            values, which are used to configure workload
            execution.
    """

    version: str = proto.Field(
        proto.STRING,
        number=1,
    )
    container_image: str = proto.Field(
        proto.STRING,
        number=2,
    )
    properties: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )


class EnvironmentConfig(proto.Message):
    r"""Environment configuration for a workload.

    Attributes:
        execution_config (google.cloud.dataproc_v1.types.ExecutionConfig):
            Optional. Execution configuration for a
            workload.
        peripherals_config (google.cloud.dataproc_v1.types.PeripheralsConfig):
            Optional. Peripherals configuration that
            workload has access to.
    """

    execution_config: "ExecutionConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ExecutionConfig",
    )
    peripherals_config: "PeripheralsConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="PeripheralsConfig",
    )


class ExecutionConfig(proto.Message):
    r"""Execution configuration for a workload.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        service_account (str):
            Optional. Service account that used to
            execute workload.
        network_uri (str):
            Optional. Network URI to connect workload to.

            This field is a member of `oneof`_ ``network``.
        subnetwork_uri (str):
            Optional. Subnetwork URI to connect workload
            to.

            This field is a member of `oneof`_ ``network``.
        network_tags (MutableSequence[str]):
            Optional. Tags used for network traffic
            control.
        kms_key (str):
            Optional. The Cloud KMS key to use for
            encryption.
    """

    service_account: str = proto.Field(
        proto.STRING,
        number=2,
    )
    network_uri: str = proto.Field(
        proto.STRING,
        number=4,
        oneof="network",
    )
    subnetwork_uri: str = proto.Field(
        proto.STRING,
        number=5,
        oneof="network",
    )
    network_tags: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    kms_key: str = proto.Field(
        proto.STRING,
        number=7,
    )


class SparkHistoryServerConfig(proto.Message):
    r"""Spark History Server configuration for the workload.

    Attributes:
        dataproc_cluster (str):
            Optional. Resource name of an existing Dataproc Cluster to
            act as a Spark History Server for the workload.

            Example:

            -  ``projects/[project_id]/regions/[region]/clusters/[cluster_name]``
    """

    dataproc_cluster: str = proto.Field(
        proto.STRING,
        number=1,
    )


class PeripheralsConfig(proto.Message):
    r"""Auxiliary services configuration for a workload.

    Attributes:
        metastore_service (str):
            Optional. Resource name of an existing Dataproc Metastore
            service.

            Example:

            -  ``projects/[project_id]/locations/[region]/services/[service_id]``
        spark_history_server_config (google.cloud.dataproc_v1.types.SparkHistoryServerConfig):
            Optional. The Spark History Server
            configuration for the workload.
    """

    metastore_service: str = proto.Field(
        proto.STRING,
        number=1,
    )
    spark_history_server_config: "SparkHistoryServerConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="SparkHistoryServerConfig",
    )


class RuntimeInfo(proto.Message):
    r"""Runtime information about workload execution.

    Attributes:
        endpoints (MutableMapping[str, str]):
            Output only. Map of remote access endpoints
            (such as web interfaces and APIs) to their URIs.
        output_uri (str):
            Output only. A URI pointing to the location
            of the stdout and stderr of the workload.
        diagnostic_output_uri (str):
            Output only. A URI pointing to the location
            of the diagnostics tarball.
    """

    endpoints: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )
    output_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    diagnostic_output_uri: str = proto.Field(
        proto.STRING,
        number=3,
    )


class GkeClusterConfig(proto.Message):
    r"""The cluster's GKE config.

    Attributes:
        gke_cluster_target (str):
            Optional. A target GKE cluster to deploy to. It must be in
            the same project and region as the Dataproc cluster (the GKE
            cluster can be zonal or regional). Format:
            'projects/{project}/locations/{location}/clusters/{cluster_id}'
        node_pool_target (MutableSequence[google.cloud.dataproc_v1.types.GkeNodePoolTarget]):
            Optional. GKE NodePools where workloads will
            be scheduled. At least one node pool must be
            assigned the 'default' role. Each role can be
            given to only a single NodePoolTarget. All
            NodePools must have the same location settings.
            If a nodePoolTarget is not specified, Dataproc
            constructs a default nodePoolTarget.
    """

    gke_cluster_target: str = proto.Field(
        proto.STRING,
        number=2,
    )
    node_pool_target: MutableSequence["GkeNodePoolTarget"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="GkeNodePoolTarget",
    )


class KubernetesClusterConfig(proto.Message):
    r"""The configuration for running the Dataproc cluster on
    Kubernetes.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        kubernetes_namespace (str):
            Optional. A namespace within the Kubernetes
            cluster to deploy into. If this namespace does
            not exist, it is created. If it exists, Dataproc
            verifies that another Dataproc VirtualCluster is
            not installed into it. If not specified, the
            name of the Dataproc Cluster is used.
        gke_cluster_config (google.cloud.dataproc_v1.types.GkeClusterConfig):
            Required. The configuration for running the
            Dataproc cluster on GKE.

            This field is a member of `oneof`_ ``config``.
        kubernetes_software_config (google.cloud.dataproc_v1.types.KubernetesSoftwareConfig):
            Optional. The software configuration for this
            Dataproc cluster running on Kubernetes.
    """

    kubernetes_namespace: str = proto.Field(
        proto.STRING,
        number=1,
    )
    gke_cluster_config: "GkeClusterConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="config",
        message="GkeClusterConfig",
    )
    kubernetes_software_config: "KubernetesSoftwareConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="KubernetesSoftwareConfig",
    )


class KubernetesSoftwareConfig(proto.Message):
    r"""The software configuration for this Dataproc cluster running
    on Kubernetes.

    Attributes:
        component_version (MutableMapping[str, str]):
            The components that should be installed in
            this Dataproc cluster. The key must be a string
            from the KubernetesComponent enumeration. The
            value is the version of the software to be
            installed.
            At least one entry must be specified.
        properties (MutableMapping[str, str]):
            The properties to set on daemon config files.

            Property keys are specified in ``prefix:property`` format,
            for example ``spark:spark.kubernetes.container.image``. The
            following are supported prefixes and their mappings:

            -  spark: ``spark-defaults.conf``

            For more information, see `Cluster
            properties <https://cloud.google.com/dataproc/docs/concepts/cluster-properties>`__.
    """

    component_version: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )
    properties: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )


class GkeNodePoolTarget(proto.Message):
    r"""GKE NodePools that Dataproc workloads run on.

    Attributes:
        node_pool (str):
            Required. The target GKE NodePool. Format:
            'projects/{project}/locations/{location}/clusters/{cluster}/nodePools/{node_pool}'
        roles (MutableSequence[google.cloud.dataproc_v1.types.GkeNodePoolTarget.Role]):
            Required. The types of role for a GKE
            NodePool
        node_pool_config (google.cloud.dataproc_v1.types.GkeNodePoolConfig):
            Optional. The configuration for the GKE
            NodePool.
            If specified, Dataproc attempts to create a
            NodePool with the specified shape. If one with
            the same name already exists, it is verified
            against all specified fields. If a field
            differs, the virtual cluster creation will fail.

            If omitted, any NodePool with the specified name
            is used. If a NodePool with the specified name
            does not exist, Dataproc create a NodePool with
            default values.
    """

    class Role(proto.Enum):
        r"""``Role`` specifies whose tasks will run on the NodePool. The roles
        can be specific to workloads. Exactly one GkeNodePoolTarget within
        the VirtualCluster must have 'default' role, which is used to run
        all workloads that are not associated with a NodePool.

        Values:
            ROLE_UNSPECIFIED (0):
                Role is unspecified.
            DEFAULT (1):
                Any roles that are not directly assigned to a NodePool run
                on the ``default`` role's NodePool.
            CONTROLLER (2):
                Run controllers and webhooks.
            SPARK_DRIVER (3):
                Run spark driver.
            SPARK_EXECUTOR (4):
                Run spark executors.
        """
        ROLE_UNSPECIFIED = 0
        DEFAULT = 1
        CONTROLLER = 2
        SPARK_DRIVER = 3
        SPARK_EXECUTOR = 4

    node_pool: str = proto.Field(
        proto.STRING,
        number=1,
    )
    roles: MutableSequence[Role] = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum=Role,
    )
    node_pool_config: "GkeNodePoolConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="GkeNodePoolConfig",
    )


class GkeNodePoolConfig(proto.Message):
    r"""The configuration of a GKE NodePool used by a `Dataproc-on-GKE
    cluster <https://cloud.google.com/dataproc/docs/concepts/jobs/dataproc-gke#create-a-dataproc-on-gke-cluster>`__.

    Attributes:
        config (google.cloud.dataproc_v1.types.GkeNodePoolConfig.GkeNodeConfig):
            Optional. The node pool configuration.
        locations (MutableSequence[str]):
            Optional. The list of Compute Engine
            `zones <https://cloud.google.com/compute/docs/zones#available>`__
            where NodePool's nodes will be located.

            **Note:** Currently, only one zone may be specified.

            If a location is not specified during NodePool creation,
            Dataproc will choose a location.
        autoscaling (google.cloud.dataproc_v1.types.GkeNodePoolConfig.GkeNodePoolAutoscalingConfig):
            Optional. The autoscaler configuration for
            this NodePool. The autoscaler is enabled only
            when a valid configuration is present.
    """

    class GkeNodeConfig(proto.Message):
        r"""Parameters that describe cluster nodes.

        Attributes:
            machine_type (str):
                Optional. The name of a Compute Engine `machine
                type <https://cloud.google.com/compute/docs/machine-types>`__.
            preemptible (bool):
                Optional. Whether the nodes are created as `preemptible VM
                instances <https://cloud.google.com/compute/docs/instances/preemptible>`__.
            local_ssd_count (int):
                Optional. The number of local SSD disks to attach to the
                node, which is limited by the maximum number of disks
                allowable per zone (see `Adding Local
                SSDs <https://cloud.google.com/compute/docs/disks/local-ssd>`__).
            accelerators (MutableSequence[google.cloud.dataproc_v1.types.GkeNodePoolConfig.GkeNodePoolAcceleratorConfig]):
                Optional. A list of `hardware
                accelerators <https://cloud.google.com/compute/docs/gpus>`__
                to attach to each node.
            min_cpu_platform (str):
                Optional. `Minimum CPU
                platform <https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform>`__
                to be used by this instance. The instance may be scheduled
                on the specified or a newer CPU platform. Specify the
                friendly names of CPU platforms, such as "Intel Haswell"\`
                or Intel Sandy Bridge".
        """

        machine_type: str = proto.Field(
            proto.STRING,
            number=1,
        )
        preemptible: bool = proto.Field(
            proto.BOOL,
            number=10,
        )
        local_ssd_count: int = proto.Field(
            proto.INT32,
            number=7,
        )
        accelerators: MutableSequence[
            "GkeNodePoolConfig.GkeNodePoolAcceleratorConfig"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=11,
            message="GkeNodePoolConfig.GkeNodePoolAcceleratorConfig",
        )
        min_cpu_platform: str = proto.Field(
            proto.STRING,
            number=13,
        )

    class GkeNodePoolAcceleratorConfig(proto.Message):
        r"""A GkeNodeConfigAcceleratorConfig represents a Hardware
        Accelerator request for a NodePool.

        Attributes:
            accelerator_count (int):
                The number of accelerator cards exposed to an
                instance.
            accelerator_type (str):
                The accelerator type resource namename (see
                GPUs on Compute Engine).
        """

        accelerator_count: int = proto.Field(
            proto.INT64,
            number=1,
        )
        accelerator_type: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class GkeNodePoolAutoscalingConfig(proto.Message):
        r"""GkeNodePoolAutoscaling contains information the cluster
        autoscaler needs to adjust the size of the node pool to the
        current cluster usage.

        Attributes:
            min_node_count (int):
                The minimum number of nodes in the NodePool. Must be >= 0
                and <= max_node_count.
            max_node_count (int):
                The maximum number of nodes in the NodePool. Must be >=
                min_node_count. **Note:** Quota must be sufficient to scale
                up the cluster.
        """

        min_node_count: int = proto.Field(
            proto.INT32,
            number=2,
        )
        max_node_count: int = proto.Field(
            proto.INT32,
            number=3,
        )

    config: GkeNodeConfig = proto.Field(
        proto.MESSAGE,
        number=2,
        message=GkeNodeConfig,
    )
    locations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=13,
    )
    autoscaling: GkeNodePoolAutoscalingConfig = proto.Field(
        proto.MESSAGE,
        number=4,
        message=GkeNodePoolAutoscalingConfig,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
