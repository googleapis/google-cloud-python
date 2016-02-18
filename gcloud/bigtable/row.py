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


import struct

import six

from gcloud._helpers import _datetime_from_microseconds
from gcloud._helpers import _microseconds_from_datetime
from gcloud._helpers import _to_bytes
from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2
from gcloud.bigtable._generated import (
    bigtable_service_messages_pb2 as messages_pb2)


_MAX_MUTATIONS = 100000
_PACK_I64 = struct.Struct('>q').pack


class Row(object):
    """Representation of a Google Cloud Bigtable Row.

    .. note::

        A :class:`Row` accumulates mutations locally via the :meth:`set_cell`,
        :meth:`delete`, :meth:`delete_cell` and :meth:`delete_cells` methods.
        To actually send these mutations to the Google Cloud Bigtable API, you
        must call :meth:`commit`. If a ``filter_`` is set on the :class:`Row`,
        the mutations must have an associated state: :data:`True` or
        :data:`False`. The mutations will be applied conditionally, based on
        whether the filter matches any cells in the :class:`Row` or not.

    :type row_key: bytes
    :param row_key: The key for the current row.

    :type table: :class:`Table <gcloud.bigtable.table.Table>`
    :param table: The table that owns the row.

    :type filter_: :class:`RowFilter`
    :param filter_: (Optional) Filter to be used for conditional mutations.
                    If a filter is set, then the :class:`Row` will accumulate
                    mutations for either a :data:`True` or :data:`False` state.
                    When :meth:`commit`-ed, the mutations for the :data:`True`
                    state will be applied if the filter matches any cells in
                    the row, otherwise the :data:`False` state will be.
    """

    ALL_COLUMNS = object()
    """Sentinel value used to indicate all columns in a column family."""

    def __init__(self, row_key, table, filter_=None):
        self._row_key = _to_bytes(row_key)
        self._table = table
        self._filter = filter_
        self._rule_pb_list = []
        if self._filter is None:
            self._pb_mutations = []
            self._true_pb_mutations = None
            self._false_pb_mutations = None
        else:
            self._pb_mutations = None
            self._true_pb_mutations = []
            self._false_pb_mutations = []

    def _get_mutations(self, state=None):
        """Gets the list of mutations for a given state.

        If the state is :data`None` but there is a filter set, then we've
        reached an invalid state. Similarly if no filter is set but the
        state is not :data:`None`.

        :type state: bool
        :param state: (Optional) The state that the mutation should be
                      applied in. Unset if the mutation is not conditional,
                      otherwise :data:`True` or :data:`False`.

        :rtype: list
        :returns: The list to add new mutations to (for the current state).
        :raises: :class:`ValueError <exceptions.ValueError>`
        """
        if state is None:
            if self._filter is not None:
                raise ValueError('A filter is set on the current row, but no '
                                 'state given for the mutation')
            return self._pb_mutations
        else:
            if self._filter is None:
                raise ValueError('No filter was set on the current row, but a '
                                 'state was given for the mutation')
            if state:
                return self._true_pb_mutations
            else:
                return self._false_pb_mutations

    def set_cell(self, column_family_id, column, value, timestamp=None,
                 state=None):
        """Sets a value in this row.

        The cell is determined by the ``row_key`` of the :class:`Row` and the
        ``column``. The ``column`` must be in an existing
        :class:`.column_family.ColumnFamily` (as determined by
        ``column_family_id``).

        .. note::

            This method adds a mutation to the accumulated mutations on this
            :class:`Row`, but does not make an API request. To actually
            send an API request (with the mutations) to the Google Cloud
            Bigtable API, call :meth:`commit`.

        :type column_family_id: str
        :param column_family_id: The column family that contains the column.
                                 Must be of the form
                                 ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

        :type column: bytes
        :param column: The column within the column family where the cell
                       is located.

        :type value: bytes or :class:`int`
        :param value: The value to set in the cell. If an integer is used,
                      will be interpreted as a 64-bit big-endian signed
                      integer (8 bytes).

        :type timestamp: :class:`datetime.datetime`
        :param timestamp: (Optional) The timestamp of the operation.

        :type state: bool
        :param state: (Optional) The state that the mutation should be
                      applied in. Unset if the mutation is not conditional,
                      otherwise :data:`True` or :data:`False`.
        """
        column = _to_bytes(column)
        if isinstance(value, six.integer_types):
            value = _PACK_I64(value)
        value = _to_bytes(value)
        if timestamp is None:
            # Use -1 for current Bigtable server time.
            timestamp_micros = -1
        else:
            timestamp_micros = _microseconds_from_datetime(timestamp)
            # Truncate to millisecond granularity.
            timestamp_micros -= (timestamp_micros % 1000)

        mutation_val = data_pb2.Mutation.SetCell(
            family_name=column_family_id,
            column_qualifier=column,
            timestamp_micros=timestamp_micros,
            value=value,
        )
        mutation_pb = data_pb2.Mutation(set_cell=mutation_val)
        self._get_mutations(state).append(mutation_pb)

    def append_cell_value(self, column_family_id, column, value):
        """Appends a value to an existing cell.

        .. note::

            This method adds a read-modify rule protobuf to the accumulated
            read-modify rules on this :class:`Row`, but does not make an API
            request. To actually send an API request (with the rules) to the
            Google Cloud Bigtable API, call :meth:`commit_modifications`.

        :type column_family_id: str
        :param column_family_id: The column family that contains the column.
                                 Must be of the form
                                 ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

        :type column: bytes
        :param column: The column within the column family where the cell
                       is located.

        :type value: bytes
        :param value: The value to append to the existing value in the cell. If
                      the targeted cell is unset, it will be treated as
                      containing the empty string.
        """
        column = _to_bytes(column)
        value = _to_bytes(value)
        rule_pb = data_pb2.ReadModifyWriteRule(family_name=column_family_id,
                                               column_qualifier=column,
                                               append_value=value)
        self._rule_pb_list.append(rule_pb)

    def increment_cell_value(self, column_family_id, column, int_value):
        """Increments a value in an existing cell.

        Assumes the value in the cell is stored as a 64 bit integer
        serialized to bytes.

        .. note::

            This method adds a read-modify rule protobuf to the accumulated
            read-modify rules on this :class:`Row`, but does not make an API
            request. To actually send an API request (with the rules) to the
            Google Cloud Bigtable API, call :meth:`commit_modifications`.

        :type column_family_id: str
        :param column_family_id: The column family that contains the column.
                                 Must be of the form
                                 ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

        :type column: bytes
        :param column: The column within the column family where the cell
                       is located.

        :type int_value: int
        :param int_value: The value to increment the existing value in the cell
                          by. If the targeted cell is unset, it will be treated
                          as containing a zero. Otherwise, the targeted cell
                          must contain an 8-byte value (interpreted as a 64-bit
                          big-endian signed integer), or the entire request
                          will fail.
        """
        column = _to_bytes(column)
        rule_pb = data_pb2.ReadModifyWriteRule(family_name=column_family_id,
                                               column_qualifier=column,
                                               increment_amount=int_value)
        self._rule_pb_list.append(rule_pb)

    def delete(self, state=None):
        """Deletes this row from the table.

        .. note::

            This method adds a mutation to the accumulated mutations on this
            :class:`Row`, but does not make an API request. To actually
            send an API request (with the mutations) to the Google Cloud
            Bigtable API, call :meth:`commit`.

        :type state: bool
        :param state: (Optional) The state that the mutation should be
                      applied in. Unset if the mutation is not conditional,
                      otherwise :data:`True` or :data:`False`.
        """
        mutation_val = data_pb2.Mutation.DeleteFromRow()
        mutation_pb = data_pb2.Mutation(delete_from_row=mutation_val)
        self._get_mutations(state).append(mutation_pb)

    def delete_cell(self, column_family_id, column, time_range=None,
                    state=None):
        """Deletes cell in this row.

        .. note::

            This method adds a mutation to the accumulated mutations on this
            :class:`Row`, but does not make an API request. To actually
            send an API request (with the mutations) to the Google Cloud
            Bigtable API, call :meth:`commit`.

        :type column_family_id: str
        :param column_family_id: The column family that contains the column
                                 or columns with cells being deleted. Must be
                                 of the form ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

        :type column: bytes
        :param column: The column within the column family that will have a
                       cell deleted.

        :type time_range: :class:`TimestampRange`
        :param time_range: (Optional) The range of time within which cells
                           should be deleted.

        :type state: bool
        :param state: (Optional) The state that the mutation should be
                      applied in. Unset if the mutation is not conditional,
                      otherwise :data:`True` or :data:`False`.
        """
        self.delete_cells(column_family_id, [column], time_range=time_range,
                          state=state)

    def delete_cells(self, column_family_id, columns, time_range=None,
                     state=None):
        """Deletes cells in this row.

        .. note::

            This method adds a mutation to the accumulated mutations on this
            :class:`Row`, but does not make an API request. To actually
            send an API request (with the mutations) to the Google Cloud
            Bigtable API, call :meth:`commit`.

        :type column_family_id: str
        :param column_family_id: The column family that contains the column
                                 or columns with cells being deleted. Must be
                                 of the form ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

        :type columns: :class:`list` of :class:`str` /
                       :func:`unicode <unicode>`, or :class:`object`
        :param columns: The columns within the column family that will have
                        cells deleted. If :attr:`Row.ALL_COLUMNS` is used then
                        the entire column family will be deleted from the row.

        :type time_range: :class:`TimestampRange`
        :param time_range: (Optional) The range of time within which cells
                           should be deleted.

        :type state: bool
        :param state: (Optional) The state that the mutation should be
                      applied in. Unset if the mutation is not conditional,
                      otherwise :data:`True` or :data:`False`.
        """
        mutations_list = self._get_mutations(state)
        if columns is self.ALL_COLUMNS:
            mutation_val = data_pb2.Mutation.DeleteFromFamily(
                family_name=column_family_id,
            )
            mutation_pb = data_pb2.Mutation(delete_from_family=mutation_val)
            mutations_list.append(mutation_pb)
        else:
            delete_kwargs = {}
            if time_range is not None:
                delete_kwargs['time_range'] = time_range.to_pb()

            to_append = []
            for column in columns:
                column = _to_bytes(column)
                # time_range will never change if present, but the rest of
                # delete_kwargs will
                delete_kwargs.update(
                    family_name=column_family_id,
                    column_qualifier=column,
                )
                mutation_val = data_pb2.Mutation.DeleteFromColumn(
                    **delete_kwargs)
                mutation_pb = data_pb2.Mutation(
                    delete_from_column=mutation_val)
                to_append.append(mutation_pb)

            # We don't add the mutations until all columns have been
            # processed without error.
            mutations_list.extend(to_append)

    def _commit_mutate(self):
        """Makes a ``MutateRow`` API request.

        Assumes no filter is set on the :class:`Row` and is meant to be called
        by :meth:`commit`.

        :raises: :class:`ValueError <exceptions.ValueError>` if the number of
                 mutations exceeds the ``_MAX_MUTATIONS``.
        """
        mutations_list = self._get_mutations()
        num_mutations = len(mutations_list)
        if num_mutations == 0:
            return
        if num_mutations > _MAX_MUTATIONS:
            raise ValueError('%d total mutations exceed the maximum allowable '
                             '%d.' % (num_mutations, _MAX_MUTATIONS))
        request_pb = messages_pb2.MutateRowRequest(
            table_name=self._table.name,
            row_key=self._row_key,
            mutations=mutations_list,
        )
        # We expect a `google.protobuf.empty_pb2.Empty`
        client = self._table._cluster._client
        client._data_stub.MutateRow(request_pb, client.timeout_seconds)

    def _commit_check_and_mutate(self):
        """Makes a ``CheckAndMutateRow`` API request.

        Assumes a filter is set on the :class:`Row` and is meant to be called
        by :meth:`commit`.

        :rtype: bool
        :returns: Flag indicating if the filter was matched (which also
                  indicates which set of mutations were applied by the server).
        :raises: :class:`ValueError <exceptions.ValueError>` if the number of
                 mutations exceeds the ``_MAX_MUTATIONS``.
        """
        true_mutations = self._get_mutations(state=True)
        false_mutations = self._get_mutations(state=False)
        num_true_mutations = len(true_mutations)
        num_false_mutations = len(false_mutations)
        if num_true_mutations == 0 and num_false_mutations == 0:
            return
        if (num_true_mutations > _MAX_MUTATIONS or
                num_false_mutations > _MAX_MUTATIONS):
            raise ValueError(
                'Exceed the maximum allowable mutations (%d). Had %s true '
                'mutations and %d false mutations.' % (
                    _MAX_MUTATIONS, num_true_mutations, num_false_mutations))

        request_pb = messages_pb2.CheckAndMutateRowRequest(
            table_name=self._table.name,
            row_key=self._row_key,
            predicate_filter=self._filter.to_pb(),
            true_mutations=true_mutations,
            false_mutations=false_mutations,
        )
        # We expect a `.messages_pb2.CheckAndMutateRowResponse`
        client = self._table._cluster._client
        resp = client._data_stub.CheckAndMutateRow(
            request_pb, client.timeout_seconds)
        return resp.predicate_matched

    def clear_mutations(self):
        """Removes all currently accumulated mutations on the current row."""
        if self._filter is None:
            del self._pb_mutations[:]
        else:
            del self._true_pb_mutations[:]
            del self._false_pb_mutations[:]

    def commit(self):
        """Makes a ``MutateRow`` or ``CheckAndMutateRow`` API request.

        If no mutations have been created in the row, no request is made.

        Mutations are applied atomically and in order, meaning that earlier
        mutations can be masked / negated by later ones. Cells already present
        in the row are left unchanged unless explicitly changed by a mutation.

        After committing the accumulated mutations, resets the local
        mutations to an empty list.

        In the case that a filter is set on the :class:`Row`, the mutations
        will be applied conditionally, based on whether the filter matches
        any cells in the :class:`Row` or not. (Each method which adds a
        mutation has a ``state`` parameter for this purpose.)

        :rtype: :class:`bool` or :data:`NoneType <types.NoneType>`
        :returns: :data:`None` if there is no filter, otherwise a flag
                  indicating if the filter was matched (which also
                  indicates which set of mutations were applied by the server).
        :raises: :class:`ValueError <exceptions.ValueError>` if the number of
                 mutations exceeds the ``_MAX_MUTATIONS``.
        """
        if self._filter is None:
            result = self._commit_mutate()
        else:
            result = self._commit_check_and_mutate()

        # Reset mutations after commit-ing request.
        self.clear_mutations()

        return result

    def clear_modification_rules(self):
        """Removes all currently accumulated modifications on current row."""
        del self._rule_pb_list[:]

    def commit_modifications(self):
        """Makes a ``ReadModifyWriteRow`` API request.

        This commits modifications made by :meth:`append_cell_value` and
        :meth:`increment_cell_value`. If no modifications were made, makes
        no API request and just returns ``{}``.

        Modifies a row atomically, reading the latest existing timestamp/value
        from the specified columns and writing a new value by appending /
        incrementing. The new cell created uses either the current server time
        or the highest timestamp of a cell in that column (if it exceeds the
        server time).

        :rtype: dict
        :returns: The new contents of all modified cells. Returned as a
                  dictionary of column families, each of which holds a
                  dictionary of columns. Each column contains a list of cells
                  modified. Each cell is represented with a two-tuple with the
                  value (in bytes) and the timestamp for the cell. For example:

                  .. code:: python

                      {
                          u'col-fam-id': {
                              b'col-name1': [
                                  (b'cell-val', datetime.datetime(...)),
                                  (b'cell-val-newer', datetime.datetime(...)),
                              ],
                              b'col-name2': [
                                  (b'altcol-cell-val', datetime.datetime(...)),
                              ],
                          },
                          u'col-fam-id2': {
                              b'col-name3-but-other-fam': [
                                  (b'foo', datetime.datetime(...)),
                              ],
                          },
                      }
        """
        if len(self._rule_pb_list) == 0:
            return {}
        request_pb = messages_pb2.ReadModifyWriteRowRequest(
            table_name=self._table.name,
            row_key=self._row_key,
            rules=self._rule_pb_list,
        )
        # We expect a `.data_pb2.Row`
        client = self._table._cluster._client
        row_response = client._data_stub.ReadModifyWriteRow(
            request_pb, client.timeout_seconds)

        # Reset modifications after commit-ing request.
        self.clear_modification_rules()

        # NOTE: We expect row_response.key == self._row_key but don't check.
        return _parse_rmw_row_response(row_response)


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


