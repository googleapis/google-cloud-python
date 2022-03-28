# Copyright 2016 Google LLC
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

"""Container for Google Cloud Bigtable Cells and Streaming Row Contents."""


import copy

import grpc  # type: ignore

from google.api_core import exceptions
from google.api_core import retry
from google.cloud._helpers import _datetime_from_microseconds  # type: ignore
from google.cloud._helpers import _to_bytes  # type: ignore
from google.cloud.bigtable_v2.types import bigtable as data_messages_v2_pb2
from google.cloud.bigtable_v2.types import data as data_v2_pb2

_MISSING_COLUMN_FAMILY = "Column family {} is not among the cells stored in this row."
_MISSING_COLUMN = (
    "Column {} is not among the cells stored in this row in the " "column family {}."
)
_MISSING_INDEX = (
    "Index {!r} is not valid for the cells stored in this row for column {} "
    "in the column family {}. There are {} such cells."
)


class Cell(object):
    """Representation of a Google Cloud Bigtable Cell.

    :type value: bytes
    :param value: The value stored in the cell.

    :type timestamp_micros: int
    :param timestamp_micros: The timestamp_micros when the cell was stored.

    :type labels: list
    :param labels: (Optional) List of strings. Labels applied to the cell.
    """

    def __init__(self, value, timestamp_micros, labels=None):
        self.value = value
        self.timestamp_micros = timestamp_micros
        self.labels = list(labels) if labels is not None else []

    @classmethod
    def from_pb(cls, cell_pb):
        """Create a new cell from a Cell protobuf.

        :type cell_pb: :class:`._generated.data_pb2.Cell`
        :param cell_pb: The protobuf to convert.

        :rtype: :class:`Cell`
        :returns: The cell corresponding to the protobuf.
        """
        if cell_pb.labels:
            return cls(cell_pb.value, cell_pb.timestamp_micros, labels=cell_pb.labels)
        else:
            return cls(cell_pb.value, cell_pb.timestamp_micros)

    @property
    def timestamp(self):
        return _datetime_from_microseconds(self.timestamp_micros)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            other.value == self.value
            and other.timestamp_micros == self.timestamp_micros
            and other.labels == self.labels
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "<{name} value={value!r} timestamp={timestamp}>".format(
            name=self.__class__.__name__, value=self.value, timestamp=self.timestamp
        )


class PartialCellData(object):
    """Representation of partial cell in a Google Cloud Bigtable Table.

    These are expected to be updated directly from a
    :class:`._generated.bigtable_service_messages_pb2.ReadRowsResponse`

    :type row_key: bytes
    :param row_key: The key for the row holding the (partial) cell.

    :type family_name: str
    :param family_name: The family name of the (partial) cell.

    :type qualifier: bytes
    :param qualifier: The column qualifier of the (partial) cell.

    :type timestamp_micros: int
    :param timestamp_micros: The timestamp (in microsecods) of the
                             (partial) cell.

    :type labels: list of str
    :param labels: labels assigned to the (partial) cell

    :type value: bytes
    :param value: The (accumulated) value of the (partial) cell.
    """

    def __init__(
        self, row_key, family_name, qualifier, timestamp_micros, labels=(), value=b""
    ):
        self.row_key = row_key
        self.family_name = family_name
        self.qualifier = qualifier
        self.timestamp_micros = timestamp_micros
        self.labels = labels
        self.value = value

    def append_value(self, value):
        """Append bytes from a new chunk to value.

        :type value: bytes
        :param value: bytes to append
        """
        self.value += value


