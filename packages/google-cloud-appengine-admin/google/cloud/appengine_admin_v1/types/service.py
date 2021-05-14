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

from google.cloud.appengine_admin_v1.types import (
    network_settings as ga_network_settings,
)


__protobuf__ = proto.module(
    package="google.appengine.v1", manifest={"Service", "TrafficSplit",},
)


class Service(proto.Message):
    r"""A Service resource is a logical component of an application
    that can share state and communicate in a secure fashion with
    other services. For example, an application that handles
    customer requests might include separate services to handle
    tasks such as backend data analysis or API requests from mobile
    devices. Each service has a collection of versions that define a
    specific set of code used to implement the functionality of that
    service.

    Attributes:
        name (str):
            Full path to the Service resource in the API. Example:
            ``apps/myapp/services/default``.

            @OutputOnly
        id (str):
            Relative name of the service within the application.
            Example: ``default``.

            @OutputOnly
        split (google.cloud.appengine_admin_v1.types.TrafficSplit):
            Mapping that defines fractional HTTP traffic
            diversion to different versions within the
            service.
        network_settings (google.cloud.appengine_admin_v1.types.NetworkSettings):
            Ingress settings for this service. Will apply
            to all versions.
    """

    name = proto.Field(proto.STRING, number=1,)
    id = proto.Field(proto.STRING, number=2,)
    split = proto.Field(proto.MESSAGE, number=3, message="TrafficSplit",)
    network_settings = proto.Field(
        proto.MESSAGE, number=6, message=ga_network_settings.NetworkSettings,
    )


class TrafficSplit(proto.Message):
    r"""Traffic routing configuration for versions within a single
    service. Traffic splits define how traffic directed to the
    service is assigned to versions.

    Attributes:
        shard_by (google.cloud.appengine_admin_v1.types.TrafficSplit.ShardBy):
            Mechanism used to determine which version a
            request is sent to. The traffic selection
            algorithm will be stable for either type until
            allocations are changed.
        allocations (Sequence[google.cloud.appengine_admin_v1.types.TrafficSplit.AllocationsEntry]):
            Mapping from version IDs within the service to fractional
            (0.000, 1] allocations of traffic for that version. Each
            version can be specified only once, but some versions in the
            service may not have any traffic allocation. Services that
            have traffic allocated cannot be deleted until either the
            service is deleted or their traffic allocation is removed.
            Allocations must sum to 1. Up to two decimal place precision
            is supported for IP-based splits and up to three decimal
            places is supported for cookie-based splits.
    """

    class ShardBy(proto.Enum):
        r"""Available sharding mechanisms."""
        UNSPECIFIED = 0
        COOKIE = 1
        IP = 2
        RANDOM = 3

    shard_by = proto.Field(proto.ENUM, number=1, enum=ShardBy,)
    allocations = proto.MapField(proto.STRING, proto.DOUBLE, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
