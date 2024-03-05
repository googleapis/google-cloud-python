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

from google.cloud.gke_multicloud_v1.types import common_resources

__protobuf__ = proto.module(
    package="google.cloud.gkemulticloud.v1",
    manifest={
        "AttachedCluster",
        "AttachedClustersAuthorization",
        "AttachedClusterUser",
        "AttachedClusterGroup",
        "AttachedOidcConfig",
        "AttachedServerConfig",
        "AttachedPlatformVersionInfo",
        "AttachedClusterError",
        "AttachedProxyConfig",
        "KubernetesSecret",
    },
)


class AttachedCluster(proto.Message):
    r"""An Anthos cluster running on customer own infrastructure.

    Attributes:
        name (str):
            The name of this resource.

            Cluster names are formatted as
            ``projects/<project-number>/locations/<region>/attachedClusters/<cluster-id>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud Platform resource names.
        description (str):
            Optional. A human readable description of
            this cluster. Cannot be longer than 255 UTF-8
            encoded bytes.
        oidc_config (google.cloud.gke_multicloud_v1.types.AttachedOidcConfig):
            Required. OpenID Connect (OIDC) configuration
            for the cluster.
        platform_version (str):
            Required. The platform version for the cluster (e.g.
            ``1.19.0-gke.1000``).

            You can list all supported versions on a given Google Cloud
            region by calling
            [GetAttachedServerConfig][google.cloud.gkemulticloud.v1.AttachedClusters.GetAttachedServerConfig].
        distribution (str):
            Required. The Kubernetes distribution of the underlying
            attached cluster.

            Supported values: ["eks", "aks", "generic"].
        cluster_region (str):
            Output only. The region where this cluster
            runs.
            For EKS clusters, this is a AWS region. For AKS
            clusters, this is an Azure region.
        fleet (google.cloud.gke_multicloud_v1.types.Fleet):
            Required. Fleet configuration.
        state (google.cloud.gke_multicloud_v1.types.AttachedCluster.State):
            Output only. The current state of the
            cluster.
        uid (str):
            Output only. A globally unique identifier for
            the cluster.
        reconciling (bool):
            Output only. If set, there are currently
            changes in flight to the cluster.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this cluster
            was registered.
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
        kubernetes_version (str):
            Output only. The Kubernetes version of the
            cluster.
        annotations (MutableMapping[str, str]):
            Optional. Annotations on the cluster.

            This field has the same restrictions as Kubernetes
            annotations. The total size of all keys and values combined
            is limited to 256k. Key can have 2 segments: prefix
            (optional) and name (required), separated by a slash (/).
            Prefix must be a DNS subdomain. Name must be 63 characters
            or less, begin and end with alphanumerics, with dashes (-),
            underscores (_), dots (.), and alphanumerics between.
        workload_identity_config (google.cloud.gke_multicloud_v1.types.WorkloadIdentityConfig):
            Output only. Workload Identity settings.
        logging_config (google.cloud.gke_multicloud_v1.types.LoggingConfig):
            Optional. Logging configuration for this
            cluster.
        errors (MutableSequence[google.cloud.gke_multicloud_v1.types.AttachedClusterError]):
            Output only. A set of errors found in the
            cluster.
        authorization (google.cloud.gke_multicloud_v1.types.AttachedClustersAuthorization):
            Optional. Configuration related to the
            cluster RBAC settings.
        monitoring_config (google.cloud.gke_multicloud_v1.types.MonitoringConfig):
            Optional. Monitoring configuration for this
            cluster.
        proxy_config (google.cloud.gke_multicloud_v1.types.AttachedProxyConfig):
            Optional. Proxy configuration for outbound
            HTTP(S) traffic.
        binary_authorization (google.cloud.gke_multicloud_v1.types.BinaryAuthorization):
            Optional. Binary Authorization configuration
            for this cluster.
    """

    class State(proto.Enum):
        r"""The lifecycle state of the cluster.

        Values:
            STATE_UNSPECIFIED (0):
                Not set.
            PROVISIONING (1):
                The PROVISIONING state indicates the cluster
                is being registered.
            RUNNING (2):
                The RUNNING state indicates the cluster has
                been register and is fully usable.
            RECONCILING (3):
                The RECONCILING state indicates that some
                work is actively being done on the cluster, such
                as upgrading software components.
            STOPPING (4):
                The STOPPING state indicates the cluster is
                being de-registered.
            ERROR (5):
                The ERROR state indicates the cluster is in a
                broken unrecoverable state.
            DEGRADED (6):
                The DEGRADED state indicates the cluster
                requires user action to restore full
                functionality.
        """
        STATE_UNSPECIFIED = 0
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
    oidc_config: "AttachedOidcConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="AttachedOidcConfig",
    )
    platform_version: str = proto.Field(
        proto.STRING,
        number=4,
    )
    distribution: str = proto.Field(
        proto.STRING,
        number=16,
    )
    cluster_region: str = proto.Field(
        proto.STRING,
        number=22,
    )
    fleet: common_resources.Fleet = proto.Field(
        proto.MESSAGE,
        number=5,
        message=common_resources.Fleet,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=6,
        enum=State,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=7,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=11,
    )
    kubernetes_version: str = proto.Field(
        proto.STRING,
        number=12,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=13,
    )
    workload_identity_config: common_resources.WorkloadIdentityConfig = proto.Field(
        proto.MESSAGE,
        number=14,
        message=common_resources.WorkloadIdentityConfig,
    )
    logging_config: common_resources.LoggingConfig = proto.Field(
        proto.MESSAGE,
        number=15,
        message=common_resources.LoggingConfig,
    )
    errors: MutableSequence["AttachedClusterError"] = proto.RepeatedField(
        proto.MESSAGE,
        number=20,
        message="AttachedClusterError",
    )
    authorization: "AttachedClustersAuthorization" = proto.Field(
        proto.MESSAGE,
        number=21,
        message="AttachedClustersAuthorization",
    )
    monitoring_config: common_resources.MonitoringConfig = proto.Field(
        proto.MESSAGE,
        number=23,
        message=common_resources.MonitoringConfig,
    )
    proxy_config: "AttachedProxyConfig" = proto.Field(
        proto.MESSAGE,
        number=24,
        message="AttachedProxyConfig",
    )
    binary_authorization: common_resources.BinaryAuthorization = proto.Field(
        proto.MESSAGE,
        number=25,
        message=common_resources.BinaryAuthorization,
    )


