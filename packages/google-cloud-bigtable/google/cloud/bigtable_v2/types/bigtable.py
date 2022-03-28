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

from google.cloud.bigtable_v2.types import data
from google.protobuf import wrappers_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.bigtable.v2",
    manifest={
        "ReadRowsRequest",
        "ReadRowsResponse",
        "SampleRowKeysRequest",
        "SampleRowKeysResponse",
        "MutateRowRequest",
        "MutateRowResponse",
        "MutateRowsRequest",
        "MutateRowsResponse",
        "CheckAndMutateRowRequest",
        "CheckAndMutateRowResponse",
        "PingAndWarmRequest",
        "PingAndWarmResponse",
        "ReadModifyWriteRowRequest",
        "ReadModifyWriteRowResponse",
    },
)


class ReadRowsRequest(proto.Message):
    r"""Request message for Bigtable.ReadRows.

    Attributes:
        table_name (str):
            Required. The unique name of the table from which to read.
            Values are of the form
            ``projects/<project>/instances/<instance>/tables/<table>``.
        app_profile_id (str):
            This value specifies routing for replication.
            If not specified, the "default" application
            profile will be used.
        rows (google.cloud.bigtable_v2.types.RowSet):
            The row keys and/or ranges to read
            sequentially. If not specified, reads from all
            rows.
        filter (google.cloud.bigtable_v2.types.RowFilter):
            The filter to apply to the contents of the
            specified row(s). If unset, reads the entirety
            of each row.
        rows_limit (int):
            The read will stop after committing to N
            rows' worth of results. The default (zero) is to
            return all results.
    """

    table_name = proto.Field(
        proto.STRING,
        number=1,
    )
    app_profile_id = proto.Field(
        proto.STRING,
        number=5,
    )
    rows = proto.Field(
        proto.MESSAGE,
        number=2,
        message=data.RowSet,
    )
    filter = proto.Field(
        proto.MESSAGE,
        number=3,
        message=data.RowFilter,
    )
    rows_limit = proto.Field(
        proto.INT64,
        number=4,
    )


