# Copyright 2016 Google Inc. All rights reserved.
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

"""Google Cloud Bigtable HappyBase table module."""


import struct
import warnings

import six

from gcloud._helpers import _datetime_from_microseconds
from gcloud._helpers import _microseconds_from_datetime
from gcloud._helpers import _to_bytes
from gcloud._helpers import _total_seconds
from gcloud.bigtable.column_family import GCRuleIntersection
from gcloud.bigtable.column_family import MaxAgeGCRule
from gcloud.bigtable.column_family import MaxVersionsGCRule
from gcloud.bigtable.happybase.batch import _get_column_pairs
from gcloud.bigtable.happybase.batch import _WAL_SENTINEL
from gcloud.bigtable.happybase.batch import Batch
from gcloud.bigtable.row_filters import CellsColumnLimitFilter
from gcloud.bigtable.row_filters import ColumnQualifierRegexFilter
from gcloud.bigtable.row_filters import FamilyNameRegexFilter
from gcloud.bigtable.row_filters import RowFilterChain
from gcloud.bigtable.row_filters import RowFilterUnion
from gcloud.bigtable.row_filters import RowKeyRegexFilter
from gcloud.bigtable.row_filters import TimestampRange
from gcloud.bigtable.row_filters import TimestampRangeFilter
from gcloud.bigtable.table import Table as _LowLevelTable


_WARN = warnings.warn
_PACK_I64 = struct.Struct('>q').pack
_UNPACK_I64 = struct.Struct('>q').unpack
_SIMPLE_GC_RULES = (MaxAgeGCRule, MaxVersionsGCRule)


def make_row(cell_map, include_timestamp):
    """Make a row dict for a Thrift cell mapping.

    .. warning::

        This method is only provided for HappyBase compatibility, but does not
        actually work.

    :type cell_map: dict
    :param cell_map: Dictionary with ``fam:col`` strings as keys and ``TCell``
                     instances as values.

    :type include_timestamp: bool
    :param include_timestamp: Flag to indicate if cell timestamps should be
                              included with the output.

    :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
             always
    """
    raise NotImplementedError('The Cloud Bigtable API output is not the same '
                              'as the output from the Thrift server, so this '
                              'helper can not be implemented.', 'Called with',
                              cell_map, include_timestamp)


def make_ordered_row(sorted_columns, include_timestamp):
    """Make a row dict for sorted Thrift column results from scans.

    .. warning::

        This method is only provided for HappyBase compatibility, but does not
        actually work.

    :type sorted_columns: list
    :param sorted_columns: List of ``TColumn`` instances from Thrift.

    :type include_timestamp: bool
    :param include_timestamp: Flag to indicate if cell timestamps should be
                              included with the output.

    :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
             always
    """
    raise NotImplementedError('The Cloud Bigtable API output is not the same '
                              'as the output from the Thrift server, so this '
                              'helper can not be implemented.', 'Called with',
                              sorted_columns, include_timestamp)


