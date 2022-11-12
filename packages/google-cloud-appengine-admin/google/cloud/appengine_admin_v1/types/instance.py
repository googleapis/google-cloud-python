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
from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.appengine.v1",
    manifest={
        "Instance",
    },
)


class Instance(proto.Message):
    r"""An Instance resource is the computing unit that App Engine
    uses to automatically scale an application.

    Attributes:
        name (str):
            Output only. Full path to the Instance resource in the API.
            Example:
            ``apps/myapp/services/default/versions/v1/instances/instance-1``.
        id (str):
            Output only. Relative name of the instance within the
            version. Example: ``instance-1``.
        app_engine_release (str):
            Output only. App Engine release this instance
            is running on.
        availability (google.cloud.appengine_admin_v1.types.Instance.Availability):
            Output only. Availability of the instance.
        vm_name (str):
            Output only. Name of the virtual machine
            where this instance lives. Only applicable for
            instances in App Engine flexible environment.
        vm_zone_name (str):
            Output only. Zone where the virtual machine
            is located. Only applicable for instances in App
            Engine flexible environment.
        vm_id (str):
            Output only. Virtual machine ID of this
            instance. Only applicable for instances in App
            Engine flexible environment.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time that this instance was
            started.
            @OutputOnly
        requests (int):
            Output only. Number of requests since this
            instance was started.
        errors (int):
            Output only. Number of errors since this
            instance was started.
        qps (float):
            Output only. Average queries per second (QPS)
            over the last minute.
        average_latency (int):
            Output only. Average latency (ms) over the
            last minute.
        memory_usage (int):
            Output only. Total memory in use (bytes).
        vm_status (str):
            Output only. Status of the virtual machine
            where this instance lives. Only applicable for
            instances in App Engine flexible environment.
        vm_debug_enabled (bool):
            Output only. Whether this instance is in
            debug mode. Only applicable for instances in App
            Engine flexible environment.
        vm_ip (str):
            Output only. The IP address of this instance.
            Only applicable for instances in App Engine
            flexible environment.
        vm_liveness (google.cloud.appengine_admin_v1.types.Instance.Liveness.LivenessState):
            Output only. The liveness health check of
            this instance. Only applicable for instances in
            App Engine flexible environment.
    """

    class Availability(proto.Enum):
        r"""Availability of the instance."""
        UNSPECIFIED = 0
        RESIDENT = 1
        DYNAMIC = 2

    class Liveness(proto.Message):
        r"""Wrapper for LivenessState enum."""

        class LivenessState(proto.Enum):
            r"""Liveness health check status for Flex instances."""
            LIVENESS_STATE_UNSPECIFIED = 0
            UNKNOWN = 1
            HEALTHY = 2
            UNHEALTHY = 3
            DRAINING = 4
            TIMEOUT = 5

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    app_engine_release: str = proto.Field(
        proto.STRING,
        number=3,
    )
    availability: Availability = proto.Field(
        proto.ENUM,
        number=4,
        enum=Availability,
    )
    vm_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    vm_zone_name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    vm_id: str = proto.Field(
        proto.STRING,
        number=7,
    )
    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    requests: int = proto.Field(
        proto.INT32,
        number=9,
    )
    errors: int = proto.Field(
        proto.INT32,
        number=10,
    )
    qps: float = proto.Field(
        proto.FLOAT,
        number=11,
    )
    average_latency: int = proto.Field(
        proto.INT32,
        number=12,
    )
    memory_usage: int = proto.Field(
        proto.INT64,
        number=13,
    )
    vm_status: str = proto.Field(
        proto.STRING,
        number=14,
    )
    vm_debug_enabled: bool = proto.Field(
        proto.BOOL,
        number=15,
    )
    vm_ip: str = proto.Field(
        proto.STRING,
        number=16,
    )
    vm_liveness: Liveness.LivenessState = proto.Field(
        proto.ENUM,
        number=17,
        enum=Liveness.LivenessState,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
