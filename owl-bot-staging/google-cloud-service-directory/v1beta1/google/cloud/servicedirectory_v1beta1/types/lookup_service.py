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

import proto  # type: ignore

from google.cloud.servicedirectory_v1beta1.types import service as gcs_service


__protobuf__ = proto.module(
    package='google.cloud.servicedirectory.v1beta1',
    manifest={
        'ResolveServiceRequest',
        'ResolveServiceResponse',
    },
)


class ResolveServiceRequest(proto.Message):
    r"""The request message for
    [LookupService.ResolveService][google.cloud.servicedirectory.v1beta1.LookupService.ResolveService].
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

            General ``filter`` string syntax:
            ``<field> <operator> <value> (<logical connector>)``

            -  ``<field>`` can be ``name``, ``address``, ``port``, or
               ``metadata.<key>`` for map field
            -  ``<operator>`` can be ``<``, ``>``, ``<=``, ``>=``,
               ``!=``, ``=``, ``:``. Of which ``:`` means ``HAS``, and
               is roughly the same as ``=``
            -  ``<value>`` must be the same data type as field
            -  ``<logical connector>`` can be ``AND``, ``OR``, ``NOT``

            Examples of valid filters:

            -  ``metadata.owner`` returns endpoints that have a
               annotation with the key ``owner``, this is the same as
               ``metadata:owner``
            -  ``metadata.protocol=gRPC`` returns endpoints that have
               key/value ``protocol=gRPC``
            -  ``address=192.108.1.105`` returns endpoints that have
               this address
            -  ``port>8080`` returns endpoints that have port number
               larger than 8080
            -

            ``name>projects/my-project/locations/us-east1/namespaces/my-namespace/services/my-service/endpoints/endpoint-c``
            returns endpoints that have name that is alphabetically
            later than the string, so "endpoint-e" is returned but
            "endpoint-a" is not \*
            ``name=projects/my-project/locations/us-central1/namespaces/my-namespace/services/my-service/endpoints/ep-1``
            returns the endpoint that has an endpoint_id equal to
            ``ep-1``

            -  ``metadata.owner!=sd AND metadata.foo=bar`` returns
               endpoints that have ``owner`` in annotation key but value
               is not ``sd`` AND have key/value ``foo=bar``
            -  ``doesnotexist.foo=bar`` returns an empty list. Note that
               endpoint doesn't have a field called "doesnotexist".
               Since the filter does not match any endpoint, it returns
               no results

            For more information about filtering, see `API
            Filtering <https://aip.dev/160>`__.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    max_endpoints: int = proto.Field(
        proto.INT32,
        number=2,
    )
    endpoint_filter: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ResolveServiceResponse(proto.Message):
    r"""The response message for
    [LookupService.ResolveService][google.cloud.servicedirectory.v1beta1.LookupService.ResolveService].

    Attributes:
        service (google.cloud.servicedirectory_v1beta1.types.Service):

    """

    service: gcs_service.Service = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcs_service.Service,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
