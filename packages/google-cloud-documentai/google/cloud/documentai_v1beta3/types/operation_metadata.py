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


__protobuf__ = proto.module(
    package="google.cloud.documentai.v1beta3", manifest={"CommonOperationMetadata",},
)


class CommonOperationMetadata(proto.Message):
    r"""The common metadata for long running operations.

    Attributes:
        state (google.cloud.documentai_v1beta3.types.CommonOperationMetadata.State):
            The state of the operation.
        state_message (str):
            A message providing more details about the
            current state of processing.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The creation time of the operation.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The last update time of the operation.
    """

    class State(proto.Enum):
        r"""State of the longrunning operation."""
        STATE_UNSPECIFIED = 0
        RUNNING = 1
        CANCELLING = 2
        SUCCEEDED = 3
        FAILED = 4
        CANCELLED = 5

    state = proto.Field(proto.ENUM, number=1, enum=State,)
    state_message = proto.Field(proto.STRING, number=2,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)


__all__ = tuple(sorted(__protobuf__.manifest))