class Table(object):
    """Representation of Cloud Bigtable table.

    Used for adding data and

    :type name: str
    :param name: The name of the table.

    :type connection: :class:`Connection <.happybase.connection.Connection>`
    :param connection: The connection which has access to the table.
    """

    def __init__(self, name, connection):
        self.name = name
        # This remains as legacy for HappyBase, but only the instance
        # from the connection is needed.
        self.connection = connection
        self._low_level_table = None
        if self.connection is not None:
            self._low_level_table = _LowLevelTable(self.name,
                                                   self.connection._instance)

    def __repr__(self):
        return '<table.Table name=%r>' % (self.name,)

    def families(self):
        """Retrieve the column families for this table.

        :rtype: dict
        :returns: Mapping from column family name to garbage collection rule
                  for a column family.
        """
        column_family_map = self._low_level_table.list_column_families()
        result = {}
        for col_fam, col_fam_obj in six.iteritems(column_family_map):
            result[col_fam] = _gc_rule_to_dict(col_fam_obj.gc_rule)
        return result

    def regions(self):
        """Retrieve the regions for this table.

        .. warning::

            Cloud Bigtable does not give information about how a table is laid
            out in memory, so this method does not work. It is
            provided simply for compatibility.

        :raises: :class:`NotImplementedError <exceptions.NotImplementedError>`
                 always
        """
        raise NotImplementedError('The Cloud Bigtable API does not have a '
                                  'concept of splitting a table into regions.')

    def row(self, row, columns=None, timestamp=None, include_timestamp=False):
        """Retrieve a single row of data.

        Returns the latest cells in each column (or all columns if ``columns``
        is not specified). If a ``timestamp`` is set, then **latest** becomes
        **latest** up until ``timestamp``.

        :type row: str
        :param row: Row key for the row we are reading from.

        :type columns: list
        :param columns: (Optional) Iterable containing column names (as
                        strings). Each column name can be either

                          * an entire column family: ``fam`` or ``fam:``
                          * a single column: ``fam:col``

        :type timestamp: int
        :param timestamp: (Optional) Timestamp (in milliseconds since the
                          epoch). If specified, only cells returned before the
                          the timestamp will be returned.

        :type include_timestamp: bool
        :param include_timestamp: Flag to indicate if cell timestamps should be
                                  included with the output.

        :rtype: dict
        :returns: Dictionary containing all the latest column values in
                  the row.
        """
        filters = []
        if columns is not None:
            filters.append(_columns_filter_helper(columns))
        # versions == 1 since we only want the latest.
        filter_ = _filter_chain_helper(versions=1, timestamp=timestamp,
                                       filters=filters)

        partial_row_data = self._low_level_table.read_row(
            row, filter_=filter_)
        if partial_row_data is None:
            return {}

        return _partial_row_to_dict(partial_row_data,
                                    include_timestamp=include_timestamp)

    def rows(self, rows, columns=None, timestamp=None,
             include_timestamp=False):
        """Retrieve multiple rows of data.

        All optional arguments behave the same in this method as they do in
        :meth:`row`.

        :type rows: list
        :param rows: Iterable of the row keys for the rows we are reading from.

        :type columns: list
        :param columns: (Optional) Iterable containing column names (as
                        strings). Each column name can be either

                          * an entire column family: ``fam`` or ``fam:``
                          * a single column: ``fam:col``

        :type timestamp: int
        :param timestamp: (Optional) Timestamp (in milliseconds since the
                          epoch). If specified, only cells returned before (or
                          at) the timestamp will be returned.

        :type include_timestamp: bool
        :param include_timestamp: Flag to indicate if cell timestamps should be
                                  included with the output.

        :rtype: list
        :returns: A list of pairs, where the first is the row key and the
                  second is a dictionary with the filtered values returned.
        """
        if not rows:
            # Avoid round-trip if the result is empty anyway
            return []

        filters = []
        if columns is not None:
            filters.append(_columns_filter_helper(columns))
        filters.append(_row_keys_filter_helper(rows))
        # versions == 1 since we only want the latest.
        filter_ = _filter_chain_helper(versions=1, timestamp=timestamp,
                                       filters=filters)

        partial_rows_data = self._low_level_table.read_rows(filter_=filter_)
        # NOTE: We could use max_loops = 1000 or some similar value to ensure
        #       that the stream isn't open too long.
        partial_rows_data.consume_all()

        result = []
        for row_key in rows:
            if row_key not in partial_rows_data.rows:
                continue
            curr_row_data = partial_rows_data.rows[row_key]
            curr_row_dict = _partial_row_to_dict(
                curr_row_data, include_timestamp=include_timestamp)
            result.append((row_key, curr_row_dict))

        return result

    def cells(self, row, column, versions=None, timestamp=None,
              include_timestamp=False):
        """Retrieve multiple versions of a single cell from the table.

        :type row: str
        :param row: Row key for the row we are reading from.

        :type column: str
        :param column: Column we are reading from; of the form ``fam:col``.

        :type versions: int
        :param versions: (Optional) The maximum number of cells to return. If
                         not set, returns all cells found.

        :type timestamp: int
        :param timestamp: (Optional) Timestamp (in milliseconds since the
                          epoch). If specified, only cells returned before (or
                          at) the timestamp will be returned.

        :type include_timestamp: bool
        :param include_timestamp: Flag to indicate if cell timestamps should be
                                  included with the output.

        :rtype: list
        :returns: List of values in the cell (with timestamps if
                  ``include_timestamp`` is :data:`True`).
        """
        filter_ = _filter_chain_helper(column=column, versions=versions,
                                       timestamp=timestamp)
        partial_row_data = self._low_level_table.read_row(row, filter_=filter_)
        if partial_row_data is None:
            return []
        else:
            cells = partial_row_data._cells
            # We know that `_filter_chain_helper` has already verified that
            # column will split as such.
            column_family_id, column_qualifier = column.split(':')
            # NOTE: We expect the only key in `cells` is `column_family_id`
            #       and the only key `cells[column_family_id]` is
            #       `column_qualifier`. But we don't check that this is true.
            curr_cells = cells[column_family_id][column_qualifier]
            return _cells_to_pairs(
                curr_cells, include_timestamp=include_timestamp)

    def scan(self, row_start=None, row_stop=None, row_prefix=None,
             columns=None, timestamp=None,
             include_timestamp=False, limit=None, **kwargs):
        """Create a scanner for data in this table.

        This method returns a generator that can be used for looping over the
        matching rows.

        If ``row_prefix`` is specified, only rows with row keys matching the
        prefix will be returned. If given, ``row_start`` and ``row_stop``
        cannot be used.

        .. note::

            Both ``row_start`` and ``row_stop`` can be :data:`None` to specify
            the start and the end of the table respectively. If both are
            omitted, a full table scan is done. Note that this usually results
            in severe performance problems.

        The keyword argument ``filter`` is also supported (beyond column and
        row range filters supported here). HappyBase / HBase users will have
        used this as an HBase filter string. (See the `Thrift docs`_ for more
        details on those filters.) However, Google Cloud Bigtable doesn't
        support those filter strings so a
        :class:`~gcloud.bigtable.row.RowFilter` should be used instead.

        .. _Thrift docs: http://hbase.apache.org/0.94/book/thrift.html

        The arguments ``batch_size``, ``scan_batching`` and ``sorted_columns``
        are allowed (as keyword arguments) for compatibility with
        HappyBase. However, they will not be used in any way, and will cause a
        warning if passed. (The ``batch_size`` determines the number of
        results to retrieve per request. The HBase scanner defaults to reading
        one record at a time, so this argument allows HappyBase to increase
        that number. However, the Cloud Bigtable API uses HTTP/2 streaming so
        there is no concept of a batched scan. The ``sorted_columns`` flag
        tells HBase to return columns in order, but Cloud Bigtable doesn't
        have this feature.)

        :type row_start: str
        :param row_start: (Optional) Row key where the scanner should start
                          (includes ``row_start``). If not specified, reads
                          from the first key. If the table does not contain
                          ``row_start``, it will start from the next key after
                          it that **is** contained in the table.

        :type row_stop: str
        :param row_stop: (Optional) Row key where the scanner should stop
                         (excludes ``row_stop``). If not specified, reads
                         until the last key. The table does not have to contain
                         ``row_stop``.

        :type row_prefix: str
        :param row_prefix: (Optional) Prefix to match row keys.

        :type columns: list
        :param columns: (Optional) Iterable containing column names (as
                        strings). Each column name can be either

                          * an entire column family: ``fam`` or ``fam:``
                          * a single column: ``fam:col``

        :type timestamp: int
        :param timestamp: (Optional) Timestamp (in milliseconds since the
                          epoch). If specified, only cells returned before (or
                          at) the timestamp will be returned.

        :type include_timestamp: bool
        :param include_timestamp: Flag to indicate if cell timestamps should be
                                  included with the output.

        :type limit: int
        :param limit: (Optional) Maximum number of rows to return.

        :type kwargs: dict
        :param kwargs: Remaining keyword arguments. Provided for HappyBase
                       compatibility.

        :raises: If ``limit`` is set but non-positive, or if ``row_prefix`` is
                 used with row start/stop,
                 :class:`TypeError <exceptions.TypeError>` if a string
                 ``filter`` is used.
        """
        row_start, row_stop, filter_chain = _scan_filter_helper(
            row_start, row_stop, row_prefix, columns, timestamp, limit, kwargs)

        partial_rows_data = self._low_level_table.read_rows(
            start_key=row_start, end_key=row_stop,
            limit=limit, filter_=filter_chain)

        # Mutable copy of data.
        rows_dict = partial_rows_data.rows
        while True:
            try:
                partial_rows_data.consume_next()
                for row_key in sorted(rows_dict):
                    curr_row_data = rows_dict.pop(row_key)
                    # NOTE: We expect len(rows_dict) == 0, but don't check it.
                    curr_row_dict = _partial_row_to_dict(
                        curr_row_data, include_timestamp=include_timestamp)
                    yield (row_key, curr_row_dict)
            except StopIteration:
                break

    def put(self, row, data, timestamp=None, wal=_WAL_SENTINEL):
        """Insert data into a row in this table.

        .. note::

            This method will send a request with a single "put" mutation.
            In many situations, :meth:`batch` is a more appropriate
            method to manipulate data since it helps combine many mutations
            into a single request.

        :type row: str
        :param row: The row key where the mutation will be "put".

        :type data: dict
        :param data: Dictionary containing the data to be inserted. The keys
                     are columns names (of the form ``fam:col``) and the values
                     are strings (bytes) to be stored in those columns.

        :type timestamp: int
        :param timestamp: (Optional) Timestamp (in milliseconds since the
                          epoch) that the mutation will be applied at.

        :type wal: object
        :param wal: Unused parameter (to be passed to a created batch).
                    Provided for compatibility with HappyBase, but irrelevant
                    for Cloud Bigtable since it does not have a Write Ahead
                    Log.
        """
        with self.batch(timestamp=timestamp, wal=wal) as batch:
            batch.put(row, data)

    def delete(self, row, columns=None, timestamp=None, wal=_WAL_SENTINEL):
        """Delete data from a row in this table.

        This method deletes the entire ``row`` if ``columns`` is not
        specified.

        .. note::

            This method will send a request with a single delete mutation.
            In many situations, :meth:`batch` is a more appropriate
            method to manipulate data since it helps combine many mutations
            into a single request.

        :type row: str
        :param row: The row key where the delete will occur.

        :type columns: list
        :param columns: (Optional) Iterable containing column names (as
                        strings). Each column name can be either

                          * an entire column family: ``fam`` or ``fam:``
                          * a single column: ``fam:col``

        :type timestamp: int
        :param timestamp: (Optional) Timestamp (in milliseconds since the
                          epoch) that the mutation will be applied at.

        :type wal: object
        :param wal: Unused parameter (to be passed to a created batch).
                    Provided for compatibility with HappyBase, but irrelevant
                    for Cloud Bigtable since it does not have a Write Ahead
                    Log.
        """
        with self.batch(timestamp=timestamp, wal=wal) as batch:
            batch.delete(row, columns)

    def batch(self, timestamp=None, batch_size=None, transaction=False,
              wal=_WAL_SENTINEL):
        """Create a new batch operation for this table.

        This method returns a new
        :class:`Batch <.happybase.batch.Batch>` instance that can be
        used for mass data manipulation.

        :type timestamp: int
        :param timestamp: (Optional) Timestamp (in milliseconds since the
                          epoch) that all mutations will be applied at.

        :type batch_size: int
        :param batch_size: (Optional) The maximum number of mutations to allow
                           to accumulate before committing them.

        :type transaction: bool
        :param transaction: Flag indicating if the mutations should be sent
                            transactionally or not. If ``transaction=True`` and
                            an error occurs while a
                            :class:`Batch <.happybase.batch.Batch>` is
                            active, then none of the accumulated mutations will
                            be committed. If ``batch_size`` is set, the
                            mutation can't be transactional.

        :type wal: object
        :param wal: Unused parameter (to be passed to the created batch).
                    Provided for compatibility with HappyBase, but irrelevant
                    for Cloud Bigtable since it does not have a Write Ahead
                    Log.

        :rtype: :class:`Batch <gcloud.bigtable.happybase.batch.Batch>`
        :returns: A batch bound to this table.
        """
        return Batch(self, timestamp=timestamp, batch_size=batch_size,
                     transaction=transaction, wal=wal)

    def counter_get(self, row, column):
        """Retrieve the current value of a counter column.

        This method retrieves the current value of a counter column. If the
        counter column does not exist, this function initializes it to ``0``.

        .. note::

            Application code should **never** store a counter value directly;
            use the atomic :meth:`counter_inc` and :meth:`counter_dec` methods
            for that.

        :type row: str
        :param row: Row key for the row we are getting a counter from.

        :type column: str
        :param column: Column we are ``get``-ing from; of the form ``fam:col``.

        :rtype: int
        :returns: Counter value (after initializing / incrementing by 0).
        """
        # Don't query directly, but increment with value=0 so that the counter
        # is correctly initialized if didn't exist yet.
        return self.counter_inc(row, column, value=0)

    def counter_set(self, row, column, value=0):
        """Set a counter column to a specific value.

        .. note::

            Be careful using this method. It can be useful for setting the
            initial value of a counter, but it defeats the purpose of using
            atomic increment and decrement.

        :type row: str
        :param row: Row key for the row we are setting a counter in.

        :type column: str
        :param column: Column we are setting a value in; of
                       the form ``fam:col``.

        :type value: int
        :param value: Value to set the counter to.
        """
        self.put(row, {column: _PACK_I64(value)})

    def counter_inc(self, row, column, value=1):
        """Atomically increment a counter column.

        This method atomically increments a counter column in ``row``.
        If the counter column does not exist, it is automatically initialized
        to ``0`` before being incremented.

        :type row: str
        :param row: Row key for the row we are incrementing a counter in.

        :type column: str
        :param column: Column we are incrementing a value in; of the
                       form ``fam:col``.

        :type value: int
        :param value: Amount to increment the counter by. (If negative,
                      this is equivalent to decrement.)

        :rtype: int
        :returns: Counter value after incrementing.
        """
        row = self._low_level_table.row(row, append=True)
        if isinstance(column, six.binary_type):
            column = column.decode('utf-8')
        column_family_id, column_qualifier = column.split(':')
        row.increment_cell_value(column_family_id, column_qualifier, value)
        # See AppendRow.commit() will return a dictionary:
        # {
        #     u'col-fam-id': {
        #         b'col-name1': [
        #             (b'cell-val', datetime.datetime(...)),
        #             ...
        #         ],
        #         ...
        #     },
        # }
        modified_cells = row.commit()
        # Get the cells in the modified column,
        column_cells = modified_cells[column_family_id][column_qualifier]
        # Make sure there is exactly one cell in the column.
        if len(column_cells) != 1:
            raise ValueError('Expected server to return one modified cell.')
        column_cell = column_cells[0]
        # Get the bytes value from the column and convert it to an integer.
        bytes_value = column_cell[0]
        int_value, = _UNPACK_I64(bytes_value)
        return int_value

    def counter_dec(self, row, column, value=1):
        """Atomically decrement a counter column.

        This method atomically decrements a counter column in ``row``.
        If the counter column does not exist, it is automatically initialized
        to ``0`` before being decremented.

        :type row: str
        :param row: Row key for the row we are decrementing a counter in.

        :type column: str
        :param column: Column we are decrementing a value in; of the
                       form ``fam:col``.

        :type value: int
        :param value: Amount to decrement the counter by. (If negative,
                      this is equivalent to increment.)

        :rtype: int
        :returns: Counter value after decrementing.
        """
        return self.counter_inc(row, column, -value)


