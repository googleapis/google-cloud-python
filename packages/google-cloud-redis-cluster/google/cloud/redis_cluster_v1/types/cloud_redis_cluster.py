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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.redis.cluster.v1",
    manifest={
        "AuthorizationMode",
        "NodeType",
        "TransitEncryptionMode",
        "CreateClusterRequest",
        "ListClustersRequest",
        "ListClustersResponse",
        "UpdateClusterRequest",
        "GetClusterRequest",
        "DeleteClusterRequest",
        "GetClusterCertificateAuthorityRequest",
        "Cluster",
        "PscConfig",
        "DiscoveryEndpoint",
        "PscConnection",
        "OperationMetadata",
        "CertificateAuthority",
        "ClusterPersistenceConfig",
        "ZoneDistributionConfig",
    },
)


class AuthorizationMode(proto.Enum):
    r"""Available authorization mode of a Redis cluster.

    Values:
        AUTH_MODE_UNSPECIFIED (0):
            Not set.
        AUTH_MODE_IAM_AUTH (1):
            IAM basic authorization mode
        AUTH_MODE_DISABLED (2):
            Authorization disabled mode
    """
    AUTH_MODE_UNSPECIFIED = 0
    AUTH_MODE_IAM_AUTH = 1
    AUTH_MODE_DISABLED = 2


class NodeType(proto.Enum):
    r"""NodeType of a redis cluster node,

    Values:
        NODE_TYPE_UNSPECIFIED (0):
            No description available.
        REDIS_SHARED_CORE_NANO (1):
            Redis shared core nano node_type.
        REDIS_HIGHMEM_MEDIUM (2):
            Redis highmem medium node_type.
        REDIS_HIGHMEM_XLARGE (3):
            Redis highmem xlarge node_type.
        REDIS_STANDARD_SMALL (4):
            Redis standard small node_type.
    """
    NODE_TYPE_UNSPECIFIED = 0
    REDIS_SHARED_CORE_NANO = 1
    REDIS_HIGHMEM_MEDIUM = 2
    REDIS_HIGHMEM_XLARGE = 3
    REDIS_STANDARD_SMALL = 4


class TransitEncryptionMode(proto.Enum):
    r"""Available mode of in-transit encryption.

    Values:
        TRANSIT_ENCRYPTION_MODE_UNSPECIFIED (0):
            In-transit encryption not set.
        TRANSIT_ENCRYPTION_MODE_DISABLED (1):
            In-transit encryption disabled.
        TRANSIT_ENCRYPTION_MODE_SERVER_AUTHENTICATION (2):
            Use server managed encryption for in-transit
            encryption.
    """
    TRANSIT_ENCRYPTION_MODE_UNSPECIFIED = 0
    TRANSIT_ENCRYPTION_MODE_DISABLED = 1
    TRANSIT_ENCRYPTION_MODE_SERVER_AUTHENTICATION = 2


