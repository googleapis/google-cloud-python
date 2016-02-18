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