def _gc_rule_to_dict(gc_rule):
    """Converts garbage collection rule to dictionary if possible.

    This is in place to support dictionary values as was done
    in HappyBase, which has somewhat different garbage collection rule
    settings for column families.

    Only does this if the garbage collection rule is:

    * :class:`gcloud.bigtable.column_family.MaxAgeGCRule`
    * :class:`gcloud.bigtable.column_family.MaxVersionsGCRule`
    * Composite :class:`gcloud.bigtable.column_family.GCRuleIntersection`
      with two rules, one each of type
      :class:`gcloud.bigtable.column_family.MaxAgeGCRule` and
      :class:`gcloud.bigtable.column_family.MaxVersionsGCRule`

    Otherwise, just returns the input without change.

    :type gc_rule: :data:`NoneType <types.NoneType>`,
                   :class:`.GarbageCollectionRule`
    :param gc_rule: A garbage collection rule to convert to a dictionary
                    (if possible).

    :rtype: dict or
            :class:`gcloud.bigtable.column_family.GarbageCollectionRule`
    :returns: The converted garbage collection rule.
    """
    result = gc_rule
    if gc_rule is None:
        result = {}
    elif isinstance(gc_rule, MaxAgeGCRule):
        result = {'time_to_live': _total_seconds(gc_rule.max_age)}
    elif isinstance(gc_rule, MaxVersionsGCRule):
        result = {'max_versions': gc_rule.max_num_versions}
    elif isinstance(gc_rule, GCRuleIntersection):
        if len(gc_rule.rules) == 2:
            rule1, rule2 = gc_rule.rules
            if (isinstance(rule1, _SIMPLE_GC_RULES) and
                    isinstance(rule2, _SIMPLE_GC_RULES)):
                rule1 = _gc_rule_to_dict(rule1)
                rule2 = _gc_rule_to_dict(rule2)
                key1, = rule1.keys()
                key2, = rule2.keys()
                if key1 != key2:
                    result = {key1: rule1[key1], key2: rule2[key2]}
    return result


