# Copyright 2018 Google LLC
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

"""User-friendly container for Google Cloud Bigtable RowSet """


from google.cloud._helpers import _to_bytes
from google.cloud.bigtable_v2.proto import (
    bigtable_pb2 as data_messages_v2_pb2)


class RowSet(object):
    """ Convenience wrapper of google.bigtable.v2.RowSet
        Useful for creating a set of row keys and row ranges, which can
        be passed to yield_rows method of class:`.Table.yield_rows`.
    """

    def __init__(self):
        self.row_keys = []
        self.row_ranges = []

    def add_row_key(self, row_key):
        """Add row key to row_keys list.

        :type row_key: string utf-8
        :param row_key: The key of a row to read
        """
        self.row_keys.append(row_key)

    def add_row_range(self, row_range):
        """Add row_range to row_ranges list.

        :type row_range: class:`RowRange`
        :param row_range: The row range object having start and end key
        """
        self.row_ranges.append(row_range)

    def _update_message_request(self, message):
        """Add row keys and row range to given request message

        :type message: class:`data_messages_v2_pb2.ReadRowsRequest`
        :param message: The ``ReadRowsRequest`` protobuf
        """
        for each in self.row_keys:
            message.rows.row_keys.append(_to_bytes(each))

        for each in self.row_ranges:
            r_kwrags = each.get_range_kwargs()
            message.rows.row_ranges.add(**r_kwrags)


class RowRange(object):
    """ Convenience wrapper of google.bigtable.v2.RowRange

    :type start_key: string utf-8
    :param start_key: start key of the row range

    :type end_key: string utf-8
    :param end_key: end key of the row range

    :type start_inclusive: bool
    :param start_inclusive: (Optional) Whether the ``start_key`` should be
                  considered inclusive. The default is True (inclusive).

    :type end_inclusive: bool
    :param end_inclusive: (Optional) Whether the ``end_key`` should be
                  considered inclusive. The default is False (exclusive).
    """

    def __init__(self, start_key, end_key,
                 start_inclusive=True,
                 end_inclusive=False):
        self.start_key = start_key
        self.start_inclusive = start_inclusive
        self.end_key = end_key
        self.end_inclusive = end_inclusive

    def get_range_kwargs(self):
        """ Convert row range object to dict which can be passed to
        google.bigtable.v2.RowRange add method.
        """
        range_kwargs = {}
        start_key_key = 'start_key_open'
        if self.start_inclusive:
            start_key_key = 'start_key_closed'
        range_kwargs[start_key_key] = _to_bytes(self.start_key)
        end_key_key = 'end_key_open'
        if self.end_inclusive:
            end_key_key = 'end_key_closed'
        range_kwargs[end_key_key] = _to_bytes(self.end_key)
        return range_kwargs


class ReadRowsRequestManager(object):
    """ Update the ReadRowsRequest message in case of failures by
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
        self.new_message = None

    def build_updated_request(self):
        """ Updates the given message request as per last scanned key
        """
        r_kwargs = {'table_name': self.message.table_name}
        r_kwargs['filter'] = self.message.filter

        if self.message.rows_limit != 0:
            r_kwargs['rows_limit'] = max(1, self.message.rows_limit -
                                         self.rows_read_so_far)

        self.new_message = data_messages_v2_pb2.ReadRowsRequest(**r_kwargs)
        self._filter_rows_keys()
        self._filter_row_ranges()
        return self.new_message

    def _filter_rows_keys(self):
        """ Helper for :meth:`build_updated_request`"""
        for row_key in self.message.rows.row_keys:
            if(row_key > self.last_scanned_key):
                self.new_message.rows.row_keys.append(row_key)

    def _filter_row_ranges(self):
        """ Helper for :meth:`build_updated_request`"""
        new_row_ranges = []

        for row_range in self.message.rows.row_ranges:
            if((row_range.end_key_open and
                self._key_already_read(row_range.end_key_open)) or
                (row_range.end_key_closed and
                 self._key_already_read(row_range.end_key_closed))):
                    continue

            if ((row_range.start_key_open and
                self._key_already_read(row_range.start_key_open)) or
                (row_range.start_key_closed and
                 self._key_already_read(row_range.start_key_closed))):
                row_range.start_key_closed = _to_bytes("")
                row_range.start_key_open = self.last_scanned_key

                new_row_ranges.append(row_range)
            else:
                new_row_ranges.append(row_range)

        self.new_message.rows.row_ranges.extend(new_row_ranges)

    def _key_already_read(self, key):
        """ Helper for :meth:`_filter_row_ranges`"""
        return key <= self.last_scanned_key
