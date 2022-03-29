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
    package="google.cloud.dataproc.v1",
    manifest={
        "BatchOperationMetadata",
        "ClusterOperationStatus",
        "ClusterOperationMetadata",
    },
)


class BatchOperationMetadata(proto.Message):
    r"""Metadata describing the Batch operation.

    Attributes:
        batch (str):
            Name of the batch for the operation.
        batch_uuid (str):
            Batch UUID for the operation.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the operation was created.
        done_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the operation finished.
        operation_type (google.cloud.dataproc_v1.types.BatchOperationMetadata.BatchOperationType):
            The operation type.
        description (str):
            Short description of the operation.
        labels (Sequence[google.cloud.dataproc_v1.types.BatchOperationMetadata.LabelsEntry]):
            Labels associated with the operation.
        warnings (Sequence[str]):
            Warnings encountered during operation
            execution.
    """

    class BatchOperationType(proto.Enum):
        r"""Operation type for Batch resources"""
        BATCH_OPERATION_TYPE_UNSPECIFIED = 0
        BATCH = 1

    batch = proto.Field(
        proto.STRING,
        number=1,
    )
    batch_uuid = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    done_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    operation_type = proto.Field(
        proto.ENUM,
        number=6,
        enum=BatchOperationType,
    )
    description = proto.Field(
        proto.STRING,
        number=7,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=8,
    )
    warnings = proto.RepeatedField(
        proto.STRING,
        number=9,
    )


class ClusterOperationStatus(proto.Message):
    r"""The status of the operation.

    Attributes:
        state (google.cloud.dataproc_v1.types.ClusterOperationStatus.State):
            Output only. A message containing the
            operation state.
        inner_state (str):
            Output only. A message containing the
            detailed operation state.
        details (str):
            Output only. A message containing any
            operation metadata details.
        state_start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time this state was entered.
    """

    class State(proto.Enum):
        r"""The operation state."""
        UNKNOWN = 0
        PENDING = 1
        RUNNING = 2
        DONE = 3

    state = proto.Field(
        proto.ENUM,
        number=1,
        enum=State,
    )
    inner_state = proto.Field(
        proto.STRING,
        number=2,
    )
    details = proto.Field(
        proto.STRING,
        number=3,
    )
    state_start_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )


class ClusterOperationMetadata(proto.Message):
    r"""Metadata describing the operation.

    Attributes:
        cluster_name (str):
            Output only. Name of the cluster for the
            operation.
        cluster_uuid (str):
            Output only. Cluster UUID for the operation.
        status (google.cloud.dataproc_v1.types.ClusterOperationStatus):
            Output only. Current operation status.
        status_history (Sequence[google.cloud.dataproc_v1.types.ClusterOperationStatus]):
            Output only. The previous operation status.
        operation_type (str):
            Output only. The operation type.
        description (str):
            Output only. Short description of operation.
        labels (Sequence[google.cloud.dataproc_v1.types.ClusterOperationMetadata.LabelsEntry]):
            Output only. Labels associated with the
            operation
        warnings (Sequence[str]):
            Output only. Errors encountered during
            operation execution.
    """

    cluster_name = proto.Field(
        proto.STRING,
        number=7,
    )
    cluster_uuid = proto.Field(
        proto.STRING,
        number=8,
    )
    status = proto.Field(
        proto.MESSAGE,
        number=9,
        message="ClusterOperationStatus",
    )
    status_history = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message="ClusterOperationStatus",
    )
    operation_type = proto.Field(
        proto.STRING,
        number=11,
    )
    description = proto.Field(
        proto.STRING,
        number=12,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=13,
    )
    warnings = proto.RepeatedField(
        proto.STRING,
        number=14,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
