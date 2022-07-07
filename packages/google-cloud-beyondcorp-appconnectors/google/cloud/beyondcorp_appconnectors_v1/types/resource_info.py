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

from google.protobuf import any_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.beyondcorp.appconnectors.v1",
    manifest={
        "HealthStatus",
        "ResourceInfo",
    },
)


class HealthStatus(proto.Enum):
    r"""HealthStatus represents the health status."""
    HEALTH_STATUS_UNSPECIFIED = 0
    HEALTHY = 1
    UNHEALTHY = 2
    UNRESPONSIVE = 3
    DEGRADED = 4


class ResourceInfo(proto.Message):
    r"""ResourceInfo represents the information/status of an app connector
    resource. Such as:

    -  remote_agent

       -  container

          -  runtime
          -  appgateway

             -  appconnector

                -  appconnection

                   -  tunnel

             -  logagent

    Attributes:
        id (str):
            Required. Unique Id for the resource.
        status (google.cloud.beyondcorp_appconnectors_v1.types.HealthStatus):
            Overall health status. Overall status is
            derived based on the status of each sub level
            resources.
        resource (google.protobuf.any_pb2.Any):
            Specific details for the resource. This is
            for internal use only.
        time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp to collect the info. It is
            suggested to be set by the topmost level
            resource only.
        sub (Sequence[google.cloud.beyondcorp_appconnectors_v1.types.ResourceInfo]):
            List of Info for the sub level resources.
    """

    id = proto.Field(
        proto.STRING,
        number=1,
    )
    status = proto.Field(
        proto.ENUM,
        number=2,
        enum="HealthStatus",
    )
    resource = proto.Field(
        proto.MESSAGE,
        number=3,
        message=any_pb2.Any,
    )
    time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    sub = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="ResourceInfo",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