class PartialRowData(object):
    """Representation of partial row in a Google Cloud Bigtable Table.

    These are expected to be updated directly from a
    :class:`._generated.bigtable_service_messages_pb2.ReadRowsResponse`

    :type row_key: bytes
    :param row_key: The key for the row holding the (partial) data.
    """

    def __init__(self, row_key):
        self._row_key = row_key
        self._cells = {}

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other._row_key == self._row_key and other._cells == self._cells

    def __ne__(self, other):
        return not self == other

    def to_dict(self):
        """Convert the cells to a dictionary.

        This is intended to be used with HappyBase, so the column family and
        column qualiers are combined (with ``:``).

        :rtype: dict
        :returns: Dictionary containing all the data in the cells of this row.
        """
        result = {}
        for column_family_id, columns in self._cells.items():
            for column_qual, cells in columns.items():
                key = _to_bytes(column_family_id) + b":" + _to_bytes(column_qual)
                result[key] = cells
        return result

    @property
    def cells(self):
        """Property returning all the cells accumulated on this partial row.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_api_row_data_cells]
            :end-before: [END bigtable_api_row_data_cells]
            :dedent: 4

        :rtype: dict
        :returns: Dictionary of the :class:`Cell` objects accumulated. This
                  dictionary has two-levels of keys (first for column families
                  and second for column names/qualifiers within a family). For
                  a given column, a list of :class:`Cell` objects is stored.
        """
        return self._cells

    @property
    def row_key(self):
        """Getter for the current (partial) row's key.

        :rtype: bytes
        :returns: The current (partial) row's key.
        """
        return self._row_key

    def find_cells(self, column_family_id, column):
        """Get a time series of cells stored on this instance.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_api_row_find_cells]
            :end-before: [END bigtable_api_row_find_cells]
            :dedent: 4

        Args:
            column_family_id (str): The ID of the column family. Must be of the
                form ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.
            column (bytes): The column within the column family where the cells
                are located.

        Returns:
            List[~google.cloud.bigtable.row_data.Cell]: The cells stored in the
            specified column.

        Raises:
            KeyError: If ``column_family_id`` is not among the cells stored
                in this row.
            KeyError: If ``column`` is not among the cells stored in this row
                for the given ``column_family_id``.
        """
        try:
            column_family = self._cells[column_family_id]
        except KeyError:
            raise KeyError(_MISSING_COLUMN_FAMILY.format(column_family_id))

        try:
            cells = column_family[column]
        except KeyError:
            raise KeyError(_MISSING_COLUMN.format(column, column_family_id))

        return cells

    def cell_value(self, column_family_id, column, index=0):
        """Get a single cell value stored on this instance.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_api_row_cell_value]
            :end-before: [END bigtable_api_row_cell_value]
            :dedent: 4

        Args:
            column_family_id (str): The ID of the column family. Must be of the
                form ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.
            column (bytes): The column within the column family where the cell
                is located.
            index (Optional[int]): The offset within the series of values. If
                not specified, will return the first cell.

        Returns:
            ~google.cloud.bigtable.row_data.Cell value: The cell value stored
            in the specified column and specified index.

        Raises:
            KeyError: If ``column_family_id`` is not among the cells stored
                in this row.
            KeyError: If ``column`` is not among the cells stored in this row
                for the given ``column_family_id``.
            IndexError: If ``index`` cannot be found within the cells stored
                in this row for the given ``column_family_id``, ``column``
                pair.
        """
        cells = self.find_cells(column_family_id, column)

        try:
            cell = cells[index]
        except (TypeError, IndexError):
            num_cells = len(cells)
            msg = _MISSING_INDEX.format(index, column, column_family_id, num_cells)
            raise IndexError(msg)

        return cell.value

    def cell_values(self, column_family_id, column, max_count=None):
        """Get a time series of cells stored on this instance.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_api_row_cell_values]
            :end-before: [END bigtable_api_row_cell_values]
            :dedent: 4

        Args:
            column_family_id (str): The ID of the column family. Must be of the
                form ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.
            column (bytes): The column within the column family where the cells
                are located.
            max_count (int): The maximum number of cells to use.

        Returns:
            A generator which provides: cell.value, cell.timestamp_micros
                for each cell in the list of cells

        Raises:
            KeyError: If ``column_family_id`` is not among the cells stored
                in this row.
            KeyError: If ``column`` is not among the cells stored in this row
                for the given ``column_family_id``.
        """
        cells = self.find_cells(column_family_id, column)
        if max_count is None:
            max_count = len(cells)

        for index, cell in enumerate(cells):
            if index == max_count:
                break

            yield cell.value, cell.timestamp_micros


class InvalidReadRowsResponse(RuntimeError):
    """Exception raised to to invalid response data from back-end."""


class InvalidChunk(RuntimeError):
    """Exception raised to to invalid chunk data from back-end."""


