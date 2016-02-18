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


import unittest2


class TestCell(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.row_data import Cell
        return Cell

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _from_pb_test_helper(self, labels=None):
        import datetime
        from gcloud._helpers import _EPOCH
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        timestamp_micros = 18738724000  # Make sure millis granularity
        timestamp = _EPOCH + datetime.timedelta(microseconds=timestamp_micros)
        value = b'value-bytes'

        if labels is None:
            cell_pb = data_pb2.Cell(value=value,
                                    timestamp_micros=timestamp_micros)
            cell_expected = self._makeOne(value, timestamp)
        else:
            cell_pb = data_pb2.Cell(value=value,
                                    timestamp_micros=timestamp_micros,
                                    labels=labels)
            cell_expected = self._makeOne(value, timestamp, labels=labels)

        klass = self._getTargetClass()
        result = klass.from_pb(cell_pb)
        self.assertEqual(result, cell_expected)

    def test_from_pb(self):
        self._from_pb_test_helper()

    def test_from_pb_with_labels(self):
        labels = [u'label1', u'label2']
        self._from_pb_test_helper(labels)

    def test_constructor(self):
        value = object()
        timestamp = object()
        cell = self._makeOne(value, timestamp)
        self.assertEqual(cell.value, value)
        self.assertEqual(cell.timestamp, timestamp)

    def test___eq__(self):
        value = object()
        timestamp = object()
        cell1 = self._makeOne(value, timestamp)
        cell2 = self._makeOne(value, timestamp)
        self.assertEqual(cell1, cell2)

    def test___eq__type_differ(self):
        cell1 = self._makeOne(None, None)
        cell2 = object()
        self.assertNotEqual(cell1, cell2)

    def test___ne__same_value(self):
        value = object()
        timestamp = object()
        cell1 = self._makeOne(value, timestamp)
        cell2 = self._makeOne(value, timestamp)
        comparison_val = (cell1 != cell2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        value1 = 'value1'
        value2 = 'value2'
        timestamp = object()
        cell1 = self._makeOne(value1, timestamp)
        cell2 = self._makeOne(value2, timestamp)
        self.assertNotEqual(cell1, cell2)


class TestPartialRowData(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.row_data import PartialRowData
        return PartialRowData

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        row_key = object()
        partial_row_data = self._makeOne(row_key)
        self.assertTrue(partial_row_data._row_key is row_key)
        self.assertEqual(partial_row_data._cells, {})
        self.assertFalse(partial_row_data._committed)
        self.assertFalse(partial_row_data._chunks_encountered)

    def test___eq__(self):
        row_key = object()
        partial_row_data1 = self._makeOne(row_key)
        partial_row_data2 = self._makeOne(row_key)
        self.assertEqual(partial_row_data1, partial_row_data2)

    def test___eq__type_differ(self):
        partial_row_data1 = self._makeOne(None)
        partial_row_data2 = object()
        self.assertNotEqual(partial_row_data1, partial_row_data2)

    def test___ne__same_value(self):
        row_key = object()
        partial_row_data1 = self._makeOne(row_key)
        partial_row_data2 = self._makeOne(row_key)
        comparison_val = (partial_row_data1 != partial_row_data2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        row_key1 = object()
        partial_row_data1 = self._makeOne(row_key1)
        row_key2 = object()
        partial_row_data2 = self._makeOne(row_key2)
        self.assertNotEqual(partial_row_data1, partial_row_data2)

    def test___ne__committed(self):
        row_key = object()
        partial_row_data1 = self._makeOne(row_key)
        partial_row_data1._committed = object()
        partial_row_data2 = self._makeOne(row_key)
        self.assertNotEqual(partial_row_data1, partial_row_data2)

    def test___ne__cells(self):
        row_key = object()
        partial_row_data1 = self._makeOne(row_key)
        partial_row_data1._cells = object()
        partial_row_data2 = self._makeOne(row_key)
        self.assertNotEqual(partial_row_data1, partial_row_data2)

    def test_to_dict(self):
        cell1 = object()
        cell2 = object()
        cell3 = object()

        family_name1 = u'name1'
        family_name2 = u'name2'
        qual1 = b'col1'
        qual2 = b'col2'
        qual3 = b'col3'

        partial_row_data = self._makeOne(None)
        partial_row_data._cells = {
            family_name1: {
                qual1: cell1,
                qual2: cell2,
            },
            family_name2: {
                qual3: cell3,
            },
        }

        result = partial_row_data.to_dict()
        expected_result = {
            b'name1:col1': cell1,
            b'name1:col2': cell2,
            b'name2:col3': cell3,
        }
        self.assertEqual(result, expected_result)

    def test_cells_property(self):
        partial_row_data = self._makeOne(None)
        cells = {1: 2}
        partial_row_data._cells = cells
        # Make sure we get a copy, not the original.
        self.assertFalse(partial_row_data.cells is cells)
        self.assertEqual(partial_row_data.cells, cells)

    def test_row_key_getter(self):
        row_key = object()
        partial_row_data = self._makeOne(row_key)
        self.assertTrue(partial_row_data.row_key is row_key)

    def test_committed_getter(self):
        partial_row_data = self._makeOne(None)
        partial_row_data._committed = value = object()
        self.assertTrue(partial_row_data.committed is value)

    def test_clear(self):
        partial_row_data = self._makeOne(None)
        cells = {1: 2}
        partial_row_data._cells = cells
        self.assertEqual(partial_row_data.cells, cells)
        partial_row_data._committed = True
        partial_row_data._chunks_encountered = True
        partial_row_data.clear()
        self.assertFalse(partial_row_data.committed)
        self.assertFalse(partial_row_data._chunks_encountered)
        self.assertEqual(partial_row_data.cells, {})

    def test__handle_commit_row(self):
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)

        partial_row_data = self._makeOne(None)
        chunk = messages_pb2.ReadRowsResponse.Chunk(commit_row=True)

        index = last_chunk_index = 1
        self.assertFalse(partial_row_data.committed)
        partial_row_data._handle_commit_row(chunk, index, last_chunk_index)
        self.assertTrue(partial_row_data.committed)

    def test__handle_commit_row_false(self):
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)

        partial_row_data = self._makeOne(None)
        chunk = messages_pb2.ReadRowsResponse.Chunk(commit_row=False)

        with self.assertRaises(ValueError):
            partial_row_data._handle_commit_row(chunk, None, None)

    def test__handle_commit_row_not_last_chunk(self):
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)

        partial_row_data = self._makeOne(None)
        chunk = messages_pb2.ReadRowsResponse.Chunk(commit_row=True)

        with self.assertRaises(ValueError):
            index = 0
            last_chunk_index = 1
            self.assertNotEqual(index, last_chunk_index)
            partial_row_data._handle_commit_row(chunk, index, last_chunk_index)

    def test__handle_reset_row(self):
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)

        partial_row_data = self._makeOne(None)
        chunk = messages_pb2.ReadRowsResponse.Chunk(reset_row=True)

        # Modify the PartialRowData object so we can check it's been cleared.
        partial_row_data._cells = {1: 2}
        partial_row_data._committed = True
        partial_row_data._handle_reset_row(chunk)
        self.assertEqual(partial_row_data.cells, {})
        self.assertFalse(partial_row_data.committed)

    def test__handle_reset_row_failure(self):
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)

        partial_row_data = self._makeOne(None)
        chunk = messages_pb2.ReadRowsResponse.Chunk(reset_row=False)

        with self.assertRaises(ValueError):
            partial_row_data._handle_reset_row(chunk)

    def test__handle_row_contents(self):
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable.row_data import Cell

        partial_row_data = self._makeOne(None)
        cell1_pb = data_pb2.Cell(timestamp_micros=1, value=b'val1')
        cell2_pb = data_pb2.Cell(timestamp_micros=200, value=b'val2')
        cell3_pb = data_pb2.Cell(timestamp_micros=300000, value=b'val3')
        col1 = b'col1'
        col2 = b'col2'
        columns = [
            data_pb2.Column(qualifier=col1, cells=[cell1_pb, cell2_pb]),
            data_pb2.Column(qualifier=col2, cells=[cell3_pb]),
        ]
        family_name = u'name'
        row_contents = data_pb2.Family(name=family_name, columns=columns)
        chunk = messages_pb2.ReadRowsResponse.Chunk(row_contents=row_contents)

        self.assertEqual(partial_row_data.cells, {})
        partial_row_data._handle_row_contents(chunk)
        expected_cells = {
            family_name: {
                col1: [Cell.from_pb(cell1_pb), Cell.from_pb(cell2_pb)],
                col2: [Cell.from_pb(cell3_pb)],
            }
        }
        self.assertEqual(partial_row_data.cells, expected_cells)

    def test_update_from_read_rows(self):
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)

        row_key = b'row-key'
        partial_row_data = self._makeOne(row_key)

        # Set-up chunk1, some data that will be reset by chunk2.
        ignored_family_name = u'ignore-name'
        row_contents = data_pb2.Family(name=ignored_family_name)
        chunk1 = messages_pb2.ReadRowsResponse.Chunk(row_contents=row_contents)

        # Set-up chunk2, a reset row.
        chunk2 = messages_pb2.ReadRowsResponse.Chunk(reset_row=True)

        # Set-up chunk3, a column family with no columns.
        family_name = u'name'
        row_contents = data_pb2.Family(name=family_name)
        chunk3 = messages_pb2.ReadRowsResponse.Chunk(row_contents=row_contents)

        # Set-up chunk4, a commit row.
        chunk4 = messages_pb2.ReadRowsResponse.Chunk(commit_row=True)

        # Prepare request and make sure PartialRowData is empty before.
        read_rows_response_pb = messages_pb2.ReadRowsResponse(
            row_key=row_key, chunks=[chunk1, chunk2, chunk3, chunk4])
        self.assertEqual(partial_row_data.cells, {})
        self.assertFalse(partial_row_data.committed)
        self.assertFalse(partial_row_data._chunks_encountered)

        # Parse the response and make sure the cells took place.
        partial_row_data.update_from_read_rows(read_rows_response_pb)
        self.assertEqual(partial_row_data.cells, {family_name: {}})
        self.assertFalse(ignored_family_name in partial_row_data.cells)
        self.assertTrue(partial_row_data.committed)
        self.assertTrue(partial_row_data._chunks_encountered)

    def test_update_from_read_rows_while_committed(self):
        partial_row_data = self._makeOne(None)
        partial_row_data._committed = True
        self.assertFalse(partial_row_data._chunks_encountered)

        with self.assertRaises(ValueError):
            partial_row_data.update_from_read_rows(None)

        self.assertFalse(partial_row_data._chunks_encountered)

    def test_update_from_read_rows_row_key_disagree(self):
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)

        row_key1 = b'row-key1'
        row_key2 = b'row-key2'
        partial_row_data = self._makeOne(row_key1)
        self.assertFalse(partial_row_data._chunks_encountered)

        self.assertNotEqual(row_key1, row_key2)
        read_rows_response_pb = messages_pb2.ReadRowsResponse(row_key=row_key2)
        with self.assertRaises(ValueError):
            partial_row_data.update_from_read_rows(read_rows_response_pb)

        self.assertFalse(partial_row_data._chunks_encountered)

    def test_update_from_read_rows_empty_chunk(self):
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)

        row_key = b'row-key'
        partial_row_data = self._makeOne(row_key)
        self.assertFalse(partial_row_data._chunks_encountered)

        chunk = messages_pb2.ReadRowsResponse.Chunk()
        read_rows_response_pb = messages_pb2.ReadRowsResponse(
            row_key=row_key, chunks=[chunk])

        # This makes it an "empty" chunk.
        self.assertEqual(chunk.WhichOneof('chunk'), None)
        with self.assertRaises(ValueError):
            partial_row_data.update_from_read_rows(read_rows_response_pb)

        self.assertFalse(partial_row_data._chunks_encountered)


