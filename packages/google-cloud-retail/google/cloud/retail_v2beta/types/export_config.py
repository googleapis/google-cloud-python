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
from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.retail.v2beta",
    manifest={
        "ExportErrorsConfig",
        "ExportMetadata",
        "ExportProductsResponse",
        "ExportUserEventsResponse",
        "OutputResult",
        "BigQueryOutputResult",
    },
)


class ExportErrorsConfig(proto.Message):
    r"""Configuration of destination for Export related errors.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_prefix (str):
            Google Cloud Storage path for import errors. This must be an
            empty, existing Cloud Storage bucket. Export errors will be
            written to a file in this bucket, one per line, as a
            JSON-encoded ``google.rpc.Status`` message.

            This field is a member of `oneof`_ ``destination``.
    """

    gcs_prefix: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="destination",
    )


class ExportMetadata(proto.Message):
    r"""Metadata related to the progress of the Export operation.
    This is returned by the google.longrunning.Operation.metadata
    field.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation create time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation last update time. If the operation
            is done, this is also the finish time.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class ExportProductsResponse(proto.Message):
    r"""Response of the ExportProductsRequest. If the long running
    operation is done, then this message is returned by the
    google.longrunning.Operations.response field if the operation
    was successful.

    Attributes:
        error_samples (MutableSequence[google.rpc.status_pb2.Status]):
            A sample of errors encountered while
            processing the request.
        errors_config (google.cloud.retail_v2beta.types.ExportErrorsConfig):
            This field is never set.
        output_result (google.cloud.retail_v2beta.types.OutputResult):
            Output result indicating where the data were
            exported to.
    """

    error_samples: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=status_pb2.Status,
    )
    errors_config: "ExportErrorsConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ExportErrorsConfig",
    )
    output_result: "OutputResult" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="OutputResult",
    )


class ExportUserEventsResponse(proto.Message):
    r"""Response of the ExportUserEventsRequest. If the long running
    operation was successful, then this message is returned by the
    google.longrunning.Operations.response field if the operation
    was successful.

    Attributes:
        error_samples (MutableSequence[google.rpc.status_pb2.Status]):
            A sample of errors encountered while
            processing the request.
        errors_config (google.cloud.retail_v2beta.types.ExportErrorsConfig):
            This field is never set.
        output_result (google.cloud.retail_v2beta.types.OutputResult):
            Output result indicating where the data were
            exported to.
    """

    error_samples: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=status_pb2.Status,
    )
    errors_config: "ExportErrorsConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ExportErrorsConfig",
    )
    output_result: "OutputResult" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="OutputResult",
    )


class OutputResult(proto.Message):
    r"""Output result.

    Attributes:
        bigquery_result (MutableSequence[google.cloud.retail_v2beta.types.BigQueryOutputResult]):
            Export result in BigQuery.
    """

    bigquery_result: MutableSequence["BigQueryOutputResult"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="BigQueryOutputResult",
    )


class BigQueryOutputResult(proto.Message):
    r"""A BigQuery output result.

    Attributes:
        dataset_id (str):
            The ID of a BigQuery Dataset.
        table_id (str):
            The ID of a BigQuery Table.
    """

    dataset_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
