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

from google.protobuf import duration_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.apigeeconnect.v1",
    manifest={
        "Action",
        "TetherEndpoint",
        "Scheme",
        "EgressRequest",
        "Payload",
        "StreamInfo",
        "EgressResponse",
        "HttpRequest",
        "Url",
        "Header",
        "HttpResponse",
    },
)


class Action(proto.Enum):
    r"""The action taken by agent."""
    ACTION_UNSPECIFIED = 0
    OPEN_NEW_STREAM = 1


class TetherEndpoint(proto.Enum):
    r"""Endpoint indicates where the messages will be delivered."""
    TETHER_ENDPOINT_UNSPECIFIED = 0
    APIGEE_MART = 1
    APIGEE_RUNTIME = 2
    APIGEE_MINT_RATING = 3


class Scheme(proto.Enum):
    r"""HTTP Scheme."""
    SCHEME_UNSPECIFIED = 0
    HTTPS = 1


class EgressRequest(proto.Message):
    r"""gRPC request payload for tether.

    Attributes:
        id (str):
            Unique identifier for the request.
        payload (google.cloud.apigeeconnect_v1.types.Payload):
            Actual payload to send to agent.
        endpoint (google.cloud.apigeeconnect_v1.types.TetherEndpoint):
            Tether Endpoint.
        project (str):
            GCP Project. Format: ``projects/{project_number}``.
        trace_id (str):
            Unique identifier for clients to trace their
            request/response.
        timeout (google.protobuf.duration_pb2.Duration):
            Timeout for the HTTP request.
    """

    id = proto.Field(
        proto.STRING,
        number=1,
    )
    payload = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Payload",
    )
    endpoint = proto.Field(
        proto.ENUM,
        number=3,
        enum="TetherEndpoint",
    )
    project = proto.Field(
        proto.STRING,
        number=4,
    )
    trace_id = proto.Field(
        proto.STRING,
        number=5,
    )
    timeout = proto.Field(
        proto.MESSAGE,
        number=6,
        message=duration_pb2.Duration,
    )


class Payload(proto.Message):
    r"""Payload for EgressRequest.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        http_request (google.cloud.apigeeconnect_v1.types.HttpRequest):
            The HttpRequest proto.

            This field is a member of `oneof`_ ``kind``.
        stream_info (google.cloud.apigeeconnect_v1.types.StreamInfo):
            The information of stream.

            This field is a member of `oneof`_ ``kind``.
        action (google.cloud.apigeeconnect_v1.types.Action):
            The action taken by agent.

            This field is a member of `oneof`_ ``kind``.
    """

    http_request = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="kind",
        message="HttpRequest",
    )
    stream_info = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="kind",
        message="StreamInfo",
    )
    action = proto.Field(
        proto.ENUM,
        number=3,
        oneof="kind",
        enum="Action",
    )


class StreamInfo(proto.Message):
    r"""The Information of bi-directional stream.

    Attributes:
        id (str):
            Unique identifier for the stream.
    """

    id = proto.Field(
        proto.STRING,
        number=1,
    )


class EgressResponse(proto.Message):
    r"""gRPC response payload for tether.

    Attributes:
        id (str):
            Unique identifier for the response. Matches
            the EgressRequest's id.
        http_response (google.cloud.apigeeconnect_v1.types.HttpResponse):
            HttpResponse.
        status (google.rpc.status_pb2.Status):
            Errors from application when handling the
            http request.
        project (str):
            GCP Project. Format: ``projects/{project_number}``.
        trace_id (str):
            Unique identifier for clients to trace their
            request/response. Matches the EgressRequest's
            trace id
        endpoint (google.cloud.apigeeconnect_v1.types.TetherEndpoint):
            Tether Endpoint.
        name (str):
            Name is the full resource path of endpoint. Format:
            ``projects/{project_number or project_id}/endpoints/{endpoint}``
    """

    id = proto.Field(
        proto.STRING,
        number=1,
    )
    http_response = proto.Field(
        proto.MESSAGE,
        number=2,
        message="HttpResponse",
    )
    status = proto.Field(
        proto.MESSAGE,
        number=3,
        message=status_pb2.Status,
    )
    project = proto.Field(
        proto.STRING,
        number=4,
    )
    trace_id = proto.Field(
        proto.STRING,
        number=5,
    )
    endpoint = proto.Field(
        proto.ENUM,
        number=6,
        enum="TetherEndpoint",
    )
    name = proto.Field(
        proto.STRING,
        number=7,
    )


class HttpRequest(proto.Message):
    r"""The proto definition of http request.

    Attributes:
        id (str):
            A unique identifier for the request.
        method (str):
            The HTTP request method.
            Valid methods: "GET", "HEAD", "POST", "PUT",
            "PATCH","DELETE".
        url (google.cloud.apigeeconnect_v1.types.Url):
            The HTTP request URL.
        headers (Sequence[google.cloud.apigeeconnect_v1.types.Header]):
            The HTTP request headers.
        body (bytes):
            HTTP request body.
    """

    id = proto.Field(
        proto.STRING,
        number=1,
    )
    method = proto.Field(
        proto.STRING,
        number=2,
    )
    url = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Url",
    )
    headers = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="Header",
    )
    body = proto.Field(
        proto.BYTES,
        number=5,
    )


class Url(proto.Message):
    r"""The proto definition of url. A url represents a URL and the general
    form represented is:

    ``[scheme://][google.cloud.apigeeconnect.v1.Url.host][path]``

    Attributes:
        scheme (google.cloud.apigeeconnect_v1.types.Scheme):
            Scheme.
        host (str):
            Host or Host:Port.
        path (str):
            Path starts with ``/``.
    """

    scheme = proto.Field(
        proto.ENUM,
        number=1,
        enum="Scheme",
    )
    host = proto.Field(
        proto.STRING,
        number=2,
    )
    path = proto.Field(
        proto.STRING,
        number=3,
    )


class Header(proto.Message):
    r"""The http headers.

    Attributes:
        key (str):

        values (Sequence[str]):

    """

    key = proto.Field(
        proto.STRING,
        number=1,
    )
    values = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class HttpResponse(proto.Message):
    r"""The proto definition of http response.

    Attributes:
        id (str):
            A unique identifier that matches the request
            ID.
        status (str):
            Status of http response, e.g. "200 OK".
        status_code (int):
            Status code of http response, e.g. 200.
        body (bytes):
            The HTTP 1.1 response body.
        headers (Sequence[google.cloud.apigeeconnect_v1.types.Header]):
            The HTTP response headers.
        content_length (int):
            Content length records the length of the
            associated content. The value -1 indicates that
            the length is unknown. Unless http method is
            "HEAD", values >= 0 indicate that the given
            number of bytes may be read from Body.
    """

    id = proto.Field(
        proto.STRING,
        number=1,
    )
    status = proto.Field(
        proto.STRING,
        number=2,
    )
    status_code = proto.Field(
        proto.INT32,
        number=3,
    )
    body = proto.Field(
        proto.BYTES,
        number=4,
    )
    headers = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="Header",
    )
    content_length = proto.Field(
        proto.INT64,
        number=6,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
