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

from google.protobuf import duration_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.automl.v1beta1", manifest={"TimeSegment",},
)


class TimeSegment(proto.Message):
    r"""A time period inside of an example that has a time dimension
    (e.g. video).

    Attributes:
        start_time_offset (google.protobuf.duration_pb2.Duration):
            Start of the time segment (inclusive),
            represented as the duration since the example
            start.
        end_time_offset (google.protobuf.duration_pb2.Duration):
            End of the time segment (exclusive),
            represented as the duration since the example
            start.
    """

    start_time_offset = proto.Field(
        proto.MESSAGE, number=1, message=duration_pb2.Duration,
    )
    end_time_offset = proto.Field(
        proto.MESSAGE, number=2, message=duration_pb2.Duration,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
