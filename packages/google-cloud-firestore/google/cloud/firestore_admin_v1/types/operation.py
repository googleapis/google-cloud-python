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

from google.cloud.firestore_admin_v1.types import index as gfa_index
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.firestore.admin.v1",
    manifest={
        "OperationState",
        "IndexOperationMetadata",
        "FieldOperationMetadata",
        "ExportDocumentsMetadata",
        "ImportDocumentsMetadata",
        "ExportDocumentsResponse",
        "Progress",
    },
)


class OperationState(proto.Enum):
    r"""Describes the state of the operation."""
    OPERATION_STATE_UNSPECIFIED = 0
    INITIALIZING = 1
    PROCESSING = 2
    CANCELLING = 3
    FINALIZING = 4
    SUCCESSFUL = 5
    FAILED = 6
    CANCELLED = 7


class IndexOperationMetadata(proto.Message):
    r"""Metadata for
    [google.longrunning.Operation][google.longrunning.Operation] results
    from
    [FirestoreAdmin.CreateIndex][google.firestore.admin.v1.FirestoreAdmin.CreateIndex].

    Attributes:
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The time this operation started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time this operation completed. Will be
            unset if operation still in progress.
        index (str):
            The index resource that this operation is acting on. For
            example:
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/indexes/{index_id}``
        state (google.cloud.firestore_admin_v1.types.OperationState):
            The state of the operation.
        progress_documents (google.cloud.firestore_admin_v1.types.Progress):
            The progress, in documents, of this
            operation.
        progress_bytes (google.cloud.firestore_admin_v1.types.Progress):
            The progress, in bytes, of this operation.
    """

    start_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    index = proto.Field(
        proto.STRING,
        number=3,
    )
    state = proto.Field(
        proto.ENUM,
        number=4,
        enum="OperationState",
    )
    progress_documents = proto.Field(
        proto.MESSAGE,
        number=5,
        message="Progress",
    )
    progress_bytes = proto.Field(
        proto.MESSAGE,
        number=6,
        message="Progress",
    )


class FieldOperationMetadata(proto.Message):
    r"""Metadata for
    [google.longrunning.Operation][google.longrunning.Operation] results
    from
    [FirestoreAdmin.UpdateField][google.firestore.admin.v1.FirestoreAdmin.UpdateField].

    Attributes:
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The time this operation started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time this operation completed. Will be
            unset if operation still in progress.
        field (str):
            The field resource that this operation is acting on. For
            example:
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/fields/{field_path}``
        index_config_deltas (Sequence[google.cloud.firestore_admin_v1.types.FieldOperationMetadata.IndexConfigDelta]):
            A list of
            [IndexConfigDelta][google.firestore.admin.v1.FieldOperationMetadata.IndexConfigDelta],
            which describe the intent of this operation.
        state (google.cloud.firestore_admin_v1.types.OperationState):
            The state of the operation.
        progress_documents (google.cloud.firestore_admin_v1.types.Progress):
            The progress, in documents, of this
            operation.
        progress_bytes (google.cloud.firestore_admin_v1.types.Progress):
            The progress, in bytes, of this operation.
        ttl_config_delta (google.cloud.firestore_admin_v1.types.FieldOperationMetadata.TtlConfigDelta):
            Describes the deltas of TTL configuration.
    """

    class IndexConfigDelta(proto.Message):
        r"""Information about an index configuration change.

        Attributes:
            change_type (google.cloud.firestore_admin_v1.types.FieldOperationMetadata.IndexConfigDelta.ChangeType):
                Specifies how the index is changing.
            index (google.cloud.firestore_admin_v1.types.Index):
                The index being changed.
        """

        class ChangeType(proto.Enum):
            r"""Specifies how the index is changing."""
            CHANGE_TYPE_UNSPECIFIED = 0
            ADD = 1
            REMOVE = 2

        change_type = proto.Field(
            proto.ENUM,
            number=1,
            enum="FieldOperationMetadata.IndexConfigDelta.ChangeType",
        )
        index = proto.Field(
            proto.MESSAGE,
            number=2,
            message=gfa_index.Index,
        )

    class TtlConfigDelta(proto.Message):
        r"""Information about an TTL configuration change.

        Attributes:
            change_type (google.cloud.firestore_admin_v1.types.FieldOperationMetadata.TtlConfigDelta.ChangeType):
                Specifies how the TTL configuration is
                changing.
        """

        class ChangeType(proto.Enum):
            r"""Specifies how the TTL config is changing."""
            CHANGE_TYPE_UNSPECIFIED = 0
            ADD = 1
            REMOVE = 2

        change_type = proto.Field(
            proto.ENUM,
            number=1,
            enum="FieldOperationMetadata.TtlConfigDelta.ChangeType",
        )

    start_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    field = proto.Field(
        proto.STRING,
        number=3,
    )
    index_config_deltas = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=IndexConfigDelta,
    )
    state = proto.Field(
        proto.ENUM,
        number=5,
        enum="OperationState",
    )
    progress_documents = proto.Field(
        proto.MESSAGE,
        number=6,
        message="Progress",
    )
    progress_bytes = proto.Field(
        proto.MESSAGE,
        number=7,
        message="Progress",
    )
    ttl_config_delta = proto.Field(
        proto.MESSAGE,
        number=8,
        message=TtlConfigDelta,
    )


