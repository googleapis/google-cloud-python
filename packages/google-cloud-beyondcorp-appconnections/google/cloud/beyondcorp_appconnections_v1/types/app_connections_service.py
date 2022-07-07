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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.beyondcorp.appconnections.v1",
    manifest={
        "ListAppConnectionsRequest",
        "ListAppConnectionsResponse",
        "GetAppConnectionRequest",
        "CreateAppConnectionRequest",
        "UpdateAppConnectionRequest",
        "DeleteAppConnectionRequest",
        "ResolveAppConnectionsRequest",
        "ResolveAppConnectionsResponse",
        "AppConnection",
        "AppConnectionOperationMetadata",
    },
)


class ListAppConnectionsRequest(proto.Message):
    r"""Request message for BeyondCorp.ListAppConnections.

    Attributes:
        parent (str):
            Required. The resource name of the AppConnection location
            using the form:
            ``projects/{project_id}/locations/{location_id}``
        page_size (int):
            Optional. The maximum number of items to return. If not
            specified, a default value of 50 will be used by the
            service. Regardless of the page_size value, the response may
            include a partial list and a caller should only rely on
            response's
            [next_page_token][BeyondCorp.ListAppConnectionsResponse.next_page_token]
            to determine if there are more instances left to be queried.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            ListAppConnectionsRequest, if any.
        filter (str):
            Optional. A filter specifying constraints of
            a list operation.
        order_by (str):
            Optional. Specifies the ordering of results. See `Sorting
            order <https://cloud.google.com/apis/design/design_patterns#sorting_order>`__
            for more information.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    filter = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by = proto.Field(
        proto.STRING,
        number=5,
    )


class ListAppConnectionsResponse(proto.Message):
    r"""Response message for BeyondCorp.ListAppConnections.

    Attributes:
        app_connections (Sequence[google.cloud.beyondcorp_appconnections_v1.types.AppConnection]):
            A list of BeyondCorp AppConnections in the
            project.
        next_page_token (str):
            A token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (Sequence[str]):
            A list of locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    app_connections = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AppConnection",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetAppConnectionRequest(proto.Message):
    r"""Request message for BeyondCorp.GetAppConnection.

    Attributes:
        name (str):
            Required. BeyondCorp AppConnection name using the form:
            ``projects/{project_id}/locations/{location_id}/appConnections/{app_connection_id}``
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateAppConnectionRequest(proto.Message):
    r"""Request message for BeyondCorp.CreateAppConnection.

    Attributes:
        parent (str):
            Required. The resource project name of the AppConnection
            location using the form:
            ``projects/{project_id}/locations/{location_id}``
        app_connection_id (str):
            Optional. User-settable AppConnection resource ID.

            -  Must start with a letter.
            -  Must contain between 4-63 characters from
               ``/[a-z][0-9]-/``.
            -  Must end with a number or a letter.
        app_connection (google.cloud.beyondcorp_appconnections_v1.types.AppConnection):
            Required. A BeyondCorp AppConnection
            resource.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set, validates request by
            executing a dry-run which would not alter the
            resource in any way.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    app_connection_id = proto.Field(
        proto.STRING,
        number=2,
    )
    app_connection = proto.Field(
        proto.MESSAGE,
        number=3,
        message="AppConnection",
    )
    request_id = proto.Field(
        proto.STRING,
        number=4,
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=5,
    )


class UpdateAppConnectionRequest(proto.Message):
    r"""Request message for BeyondCorp.UpdateAppConnection.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update. At least one path must
            be supplied in this field. The elements of the repeated
            paths field may only include these fields from
            [BeyondCorp.AppConnection]:

            -  ``labels``
            -  ``display_name``
            -  ``application_endpoint``
            -  ``connectors``
        app_connection (google.cloud.beyondcorp_appconnections_v1.types.AppConnection):
            Required. AppConnection message with updated fields. Only
            supported fields specified in update_mask are updated.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set, validates request by
            executing a dry-run which would not alter the
            resource in any way.
        allow_missing (bool):
            Optional. If set as true, will create the
            resource if it is not found.
    """

    update_mask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    app_connection = proto.Field(
        proto.MESSAGE,
        number=2,
        message="AppConnection",
    )
    request_id = proto.Field(
        proto.STRING,
        number=3,
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=4,
    )
    allow_missing = proto.Field(
        proto.BOOL,
        number=5,
    )


class DeleteAppConnectionRequest(proto.Message):
    r"""Request message for BeyondCorp.DeleteAppConnection.

    Attributes:
        name (str):
            Required. BeyondCorp Connector name using the form:
            ``projects/{project_id}/locations/{location_id}/appConnections/{app_connection_id}``
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set, validates request by
            executing a dry-run which would not alter the
            resource in any way.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id = proto.Field(
        proto.STRING,
        number=2,
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=3,
    )


class ResolveAppConnectionsRequest(proto.Message):
    r"""Request message for BeyondCorp.ResolveAppConnections.

    Attributes:
        parent (str):
            Required. The resource name of the AppConnection location
            using the form:
            ``projects/{project_id}/locations/{location_id}``
        app_connector_id (str):
            Required. BeyondCorp Connector name of the connector
            associated with those AppConnections using the form:
            ``projects/{project_id}/locations/{location_id}/appConnectors/{app_connector_id}``
        page_size (int):
            Optional. The maximum number of items to return. If not
            specified, a default value of 50 will be used by the
            service. Regardless of the page_size value, the response may
            include a partial list and a caller should only rely on
            response's
            [next_page_token][BeyondCorp.ResolveAppConnectionsResponse.next_page_token]
            to determine if there are more instances left to be queried.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            ResolveAppConnectionsResponse, if any.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    app_connector_id = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token = proto.Field(
        proto.STRING,
        number=4,
    )