class RowSampleFilter(RowFilter):
    """Matches all cells from a row with probability p.

    :type sample: float
    :param sample: The probability of matching a cell (must be in the
                   interval ``[0, 1]``).
    """

    def __init__(self, sample):
        self.sample = sample

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.sample == self.sample

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(row_sample_filter=self.sample)


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


class TimestampRange(object):
    """Range of time with inclusive lower and exclusive upper bounds.

    :type start: :class:`datetime.datetime`
    :param start: (Optional) The (inclusive) lower bound of the timestamp
                  range. If omitted, defaults to Unix epoch.

    :type end: :class:`datetime.datetime`
    :param end: (Optional) The (exclusive) upper bound of the timestamp
                range. If omitted, no upper bound is used.
    """

    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.start == self.start and
                other.end == self.end)

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_pb(self):
        """Converts the :class:`TimestampRange` to a protobuf.

        :rtype: :class:`.data_pb2.TimestampRange`
        :returns: The converted current object.
        """
        timestamp_range_kwargs = {}
        if self.start is not None:
            timestamp_range_kwargs['start_timestamp_micros'] = (
                _microseconds_from_datetime(self.start))
        if self.end is not None:
            timestamp_range_kwargs['end_timestamp_micros'] = (
                _microseconds_from_datetime(self.end))
        return data_pb2.TimestampRange(**timestamp_range_kwargs)