class ReadRowsResponse(proto.Message):
    r"""Response message for Bigtable.ReadRows.

    Attributes:
        chunks (Sequence[google.cloud.bigtable_v2.types.ReadRowsResponse.CellChunk]):
            A collection of a row's contents as part of
            the read request.
        last_scanned_row_key (bytes):
            Optionally the server might return the row
            key of the last row it has scanned.  The client
            can use this to construct a more efficient retry
            request if needed: any row keys or portions of
            ranges less than this row key can be dropped
            from the request. This is primarily useful for
            cases where the server has read a lot of data
            that was filtered out since the last committed
            row key, allowing the client to skip that work
            on a retry.
    """

    class CellChunk(proto.Message):
        r"""Specifies a piece of a row's contents returned as part of the
        read response stream.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            row_key (bytes):
                The row key for this chunk of data.  If the
                row key is empty, this CellChunk is a
                continuation of the same row as the previous
                CellChunk in the response stream, even if that
                CellChunk was in a previous ReadRowsResponse
                message.
            family_name (google.protobuf.wrappers_pb2.StringValue):
                The column family name for this chunk of data. If this
                message is not present this CellChunk is a continuation of
                the same column family as the previous CellChunk. The empty
                string can occur as a column family name in a response so
                clients must check explicitly for the presence of this
                message, not just for ``family_name.value`` being non-empty.
            qualifier (google.protobuf.wrappers_pb2.BytesValue):
                The column qualifier for this chunk of data. If this message
                is not present, this CellChunk is a continuation of the same
                column as the previous CellChunk. Column qualifiers may be
                empty so clients must check for the presence of this
                message, not just for ``qualifier.value`` being non-empty.
            timestamp_micros (int):
                The cell's stored timestamp, which also uniquely identifies
                it within its column. Values are always expressed in
                microseconds, but individual tables may set a coarser
                granularity to further restrict the allowed values. For
                example, a table which specifies millisecond granularity
                will only allow values of ``timestamp_micros`` which are
                multiples of 1000. Timestamps are only set in the first
                CellChunk per cell (for cells split into multiple chunks).
            labels (Sequence[str]):
                Labels applied to the cell by a
                [RowFilter][google.bigtable.v2.RowFilter]. Labels are only
                set on the first CellChunk per cell.
            value (bytes):
                The value stored in the cell.  Cell values
                can be split across multiple CellChunks.  In
                that case only the value field will be set in
                CellChunks after the first: the timestamp and
                labels will only be present in the first
                CellChunk, even if the first CellChunk came in a
                previous ReadRowsResponse.
            value_size (int):
                If this CellChunk is part of a chunked cell value and this
                is not the final chunk of that cell, value_size will be set
                to the total length of the cell value. The client can use
                this size to pre-allocate memory to hold the full cell
                value.
            reset_row (bool):
                Indicates that the client should drop all previous chunks
                for ``row_key``, as it will be re-read from the beginning.

                This field is a member of `oneof`_ ``row_status``.
            commit_row (bool):
                Indicates that the client can safely process all previous
                chunks for ``row_key``, as its data has been fully read.

                This field is a member of `oneof`_ ``row_status``.
        """

        row_key = proto.Field(
            proto.BYTES,
            number=1,
        )
        family_name = proto.Field(
            proto.MESSAGE,
            number=2,
            message=wrappers_pb2.StringValue,
        )
        qualifier = proto.Field(
            proto.MESSAGE,
            number=3,
            message=wrappers_pb2.BytesValue,
        )
        timestamp_micros = proto.Field(
            proto.INT64,
            number=4,
        )
        labels = proto.RepeatedField(
            proto.STRING,
            number=5,
        )
        value = proto.Field(
            proto.BYTES,
            number=6,
        )
        value_size = proto.Field(
            proto.INT32,
            number=7,
        )
        reset_row = proto.Field(
            proto.BOOL,
            number=8,
            oneof="row_status",
        )
        commit_row = proto.Field(
            proto.BOOL,
            number=9,
            oneof="row_status",
        )

    chunks = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=CellChunk,
    )
    last_scanned_row_key = proto.Field(
        proto.BYTES,
        number=2,
    )


class SampleRowKeysRequest(proto.Message):
    r"""Request message for Bigtable.SampleRowKeys.

    Attributes:
        table_name (str):
            Required. The unique name of the table from which to sample
            row keys. Values are of the form
            ``projects/<project>/instances/<instance>/tables/<table>``.
        app_profile_id (str):
            This value specifies routing for replication.
            If not specified, the "default" application
            profile will be used.
    """

    table_name = proto.Field(
        proto.STRING,
        number=1,
    )
    app_profile_id = proto.Field(
        proto.STRING,
        number=2,
    )


class SampleRowKeysResponse(proto.Message):
    r"""Response message for Bigtable.SampleRowKeys.

    Attributes:
        row_key (bytes):
            Sorted streamed sequence of sample row keys
            in the table. The table might have contents
            before the first row key in the list and after
            the last one, but a key containing the empty
            string indicates "end of table" and will be the
            last response given, if present.
            Note that row keys in this list may not have
            ever been written to or read from, and users
            should therefore not make any assumptions about
            the row key structure that are specific to their
            use case.
        offset_bytes (int):
            Approximate total storage space used by all rows in the
            table which precede ``row_key``. Buffering the contents of
            all rows between two subsequent samples would require space
            roughly equal to the difference in their ``offset_bytes``
            fields.
    """

    row_key = proto.Field(
        proto.BYTES,
        number=1,
    )
    offset_bytes = proto.Field(
        proto.INT64,
        number=2,
    )


