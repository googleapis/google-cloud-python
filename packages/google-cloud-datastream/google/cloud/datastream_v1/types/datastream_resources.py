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
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.datastream.v1",
    manifest={
        "OracleProfile",
        "OracleAsmConfig",
        "MysqlProfile",
        "PostgresqlProfile",
        "SqlServerProfile",
        "GcsProfile",
        "BigQueryProfile",
        "StaticServiceIpConnectivity",
        "ForwardSshTunnelConnectivity",
        "VpcPeeringConfig",
        "PrivateConnection",
        "PrivateConnectivity",
        "Route",
        "MysqlSslConfig",
        "OracleSslConfig",
        "ConnectionProfile",
        "OracleColumn",
        "OracleTable",
        "OracleSchema",
        "OracleRdbms",
        "OracleSourceConfig",
        "PostgresqlColumn",
        "PostgresqlTable",
        "PostgresqlSchema",
        "PostgresqlRdbms",
        "PostgresqlSourceConfig",
        "SqlServerColumn",
        "SqlServerTable",
        "SqlServerSchema",
        "SqlServerRdbms",
        "SqlServerSourceConfig",
        "SqlServerTransactionLogs",
        "SqlServerChangeTables",
        "MysqlColumn",
        "MysqlTable",
        "MysqlDatabase",
        "MysqlRdbms",
        "MysqlSourceConfig",
        "SourceConfig",
        "AvroFileFormat",
        "JsonFileFormat",
        "GcsDestinationConfig",
        "BigQueryDestinationConfig",
        "DestinationConfig",
        "Stream",
        "StreamObject",
        "SourceObjectIdentifier",
        "BackfillJob",
        "Error",
        "ValidationResult",
        "Validation",
        "ValidationMessage",
        "CdcStrategy",
        "SqlServerLsnPosition",
        "OracleScnPosition",
        "MysqlLogPosition",
    },
)


class OracleProfile(proto.Message):
    r"""Oracle database profile.
    Next ID: 10.

    Attributes:
        hostname (str):
            Required. Hostname for the Oracle connection.
        port (int):
            Port for the Oracle connection, default value
            is 1521.
        username (str):
            Required. Username for the Oracle connection.
        password (str):
            Optional. Password for the Oracle connection. Mutually
            exclusive with the ``secret_manager_stored_password`` field.
        database_service (str):
            Required. Database for the Oracle connection.
        connection_attributes (MutableMapping[str, str]):
            Connection string attributes
        oracle_ssl_config (google.cloud.datastream_v1.types.OracleSslConfig):
            Optional. SSL configuration for the Oracle
            connection.
        oracle_asm_config (google.cloud.datastream_v1.types.OracleAsmConfig):
            Optional. Configuration for Oracle ASM
            connection.
        secret_manager_stored_password (str):
            Optional. A reference to a Secret Manager resource name
            storing the Oracle connection password. Mutually exclusive
            with the ``password`` field.
    """

    hostname: str = proto.Field(
        proto.STRING,
        number=1,
    )
    port: int = proto.Field(
        proto.INT32,
        number=2,
    )
    username: str = proto.Field(
        proto.STRING,
        number=3,
    )
    password: str = proto.Field(
        proto.STRING,
        number=4,
    )
    database_service: str = proto.Field(
        proto.STRING,
        number=5,
    )
    connection_attributes: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    oracle_ssl_config: "OracleSslConfig" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="OracleSslConfig",
    )
    oracle_asm_config: "OracleAsmConfig" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="OracleAsmConfig",
    )
    secret_manager_stored_password: str = proto.Field(
        proto.STRING,
        number=9,
    )


class OracleAsmConfig(proto.Message):
    r"""Configuration for Oracle Automatic Storage Management (ASM)
    connection.

    Attributes:
        hostname (str):
            Required. Hostname for the Oracle ASM
            connection.
        port (int):
            Required. Port for the Oracle ASM connection.
        username (str):
            Required. Username for the Oracle ASM
            connection.
        password (str):
            Required. Password for the Oracle ASM
            connection.
        asm_service (str):
            Required. ASM service name for the Oracle ASM
            connection.
        connection_attributes (MutableMapping[str, str]):
            Optional. Connection string attributes
        oracle_ssl_config (google.cloud.datastream_v1.types.OracleSslConfig):
            Optional. SSL configuration for the Oracle
            connection.
    """

    hostname: str = proto.Field(
        proto.STRING,
        number=1,
    )
    port: int = proto.Field(
        proto.INT32,
        number=2,
    )
    username: str = proto.Field(
        proto.STRING,
        number=3,
    )
    password: str = proto.Field(
        proto.STRING,
        number=4,
    )
    asm_service: str = proto.Field(
        proto.STRING,
        number=5,
    )
    connection_attributes: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    oracle_ssl_config: "OracleSslConfig" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="OracleSslConfig",
    )


class MysqlProfile(proto.Message):
    r"""MySQL database profile.
    Next ID: 7.

    Attributes:
        hostname (str):
            Required. Hostname for the MySQL connection.
        port (int):
            Port for the MySQL connection, default value
            is 3306.
        username (str):
            Required. Username for the MySQL connection.
        password (str):
            Optional. Input only. Password for the MySQL connection.
            Mutually exclusive with the
            ``secret_manager_stored_password`` field.
        ssl_config (google.cloud.datastream_v1.types.MysqlSslConfig):
            SSL configuration for the MySQL connection.
    """

    hostname: str = proto.Field(
        proto.STRING,
        number=1,
    )
    port: int = proto.Field(
        proto.INT32,
        number=2,
    )
    username: str = proto.Field(
        proto.STRING,
        number=3,
    )
    password: str = proto.Field(
        proto.STRING,
        number=4,
    )
    ssl_config: "MysqlSslConfig" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="MysqlSslConfig",
    )


class PostgresqlProfile(proto.Message):
    r"""PostgreSQL database profile.

    Attributes:
        hostname (str):
            Required. Hostname for the PostgreSQL
            connection.
        port (int):
            Port for the PostgreSQL connection, default
            value is 5432.
        username (str):
            Required. Username for the PostgreSQL
            connection.
        password (str):
            Optional. Password for the PostgreSQL connection. Mutually
            exclusive with the ``secret_manager_stored_password`` field.
        database (str):
            Required. Database for the PostgreSQL
            connection.
    """

    hostname: str = proto.Field(
        proto.STRING,
        number=1,
    )
    port: int = proto.Field(
        proto.INT32,
        number=2,
    )
    username: str = proto.Field(
        proto.STRING,
        number=3,
    )
    password: str = proto.Field(
        proto.STRING,
        number=4,
    )
    database: str = proto.Field(
        proto.STRING,
        number=5,
    )


class SqlServerProfile(proto.Message):
    r"""SQLServer database profile.
    Next ID: 8.

    Attributes:
        hostname (str):
            Required. Hostname for the SQLServer
            connection.
        port (int):
            Port for the SQLServer connection, default
            value is 1433.
        username (str):
            Required. Username for the SQLServer
            connection.
        password (str):
            Optional. Password for the SQLServer connection. Mutually
            exclusive with the ``secret_manager_stored_password`` field.
        database (str):
            Required. Database for the SQLServer
            connection.
    """

    hostname: str = proto.Field(
        proto.STRING,
        number=1,
    )
    port: int = proto.Field(
        proto.INT32,
        number=2,
    )
    username: str = proto.Field(
        proto.STRING,
        number=3,
    )
    password: str = proto.Field(
        proto.STRING,
        number=4,
    )
    database: str = proto.Field(
        proto.STRING,
        number=5,
    )


class GcsProfile(proto.Message):
    r"""Cloud Storage bucket profile.

    Attributes:
        bucket (str):
            Required. The Cloud Storage bucket name.
        root_path (str):
            The root path inside the Cloud Storage
            bucket.
    """

    bucket: str = proto.Field(
        proto.STRING,
        number=1,
    )
    root_path: str = proto.Field(
        proto.STRING,
        number=2,
    )


