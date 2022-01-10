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
    },
)


class Component(proto.Enum):
    r"""Cluster components that can be activated."""
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
        properties (Sequence[google.cloud.dataproc_v1.types.RuntimeConfig.PropertiesEntry]):
            Optional. A mapping of property names to
            values, which are used to configure workload
            execution.
    """

    version = proto.Field(proto.STRING, number=1,)
    container_image = proto.Field(proto.STRING, number=2,)
    properties = proto.MapField(proto.STRING, proto.STRING, number=3,)


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

    execution_config = proto.Field(proto.MESSAGE, number=1, message="ExecutionConfig",)
    peripherals_config = proto.Field(
        proto.MESSAGE, number=2, message="PeripheralsConfig",
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
        network_tags (Sequence[str]):
            Optional. Tags used for network traffic
            control.
        kms_key (str):
            Optional. The Cloud KMS key to use for
            encryption.
    """

    service_account = proto.Field(proto.STRING, number=2,)
    network_uri = proto.Field(proto.STRING, number=4, oneof="network",)
    subnetwork_uri = proto.Field(proto.STRING, number=5, oneof="network",)
    network_tags = proto.RepeatedField(proto.STRING, number=6,)
    kms_key = proto.Field(proto.STRING, number=7,)


class SparkHistoryServerConfig(proto.Message):
    r"""Spark History Server configuration for the workload.

    Attributes:
        dataproc_cluster (str):
            Optional. Resource name of an existing Dataproc Cluster to
            act as a Spark History Server for the workload.

            Example:

            -  ``projects/[project_id]/regions/[region]/clusters/[cluster_name]``
    """

    dataproc_cluster = proto.Field(proto.STRING, number=1,)


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

    metastore_service = proto.Field(proto.STRING, number=1,)
    spark_history_server_config = proto.Field(
        proto.MESSAGE, number=2, message="SparkHistoryServerConfig",
    )


class RuntimeInfo(proto.Message):
    r"""Runtime information about workload execution.

    Attributes:
        endpoints (Sequence[google.cloud.dataproc_v1.types.RuntimeInfo.EndpointsEntry]):
            Output only. Map of remote access endpoints
            (such as web interfaces and APIs) to their URIs.
        output_uri (str):
            Output only. A URI pointing to the location
            of the stdout and stderr of the workload.
        diagnostic_output_uri (str):
            Output only. A URI pointing to the location
            of the diagnostics tarball.
    """

    endpoints = proto.MapField(proto.STRING, proto.STRING, number=1,)
    output_uri = proto.Field(proto.STRING, number=2,)
    diagnostic_output_uri = proto.Field(proto.STRING, number=3,)


__all__ = tuple(sorted(__protobuf__.manifest))
