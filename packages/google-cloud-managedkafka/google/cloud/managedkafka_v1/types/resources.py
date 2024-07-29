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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.managedkafka.v1",
    manifest={
        "Cluster",
        "CapacityConfig",
        "RebalanceConfig",
        "NetworkConfig",
        "AccessConfig",
        "GcpConfig",
        "Topic",
        "ConsumerTopicMetadata",
        "ConsumerPartitionMetadata",
        "ConsumerGroup",
        "OperationMetadata",
    },
)


class Cluster(proto.Message):
    r"""An Apache Kafka cluster deployed in a location.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcp_config (google.cloud.managedkafka_v1.types.GcpConfig):
            Required. Configuration properties for a
            Kafka cluster deployed to Google Cloud Platform.

            This field is a member of `oneof`_ ``platform_config``.
        name (str):
            Identifier. The name of the cluster. Structured like:
            projects/{project_number}/locations/{location}/clusters/{cluster_id}
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the cluster was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the cluster was
            last updated.
        labels (MutableMapping[str, str]):
            Optional. Labels as key value pairs.
        capacity_config (google.cloud.managedkafka_v1.types.CapacityConfig):
            Required. Capacity configuration for the
            Kafka cluster.
        rebalance_config (google.cloud.managedkafka_v1.types.RebalanceConfig):
            Optional. Rebalance configuration for the
            Kafka cluster.
        state (google.cloud.managedkafka_v1.types.Cluster.State):
            Output only. The current state of the
            cluster.
    """

    class State(proto.Enum):
        r"""The state of the cluster.

        Values:
            STATE_UNSPECIFIED (0):
                A state was not specified.
            CREATING (1):
                The cluster is being created.
            ACTIVE (2):
                The cluster is active.
            DELETING (3):
                The cluster is being deleted.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        DELETING = 3

    gcp_config: "GcpConfig" = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="platform_config",
        message="GcpConfig",
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
    capacity_config: "CapacityConfig" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="CapacityConfig",
    )
    rebalance_config: "RebalanceConfig" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="RebalanceConfig",
    )
    state: State = proto.Field(
        proto.ENUM,
        number=10,
        enum=State,
    )


class CapacityConfig(proto.Message):
    r"""A capacity configuration of a Kafka cluster.

    Attributes:
        vcpu_count (int):
            Required. The number of vCPUs to provision
            for the cluster. Minimum: 3.
        memory_bytes (int):
            Required. The memory to provision for the
            cluster in bytes. The CPU:memory ratio
            (vCPU:GiB) must be between 1:1 and 1:8. Minimum:
            3221225472 (3 GiB).
    """

    vcpu_count: int = proto.Field(
        proto.INT64,
        number=1,
    )
    memory_bytes: int = proto.Field(
        proto.INT64,
        number=2,
    )


class RebalanceConfig(proto.Message):
    r"""Defines rebalancing behavior of a Kafka cluster.

    Attributes:
        mode (google.cloud.managedkafka_v1.types.RebalanceConfig.Mode):
            Optional. The rebalance behavior for the cluster. When not
            specified, defaults to ``NO_REBALANCE``.
    """

    class Mode(proto.Enum):
        r"""The partition rebalance mode for the cluster.

        Values:
            MODE_UNSPECIFIED (0):
                A mode was not specified. Do not use.
            NO_REBALANCE (1):
                Do not rebalance automatically.
            AUTO_REBALANCE_ON_SCALE_UP (2):
                Automatically rebalance topic partitions
                among brokers when the cluster is scaled up.
        """
        MODE_UNSPECIFIED = 0
        NO_REBALANCE = 1
        AUTO_REBALANCE_ON_SCALE_UP = 2

    mode: Mode = proto.Field(
        proto.ENUM,
        number=1,
        enum=Mode,
    )


class NetworkConfig(proto.Message):
    r"""The configuration of a Virtual Private Cloud (VPC) network
    that can access the Kafka cluster.

    Attributes:
        subnet (str):
            Required. Name of the VPC subnet in which to create Private
            Service Connect (PSC) endpoints for the Kafka brokers and
            bootstrap address. Structured like:
            projects/{project}/regions/{region}/subnetworks/{subnet_id}

            The subnet must be located in the same region as the Kafka
            cluster. The project may differ. Multiple subnets from the
            same parent network must not be specified.

            The CIDR range of the subnet must be within the IPv4 address
            ranges for private networks, as specified in RFC 1918.
    """

    subnet: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AccessConfig(proto.Message):
    r"""The configuration of access to the Kafka cluster.

    Attributes:
        network_configs (MutableSequence[google.cloud.managedkafka_v1.types.NetworkConfig]):
            Required. Virtual Private Cloud (VPC)
            networks that must be granted direct access to
            the Kafka cluster. Minimum of 1 network is
            required. Maximum 10 networks can be specified.
    """

    network_configs: MutableSequence["NetworkConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="NetworkConfig",
    )


class GcpConfig(proto.Message):
    r"""Configuration properties for a Kafka cluster deployed to
    Google Cloud Platform.

    Attributes:
        access_config (google.cloud.managedkafka_v1.types.AccessConfig):
            Required. Access configuration for the Kafka
            cluster.
        kms_key (str):
            Optional. Immutable. The Cloud KMS Key name to use for
            encryption. The key must be located in the same region as
            the cluster and cannot be changed. Structured like:
            projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}.
    """

    access_config: "AccessConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="AccessConfig",
    )
    kms_key: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Topic(proto.Message):
    r"""A Kafka topic in a given cluster.

    Attributes:
        name (str):
            Identifier. The name of the topic. The ``topic`` segment is
            used when connecting directly to the cluster. Structured
            like:
            projects/{project}/locations/{location}/clusters/{cluster}/topics/{topic}
        partition_count (int):
            Required. The number of partitions this topic
            has. The partition count can only be increased,
            not decreased. Please note that if partitions
            are increased for a topic that has a key, the
            partitioning logic or the ordering of the
            messages will be affected.
        replication_factor (int):
            Required. Immutable. The number of replicas
            of each partition. A replication factor of 3 is
            recommended for high availability.
        configs (MutableMapping[str, str]):
            Optional. Configurations for the topic that are overridden
            from the cluster defaults. The key of the map is a Kafka
            topic property name, for example: ``cleanup.policy``,
            ``compression.type``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    partition_count: int = proto.Field(
        proto.INT32,
        number=2,
    )
    replication_factor: int = proto.Field(
        proto.INT32,
        number=3,
    )
    configs: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )


