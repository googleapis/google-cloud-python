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
from google.type import date_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.discoveryengine_v1alpha.types import completion, document, user_event

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1alpha",
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
        "ImportSuggestionDenyListEntriesRequest",
        "ImportSuggestionDenyListEntriesResponse",
        "ImportSuggestionDenyListEntriesMetadata",
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
               [Document][google.cloud.discoveryengine.v1alpha.Document]
               per line. Each document must have a valid
               [Document.id][google.cloud.discoveryengine.v1alpha.Document.id].
            -  ``content``: Unstructured data (e.g. PDF, HTML). Each
               file matched by ``input_uris`` becomes a document, with
               the ID set to the first 128 bits of SHA256(URI) encoded
               as a hex string.
            -  ``custom``: One custom data JSON per row in arbitrary
               format that conforms to the defined
               [Schema][google.cloud.discoveryengine.v1alpha.Schema] of
               the data store. This can only be used by Gen App Builder.
            -  ``csv``: A CSV file with header conforming to the defined
               [Schema][google.cloud.discoveryengine.v1alpha.Schema] of
               the data store. Each entry after the header is imported
               as a Document. This can only be used by Gen App Builder.

            Supported values for user even imports:

            -  ``user_event`` (default): One JSON
               [UserEvent][google.cloud.discoveryengine.v1alpha.UserEvent]
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
               [UserEvent][google.cloud.discoveryengine.v1alpha.UserEvent]
               per row.

            Supported values for document imports:

            -  ``document`` (default): One
               [Document][google.cloud.discoveryengine.v1alpha.Document]
               format per row. Each document must have a valid
               [Document.id][google.cloud.discoveryengine.v1alpha.Document.id]
               and one of
               [Document.json_data][google.cloud.discoveryengine.v1alpha.Document.json_data]
               or
               [Document.struct_data][google.cloud.discoveryengine.v1alpha.Document.struct_data].
            -  ``custom``: One custom data per row in arbitrary format
               that conforms to the defined
               [Schema][google.cloud.discoveryengine.v1alpha.Schema] of
               the data store. This can only be used by Gen App Builder.
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
            empty, existing Cloud Storage directory. Import errors are
            written to sharded files in this directory, one per line, as
            a JSON-encoded ``google.rpc.Status`` message.

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
        inline_source (google.cloud.discoveryengine_v1alpha.types.ImportUserEventsRequest.InlineSource):
            The Inline source for the input content for
            UserEvents.

            This field is a member of `oneof`_ ``source``.
        gcs_source (google.cloud.discoveryengine_v1alpha.types.GcsSource):
            Cloud Storage location for the input content.

            This field is a member of `oneof`_ ``source``.
        bigquery_source (google.cloud.discoveryengine_v1alpha.types.BigQuerySource):
            BigQuery input source.

            This field is a member of `oneof`_ ``source``.
        parent (str):
            Required. Parent DataStore resource name, of the form
            ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}``
        error_config (google.cloud.discoveryengine_v1alpha.types.ImportErrorConfig):
            The desired location of errors incurred
            during the Import. Cannot be set for inline user
            event imports.
    """

    class InlineSource(proto.Message):
        r"""The inline source for the input config for ImportUserEvents
        method.

        Attributes:
            user_events (MutableSequence[google.cloud.discoveryengine_v1alpha.types.UserEvent]):
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
        error_config (google.cloud.discoveryengine_v1alpha.types.ImportErrorConfig):
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
    This is returned by the google.longrunning.Operation.metadata
    field.

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
    operation. This is returned by the
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
        inline_source (google.cloud.discoveryengine_v1alpha.types.ImportDocumentsRequest.InlineSource):
            The Inline source for the input content for
            documents.

            This field is a member of `oneof`_ ``source``.
        gcs_source (google.cloud.discoveryengine_v1alpha.types.GcsSource):
            Cloud Storage location for the input content.

            This field is a member of `oneof`_ ``source``.
        bigquery_source (google.cloud.discoveryengine_v1alpha.types.BigQuerySource):
            BigQuery input source.

            This field is a member of `oneof`_ ``source``.
        parent (str):
            Required. The parent branch resource name, such as
            ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}``.
            Requires create/update permission.
        error_config (google.cloud.discoveryengine_v1alpha.types.ImportErrorConfig):
            The desired location of errors incurred
            during the Import.
        reconciliation_mode (google.cloud.discoveryengine_v1alpha.types.ImportDocumentsRequest.ReconciliationMode):
            The mode of reconciliation between existing documents and
            the documents to be imported. Defaults to
            [ReconciliationMode.INCREMENTAL][google.cloud.discoveryengine.v1alpha.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL].
        auto_generate_ids (bool):
            Whether to automatically generate IDs for the documents if
            absent.

            If set to ``true``,
            [Document.id][google.cloud.discoveryengine.v1alpha.Document.id]s
            are automatically generated based on the hash of the
            payload, where IDs may not be consistent during multiple
            imports. In which case
            [ReconciliationMode.FULL][google.cloud.discoveryengine.v1alpha.ImportDocumentsRequest.ReconciliationMode.FULL]
            is highly recommended to avoid duplicate contents. If unset
            or set to ``false``,
            [Document.id][google.cloud.discoveryengine.v1alpha.Document.id]s
            have to be specified using
            [id_field][google.cloud.discoveryengine.v1alpha.ImportDocumentsRequest.id_field],
            otherwise, documents without IDs fail to be imported.

            Only set this field when using
            [GcsSource][google.cloud.discoveryengine.v1alpha.GcsSource]
            or
            [BigQuerySource][google.cloud.discoveryengine.v1alpha.BigQuerySource],
            and when
            [GcsSource.data_schema][google.cloud.discoveryengine.v1alpha.GcsSource.data_schema]
            or
            [BigQuerySource.data_schema][google.cloud.discoveryengine.v1alpha.BigQuerySource.data_schema]
            is ``custom`` or ``csv``. Otherwise, an INVALID_ARGUMENT
            error is thrown.
        id_field (str):
            The field in the Cloud Storage and BigQuery sources that
            indicates the unique IDs of the documents.

            For
            [GcsSource][google.cloud.discoveryengine.v1alpha.GcsSource]
            it is the key of the JSON field. For instance, ``my_id`` for
            JSON ``{"my_id": "some_uuid"}``. For
            [BigQuerySource][google.cloud.discoveryengine.v1alpha.BigQuerySource]
            it is the column name of the BigQuery table where the unique
            ids are stored.

            The values of the JSON field or the BigQuery column are used
            as the
            [Document.id][google.cloud.discoveryengine.v1alpha.Document.id]s.
            The JSON field or the BigQuery column must be of string
            type, and the values must be set as valid strings conform to
            `RFC-1034 <https://tools.ietf.org/html/rfc1034>`__ with 1-63
            characters. Otherwise, documents without valid IDs fail to
            be imported.

            Only set this field when using
            [GcsSource][google.cloud.discoveryengine.v1alpha.GcsSource]
            or
            [BigQuerySource][google.cloud.discoveryengine.v1alpha.BigQuerySource],
            and when
            [GcsSource.data_schema][google.cloud.discoveryengine.v1alpha.GcsSource.data_schema]
            or
            [BigQuerySource.data_schema][google.cloud.discoveryengine.v1alpha.BigQuerySource.data_schema]
            is ``custom``. And only set this field when
            [auto_generate_ids][google.cloud.discoveryengine.v1alpha.ImportDocumentsRequest.auto_generate_ids]
            is unset or set as ``false``. Otherwise, an INVALID_ARGUMENT
            error is thrown.

            If it is unset, a default value ``_id`` is used when
            importing from the allowed data sources.
    """

    class ReconciliationMode(proto.Enum):
        r"""Indicates how imported documents are reconciled with the
        existing documents created or imported before.

        Values:
            RECONCILIATION_MODE_UNSPECIFIED (0):
                Defaults to ``INCREMENTAL``.
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
            documents (MutableSequence[google.cloud.discoveryengine_v1alpha.types.Document]):
                Required. A list of documents to update/create. Each
                document must have a valid
                [Document.id][google.cloud.discoveryengine.v1alpha.Document.id].
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
    auto_generate_ids: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    id_field: str = proto.Field(
        proto.STRING,
        number=9,
    )