def _next_char(str_val, index):
    """Gets the next character based on a position in a string.

    :type str_val: str
    :param str_val: A string containing the character to update.

    :type index: int
    :param index: An integer index in ``str_val``.

    :rtype: str
    :returns: The next character after the character at ``index``
              in ``str_val``.
    """
    ord_val = six.indexbytes(str_val, index)
    return _to_bytes(chr(ord_val + 1), encoding='latin-1')


def _string_successor(str_val):
    """Increment and truncate a byte string.

    Determines shortest string that sorts after the given string when
    compared using regular string comparison semantics.

    Modeled after implementation in ``gcloud-golang``.

    Increments the last byte that is smaller than ``0xFF``, and
    drops everything after it. If the string only contains ``0xFF`` bytes,
    ``''`` is returned.

    :type str_val: str
    :param str_val: String to increment.

    :rtype: str
    :returns: The next string in lexical order after ``str_val``.
    """
    str_val = _to_bytes(str_val, encoding='latin-1')
    if str_val == b'':
        return str_val

    index = len(str_val) - 1
    while index >= 0:
        if six.indexbytes(str_val, index) != 0xff:
            break
        index -= 1

    if index == -1:
        return b''

    return str_val[:index] + _next_char(str_val, index)


def _convert_to_time_range(timestamp=None):
    """Create a timestamp range from an HBase / HappyBase timestamp.

    HBase uses timestamp as an argument to specify an exclusive end
    deadline. Cloud Bigtable also uses exclusive end times, so
    the behavior matches.

    :type timestamp: int
    :param timestamp: (Optional) Timestamp (in milliseconds since the
                      epoch). Intended to be used as the end of an HBase
                      time range, which is exclusive.

    :rtype: :class:`gcloud.bigtable.row.TimestampRange`,
            :data:`NoneType <types.NoneType>`
    :returns: The timestamp range corresponding to the passed in
              ``timestamp``.
    """
    if timestamp is None:
        return None

    next_timestamp = _datetime_from_microseconds(1000 * timestamp)
    return TimestampRange(end=next_timestamp)


