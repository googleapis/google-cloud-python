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
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.networkservices.v1",
    manifest={
        "EventType",
        "LoadBalancingScheme",
        "ExtensionChain",
        "LbTrafficExtension",
        "ListLbTrafficExtensionsRequest",
        "ListLbTrafficExtensionsResponse",
        "GetLbTrafficExtensionRequest",
        "CreateLbTrafficExtensionRequest",
        "UpdateLbTrafficExtensionRequest",
        "DeleteLbTrafficExtensionRequest",
        "LbRouteExtension",
        "ListLbRouteExtensionsRequest",
        "ListLbRouteExtensionsResponse",
        "GetLbRouteExtensionRequest",
        "CreateLbRouteExtensionRequest",
        "UpdateLbRouteExtensionRequest",
        "DeleteLbRouteExtensionRequest",
    },
)


class EventType(proto.Enum):
    r"""The part of the request or response for which the extension
    is called.

    Values:
        EVENT_TYPE_UNSPECIFIED (0):
            Unspecified value. Do not use.
        REQUEST_HEADERS (1):
            If included in ``supported_events``, the extension is called
            when the HTTP request headers arrive.
        REQUEST_BODY (2):
            If included in ``supported_events``, the extension is called
            when the HTTP request body arrives.
        RESPONSE_HEADERS (3):
            If included in ``supported_events``, the extension is called
            when the HTTP response headers arrive.
        RESPONSE_BODY (4):
            If included in ``supported_events``, the extension is called
            when the HTTP response body arrives.
        REQUEST_TRAILERS (5):
            If included in ``supported_events``, the extension is called
            when the HTTP request trailers arrives.
        RESPONSE_TRAILERS (6):
            If included in ``supported_events``, the extension is called
            when the HTTP response trailers arrives.
    """
    EVENT_TYPE_UNSPECIFIED = 0
    REQUEST_HEADERS = 1
    REQUEST_BODY = 2
    RESPONSE_HEADERS = 3
    RESPONSE_BODY = 4
    REQUEST_TRAILERS = 5
    RESPONSE_TRAILERS = 6


class LoadBalancingScheme(proto.Enum):
    r"""Load balancing schemes supported by the ``LbTrafficExtension``
    resource and ``LbRouteExtension`` resource. For more information,
    refer to `Choosing a load
    balancer <https://cloud.google.com/load-balancing/docs/backend-service>`__.

    Values:
        LOAD_BALANCING_SCHEME_UNSPECIFIED (0):
            Default value. Do not use.
        INTERNAL_MANAGED (1):
            Signifies that this is used for Internal
            HTTP(S) Load Balancing.
        EXTERNAL_MANAGED (2):
            Signifies that this is used for External
            Managed HTTP(S) Load Balancing.
    """
    LOAD_BALANCING_SCHEME_UNSPECIFIED = 0
    INTERNAL_MANAGED = 1
    EXTERNAL_MANAGED = 2


