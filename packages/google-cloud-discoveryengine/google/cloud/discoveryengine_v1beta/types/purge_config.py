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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1beta",
    manifest={
        "PurgeDocumentsRequest",
        "PurgeDocumentsResponse",
        "PurgeDocumentsMetadata",
    },
)


class PurgeDocumentsRequest(proto.Message):
    r"""Request message for
    [DocumentService.PurgeDocuments][google.cloud.discoveryengine.v1beta.DocumentService.PurgeDocuments]
    method.

    Attributes:
        parent (str):
            Required. The parent resource name, such as
            ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}``.
        filter (str):
            Required. Filter matching documents to purge. Only currently
            supported value is ``*`` (all items).
        force (bool):
            Actually performs the purge. If ``force`` is set to false,
            return the expected purge count without deleting any
            documents.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=2,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class PurgeDocumentsResponse(proto.Message):
    r"""Response message for
    [DocumentService.PurgeDocuments][google.cloud.discoveryengine.v1beta.DocumentService.PurgeDocuments]
    method. If the long running operation is successfully done, then
    this message is returned by the
    google.longrunning.Operations.response field.

    Attributes:
        purge_count (int):
            The total count of documents purged as a
            result of the operation.
        purge_sample (MutableSequence[str]):
            A sample of document names that will be deleted. Only
            populated if ``force`` is set to false. A max of 100 names
            will be returned and the names are chosen at random.
    """

    purge_count: int = proto.Field(
        proto.INT64,
        number=1,
    )
    purge_sample: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class PurgeDocumentsMetadata(proto.Message):
    r"""Metadata related to the progress of the PurgeDocuments
    operation. This will be returned by the
    google.longrunning.Operation.metadata field.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation create time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation last update time. If the operation
            is done, this is also the finish time.
        success_count (int):
            Count of entries that were deleted
            successfully.
        failure_count (int):
            Count of entries that encountered errors
            while processing.
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
    success_count: int = proto.Field(
        proto.INT64,
        number=3,
    )
    failure_count: int = proto.Field(
        proto.INT64,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
