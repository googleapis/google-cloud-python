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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.orchestration.airflow.service.v1beta1",
    manifest={"OperationMetadata",},
)


class OperationMetadata(proto.Message):
    r"""Metadata describing an operation.

    Attributes:
        state (google.cloud.orchestration.airflow.service_v1beta1.types.OperationMetadata.State):
            Output only. The current operation state.
        operation_type (google.cloud.orchestration.airflow.service_v1beta1.types.OperationMetadata.Type):
            Output only. The type of operation being
            performed.
        resource (str):
            Output only. The resource being operated on, as a `relative
            resource
            name </apis/design/resource_names#relative_resource_name>`__.
        resource_uuid (str):
            Output only. The UUID of the resource being
            operated on.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            submitted to the server.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the operation
            terminated, regardless of its success. This
            field is unset if the operation is still
            ongoing.
    """

    class State(proto.Enum):
        r"""An enum describing the overall state of an operation."""
        STATE_UNSPECIFIED = 0
        PENDING = 1
        RUNNING = 2
        SUCCESSFUL = 3
        FAILED = 4

    class Type(proto.Enum):
        r"""Type of longrunning operation."""
        TYPE_UNSPECIFIED = 0
        CREATE = 1
        DELETE = 2
        UPDATE = 3
        CHECK = 4

    state = proto.Field(proto.ENUM, number=1, enum=State,)
    operation_type = proto.Field(proto.ENUM, number=2, enum=Type,)
    resource = proto.Field(proto.STRING, number=3,)
    resource_uuid = proto.Field(proto.STRING, number=4,)
    create_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)


__all__ = tuple(sorted(__protobuf__.manifest))