def _retry_read_rows_exception(exc):
    if isinstance(exc, grpc.RpcError):
        exc = exceptions.from_grpc_error(exc)
    return isinstance(exc, (exceptions.ServiceUnavailable, exceptions.DeadlineExceeded))


DEFAULT_RETRY_READ_ROWS = retry.Retry(
    predicate=_retry_read_rows_exception,
    initial=1.0,
    maximum=15.0,
    multiplier=2.0,
    deadline=60.0,  # 60 seconds
)
"""The default retry strategy to be used on retry-able errors.

Used by
:meth:`~google.cloud.bigtable.row_data.PartialRowsData._read_next_response`.
"""


class PartialRowsData(object):
    """Convenience wrapper for consuming a ``ReadRows`` streaming response.

    :type read_method: :class:`client._table_data_client.read_rows`
    :param read_method: ``ReadRows`` method.

    :type request: :class:`data_messages_v2_pb2.ReadRowsRequest`
    :param request: The ``ReadRowsRequest`` message used to create a
                    ReadRowsResponse iterator. If the iterator fails, a new
                    iterator is created, allowing the scan to continue from
                    the point just beyond the last successfully read row,
                    identified by self.last_scanned_row_key. The retry happens
                    inside of the Retry class, using a predicate for the
                    expected exceptions during iteration.

    :type retry: :class:`~google.api_core.retry.Retry`
    :param retry: (Optional) Retry delay and deadline arguments. To override,
                  the default value :attr:`DEFAULT_RETRY_READ_ROWS` can be
                  used and modified with the
                  :meth:`~google.api_core.retry.Retry.with_delay` method
                  or the
                  :meth:`~google.api_core.retry.Retry.with_deadline` method.
    """

    NEW_ROW = "New row"  # No cells yet complete for row
    ROW_IN_PROGRESS = "Row in progress"  # Some cells complete for row
    CELL_IN_PROGRESS = "Cell in progress"  # Incomplete cell for row

    STATE_NEW_ROW = 1
    STATE_ROW_IN_PROGRESS = 2
    STATE_CELL_IN_PROGRESS = 3

    read_states = {
        STATE_NEW_ROW: NEW_ROW,
        STATE_ROW_IN_PROGRESS: ROW_IN_PROGRESS,
        STATE_CELL_IN_PROGRESS: CELL_IN_PROGRESS,
    }

    def __init__(self, read_method, request, retry=DEFAULT_RETRY_READ_ROWS):
        # Counter for rows returned to the user
        self._counter = 0
        # In-progress row, unset until first response, after commit/reset
        self._row = None
        # Last complete row, unset until first commit
        self._previous_row = None
        # In-progress cell, unset until first response, after completion
        self._cell = None
        # Last complete cell, unset until first completion, after new row
        self._previous_cell = None

        # May be cached from previous response
        self.last_scanned_row_key = None
        self.read_method = read_method
        self.request = request
        self.retry = retry

        # The `timeout` parameter must be somewhat greater than the value
        # contained in `self.retry`, in order to avoid race-like condition and
        # allow registering the first deadline error before invoking the retry.
        # Otherwise there is a risk of entering an infinite loop that resets
        # the timeout counter just before it being triggered. The increment
        # by 1 second here is customary but should not be much less than that.
        self.response_iterator = read_method(request, timeout=self.retry._deadline + 1)

        self.rows = {}
        self._state = self.STATE_NEW_ROW

        # Flag to stop iteration, for any reason not related to self.retry()
        self._cancelled = False

    @property
    def state(self):
        """State machine state.

        :rtype: str
        :returns:  name of state corresponding to current row / chunk
                   processing.
        """
        return self.read_states[self._state]

    def cancel(self):
        """Cancels the iterator, closing the stream."""
        self._cancelled = True
        self.response_iterator.cancel()

    def consume_all(self, max_loops=None):
        """Consume the streamed responses until there are no more.

        .. warning::
           This method will be removed in future releases.  Please use this
           class as a generator instead.

        :type max_loops: int
        :param max_loops: (Optional) Maximum number of times to try to consume
                          an additional ``ReadRowsResponse``. You can use this
                          to avoid long wait times.
        """
        for row in self:
            self.rows[row.row_key] = row

    def _create_retry_request(self):
        """Helper for :meth:`__iter__`."""
        req_manager = _ReadRowsRequestManager(
            self.request, self.last_scanned_row_key, self._counter
        )
        return req_manager.build_updated_request()

    def _on_error(self, exc):
        """Helper for :meth:`__iter__`."""
        # restart the read scan from AFTER the last successfully read row
        retry_request = self.request
        if self.last_scanned_row_key:
            retry_request = self._create_retry_request()

        self.response_iterator = self.read_method(retry_request)

    def _read_next(self):
        """Helper for :meth:`__iter__`."""
        return next(self.response_iterator)

    def _read_next_response(self):
        """Helper for :meth:`__iter__`."""
        return self.retry(self._read_next, on_error=self._on_error)()

    def __iter__(self):
        """Consume the ``ReadRowsResponse`` s from the stream.
        Read the rows and yield each to the reader

        Parse the response and its chunks into a new/existing row in
        :attr:`_rows`. Rows are returned in order by row key.
        """
        while not self._cancelled:
            try:
                response = self._read_next_response()
            except StopIteration:
                if self.state != self.NEW_ROW:
                    raise ValueError("The row remains partial / is not committed.")
                break

            for chunk in response.chunks:
                if self._cancelled:
                    break
                self._process_chunk(chunk)
                if chunk.commit_row:
                    self.last_scanned_row_key = self._previous_row.row_key
                    self._counter += 1
                    yield self._previous_row

            resp_last_key = response.last_scanned_row_key
            if resp_last_key and resp_last_key > self.last_scanned_row_key:
                self.last_scanned_row_key = resp_last_key

    def _process_chunk(self, chunk):
        if chunk.reset_row:
            self._validate_chunk_reset_row(chunk)
            self._row = None
            self._cell = self._previous_cell = None
            self._state = self.STATE_NEW_ROW
            return

        self._update_cell(chunk)

        if self._row is None:
            if (
                self._previous_row is not None
                and self._cell.row_key <= self._previous_row.row_key
            ):
                raise InvalidChunk()
            self._row = PartialRowData(self._cell.row_key)

        if chunk.value_size == 0:
            self._state = self.STATE_ROW_IN_PROGRESS
            self._save_current_cell()
        else:
            self._state = self.STATE_CELL_IN_PROGRESS

        if chunk.commit_row:
            if chunk.value_size > 0:
                raise InvalidChunk()

            self._previous_row = self._row
            self._row = None
            self._previous_cell = None
            self._state = self.STATE_NEW_ROW

    def _update_cell(self, chunk):
        if self._cell is None:
            qualifier = None
            if "qualifier" in chunk:
                qualifier = chunk.qualifier
            family = None
            if "family_name" in chunk:
                family = chunk.family_name

            self._cell = PartialCellData(
                chunk.row_key,
                family,
                qualifier,
                chunk.timestamp_micros,
                chunk.labels,
                chunk.value,
            )
            self._copy_from_previous(self._cell)
            self._validate_cell_data_new_cell()
        else:
            self._cell.append_value(chunk.value)

    def _validate_cell_data_new_cell(self):
        cell = self._cell
        if not cell.row_key or not cell.family_name or cell.qualifier is None:
            raise InvalidChunk()

        prev = self._previous_cell
        if prev and prev.row_key != cell.row_key:
            raise InvalidChunk()

    def _validate_chunk_reset_row(self, chunk):
        # No reset for new row
        _raise_if(self._state == self.STATE_NEW_ROW)

        # No reset with other keys
        _raise_if(chunk.row_key)
        _raise_if("family_name" in chunk)
        _raise_if("qualifier" in chunk)
        _raise_if(chunk.timestamp_micros)
        _raise_if(chunk.labels)
        _raise_if(chunk.value_size)
        _raise_if(chunk.value)
        _raise_if(chunk.commit_row)

    def _save_current_cell(self):
        """Helper for :meth:`consume_next`."""
        row, cell = self._row, self._cell
        family = row._cells.setdefault(cell.family_name, {})
        qualified = family.setdefault(cell.qualifier, [])
        complete = Cell.from_pb(cell)
        qualified.append(complete)
        self._cell, self._previous_cell = None, cell

    def _copy_from_previous(self, cell):
        """Helper for :meth:`consume_next`."""
        previous = self._previous_cell
        if previous is not None:
            if not cell.row_key:
                cell.row_key = previous.row_key
                if not cell.family_name:
                    cell.family_name = previous.family_name
                    # NOTE: ``cell.qualifier`` **can** be empty string.
                    if cell.qualifier is None:
                        cell.qualifier = previous.qualifier


