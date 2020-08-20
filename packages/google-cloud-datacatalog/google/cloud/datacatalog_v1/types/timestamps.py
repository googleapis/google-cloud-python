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


from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.datacatalog.v1", manifest={"SystemTimestamps",},
)


class SystemTimestamps(proto.Message):
    r"""Timestamps about this resource according to a particular
    system.

    Attributes:
        create_time (~.timestamp.Timestamp):
            The creation time of the resource within the
            given system.
        update_time (~.timestamp.Timestamp):
            The last-modified time of the resource within
            the given system.
        expire_time (~.timestamp.Timestamp):
            Output only. The expiration time of the
            resource within the given system. Currently only
            apllicable to BigQuery resources.
    """

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    expire_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)


__all__ = tuple(sorted(__protobuf__.manifest))