def _cells_to_pairs(cells, include_timestamp=False):
    """Converts list of cells to HappyBase format.

    For example::

      >>> import datetime
      >>> from gcloud.bigtable.row_data import Cell
      >>> cell1 = Cell(b'val1', datetime.datetime.utcnow())
      >>> cell2 = Cell(b'val2', datetime.datetime.utcnow())
      >>> _cells_to_pairs([cell1, cell2])
      [b'val1', b'val2']
      >>> _cells_to_pairs([cell1, cell2], include_timestamp=True)
      [(b'val1', 1456361486255), (b'val2', 1456361491927)]

    :type cells: list
    :param cells: List of :class:`gcloud.bigtable.row_data.Cell` returned
                  from a read request.

    :type include_timestamp: bool
    :param include_timestamp: Flag to indicate if cell timestamps should be
                              included with the output.

    :rtype: list
    :returns: List of values in the cell. If ``include_timestamp=True``, each
              value will be a pair, with the first part the bytes value in
              the cell and the second part the number of milliseconds in the
              timestamp on the cell.
    """
    result = []
    for cell in cells:
        if include_timestamp:
            ts_millis = _microseconds_from_datetime(cell.timestamp) // 1000
            result.append((cell.value, ts_millis))
        else:
            result.append(cell.value)
    return result


