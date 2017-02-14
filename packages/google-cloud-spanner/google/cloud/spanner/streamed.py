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

"""Wrapper for streaming results."""

from google.protobuf.struct_pb2 import ListValue
from google.protobuf.struct_pb2 import Value
from google.cloud.proto.spanner.v1 import type_pb2
import six

# pylint: disable=ungrouped-imports
from google.cloud.spanner._helpers import _parse_value_pb
# pylint: enable=ungrouped-imports


class StreamedResultSet(object):
    """Process a sequence of partial result sets into a single set of row data.

    :type response_iterator:
    :param response_iterator:
        Iterator yielding
        :class:`google.cloud.proto.spanner.v1.result_set_pb2.PartialResultSet`
        instances.
    """
    def __init__(self, response_iterator):
        self._response_iterator = response_iterator
        self._rows = []             # Fully-processed rows
        self._counter = 0           # Counter for processed responses
        self._metadata = None       # Until set from first PRS
        self._stats = None          # Until set from last PRS
        self._resume_token = None   # To resume from last received PRS
        self._current_row = []      # Accumulated values for incomplete row
        self._pending_chunk = None  # Incomplete value

    @property
    def rows(self):
        """Fully-processed rows.

        :rtype: list of row-data lists.
        :returns: list of completed row data, from proceesd PRS responses.
        """
        return self._rows

    @property
    def fields(self):
        """Field descriptors for result set columns.

        :rtype: list of :class:`~google.cloud.proto.spanner.v1.type_pb2.Field`
        :returns: list of fields describing column names / types.
        """
        return self._metadata.row_type.fields

    @property
    def metadata(self):
        """Result set metadata

        :rtype: :class:`~.result_set_pb2.ResultSetMetadata`
        :returns: structure describing the results
        """
        return self._metadata

    @property
    def stats(self):
        """Result set statistics

        :rtype:
           :class:`~google.cloud.proto.spanner.v1.result_set_pb2.ResultSetStats`
        :returns: structure describing status about the response
        """
        return self._stats

    @property
    def resume_token(self):
        """Token for resuming interrupted read / query.

        :rtype: bytes
        :returns: token from last chunk of results.
        """
        return self._resume_token

    def _merge_chunk(self, value):
        """Merge pending chunk with next value.

        :type value: :class:`~google.protobuf.struct_pb2.Value`
        :param value: continuation of chunked value from previous
                      partial result set.

        :rtype: :class:`~google.protobuf.struct_pb2.Value`
        :returns: the merged value
        """
        current_column = len(self._current_row)
        field = self.fields[current_column]
        merged = _merge_by_type(self._pending_chunk, value, field.type)
        self._pending_chunk = None
        return merged

    def _merge_values(self, values):
        """Merge values into rows.

        :type values: list of :class:`~google.protobuf.struct_pb2.Value`
        :param values: non-chunked values from partial result set.
        """
        width = len(self.fields)
        for value in values:
            index = len(self._current_row)
            field = self.fields[index]
            self._current_row.append(_parse_value_pb(value, field.type))
            if len(self._current_row) == width:
                self._rows.append(self._current_row)
                self._current_row = []

    def consume_next(self):
        """Consume the next partial result set from the stream.

        Parse the result set into new/existing rows in :attr:`_rows`
        """
        response = six.next(self._response_iterator)
        self._counter += 1
        self._resume_token = response.resume_token

        if self._metadata is None:  # first response
            self._metadata = response.metadata

        if response.HasField('stats'):  # last response
            self._stats = response.stats

        values = list(response.values)
        if self._pending_chunk is not None:
            values[0] = self._merge_chunk(values[0])

        if response.chunked_value:
            self._pending_chunk = values.pop()

        self._merge_values(values)

    def consume_all(self):
        """Consume the streamed responses until there are no more."""
        while True:
            try:
                self.consume_next()
            except StopIteration:
                break

    def __iter__(self):
        iter_rows, self._rows[:] = self._rows[:], ()
        while True:
            if len(iter_rows) == 0:
                self.consume_next()  # raises StopIteration
                iter_rows, self._rows[:] = self._rows[:], ()
            while iter_rows:
                yield iter_rows.pop(0)


