# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
    package="google.cloud.memorystore.v1",
    manifest={
        "PscConnectionStatus",
        "ConnectionType",
        "Instance",
        "PscAutoConnection",
        "PscConnection",
        "DiscoveryEndpoint",
        "PersistenceConfig",
        "NodeConfig",
        "ZoneDistributionConfig",
        "ListInstancesRequest",
        "ListInstancesResponse",
        "GetInstanceRequest",
        "CreateInstanceRequest",
        "UpdateInstanceRequest",
        "DeleteInstanceRequest",
        "GetCertificateAuthorityRequest",
        "CertificateAuthority",
        "OperationMetadata",
    },
)


class PscConnectionStatus(proto.Enum):
    r"""Status of the PSC connection.

    Values:
        PSC_CONNECTION_STATUS_UNSPECIFIED (0):
            PSC connection status is not specified.
        ACTIVE (1):
            The connection is active
        NOT_FOUND (2):
            Connection not found
    """
    PSC_CONNECTION_STATUS_UNSPECIFIED = 0
    ACTIVE = 1
    NOT_FOUND = 2


class ConnectionType(proto.Enum):
    r"""Type of a PSC connection

    Values:
        CONNECTION_TYPE_UNSPECIFIED (0):
            Connection Type is not set
        CONNECTION_TYPE_DISCOVERY (1):
            Connection that will be used for topology
            discovery.
        CONNECTION_TYPE_PRIMARY (2):
            Connection that will be used as primary
            endpoint to access primary.
        CONNECTION_TYPE_READER (3):
            Connection that will be used as reader
            endpoint to access replicas.
    """
    CONNECTION_TYPE_UNSPECIFIED = 0
    CONNECTION_TYPE_DISCOVERY = 1
    CONNECTION_TYPE_PRIMARY = 2
    CONNECTION_TYPE_READER = 3


