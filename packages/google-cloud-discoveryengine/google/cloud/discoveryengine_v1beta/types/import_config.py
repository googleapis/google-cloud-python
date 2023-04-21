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
from google.rpc import status_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.discoveryengine_v1beta.types import document, user_event

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1beta",
    manifest={
        "GcsSource",
        "BigQuerySource",
        "ImportErrorConfig",
        "ImportUserEventsRequest",
        "ImportUserEventsResponse",
        "ImportUserEventsMetadata",
        "ImportDocumentsMetadata",
        "ImportDocumentsRequest",
        "ImportDocumentsResponse",
    },
)


class GcsSource(proto.Message):
    r"""Cloud Storage location for input content.

    Attributes:
        input_uris (MutableSequence[str]):
            Required. Cloud Storage URIs to input files. URI can be up
            to 2000 characters long. URIs can match the full object path
            (for example, ``gs://bucket/directory/object.json``) or a
            pattern matching one or more files, such as
            ``gs://bucket/directory/*.json``.

            A request can contain at most 100 files (or 100,000 files if
            ``data_schema`` is ``content``). Each file can be up to 2 GB
            (or 100 MB if ``data_schema`` is ``content``).
        data_schema (str):
            The schema to use when parsing the data from the source.

            Supported values for document imports:

            -  ``document`` (default): One JSON
               [Document][google.cloud.discoveryengine.v1beta.Document]
               per line. Each document must have a valid
               [Document.id][google.cloud.discoveryengine.v1beta.Document.id].
            -  ``content``: Unstructured data (e.g. PDF, HTML). Each
               file matched by ``input_uris`` will become a document,
               with the ID set to the first 128 bits of SHA256(URI)
               encoded as a hex string.
            -  ``custom``: One custom data JSON per row in arbitrary
               format that conforms the defined
               [Schema][google.cloud.discoveryengine.v1beta.Schema] of
               the data store. This can only be used by the GENERIC Data
               Store vertical.

            Supported values for user even imports:

            -  ``user_event`` (default): One JSON
               [UserEvent][google.cloud.discoveryengine.v1beta.UserEvent]
               per line.
    """

    input_uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    data_schema: str = proto.Field(
        proto.STRING,
        number=2,
    )


class BigQuerySource(proto.Message):
    r"""BigQuery source import data from.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        partition_date (google.type.date_pb2.Date):
            BigQuery time partitioned table's \_PARTITIONDATE in
            YYYY-MM-DD format.

            This field is a member of `oneof`_ ``partition``.
        project_id (str):
            The project ID (can be project # or ID) that
            the BigQuery source is in with a length limit of
            128 characters. If not specified, inherits the
            project ID from the parent request.
        dataset_id (str):
            Required. The BigQuery data set to copy the
            data from with a length limit of 1,024
            characters.
        table_id (str):
            Required. The BigQuery table to copy the data
            from with a length limit of 1,024 characters.
        gcs_staging_dir (str):
            Intermediate Cloud Storage directory used for
            the import with a length limit of 2,000
            characters. Can be specified if one wants to
            have the BigQuery export to a specific Cloud
            Storage directory.
        data_schema (str):
            The schema to use when parsing the data from the source.

            Supported values for user event imports:

            -  ``user_event`` (default): One
               [UserEvent][google.cloud.discoveryengine.v1beta.UserEvent]
               per row.

            Supported values for document imports:

            -  ``document`` (default): One
               [Document][google.cloud.discoveryengine.v1beta.Document]
               format per row. Each document must have a valid
               [Document.id][google.cloud.discoveryengine.v1beta.Document.id]
               and one of
               [Document.json_data][google.cloud.discoveryengine.v1beta.Document.json_data]
               or
               [Document.struct_data][google.cloud.discoveryengine.v1beta.Document.struct_data].
            -  ``custom``: One custom data per row in arbitrary format
               that conforms the defined
               [Schema][google.cloud.discoveryengine.v1beta.Schema] of
               the data store. This can only be used by the GENERIC Data
               Store vertical.
    """

    partition_date: date_pb2.Date = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="partition",
        message=date_pb2.Date,
    )
    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    table_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    gcs_staging_dir: str = proto.Field(
        proto.STRING,
        number=4,
    )
    data_schema: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ImportErrorConfig(proto.Message):
    r"""Configuration of destination for Import related errors.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_prefix (str):
            Cloud Storage prefix for import errors. This must be an
            empty, existing Cloud Storage directory. Import errors will
            be written to sharded files in this directory, one per line,
            as a JSON-encoded ``google.rpc.Status`` message.

            This field is a member of `oneof`_ ``destination``.
    """

    gcs_prefix: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="destination",
    )


class ImportUserEventsRequest(proto.Message):
    r"""Request message for the ImportUserEvents request.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        inline_source (google.cloud.discoveryengine_v1beta.types.ImportUserEventsRequest.InlineSource):
            Required. The Inline source for the input
            content for UserEvents.

            This field is a member of `oneof`_ ``source``.
        gcs_source (google.cloud.discoveryengine_v1beta.types.GcsSource):
            Required. Cloud Storage location for the
            input content.

            This field is a member of `oneof`_ ``source``.
        bigquery_source (google.cloud.discoveryengine_v1beta.types.BigQuerySource):
            Required. BigQuery input source.

            This field is a member of `oneof`_ ``source``.
        parent (str):
            Required. Parent DataStore resource name, of the form
            ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}``
        error_config (google.cloud.discoveryengine_v1beta.types.ImportErrorConfig):
            The desired location of errors incurred
            during the Import. Cannot be set for inline user
            event imports.
    """

    class InlineSource(proto.Message):
        r"""The inline source for the input config for ImportUserEvents
        method.

        Attributes:
            user_events (MutableSequence[google.cloud.discoveryengine_v1beta.types.UserEvent]):
                Required. A list of user events to import.
                Recommended max of 10k items.
        """

        user_events: MutableSequence[user_event.UserEvent] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=user_event.UserEvent,
        )

    inline_source: InlineSource = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="source",
        message=InlineSource,
    )
    gcs_source: "GcsSource" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="source",
        message="GcsSource",
    )
    bigquery_source: "BigQuerySource" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="source",
        message="BigQuerySource",
    )
    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    error_config: "ImportErrorConfig" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="ImportErrorConfig",
    )


