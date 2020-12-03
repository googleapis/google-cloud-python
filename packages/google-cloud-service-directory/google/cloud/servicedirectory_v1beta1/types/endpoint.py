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


__protobuf__ = proto.module(
    package="google.cloud.servicedirectory.v1beta1", manifest={"Endpoint",},
)


class Endpoint(proto.Message):
    r"""An individual endpoint that provides a
    [service][google.cloud.servicedirectory.v1beta1.Service]. The
    service must already exist to create an endpoint.

    Attributes:
        name (str):
            Immutable. The resource name for the endpoint in the format
            ``projects/*/locations/*/namespaces/*/services/*/endpoints/*``
        address (str):
            Optional. An IPv4 or IPv6 address. Service Directory will
            reject bad addresses like: "8.8.8" "8.8.8.8:53"
            "test:bad:address" "[::1]" "[::1]:8080" Limited to 45
            characters.
        port (int):
            Optional. Service Directory will reject values outside of
            [0, 65535].
        metadata (Sequence[~.endpoint.Endpoint.MetadataEntry]):
            Optional. Metadata for the endpoint. This
            data can be consumed by service clients.  The
            entire metadata dictionary may contain up to 512
            characters, spread accoss all key-value pairs.
            Metadata that goes beyond any these limits will
            be rejected.
    """

    name = proto.Field(proto.STRING, number=1)

    address = proto.Field(proto.STRING, number=2)

    port = proto.Field(proto.INT32, number=3)

    metadata = proto.MapField(proto.STRING, proto.STRING, number=4)


__all__ = tuple(sorted(__protobuf__.manifest))