class Instance(proto.Message):
    r"""A Memorystore instance.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Identifier. Unique name of the instance.
            Format:
            projects/{project}/locations/{location}/instances/{instance}
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation timestamp of the
            instance.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Latest update timestamp of the
            instance.
        labels (MutableMapping[str, str]):
            Optional. Labels to represent user-provided
            metadata.
        state (google.cloud.memorystore_v1.types.Instance.State):
            Output only. Current state of the instance.
        state_info (google.cloud.memorystore_v1.types.Instance.StateInfo):
            Output only. Additional information about the
            state of the instance.
        uid (str):
            Output only. System assigned, unique
            identifier for the instance.
        replica_count (int):
            Optional. Number of replica nodes per shard.
            If omitted the default is 0 replicas.

            This field is a member of `oneof`_ ``_replica_count``.
        authorization_mode (google.cloud.memorystore_v1.types.Instance.AuthorizationMode):
            Optional. Immutable. Authorization mode of
            the instance.
        transit_encryption_mode (google.cloud.memorystore_v1.types.Instance.TransitEncryptionMode):
            Optional. Immutable. In-transit encryption
            mode of the instance.
        shard_count (int):
            Optional. Number of shards for the instance.
        discovery_endpoints (MutableSequence[google.cloud.memorystore_v1.types.DiscoveryEndpoint]):
            Output only. Endpoints clients can connect to
            the instance through. Currently only one
            discovery endpoint is supported.
        node_type (google.cloud.memorystore_v1.types.Instance.NodeType):
            Optional. Immutable. Machine type for
            individual nodes of the instance.
        persistence_config (google.cloud.memorystore_v1.types.PersistenceConfig):
            Optional. Persistence configuration of the
            instance.
        engine_version (str):
            Optional. Immutable. Engine version of the
            instance.
        engine_configs (MutableMapping[str, str]):
            Optional. User-provided engine configurations
            for the instance.
        node_config (google.cloud.memorystore_v1.types.NodeConfig):
            Output only. Configuration of individual
            nodes of the instance.
        zone_distribution_config (google.cloud.memorystore_v1.types.ZoneDistributionConfig):
            Optional. Immutable. Zone distribution
            configuration of the instance for node
            allocation.
        deletion_protection_enabled (bool):
            Optional. If set to true deletion of the
            instance will fail.

            This field is a member of `oneof`_ ``_deletion_protection_enabled``.
        psc_auto_connections (MutableSequence[google.cloud.memorystore_v1.types.PscAutoConnection]):
            Required. Immutable. User inputs and resource
            details of the auto-created PSC connections.
        endpoints (MutableSequence[google.cloud.memorystore_v1.types.Instance.InstanceEndpoint]):
            Optional. Endpoints for the instance.
        mode (google.cloud.memorystore_v1.types.Instance.Mode):
            Optional. The mode config for the instance.
    """

    class State(proto.Enum):
        r"""Possible states of the instance.

        Values:
            STATE_UNSPECIFIED (0):
                Not set.
            CREATING (1):
                Instance is being created.
            ACTIVE (2):
                Instance has been created and is usable.
            UPDATING (3):
                Instance is being updated.
            DELETING (4):
                Instance is being deleted.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        UPDATING = 3
        DELETING = 4

    class AuthorizationMode(proto.Enum):
        r"""Possible authorization modes of the instance.

        Values:
            AUTHORIZATION_MODE_UNSPECIFIED (0):
                Not set.
            AUTH_DISABLED (1):
                Authorization disabled.
            IAM_AUTH (2):
                IAM basic authorization.
        """
        AUTHORIZATION_MODE_UNSPECIFIED = 0
        AUTH_DISABLED = 1
        IAM_AUTH = 2

    class TransitEncryptionMode(proto.Enum):
        r"""Possible in-transit encryption modes of the instance.

        Values:
            TRANSIT_ENCRYPTION_MODE_UNSPECIFIED (0):
                Not set.
            TRANSIT_ENCRYPTION_DISABLED (1):
                In-transit encryption is disabled.
            SERVER_AUTHENTICATION (2):
                Server-managed encryption is used for
                in-transit encryption.
        """
        TRANSIT_ENCRYPTION_MODE_UNSPECIFIED = 0
        TRANSIT_ENCRYPTION_DISABLED = 1
        SERVER_AUTHENTICATION = 2

    class NodeType(proto.Enum):
        r"""Possible node types of the instance. See
        https://cloud.google.com/memorystore/docs/valkey/instance-node-specification
        for more information.

        Values:
            NODE_TYPE_UNSPECIFIED (0):
                Not set.
            SHARED_CORE_NANO (1):
                Shared core nano.
            HIGHMEM_MEDIUM (2):
                High memory medium.
            HIGHMEM_XLARGE (3):
                High memory extra large.
            STANDARD_SMALL (4):
                Standard small.
        """
        NODE_TYPE_UNSPECIFIED = 0
        SHARED_CORE_NANO = 1
        HIGHMEM_MEDIUM = 2
        HIGHMEM_XLARGE = 3
        STANDARD_SMALL = 4

    class Mode(proto.Enum):
        r"""The mode config, which is used to enable/disable cluster
        mode.

        Values:
            MODE_UNSPECIFIED (0):
                Mode is not specified.
            STANDALONE (1):
                Deprecated: Use CLUSTER_DISABLED instead.
            CLUSTER (2):
                Instance is in cluster mode.
            CLUSTER_DISABLED (4):
                Cluster mode is disabled for the instance.
        """
        MODE_UNSPECIFIED = 0
        STANDALONE = 1
        CLUSTER = 2
        CLUSTER_DISABLED = 4

    class StateInfo(proto.Message):
        r"""Additional information about the state of the instance.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            update_info (google.cloud.memorystore_v1.types.Instance.StateInfo.UpdateInfo):
                Output only. Describes ongoing update when
                instance state is UPDATING.

                This field is a member of `oneof`_ ``info``.
        """

        class UpdateInfo(proto.Message):
            r"""Represents information about instance with state UPDATING.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                target_shard_count (int):
                    Output only. Target number of shards for the
                    instance.

                    This field is a member of `oneof`_ ``_target_shard_count``.
                target_replica_count (int):
                    Output only. Target number of replica nodes
                    per shard for the instance.

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

        update_info: "Instance.StateInfo.UpdateInfo" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="info",
            message="Instance.StateInfo.UpdateInfo",
        )

    class InstanceEndpoint(proto.Message):
        r"""InstanceEndpoint consists of PSC connections that are created
        as a group in each VPC network for accessing the instance. In
        each group, there shall be one connection for each service
        attachment in the cluster.

        Attributes:
            connections (MutableSequence[google.cloud.memorystore_v1.types.Instance.ConnectionDetail]):
                Optional. A group of PSC connections. They
                are created in the same VPC network, one for
                each service attachment in the cluster.
        """

        connections: MutableSequence["Instance.ConnectionDetail"] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="Instance.ConnectionDetail",
        )

    class ConnectionDetail(proto.Message):
        r"""Information of each PSC connection.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            psc_auto_connection (google.cloud.memorystore_v1.types.PscAutoConnection):
                Detailed information of a PSC connection that
                is created through service connectivity
                automation.

                This field is a member of `oneof`_ ``connection``.
            psc_connection (google.cloud.memorystore_v1.types.PscConnection):
                Detailed information of a PSC connection that
                is created by the user.

                This field is a member of `oneof`_ ``connection``.
        """

        psc_auto_connection: "PscAutoConnection" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="connection",
            message="PscAutoConnection",
        )
        psc_connection: "PscConnection" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="connection",
            message="PscConnection",
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
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    state_info: StateInfo = proto.Field(
        proto.MESSAGE,
        number=6,
        message=StateInfo,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=7,
    )
    replica_count: int = proto.Field(
        proto.INT32,
        number=8,
        optional=True,
    )
    authorization_mode: AuthorizationMode = proto.Field(
        proto.ENUM,
        number=9,
        enum=AuthorizationMode,
    )
    transit_encryption_mode: TransitEncryptionMode = proto.Field(
        proto.ENUM,
        number=10,
        enum=TransitEncryptionMode,
    )
    shard_count: int = proto.Field(
        proto.INT32,
        number=11,
    )
    discovery_endpoints: MutableSequence["DiscoveryEndpoint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=12,
        message="DiscoveryEndpoint",
    )
    node_type: NodeType = proto.Field(
        proto.ENUM,
        number=13,
        enum=NodeType,
    )
    persistence_config: "PersistenceConfig" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="PersistenceConfig",
    )
    engine_version: str = proto.Field(
        proto.STRING,
        number=15,
    )
    engine_configs: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=16,
    )
    node_config: "NodeConfig" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="NodeConfig",
    )
    zone_distribution_config: "ZoneDistributionConfig" = proto.Field(
        proto.MESSAGE,
        number=18,
        message="ZoneDistributionConfig",
    )
    deletion_protection_enabled: bool = proto.Field(
        proto.BOOL,
        number=19,
        optional=True,
    )
    psc_auto_connections: MutableSequence["PscAutoConnection"] = proto.RepeatedField(
        proto.MESSAGE,
        number=20,
        message="PscAutoConnection",
    )
    endpoints: MutableSequence[InstanceEndpoint] = proto.RepeatedField(
        proto.MESSAGE,
        number=25,
        message=InstanceEndpoint,
    )
    mode: Mode = proto.Field(
        proto.ENUM,
        number=26,
        enum=Mode,
    )