class CreateClusterRequest(proto.Message):
    r"""Request for [CreateCluster][CloudRedis.CreateCluster].

    Attributes:
        parent (str):
            Required. The resource name of the cluster location using
            the form: ``projects/{project_id}/locations/{location_id}``
            where ``location_id`` refers to a GCP region.
        cluster_id (str):
            Required. The logical name of the Redis cluster in the
            customer project with the following restrictions:

            -  Must contain only lowercase letters, numbers, and
               hyphens.
            -  Must start with a letter.
            -  Must be between 1-63 characters.
            -  Must end with a number or a letter.
            -  Must be unique within the customer project / location
        cluster (google.cloud.redis_cluster_v1.types.Cluster):
            Required. The cluster that is to be created.
        request_id (str):
            Idempotent request UUID.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster: "Cluster" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Cluster",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListClustersRequest(proto.Message):
    r"""Request for [ListClusters][CloudRedis.ListClusters].

    Attributes:
        parent (str):
            Required. The resource name of the cluster location using
            the form: ``projects/{project_id}/locations/{location_id}``
            where ``location_id`` refers to a GCP region.
        page_size (int):
            The maximum number of items to return.

            If not specified, a default value of 1000 will be used by
            the service. Regardless of the page_size value, the response
            may include a partial list and a caller should only rely on
            response's
            [``next_page_token``][google.cloud.redis.cluster.v1.ListClustersResponse.next_page_token]
            to determine if there are more clusters left to be queried.
        page_token (str):
            The ``next_page_token`` value returned from a previous
            [ListClusters][CloudRedis.ListClusters] request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListClustersResponse(proto.Message):
    r"""Response for [ListClusters][CloudRedis.ListClusters].

    Attributes:
        clusters (MutableSequence[google.cloud.redis_cluster_v1.types.Cluster]):
            A list of Redis clusters in the project in the specified
            location, or across all locations.

            If the ``location_id`` in the parent field of the request is
            "-", all regions available to the project are queried, and
            the results aggregated. If in such an aggregated query a
            location is unavailable, a placeholder Redis entry is
            included in the response with the ``name`` field set to a
            value of the form
            ``projects/{project_id}/locations/{location_id}/clusters/``-
            and the ``status`` field set to ERROR and ``status_message``
            field set to "location not available for ListClusters".
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    clusters: MutableSequence["Cluster"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Cluster",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class UpdateClusterRequest(proto.Message):
    r"""Request for [UpdateCluster][CloudRedis.UpdateCluster].

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update. At least one path must
            be supplied in this field. The elements of the repeated
            paths field may only include these fields from
            [Cluster][google.cloud.redis.cluster.v1.Cluster]:

            -  ``size_gb``
            -  ``replica_count``
        cluster (google.cloud.redis_cluster_v1.types.Cluster):
            Required. Update description. Only fields specified in
            update_mask are updated.
        request_id (str):
            Idempotent request UUID.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    cluster: "Cluster" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Cluster",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class GetClusterRequest(proto.Message):
    r"""Request for [GetCluster][CloudRedis.GetCluster].

    Attributes:
        name (str):
            Required. Redis cluster resource name using the form:
            ``projects/{project_id}/locations/{location_id}/clusters/{cluster_id}``
            where ``location_id`` refers to a GCP region.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteClusterRequest(proto.Message):
    r"""Request for [DeleteCluster][CloudRedis.DeleteCluster].

    Attributes:
        name (str):
            Required. Redis cluster resource name using the form:
            ``projects/{project_id}/locations/{location_id}/clusters/{cluster_id}``
            where ``location_id`` refers to a GCP region.
        request_id (str):
            Idempotent request UUID.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetClusterCertificateAuthorityRequest(proto.Message):
    r"""Request for
    [GetClusterCertificateAuthorityRequest][CloudRedis.GetClusterCertificateAuthorityRequest].

    Attributes:
        name (str):
            Required. Redis cluster certificate authority resource name
            using the form:
            ``projects/{project_id}/locations/{location_id}/clusters/{cluster_id}/certificateAuthority``
            where ``location_id`` refers to a GCP region.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class Cluster(proto.Message):
    r"""A cluster instance.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. Unique name of the resource in this scope
            including project and location using the form:
            ``projects/{project_id}/locations/{location_id}/clusters/{cluster_id}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp associated with
            the cluster creation request.
        state (google.cloud.redis_cluster_v1.types.Cluster.State):
            Output only. The current state of this
            cluster. Can be CREATING, READY, UPDATING,
            DELETING and SUSPENDED
        uid (str):
            Output only. System assigned, unique
            identifier for the cluster.
        replica_count (int):
            Optional. The number of replica nodes per
            shard.

            This field is a member of `oneof`_ ``_replica_count``.
        authorization_mode (google.cloud.redis_cluster_v1.types.AuthorizationMode):
            Optional. The authorization mode of the Redis
            cluster. If not provided, auth feature is
            disabled for the cluster.
        transit_encryption_mode (google.cloud.redis_cluster_v1.types.TransitEncryptionMode):
            Optional. The in-transit encryption for the
            Redis cluster. If not provided, encryption  is
            disabled for the cluster.
        size_gb (int):
            Output only. Redis memory size in GB for the
            entire cluster rounded up to the next integer.

            This field is a member of `oneof`_ ``_size_gb``.
        shard_count (int):
            Required. Number of shards for the Redis
            cluster.

            This field is a member of `oneof`_ ``_shard_count``.
        psc_configs (MutableSequence[google.cloud.redis_cluster_v1.types.PscConfig]):
            Required. Each PscConfig configures the
            consumer network where IPs will be designated to
            the cluster for client access through Private
            Service Connect Automation. Currently, only one
            PscConfig is supported.
        discovery_endpoints (MutableSequence[google.cloud.redis_cluster_v1.types.DiscoveryEndpoint]):
            Output only. Endpoints created on each given
            network, for Redis clients to connect to the
            cluster. Currently only one discovery endpoint
            is supported.
        psc_connections (MutableSequence[google.cloud.redis_cluster_v1.types.PscConnection]):
            Output only. PSC connections for discovery of
            the cluster topology and accessing the cluster.
        state_info (google.cloud.redis_cluster_v1.types.Cluster.StateInfo):
            Output only. Additional information about the
            current state of the cluster.
        node_type (google.cloud.redis_cluster_v1.types.NodeType):
            Optional. The type of a redis node in the
            cluster. NodeType determines the underlying
            machine-type of a redis node.
        persistence_config (google.cloud.redis_cluster_v1.types.ClusterPersistenceConfig):
            Optional. Persistence config (RDB, AOF) for
            the cluster.
        redis_configs (MutableMapping[str, str]):
            Optional. Key/Value pairs of customer
            overrides for mutable Redis Configs
        precise_size_gb (float):
            Output only. Precise value of redis memory
            size in GB for the entire cluster.

            This field is a member of `oneof`_ ``_precise_size_gb``.
        zone_distribution_config (google.cloud.redis_cluster_v1.types.ZoneDistributionConfig):
            Optional. This config will be used to
            determine how the customer wants us to
            distribute cluster resources within the region.
        deletion_protection_enabled (bool):
            Optional. The delete operation will fail when
            the value is set to true.

            This field is a member of `oneof`_ ``_deletion_protection_enabled``.
    """

    class State(proto.Enum):
        r"""Represents the different states of a Redis cluster.

        Values:
            STATE_UNSPECIFIED (0):
                Not set.
            CREATING (1):
                Redis cluster is being created.
            ACTIVE (2):
                Redis cluster has been created and is fully
                usable.
            UPDATING (3):
                Redis cluster configuration is being updated.
            DELETING (4):
                Redis cluster is being deleted.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        UPDATING = 3
        DELETING = 4

    class StateInfo(proto.Message):
        r"""Represents additional information about the state of the
        cluster.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            update_info (google.cloud.redis_cluster_v1.types.Cluster.StateInfo.UpdateInfo):
                Describes ongoing update on the cluster when
                cluster state is UPDATING.

                This field is a member of `oneof`_ ``info``.
        """

        class UpdateInfo(proto.Message):
            r"""Represents information about an updating cluster.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                target_shard_count (int):
                    Target number of shards for redis cluster

                    This field is a member of `oneof`_ ``_target_shard_count``.
                target_replica_count (int):
                    Target number of replica nodes per shard.

                    This field is a member of `oneof`_ ``_target_replica_count``.
            """

            target_shard_count: int = proto.Field(
                proto.INT32,
                number=1,
                optional=True,
            )
            target_replica_count: int = proto.Field(
                proto.INT32,
                number=2,
                optional=True,
            )

        update_info: "Cluster.StateInfo.UpdateInfo" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="info",
            message="Cluster.StateInfo.UpdateInfo",
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=5,
    )
    replica_count: int = proto.Field(
        proto.INT32,
        number=8,
        optional=True,
    )
    authorization_mode: "AuthorizationMode" = proto.Field(
        proto.ENUM,
        number=11,
        enum="AuthorizationMode",
    )
    transit_encryption_mode: "TransitEncryptionMode" = proto.Field(
        proto.ENUM,
        number=12,
        enum="TransitEncryptionMode",
    )
    size_gb: int = proto.Field(
        proto.INT32,
        number=13,
        optional=True,
    )
    shard_count: int = proto.Field(
        proto.INT32,
        number=14,
        optional=True,
    )
    psc_configs: MutableSequence["PscConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=15,
        message="PscConfig",
    )
    discovery_endpoints: MutableSequence["DiscoveryEndpoint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=16,
        message="DiscoveryEndpoint",
    )
    psc_connections: MutableSequence["PscConnection"] = proto.RepeatedField(
        proto.MESSAGE,
        number=17,
        message="PscConnection",
    )
    state_info: StateInfo = proto.Field(
        proto.MESSAGE,
        number=18,
        message=StateInfo,
    )
    node_type: "NodeType" = proto.Field(
        proto.ENUM,
        number=19,
        enum="NodeType",
    )
    persistence_config: "ClusterPersistenceConfig" = proto.Field(
        proto.MESSAGE,
        number=20,
        message="ClusterPersistenceConfig",
    )
    redis_configs: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=21,
    )
    precise_size_gb: float = proto.Field(
        proto.DOUBLE,
        number=22,
        optional=True,
    )
    zone_distribution_config: "ZoneDistributionConfig" = proto.Field(
        proto.MESSAGE,
        number=23,
        message="ZoneDistributionConfig",
    )
    deletion_protection_enabled: bool = proto.Field(
        proto.BOOL,
        number=25,
        optional=True,
    )