class TimestampRangeFilter(RowFilter):
    """Row filter that limits cells to a range of time.

    :type range_: :class:`TimestampRange`
    :param range_: Range of time that cells should match against.
    """

    def __init__(self, range_):
        self.range_ = range_

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.range_ == self.range_

    def to_pb(self):
        """Converts the row filter to a protobuf.

        First converts the ``range_`` on the current object to a protobuf and
        then uses it in the ``timestamp_range_filter`` field.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(timestamp_range_filter=self.range_.to_pb())


class ColumnRangeFilter(RowFilter):
    """A row filter to restrict to a range of columns.

    Both the start and end column can be included or excluded in the range.
    By default, we include them both, but this can be changed with optional
    flags.

    :type column_family_id: str
    :param column_family_id: The column family that contains the columns. Must
                             be of the form ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

    :type start_column: bytes
    :param start_column: The start of the range of columns. If no value is
                         used, the backend applies no upper bound to the
                         values.

    :type end_column: bytes
    :param end_column: The end of the range of columns. If no value is used,
                       the backend applies no upper bound to the values.

    :type inclusive_start: bool
    :param inclusive_start: Boolean indicating if the start column should be
                            included in the range (or excluded). Defaults
                            to :data:`True` if ``start_column`` is passed and
                            no ``inclusive_start`` was given.

    :type inclusive_end: bool
    :param inclusive_end: Boolean indicating if the end column should be
                          included in the range (or excluded). Defaults
                          to :data:`True` if ``end_column`` is passed and
                          no ``inclusive_end`` was given.

    :raises: :class:`ValueError <exceptions.ValueError>` if ``inclusive_start``
             is set but no ``start_column`` is given or if ``inclusive_end``
             is set but no ``end_column`` is given
    """

    def __init__(self, column_family_id, start_column=None, end_column=None,
                 inclusive_start=None, inclusive_end=None):
        self.column_family_id = column_family_id

        if inclusive_start is None:
            inclusive_start = True
        elif start_column is None:
            raise ValueError('Inclusive start was specified but no '
                             'start column was given.')
        self.start_column = start_column
        self.inclusive_start = inclusive_start

        if inclusive_end is None:
            inclusive_end = True
        elif end_column is None:
            raise ValueError('Inclusive end was specified but no '
                             'end column was given.')
        self.end_column = end_column
        self.inclusive_end = inclusive_end

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.column_family_id == self.column_family_id and
                other.start_column == self.start_column and
                other.end_column == self.end_column and
                other.inclusive_start == self.inclusive_start and
                other.inclusive_end == self.inclusive_end)

    def to_pb(self):
        """Converts the row filter to a protobuf.

        First converts to a :class:`.data_pb2.ColumnRange` and then uses it
        in the ``column_range_filter`` field.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        column_range_kwargs = {'family_name': self.column_family_id}
        if self.start_column is not None:
            if self.inclusive_start:
                key = 'start_qualifier_inclusive'
            else:
                key = 'start_qualifier_exclusive'
            column_range_kwargs[key] = _to_bytes(self.start_column)
        if self.end_column is not None:
            if self.inclusive_end:
                key = 'end_qualifier_inclusive'
            else:
                key = 'end_qualifier_exclusive'
            column_range_kwargs[key] = _to_bytes(self.end_column)

        column_range = data_pb2.ColumnRange(**column_range_kwargs)
        return data_pb2.RowFilter(column_range_filter=column_range)


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


