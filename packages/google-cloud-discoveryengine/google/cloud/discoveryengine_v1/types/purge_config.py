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

from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1",
    manifest={
        "PurgeDocumentsRequest",
        "PurgeDocumentsResponse",
        "PurgeDocumentsMetadata",
        "PurgeSuggestionDenyListEntriesRequest",
        "PurgeSuggestionDenyListEntriesResponse",
        "PurgeSuggestionDenyListEntriesMetadata",
        "PurgeCompletionSuggestionsRequest",
        "PurgeCompletionSuggestionsResponse",
        "PurgeCompletionSuggestionsMetadata",
    },
)


class PurgeDocumentsRequest(proto.Message):
    r"""Request message for
    [DocumentService.PurgeDocuments][google.cloud.discoveryengine.v1.DocumentService.PurgeDocuments]
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
    [DocumentService.PurgeDocuments][google.cloud.discoveryengine.v1.DocumentService.PurgeDocuments]
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
        ignored_count (int):
            Count of entries that were ignored as entries
            were not found.
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
    ignored_count: int = proto.Field(
        proto.INT64,
        number=5,
    )


class PurgeSuggestionDenyListEntriesRequest(proto.Message):
    r"""Request message for
    [CompletionService.PurgeSuggestionDenyListEntries][google.cloud.discoveryengine.v1.CompletionService.PurgeSuggestionDenyListEntries]
    method.

    Attributes:
        parent (str):
            Required. The parent data store resource name for which to
            import denylist entries. Follows pattern
            projects/\ */locations/*/collections/*/dataStores/*.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class PurgeSuggestionDenyListEntriesResponse(proto.Message):
    r"""Response message for
    [CompletionService.PurgeSuggestionDenyListEntries][google.cloud.discoveryengine.v1.CompletionService.PurgeSuggestionDenyListEntries]
    method.

    Attributes:
        purge_count (int):
            Number of suggestion deny list entries
            purged.
        error_samples (MutableSequence[google.rpc.status_pb2.Status]):
            A sample of errors encountered while
            processing the request.
    """

    purge_count: int = proto.Field(
        proto.INT64,
        number=1,
    )
    error_samples: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=status_pb2.Status,
    )


class PurgeSuggestionDenyListEntriesMetadata(proto.Message):
    r"""Metadata related to the progress of the
    PurgeSuggestionDenyListEntries operation. This is returned by
    the google.longrunning.Operation.metadata field.

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


class PurgeCompletionSuggestionsRequest(proto.Message):
    r"""Request message for
    [CompletionService.PurgeCompletionSuggestions][google.cloud.discoveryengine.v1.CompletionService.PurgeCompletionSuggestions]
    method.

    Attributes:
        parent (str):
            Required. The parent data store resource name for which to
            purge completion suggestions. Follows pattern
            projects/\ */locations/*/collections/*/dataStores/*.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class PurgeCompletionSuggestionsResponse(proto.Message):
    r"""Response message for
    [CompletionService.PurgeCompletionSuggestions][google.cloud.discoveryengine.v1.CompletionService.PurgeCompletionSuggestions]
    method.

    Attributes:
        purge_succeeded (bool):
            Whether the completion suggestions were
            successfully purged.
        error_samples (MutableSequence[google.rpc.status_pb2.Status]):
            A sample of errors encountered while
            processing the request.
    """

    purge_succeeded: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    error_samples: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=status_pb2.Status,
    )


class PurgeCompletionSuggestionsMetadata(proto.Message):
    r"""Metadata related to the progress of the
    PurgeCompletionSuggestions operation. This is returned by the
    google.longrunning.Operation.metadata field.

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


__all__ = tuple(sorted(__protobuf__.manifest))