class _ReadRowsRequestManager(object):
    """Update the ReadRowsRequest message in case of failures by
        filtering the already read keys.

    :type message: class:`data_messages_v2_pb2.ReadRowsRequest`
    :param message: Original ReadRowsRequest containing all of the parameters
                    of API call

    :type last_scanned_key: bytes
    :param last_scanned_key: last successfully scanned key

    :type rows_read_so_far: int
    :param rows_read_so_far: total no of rows successfully read so far.
                            this will be used for updating rows_limit

    """

    def __init__(self, message, last_scanned_key, rows_read_so_far):
        self.message = message
        self.last_scanned_key = last_scanned_key
        self.rows_read_so_far = rows_read_so_far

    def build_updated_request(self):
        """Updates the given message request as per last scanned key"""

        resume_request = data_messages_v2_pb2.ReadRowsRequest()
        data_messages_v2_pb2.ReadRowsRequest.copy_from(resume_request, self.message)

        if self.message.rows_limit != 0:
            # TODO: Throw an error if rows_limit - read_so_far is 0 or negative.
            resume_request.rows_limit = max(
                1, self.message.rows_limit - self.rows_read_so_far
            )

        # if neither RowSet.row_keys nor RowSet.row_ranges currently exist,
        # add row_range that starts with last_scanned_key as start_key_open
        # to request only rows that have not been returned yet
        if "rows" not in self.message:
            row_range = data_v2_pb2.RowRange(start_key_open=self.last_scanned_key)
            resume_request.rows = data_v2_pb2.RowSet(row_ranges=[row_range])
        else:
            row_keys = self._filter_rows_keys()
            row_ranges = self._filter_row_ranges()
            resume_request.rows = data_v2_pb2.RowSet(
                row_keys=row_keys, row_ranges=row_ranges
            )
        return resume_request

    def _filter_rows_keys(self):
        """Helper for :meth:`build_updated_request`"""
        return [
            row_key
            for row_key in self.message.rows.row_keys
            if row_key > self.last_scanned_key
        ]

    def _filter_row_ranges(self):
        """Helper for :meth:`build_updated_request`"""
        new_row_ranges = []

        for row_range in self.message.rows.row_ranges:
            # if current end_key (open or closed) is set, return its value,
            # if not, set to empty string ('').
            # NOTE: Empty string in end_key means "end of table"
            end_key = self._end_key_set(row_range)
            # if end_key is already read, skip to the next row_range
            if end_key and self._key_already_read(end_key):
                continue

            # if current start_key (open or closed) is set, return its value,
            # if not, then set to empty string ('')
            # NOTE: Empty string in start_key means "beginning of table"
            start_key = self._start_key_set(row_range)

            # if start_key was already read or doesn't exist,
            # create a row_range with last_scanned_key as start_key_open
            # to be passed to retry request
            retry_row_range = row_range
            if self._key_already_read(start_key):
                retry_row_range = copy.deepcopy(row_range)
                retry_row_range.start_key_closed = _to_bytes("")
                retry_row_range.start_key_open = self.last_scanned_key

            new_row_ranges.append(retry_row_range)

        return new_row_ranges

    def _key_already_read(self, key):
        """Helper for :meth:`_filter_row_ranges`"""
        return key <= self.last_scanned_key

    @staticmethod
    def _start_key_set(row_range):
        """Helper for :meth:`_filter_row_ranges`"""
        return row_range.start_key_open or row_range.start_key_closed

    @staticmethod
    def _end_key_set(row_range):
        """Helper for :meth:`_filter_row_ranges`"""
        return row_range.end_key_open or row_range.end_key_closed


def _raise_if(predicate, *args):
    """Helper for validation methods."""
    if predicate:
        raise InvalidChunk(*args)