class BigQueryProfile(proto.Message):
    r"""BigQuery warehouse profile."""


class StaticServiceIpConnectivity(proto.Message):
    r"""Static IP address connectivity. Used when the source database
    is configured to allow incoming connections from the Datastream
    public IP addresses for the region specified in the connection
    profile.

    """


class ForwardSshTunnelConnectivity(proto.Message):
    r"""Forward SSH Tunnel connectivity.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        hostname (str):
            Required. Hostname for the SSH tunnel.
        username (str):
            Required. Username for the SSH tunnel.
        port (int):
            Port for the SSH tunnel, default value is 22.
        password (str):
            Input only. SSH password.

            This field is a member of `oneof`_ ``authentication_method``.
        private_key (str):
            Input only. SSH private key.

            This field is a member of `oneof`_ ``authentication_method``.
    """

    hostname: str = proto.Field(
        proto.STRING,
        number=1,
    )
    username: str = proto.Field(
        proto.STRING,
        number=2,
    )
    port: int = proto.Field(
        proto.INT32,
        number=3,
    )
    password: str = proto.Field(
        proto.STRING,
        number=100,
        oneof="authentication_method",
    )
    private_key: str = proto.Field(
        proto.STRING,
        number=101,
        oneof="authentication_method",
    )


class VpcPeeringConfig(proto.Message):
    r"""The VPC Peering configuration is used to create VPC peering
    between Datastream and the consumer's VPC.

    Attributes:
        vpc (str):
            Required. Fully qualified name of the VPC that Datastream
            will peer to. Format:
            ``projects/{project}/global/{networks}/{name}``
        subnet (str):
            Required. A free subnet for peering. (CIDR of
            /29)
    """

    vpc: str = proto.Field(
        proto.STRING,
        number=1,
    )
    subnet: str = proto.Field(
        proto.STRING,
        number=2,
    )


