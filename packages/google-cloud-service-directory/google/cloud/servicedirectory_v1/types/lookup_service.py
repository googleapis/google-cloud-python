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

from google.cloud.servicedirectory_v1.types import service as gcs_service


__protobuf__ = proto.module(
    package="google.cloud.servicedirectory.v1",
    manifest={"ResolveServiceRequest", "ResolveServiceResponse",},
)


class ResolveServiceRequest(proto.Message):
    r"""The request message for
    [LookupService.ResolveService][google.cloud.servicedirectory.v1.LookupService.ResolveService].
    Looks up a service by its name, returns the service and its
    endpoints.

    Attributes:
        name (str):
            Required. The name of the service to resolve.
        max_endpoints (int):
            Optional. The maximum number of endpoints to
            return. Defaults to 25. Maximum is 100. If a
            value less than one is specified, the Default is
            used. If a value greater than the Maximum is
            specified, the Maximum is used.
        endpoint_filter (str):
            Optional. The filter applied to the endpoints of the
            resolved service.

            General filter string syntax: () can be "name" or
            "metadata." for map field. can be "<, >, <=, >=, !=, =, :".
            Of which ":" means HAS and is roughly the same as "=". must
            be the same data type as the field. can be "AND, OR, NOT".

            Examples of valid filters:

            -  "metadata.owner" returns Endpoints that have a label with
               the key "owner", this is the same as "metadata:owner"
            -  "metadata.protocol=gRPC" returns Endpoints that have
               key/value "protocol=gRPC"
            -  "metadata.owner!=sd AND metadata.foo=bar" returns
               Endpoints that have "owner" field in metadata with a
               value that is not "sd" AND have the key/value foo=bar.
    """

    name = proto.Field(proto.STRING, number=1,)
    max_endpoints = proto.Field(proto.INT32, number=2,)
    endpoint_filter = proto.Field(proto.STRING, number=3,)


class ResolveServiceResponse(proto.Message):
    r"""The response message for
    [LookupService.ResolveService][google.cloud.servicedirectory.v1.LookupService.ResolveService].

    Attributes:
        service (google.cloud.servicedirectory_v1.types.Service):

    """

    service = proto.Field(proto.MESSAGE, number=1, message=gcs_service.Service,)


__all__ = tuple(sorted(__protobuf__.manifest))