class ExtensionChain(proto.Message):
    r"""A single extension chain wrapper that contains the match
    conditions and extensions to execute.

    Attributes:
        name (str):
            Required. The name for this extension chain.
            The name is logged as part of the HTTP request
            logs. The name must conform with RFC-1034, is
            restricted to lower-cased letters, numbers and
            hyphens, and can have a maximum length of 63
            characters. Additionally, the first character
            must be a letter and the last a letter or a
            number.
        match_condition (google.cloud.network_services_v1.types.ExtensionChain.MatchCondition):
            Required. Conditions under which this chain
            is invoked for a request.
        extensions (MutableSequence[google.cloud.network_services_v1.types.ExtensionChain.Extension]):
            Required. A set of extensions to execute for the matching
            request. At least one extension is required. Up to 3
            extensions can be defined for each extension chain for
            ``LbTrafficExtension`` resource. ``LbRouteExtension`` chains
            are limited to 1 extension per extension chain.
    """

    class MatchCondition(proto.Message):
        r"""Conditions under which this chain is invoked for a request.

        Attributes:
            cel_expression (str):
                Required. A Common Expression Language (CEL) expression that
                is used to match requests for which the extension chain is
                executed.

                For more information, see `CEL matcher language
                reference <https://cloud.google.com/service-extensions/docs/cel-matcher-language-reference>`__.
        """

        cel_expression: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class Extension(proto.Message):
        r"""A single extension in the chain to execute for the matching
        request.

        Attributes:
            name (str):
                Required. The name for this extension.
                The name is logged as part of the HTTP request
                logs. The name must conform with RFC-1034, is
                restricted to lower-cased letters, numbers and
                hyphens, and can have a maximum length of 63
                characters. Additionally, the first character
                must be a letter and the last a letter or a
                number.
            authority (str):
                Optional. The ``:authority`` header in the gRPC request sent
                from Envoy to the extension service. Required for Callout
                extensions.
            service (str):
                Required. The reference to the service that runs the
                extension.

                Currently only callout extensions are supported here.

                To configure a callout extension, ``service`` must be a
                fully-qualified reference to a `backend
                service <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`__
                in the format:
                ``https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/backendServices/{backendService}``
                or
                ``https://www.googleapis.com/compute/v1/projects/{project}/global/backendServices/{backendService}``.
            supported_events (MutableSequence[google.cloud.network_services_v1.types.EventType]):
                Optional. A set of events during request or response
                processing for which this extension is called. This field is
                required for the ``LbTrafficExtension`` resource. It must
                not be set for the ``LbRouteExtension`` resource.
            timeout (google.protobuf.duration_pb2.Duration):
                Optional. Specifies the timeout for each
                individual message on the stream. The timeout
                must be between 10-1000 milliseconds. Required
                for Callout extensions.
            fail_open (bool):
                Optional. Determines how the proxy behaves if the call to
                the extension fails or times out.

                When set to ``TRUE``, request or response processing
                continues without error. Any subsequent extensions in the
                extension chain are also executed. When set to ``FALSE`` or
                the default setting of ``FALSE`` is used, one of the
                following happens:

                -  If response headers have not been delivered to the
                   downstream client, a generic 500 error is returned to the
                   client. The error response can be tailored by configuring
                   a custom error response in the load balancer.

                -  If response headers have been delivered, then the HTTP
                   stream to the downstream client is reset.
            forward_headers (MutableSequence[str]):
                Optional. List of the HTTP headers to forward
                to the extension (from the client or backend).
                If omitted, all headers are sent. Each element
                is a string indicating the header name.
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        authority: str = proto.Field(
            proto.STRING,
            number=2,
        )
        service: str = proto.Field(
            proto.STRING,
            number=3,
        )
        supported_events: MutableSequence["EventType"] = proto.RepeatedField(
            proto.ENUM,
            number=4,
            enum="EventType",
        )
        timeout: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=5,
            message=duration_pb2.Duration,
        )
        fail_open: bool = proto.Field(
            proto.BOOL,
            number=6,
        )
        forward_headers: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=7,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    match_condition: MatchCondition = proto.Field(
        proto.MESSAGE,
        number=2,
        message=MatchCondition,
    )
    extensions: MutableSequence[Extension] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=Extension,
    )


class LbTrafficExtension(proto.Message):
    r"""``LbTrafficExtension`` is a resource that lets the extension service
    modify the headers and payloads of both requests and responses
    without impacting the choice of backend services or any other
    security policies associated with the backend service.

    Attributes:
        name (str):
            Required. Identifier. Name of the ``LbTrafficExtension``
            resource in the following format:
            ``projects/{project}/locations/{location}/lbTrafficExtensions/{lb_traffic_extension}``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the resource
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the resource
            was updated.
        description (str):
            Optional. A human-readable description of the
            resource.
        labels (MutableMapping[str, str]):
            Optional. Set of labels associated with the
            ``LbTrafficExtension`` resource.

            The format must comply with `the requirements for
            labels <https://cloud.google.com/compute/docs/labeling-resources#requirements>`__
            for Google Cloud resources.
        forwarding_rules (MutableSequence[str]):
            Required. A list of references to the forwarding rules to
            which this service extension is attached to. At least one
            forwarding rule is required. There can be only one
            ``LBTrafficExtension`` resource per forwarding rule.
        extension_chains (MutableSequence[google.cloud.network_services_v1.types.ExtensionChain]):
            Required. A set of ordered extension chains
            that contain the match conditions and extensions
            to execute. Match conditions for each extension
            chain are evaluated in sequence for a given
            request. The first extension chain that has a
            condition that matches the request is executed.
            Any subsequent extension chains do not execute.
            Limited to 5 extension chains per resource.
        load_balancing_scheme (google.cloud.network_services_v1.types.LoadBalancingScheme):
            Required. All backend services and forwarding rules
            referenced by this extension must share the same load
            balancing scheme. Supported values: ``INTERNAL_MANAGED``,
            ``EXTERNAL_MANAGED``. For more information, refer to
            `Choosing a load
            balancer <https://cloud.google.com/load-balancing/docs/backend-service>`__.
        metadata (google.protobuf.struct_pb2.Struct):
            Optional. The metadata provided here is included in the
            ``ProcessingRequest.metadata_context.filter_metadata`` map
            field. The metadata is available under the key
            ``com.google.lb_traffic_extension.<resource_name>``. The
            following variables are supported in the metadata:

            ``{forwarding_rule_id}`` - substituted with the forwarding
            rule's fully qualified resource name.
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
    description: str = proto.Field(
        proto.STRING,
        number=9,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    forwarding_rules: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    extension_chains: MutableSequence["ExtensionChain"] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="ExtensionChain",
    )
    load_balancing_scheme: "LoadBalancingScheme" = proto.Field(
        proto.ENUM,
        number=8,
        enum="LoadBalancingScheme",
    )
    metadata: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=10,
        message=struct_pb2.Struct,
    )


