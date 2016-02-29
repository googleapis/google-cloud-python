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
