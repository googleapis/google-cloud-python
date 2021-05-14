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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(package="google.appengine.v1", manifest={"Instance",},)


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
        r"""Wrapper for LivenessState enum.    """

        class LivenessState(proto.Enum):
            r"""Liveness health check status for Flex instances."""
            LIVENESS_STATE_UNSPECIFIED = 0
            UNKNOWN = 1
            HEALTHY = 2
            UNHEALTHY = 3
            DRAINING = 4
            TIMEOUT = 5

    name = proto.Field(proto.STRING, number=1,)
    id = proto.Field(proto.STRING, number=2,)
    app_engine_release = proto.Field(proto.STRING, number=3,)
    availability = proto.Field(proto.ENUM, number=4, enum=Availability,)
    vm_name = proto.Field(proto.STRING, number=5,)
    vm_zone_name = proto.Field(proto.STRING, number=6,)
    vm_id = proto.Field(proto.STRING, number=7,)
    start_time = proto.Field(proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,)
    requests = proto.Field(proto.INT32, number=9,)
    errors = proto.Field(proto.INT32, number=10,)
    qps = proto.Field(proto.FLOAT, number=11,)
    average_latency = proto.Field(proto.INT32, number=12,)
    memory_usage = proto.Field(proto.INT64, number=13,)
    vm_status = proto.Field(proto.STRING, number=14,)
    vm_debug_enabled = proto.Field(proto.BOOL, number=15,)
    vm_ip = proto.Field(proto.STRING, number=16,)
    vm_liveness = proto.Field(proto.ENUM, number=17, enum=Liveness.LivenessState,)


__all__ = tuple(sorted(__protobuf__.manifest))
