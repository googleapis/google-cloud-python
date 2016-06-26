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

"""Container for Google Cloud Bigtable Cells and Streaming Row Contents."""


import copy
import six

from gcloud._helpers import _datetime_from_microseconds
from gcloud._helpers import _to_bytes


class Cell(object):
    """Representation of a Google Cloud Bigtable Cell.

    :type value: bytes
    :param value: The value stored in the cell.

    :type timestamp: :class:`datetime.datetime`
    :param timestamp: The timestamp when the cell was stored.

    :type labels: list
    :param labels: (Optional) List of strings. Labels applied to the cell.
    """

    def __init__(self, value, timestamp, labels=()):
        self.value = value
        self.timestamp = timestamp
        self.labels = list(labels)

    @classmethod
    def from_pb(cls, cell_pb):
        """Create a new cell from a Cell protobuf.

        :type cell_pb: :class:`._generated.bigtable_data_pb2.Cell`
        :param cell_pb: The protobuf to convert.

        :rtype: :class:`Cell`
        :returns: The cell corresponding to the protobuf.
        """
        timestamp = _datetime_from_microseconds(cell_pb.timestamp_micros)
        if cell_pb.labels:
            return cls(cell_pb.value, timestamp, labels=cell_pb.labels)
        else:
            return cls(cell_pb.value, timestamp)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.value == self.value and
                other.timestamp == self.timestamp and
                other.labels == self.labels)

    def __ne__(self, other):
        return not self.__eq__(other)


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
        self._committed = False
        self._chunks_encountered = False

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other._row_key == self._row_key and
                other._committed == self._committed and
                other._chunks_encountered == self._chunks_encountered and
                other._cells == self._cells)

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self):
        """Convert the cells to a dictionary.

        This is intended to be used with HappyBase, so the column family and
        column qualiers are combined (with ``:``).

        :rtype: dict
        :returns: Dictionary containing all the data in the cells of this row.
        """
        result = {}
        for column_family_id, columns in six.iteritems(self._cells):
            for column_qual, cells in six.iteritems(columns):
                key = (_to_bytes(column_family_id) + b':' +
                       _to_bytes(column_qual))
                result[key] = cells
        return result

    @property
    def cells(self):
        """Property returning all the cells accumulated on this partial row.

        :rtype: dict
        :returns: Dictionary of the :class:`Cell` objects accumulated. This
                  dictionary has two-levels of keys (first for column families
                  and second for column names/qualifiers within a family). For
                  a given column, a list of :class:`Cell` objects is stored.
        """
        return copy.deepcopy(self._cells)

    @property
    def row_key(self):
        """Getter for the current (partial) row's key.

        :rtype: bytes
        :returns: The current (partial) row's key.
        """
        return self._row_key

    @property
    def committed(self):
        """Getter for the committed status of the (partial) row.

        :rtype: bool
        :returns: The committed status of the (partial) row.
        """
        return self._committed

    def clear(self):
        """Clears all cells that have been added."""
        self._committed = False
        self._chunks_encountered = False
        self._cells.clear()

    def _handle_commit_row(self, chunk, index, last_chunk_index):
        """Handles a ``commit_row`` chunk.

        :type chunk: ``ReadRowsResponse.Chunk``
        :param chunk: The chunk being handled.

        :type index: int
        :param index: The current index of the chunk.

        :type last_chunk_index: int
        :param last_chunk_index: The index of the last chunk.

        :raises: :class:`ValueError <exceptions.ValueError>` if the value of
                 ``commit_row`` is :data:`False` or if the chunk passed is not
                 the last chunk in a response.
        """
        # NOTE: We assume the caller has checked that the ``ONEOF`` property
        #       for ``chunk`` is ``commit_row``.
        if not chunk.commit_row:
            raise ValueError('Received commit_row that was False.')

        if index != last_chunk_index:
            raise ValueError('Commit row chunk was not the last chunk')
        else:
            self._committed = True

    def _handle_reset_row(self, chunk):
        """Handles a ``reset_row`` chunk.

        :type chunk: ``ReadRowsResponse.Chunk``
        :param chunk: The chunk being handled.

        :raises: :class:`ValueError <exceptions.ValueError>` if the value of
                 ``reset_row`` is :data:`False`
        """
        # NOTE: We assume the caller has checked that the ``ONEOF`` property
        #       for ``chunk`` is ``reset_row``.
        if not chunk.reset_row:
            raise ValueError('Received reset_row that was False.')

        self.clear()

    def _handle_row_contents(self, chunk):
        """Handles a ``row_contents`` chunk.

        :type chunk: ``ReadRowsResponse.Chunk``
        :param chunk: The chunk being handled.
        """
        # NOTE: We assume the caller has checked that the ``ONEOF`` property
        #       for ``chunk`` is ``row_contents``.

        # chunk.row_contents is ._generated.bigtable_data_pb2.Family
        column_family_id = chunk.row_contents.name
        column_family_dict = self._cells.setdefault(column_family_id, {})
        for column in chunk.row_contents.columns:
            cells = [Cell.from_pb(cell) for cell in column.cells]

            column_name = column.qualifier
            column_cells = column_family_dict.setdefault(column_name, [])
            column_cells.extend(cells)

    def update_from_read_rows(self, read_rows_response_pb):
        """Updates the current row from a ``ReadRows`` response.

        :type read_rows_response_pb:
            :class:`._generated.bigtable_service_messages_pb2.ReadRowsResponse`
        :param read_rows_response_pb: A response streamed back as part of a
                                      ``ReadRows`` request.

        :raises: :class:`ValueError <exceptions.ValueError>` if the current
                 partial row has already been committed, if the row key on the
                 response doesn't match the current one or if there is a chunk
                 encountered with an unexpected ``ONEOF`` protobuf property.
        """
        if self._committed:
            raise ValueError('The row has been committed')

        if read_rows_response_pb.row_key != self.row_key:
            raise ValueError('Response row key (%r) does not match current '
                             'one (%r).' % (read_rows_response_pb.row_key,
                                            self.row_key))

        last_chunk_index = len(read_rows_response_pb.chunks) - 1
        for index, chunk in enumerate(read_rows_response_pb.chunks):
            chunk_property = chunk.WhichOneof('chunk')
            if chunk_property == 'row_contents':
                self._handle_row_contents(chunk)
            elif chunk_property == 'reset_row':
                self._handle_reset_row(chunk)
            elif chunk_property == 'commit_row':
                self._handle_commit_row(chunk, index, last_chunk_index)
            else:
                # NOTE: This includes chunk_property == None since we always
                #       want a value to be set
                raise ValueError('Unexpected chunk property: %s' % (
                    chunk_property,))

            self._chunks_encountered = True


