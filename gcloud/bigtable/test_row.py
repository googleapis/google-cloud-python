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


import unittest2


class Test_SetDeleteRow(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.row import _SetDeleteRow
        return _SetDeleteRow

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test__get_mutations_virtual(self):
        row = self._makeOne(b'row-key', None)
        with self.assertRaises(NotImplementedError):
            row._get_mutations(None)


class TestDirectRow(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.row import DirectRow
        return DirectRow

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        row_key = b'row_key'
        table = object()

        row = self._makeOne(row_key, table)
        self.assertEqual(row._row_key, row_key)
        self.assertTrue(row._table is table)
        self.assertEqual(row._pb_mutations, [])

    def test_constructor_with_unicode(self):
        row_key = u'row_key'
        row_key_bytes = b'row_key'
        table = object()

        row = self._makeOne(row_key, table)
        self.assertEqual(row._row_key, row_key_bytes)
        self.assertTrue(row._table is table)

    def test_constructor_with_non_bytes(self):
        row_key = object()
        with self.assertRaises(TypeError):
            self._makeOne(row_key, None)

    def test__get_mutations(self):
        row_key = b'row_key'
        row = self._makeOne(row_key, None)

        row._pb_mutations = mutations = object()
        self.assertTrue(mutations is row._get_mutations(None))

    def _set_cell_helper(self, column=None, column_bytes=None,
                         value=b'foobar', timestamp=None,
                         timestamp_micros=-1):
        import six
        import struct
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        row_key = b'row_key'
        column_family_id = u'column_family_id'
        if column is None:
            column = b'column'
        table = object()
        row = self._makeOne(row_key, table)
        self.assertEqual(row._pb_mutations, [])
        row.set_cell(column_family_id, column,
                     value, timestamp=timestamp)

        if isinstance(value, six.integer_types):
            value = struct.pack('>q', value)
        expected_pb = data_pb2.Mutation(
            set_cell=data_pb2.Mutation.SetCell(
                family_name=column_family_id,
                column_qualifier=column_bytes or column,
                timestamp_micros=timestamp_micros,
                value=value,
            ),
        )
        self.assertEqual(row._pb_mutations, [expected_pb])

    def test_set_cell(self):
        self._set_cell_helper()

    def test_set_cell_with_string_column(self):
        column_bytes = b'column'
        column_non_bytes = u'column'
        self._set_cell_helper(column=column_non_bytes,
                              column_bytes=column_bytes)

    def test_set_cell_with_integer_value(self):
        value = 1337
        self._set_cell_helper(value=value)

    def test_set_cell_with_non_bytes_value(self):
        row_key = b'row_key'
        column = b'column'
        column_family_id = u'column_family_id'
        table = object()

        row = self._makeOne(row_key, table)
        value = object()  # Not bytes
        with self.assertRaises(TypeError):
            row.set_cell(column_family_id, column, value)

    def test_set_cell_with_non_null_timestamp(self):
        import datetime
        from gcloud._helpers import _EPOCH

        microseconds = 898294371
        millis_granularity = microseconds - (microseconds % 1000)
        timestamp = _EPOCH + datetime.timedelta(microseconds=microseconds)
        self._set_cell_helper(timestamp=timestamp,
                              timestamp_micros=millis_granularity)

    def test_delete(self):
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        row_key = b'row_key'
        row = self._makeOne(row_key, object())
        self.assertEqual(row._pb_mutations, [])
        row.delete()

        expected_pb = data_pb2.Mutation(
            delete_from_row=data_pb2.Mutation.DeleteFromRow(),
        )
        self.assertEqual(row._pb_mutations, [expected_pb])

    def test_delete_cell(self):
        klass = self._getTargetClass()

        class MockRow(klass):

            def __init__(self, *args, **kwargs):
                super(MockRow, self).__init__(*args, **kwargs)
                self._args = []
                self._kwargs = []

            # Replace the called method with one that logs arguments.
            def _delete_cells(self, *args, **kwargs):
                self._args.append(args)
                self._kwargs.append(kwargs)

        row_key = b'row_key'
        column = b'column'
        column_family_id = u'column_family_id'
        table = object()

        mock_row = MockRow(row_key, table)
        # Make sure no values are set before calling the method.
        self.assertEqual(mock_row._pb_mutations, [])
        self.assertEqual(mock_row._args, [])
        self.assertEqual(mock_row._kwargs, [])

        # Actually make the request against the mock class.
        time_range = object()
        mock_row.delete_cell(column_family_id, column, time_range=time_range)
        self.assertEqual(mock_row._pb_mutations, [])
        self.assertEqual(mock_row._args, [(column_family_id, [column])])
        self.assertEqual(mock_row._kwargs, [{
            'state': None,
            'time_range': time_range,
        }])

    def test_delete_cells_non_iterable(self):
        row_key = b'row_key'
        column_family_id = u'column_family_id'
        table = object()

        row = self._makeOne(row_key, table)
        columns = object()  # Not iterable
        with self.assertRaises(TypeError):
            row.delete_cells(column_family_id, columns)

    def test_delete_cells_all_columns(self):
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        row_key = b'row_key'
        column_family_id = u'column_family_id'
        table = object()

        row = self._makeOne(row_key, table)
        klass = self._getTargetClass()
        self.assertEqual(row._pb_mutations, [])
        row.delete_cells(column_family_id, klass.ALL_COLUMNS)

        expected_pb = data_pb2.Mutation(
            delete_from_family=data_pb2.Mutation.DeleteFromFamily(
                family_name=column_family_id,
            ),
        )
        self.assertEqual(row._pb_mutations, [expected_pb])

    def test_delete_cells_no_columns(self):
        row_key = b'row_key'
        column_family_id = u'column_family_id'
        table = object()

        row = self._makeOne(row_key, table)
        columns = []
        self.assertEqual(row._pb_mutations, [])
        row.delete_cells(column_family_id, columns)
        self.assertEqual(row._pb_mutations, [])

    def _delete_cells_helper(self, time_range=None):
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        row_key = b'row_key'
        column = b'column'
        column_family_id = u'column_family_id'
        table = object()

        row = self._makeOne(row_key, table)
        columns = [column]
        self.assertEqual(row._pb_mutations, [])
        row.delete_cells(column_family_id, columns, time_range=time_range)

        expected_pb = data_pb2.Mutation(
            delete_from_column=data_pb2.Mutation.DeleteFromColumn(
                family_name=column_family_id,
                column_qualifier=column,
            ),
        )
        if time_range is not None:
            expected_pb.delete_from_column.time_range.CopyFrom(
                time_range.to_pb())
        self.assertEqual(row._pb_mutations, [expected_pb])

    def test_delete_cells_no_time_range(self):
        self._delete_cells_helper()

    def test_delete_cells_with_time_range(self):
        import datetime
        from gcloud._helpers import _EPOCH
        from gcloud.bigtable.row_filters import TimestampRange

        microseconds = 30871000  # Makes sure already milliseconds granularity
        start = _EPOCH + datetime.timedelta(microseconds=microseconds)
        time_range = TimestampRange(start=start)
        self._delete_cells_helper(time_range=time_range)

    def test_delete_cells_with_bad_column(self):
        # This makes sure a failure on one of the columns doesn't leave
        # the row's mutations in a bad state.
        row_key = b'row_key'
        column = b'column'
        column_family_id = u'column_family_id'
        table = object()

        row = self._makeOne(row_key, table)
        columns = [column, object()]
        self.assertEqual(row._pb_mutations, [])
        with self.assertRaises(TypeError):
            row.delete_cells(column_family_id, columns)
        self.assertEqual(row._pb_mutations, [])

    def test_delete_cells_with_string_columns(self):
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        row_key = b'row_key'
        column_family_id = u'column_family_id'
        column1 = u'column1'
        column1_bytes = b'column1'
        column2 = u'column2'
        column2_bytes = b'column2'
        table = object()

        row = self._makeOne(row_key, table)
        columns = [column1, column2]
        self.assertEqual(row._pb_mutations, [])
        row.delete_cells(column_family_id, columns)

        expected_pb1 = data_pb2.Mutation(
            delete_from_column=data_pb2.Mutation.DeleteFromColumn(
                family_name=column_family_id,
                column_qualifier=column1_bytes,
            ),
        )
        expected_pb2 = data_pb2.Mutation(
            delete_from_column=data_pb2.Mutation.DeleteFromColumn(
                family_name=column_family_id,
                column_qualifier=column2_bytes,
            ),
        )
        self.assertEqual(row._pb_mutations, [expected_pb1, expected_pb2])

    def test_commit(self):
        from google.protobuf import empty_pb2
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub

        row_key = b'row_key'
        table_name = 'projects/more-stuff'
        column_family_id = u'column_family_id'
        column = b'column'
        timeout_seconds = 711
        client = _Client(timeout_seconds=timeout_seconds)
        table = _Table(table_name, client=client)
        row = self._makeOne(row_key, table)

        # Create request_pb
        value = b'bytes-value'
        mutation = data_pb2.Mutation(
            set_cell=data_pb2.Mutation.SetCell(
                family_name=column_family_id,
                column_qualifier=column,
                timestamp_micros=-1,  # Default value.
                value=value,
            ),
        )
        request_pb = messages_pb2.MutateRowRequest(
            table_name=table_name,
            row_key=row_key,
            mutations=[mutation],
        )

        # Create response_pb
        response_pb = empty_pb2.Empty()

        # Patch the stub used by the API method.
        client._data_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # commit() has no return value when no filter.

        # Perform the method and check the result.
        row.set_cell(column_family_id, column, value)
        result = row.commit()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'MutateRow',
            (request_pb, timeout_seconds),
            {},
        )])
        self.assertEqual(row._pb_mutations, [])

    def test_commit_too_many_mutations(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import row as MUT

        row_key = b'row_key'
        table = object()
        row = self._makeOne(row_key, table)
        row._pb_mutations = [1, 2, 3]
        num_mutations = len(row._pb_mutations)
        with _Monkey(MUT, MAX_MUTATIONS=num_mutations - 1):
            with self.assertRaises(ValueError):
                row.commit()

    def test_commit_no_mutations(self):
        from gcloud.bigtable._testing import _FakeStub

        row_key = b'row_key'
        client = _Client()
        table = _Table(None, client=client)
        row = self._makeOne(row_key, table)
        self.assertEqual(row._pb_mutations, [])

        # Patch the stub used by the API method.
        client._data_stub = stub = _FakeStub()

        # Perform the method and check the result.
        result = row.commit()
        self.assertEqual(result, None)
        # Make sure no request was sent.
        self.assertEqual(stub.method_calls, [])


class TestConditionalRow(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.row import ConditionalRow
        return ConditionalRow

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        row_key = b'row_key'
        table = object()
        filter_ = object()

        row = self._makeOne(row_key, table, filter_=filter_)
        self.assertEqual(row._row_key, row_key)
        self.assertTrue(row._table is table)
        self.assertTrue(row._filter is filter_)
        self.assertEqual(row._true_pb_mutations, [])
        self.assertEqual(row._false_pb_mutations, [])

    def test__get_mutations(self):
        row_key = b'row_key'
        filter_ = object()
        row = self._makeOne(row_key, None, filter_=filter_)

        row._true_pb_mutations = true_mutations = object()
        row._false_pb_mutations = false_mutations = object()
        self.assertTrue(true_mutations is row._get_mutations(True))
        self.assertTrue(false_mutations is row._get_mutations(False))
        self.assertTrue(false_mutations is row._get_mutations(None))

    def test_commit(self):
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable.row_filters import RowSampleFilter

        row_key = b'row_key'
        table_name = 'projects/more-stuff'
        column_family_id1 = u'column_family_id1'
        column_family_id2 = u'column_family_id2'
        column_family_id3 = u'column_family_id3'
        column1 = b'column1'
        column2 = b'column2'
        timeout_seconds = 262
        client = _Client(timeout_seconds=timeout_seconds)
        table = _Table(table_name, client=client)
        row_filter = RowSampleFilter(0.33)
        row = self._makeOne(row_key, table, filter_=row_filter)

        # Create request_pb
        value1 = b'bytes-value'
        mutation1 = data_pb2.Mutation(
            set_cell=data_pb2.Mutation.SetCell(
                family_name=column_family_id1,
                column_qualifier=column1,
                timestamp_micros=-1,  # Default value.
                value=value1,
            ),
        )
        mutation2 = data_pb2.Mutation(
            delete_from_row=data_pb2.Mutation.DeleteFromRow(),
        )
        mutation3 = data_pb2.Mutation(
            delete_from_column=data_pb2.Mutation.DeleteFromColumn(
                family_name=column_family_id2,
                column_qualifier=column2,
            ),
        )
        mutation4 = data_pb2.Mutation(
            delete_from_family=data_pb2.Mutation.DeleteFromFamily(
                family_name=column_family_id3,
            ),
        )
        request_pb = messages_pb2.CheckAndMutateRowRequest(
            table_name=table_name,
            row_key=row_key,
            predicate_filter=row_filter.to_pb(),
            true_mutations=[mutation1, mutation3, mutation4],
            false_mutations=[mutation2],
        )

        # Create response_pb
        predicate_matched = True
        response_pb = messages_pb2.CheckAndMutateRowResponse(
            predicate_matched=predicate_matched)

        # Patch the stub used by the API method.
        client._data_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = predicate_matched

        # Perform the method and check the result.
        row.set_cell(column_family_id1, column1, value1, state=True)
        row.delete(state=False)
        row.delete_cell(column_family_id2, column2, state=True)
        row.delete_cells(column_family_id3, row.ALL_COLUMNS, state=True)
        result = row.commit()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'CheckAndMutateRow',
            (request_pb, timeout_seconds),
            {},
        )])
        self.assertEqual(row._true_pb_mutations, [])
        self.assertEqual(row._false_pb_mutations, [])

    def test_commit_too_many_mutations(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import row as MUT

        row_key = b'row_key'
        table = object()
        filter_ = object()
        row = self._makeOne(row_key, table, filter_=filter_)
        row._true_pb_mutations = [1, 2, 3]
        num_mutations = len(row._true_pb_mutations)
        with _Monkey(MUT, MAX_MUTATIONS=num_mutations - 1):
            with self.assertRaises(ValueError):
                row.commit()

    def test_commit_no_mutations(self):
        from gcloud.bigtable._testing import _FakeStub

        row_key = b'row_key'
        client = _Client()
        table = _Table(None, client=client)
        filter_ = object()
        row = self._makeOne(row_key, table, filter_=filter_)
        self.assertEqual(row._true_pb_mutations, [])
        self.assertEqual(row._false_pb_mutations, [])

        # Patch the stub used by the API method.
        client._data_stub = stub = _FakeStub()

        # Perform the method and check the result.
        result = row.commit()
        self.assertEqual(result, None)
        # Make sure no request was sent.
        self.assertEqual(stub.method_calls, [])


class TestAppendRow(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.row import AppendRow
        return AppendRow

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        row_key = b'row_key'
        table = object()

        row = self._makeOne(row_key, table)
        self.assertEqual(row._row_key, row_key)
        self.assertTrue(row._table is table)
        self.assertEqual(row._rule_pb_list, [])

    def test_clear(self):
        row_key = b'row_key'
        table = object()
        row = self._makeOne(row_key, table)
        row._rule_pb_list = [1, 2, 3]
        row.clear()
        self.assertEqual(row._rule_pb_list, [])

    def test_append_cell_value(self):
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        table = object()
        row_key = b'row_key'
        row = self._makeOne(row_key, table)
        self.assertEqual(row._rule_pb_list, [])

        column = b'column'
        column_family_id = u'column_family_id'
        value = b'bytes-val'
        row.append_cell_value(column_family_id, column, value)
        expected_pb = data_pb2.ReadModifyWriteRule(
            family_name=column_family_id, column_qualifier=column,
            append_value=value)
        self.assertEqual(row._rule_pb_list, [expected_pb])

    def test_increment_cell_value(self):
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        table = object()
        row_key = b'row_key'
        row = self._makeOne(row_key, table)
        self.assertEqual(row._rule_pb_list, [])

        column = b'column'
        column_family_id = u'column_family_id'
        int_value = 281330
        row.increment_cell_value(column_family_id, column, int_value)
        expected_pb = data_pb2.ReadModifyWriteRule(
            family_name=column_family_id, column_qualifier=column,
            increment_amount=int_value)
        self.assertEqual(row._rule_pb_list, [expected_pb])

    def test_commit(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable import row as MUT

        row_key = b'row_key'
        table_name = 'projects/more-stuff'
        column_family_id = u'column_family_id'
        column = b'column'
        timeout_seconds = 87
        client = _Client(timeout_seconds=timeout_seconds)
        table = _Table(table_name, client=client)
        row = self._makeOne(row_key, table)

        # Create request_pb
        value = b'bytes-value'
        # We will call row.append_cell_value(COLUMN_FAMILY_ID, COLUMN, value).
        request_pb = messages_pb2.ReadModifyWriteRowRequest(
            table_name=table_name,
            row_key=row_key,
            rules=[
                data_pb2.ReadModifyWriteRule(
                    family_name=column_family_id,
                    column_qualifier=column,
                    append_value=value,
                ),
            ],
        )

        # Create response_pb
        response_pb = object()

        # Patch the stub used by the API method.
        client._data_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        row_responses = []
        expected_result = object()

        def mock_parse_rmw_row_response(row_response):
            row_responses.append(row_response)
            return expected_result

        # Perform the method and check the result.
        with _Monkey(MUT, _parse_rmw_row_response=mock_parse_rmw_row_response):
            row.append_cell_value(column_family_id, column, value)
            result = row.commit()

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'ReadModifyWriteRow',
            (request_pb, timeout_seconds),
            {},
        )])
        self.assertEqual(row_responses, [response_pb])
        self.assertEqual(row._rule_pb_list, [])

    def test_commit_no_rules(self):
        from gcloud.bigtable._testing import _FakeStub

        row_key = b'row_key'
        client = _Client()
        table = _Table(None, client=client)
        row = self._makeOne(row_key, table)
        self.assertEqual(row._rule_pb_list, [])

        # Patch the stub used by the API method.
        client._data_stub = stub = _FakeStub()

        # Perform the method and check the result.
        result = row.commit()
        self.assertEqual(result, {})
        # Make sure no request was sent.
        self.assertEqual(stub.method_calls, [])

    def test_commit_too_many_mutations(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import row as MUT

        row_key = b'row_key'
        table = object()
        row = self._makeOne(row_key, table)
        row._rule_pb_list = [1, 2, 3]
        num_mutations = len(row._rule_pb_list)
        with _Monkey(MUT, MAX_MUTATIONS=num_mutations - 1):
            with self.assertRaises(ValueError):
                row.commit()


class Test__parse_rmw_row_response(unittest2.TestCase):

    def _callFUT(self, row_response):
        from gcloud.bigtable.row import _parse_rmw_row_response
        return _parse_rmw_row_response(row_response)

    def test_it(self):
        from gcloud._helpers import _datetime_from_microseconds
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        col_fam1 = u'col-fam-id'
        col_fam2 = u'col-fam-id2'
        col_name1 = b'col-name1'
        col_name2 = b'col-name2'
        col_name3 = b'col-name3-but-other-fam'
        cell_val1 = b'cell-val'
        cell_val2 = b'cell-val-newer'
        cell_val3 = b'altcol-cell-val'
        cell_val4 = b'foo'

        microseconds = 1000871
        timestamp = _datetime_from_microseconds(microseconds)
        expected_output = {
            col_fam1: {
                col_name1: [
                    (cell_val1, timestamp),
                    (cell_val2, timestamp),
                ],
                col_name2: [
                    (cell_val3, timestamp),
                ],
            },
            col_fam2: {
                col_name3: [
                    (cell_val4, timestamp),
                ],
            },
        }
        sample_input = data_pb2.Row(
            families=[
                data_pb2.Family(
                    name=col_fam1,
                    columns=[
                        data_pb2.Column(
                            qualifier=col_name1,
                            cells=[
                                data_pb2.Cell(
                                    value=cell_val1,
                                    timestamp_micros=microseconds,
                                ),
                                data_pb2.Cell(
                                    value=cell_val2,
                                    timestamp_micros=microseconds,
                                ),
                            ],
                        ),
                        data_pb2.Column(
                            qualifier=col_name2,
                            cells=[
                                data_pb2.Cell(
                                    value=cell_val3,
                                    timestamp_micros=microseconds,
                                ),
                            ],
                        ),
                    ],
                ),
                data_pb2.Family(
                    name=col_fam2,
                    columns=[
                        data_pb2.Column(
                            qualifier=col_name3,
                            cells=[
                                data_pb2.Cell(
                                    value=cell_val4,
                                    timestamp_micros=microseconds,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
        self.assertEqual(expected_output, self._callFUT(sample_input))


class Test__parse_family_pb(unittest2.TestCase):

    def _callFUT(self, family_pb):
        from gcloud.bigtable.row import _parse_family_pb
        return _parse_family_pb(family_pb)

    def test_it(self):
        from gcloud._helpers import _datetime_from_microseconds
        from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2

        col_fam1 = u'col-fam-id'
        col_name1 = b'col-name1'
        col_name2 = b'col-name2'
        cell_val1 = b'cell-val'
        cell_val2 = b'cell-val-newer'
        cell_val3 = b'altcol-cell-val'

        microseconds = 5554441037
        timestamp = _datetime_from_microseconds(microseconds)
        expected_dict = {
            col_name1: [
                (cell_val1, timestamp),
                (cell_val2, timestamp),
            ],
            col_name2: [
                (cell_val3, timestamp),
            ],
        }
        expected_output = (col_fam1, expected_dict)
        sample_input = data_pb2.Family(
            name=col_fam1,
            columns=[
                data_pb2.Column(
                    qualifier=col_name1,
                    cells=[
                        data_pb2.Cell(
                            value=cell_val1,
                            timestamp_micros=microseconds,
                        ),
                        data_pb2.Cell(
                            value=cell_val2,
                            timestamp_micros=microseconds,
                        ),
                    ],
                ),
                data_pb2.Column(
                    qualifier=col_name2,
                    cells=[
                        data_pb2.Cell(
                            value=cell_val3,
                            timestamp_micros=microseconds,
                        ),
                    ],
                ),
            ],
        )
        self.assertEqual(expected_output, self._callFUT(sample_input))


class _Client(object):

    data_stub = None

    def __init__(self, timeout_seconds=None):
        self.timeout_seconds = timeout_seconds


class _Cluster(object):

    def __init__(self, client=None):
        self._client = client


class _Table(object):

    def __init__(self, name, client=None):
        self.name = name
        self._cluster = _Cluster(client)
