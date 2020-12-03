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


from google.cloud.servicedirectory_v1beta1.types import endpoint


__protobuf__ = proto.module(
    package="google.cloud.servicedirectory.v1beta1", manifest={"Service",},
)


class Service(proto.Message):
    r"""An individual service. A service contains a name and optional
    metadata. A service must exist before
    [endpoints][google.cloud.servicedirectory.v1beta1.Endpoint] can be
    added to it.

    Attributes:
        name (str):
            Immutable. The resource name for the service in the format
            ``projects/*/locations/*/namespaces/*/services/*``
        metadata (Sequence[~.service.Service.MetadataEntry]):
            Optional. Metadata for the service. This data
            can be consumed by service clients.  The entire
            metadata dictionary may contain up to 2000
            characters, spread across all key-value pairs.
            Metadata that goes beyond any these limits will
            be rejected.
        endpoints (Sequence[~.endpoint.Endpoint]):
            Output only. Endpoints associated with this
            service. Returned on LookupService.Resolve.
            Control plane clients should use
            RegistrationService.ListEndpoints.
    """

    name = proto.Field(proto.STRING, number=1)

    metadata = proto.MapField(proto.STRING, proto.STRING, number=2)

    endpoints = proto.RepeatedField(proto.MESSAGE, number=3, message=endpoint.Endpoint,)


__all__ = tuple(sorted(__protobuf__.manifest))
