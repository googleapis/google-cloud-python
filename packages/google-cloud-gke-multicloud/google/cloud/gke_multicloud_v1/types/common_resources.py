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
    package="google.cloud.gkemulticloud.v1",
    manifest={
        "Jwk",
        "WorkloadIdentityConfig",
        "MaxPodsConstraint",
        "OperationMetadata",
        "NodeTaint",
        "Fleet",
        "LoggingConfig",
        "LoggingComponentConfig",
        "MonitoringConfig",
        "ManagedPrometheusConfig",
        "BinaryAuthorization",
    },
)


class Jwk(proto.Message):
    r"""Jwk is a JSON Web Key as specified in RFC 7517.

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

    issuer_uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    workload_pool: str = proto.Field(
        proto.STRING,
        number=2,
    )
    identity_provider: str = proto.Field(
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

    max_pods_per_node: int = proto.Field(
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
        verb (str):
            Output only. The verb associated with the API
            method which triggered this operation. Possible
            values are "create", "delete", "update" and
            "import".
        requested_cancellation (bool):
            Output only. Identifies whether it has been requested
            cancellation for the operation. Operations that have
            successfully been cancelled have [Operation.error][] value
            with a [google.rpc.Status.code][google.rpc.Status.code] of
            1, corresponding to ``Code.CANCELLED``.
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
    status_detail: str = proto.Field(
        proto.STRING,
        number=4,
    )
    error_detail: str = proto.Field(
        proto.STRING,
        number=5,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=7,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
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
        r"""The taint effect.

        Values:
            EFFECT_UNSPECIFIED (0):
                Not set.
            NO_SCHEDULE (1):
                Do not allow new pods to schedule onto the
                node unless they tolerate the taint, but allow
                all pods submitted to Kubelet without going
                through the scheduler to start, and allow all
                already-running pods to continue running.
                Enforced by the scheduler.
            PREFER_NO_SCHEDULE (2):
                Like TaintEffectNoSchedule, but the scheduler
                tries not to schedule new pods onto the node,
                rather than prohibiting new pods from scheduling
                onto the node entirely. Enforced by the
                scheduler.
            NO_EXECUTE (3):
                Evict any already-running pods that do not
                tolerate the taint. Currently enforced by
                NodeController.
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

    project: str = proto.Field(
        proto.STRING,
        number=1,
    )
    membership: str = proto.Field(
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

    component_config: "LoggingComponentConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="LoggingComponentConfig",
    )


class LoggingComponentConfig(proto.Message):
    r"""Parameters that describe the Logging component configuration
    in a cluster.

    Attributes:
        enable_components (MutableSequence[google.cloud.gke_multicloud_v1.types.LoggingComponentConfig.Component]):
            The components to be enabled.
    """

    class Component(proto.Enum):
        r"""The components of the logging configuration;

        Values:
            COMPONENT_UNSPECIFIED (0):
                No component is specified
            SYSTEM_COMPONENTS (1):
                This indicates that system logging components
                is enabled.
            WORKLOADS (2):
                This indicates that user workload logging
                component is enabled.
        """
        COMPONENT_UNSPECIFIED = 0
        SYSTEM_COMPONENTS = 1
        WORKLOADS = 2

    enable_components: MutableSequence[Component] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum=Component,
    )


class MonitoringConfig(proto.Message):
    r"""Parameters that describe the Monitoring configuration in a
    cluster.

    Attributes:
        managed_prometheus_config (google.cloud.gke_multicloud_v1.types.ManagedPrometheusConfig):
            Enable Google Cloud Managed Service for
            Prometheus in the cluster.
    """

    managed_prometheus_config: "ManagedPrometheusConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ManagedPrometheusConfig",
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


class BinaryAuthorization(proto.Message):
    r"""Configuration for Binary Authorization.

    Attributes:
        evaluation_mode (google.cloud.gke_multicloud_v1.types.BinaryAuthorization.EvaluationMode):
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
                singleton policy.
        """
        EVALUATION_MODE_UNSPECIFIED = 0
        DISABLED = 1
        PROJECT_SINGLETON_POLICY_ENFORCE = 2

    evaluation_mode: EvaluationMode = proto.Field(
        proto.ENUM,
        number=1,
        enum=EvaluationMode,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