class PscConfig(proto.Message):
    r"""

    Attributes:
        network (str):
            Required. The network where the IP address of the discovery
            endpoint will be reserved, in the form of
            projects/{network_project}/global/networks/{network_id}.
    """

    network: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DiscoveryEndpoint(proto.Message):
    r"""Endpoints on each network, for Redis clients to connect to
    the cluster.

    Attributes:
        address (str):
            Output only. Address of the exposed Redis
            endpoint used by clients to connect to the
            service. The address could be either IP or
            hostname.
        port (int):
            Output only. The port number of the exposed
            Redis endpoint.
        psc_config (google.cloud.redis_cluster_v1.types.PscConfig):
            Output only. Customer configuration for where
            the endpoint is created and accessed from.
    """

    address: str = proto.Field(
        proto.STRING,
        number=1,
    )
    port: int = proto.Field(
        proto.INT32,
        number=2,
    )
    psc_config: "PscConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="PscConfig",
    )


class PscConnection(proto.Message):
    r"""Details of consumer resources in a PSC connection.

    Attributes:
        psc_connection_id (str):
            Output only. The PSC connection id of the
            forwarding rule connected to the service
            attachment.
        address (str):
            Output only. The IP allocated on the consumer
            network for the PSC forwarding rule.
        forwarding_rule (str):
            Output only. The URI of the consumer side
            forwarding rule. Example:

            projects/{projectNumOrId}/regions/us-east1/forwardingRules/{resourceId}.
        project_id (str):
            Output only. The consumer project_id where the forwarding
            rule is created from.
        network (str):
            The consumer network where the IP address resides, in the
            form of projects/{project_id}/global/networks/{network_id}.
    """

    psc_connection_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    address: str = proto.Field(
        proto.STRING,
        number=2,
    )
    forwarding_rule: str = proto.Field(
        proto.STRING,
        number=3,
    )
    project_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    network: str = proto.Field(
        proto.STRING,
        number=5,
    )


