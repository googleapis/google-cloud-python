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


__protobuf__ = proto.module(
    package="google.bigtable.v2",
    manifest={
        "Row",
        "Family",
        "Column",
        "Cell",
        "RowRange",
        "RowSet",
        "ColumnRange",
        "TimestampRange",
        "ValueRange",
        "RowFilter",
        "Mutation",
        "ReadModifyWriteRule",
    },
)


class Row(proto.Message):
    r"""Specifies the complete (requested) contents of a single row
    of a table. Rows which exceed 256MiB in size cannot be read in
    full.

    Attributes:
        key (bytes):
            The unique key which identifies this row
            within its table. This is the same key that's
            used to identify the row in, for example, a
            MutateRowRequest. May contain any non-empty byte
            string up to 4KiB in length.
        families (Sequence[google.cloud.bigtable_v2.types.Family]):
            May be empty, but only if the entire row is
            empty. The mutual ordering of column families is
            not specified.
    """

    key = proto.Field(
        proto.BYTES,
        number=1,
    )
    families = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Family",
    )


class Family(proto.Message):
    r"""Specifies (some of) the contents of a single row/column
    family intersection of a table.

    Attributes:
        name (str):
            The unique key which identifies this family within its row.
            This is the same key that's used to identify the family in,
            for example, a RowFilter which sets its
            "family_name_regex_filter" field. Must match
            ``[-_.a-zA-Z0-9]+``, except that AggregatingRowProcessors
            may produce cells in a sentinel family with an empty name.
            Must be no greater than 64 characters in length.
        columns (Sequence[google.cloud.bigtable_v2.types.Column]):
            Must not be empty. Sorted in order of
            increasing "qualifier".
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    columns = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Column",
    )


class Column(proto.Message):
    r"""Specifies (some of) the contents of a single row/column
    intersection of a table.

    Attributes:
        qualifier (bytes):
            The unique key which identifies this column within its
            family. This is the same key that's used to identify the
            column in, for example, a RowFilter which sets its
            ``column_qualifier_regex_filter`` field. May contain any
            byte string, including the empty string, up to 16kiB in
            length.
        cells (Sequence[google.cloud.bigtable_v2.types.Cell]):
            Must not be empty. Sorted in order of decreasing
            "timestamp_micros".
    """

    qualifier = proto.Field(
        proto.BYTES,
        number=1,
    )
    cells = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Cell",
    )


class Cell(proto.Message):
    r"""Specifies (some of) the contents of a single
    row/column/timestamp of a table.

    Attributes:
        timestamp_micros (int):
            The cell's stored timestamp, which also uniquely identifies
            it within its column. Values are always expressed in
            microseconds, but individual tables may set a coarser
            granularity to further restrict the allowed values. For
            example, a table which specifies millisecond granularity
            will only allow values of ``timestamp_micros`` which are
            multiples of 1000.
        value (bytes):
            The value stored in the cell.
            May contain any byte string, including the empty
            string, up to 100MiB in length.
        labels (Sequence[str]):
            Labels applied to the cell by a
            [RowFilter][google.bigtable.v2.RowFilter].
    """

    timestamp_micros = proto.Field(
        proto.INT64,
        number=1,
    )
    value = proto.Field(
        proto.BYTES,
        number=2,
    )
    labels = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class RowRange(proto.Message):
    r"""Specifies a contiguous range of rows.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        start_key_closed (bytes):
            Used when giving an inclusive lower bound for
            the range.

            This field is a member of `oneof`_ ``start_key``.
        start_key_open (bytes):
            Used when giving an exclusive lower bound for
            the range.

            This field is a member of `oneof`_ ``start_key``.
        end_key_open (bytes):
            Used when giving an exclusive upper bound for
            the range.

            This field is a member of `oneof`_ ``end_key``.
        end_key_closed (bytes):
            Used when giving an inclusive upper bound for
            the range.

            This field is a member of `oneof`_ ``end_key``.
    """

    start_key_closed = proto.Field(
        proto.BYTES,
        number=1,
        oneof="start_key",
    )
    start_key_open = proto.Field(
        proto.BYTES,
        number=2,
        oneof="start_key",
    )
    end_key_open = proto.Field(
        proto.BYTES,
        number=3,
        oneof="end_key",
    )
    end_key_closed = proto.Field(
        proto.BYTES,
        number=4,
        oneof="end_key",
    )


class RowSet(proto.Message):
    r"""Specifies a non-contiguous set of rows.

    Attributes:
        row_keys (Sequence[bytes]):
            Single rows included in the set.
        row_ranges (Sequence[google.cloud.bigtable_v2.types.RowRange]):
            Contiguous row ranges included in the set.
    """

    row_keys = proto.RepeatedField(
        proto.BYTES,
        number=1,
    )
    row_ranges = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="RowRange",
    )


class ColumnRange(proto.Message):
    r"""Specifies a contiguous range of columns within a single column
    family. The range spans from <column_family>:<start_qualifier> to
    <column_family>:<end_qualifier>, where both bounds can be either
    inclusive or exclusive.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        family_name (str):
            The name of the column family within which
            this range falls.
        start_qualifier_closed (bytes):
            Used when giving an inclusive lower bound for
            the range.

            This field is a member of `oneof`_ ``start_qualifier``.
        start_qualifier_open (bytes):
            Used when giving an exclusive lower bound for
            the range.

            This field is a member of `oneof`_ ``start_qualifier``.
        end_qualifier_closed (bytes):
            Used when giving an inclusive upper bound for
            the range.

            This field is a member of `oneof`_ ``end_qualifier``.
        end_qualifier_open (bytes):
            Used when giving an exclusive upper bound for
            the range.

            This field is a member of `oneof`_ ``end_qualifier``.
    """

    family_name = proto.Field(
        proto.STRING,
        number=1,
    )
    start_qualifier_closed = proto.Field(
        proto.BYTES,
        number=2,
        oneof="start_qualifier",
    )
    start_qualifier_open = proto.Field(
        proto.BYTES,
        number=3,
        oneof="start_qualifier",
    )
    end_qualifier_closed = proto.Field(
        proto.BYTES,
        number=4,
        oneof="end_qualifier",
    )
    end_qualifier_open = proto.Field(
        proto.BYTES,
        number=5,
        oneof="end_qualifier",
    )


class TimestampRange(proto.Message):
    r"""Specified a contiguous range of microsecond timestamps.

    Attributes:
        start_timestamp_micros (int):
            Inclusive lower bound. If left empty,
            interpreted as 0.
        end_timestamp_micros (int):
            Exclusive upper bound. If left empty,
            interpreted as infinity.
    """

    start_timestamp_micros = proto.Field(
        proto.INT64,
        number=1,
    )
    end_timestamp_micros = proto.Field(
        proto.INT64,
        number=2,
    )


class ValueRange(proto.Message):
    r"""Specifies a contiguous range of raw byte values.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        start_value_closed (bytes):
            Used when giving an inclusive lower bound for
            the range.

            This field is a member of `oneof`_ ``start_value``.
        start_value_open (bytes):
            Used when giving an exclusive lower bound for
            the range.

            This field is a member of `oneof`_ ``start_value``.
        end_value_closed (bytes):
            Used when giving an inclusive upper bound for
            the range.

            This field is a member of `oneof`_ ``end_value``.
        end_value_open (bytes):
            Used when giving an exclusive upper bound for
            the range.

            This field is a member of `oneof`_ ``end_value``.
    """

    start_value_closed = proto.Field(
        proto.BYTES,
        number=1,
        oneof="start_value",
    )
    start_value_open = proto.Field(
        proto.BYTES,
        number=2,
        oneof="start_value",
    )
    end_value_closed = proto.Field(
        proto.BYTES,
        number=3,
        oneof="end_value",
    )
    end_value_open = proto.Field(
        proto.BYTES,
        number=4,
        oneof="end_value",
    )


class RowFilter(proto.Message):
    r"""Takes a row as input and produces an alternate view of the row based
    on specified rules. For example, a RowFilter might trim down a row
    to include just the cells from columns matching a given regular
    expression, or might return all the cells of a row but not their
    values. More complicated filters can be composed out of these
    components to express requests such as, "within every column of a
    particular family, give just the two most recent cells which are
    older than timestamp X."

    There are two broad categories of RowFilters (true filters and
    transformers), as well as two ways to compose simple filters into
    more complex ones (chains and interleaves). They work as follows:

    -  True filters alter the input row by excluding some of its cells
       wholesale from the output row. An example of a true filter is the
       ``value_regex_filter``, which excludes cells whose values don't
       match the specified pattern. All regex true filters use RE2
       syntax (https://github.com/google/re2/wiki/Syntax) in raw byte
       mode (RE2::Latin1), and are evaluated as full matches. An
       important point to keep in mind is that ``RE2(.)`` is equivalent
       by default to ``RE2([^\n])``, meaning that it does not match
       newlines. When attempting to match an arbitrary byte, you should
       therefore use the escape sequence ``\C``, which may need to be
       further escaped as ``\\C`` in your client language.

    -  Transformers alter the input row by changing the values of some
       of its cells in the output, without excluding them completely.
       Currently, the only supported transformer is the
       ``strip_value_transformer``, which replaces every cell's value
       with the empty string.

    -  Chains and interleaves are described in more detail in the
       RowFilter.Chain and RowFilter.Interleave documentation.

    The total serialized size of a RowFilter message must not exceed
    20480 bytes, and RowFilters may not be nested within each other (in
    Chains or Interleaves) to a depth of more than 20.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        chain (google.cloud.bigtable_v2.types.RowFilter.Chain):
            Applies several RowFilters to the data in
            sequence, progressively narrowing the results.

            This field is a member of `oneof`_ ``filter``.
        interleave (google.cloud.bigtable_v2.types.RowFilter.Interleave):
            Applies several RowFilters to the data in
            parallel and combines the results.

            This field is a member of `oneof`_ ``filter``.
        condition (google.cloud.bigtable_v2.types.RowFilter.Condition):
            Applies one of two possible RowFilters to the
            data based on the output of a predicate
            RowFilter.

            This field is a member of `oneof`_ ``filter``.
        sink (bool):
            ADVANCED USE ONLY. Hook for introspection into the
            RowFilter. Outputs all cells directly to the output of the
            read rather than to any parent filter. Consider the
            following example:

            ::

                Chain(
                  FamilyRegex("A"),
                  Interleave(
                    All(),
                    Chain(Label("foo"), Sink())
                  ),
                  QualifierRegex("B")
                )

                                    A,A,1,w
                                    A,B,2,x
                                    B,B,4,z
                                       |
                                FamilyRegex("A")
                                       |
                                    A,A,1,w
                                    A,B,2,x
                                       |
                          +------------+-------------+
                          |                          |
                        All()                    Label(foo)
                          |                          |
                       A,A,1,w              A,A,1,w,labels:[foo]
                       A,B,2,x              A,B,2,x,labels:[foo]
                          |                          |
                          |                        Sink() --------------+
                          |                          |                  |
                          +------------+      x------+          A,A,1,w,labels:[foo]
                                       |                        A,B,2,x,labels:[foo]
                                    A,A,1,w                             |
                                    A,B,2,x                             |
                                       |                                |
                               QualifierRegex("B")                      |
                                       |                                |
                                    A,B,2,x                             |
                                       |                                |
                                       +--------------------------------+
                                       |
                                    A,A,1,w,labels:[foo]
                                    A,B,2,x,labels:[foo]  // could be switched
                                    A,B,2,x               // could be switched

            Despite being excluded by the qualifier filter, a copy of
            every cell that reaches the sink is present in the final
            result.

            As with an
            [Interleave][google.bigtable.v2.RowFilter.Interleave],
            duplicate cells are possible, and appear in an unspecified
            mutual order. In this case we have a duplicate with column
            "A:B" and timestamp 2, because one copy passed through the
            all filter while the other was passed through the label and
            sink. Note that one copy has label "foo", while the other
            does not.

            Cannot be used within the ``predicate_filter``,
            ``true_filter``, or ``false_filter`` of a
            [Condition][google.bigtable.v2.RowFilter.Condition].

            This field is a member of `oneof`_ ``filter``.
        pass_all_filter (bool):
            Matches all cells, regardless of input. Functionally
            equivalent to leaving ``filter`` unset, but included for
            completeness.

            This field is a member of `oneof`_ ``filter``.
        block_all_filter (bool):
            Does not match any cells, regardless of
            input. Useful for temporarily disabling just
            part of a filter.

            This field is a member of `oneof`_ ``filter``.
        row_key_regex_filter (bytes):
            Matches only cells from rows whose keys satisfy the given
            RE2 regex. In other words, passes through the entire row
            when the key matches, and otherwise produces an empty row.
            Note that, since row keys can contain arbitrary bytes, the
            ``\C`` escape sequence must be used if a true wildcard is
            desired. The ``.`` character will not match the new line
            character ``\n``, which may be present in a binary key.

            This field is a member of `oneof`_ ``filter``.
        row_sample_filter (float):
            Matches all cells from a row with probability
            p, and matches no cells from the row with
            probability 1-p.

            This field is a member of `oneof`_ ``filter``.
        family_name_regex_filter (str):
            Matches only cells from columns whose families satisfy the
            given RE2 regex. For technical reasons, the regex must not
            contain the ``:`` character, even if it is not being used as
            a literal. Note that, since column families cannot contain
            the new line character ``\n``, it is sufficient to use ``.``
            as a full wildcard when matching column family names.

            This field is a member of `oneof`_ ``filter``.
        column_qualifier_regex_filter (bytes):
            Matches only cells from columns whose qualifiers satisfy the
            given RE2 regex. Note that, since column qualifiers can
            contain arbitrary bytes, the ``\C`` escape sequence must be
            used if a true wildcard is desired. The ``.`` character will
            not match the new line character ``\n``, which may be
            present in a binary qualifier.

            This field is a member of `oneof`_ ``filter``.
        column_range_filter (google.cloud.bigtable_v2.types.ColumnRange):
            Matches only cells from columns within the
            given range.

            This field is a member of `oneof`_ ``filter``.
        timestamp_range_filter (google.cloud.bigtable_v2.types.TimestampRange):
            Matches only cells with timestamps within the
            given range.

            This field is a member of `oneof`_ ``filter``.
        value_regex_filter (bytes):
            Matches only cells with values that satisfy the given
            regular expression. Note that, since cell values can contain
            arbitrary bytes, the ``\C`` escape sequence must be used if
            a true wildcard is desired. The ``.`` character will not
            match the new line character ``\n``, which may be present in
            a binary value.

            This field is a member of `oneof`_ ``filter``.
        value_range_filter (google.cloud.bigtable_v2.types.ValueRange):
            Matches only cells with values that fall
            within the given range.

            This field is a member of `oneof`_ ``filter``.
        cells_per_row_offset_filter (int):
            Skips the first N cells of each row, matching
            all subsequent cells. If duplicate cells are
            present, as is possible when using an
            Interleave, each copy of the cell is counted
            separately.

            This field is a member of `oneof`_ ``filter``.
        cells_per_row_limit_filter (int):
            Matches only the first N cells of each row.
            If duplicate cells are present, as is possible
            when using an Interleave, each copy of the cell
            is counted separately.

            This field is a member of `oneof`_ ``filter``.
        cells_per_column_limit_filter (int):
            Matches only the most recent N cells within each column. For
            example, if N=2, this filter would match column ``foo:bar``
            at timestamps 10 and 9, skip all earlier cells in
            ``foo:bar``, and then begin matching again in column
            ``foo:bar2``. If duplicate cells are present, as is possible
            when using an Interleave, each copy of the cell is counted
            separately.

            This field is a member of `oneof`_ ``filter``.
        strip_value_transformer (bool):
            Replaces each cell's value with the empty
            string.

            This field is a member of `oneof`_ ``filter``.
        apply_label_transformer (str):
            Applies the given label to all cells in the output row. This
            allows the client to determine which results were produced
            from which part of the filter.

            Values must be at most 15 characters in length, and match
            the RE2 pattern ``[a-z0-9\\-]+``

            Due to a technical limitation, it is not currently possible
            to apply multiple labels to a cell. As a result, a Chain may
            have no more than one sub-filter which contains a
            ``apply_label_transformer``. It is okay for an Interleave to
            contain multiple ``apply_label_transformers``, as they will
            be applied to separate copies of the input. This may be
            relaxed in the future.

            This field is a member of `oneof`_ ``filter``.
    """

    class Chain(proto.Message):
        r"""A RowFilter which sends rows through several RowFilters in
        sequence.

        Attributes:
            filters (Sequence[google.cloud.bigtable_v2.types.RowFilter]):
                The elements of "filters" are chained
                together to process the input row: in row ->
                f(0) -> intermediate row -> f(1) -> ... -> f(N)
                -> out row The full chain is executed
                atomically.
        """

        filters = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="RowFilter",
        )

    class Interleave(proto.Message):
        r"""A RowFilter which sends each row to each of several component
        RowFilters and interleaves the results.

        Attributes:
            filters (Sequence[google.cloud.bigtable_v2.types.RowFilter]):
                The elements of "filters" all process a copy of the input
                row, and the results are pooled, sorted, and combined into a
                single output row. If multiple cells are produced with the
                same column and timestamp, they will all appear in the
                output row in an unspecified mutual order. Consider the
                following example, with three filters:

                ::

                                                 input row
                                                     |
                           -----------------------------------------------------
                           |                         |                         |
                          f(0)                      f(1)                      f(2)
                           |                         |                         |
                    1: foo,bar,10,x             foo,bar,10,z              far,bar,7,a
                    2: foo,blah,11,z            far,blah,5,x              far,blah,5,x
                           |                         |                         |
                           -----------------------------------------------------
                                                     |
                    1:                      foo,bar,10,z   // could have switched with #2
                    2:                      foo,bar,10,x   // could have switched with #1
                    3:                      foo,blah,11,z
                    4:                      far,bar,7,a
                    5:                      far,blah,5,x   // identical to #6
                    6:                      far,blah,5,x   // identical to #5

                All interleaved filters are executed atomically.
        """

        filters = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="RowFilter",
        )

    class Condition(proto.Message):
        r"""A RowFilter which evaluates one of two possible RowFilters,
        depending on whether or not a predicate RowFilter outputs any
        cells from the input row.
        IMPORTANT NOTE: The predicate filter does not execute atomically
        with the true and false filters, which may lead to inconsistent
        or unexpected results. Additionally, Condition filters have poor
        performance, especially when filters are set for the false
        condition.

        Attributes:
            predicate_filter (google.cloud.bigtable_v2.types.RowFilter):
                If ``predicate_filter`` outputs any cells, then
                ``true_filter`` will be evaluated on the input row.
                Otherwise, ``false_filter`` will be evaluated.
            true_filter (google.cloud.bigtable_v2.types.RowFilter):
                The filter to apply to the input row if ``predicate_filter``
                returns any results. If not provided, no results will be
                returned in the true case.
            false_filter (google.cloud.bigtable_v2.types.RowFilter):
                The filter to apply to the input row if ``predicate_filter``
                does not return any results. If not provided, no results
                will be returned in the false case.
        """

        predicate_filter = proto.Field(
            proto.MESSAGE,
            number=1,
            message="RowFilter",
        )
        true_filter = proto.Field(
            proto.MESSAGE,
            number=2,
            message="RowFilter",
        )
        false_filter = proto.Field(
            proto.MESSAGE,
            number=3,
            message="RowFilter",
        )

    chain = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="filter",
        message=Chain,
    )
    interleave = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="filter",
        message=Interleave,
    )
    condition = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="filter",
        message=Condition,
    )
    sink = proto.Field(
        proto.BOOL,
        number=16,
        oneof="filter",
    )
    pass_all_filter = proto.Field(
        proto.BOOL,
        number=17,
        oneof="filter",
    )
    block_all_filter = proto.Field(
        proto.BOOL,
        number=18,
        oneof="filter",
    )
    row_key_regex_filter = proto.Field(
        proto.BYTES,
        number=4,
        oneof="filter",
    )
    row_sample_filter = proto.Field(
        proto.DOUBLE,
        number=14,
        oneof="filter",
    )
    family_name_regex_filter = proto.Field(
        proto.STRING,
        number=5,
        oneof="filter",
    )
    column_qualifier_regex_filter = proto.Field(
        proto.BYTES,
        number=6,
        oneof="filter",
    )
    column_range_filter = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="filter",
        message="ColumnRange",
    )
    timestamp_range_filter = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="filter",
        message="TimestampRange",
    )
    value_regex_filter = proto.Field(
        proto.BYTES,
        number=9,
        oneof="filter",
    )
    value_range_filter = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="filter",
        message="ValueRange",
    )
    cells_per_row_offset_filter = proto.Field(
        proto.INT32,
        number=10,
        oneof="filter",
    )
    cells_per_row_limit_filter = proto.Field(
        proto.INT32,
        number=11,
        oneof="filter",
    )
    cells_per_column_limit_filter = proto.Field(
        proto.INT32,
        number=12,
        oneof="filter",
    )
    strip_value_transformer = proto.Field(
        proto.BOOL,
        number=13,
        oneof="filter",
    )
    apply_label_transformer = proto.Field(
        proto.STRING,
        number=19,
        oneof="filter",
    )


class Mutation(proto.Message):
    r"""Specifies a particular change to be made to the contents of a
    row.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        set_cell (google.cloud.bigtable_v2.types.Mutation.SetCell):
            Set a cell's value.

            This field is a member of `oneof`_ ``mutation``.
        delete_from_column (google.cloud.bigtable_v2.types.Mutation.DeleteFromColumn):
            Deletes cells from a column.

            This field is a member of `oneof`_ ``mutation``.
        delete_from_family (google.cloud.bigtable_v2.types.Mutation.DeleteFromFamily):
            Deletes cells from a column family.

            This field is a member of `oneof`_ ``mutation``.
        delete_from_row (google.cloud.bigtable_v2.types.Mutation.DeleteFromRow):
            Deletes cells from the entire row.

            This field is a member of `oneof`_ ``mutation``.
    """

    class SetCell(proto.Message):
        r"""A Mutation which sets the value of the specified cell.

        Attributes:
            family_name (str):
                The name of the family into which new data should be
                written. Must match ``[-_.a-zA-Z0-9]+``
            column_qualifier (bytes):
                The qualifier of the column into which new
                data should be written. Can be any byte string,
                including the empty string.
            timestamp_micros (int):
                The timestamp of the cell into which new data
                should be written. Use -1 for current Bigtable
                server time. Otherwise, the client should set
                this value itself, noting that the default value
                is a timestamp of zero if the field is left
                unspecified. Values must match the granularity
                of the table (e.g. micros, millis).
            value (bytes):
                The value to be written into the specified
                cell.
        """

        family_name = proto.Field(
            proto.STRING,
            number=1,
        )
        column_qualifier = proto.Field(
            proto.BYTES,
            number=2,
        )
        timestamp_micros = proto.Field(
            proto.INT64,
            number=3,
        )
        value = proto.Field(
            proto.BYTES,
            number=4,
        )

    class DeleteFromColumn(proto.Message):
        r"""A Mutation which deletes cells from the specified column,
        optionally restricting the deletions to a given timestamp range.

        Attributes:
            family_name (str):
                The name of the family from which cells should be deleted.
                Must match ``[-_.a-zA-Z0-9]+``
            column_qualifier (bytes):
                The qualifier of the column from which cells
                should be deleted. Can be any byte string,
                including the empty string.
            time_range (google.cloud.bigtable_v2.types.TimestampRange):
                The range of timestamps within which cells
                should be deleted.
        """

        family_name = proto.Field(
            proto.STRING,
            number=1,
        )
        column_qualifier = proto.Field(
            proto.BYTES,
            number=2,
        )
        time_range = proto.Field(
            proto.MESSAGE,
            number=3,
            message="TimestampRange",
        )

    class DeleteFromFamily(proto.Message):
        r"""A Mutation which deletes all cells from the specified column
        family.

        Attributes:
            family_name (str):
                The name of the family from which cells should be deleted.
                Must match ``[-_.a-zA-Z0-9]+``
        """

        family_name = proto.Field(
            proto.STRING,
            number=1,
        )

    class DeleteFromRow(proto.Message):
        r"""A Mutation which deletes all cells from the containing row."""

    set_cell = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="mutation",
        message=SetCell,
    )
    delete_from_column = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="mutation",
        message=DeleteFromColumn,
    )
    delete_from_family = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="mutation",
        message=DeleteFromFamily,
    )
    delete_from_row = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="mutation",
        message=DeleteFromRow,
    )


class ReadModifyWriteRule(proto.Message):
    r"""Specifies an atomic read/modify/write operation on the latest
    value of the specified column.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        family_name (str):
            The name of the family to which the read/modify/write should
            be applied. Must match ``[-_.a-zA-Z0-9]+``
        column_qualifier (bytes):
            The qualifier of the column to which the
            read/modify/write should be applied.
            Can be any byte string, including the empty
            string.
        append_value (bytes):
            Rule specifying that ``append_value`` be appended to the
            existing value. If the targeted cell is unset, it will be
            treated as containing the empty string.

            This field is a member of `oneof`_ ``rule``.
        increment_amount (int):
            Rule specifying that ``increment_amount`` be added to the
            existing value. If the targeted cell is unset, it will be
            treated as containing a zero. Otherwise, the targeted cell
            must contain an 8-byte value (interpreted as a 64-bit
            big-endian signed integer), or the entire request will fail.

            This field is a member of `oneof`_ ``rule``.
    """

    family_name = proto.Field(
        proto.STRING,
        number=1,
    )
    column_qualifier = proto.Field(
        proto.BYTES,
        number=2,
    )
    append_value = proto.Field(
        proto.BYTES,
        number=3,
        oneof="rule",
    )
    increment_amount = proto.Field(
        proto.INT64,
        number=4,
        oneof="rule",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
