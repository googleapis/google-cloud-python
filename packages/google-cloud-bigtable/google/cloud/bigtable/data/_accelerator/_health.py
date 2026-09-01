# Copyright 2026 Google LLC
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
"""Wire codec for ``grpc.health.v1.Health/Check`` against the daemon.

The daemon serves the standard gRPC health service. The generated Python stubs
for it live in ``grpcio-health-checking``, a separate distribution this package
does not depend on, and health.proto is far too small to justify adding one: the
request we send is the empty message, and the response is a single varint.

    HealthCheckRequest{service: ""}  ->  b""
    HealthCheckResponse{status: S}   ->  b"\\x08" + varint(S)
                                         b""          -> UNKNOWN (proto3 omits 0)
                                         b"\\x08\\x01"  -> SERVING
                                         b"\\x08\\x02"  -> NOT_SERVING

So the two functions below are the whole codec. Note that we always probe the
empty service name (""), which is the daemon's overall-process status.

This module is plain sync-only logic, shared verbatim by the async and generated
sync clients; no CrossSync branching is needed.
"""

from __future__ import annotations

import enum

#: Full method name of the health check RPC, as registered by the daemon.
HEALTH_CHECK_METHOD = "/grpc.health.v1.Health/Check"

#: Tag byte for ``HealthCheckResponse.status``: field 1, wire type 0 (varint).
_STATUS_TAG = 0x08


class ServingStatus(enum.IntEnum):
    """Mirror of ``grpc.health.v1.HealthCheckResponse.ServingStatus``."""

    UNKNOWN = 0
    SERVING = 1
    NOT_SERVING = 2
    SERVICE_UNKNOWN = 3


def serialize_health_request(_request: object = None) -> bytes:
    """Serialize ``HealthCheckRequest{service: ""}``.

    Every field is at its proto3 default, so the encoding is empty. Takes and
    ignores an argument because gRPC calls it with the request object.
    """
    return b""


def parse_health_response(payload: bytes) -> ServingStatus:
    """Decode a ``HealthCheckResponse`` into its status.

    Anything that isn't a recognizable status field decodes to ``UNKNOWN``,
    which callers treat as a failed probe. That is the right default: the only
    field the message has is ``status`` at field 1, and proto3 serializes fields
    in ascending field-number order, so a payload that doesn't start with tag 1
    is not a response we understand.
    """
    if not payload or payload[0] != _STATUS_TAG:
        return ServingStatus.UNKNOWN
    value = 0
    shift = 0
    for byte in payload[1:]:
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            break
        shift += 7
    else:
        # Ran off the end of a continued varint: truncated message.
        return ServingStatus.UNKNOWN
    try:
        return ServingStatus(value)
    except ValueError:
        # A status this client predates. Not SERVING as far as we know.
        return ServingStatus.UNKNOWN