class ValueRangeFilter(RowFilter):
    """A range of values to restrict to in a row filter.

    Will only match cells that have values in this range.

    Both the start and end value can be included or excluded in the range.
    By default, we include them both, but this can be changed with optional
    flags.

    :type start_value: bytes
    :param start_value: The start of the range of values. If no value is used,
                        the backend applies no lower bound to the values.

    :type end_value: bytes
    :param end_value: The end of the range of values. If no value is used,
                      the backend applies no upper bound to the values.

    :type inclusive_start: bool
    :param inclusive_start: Boolean indicating if the start value should be
                            included in the range (or excluded). Defaults
                            to :data:`True` if ``start_value`` is passed and
                            no ``inclusive_start`` was given.

    :type inclusive_end: bool
    :param inclusive_end: Boolean indicating if the end value should be
                          included in the range (or excluded). Defaults
                          to :data:`True` if ``end_value`` is passed and
                          no ``inclusive_end`` was given.

    :raises: :class:`ValueError <exceptions.ValueError>` if ``inclusive_start``
             is set but no ``start_value`` is given or if ``inclusive_end``
             is set but no ``end_value`` is given
    """

    def __init__(self, start_value=None, end_value=None,
                 inclusive_start=None, inclusive_end=None):
        if inclusive_start is None:
            inclusive_start = True
        elif start_value is None:
            raise ValueError('Inclusive start was specified but no '
                             'start value was given.')
        self.start_value = start_value
        self.inclusive_start = inclusive_start

        if inclusive_end is None:
            inclusive_end = True
        elif end_value is None:
            raise ValueError('Inclusive end was specified but no '
                             'end value was given.')
        self.end_value = end_value
        self.inclusive_end = inclusive_end

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.start_value == self.start_value and
                other.end_value == self.end_value and
                other.inclusive_start == self.inclusive_start and
                other.inclusive_end == self.inclusive_end)

    def to_pb(self):
        """Converts the row filter to a protobuf.

        First converts to a :class:`.data_pb2.ValueRange` and then uses
        it to create a row filter protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        value_range_kwargs = {}
        if self.start_value is not None:
            if self.inclusive_start:
                key = 'start_value_inclusive'
            else:
                key = 'start_value_exclusive'
            value_range_kwargs[key] = _to_bytes(self.start_value)
        if self.end_value is not None:
            if self.inclusive_end:
                key = 'end_value_inclusive'
            else:
                key = 'end_value_exclusive'
            value_range_kwargs[key] = _to_bytes(self.end_value)

        value_range = data_pb2.ValueRange(**value_range_kwargs)
        return data_pb2.RowFilter(value_range_filter=value_range)


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


class ApplyLabelFilter(RowFilter):
    """Filter to apply labels to cells.

    Intended to be used as an intermediate filter on a pre-existing filtered
    result set. This was if two sets are combined, the label can tell where
    the cell(s) originated.This allows the client to determine which results
    were produced from which part of the filter.

    .. note::

        Due to a technical limitation, it is not currently possible to apply
        multiple labels to a cell.

    :type label: str
    :param label: Label to apply to cells in the output row. Values must be
                  at most 15 characters long, and match the pattern
                  ``[a-z0-9\\-]+``.
    """

    def __init__(self, label):
        self.label = label

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.label == self.label

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(apply_label_transformer=self.label)


class _FilterCombination(RowFilter):
    """Chain of row filters.

    Sends rows through several filters in sequence. The filters are "chained"
    together to process a row. After the first filter is applied, the second
    is applied to the filtered output and so on for subsequent filters.

    :type filters: list
    :param filters: List of :class:`RowFilter`
    """

    def __init__(self, filters=None):
        if filters is None:
            filters = []
        self.filters = filters

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.filters == self.filters


class RowFilterChain(_FilterCombination):
    """Chain of row filters.

    Sends rows through several filters in sequence. The filters are "chained"
    together to process a row. After the first filter is applied, the second
    is applied to the filtered output and so on for subsequent filters.

    :type filters: list
    :param filters: List of :class:`RowFilter`
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        chain = data_pb2.RowFilter.Chain(
            filters=[row_filter.to_pb() for row_filter in self.filters])
        return data_pb2.RowFilter(chain=chain)