class ResolveAppConnectionsResponse(proto.Message):
    r"""Response message for BeyondCorp.ResolveAppConnections.

    Attributes:
        app_connection_details (Sequence[google.cloud.beyondcorp_appconnections_v1.types.ResolveAppConnectionsResponse.AppConnectionDetails]):
            A list of BeyondCorp AppConnections with
            details in the project.
        next_page_token (str):
            A token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (Sequence[str]):
            A list of locations that could not be
            reached.
    """

    class AppConnectionDetails(proto.Message):
        r"""Details of the AppConnection.

        Attributes:
            app_connection (google.cloud.beyondcorp_appconnections_v1.types.AppConnection):
                A BeyondCorp AppConnection in the project.
            recent_mig_vms (Sequence[str]):
                If type=GCP_REGIONAL_MIG, contains most recent VM instances,
                like
                ``https://www.googleapis.com/compute/v1/projects/{project_id}/zones/{zone_id}/instances/{instance_id}``.
        """

        app_connection = proto.Field(
            proto.MESSAGE,
            number=1,
            message="AppConnection",
        )
        recent_mig_vms = proto.RepeatedField(
            proto.STRING,
            number=2,
        )

    @property
    def raw_page(self):
        return self

    app_connection_details = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=AppConnectionDetails,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class AppConnection(proto.Message):
    r"""A BeyondCorp AppConnection resource represents a BeyondCorp
    protected AppConnection to a remote application. It creates all
    the necessary GCP components needed for creating a BeyondCorp
    protected AppConnection. Multiple connectors can be authorised
    for a single AppConnection.

    Attributes:
        name (str):
            Required. Unique resource name of the
            AppConnection. The name is ignored when creating
            a AppConnection.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the resource was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the resource was
            last modified.
        labels (Mapping[str, str]):
            Optional. Resource labels to represent user
            provided metadata.
        display_name (str):
            Optional. An arbitrary user-provided name for
            the AppConnection. Cannot exceed 64 characters.
        uid (str):
            Output only. A unique identifier for the
            instance generated by the system.
        type_ (google.cloud.beyondcorp_appconnections_v1.types.AppConnection.Type):
            Required. The type of network connectivity
            used by the AppConnection.
        application_endpoint (google.cloud.beyondcorp_appconnections_v1.types.AppConnection.ApplicationEndpoint):
            Required. Address of the remote application
            endpoint for the BeyondCorp AppConnection.
        connectors (Sequence[str]):
            Optional. List of
            [google.cloud.beyondcorp.v1main.Connector.name] that are
            authorised to be associated with this AppConnection.
        state (google.cloud.beyondcorp_appconnections_v1.types.AppConnection.State):
            Output only. The current state of the
            AppConnection.
        gateway (google.cloud.beyondcorp_appconnections_v1.types.AppConnection.Gateway):
            Optional. Gateway used by the AppConnection.
    """

    class Type(proto.Enum):
        r"""Enum containing list of all possible network connectivity
        options supported by BeyondCorp AppConnection.
        """
        TYPE_UNSPECIFIED = 0
        TCP_PROXY = 1

    class State(proto.Enum):
        r"""Represents the different states of a AppConnection."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        CREATED = 2
        UPDATING = 3
        DELETING = 4
        DOWN = 5

    class ApplicationEndpoint(proto.Message):
        r"""ApplicationEndpoint represents a remote application endpoint.

        Attributes:
            host (str):
                Required. Hostname or IP address of the
                remote application endpoint.
            port (int):
                Required. Port of the remote application
                endpoint.
        """

        host = proto.Field(
            proto.STRING,
            number=1,
        )
        port = proto.Field(
            proto.INT32,
            number=2,
        )

    class Gateway(proto.Message):
        r"""Gateway represents a user facing component that serves as an
        entrance to enable connectivity.

        Attributes:
            type_ (google.cloud.beyondcorp_appconnections_v1.types.AppConnection.Gateway.Type):
                Required. The type of hosting used by the
                gateway.
            uri (str):
                Output only. Server-defined URI for this
                resource.
            ingress_port (int):
                Output only. Ingress port reserved on the
                gateways for this AppConnection, if not
                specified or zero, the default port is 19443.
            app_gateway (str):
                Required. AppGateway name in following format:
                ``projects/{project_id}/locations/{location_id}/appgateways/{gateway_id}``
        """

        class Type(proto.Enum):
            r"""Enum listing possible gateway hosting options."""
            TYPE_UNSPECIFIED = 0
            GCP_REGIONAL_MIG = 1

        type_ = proto.Field(
            proto.ENUM,
            number=2,
            enum="AppConnection.Gateway.Type",
        )
        uri = proto.Field(
            proto.STRING,
            number=3,
        )
        ingress_port = proto.Field(
            proto.INT32,
            number=4,
        )
        app_gateway = proto.Field(
            proto.STRING,
            number=5,
        )

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    display_name = proto.Field(
        proto.STRING,
        number=5,
    )
    uid = proto.Field(
        proto.STRING,
        number=6,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=7,
        enum=Type,
    )
    application_endpoint = proto.Field(
        proto.MESSAGE,
        number=8,
        message=ApplicationEndpoint,
    )
    connectors = proto.RepeatedField(
        proto.STRING,
        number=9,
    )
    state = proto.Field(
        proto.ENUM,
        number=10,
        enum=State,
    )
    gateway = proto.Field(
        proto.MESSAGE,
        number=11,
        message=Gateway,
    )


class AppConnectionOperationMetadata(proto.Message):
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
            cancellation of the operation. Operations that have
            successfully been cancelled have [Operation.error][] value
            with a [google.rpc.Status.code][google.rpc.Status.code] of
            1, corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
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
    verb = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version = proto.Field(
        proto.STRING,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