class PartialRowsData(object):
    """Convenience wrapper for consuming a ``ReadRows`` streaming response.

    :type response_iterator:
        :class:`grpc.framework.alpha._reexport._CancellableIterator`
    :param response_iterator: A streaming iterator returned from a
                              ``ReadRows`` request.
    """

    def __init__(self, response_iterator):
        # We expect an iterator of `data_messages_pb2.ReadRowsResponse`
        self._response_iterator = response_iterator
        self._rows = {}

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other._response_iterator == self._response_iterator

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def rows(self):
        """Property returning all rows accumulated from the stream.

        :rtype: dict
        :returns: Dictionary of :class:`PartialRowData`.
        """
        # NOTE: To avoid duplicating large objects, this is just the
        #       mutable private data.
        return self._rows

    def cancel(self):
        """Cancels the iterator, closing the stream."""
        self._response_iterator.cancel()

    def consume_next(self):
        """Consumes the next ``ReadRowsResponse`` from the stream.

        Parses the response and stores it as a :class:`PartialRowData`
        in a dictionary owned by this object.

        :raises: :class:`StopIteration <exceptions.StopIteration>` if the
                 response iterator has no more responses to stream.
        """
        read_rows_response = self._response_iterator.next()
        row_key = read_rows_response.row_key
        partial_row = self._rows.get(row_key)
        if partial_row is None:
            partial_row = self._rows[row_key] = PartialRowData(row_key)
        # NOTE: This is not atomic in the case of failures.
        partial_row.update_from_read_rows(read_rows_response)

    def consume_all(self, max_loops=None):
        """Consume the streamed responses until there are no more.

        This simply calls :meth:`consume_next` until there are no
        more to consume.

        :type max_loops: int
        :param max_loops: (Optional) Maximum number of times to try to consume
                          an additional ``ReadRowsResponse``. You can use this
                          to avoid long wait times.
        """
        curr_loop = 0
        if max_loops is None:
            max_loops = float('inf')
        while curr_loop < max_loops:
            curr_loop += 1
            try:
                self.consume_next()
            except StopIteration:
                break