class ImportUserEventsResponse(proto.Message):
    r"""Response of the ImportUserEventsRequest. If the long running
    operation was successful, then this message is returned by the
    google.longrunning.Operations.response field if the operation
    was successful.

    Attributes:
        error_samples (MutableSequence[google.rpc.status_pb2.Status]):
            A sample of errors encountered while
            processing the request.
        error_config (google.cloud.discoveryengine_v1beta.types.ImportErrorConfig):
            Echoes the destination for the complete
            errors if this field was set in the request.
        joined_events_count (int):
            Count of user events imported with complete
            existing Documents.
        unjoined_events_count (int):
            Count of user events imported, but with
            Document information not found in the existing
            Branch.
    """

    error_samples: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=status_pb2.Status,
    )
    error_config: "ImportErrorConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ImportErrorConfig",
    )
    joined_events_count: int = proto.Field(
        proto.INT64,
        number=3,
    )
    unjoined_events_count: int = proto.Field(
        proto.INT64,
        number=4,
    )


class ImportUserEventsMetadata(proto.Message):
    r"""Metadata related to the progress of the Import operation.
    This will be returned by the
    google.longrunning.Operation.metadata field.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation create time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation last update time. If the operation
            is done, this is also the finish time.
        success_count (int):
            Count of entries that were processed
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


class ImportDocumentsMetadata(proto.Message):
    r"""Metadata related to the progress of the ImportDocuments
    operation. This will be returned by the
    google.longrunning.Operation.metadata field.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation create time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation last update time. If the operation
            is done, this is also the finish time.
        success_count (int):
            Count of entries that were processed
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


class ImportDocumentsRequest(proto.Message):
    r"""Request message for Import methods.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        inline_source (google.cloud.discoveryengine_v1beta.types.ImportDocumentsRequest.InlineSource):
            The Inline source for the input content for
            documents.

            This field is a member of `oneof`_ ``source``.
        gcs_source (google.cloud.discoveryengine_v1beta.types.GcsSource):
            Cloud Storage location for the input content.

            This field is a member of `oneof`_ ``source``.
        bigquery_source (google.cloud.discoveryengine_v1beta.types.BigQuerySource):
            BigQuery input source.

            This field is a member of `oneof`_ ``source``.
        parent (str):
            Required. The parent branch resource name, such as
            ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}``.
            Requires create/update permission.
        error_config (google.cloud.discoveryengine_v1beta.types.ImportErrorConfig):
            The desired location of errors incurred
            during the Import.
        reconciliation_mode (google.cloud.discoveryengine_v1beta.types.ImportDocumentsRequest.ReconciliationMode):
            The mode of reconciliation between existing documents and
            the documents to be imported. Defaults to
            [ReconciliationMode.INCREMENTAL][google.cloud.discoveryengine.v1beta.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL].
    """

    class ReconciliationMode(proto.Enum):
        r"""Indicates how imported documents are reconciled with the
        existing documents created or imported before.

        Values:
            RECONCILIATION_MODE_UNSPECIFIED (0):
                Defaults to INCREMENTAL.
            INCREMENTAL (1):
                Inserts new documents or updates existing
                documents.
            FULL (2):
                Calculates diff and replaces the entire
                document dataset. Existing documents may be
                deleted if they are not present in the source
                location.
        """
        RECONCILIATION_MODE_UNSPECIFIED = 0
        INCREMENTAL = 1
        FULL = 2

    class InlineSource(proto.Message):
        r"""The inline source for the input config for ImportDocuments
        method.

        Attributes:
            documents (MutableSequence[google.cloud.discoveryengine_v1beta.types.Document]):
                Required. A list of documents to update/create. Each
                document must have a valid
                [Document.id][google.cloud.discoveryengine.v1beta.Document.id].
                Recommended max of 100 items.
        """

        documents: MutableSequence[document.Document] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=document.Document,
        )

    inline_source: InlineSource = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="source",
        message=InlineSource,
    )
    gcs_source: "GcsSource" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="source",
        message="GcsSource",
    )
    bigquery_source: "BigQuerySource" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="source",
        message="BigQuerySource",
    )
    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    error_config: "ImportErrorConfig" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="ImportErrorConfig",
    )
    reconciliation_mode: ReconciliationMode = proto.Field(
        proto.ENUM,
        number=6,
        enum=ReconciliationMode,
    )


class ImportDocumentsResponse(proto.Message):
    r"""Response of the
    [ImportDocumentsRequest][google.cloud.discoveryengine.v1beta.ImportDocumentsRequest].
    If the long running operation is done, then this message is returned
    by the google.longrunning.Operations.response field if the operation
    was successful.

    Attributes:
        error_samples (MutableSequence[google.rpc.status_pb2.Status]):
            A sample of errors encountered while
            processing the request.
        error_config (google.cloud.discoveryengine_v1beta.types.ImportErrorConfig):
            Echoes the destination for the complete
            errors in the request if set.
    """

    error_samples: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=status_pb2.Status,
    )
    error_config: "ImportErrorConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ImportErrorConfig",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