class ListLbTrafficExtensionsRequest(proto.Message):
    r"""Message for requesting list of ``LbTrafficExtension`` resources.

    Attributes:
        parent (str):
            Required. The project and location from which the
            ``LbTrafficExtension`` resources are listed, specified in
            the following format:
            ``projects/{project}/locations/{location}``.
        page_size (int):
            Optional. Requested page size. The server
            might return fewer items than requested. If
            unspecified, the server picks an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results that the server returns.
        filter (str):
            Optional. Filtering results.
        order_by (str):
            Optional. Hint for how to order the results.
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


class ListLbTrafficExtensionsResponse(proto.Message):
    r"""Message for response to listing ``LbTrafficExtension`` resources.

    Attributes:
        lb_traffic_extensions (MutableSequence[google.cloud.network_services_v1.types.LbTrafficExtension]):
            The list of ``LbTrafficExtension`` resources.
        next_page_token (str):
            A token identifying a page of results that
            the server returns.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    lb_traffic_extensions: MutableSequence["LbTrafficExtension"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="LbTrafficExtension",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetLbTrafficExtensionRequest(proto.Message):
    r"""Message for getting a ``LbTrafficExtension`` resource.

    Attributes:
        name (str):
            Required. A name of the ``LbTrafficExtension`` resource to
            get. Must be in the format
            ``projects/{project}/locations/{location}/lbTrafficExtensions/{lb_traffic_extension}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateLbTrafficExtensionRequest(proto.Message):
    r"""Message for creating a ``LbTrafficExtension`` resource.

    Attributes:
        parent (str):
            Required. The parent resource of the ``LbTrafficExtension``
            resource. Must be in the format
            ``projects/{project}/locations/{location}``.
        lb_traffic_extension_id (str):
            Required. User-provided ID of the ``LbTrafficExtension``
            resource to be created.
        lb_traffic_extension (google.cloud.network_services_v1.types.LbTrafficExtension):
            Required. ``LbTrafficExtension`` resource to be created.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server can
            ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, ignores the second request. This prevents
            clients from accidentally creating duplicate
            commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    lb_traffic_extension_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    lb_traffic_extension: "LbTrafficExtension" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="LbTrafficExtension",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateLbTrafficExtensionRequest(proto.Message):
    r"""Message for updating a ``LbTrafficExtension`` resource.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Used to specify the fields to be overwritten in
            the ``LbTrafficExtension`` resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request. A field is overwritten if it
            is in the mask. If the user does not specify a mask, then
            all fields are overwritten.
        lb_traffic_extension (google.cloud.network_services_v1.types.LbTrafficExtension):
            Required. ``LbTrafficExtension`` resource being updated.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server can
            ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, ignores the second request. This prevents
            clients from accidentally creating duplicate
            commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    lb_traffic_extension: "LbTrafficExtension" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="LbTrafficExtension",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteLbTrafficExtensionRequest(proto.Message):
    r"""Message for deleting a ``LbTrafficExtension`` resource.

    Attributes:
        name (str):
            Required. The name of the ``LbTrafficExtension`` resource to
            delete. Must be in the format
            ``projects/{project}/locations/{location}/lbTrafficExtensions/{lb_traffic_extension}``.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server can
            ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, ignores the second request. This prevents
            clients from accidentally creating duplicate
            commitments.

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


class LbRouteExtension(proto.Message):
    r"""``LbRouteExtension`` is a resource that lets you control where
    traffic is routed to for a given request.

    Attributes:
        name (str):
            Required. Identifier. Name of the ``LbRouteExtension``
            resource in the following format:
            ``projects/{project}/locations/{location}/lbRouteExtensions/{lb_route_extension}``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the resource
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the resource
            was updated.
        description (str):
            Optional. A human-readable description of the
            resource.
        labels (MutableMapping[str, str]):
            Optional. Set of labels associated with the
            ``LbRouteExtension`` resource.

            The format must comply with `the requirements for
            labels <https://cloud.google.com/compute/docs/labeling-resources#requirements>`__
            for Google Cloud resources.
        forwarding_rules (MutableSequence[str]):
            Required. A list of references to the forwarding rules to
            which this service extension is attached to. At least one
            forwarding rule is required. There can be only one
            ``LbRouteExtension`` resource per forwarding rule.
        extension_chains (MutableSequence[google.cloud.network_services_v1.types.ExtensionChain]):
            Required. A set of ordered extension chains
            that contain the match conditions and extensions
            to execute. Match conditions for each extension
            chain are evaluated in sequence for a given
            request. The first extension chain that has a
            condition that matches the request is executed.
            Any subsequent extension chains do not execute.
            Limited to 5 extension chains per resource.
        load_balancing_scheme (google.cloud.network_services_v1.types.LoadBalancingScheme):
            Required. All backend services and forwarding rules
            referenced by this extension must share the same load
            balancing scheme. Supported values: ``INTERNAL_MANAGED``,
            ``EXTERNAL_MANAGED``. For more information, refer to
            `Choosing a load
            balancer <https://cloud.google.com/load-balancing/docs/backend-service>`__.
        metadata (google.protobuf.struct_pb2.Struct):
            Optional. The metadata provided here is included as part of
            the ``metadata_context`` (of type
            ``google.protobuf.Struct``) in the ``ProcessingRequest``
            message sent to the extension server. The metadata is
            available under the namespace
            ``com.google.lb_route_extension.<resource_name>``. The
            following variables are supported in the metadata Struct:

            ``{forwarding_rule_id}`` - substituted with the forwarding
            rule's fully qualified resource name.
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
    description: str = proto.Field(
        proto.STRING,
        number=9,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    forwarding_rules: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    extension_chains: MutableSequence["ExtensionChain"] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="ExtensionChain",
    )
    load_balancing_scheme: "LoadBalancingScheme" = proto.Field(
        proto.ENUM,
        number=8,
        enum="LoadBalancingScheme",
    )
    metadata: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=10,
        message=struct_pb2.Struct,
    )


class ListLbRouteExtensionsRequest(proto.Message):
    r"""Message for requesting list of ``LbRouteExtension`` resources.

    Attributes:
        parent (str):
            Required. The project and location from which the
            ``LbRouteExtension`` resources are listed, specified in the
            following format:
            ``projects/{project}/locations/{location}``.
        page_size (int):
            Optional. Requested page size. The server
            might return fewer items than requested. If
            unspecified, the server picks an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results that the server returns.
        filter (str):
            Optional. Filtering results.
        order_by (str):
            Optional. Hint for how to order the results.
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


class ListLbRouteExtensionsResponse(proto.Message):
    r"""Message for response to listing ``LbRouteExtension`` resources.

    Attributes:
        lb_route_extensions (MutableSequence[google.cloud.network_services_v1.types.LbRouteExtension]):
            The list of ``LbRouteExtension`` resources.
        next_page_token (str):
            A token identifying a page of results that
            the server returns.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    lb_route_extensions: MutableSequence["LbRouteExtension"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="LbRouteExtension",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetLbRouteExtensionRequest(proto.Message):
    r"""Message for getting a ``LbRouteExtension`` resource.

    Attributes:
        name (str):
            Required. A name of the ``LbRouteExtension`` resource to
            get. Must be in the format
            ``projects/{project}/locations/{location}/lbRouteExtensions/{lb_route_extension}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateLbRouteExtensionRequest(proto.Message):
    r"""Message for creating a ``LbRouteExtension`` resource.

    Attributes:
        parent (str):
            Required. The parent resource of the ``LbRouteExtension``
            resource. Must be in the format
            ``projects/{project}/locations/{location}``.
        lb_route_extension_id (str):
            Required. User-provided ID of the ``LbRouteExtension``
            resource to be created.
        lb_route_extension (google.cloud.network_services_v1.types.LbRouteExtension):
            Required. ``LbRouteExtension`` resource to be created.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server can
            ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, ignores the second request. This prevents
            clients from accidentally creating duplicate
            commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    lb_route_extension_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    lb_route_extension: "LbRouteExtension" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="LbRouteExtension",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateLbRouteExtensionRequest(proto.Message):
    r"""Message for updating a ``LbRouteExtension`` resource.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Used to specify the fields to be overwritten in
            the ``LbRouteExtension`` resource by the update. The fields
            specified in the update_mask are relative to the resource,
            not the full request. A field is overwritten if it is in the
            mask. If the user does not specify a mask, then all fields
            are overwritten.
        lb_route_extension (google.cloud.network_services_v1.types.LbRouteExtension):
            Required. ``LbRouteExtension`` resource being updated.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server can
            ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, ignores the second request. This prevents
            clients from accidentally creating duplicate
            commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    lb_route_extension: "LbRouteExtension" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="LbRouteExtension",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteLbRouteExtensionRequest(proto.Message):
    r"""Message for deleting a ``LbRouteExtension`` resource.

    Attributes:
        name (str):
            Required. The name of the ``LbRouteExtension`` resource to
            delete. Must be in the format
            ``projects/{project}/locations/{location}/lbRouteExtensions/{lb_route_extension}``.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server can
            ignore the request if it has already been
            completed. The server guarantees that for at
            least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, ignores the second request. This prevents
            clients from accidentally creating duplicate
            commitments.

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


__all__ = tuple(sorted(__protobuf__.manifest))
