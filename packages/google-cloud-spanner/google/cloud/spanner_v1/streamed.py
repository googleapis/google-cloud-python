# Copyright 2016 Google LLC All rights reserved.
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

from google.cloud import exceptions
from google.cloud.spanner_v1 import TypeCode
import six

# pylint: disable=ungrouped-imports
from google.cloud.spanner_v1._helpers import _parse_value

# pylint: enable=ungrouped-imports


class StreamedResultSet(object):
    """Process a sequence of partial result sets into a single set of row data.

    :type response_iterator:
    :param response_iterator:
        Iterator yielding
        :class:`~google.cloud.spanner_v1.PartialResultSet`
        instances.

    :type source: :class:`~google.cloud.spanner_v1.snapshot.Snapshot`
    :param source: Snapshot from which the result set was fetched.
    """

    def __init__(self, response_iterator, source=None):
        self._response_iterator = response_iterator
        self._rows = []  # Fully-processed rows
        self._metadata = None  # Until set from first PRS
        self._stats = None  # Until set from last PRS
        self._current_row = []  # Accumulated values for incomplete row
        self._pending_chunk = None  # Incomplete value
        self._source = source  # Source snapshot

    @property
    def fields(self):
        """Field descriptors for result set columns.

        :rtype: list of :class:`~google.cloud.spanner_v1.StructType.Field`
        :returns: list of fields describing column names / types.
        """
        return self._metadata.row_type.fields

    @property
    def metadata(self):
        """Result set metadata

        :rtype: :class:`~google.cloud.spanner_v1.ResultSetMetadata`
        :returns: structure describing the results
        """
        return self._metadata

    @property
    def stats(self):
        """Result set statistics

        :rtype:
           :class:`~google.cloud.spanner_v1.ResultSetStats`
        :returns: structure describing status about the response
        """
        return self._stats

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
        merged = _merge_by_type(self._pending_chunk, value, field.type_)
        self._pending_chunk = None
        return _parse_value(merged, field.type_)

    def _merge_values(self, values):
        """Merge values into rows.

        :type values: list of :class:`~google.protobuf.struct_pb2.Value`
        :param values: non-chunked values from partial result set.
        """
        width = len(self.fields)
        for value in values:
            index = len(self._current_row)
            field = self.fields[index]
            self._current_row.append(_parse_value(value, field.type_))
            if len(self._current_row) == width:
                self._rows.append(self._current_row)
                self._current_row = []

    def _consume_next(self):
        """Consume the next partial result set from the stream.

        Parse the result set into new/existing rows in :attr:`_rows`
        """
        response = six.next(self._response_iterator)

        if self._metadata is None:  # first response
            metadata = self._metadata = response.metadata

            source = self._source
            if source is not None and source._transaction_id is None:
                source._transaction_id = metadata.transaction.id

        if "stats" in response:  # last response
            self._stats = response.stats

        values = list(response.values)
        if self._pending_chunk is not None:
            values[0] = self._merge_chunk(values[0])

        if response.chunked_value:
            self._pending_chunk = values.pop()

        self._merge_values(values)

    def __iter__(self):
        iter_rows, self._rows[:] = self._rows[:], ()
        while True:
            if not iter_rows:
                try:
                    self._consume_next()
                except StopIteration:
                    return
                iter_rows, self._rows[:] = self._rows[:], ()
            while iter_rows:
                yield iter_rows.pop(0)

    def one(self):
        """Return exactly one result, or raise an exception.

        :raises: :exc:`NotFound`: If there are no results.
        :raises: :exc:`ValueError`: If there are multiple results.
        :raises: :exc:`RuntimeError`: If consumption has already occurred,
            in whole or in part.
        """
        answer = self.one_or_none()
        if answer is None:
            raise exceptions.NotFound("No rows matched the given query.")
        return answer

    def one_or_none(self):
        """Return exactly one result, or None if there are no results.

        :raises: :exc:`ValueError`: If there are multiple results.
        :raises: :exc:`RuntimeError`: If consumption has already occurred,
            in whole or in part.
        """
        # Sanity check: Has consumption of this query already started?
        # If it has, then this is an exception.
        if self._metadata is not None:
            raise RuntimeError(
                "Can not call `.one` or `.one_or_none` after "
                "stream consumption has already started."
            )

        # Consume the first result of the stream.
        # If there is no first result, then return None.
        iterator = iter(self)
        try:
            answer = next(iterator)
        except StopIteration:
            return None

        # Attempt to consume more. This should no-op; if we get additional
        # rows, then this is an error case.
        try:
            next(iterator)
            raise ValueError("Expected one result; got more.")
        except StopIteration:
            return answer