def _partial_row_to_dict(partial_row_data, include_timestamp=False):
    """Convert a low-level row data object to a dictionary.

    Assumes only the latest value in each row is needed. This assumption
    is due to the fact that this method is used by callers which use
    a ``CellsColumnLimitFilter(1)`` filter.

    For example::

      >>> import datetime
      >>> from gcloud.bigtable.row_data import Cell, PartialRowData
      >>> cell1 = Cell(b'val1', datetime.datetime.utcnow())
      >>> cell2 = Cell(b'val2', datetime.datetime.utcnow())
      >>> row_data = PartialRowData(b'row-key')
      >>> _partial_row_to_dict(row_data)
      {}
      >>> row_data._cells[u'fam1'] = {b'col1': [cell1], b'col2': [cell2]}
      >>> _partial_row_to_dict(row_data)
      {b'fam1:col2': b'val2', b'fam1:col1': b'val1'}
      >>> _partial_row_to_dict(row_data, include_timestamp=True)
      {b'fam1:col2': (b'val2', 1456361724480),
       b'fam1:col1': (b'val1', 1456361721135)}

    :type partial_row_data: :class:`.row_data.PartialRowData`
    :param partial_row_data: Row data consumed from a stream.

    :type include_timestamp: bool
    :param include_timestamp: Flag to indicate if cell timestamps should be
                              included with the output.

    :rtype: dict
    :returns: The row data converted to a dictionary.
    """
    result = {}
    for column, cells in six.iteritems(partial_row_data.to_dict()):
        cell_vals = _cells_to_pairs(cells,
                                    include_timestamp=include_timestamp)
        # NOTE: We assume there is exactly 1 version since we used that in
        #       our filter, but we don't check this.
        result[column] = cell_vals[0]
    return result


