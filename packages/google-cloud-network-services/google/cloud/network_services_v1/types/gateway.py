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
    package="google.cloud.networkservices.v1",
    manifest={
        "Gateway",
        "ListGatewaysRequest",
        "ListGatewaysResponse",
        "GetGatewayRequest",
        "CreateGatewayRequest",
        "UpdateGatewayRequest",
        "DeleteGatewayRequest",
    },
)


class Gateway(proto.Message):
    r"""Gateway represents the configuration for a proxy, typically a
    load balancer. It captures the ip:port over which the services
    are exposed by the proxy, along with any policy configurations.
    Routes have reference to to Gateways to dictate how requests
    should be routed by this Gateway.

    Attributes:
        name (str):
            Required. Name of the Gateway resource. It matches pattern
            ``projects/*/locations/*/gateways/<gateway_name>``.
        self_link (str):
            Output only. Server-defined URL of this
            resource
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the resource
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the resource
            was updated.
        labels (MutableMapping[str, str]):
            Optional. Set of label tags associated with
            the Gateway resource.
        description (str):
            Optional. A free-text description of the
            resource. Max length 1024 characters.
        type_ (google.cloud.network_services_v1.types.Gateway.Type):
            Immutable. The type of the customer managed
            gateway. This field is required. If unspecified,
            an error is returned.
        ports (MutableSequence[int]):
            Required. One or more ports that the Gateway
            must receive traffic on. The proxy binds to the
            ports specified. Gateway listen on 0.0.0.0 on
            the ports specified below.
        scope (str):
            Required. Immutable. Scope determines how
            configuration across multiple Gateway instances
            are merged. The configuration for multiple
            Gateway instances with the same scope will be
            merged as presented as a single coniguration to
            the proxy/load balancer.

            Max length 64 characters.
            Scope should start with a letter and can only
            have letters, numbers, hyphens.
        server_tls_policy (str):
            Optional. A fully-qualified ServerTLSPolicy
            URL reference. Specifies how TLS traffic is
            terminated. If empty, TLS termination is
            disabled.
    """

    class Type(proto.Enum):
        r"""The type of the customer-managed gateway. Possible values are:

        -  OPEN_MESH
        -  SECURE_WEB_GATEWAY

        Values:
            TYPE_UNSPECIFIED (0):
                The type of the customer managed gateway is
                unspecified.
            OPEN_MESH (1):
                The type of the customer managed gateway is
                TrafficDirector Open Mesh.
            SECURE_WEB_GATEWAY (2):
                The type of the customer managed gateway is
                SecureWebGateway (SWG).
        """
        TYPE_UNSPECIFIED = 0
        OPEN_MESH = 1
        SECURE_WEB_GATEWAY = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    self_link: str = proto.Field(
        proto.STRING,
        number=13,
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
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=6,
        enum=Type,
    )
    ports: MutableSequence[int] = proto.RepeatedField(
        proto.INT32,
        number=11,
    )
    scope: str = proto.Field(
        proto.STRING,
        number=8,
    )
    server_tls_policy: str = proto.Field(
        proto.STRING,
        number=9,
    )


class ListGatewaysRequest(proto.Message):
    r"""Request used with the ListGateways method.

    Attributes:
        parent (str):
            Required. The project and location from which the Gateways
            should be listed, specified in the format
            ``projects/*/locations/*``.
        page_size (int):
            Maximum number of Gateways to return per
            call.
        page_token (str):
            The value returned by the last ``ListGatewaysResponse``
            Indicates that this is a continuation of a prior
            ``ListGateways`` call, and that the system should return the
            next page of data.
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


class ListGatewaysResponse(proto.Message):
    r"""Response returned by the ListGateways method.

    Attributes:
        gateways (MutableSequence[google.cloud.network_services_v1.types.Gateway]):
            List of Gateway resources.
        next_page_token (str):
            If there might be more results than those appearing in this
            response, then ``next_page_token`` is included. To get the
            next set of results, call this method again using the value
            of ``next_page_token`` as ``page_token``.
    """

    @property
    def raw_page(self):
        return self

    gateways: MutableSequence["Gateway"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Gateway",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetGatewayRequest(proto.Message):
    r"""Request used by the GetGateway method.

    Attributes:
        name (str):
            Required. A name of the Gateway to get. Must be in the
            format ``projects/*/locations/*/gateways/*``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateGatewayRequest(proto.Message):
    r"""Request used by the CreateGateway method.

    Attributes:
        parent (str):
            Required. The parent resource of the Gateway. Must be in the
            format ``projects/*/locations/*``.
        gateway_id (str):
            Required. Short name of the Gateway resource
            to be created.
        gateway (google.cloud.network_services_v1.types.Gateway):
            Required. Gateway resource to be created.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    gateway_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    gateway: "Gateway" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Gateway",
    )


class UpdateGatewayRequest(proto.Message):
    r"""Request used by the UpdateGateway method.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask is used to specify the fields to be
            overwritten in the Gateway resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If the user does not provide a mask
            then all fields will be overwritten.
        gateway (google.cloud.network_services_v1.types.Gateway):
            Required. Updated Gateway resource.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    gateway: "Gateway" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Gateway",
    )


class DeleteGatewayRequest(proto.Message):
    r"""Request used by the DeleteGateway method.

    Attributes:
        name (str):
            Required. A name of the Gateway to delete. Must be in the
            format ``projects/*/locations/*/gateways/*``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
