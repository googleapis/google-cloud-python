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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.gkemulticloud.v1",
    manifest={
        "WorkloadIdentityConfig",
        "MaxPodsConstraint",
        "OperationMetadata",
        "NodeTaint",
        "Fleet",
        "LoggingConfig",
        "LoggingComponentConfig",
    },
)


class WorkloadIdentityConfig(proto.Message):
    r"""Workload Identity settings.

    Attributes:
        issuer_uri (str):
            The OIDC issuer URL for this cluster.
        workload_pool (str):
            The Workload Identity Pool associated to the
            cluster.
        identity_provider (str):
            The ID of the OIDC Identity Provider (IdP)
            associated to the Workload Identity Pool.
    """

    issuer_uri = proto.Field(
        proto.STRING,
        number=1,
    )
    workload_pool = proto.Field(
        proto.STRING,
        number=2,
    )
    identity_provider = proto.Field(
        proto.STRING,
        number=3,
    )


class MaxPodsConstraint(proto.Message):
    r"""Constraints applied to pods.

    Attributes:
        max_pods_per_node (int):
            Required. The maximum number of pods to
            schedule on a single node.
    """

    max_pods_per_node = proto.Field(
        proto.INT64,
        number=1,
    )


class OperationMetadata(proto.Message):
    r"""Metadata about a long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this operation
            was created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this operation
            was completed.
        target (str):
            Output only. The name of the resource
            associated to this operation.
        status_detail (str):
            Output only. Human-readable status of the
            operation, if any.
        error_detail (str):
            Output only. Human-readable status of any
            error that occurred during the operation.
    """

    create_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target = proto.Field(
        proto.STRING,
        number=3,
    )
    status_detail = proto.Field(
        proto.STRING,
        number=4,
    )
    error_detail = proto.Field(
        proto.STRING,
        number=5,
    )


class NodeTaint(proto.Message):
    r"""The taint content for the node taint.

    Attributes:
        key (str):
            Required. Key for the taint.
        value (str):
            Required. Value for the taint.
        effect (google.cloud.gke_multicloud_v1.types.NodeTaint.Effect):
            Required. The taint effect.
    """

    class Effect(proto.Enum):
        r"""The taint effect."""
        EFFECT_UNSPECIFIED = 0
        NO_SCHEDULE = 1
        PREFER_NO_SCHEDULE = 2
        NO_EXECUTE = 3

    key = proto.Field(
        proto.STRING,
        number=1,
    )
    value = proto.Field(
        proto.STRING,
        number=2,
    )
    effect = proto.Field(
        proto.ENUM,
        number=3,
        enum=Effect,
    )


class Fleet(proto.Message):
    r"""Fleet related configuration.

    Fleets are a Google Cloud concept for logically organizing clusters,
    letting you use and manage multi-cluster capabilities and apply
    consistent policies across your systems.

    See `Anthos
    Fleets <https://cloud.google.com/anthos/multicluster-management/fleets>`__
    for more details on Anthos multi-cluster capabilities using Fleets.

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

    project = proto.Field(
        proto.STRING,
        number=1,
    )
    membership = proto.Field(
        proto.STRING,
        number=2,
    )


class LoggingConfig(proto.Message):
    r"""Parameters that describe the Logging configuration in a
    cluster.

    Attributes:
        component_config (google.cloud.gke_multicloud_v1.types.LoggingComponentConfig):
            The configuration of the logging components;
    """

    component_config = proto.Field(
        proto.MESSAGE,
        number=1,
        message="LoggingComponentConfig",
    )


class LoggingComponentConfig(proto.Message):
    r"""Parameters that describe the Logging component configuration
    in a cluster.

    Attributes:
        enable_components (Sequence[google.cloud.gke_multicloud_v1.types.LoggingComponentConfig.Component]):
            The components to be enabled.
    """

    class Component(proto.Enum):
        r"""The components of the logging configuration;"""
        COMPONENT_UNSPECIFIED = 0
        SYSTEM_COMPONENTS = 1
        WORKLOADS = 2

    enable_components = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum=Component,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