class PrivateConnection(proto.Message):
    r"""The PrivateConnection resource is used to establish private
    connectivity between Datastream and a customer's network.

    Attributes:
        name (str):
            Output only. The resource's name.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The create time of the resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The update time of the resource.
        labels (MutableMapping[str, str]):
            Labels.
        display_name (str):
            Required. Display name.
        state (google.cloud.datastream_v1.types.PrivateConnection.State):
            Output only. The state of the Private
            Connection.
        error (google.cloud.datastream_v1.types.Error):
            Output only. In case of error, the details of
            the error in a user-friendly format.
        vpc_peering_config (google.cloud.datastream_v1.types.VpcPeeringConfig):
            VPC Peering Config.
    """

    class State(proto.Enum):
        r"""Private Connection state.

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified state.
            CREATING (1):
                The private connection is in creation state -
                creating resources.
            CREATED (2):
                The private connection has been created with
                all of its resources.
            FAILED (3):
                The private connection creation has failed.
            DELETING (4):
                The private connection is being deleted.
            FAILED_TO_DELETE (5):
                Delete request has failed, resource is in
                invalid state.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        CREATED = 2
        FAILED = 3
        DELETING = 4
        FAILED_TO_DELETE = 5

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
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=6,
        enum=State,
    )
    error: "Error" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="Error",
    )
    vpc_peering_config: "VpcPeeringConfig" = proto.Field(
        proto.MESSAGE,
        number=100,
        message="VpcPeeringConfig",
    )


class PrivateConnectivity(proto.Message):
    r"""Private Connectivity

    Attributes:
        private_connection (str):
            Required. A reference to a private connection resource.
            Format:
            ``projects/{project}/locations/{location}/privateConnections/{name}``
    """

    private_connection: str = proto.Field(
        proto.STRING,
        number=1,
    )


class Route(proto.Message):
    r"""The route resource is the child of the private connection
    resource, used for defining a route for a private connection.

    Attributes:
        name (str):
            Output only. The resource's name.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The create time of the resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The update time of the resource.
        labels (MutableMapping[str, str]):
            Labels.
        display_name (str):
            Required. Display name.
        destination_address (str):
            Required. Destination address for connection
        destination_port (int):
            Destination port for connection
    """

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
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    destination_address: str = proto.Field(
        proto.STRING,
        number=6,
    )
    destination_port: int = proto.Field(
        proto.INT32,
        number=7,
    )


class MysqlSslConfig(proto.Message):
    r"""MySQL SSL configuration information.

    Attributes:
        client_key (str):
            Input only. PEM-encoded private key associated with the
            Client Certificate. If this field is used then the
            'client_certificate' and the 'ca_certificate' fields are
            mandatory.
        client_key_set (bool):
            Output only. Indicates whether the client_key field is set.
        client_certificate (str):
            Input only. PEM-encoded certificate that will be used by the
            replica to authenticate against the source database server.
            If this field is used then the 'client_key' and the
            'ca_certificate' fields are mandatory.
        client_certificate_set (bool):
            Output only. Indicates whether the client_certificate field
            is set.
        ca_certificate (str):
            Input only. PEM-encoded certificate of the CA
            that signed the source database server's
            certificate.
        ca_certificate_set (bool):
            Output only. Indicates whether the ca_certificate field is
            set.
    """

    client_key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    client_key_set: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    client_certificate: str = proto.Field(
        proto.STRING,
        number=3,
    )
    client_certificate_set: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    ca_certificate: str = proto.Field(
        proto.STRING,
        number=5,
    )
    ca_certificate_set: bool = proto.Field(
        proto.BOOL,
        number=6,
    )


class OracleSslConfig(proto.Message):
    r"""Oracle SSL configuration information.

    Attributes:
        ca_certificate (str):
            Input only. PEM-encoded certificate of the CA
            that signed the source database server's
            certificate.
        ca_certificate_set (bool):
            Output only. Indicates whether the ca_certificate field has
            been set for this Connection-Profile.
    """

    ca_certificate: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ca_certificate_set: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class ConnectionProfile(proto.Message):
    r"""A set of reusable connection configurations to be used as a
    source or destination for a stream.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. The resource's name.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The create time of the resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The update time of the resource.
        labels (MutableMapping[str, str]):
            Labels.
        display_name (str):
            Required. Display name.
        oracle_profile (google.cloud.datastream_v1.types.OracleProfile):
            Oracle ConnectionProfile configuration.

            This field is a member of `oneof`_ ``profile``.
        gcs_profile (google.cloud.datastream_v1.types.GcsProfile):
            Cloud Storage ConnectionProfile
            configuration.

            This field is a member of `oneof`_ ``profile``.
        mysql_profile (google.cloud.datastream_v1.types.MysqlProfile):
            MySQL ConnectionProfile configuration.

            This field is a member of `oneof`_ ``profile``.
        bigquery_profile (google.cloud.datastream_v1.types.BigQueryProfile):
            BigQuery Connection Profile configuration.

            This field is a member of `oneof`_ ``profile``.
        postgresql_profile (google.cloud.datastream_v1.types.PostgresqlProfile):
            PostgreSQL Connection Profile configuration.

            This field is a member of `oneof`_ ``profile``.
        sql_server_profile (google.cloud.datastream_v1.types.SqlServerProfile):
            SQLServer Connection Profile configuration.

            This field is a member of `oneof`_ ``profile``.
        static_service_ip_connectivity (google.cloud.datastream_v1.types.StaticServiceIpConnectivity):
            Static Service IP connectivity.

            This field is a member of `oneof`_ ``connectivity``.
        forward_ssh_connectivity (google.cloud.datastream_v1.types.ForwardSshTunnelConnectivity):
            Forward SSH tunnel connectivity.

            This field is a member of `oneof`_ ``connectivity``.
        private_connectivity (google.cloud.datastream_v1.types.PrivateConnectivity):
            Private connectivity.

            This field is a member of `oneof`_ ``connectivity``.
    """

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
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    oracle_profile: "OracleProfile" = proto.Field(
        proto.MESSAGE,
        number=100,
        oneof="profile",
        message="OracleProfile",
    )
    gcs_profile: "GcsProfile" = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="profile",
        message="GcsProfile",
    )
    mysql_profile: "MysqlProfile" = proto.Field(
        proto.MESSAGE,
        number=102,
        oneof="profile",
        message="MysqlProfile",
    )
    bigquery_profile: "BigQueryProfile" = proto.Field(
        proto.MESSAGE,
        number=103,
        oneof="profile",
        message="BigQueryProfile",
    )
    postgresql_profile: "PostgresqlProfile" = proto.Field(
        proto.MESSAGE,
        number=104,
        oneof="profile",
        message="PostgresqlProfile",
    )
    sql_server_profile: "SqlServerProfile" = proto.Field(
        proto.MESSAGE,
        number=105,
        oneof="profile",
        message="SqlServerProfile",
    )
    static_service_ip_connectivity: "StaticServiceIpConnectivity" = proto.Field(
        proto.MESSAGE,
        number=200,
        oneof="connectivity",
        message="StaticServiceIpConnectivity",
    )
    forward_ssh_connectivity: "ForwardSshTunnelConnectivity" = proto.Field(
        proto.MESSAGE,
        number=201,
        oneof="connectivity",
        message="ForwardSshTunnelConnectivity",
    )
    private_connectivity: "PrivateConnectivity" = proto.Field(
        proto.MESSAGE,
        number=202,
        oneof="connectivity",
        message="PrivateConnectivity",
    )


class OracleColumn(proto.Message):
    r"""Oracle Column.

    Attributes:
        column (str):
            Column name.
        data_type (str):
            The Oracle data type.
        length (int):
            Column length.
        precision (int):
            Column precision.
        scale (int):
            Column scale.
        encoding (str):
            Column encoding.
        primary_key (bool):
            Whether or not the column represents a
            primary key.
        nullable (bool):
            Whether or not the column can accept a null
            value.
        ordinal_position (int):
            The ordinal position of the column in the
            table.
    """

    column: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data_type: str = proto.Field(
        proto.STRING,
        number=2,
    )
    length: int = proto.Field(
        proto.INT32,
        number=3,
    )
    precision: int = proto.Field(
        proto.INT32,
        number=4,
    )
    scale: int = proto.Field(
        proto.INT32,
        number=5,
    )
    encoding: str = proto.Field(
        proto.STRING,
        number=6,
    )
    primary_key: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    nullable: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    ordinal_position: int = proto.Field(
        proto.INT32,
        number=9,
    )


class OracleTable(proto.Message):
    r"""Oracle table.

    Attributes:
        table (str):
            Table name.
        oracle_columns (MutableSequence[google.cloud.datastream_v1.types.OracleColumn]):
            Oracle columns in the schema.
            When unspecified as part of include/exclude
            objects, includes/excludes everything.
    """

    table: str = proto.Field(
        proto.STRING,
        number=1,
    )
    oracle_columns: MutableSequence["OracleColumn"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="OracleColumn",
    )


class OracleSchema(proto.Message):
    r"""Oracle schema.

    Attributes:
        schema (str):
            Schema name.
        oracle_tables (MutableSequence[google.cloud.datastream_v1.types.OracleTable]):
            Tables in the schema.
    """

    schema: str = proto.Field(
        proto.STRING,
        number=1,
    )
    oracle_tables: MutableSequence["OracleTable"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="OracleTable",
    )


class OracleRdbms(proto.Message):
    r"""Oracle database structure.

    Attributes:
        oracle_schemas (MutableSequence[google.cloud.datastream_v1.types.OracleSchema]):
            Oracle schemas/databases in the database
            server.
    """

    oracle_schemas: MutableSequence["OracleSchema"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="OracleSchema",
    )


class OracleSourceConfig(proto.Message):
    r"""Oracle data source configuration

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        include_objects (google.cloud.datastream_v1.types.OracleRdbms):
            Oracle objects to include in the stream.
        exclude_objects (google.cloud.datastream_v1.types.OracleRdbms):
            Oracle objects to exclude from the stream.
        max_concurrent_cdc_tasks (int):
            Maximum number of concurrent CDC tasks. The
            number should be non-negative. If not set (or
            set to 0), the system's default value is used.
        max_concurrent_backfill_tasks (int):
            Maximum number of concurrent backfill tasks.
            The number should be non-negative. If not set
            (or set to 0), the system's default value is
            used.
        drop_large_objects (google.cloud.datastream_v1.types.OracleSourceConfig.DropLargeObjects):
            Drop large object values.

            This field is a member of `oneof`_ ``large_objects_handling``.
        stream_large_objects (google.cloud.datastream_v1.types.OracleSourceConfig.StreamLargeObjects):
            Stream large object values.

            This field is a member of `oneof`_ ``large_objects_handling``.
        log_miner (google.cloud.datastream_v1.types.OracleSourceConfig.LogMiner):
            Use LogMiner.

            This field is a member of `oneof`_ ``cdc_method``.
        binary_log_parser (google.cloud.datastream_v1.types.OracleSourceConfig.BinaryLogParser):
            Use Binary Log Parser.

            This field is a member of `oneof`_ ``cdc_method``.
    """

    class DropLargeObjects(proto.Message):
        r"""Configuration to drop large object values."""

    class StreamLargeObjects(proto.Message):
        r"""Configuration to stream large object values."""

    class LogMiner(proto.Message):
        r"""Configuration to use LogMiner CDC method."""

    class BinaryLogParser(proto.Message):
        r"""Configuration to use Binary Log Parser CDC technique.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            oracle_asm_log_file_access (google.cloud.datastream_v1.types.OracleSourceConfig.BinaryLogParser.OracleAsmLogFileAccess):
                Use Oracle ASM.

                This field is a member of `oneof`_ ``log_file_access``.
            log_file_directories (google.cloud.datastream_v1.types.OracleSourceConfig.BinaryLogParser.LogFileDirectories):
                Use Oracle directories.

                This field is a member of `oneof`_ ``log_file_access``.
        """

        class OracleAsmLogFileAccess(proto.Message):
            r"""Configuration to use Oracle ASM to access the log files."""

        class LogFileDirectories(proto.Message):
            r"""Configuration to specify the Oracle directories to access the
            log files.

            Attributes:
                online_log_directory (str):
                    Required. Oracle directory for online logs.
                archived_log_directory (str):
                    Required. Oracle directory for archived logs.
            """

            online_log_directory: str = proto.Field(
                proto.STRING,
                number=1,
            )
            archived_log_directory: str = proto.Field(
                proto.STRING,
                number=2,
            )

        oracle_asm_log_file_access: "OracleSourceConfig.BinaryLogParser.OracleAsmLogFileAccess" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="log_file_access",
            message="OracleSourceConfig.BinaryLogParser.OracleAsmLogFileAccess",
        )
        log_file_directories: "OracleSourceConfig.BinaryLogParser.LogFileDirectories" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="log_file_access",
            message="OracleSourceConfig.BinaryLogParser.LogFileDirectories",
        )

    include_objects: "OracleRdbms" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="OracleRdbms",
    )
    exclude_objects: "OracleRdbms" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="OracleRdbms",
    )
    max_concurrent_cdc_tasks: int = proto.Field(
        proto.INT32,
        number=3,
    )
    max_concurrent_backfill_tasks: int = proto.Field(
        proto.INT32,
        number=4,
    )
    drop_large_objects: DropLargeObjects = proto.Field(
        proto.MESSAGE,
        number=100,
        oneof="large_objects_handling",
        message=DropLargeObjects,
    )
    stream_large_objects: StreamLargeObjects = proto.Field(
        proto.MESSAGE,
        number=102,
        oneof="large_objects_handling",
        message=StreamLargeObjects,
    )
    log_miner: LogMiner = proto.Field(
        proto.MESSAGE,
        number=103,
        oneof="cdc_method",
        message=LogMiner,
    )
    binary_log_parser: BinaryLogParser = proto.Field(
        proto.MESSAGE,
        number=104,
        oneof="cdc_method",
        message=BinaryLogParser,
    )


class PostgresqlColumn(proto.Message):
    r"""PostgreSQL Column.

    Attributes:
        column (str):
            Column name.
        data_type (str):
            The PostgreSQL data type.
        length (int):
            Column length.
        precision (int):
            Column precision.
        scale (int):
            Column scale.
        primary_key (bool):
            Whether or not the column represents a
            primary key.
        nullable (bool):
            Whether or not the column can accept a null
            value.
        ordinal_position (int):
            The ordinal position of the column in the
            table.
    """

    column: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data_type: str = proto.Field(
        proto.STRING,
        number=2,
    )
    length: int = proto.Field(
        proto.INT32,
        number=3,
    )
    precision: int = proto.Field(
        proto.INT32,
        number=4,
    )
    scale: int = proto.Field(
        proto.INT32,
        number=5,
    )
    primary_key: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    nullable: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    ordinal_position: int = proto.Field(
        proto.INT32,
        number=9,
    )


class PostgresqlTable(proto.Message):
    r"""PostgreSQL table.

    Attributes:
        table (str):
            Table name.
        postgresql_columns (MutableSequence[google.cloud.datastream_v1.types.PostgresqlColumn]):
            PostgreSQL columns in the schema.
            When unspecified as part of include/exclude
            objects, includes/excludes everything.
    """

    table: str = proto.Field(
        proto.STRING,
        number=1,
    )
    postgresql_columns: MutableSequence["PostgresqlColumn"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="PostgresqlColumn",
    )


class PostgresqlSchema(proto.Message):
    r"""PostgreSQL schema.

    Attributes:
        schema (str):
            Schema name.
        postgresql_tables (MutableSequence[google.cloud.datastream_v1.types.PostgresqlTable]):
            Tables in the schema.
    """

    schema: str = proto.Field(
        proto.STRING,
        number=1,
    )
    postgresql_tables: MutableSequence["PostgresqlTable"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="PostgresqlTable",
    )


class PostgresqlRdbms(proto.Message):
    r"""PostgreSQL database structure.

    Attributes:
        postgresql_schemas (MutableSequence[google.cloud.datastream_v1.types.PostgresqlSchema]):
            PostgreSQL schemas in the database server.
    """

    postgresql_schemas: MutableSequence["PostgresqlSchema"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="PostgresqlSchema",
    )


class PostgresqlSourceConfig(proto.Message):
    r"""PostgreSQL data source configuration

    Attributes:
        include_objects (google.cloud.datastream_v1.types.PostgresqlRdbms):
            PostgreSQL objects to include in the stream.
        exclude_objects (google.cloud.datastream_v1.types.PostgresqlRdbms):
            PostgreSQL objects to exclude from the
            stream.
        replication_slot (str):
            Required. Immutable. The name of the logical
            replication slot that's configured with the
            pgoutput plugin.
        publication (str):
            Required. The name of the publication that includes the set
            of all tables that are defined in the stream's
            include_objects.
        max_concurrent_backfill_tasks (int):
            Maximum number of concurrent backfill tasks.
            The number should be non negative. If not set
            (or set to 0), the system's default value will
            be used.
    """

    include_objects: "PostgresqlRdbms" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="PostgresqlRdbms",
    )
    exclude_objects: "PostgresqlRdbms" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="PostgresqlRdbms",
    )
    replication_slot: str = proto.Field(
        proto.STRING,
        number=3,
    )
    publication: str = proto.Field(
        proto.STRING,
        number=4,
    )
    max_concurrent_backfill_tasks: int = proto.Field(
        proto.INT32,
        number=5,
    )


class SqlServerColumn(proto.Message):
    r"""SQLServer Column.

    Attributes:
        column (str):
            Column name.
        data_type (str):
            The SQLServer data type.
        length (int):
            Column length.
        precision (int):
            Column precision.
        scale (int):
            Column scale.
        primary_key (bool):
            Whether or not the column represents a
            primary key.
        nullable (bool):
            Whether or not the column can accept a null
            value.
        ordinal_position (int):
            The ordinal position of the column in the
            table.
    """

    column: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data_type: str = proto.Field(
        proto.STRING,
        number=2,
    )
    length: int = proto.Field(
        proto.INT32,
        number=3,
    )
    precision: int = proto.Field(
        proto.INT32,
        number=4,
    )
    scale: int = proto.Field(
        proto.INT32,
        number=5,
    )
    primary_key: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    nullable: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    ordinal_position: int = proto.Field(
        proto.INT32,
        number=8,
    )


class SqlServerTable(proto.Message):
    r"""SQLServer table.

    Attributes:
        table (str):
            Table name.
        columns (MutableSequence[google.cloud.datastream_v1.types.SqlServerColumn]):
            SQLServer columns in the schema.
            When unspecified as part of include/exclude
            objects, includes/excludes everything.
    """

    table: str = proto.Field(
        proto.STRING,
        number=1,
    )
    columns: MutableSequence["SqlServerColumn"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="SqlServerColumn",
    )


class SqlServerSchema(proto.Message):
    r"""SQLServer schema.

    Attributes:
        schema (str):
            Schema name.
        tables (MutableSequence[google.cloud.datastream_v1.types.SqlServerTable]):
            Tables in the schema.
    """

    schema: str = proto.Field(
        proto.STRING,
        number=1,
    )
    tables: MutableSequence["SqlServerTable"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="SqlServerTable",
    )


class SqlServerRdbms(proto.Message):
    r"""SQLServer database structure.

    Attributes:
        schemas (MutableSequence[google.cloud.datastream_v1.types.SqlServerSchema]):
            SQLServer schemas in the database server.
    """

    schemas: MutableSequence["SqlServerSchema"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SqlServerSchema",
    )


class SqlServerSourceConfig(proto.Message):
    r"""SQLServer data source configuration

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        include_objects (google.cloud.datastream_v1.types.SqlServerRdbms):
            SQLServer objects to include in the stream.
        exclude_objects (google.cloud.datastream_v1.types.SqlServerRdbms):
            SQLServer objects to exclude from the stream.
        max_concurrent_cdc_tasks (int):
            Max concurrent CDC tasks.
        max_concurrent_backfill_tasks (int):
            Max concurrent backfill tasks.
        transaction_logs (google.cloud.datastream_v1.types.SqlServerTransactionLogs):
            CDC reader reads from transaction logs.

            This field is a member of `oneof`_ ``cdc_method``.
        change_tables (google.cloud.datastream_v1.types.SqlServerChangeTables):
            CDC reader reads from change tables.

            This field is a member of `oneof`_ ``cdc_method``.
    """

    include_objects: "SqlServerRdbms" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="SqlServerRdbms",
    )
    exclude_objects: "SqlServerRdbms" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="SqlServerRdbms",
    )
    max_concurrent_cdc_tasks: int = proto.Field(
        proto.INT32,
        number=3,
    )
    max_concurrent_backfill_tasks: int = proto.Field(
        proto.INT32,
        number=4,
    )
    transaction_logs: "SqlServerTransactionLogs" = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="cdc_method",
        message="SqlServerTransactionLogs",
    )
    change_tables: "SqlServerChangeTables" = proto.Field(
        proto.MESSAGE,
        number=102,
        oneof="cdc_method",
        message="SqlServerChangeTables",
    )


class SqlServerTransactionLogs(proto.Message):
    r"""Configuration to use Transaction Logs CDC read method."""


class SqlServerChangeTables(proto.Message):
    r"""Configuration to use Change Tables CDC read method."""


class MysqlColumn(proto.Message):
    r"""MySQL Column.

    Attributes:
        column (str):
            Column name.
        data_type (str):
            The MySQL data type. Full data types list can
            be found here:
            https://dev.mysql.com/doc/refman/8.0/en/data-types.html
        length (int):
            Column length.
        collation (str):
            Column collation.
        primary_key (bool):
            Whether or not the column represents a
            primary key.
        nullable (bool):
            Whether or not the column can accept a null
            value.
        ordinal_position (int):
            The ordinal position of the column in the
            table.
        precision (int):
            Column precision.
        scale (int):
            Column scale.
    """

    column: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data_type: str = proto.Field(
        proto.STRING,
        number=2,
    )
    length: int = proto.Field(
        proto.INT32,
        number=3,
    )
    collation: str = proto.Field(
        proto.STRING,
        number=4,
    )
    primary_key: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    nullable: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    ordinal_position: int = proto.Field(
        proto.INT32,
        number=7,
    )
    precision: int = proto.Field(
        proto.INT32,
        number=8,
    )
    scale: int = proto.Field(
        proto.INT32,
        number=9,
    )


class MysqlTable(proto.Message):
    r"""MySQL table.

    Attributes:
        table (str):
            Table name.
        mysql_columns (MutableSequence[google.cloud.datastream_v1.types.MysqlColumn]):
            MySQL columns in the database.
            When unspecified as part of include/exclude
            objects, includes/excludes everything.
    """

    table: str = proto.Field(
        proto.STRING,
        number=1,
    )
    mysql_columns: MutableSequence["MysqlColumn"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="MysqlColumn",
    )


class MysqlDatabase(proto.Message):
    r"""MySQL database.

    Attributes:
        database (str):
            Database name.
        mysql_tables (MutableSequence[google.cloud.datastream_v1.types.MysqlTable]):
            Tables in the database.
    """

    database: str = proto.Field(
        proto.STRING,
        number=1,
    )
    mysql_tables: MutableSequence["MysqlTable"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="MysqlTable",
    )


class MysqlRdbms(proto.Message):
    r"""MySQL database structure

    Attributes:
        mysql_databases (MutableSequence[google.cloud.datastream_v1.types.MysqlDatabase]):
            Mysql databases on the server
    """

    mysql_databases: MutableSequence["MysqlDatabase"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="MysqlDatabase",
    )


class MysqlSourceConfig(proto.Message):
    r"""MySQL source configuration

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        include_objects (google.cloud.datastream_v1.types.MysqlRdbms):
            MySQL objects to retrieve from the source.
        exclude_objects (google.cloud.datastream_v1.types.MysqlRdbms):
            MySQL objects to exclude from the stream.
        max_concurrent_cdc_tasks (int):
            Maximum number of concurrent CDC tasks. The
            number should be non negative. If not set (or
            set to 0), the system's default value will be
            used.
        max_concurrent_backfill_tasks (int):
            Maximum number of concurrent backfill tasks.
            The number should be non negative. If not set
            (or set to 0), the system's default value will
            be used.
        binary_log_position (google.cloud.datastream_v1.types.MysqlSourceConfig.BinaryLogPosition):
            Use Binary log position based replication.

            This field is a member of `oneof`_ ``cdc_method``.
        gtid (google.cloud.datastream_v1.types.MysqlSourceConfig.Gtid):
            Use GTID based replication.

            This field is a member of `oneof`_ ``cdc_method``.
    """

    class BinaryLogPosition(proto.Message):
        r"""Use Binary log position based replication."""

    class Gtid(proto.Message):
        r"""Use GTID based replication."""

    include_objects: "MysqlRdbms" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="MysqlRdbms",
    )
    exclude_objects: "MysqlRdbms" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="MysqlRdbms",
    )
    max_concurrent_cdc_tasks: int = proto.Field(
        proto.INT32,
        number=3,
    )
    max_concurrent_backfill_tasks: int = proto.Field(
        proto.INT32,
        number=4,
    )
    binary_log_position: BinaryLogPosition = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="cdc_method",
        message=BinaryLogPosition,
    )
    gtid: Gtid = proto.Field(
        proto.MESSAGE,
        number=102,
        oneof="cdc_method",
        message=Gtid,
    )


class SourceConfig(proto.Message):
    r"""The configuration of the stream source.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        source_connection_profile (str):
            Required. Source connection profile resoource. Format:
            ``projects/{project}/locations/{location}/connectionProfiles/{name}``
        oracle_source_config (google.cloud.datastream_v1.types.OracleSourceConfig):
            Oracle data source configuration.

            This field is a member of `oneof`_ ``source_stream_config``.
        mysql_source_config (google.cloud.datastream_v1.types.MysqlSourceConfig):
            MySQL data source configuration.

            This field is a member of `oneof`_ ``source_stream_config``.
        postgresql_source_config (google.cloud.datastream_v1.types.PostgresqlSourceConfig):
            PostgreSQL data source configuration.

            This field is a member of `oneof`_ ``source_stream_config``.
        sql_server_source_config (google.cloud.datastream_v1.types.SqlServerSourceConfig):
            SQLServer data source configuration.

            This field is a member of `oneof`_ ``source_stream_config``.
    """

    source_connection_profile: str = proto.Field(
        proto.STRING,
        number=1,
    )
    oracle_source_config: "OracleSourceConfig" = proto.Field(
        proto.MESSAGE,
        number=100,
        oneof="source_stream_config",
        message="OracleSourceConfig",
    )
    mysql_source_config: "MysqlSourceConfig" = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="source_stream_config",
        message="MysqlSourceConfig",
    )
    postgresql_source_config: "PostgresqlSourceConfig" = proto.Field(
        proto.MESSAGE,
        number=102,
        oneof="source_stream_config",
        message="PostgresqlSourceConfig",
    )
    sql_server_source_config: "SqlServerSourceConfig" = proto.Field(
        proto.MESSAGE,
        number=103,
        oneof="source_stream_config",
        message="SqlServerSourceConfig",
    )


class AvroFileFormat(proto.Message):
    r"""AVRO file format configuration."""


class JsonFileFormat(proto.Message):
    r"""JSON file format configuration.

    Attributes:
        schema_file_format (google.cloud.datastream_v1.types.JsonFileFormat.SchemaFileFormat):
            The schema file format along JSON data files.
        compression (google.cloud.datastream_v1.types.JsonFileFormat.JsonCompression):
            Compression of the loaded JSON file.
    """

    class SchemaFileFormat(proto.Enum):
        r"""Schema file format.

        Values:
            SCHEMA_FILE_FORMAT_UNSPECIFIED (0):
                Unspecified schema file format.
            NO_SCHEMA_FILE (1):
                Do not attach schema file.
            AVRO_SCHEMA_FILE (2):
                Avro schema format.
        """
        SCHEMA_FILE_FORMAT_UNSPECIFIED = 0
        NO_SCHEMA_FILE = 1
        AVRO_SCHEMA_FILE = 2

    class JsonCompression(proto.Enum):
        r"""Json file compression.

        Values:
            JSON_COMPRESSION_UNSPECIFIED (0):
                Unspecified json file compression.
            NO_COMPRESSION (1):
                Do not compress JSON file.
            GZIP (2):
                Gzip compression.
        """
        JSON_COMPRESSION_UNSPECIFIED = 0
        NO_COMPRESSION = 1
        GZIP = 2

    schema_file_format: SchemaFileFormat = proto.Field(
        proto.ENUM,
        number=1,
        enum=SchemaFileFormat,
    )
    compression: JsonCompression = proto.Field(
        proto.ENUM,
        number=2,
        enum=JsonCompression,
    )


class GcsDestinationConfig(proto.Message):
    r"""Google Cloud Storage destination configuration

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        path (str):
            Path inside the Cloud Storage bucket to write
            data to.
        file_rotation_mb (int):
            The maximum file size to be saved in the
            bucket.
        file_rotation_interval (google.protobuf.duration_pb2.Duration):
            The maximum duration for which new events are
            added before a file is closed and a new file is
            created. Values within the range of 15-60
            seconds are allowed.
        avro_file_format (google.cloud.datastream_v1.types.AvroFileFormat):
            AVRO file format configuration.

            This field is a member of `oneof`_ ``file_format``.
        json_file_format (google.cloud.datastream_v1.types.JsonFileFormat):
            JSON file format configuration.

            This field is a member of `oneof`_ ``file_format``.
    """

    path: str = proto.Field(
        proto.STRING,
        number=1,
    )
    file_rotation_mb: int = proto.Field(
        proto.INT32,
        number=2,
    )
    file_rotation_interval: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=3,
        message=duration_pb2.Duration,
    )
    avro_file_format: "AvroFileFormat" = proto.Field(
        proto.MESSAGE,
        number=100,
        oneof="file_format",
        message="AvroFileFormat",
    )
    json_file_format: "JsonFileFormat" = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="file_format",
        message="JsonFileFormat",
    )


class BigQueryDestinationConfig(proto.Message):
    r"""BigQuery destination configuration

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        single_target_dataset (google.cloud.datastream_v1.types.BigQueryDestinationConfig.SingleTargetDataset):
            Single destination dataset.

            This field is a member of `oneof`_ ``dataset_config``.
        source_hierarchy_datasets (google.cloud.datastream_v1.types.BigQueryDestinationConfig.SourceHierarchyDatasets):
            Source hierarchy datasets.

            This field is a member of `oneof`_ ``dataset_config``.
        data_freshness (google.protobuf.duration_pb2.Duration):
            The guaranteed data freshness (in seconds)
            when querying tables created by the stream.
            Editing this field will only affect new tables
            created in the future, but existing tables will
            not be impacted. Lower values mean that queries
            will return fresher data, but may result in
            higher cost.
        merge (google.cloud.datastream_v1.types.BigQueryDestinationConfig.Merge):
            The standard mode

            This field is a member of `oneof`_ ``write_mode``.
        append_only (google.cloud.datastream_v1.types.BigQueryDestinationConfig.AppendOnly):
            Append only mode

            This field is a member of `oneof`_ ``write_mode``.
    """

    class SingleTargetDataset(proto.Message):
        r"""A single target dataset to which all data will be streamed.

        Attributes:
            dataset_id (str):
                The dataset ID of the target dataset.
                DatasetIds allowed characters:

                https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets#datasetreference.
        """

        dataset_id: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class SourceHierarchyDatasets(proto.Message):
        r"""Destination datasets are created so that hierarchy of the
        destination data objects matches the source hierarchy.

        Attributes:
            dataset_template (google.cloud.datastream_v1.types.BigQueryDestinationConfig.SourceHierarchyDatasets.DatasetTemplate):
                The dataset template to use for dynamic
                dataset creation.
        """

        class DatasetTemplate(proto.Message):
            r"""Dataset template used for dynamic dataset creation.

            Attributes:
                location (str):
                    Required. The geographic location where the
                    dataset should reside. See
                    https://cloud.google.com/bigquery/docs/locations
                    for supported locations.
                dataset_id_prefix (str):
                    If supplied, every created dataset will have its name
                    prefixed by the provided value. The prefix and name will be
                    separated by an underscore. i.e. \_<dataset_name>.
                kms_key_name (str):
                    Describes the Cloud KMS encryption key that will be used to
                    protect destination BigQuery table. The BigQuery Service
                    Account associated with your project requires access to this
                    encryption key. i.e.
                    projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{cryptoKey}.
                    See
                    https://cloud.google.com/bigquery/docs/customer-managed-encryption
                    for more information.
            """

            location: str = proto.Field(
                proto.STRING,
                number=1,
            )
            dataset_id_prefix: str = proto.Field(
                proto.STRING,
                number=2,
            )
            kms_key_name: str = proto.Field(
                proto.STRING,
                number=3,
            )

        dataset_template: "BigQueryDestinationConfig.SourceHierarchyDatasets.DatasetTemplate" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="BigQueryDestinationConfig.SourceHierarchyDatasets.DatasetTemplate",
        )

    class AppendOnly(proto.Message):
        r"""AppendOnly mode defines that all changes to a table will be
        written to the destination table.

        """

    class Merge(proto.Message):
        r"""Merge mode defines that all changes to a table will be merged
        at the destination table.

        """

    single_target_dataset: SingleTargetDataset = proto.Field(
        proto.MESSAGE,
        number=201,
        oneof="dataset_config",
        message=SingleTargetDataset,
    )
    source_hierarchy_datasets: SourceHierarchyDatasets = proto.Field(
        proto.MESSAGE,
        number=202,
        oneof="dataset_config",
        message=SourceHierarchyDatasets,
    )
    data_freshness: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=300,
        message=duration_pb2.Duration,
    )
    merge: Merge = proto.Field(
        proto.MESSAGE,
        number=301,
        oneof="write_mode",
        message=Merge,
    )
    append_only: AppendOnly = proto.Field(
        proto.MESSAGE,
        number=302,
        oneof="write_mode",
        message=AppendOnly,
    )


class DestinationConfig(proto.Message):
    r"""The configuration of the stream destination.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        destination_connection_profile (str):
            Required. Destination connection profile resource. Format:
            ``projects/{project}/locations/{location}/connectionProfiles/{name}``
        gcs_destination_config (google.cloud.datastream_v1.types.GcsDestinationConfig):
            A configuration for how data should be loaded
            to Cloud Storage.

            This field is a member of `oneof`_ ``destination_stream_config``.
        bigquery_destination_config (google.cloud.datastream_v1.types.BigQueryDestinationConfig):
            BigQuery destination configuration.

            This field is a member of `oneof`_ ``destination_stream_config``.
    """

    destination_connection_profile: str = proto.Field(
        proto.STRING,
        number=1,
    )
    gcs_destination_config: "GcsDestinationConfig" = proto.Field(
        proto.MESSAGE,
        number=100,
        oneof="destination_stream_config",
        message="GcsDestinationConfig",
    )
    bigquery_destination_config: "BigQueryDestinationConfig" = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="destination_stream_config",
        message="BigQueryDestinationConfig",
    )


class Stream(proto.Message):
    r"""A resource representing streaming data from a source to a
    destination.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. The stream's name.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time of the stream.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last update time of the
            stream.
        labels (MutableMapping[str, str]):
            Labels.
        display_name (str):
            Required. Display name.
        source_config (google.cloud.datastream_v1.types.SourceConfig):
            Required. Source connection profile
            configuration.
        destination_config (google.cloud.datastream_v1.types.DestinationConfig):
            Required. Destination connection profile
            configuration.
        state (google.cloud.datastream_v1.types.Stream.State):
            The state of the stream.
        backfill_all (google.cloud.datastream_v1.types.Stream.BackfillAllStrategy):
            Automatically backfill objects included in
            the stream source configuration. Specific
            objects can be excluded.

            This field is a member of `oneof`_ ``backfill_strategy``.
        backfill_none (google.cloud.datastream_v1.types.Stream.BackfillNoneStrategy):
            Do not automatically backfill any objects.

            This field is a member of `oneof`_ ``backfill_strategy``.
        errors (MutableSequence[google.cloud.datastream_v1.types.Error]):
            Output only. Errors on the Stream.
        customer_managed_encryption_key (str):
            Immutable. A reference to a KMS encryption
            key. If provided, it will be used to encrypt the
            data. If left blank, data will be encrypted
            using an internal Stream-specific encryption key
            provisioned through KMS.

            This field is a member of `oneof`_ ``_customer_managed_encryption_key``.
        last_recovery_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. If the stream was recovered, the
            time of the last recovery. Note: This field is
            currently experimental.
    """

    class State(proto.Enum):
        r"""Stream state.

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified stream state.
            NOT_STARTED (1):
                The stream has been created but has not yet
                started streaming data.
            RUNNING (2):
                The stream is running.
            PAUSED (3):
                The stream is paused.
            MAINTENANCE (4):
                The stream is in maintenance mode.

                Updates are rejected on the resource in this
                state.
            FAILED (5):
                The stream is experiencing an error that is
                preventing data from being streamed.
            FAILED_PERMANENTLY (6):
                The stream has experienced a terminal
                failure.
            STARTING (7):
                The stream is starting, but not yet running.
            DRAINING (8):
                The Stream is no longer reading new events,
                but still writing events in the buffer.
        """
        STATE_UNSPECIFIED = 0
        NOT_STARTED = 1
        RUNNING = 2
        PAUSED = 3
        MAINTENANCE = 4
        FAILED = 5
        FAILED_PERMANENTLY = 6
        STARTING = 7
        DRAINING = 8

    class BackfillAllStrategy(proto.Message):
        r"""Backfill strategy to automatically backfill the Stream's
        objects. Specific objects can be excluded.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            oracle_excluded_objects (google.cloud.datastream_v1.types.OracleRdbms):
                Oracle data source objects to avoid
                backfilling.

                This field is a member of `oneof`_ ``excluded_objects``.
            mysql_excluded_objects (google.cloud.datastream_v1.types.MysqlRdbms):
                MySQL data source objects to avoid
                backfilling.

                This field is a member of `oneof`_ ``excluded_objects``.
            postgresql_excluded_objects (google.cloud.datastream_v1.types.PostgresqlRdbms):
                PostgreSQL data source objects to avoid
                backfilling.

                This field is a member of `oneof`_ ``excluded_objects``.
            sql_server_excluded_objects (google.cloud.datastream_v1.types.SqlServerRdbms):
                SQLServer data source objects to avoid
                backfilling

                This field is a member of `oneof`_ ``excluded_objects``.
        """

        oracle_excluded_objects: "OracleRdbms" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="excluded_objects",
            message="OracleRdbms",
        )
        mysql_excluded_objects: "MysqlRdbms" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="excluded_objects",
            message="MysqlRdbms",
        )
        postgresql_excluded_objects: "PostgresqlRdbms" = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="excluded_objects",
            message="PostgresqlRdbms",
        )
        sql_server_excluded_objects: "SqlServerRdbms" = proto.Field(
            proto.MESSAGE,
            number=4,
            oneof="excluded_objects",
            message="SqlServerRdbms",
        )

    class BackfillNoneStrategy(proto.Message):
        r"""Backfill strategy to disable automatic backfill for the
        Stream's objects.

        """

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
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    source_config: "SourceConfig" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="SourceConfig",
    )
    destination_config: "DestinationConfig" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="DestinationConfig",
    )
    state: State = proto.Field(
        proto.ENUM,
        number=8,
        enum=State,
    )
    backfill_all: BackfillAllStrategy = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="backfill_strategy",
        message=BackfillAllStrategy,
    )
    backfill_none: BackfillNoneStrategy = proto.Field(
        proto.MESSAGE,
        number=102,
        oneof="backfill_strategy",
        message=BackfillNoneStrategy,
    )
    errors: MutableSequence["Error"] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message="Error",
    )
    customer_managed_encryption_key: str = proto.Field(
        proto.STRING,
        number=10,
        optional=True,
    )
    last_recovery_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=13,
        message=timestamp_pb2.Timestamp,
    )


class StreamObject(proto.Message):
    r"""A specific stream object (e.g a specific DB table).

    Attributes:
        name (str):
            Output only. The object resource's name.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time of the object.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last update time of the
            object.
        display_name (str):
            Required. Display name.
        errors (MutableSequence[google.cloud.datastream_v1.types.Error]):
            Output only. Active errors on the object.
        backfill_job (google.cloud.datastream_v1.types.BackfillJob):
            The latest backfill job that was initiated
            for the stream object.
        source_object (google.cloud.datastream_v1.types.SourceObjectIdentifier):
            The object identifier in the data source.
    """

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
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    errors: MutableSequence["Error"] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="Error",
    )
    backfill_job: "BackfillJob" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="BackfillJob",
    )
    source_object: "SourceObjectIdentifier" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="SourceObjectIdentifier",
    )


class SourceObjectIdentifier(proto.Message):
    r"""Represents an identifier of an object in the data source.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        oracle_identifier (google.cloud.datastream_v1.types.SourceObjectIdentifier.OracleObjectIdentifier):
            Oracle data source object identifier.

            This field is a member of `oneof`_ ``source_identifier``.
        mysql_identifier (google.cloud.datastream_v1.types.SourceObjectIdentifier.MysqlObjectIdentifier):
            Mysql data source object identifier.

            This field is a member of `oneof`_ ``source_identifier``.
        postgresql_identifier (google.cloud.datastream_v1.types.SourceObjectIdentifier.PostgresqlObjectIdentifier):
            PostgreSQL data source object identifier.

            This field is a member of `oneof`_ ``source_identifier``.
        sql_server_identifier (google.cloud.datastream_v1.types.SourceObjectIdentifier.SqlServerObjectIdentifier):
            SQLServer data source object identifier.

            This field is a member of `oneof`_ ``source_identifier``.
    """

    class OracleObjectIdentifier(proto.Message):
        r"""Oracle data source object identifier.

        Attributes:
            schema (str):
                Required. The schema name.
            table (str):
                Required. The table name.
        """

        schema: str = proto.Field(
            proto.STRING,
            number=1,
        )
        table: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class PostgresqlObjectIdentifier(proto.Message):
        r"""PostgreSQL data source object identifier.

        Attributes:
            schema (str):
                Required. The schema name.
            table (str):
                Required. The table name.
        """

        schema: str = proto.Field(
            proto.STRING,
            number=1,
        )
        table: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class MysqlObjectIdentifier(proto.Message):
        r"""Mysql data source object identifier.

        Attributes:
            database (str):
                Required. The database name.
            table (str):
                Required. The table name.
        """

        database: str = proto.Field(
            proto.STRING,
            number=1,
        )
        table: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class SqlServerObjectIdentifier(proto.Message):
        r"""SQLServer data source object identifier.

        Attributes:
            schema (str):
                Required. The schema name.
            table (str):
                Required. The table name.
        """

        schema: str = proto.Field(
            proto.STRING,
            number=1,
        )
        table: str = proto.Field(
            proto.STRING,
            number=2,
        )

    oracle_identifier: OracleObjectIdentifier = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="source_identifier",
        message=OracleObjectIdentifier,
    )
    mysql_identifier: MysqlObjectIdentifier = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="source_identifier",
        message=MysqlObjectIdentifier,
    )
    postgresql_identifier: PostgresqlObjectIdentifier = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="source_identifier",
        message=PostgresqlObjectIdentifier,
    )
    sql_server_identifier: SqlServerObjectIdentifier = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="source_identifier",
        message=SqlServerObjectIdentifier,
    )


class BackfillJob(proto.Message):
    r"""Represents a backfill job on a specific stream object.

    Attributes:
        state (google.cloud.datastream_v1.types.BackfillJob.State):
            Output only. Backfill job state.
        trigger (google.cloud.datastream_v1.types.BackfillJob.Trigger):
            Backfill job's triggering reason.
        last_start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Backfill job's start time.
        last_end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Backfill job's end time.
        errors (MutableSequence[google.cloud.datastream_v1.types.Error]):
            Output only. Errors which caused the backfill
            job to fail.
    """

    class State(proto.Enum):
        r"""State of the stream object's backfill job.

        Values:
            STATE_UNSPECIFIED (0):
                Default value.
            NOT_STARTED (1):
                Backfill job was never started for the stream
                object (stream has backfill strategy defined as
                manual or object was explicitly excluded from
                automatic backfill).
            PENDING (2):
                Backfill job will start pending available
                resources.
            ACTIVE (3):
                Backfill job is running.
            STOPPED (4):
                Backfill job stopped (next job run will start
                from beginning).
            FAILED (5):
                Backfill job failed (due to an error).
            COMPLETED (6):
                Backfill completed successfully.
            UNSUPPORTED (7):
                Backfill job failed since the table structure
                is currently unsupported for backfill.
        """
        STATE_UNSPECIFIED = 0
        NOT_STARTED = 1
        PENDING = 2
        ACTIVE = 3
        STOPPED = 4
        FAILED = 5
        COMPLETED = 6
        UNSUPPORTED = 7

    class Trigger(proto.Enum):
        r"""Triggering reason for a backfill job.

        Values:
            TRIGGER_UNSPECIFIED (0):
                Default value.
            AUTOMATIC (1):
                Object backfill job was triggered
                automatically according to the stream's backfill
                strategy.
            MANUAL (2):
                Object backfill job was triggered manually
                using the dedicated API.
        """
        TRIGGER_UNSPECIFIED = 0
        AUTOMATIC = 1
        MANUAL = 2

    state: State = proto.Field(
        proto.ENUM,
        number=1,
        enum=State,
    )
    trigger: Trigger = proto.Field(
        proto.ENUM,
        number=2,
        enum=Trigger,
    )
    last_start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    last_end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    errors: MutableSequence["Error"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="Error",
    )


class Error(proto.Message):
    r"""Represent a user-facing Error.

    Attributes:
        reason (str):
            A title that explains the reason for the
            error.
        error_uuid (str):
            A unique identifier for this specific error,
            allowing it to be traced throughout the system
            in logs and API responses.
        message (str):
            A message containing more information about
            the error that occurred.
        error_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the error occurred.
        details (MutableMapping[str, str]):
            Additional information about the error.
    """

    reason: str = proto.Field(
        proto.STRING,
        number=1,
    )
    error_uuid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    message: str = proto.Field(
        proto.STRING,
        number=3,
    )
    error_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    details: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )


class ValidationResult(proto.Message):
    r"""Contains the current validation results.

    Attributes:
        validations (MutableSequence[google.cloud.datastream_v1.types.Validation]):
            A list of validations (includes both executed
            as well as not executed validations).
    """

    validations: MutableSequence["Validation"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Validation",
    )


class Validation(proto.Message):
    r"""A validation to perform on a stream.

    Attributes:
        description (str):
            A short description of the validation.
        state (google.cloud.datastream_v1.types.Validation.State):
            Output only. Validation execution status.
        message (MutableSequence[google.cloud.datastream_v1.types.ValidationMessage]):
            Messages reflecting the validation results.
        code (str):
            A custom code identifying this validation.
    """

    class State(proto.Enum):
        r"""Validation execution state.

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified state.
            NOT_EXECUTED (1):
                Validation did not execute.
            FAILED (2):
                Validation failed.
            PASSED (3):
                Validation passed.
            WARNING (4):
                Validation executed with warnings.
        """
        STATE_UNSPECIFIED = 0
        NOT_EXECUTED = 1
        FAILED = 2
        PASSED = 3
        WARNING = 4

    description: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )
    message: MutableSequence["ValidationMessage"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="ValidationMessage",
    )
    code: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ValidationMessage(proto.Message):
    r"""Represent user-facing validation result message.

    Attributes:
        message (str):
            The result of the validation.
        level (google.cloud.datastream_v1.types.ValidationMessage.Level):
            Message severity level (warning or error).
        metadata (MutableMapping[str, str]):
            Additional metadata related to the result.
        code (str):
            A custom code identifying this specific
            message.
    """

    class Level(proto.Enum):
        r"""Validation message level.

        Values:
            LEVEL_UNSPECIFIED (0):
                Unspecified level.
            WARNING (1):
                Potentially cause issues with the Stream.
            ERROR (2):
                Definitely cause issues with the Stream.
        """
        LEVEL_UNSPECIFIED = 0
        WARNING = 1
        ERROR = 2

    message: str = proto.Field(
        proto.STRING,
        number=1,
    )
    level: Level = proto.Field(
        proto.ENUM,
        number=2,
        enum=Level,
    )
    metadata: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )
    code: str = proto.Field(
        proto.STRING,
        number=4,
    )


class CdcStrategy(proto.Message):
    r"""The strategy that the stream uses for CDC replication.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        most_recent_start_position (google.cloud.datastream_v1.types.CdcStrategy.MostRecentStartPosition):
            Optional. Start replicating from the most
            recent position in the source.

            This field is a member of `oneof`_ ``start_position``.
        next_available_start_position (google.cloud.datastream_v1.types.CdcStrategy.NextAvailableStartPosition):
            Optional. Resume replication from the next
            available position in the source.

            This field is a member of `oneof`_ ``start_position``.
        specific_start_position (google.cloud.datastream_v1.types.CdcStrategy.SpecificStartPosition):
            Optional. Start replicating from a specific
            position in the source.

            This field is a member of `oneof`_ ``start_position``.
    """

    class MostRecentStartPosition(proto.Message):
        r"""CDC strategy to start replicating from the most recent
        position in the source.

        """

    class NextAvailableStartPosition(proto.Message):
        r"""CDC strategy to resume replication from the next available
        position in the source.

        """

    class SpecificStartPosition(proto.Message):
        r"""CDC strategy to start replicating from a specific position in
        the source.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            mysql_log_position (google.cloud.datastream_v1.types.MysqlLogPosition):
                MySQL specific log position to start
                replicating from.

                This field is a member of `oneof`_ ``position``.
            oracle_scn_position (google.cloud.datastream_v1.types.OracleScnPosition):
                Oracle SCN to start replicating from.

                This field is a member of `oneof`_ ``position``.
            sql_server_lsn_position (google.cloud.datastream_v1.types.SqlServerLsnPosition):
                SqlServer LSN to start replicating from.

                This field is a member of `oneof`_ ``position``.
        """

        mysql_log_position: "MysqlLogPosition" = proto.Field(
            proto.MESSAGE,
            number=101,
            oneof="position",
            message="MysqlLogPosition",
        )
        oracle_scn_position: "OracleScnPosition" = proto.Field(
            proto.MESSAGE,
            number=102,
            oneof="position",
            message="OracleScnPosition",
        )
        sql_server_lsn_position: "SqlServerLsnPosition" = proto.Field(
            proto.MESSAGE,
            number=103,
            oneof="position",
            message="SqlServerLsnPosition",
        )

    most_recent_start_position: MostRecentStartPosition = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="start_position",
        message=MostRecentStartPosition,
    )
    next_available_start_position: NextAvailableStartPosition = proto.Field(
        proto.MESSAGE,
        number=102,
        oneof="start_position",
        message=NextAvailableStartPosition,
    )
    specific_start_position: SpecificStartPosition = proto.Field(
        proto.MESSAGE,
        number=103,
        oneof="start_position",
        message=SpecificStartPosition,
    )


class SqlServerLsnPosition(proto.Message):
    r"""SQL Server LSN position

    Attributes:
        lsn (str):
            Required. Log sequence number (LSN) from
            where Logs will be read
    """

    lsn: str = proto.Field(
        proto.STRING,
        number=1,
    )


class OracleScnPosition(proto.Message):
    r"""Oracle SCN position

    Attributes:
        scn (int):
            Required. SCN number from where Logs will be
            read
    """

    scn: int = proto.Field(
        proto.INT64,
        number=1,
    )


class MysqlLogPosition(proto.Message):
    r"""MySQL log position

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        log_file (str):
            Required. The binary log file name.
        log_position (int):
            Optional. The position within the binary log
            file. Default is head of file.

            This field is a member of `oneof`_ ``_log_position``.
    """

    log_file: str = proto.Field(
        proto.STRING,
        number=1,
    )
    log_position: int = proto.Field(
        proto.INT32,
        number=2,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