class AttachedClustersAuthorization(proto.Message):
    r"""Configuration related to the cluster RBAC settings.

    Attributes:
        admin_users (MutableSequence[google.cloud.gke_multicloud_v1.types.AttachedClusterUser]):
            Optional. Users that can perform operations as a cluster
            admin. A managed ClusterRoleBinding will be created to grant
            the ``cluster-admin`` ClusterRole to the users. Up to ten
            admin users can be provided.

            For more info on RBAC, see
            https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles
        admin_groups (MutableSequence[google.cloud.gke_multicloud_v1.types.AttachedClusterGroup]):
            Optional. Groups of users that can perform operations as a
            cluster admin. A managed ClusterRoleBinding will be created
            to grant the ``cluster-admin`` ClusterRole to the groups. Up
            to ten admin groups can be provided.

            For more info on RBAC, see
            https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles
    """

    admin_users: MutableSequence["AttachedClusterUser"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AttachedClusterUser",
    )
    admin_groups: MutableSequence["AttachedClusterGroup"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="AttachedClusterGroup",
    )


class AttachedClusterUser(proto.Message):
    r"""Identities of a user-type subject for Attached clusters.

    Attributes:
        username (str):
            Required. The name of the user, e.g.
            ``my-gcp-id@gmail.com``.
    """

    username: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AttachedClusterGroup(proto.Message):
    r"""Identities of a group-type subject for Attached clusters.

    Attributes:
        group (str):
            Required. The name of the group, e.g.
            ``my-group@domain.com``.
    """

    group: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AttachedOidcConfig(proto.Message):
    r"""OIDC discovery information of the target cluster.

    Kubernetes Service Account (KSA) tokens are JWT tokens signed by the
    cluster API server. This fields indicates how Google Cloud Platform
    services validate KSA tokens in order to allow system workloads
    (such as GKE Connect and telemetry agents) to authenticate back to
    Google Cloud Platform.

    Both clusters with public and private issuer URLs are supported.
    Clusters with public issuers only need to specify the ``issuer_url``
    field while clusters with private issuers need to provide both
    ``issuer_url`` and ``oidc_jwks``.

    Attributes:
        issuer_url (str):
            A JSON Web Token (JWT) issuer URI. ``issuer`` must start
            with ``https://``.
        jwks (bytes):
            Optional. OIDC verification keys in JWKS
            format (RFC 7517). It contains a list of OIDC
            verification keys that can be used to verify
            OIDC JWTs.

            This field is required for cluster that doesn't
            have a publicly available discovery endpoint.
            When provided, it will be directly used to
            verify the OIDC JWT asserted by the IDP.
    """

    issuer_url: str = proto.Field(
        proto.STRING,
        number=1,
    )
    jwks: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )


class AttachedServerConfig(proto.Message):
    r"""AttachedServerConfig provides information about supported
    Kubernetes versions

    Attributes:
        name (str):
            The resource name of the config.
        valid_versions (MutableSequence[google.cloud.gke_multicloud_v1.types.AttachedPlatformVersionInfo]):
            List of valid platform versions.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    valid_versions: MutableSequence[
        "AttachedPlatformVersionInfo"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="AttachedPlatformVersionInfo",
    )


class AttachedPlatformVersionInfo(proto.Message):
    r"""Information about a supported Attached Clusters platform
    version.

    Attributes:
        version (str):
            Platform version name.
    """

    version: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AttachedClusterError(proto.Message):
    r"""AttachedClusterError describes errors found on attached
    clusters.

    Attributes:
        message (str):
            Human-friendly description of the error.
    """

    message: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AttachedProxyConfig(proto.Message):
    r"""Details of a proxy config.

    Attributes:
        kubernetes_secret (google.cloud.gke_multicloud_v1.types.KubernetesSecret):
            The Kubernetes Secret resource that contains
            the HTTP(S) proxy configuration. The secret must
            be a JSON encoded proxy configuration as
            described in
    """

    kubernetes_secret: "KubernetesSecret" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="KubernetesSecret",
    )


class KubernetesSecret(proto.Message):
    r"""Information about a Kubernetes Secret

    Attributes:
        name (str):
            Name of the kubernetes secret.
        namespace (str):
            Namespace in which the kubernetes secret is
            stored.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    namespace: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