class ReadRowsResponseError(RuntimeError):
    """Exception raised to to invalid chunk / response data from back-end."""


def _raise_if(predicate):
    """Helper for validation methods."""
    if predicate:
        raise ReadRowsResponseError()


class PartialCellV2(object):
    """Data for a not-yet-complete cell."""

    def __init__(self, row_key, family_name, qualifier, timestamp_micros,
                 labels=(), value=b''):
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


class PartialRowsDataV2(object):
    """Handle state involved in consuming a ``ReadRows`` streaming response.

    :type response_iterator:
        :class:`grpc.framework.alpha._reexport._CancellableIterator` returning
        :class:`gcloud.bigtable._generated_v2.bigtable_pb2.ReadRowsResponse`
    :param response_iterator:
        A streaming iterator returned from a ``ReadRows`` request.
    """
    # State names
    START = "Start"
    NEW_ROW = "New row"
    ROW_IN_PROGRESS = "Row in progress"
    CELL_IN_PROGRESS = "Cell in progress"

    def __init__(self, response_iterator):
        self._response_iterator = response_iterator
        # Fully-processed rows, keyed by `row_key`
        self._rows = {}
        # Counter for responses pulled from iterator
        self._counter = 0
        # Maybe cached from previous response
        self._last_scanned_row_key = None
        # In-progress row, unset until first response, after commit/reset
        self._row = None
        # Last complete row, unset until first commit
        self._previous_row = None
        # In-progress cell, unset until first response, after completion
        self._cell = None
        # Last complete cell, unset until first completion, after new row
        self._previous_cell = None

    @property
    def state(self):
        """Name of state machine state."""
        if self._last_scanned_row_key is None:
            return self.START
        if self._row is None:
            assert self._cell is None
            assert self._previous_cell is None
            return self.NEW_ROW
        if self._cell is not None:
            return self.CELL_IN_PROGRESS
        if self._previous_cell is not None:
            return self.ROW_IN_PROGRESS
        return self.NEW_ROW  # row added, no chunk yet processed

    @property
    def rows(self):
        """Property returning all rows accumulated from the stream.

        :rtype: dict
        :returns: Dictionary of :class:`PartialRowData`.
        """
        _raise_if(self.state not in (self.NEW_ROW,))
        # NOTE: To avoid duplicating large objects, this is just the
        #       mutable private data.
        return self._rows

    @staticmethod
    def _validate_chunk_status(chunk):
        """Helper for :meth:`_validate_chunk_row_in_progress`, etc."""
        # No reseet with other keys
        if chunk.reset_row:
            _raise_if(chunk.row_key)
            _raise_if(chunk.HasField('family_name'))
            _raise_if(chunk.HasField('qualifier'))
            _raise_if(chunk.timestamp_micros)
            _raise_if(chunk.labels)
            _raise_if(chunk.value_size)
            _raise_if(chunk.value)
        # No commit with value size
        _raise_if(chunk.commit_row and chunk.value_size > 0)
        # No negative value_size (inferred as a general constraint).
        _raise_if(chunk.value_size < 0)

    def _validate_chunk_new_row(self, chunk):
        """Helper for :meth:`_validate_chunk`."""
        assert self.state == self.NEW_ROW
        _raise_if(chunk.reset_row)
        _raise_if(not chunk.row_key)
        _raise_if(not chunk.family_name)
        _raise_if(not chunk.qualifier)
        # This constraint is not enforced in the Go example.
        _raise_if(chunk.value_size > 0 and chunk.commit_row is not False)
        # This constraint is from the Go example, not the spec.
        _raise_if(self._previous_row is not None and
                  chunk.row_key <= self._previous_row.row_key)

    def _same_as_previous(self, chunk):
        """Helper for :meth:`_validate_chunk_row_in_progress`"""
        previous = self._previous_cell
        return (chunk.row_key == previous.row_key and
                chunk.family_name == previous.family_name and
                chunk.qualifier == previous.qualifier and
                chunk.labels == previous.labels)

    def _validate_chunk_row_in_progress(self, chunk):
        """Helper for :meth:`_validate_chunk`"""
        assert self.state == self.ROW_IN_PROGRESS
        self._validate_chunk_status(chunk)
        if not chunk.HasField('commit_row') and not chunk.reset_row:
            _raise_if(not chunk.timestamp_micros or not chunk.value)
        _raise_if(chunk.row_key and
                  chunk.row_key != self._row.row_key)
        _raise_if(chunk.HasField('family_name') and
                  not chunk.HasField('qualifier'))
        previous = self._previous_cell
        _raise_if(self._same_as_previous(chunk) and
                  chunk.timestamp_micros <= previous.timestamp_micros)

    def _validate_chunk_cell_in_progress(self, chunk):
        """Helper for :meth:`_validate_chunk`"""
        assert self.state == self.CELL_IN_PROGRESS
        self._validate_chunk_status(chunk)
        self._copy_from_current(chunk)

    def _validate_chunk(self, chunk):
        """Helper for :meth:`consume_next`."""
        if self.state == self.NEW_ROW:
            self._validate_chunk_new_row(chunk)
        if self.state == self.ROW_IN_PROGRESS:
            self._validate_chunk_row_in_progress(chunk)
        if self.state == self.CELL_IN_PROGRESS:
            self._validate_chunk_cell_in_progress(chunk)

    def _save_current_cell(self):
        """Helper for :meth:`consume_next`."""
        row, cell = self._row, self._cell
        family = row._cells.setdefault(cell.family_name, {})
        qualified = family.setdefault(cell.qualifier, [])
        complete = Cell.from_pb(self._cell)
        qualified.append(complete)
        self._cell, self._previous_cell = None, cell

    def _copy_from_current(self, chunk):
        """Helper for :meth:`consume_next`."""
        current = self._cell
        if current is not None:
            if not chunk.row_key:
                chunk.row_key = current.row_key
            if not chunk.HasField('family_name'):
                chunk.family_name.value = current.family_name
            if not chunk.HasField('qualifier'):
                chunk.qualifier.value = current.qualifier
            if not chunk.timestamp_micros:
                chunk.timestamp_micros = current.timestamp_micros
            if not chunk.labels:
                chunk.labels.extend(current.labels)

    def _copy_from_previous(self, cell):
        """Helper for :meth:`consume_next`."""
        previous = self._previous_cell
        if previous is not None:
            if not cell.row_key:
                cell.row_key = previous.row_key
            if not cell.family_name:
                cell.family_name = previous.family_name
            if not cell.qualifier:
                cell.qualifier = previous.qualifier

    def _save_current_row(self):
        """Helper for :meth:`consume_next`."""
        if self._cell:
            self._save_current_cell()
        self._rows[self._row.row_key] = self._row
        self._row, self._previous_row = None, self._row
        self._previous_cell = None

    def consume_next(self):
        """Consume the next ``ReadRowsResponse`` from the stream.

        Parse the response and its chunks into a new/existing row in
        :attr:`_rows`
        """
        response = self._response_iterator.next()
        self._counter += 1

        if self._last_scanned_row_key is None:  # first response
            if response.last_scanned_row_key:
                raise ReadRowsResponseError()

        self._last_scanned_row_key = response.last_scanned_row_key

        row = self._row
        cell = self._cell

        for chunk in response.chunks:

            self._validate_chunk(chunk)

            if chunk.reset_row:
                row = self._row = None
                cell = self._cell = self._previous_cell = None
                continue

            if row is None:
                row = self._row = PartialRowData(chunk.row_key)

            if cell is None:
                cell = self._cell = PartialCellV2(
                    chunk.row_key,
                    chunk.family_name.value,
                    chunk.qualifier.value,
                    chunk.timestamp_micros,
                    chunk.labels,
                    chunk.value)
                self._copy_from_previous(cell)
            else:
                cell.append_value(chunk.value)

            if chunk.commit_row:
                self._save_current_row()
                row = cell = None
                continue

            if chunk.value_size == 0:
                self._save_current_cell()
                cell = None