class ConsumerTopicMetadata(proto.Message):
    r"""Metadata for a consumer group corresponding to a specific
    topic.

    Attributes:
        partitions (MutableMapping[int, google.cloud.managedkafka_v1.types.ConsumerPartitionMetadata]):
            Optional. Metadata for this consumer group
            and topic for all partition indexes it has
            metadata for.
    """

    partitions: MutableMapping[int, "ConsumerPartitionMetadata"] = proto.MapField(
        proto.INT32,
        proto.MESSAGE,
        number=1,
        message="ConsumerPartitionMetadata",
    )


class ConsumerPartitionMetadata(proto.Message):
    r"""Metadata for a consumer group corresponding to a specific
    partition.

    Attributes:
        offset (int):
            Required. The offset for this partition, or 0
            if no offset has been committed.
        metadata (str):
            Optional. The associated metadata for this
            partition, or empty if it does not exist.
    """

    offset: int = proto.Field(
        proto.INT64,
        number=1,
    )
    metadata: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ConsumerGroup(proto.Message):
    r"""A Kafka consumer group in a given cluster.

    Attributes:
        name (str):
            Identifier. The name of the consumer group. The
            ``consumer_group`` segment is used when connecting directly
            to the cluster. Structured like:
            projects/{project}/locations/{location}/clusters/{cluster}/consumerGroups/{consumer_group}
        topics (MutableMapping[str, google.cloud.managedkafka_v1.types.ConsumerTopicMetadata]):
            Optional. Metadata for this consumer group
            for all topics it has metadata for. The key of
            the map is a topic name, structured like:

            projects/{project}/locations/{location}/clusters/{cluster}/topics/{topic}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    topics: MutableMapping[str, "ConsumerTopicMetadata"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=2,
        message="ConsumerTopicMetadata",
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have been
            cancelled successfully have [Operation.error][] value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