class ExportDocumentsMetadata(proto.Message):
    r"""Metadata for
    [google.longrunning.Operation][google.longrunning.Operation] results
    from
    [FirestoreAdmin.ExportDocuments][google.firestore.admin.v1.FirestoreAdmin.ExportDocuments].

    Attributes:
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The time this operation started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time this operation completed. Will be
            unset if operation still in progress.
        operation_state (google.cloud.firestore_admin_v1.types.OperationState):
            The state of the export operation.
        progress_documents (google.cloud.firestore_admin_v1.types.Progress):
            The progress, in documents, of this
            operation.
        progress_bytes (google.cloud.firestore_admin_v1.types.Progress):
            The progress, in bytes, of this operation.
        collection_ids (Sequence[str]):
            Which collection ids are being exported.
        output_uri_prefix (str):
            Where the entities are being exported to.
    """

    start_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    operation_state = proto.Field(
        proto.ENUM,
        number=3,
        enum="OperationState",
    )
    progress_documents = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Progress",
    )
    progress_bytes = proto.Field(
        proto.MESSAGE,
        number=5,
        message="Progress",
    )
    collection_ids = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    output_uri_prefix = proto.Field(
        proto.STRING,
        number=7,
    )


class ImportDocumentsMetadata(proto.Message):
    r"""Metadata for
    [google.longrunning.Operation][google.longrunning.Operation] results
    from
    [FirestoreAdmin.ImportDocuments][google.firestore.admin.v1.FirestoreAdmin.ImportDocuments].

    Attributes:
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The time this operation started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time this operation completed. Will be
            unset if operation still in progress.
        operation_state (google.cloud.firestore_admin_v1.types.OperationState):
            The state of the import operation.
        progress_documents (google.cloud.firestore_admin_v1.types.Progress):
            The progress, in documents, of this
            operation.
        progress_bytes (google.cloud.firestore_admin_v1.types.Progress):
            The progress, in bytes, of this operation.
        collection_ids (Sequence[str]):
            Which collection ids are being imported.
        input_uri_prefix (str):
            The location of the documents being imported.
    """

    start_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    operation_state = proto.Field(
        proto.ENUM,
        number=3,
        enum="OperationState",
    )
    progress_documents = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Progress",
    )
    progress_bytes = proto.Field(
        proto.MESSAGE,
        number=5,
        message="Progress",
    )
    collection_ids = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    input_uri_prefix = proto.Field(
        proto.STRING,
        number=7,
    )


class ExportDocumentsResponse(proto.Message):
    r"""Returned in the
    [google.longrunning.Operation][google.longrunning.Operation]
    response field.

    Attributes:
        output_uri_prefix (str):
            Location of the output files. This can be
            used to begin an import into Cloud Firestore
            (this project or another project) after the
            operation completes successfully.
    """

    output_uri_prefix = proto.Field(
        proto.STRING,
        number=1,
    )


class Progress(proto.Message):
    r"""Describes the progress of the operation. Unit of work is generic and
    must be interpreted based on where
    [Progress][google.firestore.admin.v1.Progress] is used.

    Attributes:
        estimated_work (int):
            The amount of work estimated.
        completed_work (int):
            The amount of work completed.
    """

    estimated_work = proto.Field(
        proto.INT64,
        number=1,
    )
    completed_work = proto.Field(
        proto.INT64,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