class RowFilterUnion(_FilterCombination):
    """Union of row filters.

    Sends rows through several filters simultaneously, then
    merges / interleaves all the filtered results together.

    If multiple cells are produced with the same column and timestamp,
    they will all appear in the output row in an unspecified mutual order.

    :type filters: list
    :param filters: List of :class:`RowFilter`
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        interleave = data_pb2.RowFilter.Interleave(
            filters=[row_filter.to_pb() for row_filter in self.filters])
        return data_pb2.RowFilter(interleave=interleave)


class ConditionalRowFilter(RowFilter):
    """Conditional row filter which exhibits ternary behavior.

    Executes one of two filters based on another filter. If the ``base_filter``
    returns any cells in the row, then ``true_filter`` is executed. If not,
    then ``false_filter`` is executed.

    .. note::

        The ``base_filter`` does not execute atomically with the true and false
        filters, which may lead to inconsistent or unexpected results.

        Additionally, executing a :class:`ConditionalRowFilter` has poor
        performance on the server, especially when ``false_filter`` is set.

    :type base_filter: :class:`RowFilter`
    :param base_filter: The filter to condition on before executing the
                        true/false filters.

    :type true_filter: :class:`RowFilter`
    :param true_filter: (Optional) The filter to execute if there are any cells
                        matching ``base_filter``. If not provided, no results
                        will be returned in the true case.

    :type false_filter: :class:`RowFilter`
    :param false_filter: (Optional) The filter to execute if there are no cells
                         matching ``base_filter``. If not provided, no results
                         will be returned in the false case.
    """

    def __init__(self, base_filter, true_filter=None, false_filter=None):
        self.base_filter = base_filter
        self.true_filter = true_filter
        self.false_filter = false_filter

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.base_filter == self.base_filter and
                other.true_filter == self.true_filter and
                other.false_filter == self.false_filter)

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        condition_kwargs = {'predicate_filter': self.base_filter.to_pb()}
        if self.true_filter is not None:
            condition_kwargs['true_filter'] = self.true_filter.to_pb()
        if self.false_filter is not None:
            condition_kwargs['false_filter'] = self.false_filter.to_pb()
        condition = data_pb2.RowFilter.Condition(**condition_kwargs)
        return data_pb2.RowFilter(condition=condition)


def _parse_rmw_row_response(row_response):
    """Parses the response to a ``ReadModifyWriteRow`` request.

    :type row_response: :class:`.data_pb2.Row`
    :param row_response: The response row (with only modified cells) from a
                         ``ReadModifyWriteRow`` request.

    :rtype: dict
    :returns: The new contents of all modified cells. Returned as a
              dictionary of column families, each of which holds a
              dictionary of columns. Each column contains a list of cells
              modified. Each cell is represented with a two-tuple with the
              value (in bytes) and the timestamp for the cell. For example:

              .. code:: python

                  {
                      u'col-fam-id': {
                          b'col-name1': [
                              (b'cell-val', datetime.datetime(...)),
                              (b'cell-val-newer', datetime.datetime(...)),
                          ],
                          b'col-name2': [
                              (b'altcol-cell-val', datetime.datetime(...)),
                          ],
                      },
                      u'col-fam-id2': {
                          b'col-name3-but-other-fam': [
                              (b'foo', datetime.datetime(...)),
                          ],
                      },
                  }
    """
    result = {}
    for column_family in row_response.families:
        column_family_id, curr_family = _parse_family_pb(column_family)
        result[column_family_id] = curr_family
    return result


def _parse_family_pb(family_pb):
    """Parses a Family protobuf into a dictionary.

    :type family_pb: :class:`._generated.bigtable_data_pb2.Family`
    :param family_pb: A protobuf

    :rtype: tuple
    :returns: A string and dictionary. The string is the name of the
              column family and the dictionary has column names (within the
              family) as keys and cell lists as values. Each cell is
              represented with a two-tuple with the value (in bytes) and the
              timestamp for the cell. For example:

              .. code:: python

                  {
                      b'col-name1': [
                          (b'cell-val', datetime.datetime(...)),
                          (b'cell-val-newer', datetime.datetime(...)),
                      ],
                      b'col-name2': [
                          (b'altcol-cell-val', datetime.datetime(...)),
                      ],
                  }
    """
    result = {}
    for column in family_pb.columns:
        result[column.qualifier] = cells = []
        for cell in column.cells:
            val_pair = (
                cell.value,
                _datetime_from_microseconds(cell.timestamp_micros),
            )
            cells.append(val_pair)

    return family_pb.name, result