class ImportDocumentsResponse(proto.Message):
    r"""Response of the
    [ImportDocumentsRequest][google.cloud.discoveryengine.v1alpha.ImportDocumentsRequest].
    If the long running operation is done, then this message is returned
    by the google.longrunning.Operations.response field if the operation
    was successful.

    Attributes:
        error_samples (MutableSequence[google.rpc.status_pb2.Status]):
            A sample of errors encountered while
            processing the request.
        error_config (google.cloud.discoveryengine_v1alpha.types.ImportErrorConfig):
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


class ImportSuggestionDenyListEntriesRequest(proto.Message):
    r"""Request message for
    [CompletionService.ImportSuggestionDenyListEntries][google.cloud.discoveryengine.v1alpha.CompletionService.ImportSuggestionDenyListEntries]
    method.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        inline_source (google.cloud.discoveryengine_v1alpha.types.ImportSuggestionDenyListEntriesRequest.InlineSource):
            The Inline source for the input content for
            suggestion deny list entries.

            This field is a member of `oneof`_ ``source``.
        gcs_source (google.cloud.discoveryengine_v1alpha.types.GcsSource):
            Cloud Storage location for the input content.

            Only 1 file can be specified that contains all entries to
            import. Supported values ``gcs_source.schema`` for
            autocomplete suggestion deny list entry imports:

            -  ``suggestion_deny_list`` (default): One JSON
               [SuggestionDenyListEntry] per line.

            This field is a member of `oneof`_ ``source``.
        parent (str):
            Required. The parent data store resource name for which to
            import denylist entries. Follows pattern
            projects/\ */locations/*/collections/*/dataStores/*.
    """

    class InlineSource(proto.Message):
        r"""The inline source for SuggestionDenyListEntry.

        Attributes:
            entries (MutableSequence[google.cloud.discoveryengine_v1alpha.types.SuggestionDenyListEntry]):
                Required. A list of all denylist entries to
                import. Max of 1000 items.
        """

        entries: MutableSequence[
            completion.SuggestionDenyListEntry
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=completion.SuggestionDenyListEntry,
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
    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ImportSuggestionDenyListEntriesResponse(proto.Message):
    r"""Response message for
    [CompletionService.ImportSuggestionDenyListEntries][google.cloud.discoveryengine.v1alpha.CompletionService.ImportSuggestionDenyListEntries]
    method.

    Attributes:
        error_samples (MutableSequence[google.rpc.status_pb2.Status]):
            A sample of errors encountered while
            processing the request.
        imported_entries_count (int):
            Count of deny list entries successfully
            imported.
        failed_entries_count (int):
            Count of deny list entries that failed to be
            imported.
    """

    error_samples: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=status_pb2.Status,
    )
    imported_entries_count: int = proto.Field(
        proto.INT64,
        number=2,
    )
    failed_entries_count: int = proto.Field(
        proto.INT64,
        number=3,
    )


class ImportSuggestionDenyListEntriesMetadata(proto.Message):
    r"""Metadata related to the progress of the
    ImportSuggestionDenyListEntries operation. This is returned by
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


__all__ = tuple(sorted(__protobuf__.manifest))