class MutateRowRequest(proto.Message):
    r"""Request message for Bigtable.MutateRow.

    Attributes:
        table_name (str):
            Required. The unique name of the table to which the mutation
            should be applied. Values are of the form
            ``projects/<project>/instances/<instance>/tables/<table>``.
        app_profile_id (str):
            This value specifies routing for replication.
            If not specified, the "default" application
            profile will be used.
        row_key (bytes):
            Required. The key of the row to which the
            mutation should be applied.
        mutations (Sequence[google.cloud.bigtable_v2.types.Mutation]):
            Required. Changes to be atomically applied to
            the specified row. Entries are applied in order,
            meaning that earlier mutations can be masked by
            later ones. Must contain at least one entry and
            at most 100000.
    """

    table_name = proto.Field(
        proto.STRING,
        number=1,
    )
    app_profile_id = proto.Field(
        proto.STRING,
        number=4,
    )
    row_key = proto.Field(
        proto.BYTES,
        number=2,
    )
    mutations = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=data.Mutation,
    )


class MutateRowResponse(proto.Message):
    r"""Response message for Bigtable.MutateRow."""


class MutateRowsRequest(proto.Message):
    r"""Request message for BigtableService.MutateRows.

    Attributes:
        table_name (str):
            Required. The unique name of the table to
            which the mutations should be applied.
        app_profile_id (str):
            This value specifies routing for replication.
            If not specified, the "default" application
            profile will be used.
        entries (Sequence[google.cloud.bigtable_v2.types.MutateRowsRequest.Entry]):
            Required. The row keys and corresponding
            mutations to be applied in bulk. Each entry is
            applied as an atomic mutation, but the entries
            may be applied in arbitrary order (even between
            entries for the same row). At least one entry
            must be specified, and in total the entries can
            contain at most 100000 mutations.
    """

    class Entry(proto.Message):
        r"""A mutation for a given row.

        Attributes:
            row_key (bytes):
                The key of the row to which the ``mutations`` should be
                applied.
            mutations (Sequence[google.cloud.bigtable_v2.types.Mutation]):
                Required. Changes to be atomically applied to
                the specified row. Mutations are applied in
                order, meaning that earlier mutations can be
                masked by later ones.
                You must specify at least one mutation.
        """

        row_key = proto.Field(
            proto.BYTES,
            number=1,
        )
        mutations = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message=data.Mutation,
        )

    table_name = proto.Field(
        proto.STRING,
        number=1,
    )
    app_profile_id = proto.Field(
        proto.STRING,
        number=3,
    )
    entries = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=Entry,
    )


class MutateRowsResponse(proto.Message):
    r"""Response message for BigtableService.MutateRows.

    Attributes:
        entries (Sequence[google.cloud.bigtable_v2.types.MutateRowsResponse.Entry]):
            One or more results for Entries from the
            batch request.
    """

    class Entry(proto.Message):
        r"""The result of applying a passed mutation in the original
        request.

        Attributes:
            index (int):
                The index into the original request's ``entries`` list of
                the Entry for which a result is being reported.
            status (google.rpc.status_pb2.Status):
                The result of the request Entry identified by ``index``.
                Depending on how requests are batched during execution, it
                is possible for one Entry to fail due to an error with
                another Entry. In the event that this occurs, the same error
                will be reported for both entries.
        """

        index = proto.Field(
            proto.INT64,
            number=1,
        )
        status = proto.Field(
            proto.MESSAGE,
            number=2,
            message=status_pb2.Status,
        )

    entries = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=Entry,
    )