def _filter_chain_helper(column=None, versions=None, timestamp=None,
                         filters=None):
    """Create filter chain to limit a results set.

    :type column: str
    :param column: (Optional) The column (``fam:col``) to be selected
                   with the filter.

    :type versions: int
    :param versions: (Optional) The maximum number of cells to return.

    :type timestamp: int
    :param timestamp: (Optional) Timestamp (in milliseconds since the
                      epoch). If specified, only cells returned before (or
                      at) the timestamp will be matched.

    :type filters: list
    :param filters: (Optional) List of existing filters to be extended.

    :rtype: :class:`RowFilter <gcloud.bigtable.row.RowFilter>`
    :returns: The chained filter created, or just a single filter if only
              one was needed.
    :raises: :class:`ValueError <exceptions.ValueError>` if there are no
             filters to chain.
    """
    if filters is None:
        filters = []

    if column is not None:
        if isinstance(column, six.binary_type):
            column = column.decode('utf-8')
        column_family_id, column_qualifier = column.split(':')
        fam_filter = FamilyNameRegexFilter(column_family_id)
        qual_filter = ColumnQualifierRegexFilter(column_qualifier)
        filters.extend([fam_filter, qual_filter])
    if versions is not None:
        filters.append(CellsColumnLimitFilter(versions))
    time_range = _convert_to_time_range(timestamp=timestamp)
    if time_range is not None:
        filters.append(TimestampRangeFilter(time_range))

    num_filters = len(filters)
    if num_filters == 0:
        raise ValueError('Must have at least one filter.')
    elif num_filters == 1:
        return filters[0]
    else:
        return RowFilterChain(filters=filters)