class Unmergeable(ValueError):
    """Unable to merge two values.

    :type lhs: :class:`google.protobuf.struct_pb2.Value`
    :param lhs: pending value to be merged

    :type rhs: :class:`google.protobuf.struct_pb2.Value`
    :param rhs: remaining value to be merged

    :type type_: :class:`google.cloud.proto.spanner.v1.type_pb2.Type`
    :param type_: field type of values being merged
    """
    def __init__(self, lhs, rhs, type_):
        message = "Cannot merge %s values: %s %s" % (
            type_pb2.TypeCode.Name(type_.code), lhs, rhs)
        super(Unmergeable, self).__init__(message)


def _unmergeable(lhs, rhs, type_):
    """Helper for '_merge_by_type'."""
    raise Unmergeable(lhs, rhs, type_)


def _merge_float64(lhs, rhs, type_):  # pylint: disable=unused-argument
    """Helper for '_merge_by_type'."""
    lhs_kind = lhs.WhichOneof('kind')
    if lhs_kind == 'string_value':
        return Value(string_value=lhs.string_value + rhs.string_value)
    rhs_kind = rhs.WhichOneof('kind')
    array_continuation = (
        lhs_kind == 'number_value' and
        rhs_kind == 'string_value' and
        rhs.string_value == '')
    if array_continuation:
        return lhs
    raise Unmergeable(lhs, rhs, type_)


def _merge_string(lhs, rhs, type_):  # pylint: disable=unused-argument
    """Helper for '_merge_by_type'."""
    return Value(string_value=lhs.string_value + rhs.string_value)


_UNMERGEABLE_TYPES = (type_pb2.BOOL,)


def _merge_array(lhs, rhs, type_):
    """Helper for '_merge_by_type'."""
    element_type = type_.array_element_type
    if element_type.code in _UNMERGEABLE_TYPES:
        # Individual values cannot be merged, just concatenate
        lhs.list_value.values.extend(rhs.list_value.values)
        return lhs
    lhs, rhs = list(lhs.list_value.values), list(rhs.list_value.values)
    first = rhs.pop(0)
    if first.HasField('null_value'):  # can't merge
        lhs.append(first)
    else:
        last = lhs.pop()
        try:
            merged = _merge_by_type(last, first, element_type)
        except Unmergeable:
            lhs.append(last)
            lhs.append(first)
        else:
            lhs.append(merged)
    return Value(list_value=ListValue(values=(lhs + rhs)))


def _merge_struct(lhs, rhs, type_):
    """Helper for '_merge_by_type'."""
    fields = type_.struct_type.fields
    lhs, rhs = list(lhs.list_value.values), list(rhs.list_value.values)
    candidate_type = fields[len(lhs) - 1].type
    first = rhs.pop(0)
    if (first.HasField('null_value') or
            candidate_type.code in _UNMERGEABLE_TYPES):
        lhs.append(first)
    else:
        last = lhs.pop()
        lhs.append(_merge_by_type(last, first, candidate_type))
    return Value(list_value=ListValue(values=lhs + rhs))


_MERGE_BY_TYPE = {
    type_pb2.BOOL: _unmergeable,
    type_pb2.INT64: _merge_string,
    type_pb2.FLOAT64: _merge_float64,
    type_pb2.STRING: _merge_string,
    type_pb2.ARRAY: _merge_array,
    type_pb2.STRUCT: _merge_struct,
}


def _merge_by_type(lhs, rhs, type_):
    """Helper for '_merge_chunk'."""
    merger = _MERGE_BY_TYPE[type_.code]
    return merger(lhs, rhs, type_)