class Unmergeable(ValueError):
    """Unable to merge two values.

    :type lhs: :class:`~google.protobuf.struct_pb2.Value`
    :param lhs: pending value to be merged

    :type rhs: :class:`~google.protobuf.struct_pb2.Value`
    :param rhs: remaining value to be merged

    :type type_: :class:`~google.cloud.spanner_v1.Type`
    :param type_: field type of values being merged
    """

    def __init__(self, lhs, rhs, type_):
        message = "Cannot merge %s values: %s %s" % (TypeCode(type_.code), lhs, rhs,)
        super(Unmergeable, self).__init__(message)


def _unmergeable(lhs, rhs, type_):
    """Helper for '_merge_by_type'."""
    raise Unmergeable(lhs, rhs, type_)


def _merge_float64(lhs, rhs, type_):  # pylint: disable=unused-argument
    """Helper for '_merge_by_type'."""
    if type(lhs) == str:
        return float(lhs + rhs)
    array_continuation = type(lhs) == float and type(rhs) == str and rhs == ""
    if array_continuation:
        return lhs
    raise Unmergeable(lhs, rhs, type_)


def _merge_string(lhs, rhs, type_):  # pylint: disable=unused-argument
    """Helper for '_merge_by_type'."""
    return str(lhs) + str(rhs)


_UNMERGEABLE_TYPES = (TypeCode.BOOL,)


def _merge_array(lhs, rhs, type_):
    """Helper for '_merge_by_type'."""
    element_type = type_.array_element_type
    if element_type.code in _UNMERGEABLE_TYPES:
        # Individual values cannot be merged, just concatenate
        lhs.extend(rhs)
        return lhs

    # Sanity check: If either list is empty, short-circuit.
    # This is effectively a no-op.
    if not len(lhs) or not len(rhs):
        lhs.extend(rhs)
        return lhs

    first = rhs.pop(0)
    if first is None:  # can't merge
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
    lhs.extend(rhs)
    return lhs


def _merge_struct(lhs, rhs, type_):
    """Helper for '_merge_by_type'."""
    fields = type_.struct_type.fields

    # Sanity check: If either list is empty, short-circuit.
    # This is effectively a no-op.
    if not len(lhs) or not len(rhs):
        lhs.extend(rhs)
        return lhs

    candidate_type = fields[len(lhs) - 1].type_
    first = rhs.pop(0)
    if first is None or candidate_type.code in _UNMERGEABLE_TYPES:
        lhs.append(first)
    else:
        last = lhs.pop()
        try:
            merged = _merge_by_type(last, first, candidate_type)
        except Unmergeable:
            lhs.append(last)
            lhs.append(first)
        else:
            lhs.append(merged)
    lhs.extend(rhs)
    return lhs


_MERGE_BY_TYPE = {
    TypeCode.ARRAY: _merge_array,
    TypeCode.BOOL: _unmergeable,
    TypeCode.BYTES: _merge_string,
    TypeCode.DATE: _merge_string,
    TypeCode.FLOAT64: _merge_float64,
    TypeCode.INT64: _merge_string,
    TypeCode.STRING: _merge_string,
    TypeCode.STRUCT: _merge_struct,
    TypeCode.TIMESTAMP: _merge_string,
}


def _merge_by_type(lhs, rhs, type_):
    """Helper for '_merge_chunk'."""
    merger = _MERGE_BY_TYPE[type_.code]
    return merger(lhs, rhs, type_)