def _scan_filter_helper(row_start, row_stop, row_prefix, columns,
                        timestamp, limit, kwargs):
    """Helper for :meth:`scan`:  build up a filter chain."""
    filter_ = kwargs.pop('filter', None)
    legacy_args = []
    for kw_name in ('batch_size', 'scan_batching', 'sorted_columns'):
        if kw_name in kwargs:
            legacy_args.append(kw_name)
            kwargs.pop(kw_name)
    if legacy_args:
        legacy_args = ', '.join(legacy_args)
        message = ('The HappyBase legacy arguments %s were used. These '
                   'arguments are unused by gcloud.' % (legacy_args,))
        _WARN(message)
    if kwargs:
        raise TypeError('Received unexpected arguments', kwargs.keys())

    if limit is not None and limit < 1:
        raise ValueError('limit must be positive')
    if row_prefix is not None:
        if row_start is not None or row_stop is not None:
            raise ValueError('row_prefix cannot be combined with '
                             'row_start or row_stop')
        row_start = row_prefix
        row_stop = _string_successor(row_prefix)

    filters = []
    if isinstance(filter_, six.string_types):
        raise TypeError('Specifying filters as a string is not supported '
                        'by Cloud Bigtable. Use a '
                        'gcloud.bigtable.row.RowFilter instead.')
    elif filter_ is not None:
        filters.append(filter_)

    if columns is not None:
        filters.append(_columns_filter_helper(columns))

    # versions == 1 since we only want the latest.
    filter_ = _filter_chain_helper(versions=1, timestamp=timestamp,
                                   filters=filters)
    return row_start, row_stop, filter_


def _columns_filter_helper(columns):
    """Creates a union filter for a list of columns.

    :type columns: list
    :param columns: Iterable containing column names (as strings). Each column
                    name can be either

                      * an entire column family: ``fam`` or ``fam:``
                      * a single column: ``fam:col``

    :rtype: :class:`RowFilter <gcloud.bigtable.row.RowFilter>`
    :returns: The union filter created containing all of the matched columns.
    :raises: :class:`ValueError <exceptions.ValueError>` if there are no
             filters to union.
    """
    filters = []
    for column_family_id, column_qualifier in _get_column_pairs(columns):
        fam_filter = FamilyNameRegexFilter(column_family_id)
        if column_qualifier is not None:
            qual_filter = ColumnQualifierRegexFilter(column_qualifier)
            combined_filter = RowFilterChain(
                filters=[fam_filter, qual_filter])
            filters.append(combined_filter)
        else:
            filters.append(fam_filter)

    num_filters = len(filters)
    if num_filters == 0:
        raise ValueError('Must have at least one filter.')
    elif num_filters == 1:
        return filters[0]
    else:
        return RowFilterUnion(filters=filters)


def _row_keys_filter_helper(row_keys):
    """Creates a union filter for a list of rows.

    :type row_keys: list
    :param row_keys: Iterable containing row keys (as strings).

    :rtype: :class:`RowFilter <gcloud.bigtable.row.RowFilter>`
    :returns: The union filter created containing all of the row keys.
    :raises: :class:`ValueError <exceptions.ValueError>` if there are no
             filters to union.
    """
    filters = []
    for row_key in row_keys:
        filters.append(RowKeyRegexFilter(row_key))

    num_filters = len(filters)
    if num_filters == 0:
        raise ValueError('Must have at least one filter.')
    elif num_filters == 1:
        return filters[0]
    else:
        return RowFilterUnion(filters=filters)
