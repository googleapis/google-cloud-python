# Copyright 2015 Google Inc. All rights reserved.
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

"""User friendly container for Google Cloud Bigtable Row."""


from gcloud._helpers import _to_bytes
from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2


class Row(object):
    """Representation of a Google Cloud Bigtable Row.

    :type row_key: bytes
    :param row_key: The key for the current row.

    :type table: :class:`Table <gcloud.bigtable.table.Table>`
    :param table: The table that owns the row.
    """

    def __init__(self, row_key, table):
        self._row_key = _to_bytes(row_key)
        self._table = table


class RowFilter(object):
    """Basic filter to apply to cells in a row.

    These values can be combined via :class:`RowFilterChain`,
    :class:`RowFilterUnion` and :class:`ConditionalRowFilter`.

    .. note::

        This class is a do-nothing base class for all row filters.
    """

    def __ne__(self, other):
        return not self.__eq__(other)


class _BoolFilter(RowFilter):
    """Row filter that uses a boolean flag.

    :type flag: bool
    :param flag: An indicator if a setting is turned on or off.
    """

    def __init__(self, flag):
        self.flag = flag

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.flag == self.flag


class SinkFilter(_BoolFilter):
    """Advanced row filter to skip parent filters.

    :type flag: bool
    :param flag: ADVANCED USE ONLY. Hook for introspection into the row filter.
                 Outputs all cells directly to the output of the read rather
                 than to any parent filter. Cannot be used within the
                 ``predicate_filter``, ``true_filter``, or ``false_filter``
                 of a :class:`ConditionalRowFilter`.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(sink=self.flag)


class PassAllFilter(_BoolFilter):
    """Row filter equivalent to not filtering at all.

    :type flag: bool
    :param flag: Matches all cells, regardless of input. Functionally
                 equivalent to leaving ``filter`` unset, but included for
                 completeness.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(pass_all_filter=self.flag)


class BlockAllFilter(_BoolFilter):
    """Row filter that doesn't match any cells.

    :type flag: bool
    :param flag: Does not match any cells, regardless of input. Useful for
                 temporarily disabling just part of a filter.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(block_all_filter=self.flag)


class _RegexFilter(RowFilter):
    """Row filter that uses a regular expression.

    The ``regex`` must be valid RE2 patterns. See Google's
    `RE2 reference`_ for the accepted syntax.

    .. _RE2 reference: https://github.com/google/re2/wiki/Syntax

    :type regex: bytes or str
    :param regex: A regular expression (RE2) for some row filter.
    """

    def __init__(self, regex):
        self.regex = regex

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.regex == self.regex


class RowKeyRegexFilter(_RegexFilter):
    """Row filter for a row key regular expression.

    The ``regex`` must be valid RE2 patterns. See Google's
    `RE2 reference`_ for the accepted syntax.

    .. _RE2 reference: https://github.com/google/re2/wiki/Syntax

    .. note::

        Special care need be used with the expression used. Since
        each of these properties can contain arbitrary bytes, the ``\\C``
        escape sequence must be used if a true wildcard is desired. The ``.``
        character will not match the new line character ``\\n``, which may be
        present in a binary value.

    :type regex: bytes
    :param regex: A regular expression (RE2) to match cells from rows with row
                  keys that satisfy this regex. For a
                  ``CheckAndMutateRowRequest``, this filter is unnecessary
                  since the row key is already specified.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(row_key_regex_filter=self.regex)


class FamilyNameRegexFilter(_RegexFilter):
    """Row filter for a family name regular expression.

    The ``regex`` must be valid RE2 patterns. See Google's
    `RE2 reference`_ for the accepted syntax.

    .. _RE2 reference: https://github.com/google/re2/wiki/Syntax

    :type regex: str
    :param regex: A regular expression (RE2) to match cells from columns in a
                  given column family. For technical reasons, the regex must
                  not contain the ``':'`` character, even if it is not being
                  used as a literal.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(family_name_regex_filter=self.regex)


class ColumnQualifierRegexFilter(_RegexFilter):
    """Row filter for a column qualifier regular expression.

    The ``regex`` must be valid RE2 patterns. See Google's
    `RE2 reference`_ for the accepted syntax.

    .. _RE2 reference: https://github.com/google/re2/wiki/Syntax

    .. note::

        Special care need be used with the expression used. Since
        each of these properties can contain arbitrary bytes, the ``\\C``
        escape sequence must be used if a true wildcard is desired. The ``.``
        character will not match the new line character ``\\n``, which may be
        present in a binary value.

    :type regex: bytes
    :param regex: A regular expression (RE2) to match cells from column that
                  match this regex (irrespective of column family).
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(column_qualifier_regex_filter=self.regex)


class ValueRegexFilter(_RegexFilter):
    """Row filter for a value regular expression.

    The ``regex`` must be valid RE2 patterns. See Google's
    `RE2 reference`_ for the accepted syntax.

    .. _RE2 reference: https://github.com/google/re2/wiki/Syntax

    .. note::

        Special care need be used with the expression used. Since
        each of these properties can contain arbitrary bytes, the ``\\C``
        escape sequence must be used if a true wildcard is desired. The ``.``
        character will not match the new line character ``\\n``, which may be
        present in a binary value.

    :type regex: bytes
    :param regex: A regular expression (RE2) to match cells with values that
                  match this regex.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(value_regex_filter=self.regex)


class _CellCountFilter(RowFilter):
    """Row filter that uses an integer count of cells.

    The cell count is used as an offset or a limit for the number
    of results returned.

    :type num_cells: int
    :param num_cells: An integer count / offset / limit.
    """

    def __init__(self, num_cells):
        self.num_cells = num_cells

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.num_cells == self.num_cells


class CellsRowOffsetFilter(_CellCountFilter):
    """Row filter to skip cells in a row.

    :type num_cells: int
    :param num_cells: Skips the first N cells of the row.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(cells_per_row_offset_filter=self.num_cells)


class CellsRowLimitFilter(_CellCountFilter):
    """Row filter to limit cells in a row.

    :type num_cells: int
    :param num_cells: Matches only the first N cells of the row.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(cells_per_row_limit_filter=self.num_cells)


class CellsColumnLimitFilter(_CellCountFilter):
    """Row filter to limit cells in a column.

    :type num_cells: int
    :param num_cells: Matches only the most recent N cells within each column.
                      This filters a (family name, column) pair, based on
                      timestamps of each cell.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(cells_per_column_limit_filter=self.num_cells)


class StripValueTransformerFilter(_BoolFilter):
    """Row filter that transforms cells into empty string (0 bytes).

    :type flag: bool
    :param flag: If :data:`True`, replaces each cell's value with the empty
                 string. As the name indicates, this is more useful as a
                 transformer than a generic query / filter.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(strip_value_transformer=self.flag)