class PscAutoConnection(proto.Message):
    r"""Details of consumer resources in a PSC connection.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        port (int):
            Optional. Output only. port will only be set
            for Primary/Reader or Discovery endpoint.

            This field is a member of `oneof`_ ``ports``.
        psc_connection_id (str):
            Output only. The PSC connection id of the
            forwarding rule connected to the service
            attachment.
        ip_address (str):
            Output only. The IP allocated on the consumer
            network for the PSC forwarding rule.
        forwarding_rule (str):
            Output only. The URI of the consumer side forwarding rule.
            Format:
            projects/{project}/regions/{region}/forwardingRules/{forwarding_rule}
        project_id (str):
            Required. The consumer project_id where PSC connections are
            established. This should be the same project_id that the
            instance is being created in.
        network (str):
            Required. The network where the PSC endpoints are created,
            in the form of
            projects/{project_id}/global/networks/{network_id}.
        service_attachment (str):
            Output only. The service attachment which is
            the target of the PSC connection, in the form of
            projects/{project-id}/regions/{region}/serviceAttachments/{service-attachment-id}.
        psc_connection_status (google.cloud.memorystore_v1.types.PscConnectionStatus):
            Output only. The status of the PSC
            connection: whether a connection exists and
            ACTIVE or it no longer exists. Please note that
            this value is updated periodically. Please use
            Private Service Connect APIs for the latest
            status.
        connection_type (google.cloud.memorystore_v1.types.ConnectionType):
            Output only. Type of the PSC connection.
    """

    port: int = proto.Field(
        proto.INT32,
        number=9,
        oneof="ports",
    )
    psc_connection_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ip_address: str = proto.Field(
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
    service_attachment: str = proto.Field(
        proto.STRING,
        number=6,
    )
    psc_connection_status: "PscConnectionStatus" = proto.Field(
        proto.ENUM,
        number=7,
        enum="PscConnectionStatus",
    )
    connection_type: "ConnectionType" = proto.Field(
        proto.ENUM,
        number=8,
        enum="ConnectionType",
    )


class PscConnection(proto.Message):
    r"""User created Psc connection configuration.

    Attributes:
        psc_connection_id (str):
            Output only. The PSC connection id of the
            forwarding rule connected to the service
            attachment.
        ip_address (str):
            Required. The IP allocated on the consumer
            network for the PSC forwarding rule.
        forwarding_rule (str):
            Required. The URI of the consumer side forwarding rule.
            Format:
            projects/{project}/regions/{region}/forwardingRules/{forwarding_rule}
        project_id (str):
            Output only. The consumer project_id where the forwarding
            rule is created from.
        network (str):
            Required. The consumer network where the IP address resides,
            in the form of
            projects/{project_id}/global/networks/{network_id}.
        service_attachment (str):
            Required. The service attachment which is the
            target of the PSC connection, in the form of
            projects/{project-id}/regions/{region}/serviceAttachments/{service-attachment-id}.
        psc_connection_status (google.cloud.memorystore_v1.types.PscConnectionStatus):
            Output only. The status of the PSC
            connection: whether a connection exists and
            ACTIVE or it no longer exists. Please note that
            this value is updated periodically. Please use
            Private Service Connect APIs for the latest
            status.
        connection_type (google.cloud.memorystore_v1.types.ConnectionType):
            Output only. Type of the PSC connection.
    """

    psc_connection_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ip_address: str = proto.Field(
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
    service_attachment: str = proto.Field(
        proto.STRING,
        number=6,
    )
    psc_connection_status: "PscConnectionStatus" = proto.Field(
        proto.ENUM,
        number=7,
        enum="PscConnectionStatus",
    )
    connection_type: "ConnectionType" = proto.Field(
        proto.ENUM,
        number=8,
        enum="ConnectionType",
    )


class DiscoveryEndpoint(proto.Message):
    r"""Represents an endpoint for clients to connect to the
    instance.

    Attributes:
        address (str):
            Output only. IP address of the exposed
            endpoint clients connect to.
        port (int):
            Output only. The port number of the exposed
            endpoint.
        network (str):
            Output only. The network where the IP address of the
            discovery endpoint will be reserved, in the form of
            projects/{network_project}/global/networks/{network_id}.
    """

    address: str = proto.Field(
        proto.STRING,
        number=1,
    )
    port: int = proto.Field(
        proto.INT32,
        number=2,
    )
    network: str = proto.Field(
        proto.STRING,
        number=4,
    )


class PersistenceConfig(proto.Message):
    r"""Represents persistence configuration for a instance.

    Attributes:
        mode (google.cloud.memorystore_v1.types.PersistenceConfig.PersistenceMode):
            Optional. Current persistence mode.
        rdb_config (google.cloud.memorystore_v1.types.PersistenceConfig.RDBConfig):
            Optional. RDB configuration. This field will
            be ignored if mode is not RDB.
        aof_config (google.cloud.memorystore_v1.types.PersistenceConfig.AOFConfig):
            Optional. AOF configuration. This field will
            be ignored if mode is not AOF.
    """

    class PersistenceMode(proto.Enum):
        r"""Possible persistence modes.

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
        r"""Configuration for RDB based persistence.

        Attributes:
            rdb_snapshot_period (google.cloud.memorystore_v1.types.PersistenceConfig.RDBConfig.SnapshotPeriod):
                Optional. Period between RDB snapshots.
            rdb_snapshot_start_time (google.protobuf.timestamp_pb2.Timestamp):
                Optional. Time that the first snapshot
                was/will be attempted, and to which future
                snapshots will be aligned. If not provided, the
                current time will be used.
        """

        class SnapshotPeriod(proto.Enum):
            r"""Possible snapshot periods.

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

        rdb_snapshot_period: "PersistenceConfig.RDBConfig.SnapshotPeriod" = proto.Field(
            proto.ENUM,
            number=1,
            enum="PersistenceConfig.RDBConfig.SnapshotPeriod",
        )
        rdb_snapshot_start_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=2,
            message=timestamp_pb2.Timestamp,
        )

    class AOFConfig(proto.Message):
        r"""Configuration for AOF based persistence.

        Attributes:
            append_fsync (google.cloud.memorystore_v1.types.PersistenceConfig.AOFConfig.AppendFsync):
                Optional. The fsync mode.
        """

        class AppendFsync(proto.Enum):
            r"""Possible fsync modes.

            Values:
                APPEND_FSYNC_UNSPECIFIED (0):
                    Not set. Default: EVERY_SEC
                NEVER (1):
                    Never fsync. Normally Linux will flush data
                    every 30 seconds with this configuration, but
                    it's up to the kernel's exact tuning.
                EVERY_SEC (2):
                    Fsync every second. You may lose 1 second of
                    data if there is a disaster.
                ALWAYS (3):
                    Fsync every time new write commands are
                    appended to the AOF. The best data loss
                    protection at the cost of performance.
            """
            APPEND_FSYNC_UNSPECIFIED = 0
            NEVER = 1
            EVERY_SEC = 2
            ALWAYS = 3

        append_fsync: "PersistenceConfig.AOFConfig.AppendFsync" = proto.Field(
            proto.ENUM,
            number=1,
            enum="PersistenceConfig.AOFConfig.AppendFsync",
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


class NodeConfig(proto.Message):
    r"""Represents configuration for nodes of the instance.

    Attributes:
        size_gb (float):
            Output only. Memory size in GB of the node.
    """

    size_gb: float = proto.Field(
        proto.DOUBLE,
        number=1,
    )


class ZoneDistributionConfig(proto.Message):
    r"""Zone distribution configuration for allocation of instance
    resources.

    Attributes:
        zone (str):
            Optional. Defines zone where all resources will be allocated
            with SINGLE_ZONE mode. Ignored for MULTI_ZONE mode.
        mode (google.cloud.memorystore_v1.types.ZoneDistributionConfig.ZoneDistributionMode):
            Optional. Current zone distribution mode. Defaults to
            MULTI_ZONE.
    """

    class ZoneDistributionMode(proto.Enum):
        r"""Possible zone distribution modes.

        Values:
            ZONE_DISTRIBUTION_MODE_UNSPECIFIED (0):
                Not Set. Default: MULTI_ZONE
            MULTI_ZONE (1):
                Distribute resources across 3 zones picked at
                random within the region.
            SINGLE_ZONE (2):
                Provision resources in a single zone. Zone
                field must be specified.
        """
        ZONE_DISTRIBUTION_MODE_UNSPECIFIED = 0
        MULTI_ZONE = 1
        SINGLE_ZONE = 2

    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    mode: ZoneDistributionMode = proto.Field(
        proto.ENUM,
        number=1,
        enum=ZoneDistributionMode,
    )


class ListInstancesRequest(proto.Message):
    r"""Request message for [ListInstances][].

    Attributes:
        parent (str):
            Required. The parent to list instances from.
            Format: projects/{project}/locations/{location}
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
        filter (str):
            Optional. Expression for filtering results.
        order_by (str):
            Optional. Sort results by a defined order. Supported values:
            "name", "create_time".
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListInstancesResponse(proto.Message):
    r"""Response message for [ListInstances][].

    Attributes:
        instances (MutableSequence[google.cloud.memorystore_v1.types.Instance]):
            If the {location} requested was "-" the
            response contains a list of instances from all
            locations. Instances in unreachable locations
            will be omitted.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    instances: MutableSequence["Instance"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Instance",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetInstanceRequest(proto.Message):
    r"""Request message for [GetInstance][].

    Attributes:
        name (str):
            Required. The name of the instance to
            retrieve. Format:
            projects/{project}/locations/{location}/instances/{instance}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateInstanceRequest(proto.Message):
    r"""Request message for [CreateInstance][].

    Attributes:
        parent (str):
            Required. The parent resource where this
            instance will be created. Format:
            projects/{project}/locations/{location}
        instance_id (str):
            Required. The ID to use for the instance, which will become
            the final component of the instance's resource name.

            This value is subject to the following restrictions:

            -  Must be 4-63 characters in length
            -  Must begin with a letter or digit
            -  Must contain only lowercase letters, digits, and hyphens
            -  Must not end with a hyphen
            -  Must be unique within a location
        instance (google.cloud.memorystore_v1.types.Instance):
            Required. The instance to create.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    instance_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    instance: "Instance" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Instance",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateInstanceRequest(proto.Message):
    r"""Request message for [UpdateInstance][].

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. The list of fields to be updated on
            the instance. At least one field must be
            specified.
        instance (google.cloud.memorystore_v1.types.Instance):
            Required. The instance to update.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    instance: "Instance" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Instance",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteInstanceRequest(proto.Message):
    r"""Request message for [DeleteInstance][].

    Attributes:
        name (str):
            Required. The name of the instance to delete.
            Format:
            projects/{project}/locations/{location}/instances/{instance}
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetCertificateAuthorityRequest(proto.Message):
    r"""Request message for [GetCertificateAuthority][].

    Attributes:
        name (str):
            Required. The name of the certificate
            authority. Format:

            projects/{project}/locations/{location}/instances/{instance}/certificateAuthority
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CertificateAuthority(proto.Message):
    r"""A certificate authority for an instance.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        managed_server_ca (google.cloud.memorystore_v1.types.CertificateAuthority.ManagedCertificateAuthority):
            A managed server certificate authority.

            This field is a member of `oneof`_ ``server_ca``.
        name (str):
            Identifier. Unique name of the certificate
            authority. Format:

            projects/{project}/locations/{location}/instances/{instance}
    """

    class ManagedCertificateAuthority(proto.Message):
        r"""A managed certificate authority.

        Attributes:
            ca_certs (MutableSequence[google.cloud.memorystore_v1.types.CertificateAuthority.ManagedCertificateAuthority.CertChain]):
                PEM encoded CA certificate chains for managed
                server authentication.
        """

        class CertChain(proto.Message):
            r"""A certificate chain.

            Attributes:
                certificates (MutableSequence[str]):
                    The certificates that form the CA chain in
                    order of leaf to root.
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
        number=2,
        oneof="server_ca",
        message=ManagedCertificateAuthority,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of a long-running operation.

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