class TestPartialRowsData(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.row_data import PartialRowsData
        return PartialRowsData

    def _getDoNothingClass(self):
        klass = self._getTargetClass()

        class FakePartialRowsData(klass):

            def __init__(self, *args, **kwargs):
                super(FakePartialRowsData, self).__init__(*args, **kwargs)
                self._consumed = []

            def consume_next(self):
                value = self._response_iterator.next()
                self._consumed.append(value)
                return value

        return FakePartialRowsData

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        response_iterator = object()
        partial_rows_data = self._makeOne(response_iterator)
        self.assertTrue(partial_rows_data._response_iterator
                        is response_iterator)
        self.assertEqual(partial_rows_data._rows, {})

    def test___eq__(self):
        response_iterator = object()
        partial_rows_data1 = self._makeOne(response_iterator)
        partial_rows_data2 = self._makeOne(response_iterator)
        self.assertEqual(partial_rows_data1, partial_rows_data2)

    def test___eq__type_differ(self):
        partial_rows_data1 = self._makeOne(None)
        partial_rows_data2 = object()
        self.assertNotEqual(partial_rows_data1, partial_rows_data2)

    def test___ne__same_value(self):
        response_iterator = object()
        partial_rows_data1 = self._makeOne(response_iterator)
        partial_rows_data2 = self._makeOne(response_iterator)
        comparison_val = (partial_rows_data1 != partial_rows_data2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        response_iterator1 = object()
        partial_rows_data1 = self._makeOne(response_iterator1)
        response_iterator2 = object()
        partial_rows_data2 = self._makeOne(response_iterator2)
        self.assertNotEqual(partial_rows_data1, partial_rows_data2)

    def test_rows_getter(self):
        partial_rows_data = self._makeOne(None)
        partial_rows_data._rows = value = object()
        self.assertTrue(partial_rows_data.rows is value)

    def test_cancel(self):
        response_iterator = _MockCancellableIterator()
        partial_rows_data = self._makeOne(response_iterator)
        self.assertEqual(response_iterator.cancel_calls, 0)
        partial_rows_data.cancel()
        self.assertEqual(response_iterator.cancel_calls, 1)

    def test_consume_next(self):
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable.row_data import PartialRowData

        row_key = b'row-key'
        value_pb = messages_pb2.ReadRowsResponse(row_key=row_key)
        response_iterator = _MockCancellableIterator(value_pb)
        partial_rows_data = self._makeOne(response_iterator)
        self.assertEqual(partial_rows_data.rows, {})
        partial_rows_data.consume_next()
        expected_rows = {row_key: PartialRowData(row_key)}
        self.assertEqual(partial_rows_data.rows, expected_rows)

    def test_consume_next_row_exists(self):
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable.row_data import PartialRowData

        row_key = b'row-key'
        chunk = messages_pb2.ReadRowsResponse.Chunk(commit_row=True)
        value_pb = messages_pb2.ReadRowsResponse(row_key=row_key,
                                                 chunks=[chunk])
        response_iterator = _MockCancellableIterator(value_pb)
        partial_rows_data = self._makeOne(response_iterator)
        existing_values = PartialRowData(row_key)
        partial_rows_data._rows[row_key] = existing_values
        self.assertFalse(existing_values.committed)
        partial_rows_data.consume_next()
        self.assertTrue(existing_values.committed)
        self.assertEqual(existing_values.cells, {})

    def test_consume_next_empty_iter(self):
        response_iterator = _MockCancellableIterator()
        partial_rows_data = self._makeOne(response_iterator)
        with self.assertRaises(StopIteration):
            partial_rows_data.consume_next()

    def test_consume_all(self):
        klass = self._getDoNothingClass()

        value1, value2, value3 = object(), object(), object()
        response_iterator = _MockCancellableIterator(value1, value2, value3)
        partial_rows_data = klass(response_iterator)
        self.assertEqual(partial_rows_data._consumed, [])
        partial_rows_data.consume_all()
        self.assertEqual(partial_rows_data._consumed, [value1, value2, value3])

    def test_consume_all_with_max_loops(self):
        klass = self._getDoNothingClass()

        value1, value2, value3 = object(), object(), object()
        response_iterator = _MockCancellableIterator(value1, value2, value3)
        partial_rows_data = klass(response_iterator)
        self.assertEqual(partial_rows_data._consumed, [])
        partial_rows_data.consume_all(max_loops=1)
        self.assertEqual(partial_rows_data._consumed, [value1])
        # Make sure the iterator still has the remaining values.
        self.assertEqual(list(response_iterator.iter_values), [value2, value3])


class _MockCancellableIterator(object):

    cancel_calls = 0

    def __init__(self, *values):
        self.iter_values = iter(values)

    def cancel(self):
        self.cancel_calls += 1

    def next(self):
        return next(self.iter_values)