class OperationMetadata(proto.Message):
    r"""Pre-defined metadata fields.

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
            cancellation of the operation. Operations that have
            successfully been cancelled have [Operation.error][] value
            with a [google.rpc.Status.code][google.rpc.Status.code] of
            1, corresponding to ``Code.CANCELLED``.
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


class CertificateAuthority(proto.Message):
    r"""Redis cluster certificate authority

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        managed_server_ca (google.cloud.redis_cluster_v1.types.CertificateAuthority.ManagedCertificateAuthority):

            This field is a member of `oneof`_ ``server_ca``.
        name (str):
            Identifier. Unique name of the resource in this scope
            including project, location and cluster using the form:
            ``projects/{project}/locations/{location}/clusters/{cluster}/certificateAuthority``
    """

    class ManagedCertificateAuthority(proto.Message):
        r"""

        Attributes:
            ca_certs (MutableSequence[google.cloud.redis_cluster_v1.types.CertificateAuthority.ManagedCertificateAuthority.CertChain]):
                The PEM encoded CA certificate chains for
                redis managed server authentication
        """

        class CertChain(proto.Message):
            r"""

            Attributes:
                certificates (MutableSequence[str]):
                    The certificates that form the CA chain, from
                    leaf to root order.
            """

            certificates: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=1,
            )

        ca_certs: MutableSequence[
            "CertificateAuthority.ManagedCertificateAuthority.CertChain"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="CertificateAuthority.ManagedCertificateAuthority.CertChain",
        )

    managed_server_ca: ManagedCertificateAuthority = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="server_ca",
        message=ManagedCertificateAuthority,
    )
    name: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ClusterPersistenceConfig(proto.Message):
    r"""Configuration of the persistence functionality.

    Attributes:
        mode (google.cloud.redis_cluster_v1.types.ClusterPersistenceConfig.PersistenceMode):
            Optional. The mode of persistence.
        rdb_config (google.cloud.redis_cluster_v1.types.ClusterPersistenceConfig.RDBConfig):
            Optional. RDB configuration. This field will
            be ignored if mode is not RDB.
        aof_config (google.cloud.redis_cluster_v1.types.ClusterPersistenceConfig.AOFConfig):
            Optional. AOF configuration. This field will
            be ignored if mode is not AOF.
    """

    class PersistenceMode(proto.Enum):
        r"""Available persistence modes.

        Values:
            PERSISTENCE_MODE_UNSPECIFIED (0):
                Not set.
            DISABLED (1):
                Persistence is disabled, and any snapshot
                data is deleted.
            RDB (2):
                RDB based persistence is enabled.
            AOF (3):
                AOF based persistence is enabled.
        """
        PERSISTENCE_MODE_UNSPECIFIED = 0
        DISABLED = 1
        RDB = 2
        AOF = 3

    class RDBConfig(proto.Message):
        r"""Configuration of the RDB based persistence.

        Attributes:
            rdb_snapshot_period (google.cloud.redis_cluster_v1.types.ClusterPersistenceConfig.RDBConfig.SnapshotPeriod):
                Optional. Period between RDB snapshots.
            rdb_snapshot_start_time (google.protobuf.timestamp_pb2.Timestamp):
                Optional. The time that the first snapshot
                was/will be attempted, and to which future
                snapshots will be aligned. If not provided, the
                current time will be used.
        """

        class SnapshotPeriod(proto.Enum):
            r"""Available snapshot periods.

            Values:
                SNAPSHOT_PERIOD_UNSPECIFIED (0):
                    Not set.
                ONE_HOUR (1):
                    One hour.
                SIX_HOURS (2):
                    Six hours.
                TWELVE_HOURS (3):
                    Twelve hours.
                TWENTY_FOUR_HOURS (4):
                    Twenty four hours.
            """
            SNAPSHOT_PERIOD_UNSPECIFIED = 0
            ONE_HOUR = 1
            SIX_HOURS = 2
            TWELVE_HOURS = 3
            TWENTY_FOUR_HOURS = 4

        rdb_snapshot_period: "ClusterPersistenceConfig.RDBConfig.SnapshotPeriod" = (
            proto.Field(
                proto.ENUM,
                number=1,
                enum="ClusterPersistenceConfig.RDBConfig.SnapshotPeriod",
            )
        )
        rdb_snapshot_start_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=2,
            message=timestamp_pb2.Timestamp,
        )

    class AOFConfig(proto.Message):
        r"""Configuration of the AOF based persistence.

        Attributes:
            append_fsync (google.cloud.redis_cluster_v1.types.ClusterPersistenceConfig.AOFConfig.AppendFsync):
                Optional. fsync configuration.
        """

        class AppendFsync(proto.Enum):
            r"""Available fsync modes.

            Values:
                APPEND_FSYNC_UNSPECIFIED (0):
                    Not set. Default: EVERYSEC
                NO (1):
                    Never fsync. Normally Linux will flush data
                    every 30 seconds with this configuration, but
                    it's up to the kernel's exact tuning.
                EVERYSEC (2):
                    fsync every second. Fast enough, and you may
                    lose 1 second of data if there is a disaster
                ALWAYS (3):
                    fsync every time new commands are appended to
                    the AOF. It has the best data loss protection at
                    the cost of performance
            """
            APPEND_FSYNC_UNSPECIFIED = 0
            NO = 1
            EVERYSEC = 2
            ALWAYS = 3

        append_fsync: "ClusterPersistenceConfig.AOFConfig.AppendFsync" = proto.Field(
            proto.ENUM,
            number=1,
            enum="ClusterPersistenceConfig.AOFConfig.AppendFsync",
        )

    mode: PersistenceMode = proto.Field(
        proto.ENUM,
        number=1,
        enum=PersistenceMode,
    )
    rdb_config: RDBConfig = proto.Field(
        proto.MESSAGE,
        number=2,
        message=RDBConfig,
    )
    aof_config: AOFConfig = proto.Field(
        proto.MESSAGE,
        number=3,
        message=AOFConfig,
    )


class ZoneDistributionConfig(proto.Message):
    r"""Zone distribution config for allocation of cluster resources.

    Attributes:
        mode (google.cloud.redis_cluster_v1.types.ZoneDistributionConfig.ZoneDistributionMode):
            Optional. The mode of zone distribution. Defaults to
            MULTI_ZONE, when not specified.
        zone (str):
            Optional. When SINGLE ZONE distribution is selected, zone
            field would be used to allocate all resources in that zone.
            This is not applicable to MULTI_ZONE, and would be ignored
            for MULTI_ZONE clusters.
    """

    class ZoneDistributionMode(proto.Enum):
        r"""Defines various modes of zone distribution.
        Currently supports two modes, can be expanded in future to
        support more types of distribution modes.
        design doc: go/same-zone-cluster

        Values:
            ZONE_DISTRIBUTION_MODE_UNSPECIFIED (0):
                Not Set. Default: MULTI_ZONE
            MULTI_ZONE (1):
                Distribute all resources across 3 zones
                picked at random, within the region.
            SINGLE_ZONE (2):
                Distribute all resources in a single zone.
                The zone field must be specified, when this mode
                is selected.
        """
        ZONE_DISTRIBUTION_MODE_UNSPECIFIED = 0
        MULTI_ZONE = 1
        SINGLE_ZONE = 2

    mode: ZoneDistributionMode = proto.Field(
        proto.ENUM,
        number=1,
        enum=ZoneDistributionMode,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