class CheckAndMutateRowRequest(proto.Message):
    r"""Request message for Bigtable.CheckAndMutateRow.

    Attributes:
        table_name (str):
            Required. The unique name of the table to which the
            conditional mutation should be applied. Values are of the
            form
            ``projects/<project>/instances/<instance>/tables/<table>``.
        app_profile_id (str):
            This value specifies routing for replication.
            If not specified, the "default" application
            profile will be used.
        row_key (bytes):
            Required. The key of the row to which the
            conditional mutation should be applied.
        predicate_filter (google.cloud.bigtable_v2.types.RowFilter):
            The filter to be applied to the contents of the specified
            row. Depending on whether or not any results are yielded,
            either ``true_mutations`` or ``false_mutations`` will be
            executed. If unset, checks that the row contains any values
            at all.
        true_mutations (Sequence[google.cloud.bigtable_v2.types.Mutation]):
            Changes to be atomically applied to the specified row if
            ``predicate_filter`` yields at least one cell when applied
            to ``row_key``. Entries are applied in order, meaning that
            earlier mutations can be masked by later ones. Must contain
            at least one entry if ``false_mutations`` is empty, and at
            most 100000.
        false_mutations (Sequence[google.cloud.bigtable_v2.types.Mutation]):
            Changes to be atomically applied to the specified row if
            ``predicate_filter`` does not yield any cells when applied
            to ``row_key``. Entries are applied in order, meaning that
            earlier mutations can be masked by later ones. Must contain
            at least one entry if ``true_mutations`` is empty, and at
            most 100000.
    """

    table_name = proto.Field(
        proto.STRING,
        number=1,
    )
    app_profile_id = proto.Field(
        proto.STRING,
        number=7,
    )
    row_key = proto.Field(
        proto.BYTES,
        number=2,
    )
    predicate_filter = proto.Field(
        proto.MESSAGE,
        number=6,
        message=data.RowFilter,
    )
    true_mutations = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=data.Mutation,
    )
    false_mutations = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=data.Mutation,
    )


class CheckAndMutateRowResponse(proto.Message):
    r"""Response message for Bigtable.CheckAndMutateRow.

    Attributes:
        predicate_matched (bool):
            Whether or not the request's ``predicate_filter`` yielded
            any results for the specified row.
    """

    predicate_matched = proto.Field(
        proto.BOOL,
        number=1,
    )


class PingAndWarmRequest(proto.Message):
    r"""Request message for client connection keep-alive and warming.

    Attributes:
        name (str):
            Required. The unique name of the instance to check
            permissions for as well as respond. Values are of the form
            ``projects/<project>/instances/<instance>``.
        app_profile_id (str):
            This value specifies routing for replication.
            If not specified, the "default" application
            profile will be used.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    app_profile_id = proto.Field(
        proto.STRING,
        number=2,
    )


class PingAndWarmResponse(proto.Message):
    r"""Response message for Bigtable.PingAndWarm connection
    keepalive and warming.

    """


class ReadModifyWriteRowRequest(proto.Message):
    r"""Request message for Bigtable.ReadModifyWriteRow.

    Attributes:
        table_name (str):
            Required. The unique name of the table to which the
            read/modify/write rules should be applied. Values are of the
            form
            ``projects/<project>/instances/<instance>/tables/<table>``.
        app_profile_id (str):
            This value specifies routing for replication.
            If not specified, the "default" application
            profile will be used.
        row_key (bytes):
            Required. The key of the row to which the
            read/modify/write rules should be applied.
        rules (Sequence[google.cloud.bigtable_v2.types.ReadModifyWriteRule]):
            Required. Rules specifying how the specified
            row's contents are to be transformed into
            writes. Entries are applied in order, meaning
            that earlier rules will affect the results of
            later ones.
    """

    table_name = proto.Field(
        proto.STRING,
        number=1,
    )
    app_profile_id = proto.Field(
        proto.STRING,
        number=4,
    )
    row_key = proto.Field(
        proto.BYTES,
        number=2,
    )
    rules = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=data.ReadModifyWriteRule,
    )


class ReadModifyWriteRowResponse(proto.Message):
    r"""Response message for Bigtable.ReadModifyWriteRow.

    Attributes:
        row (google.cloud.bigtable_v2.types.Row):
            A Row containing the new contents of all
            cells modified by the request.
    """

    row = proto.Field(
        proto.MESSAGE,
        number=1,
        message=data.Row,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
