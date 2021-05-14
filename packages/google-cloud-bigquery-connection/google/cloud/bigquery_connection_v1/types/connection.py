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

from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.connection.v1",
    manifest={
        "CreateConnectionRequest",
        "GetConnectionRequest",
        "ListConnectionsRequest",
        "ListConnectionsResponse",
        "UpdateConnectionRequest",
        "DeleteConnectionRequest",
        "Connection",
        "CloudSqlProperties",
        "CloudSqlCredential",
        "AwsProperties",
        "AwsCrossAccountRole",
    },
)


class CreateConnectionRequest(proto.Message):
    r"""The request for
    [ConnectionService.CreateConnection][google.cloud.bigquery.connection.v1.ConnectionService.CreateConnection].

    Attributes:
        parent (str):
            Required. Parent resource name. Must be in the format
            ``projects/{project_id}/locations/{location_id}``
        connection_id (str):
            Optional. Connection id that should be
            assigned to the created connection.
        connection (google.cloud.bigquery_connection_v1.types.Connection):
            Required. Connection to create.
    """

    parent = proto.Field(proto.STRING, number=1,)
    connection_id = proto.Field(proto.STRING, number=2,)
    connection = proto.Field(proto.MESSAGE, number=3, message="Connection",)


class GetConnectionRequest(proto.Message):
    r"""The request for
    [ConnectionService.GetConnection][google.cloud.bigquery.connection.v1.ConnectionService.GetConnection].

    Attributes:
        name (str):
            Required. Name of the requested connection, for example:
            ``projects/{project_id}/locations/{location_id}/connections/{connection_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class ListConnectionsRequest(proto.Message):
    r"""The request for
    [ConnectionService.ListConnections][google.cloud.bigquery.connection.v1.ConnectionService.ListConnections].

    Attributes:
        parent (str):
            Required. Parent resource name. Must be in the form:
            ``projects/{project_id}/locations/{location_id}``
        page_size (int):
            Required. Page size.
        page_token (str):
            Page token.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=4,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListConnectionsResponse(proto.Message):
    r"""The response for
    [ConnectionService.ListConnections][google.cloud.bigquery.connection.v1.ConnectionService.ListConnections].

    Attributes:
        next_page_token (str):
            Next page token.
        connections (Sequence[google.cloud.bigquery_connection_v1.types.Connection]):
            List of connections.
    """

    @property
    def raw_page(self):
        return self

    next_page_token = proto.Field(proto.STRING, number=1,)
    connections = proto.RepeatedField(proto.MESSAGE, number=2, message="Connection",)


class UpdateConnectionRequest(proto.Message):
    r"""The request for
    [ConnectionService.UpdateConnection][google.cloud.bigquery.connection.v1.ConnectionService.UpdateConnection].

    Attributes:
        name (str):
            Required. Name of the connection to update, for example:
            ``projects/{project_id}/locations/{location_id}/connections/{connection_id}``
        connection (google.cloud.bigquery_connection_v1.types.Connection):
            Required. Connection containing the updated
            fields.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Update mask for the connection
            fields to be updated.
    """

    name = proto.Field(proto.STRING, number=1,)
    connection = proto.Field(proto.MESSAGE, number=2, message="Connection",)
    update_mask = proto.Field(
        proto.MESSAGE, number=3, message=field_mask_pb2.FieldMask,
    )


class DeleteConnectionRequest(proto.Message):
    r"""The request for [ConnectionService.DeleteConnectionRequest][].
    Attributes:
        name (str):
            Required. Name of the deleted connection, for example:
            ``projects/{project_id}/locations/{location_id}/connections/{connection_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class Connection(proto.Message):
    r"""Configuration parameters to establish connection with an
    external data source, except the credential attributes.

    Attributes:
        name (str):
            The resource name of the connection in the form of:
            ``projects/{project_id}/locations/{location_id}/connections/{connection_id}``
        friendly_name (str):
            User provided display name for the
            connection.
        description (str):
            User provided description.
        cloud_sql (google.cloud.bigquery_connection_v1.types.CloudSqlProperties):
            Cloud SQL properties.
        aws (google.cloud.bigquery_connection_v1.types.AwsProperties):
            Amazon Web Services (AWS) properties.
        creation_time (int):
            Output only. The creation timestamp of the
            connection.
        last_modified_time (int):
            Output only. The last update timestamp of the
            connection.
        has_credential (bool):
            Output only. True, if credential is
            configured for this connection.
    """

    name = proto.Field(proto.STRING, number=1,)
    friendly_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    cloud_sql = proto.Field(
        proto.MESSAGE, number=4, oneof="properties", message="CloudSqlProperties",
    )
    aws = proto.Field(
        proto.MESSAGE, number=8, oneof="properties", message="AwsProperties",
    )
    creation_time = proto.Field(proto.INT64, number=5,)
    last_modified_time = proto.Field(proto.INT64, number=6,)
    has_credential = proto.Field(proto.BOOL, number=7,)


class CloudSqlProperties(proto.Message):
    r"""Connection properties specific to the Cloud SQL.
    Attributes:
        instance_id (str):
            Cloud SQL instance ID in the form
            ``project:location:instance``.
        database (str):
            Database name.
        type_ (google.cloud.bigquery_connection_v1.types.CloudSqlProperties.DatabaseType):
            Type of the Cloud SQL database.
        credential (google.cloud.bigquery_connection_v1.types.CloudSqlCredential):
            Input only. Cloud SQL credential.
    """

    class DatabaseType(proto.Enum):
        r"""Supported Cloud SQL database types."""
        DATABASE_TYPE_UNSPECIFIED = 0
        POSTGRES = 1
        MYSQL = 2

    instance_id = proto.Field(proto.STRING, number=1,)
    database = proto.Field(proto.STRING, number=2,)
    type_ = proto.Field(proto.ENUM, number=3, enum=DatabaseType,)
    credential = proto.Field(proto.MESSAGE, number=4, message="CloudSqlCredential",)


class CloudSqlCredential(proto.Message):
    r"""Credential info for the Cloud SQL.
    Attributes:
        username (str):
            The username for the credential.
        password (str):
            The password for the credential.
    """

    username = proto.Field(proto.STRING, number=1,)
    password = proto.Field(proto.STRING, number=2,)


class AwsProperties(proto.Message):
    r"""Connection properties specific to Amazon Web Services (AWS).
    Attributes:
        cross_account_role (google.cloud.bigquery_connection_v1.types.AwsCrossAccountRole):
            Authentication using Google owned AWS IAM
            user's access key to assume into customer's AWS
            IAM Role.
    """

    cross_account_role = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="authentication_method",
        message="AwsCrossAccountRole",
    )


class AwsCrossAccountRole(proto.Message):
    r"""Authentication method for Amazon Web Services (AWS) that uses
    Google owned AWS IAM user's access key to assume into customer's
    AWS IAM Role.

    Attributes:
        iam_role_id (str):
            The user’s AWS IAM Role that trusts the
            Google-owned AWS IAM user Connection.
        iam_user_id (str):
            Output only. Google-owned AWS IAM User for a
            Connection.
        external_id (str):
            Output only. A Google-generated id for representing
            Connection’s identity in AWS. External Id is also used for
            preventing the Confused Deputy Problem. See
            https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html
    """

    iam_role_id = proto.Field(proto.STRING, number=1,)
    iam_user_id = proto.Field(proto.STRING, number=2,)
    external_id = proto.Field(proto.STRING, number=3,)


__all__ = tuple(sorted(__protobuf__.manifest))
