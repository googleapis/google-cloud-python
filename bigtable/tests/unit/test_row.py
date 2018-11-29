# Copyright 2015 Google LLC
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


import unittest

import mock

from ._testing import _make_credentials


class TestRow(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row import Row

        return Row

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_row_key_getter(self):
        row = self._make_one(row_key=b"row_key", table="table")
        self.assertEqual(b"row_key", row.row_key)

    def test_row_table_getter(self):
        row = self._make_one(row_key=b"row_key", table="table")
        self.assertEqual("table", row.table)


class Test_SetDeleteRow(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row import _SetDeleteRow

        return _SetDeleteRow

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test__get_mutations_virtual(self):
        row = self._make_one(b"row-key", None)
        with self.assertRaises(NotImplementedError):
            row._get_mutations(None)


class TestDirectRow(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row import DirectRow

        return DirectRow

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _get_target_client_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_client(self, *args, **kwargs):
        return self._get_target_client_class()(*args, **kwargs)

    def test_constructor(self):
        row_key = b"row_key"
        table = object()

        row = self._make_one(row_key, table)
        self.assertEqual(row._row_key, row_key)
        self.assertIs(row._table, table)
        self.assertEqual(row._pb_mutations, [])

    def test_constructor_with_unicode(self):
        row_key = u"row_key"
        row_key_bytes = b"row_key"
        table = object()

        row = self._make_one(row_key, table)
        self.assertEqual(row._row_key, row_key_bytes)
        self.assertIs(row._table, table)

    def test_constructor_with_non_bytes(self):
        row_key = object()
        with self.assertRaises(TypeError):
            self._make_one(row_key, None)

    def test__get_mutations(self):
        row_key = b"row_key"
        row = self._make_one(row_key, None)

        row._pb_mutations = mutations = object()
        self.assertIs(mutations, row._get_mutations(None))

    def test_get_mutations_size(self):
        row_key = b"row_key"
        row = self._make_one(row_key, None)

        column_family_id1 = u"column_family_id1"
        column_family_id2 = u"column_family_id2"
        column1 = b"column1"
        column2 = b"column2"
        number_of_bytes = 1 * 1024 * 1024
        value = b"1" * number_of_bytes

        row.set_cell(column_family_id1, column1, value)
        row.set_cell(column_family_id2, column2, value)

        total_mutations_size = 0
        for mutation in row._get_mutations():
            total_mutations_size += mutation.ByteSize()

        self.assertEqual(row.get_mutations_size(), total_mutations_size)

    def _set_cell_helper(
        self,
        column=None,
        column_bytes=None,
        value=b"foobar",
        timestamp=None,
        timestamp_micros=-1,
    ):
        import six
        import struct

        row_key = b"row_key"
        column_family_id = u"column_family_id"
        if column is None:
            column = b"column"
        table = object()
        row = self._make_one(row_key, table)
        self.assertEqual(row._pb_mutations, [])
        row.set_cell(column_family_id, column, value, timestamp=timestamp)

        if isinstance(value, six.integer_types):
            value = struct.pack(">q", value)
        expected_pb = _MutationPB(
            set_cell=_MutationSetCellPB(
                family_name=column_family_id,
                column_qualifier=column_bytes or column,
                timestamp_micros=timestamp_micros,
                value=value,
            )
        )
        self.assertEqual(row._pb_mutations, [expected_pb])

    def test_set_cell(self):
        self._set_cell_helper()

    def test_set_cell_with_string_column(self):
        column_bytes = b"column"
        column_non_bytes = u"column"
        self._set_cell_helper(column=column_non_bytes, column_bytes=column_bytes)

    def test_set_cell_with_integer_value(self):
        value = 1337
        self._set_cell_helper(value=value)

    def test_set_cell_with_non_bytes_value(self):
        row_key = b"row_key"
        column = b"column"
        column_family_id = u"column_family_id"
        table = object()

        row = self._make_one(row_key, table)
        value = object()  # Not bytes
        with self.assertRaises(TypeError):
            row.set_cell(column_family_id, column, value)

    def test_set_cell_with_non_null_timestamp(self):
        import datetime
        from google.cloud._helpers import _EPOCH

        microseconds = 898294371
        millis_granularity = microseconds - (microseconds % 1000)
        timestamp = _EPOCH + datetime.timedelta(microseconds=microseconds)
        self._set_cell_helper(timestamp=timestamp, timestamp_micros=millis_granularity)

    def test_delete(self):
        row_key = b"row_key"
        row = self._make_one(row_key, object())
        self.assertEqual(row._pb_mutations, [])
        row.delete()

        expected_pb = _MutationPB(delete_from_row=_MutationDeleteFromRowPB())
        self.assertEqual(row._pb_mutations, [expected_pb])

    def test_delete_cell(self):
        klass = self._get_target_class()

        class MockRow(klass):
            def __init__(self, *args, **kwargs):
                super(MockRow, self).__init__(*args, **kwargs)
                self._args = []
                self._kwargs = []

            # Replace the called method with one that logs arguments.
            def _delete_cells(self, *args, **kwargs):
                self._args.append(args)
                self._kwargs.append(kwargs)

        row_key = b"row_key"
        column = b"column"
        column_family_id = u"column_family_id"
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
        self.assertEqual(mock_row._kwargs, [{"state": None, "time_range": time_range}])

    def test_delete_cells_non_iterable(self):
        row_key = b"row_key"
        column_family_id = u"column_family_id"
        table = object()

        row = self._make_one(row_key, table)
        columns = object()  # Not iterable
        with self.assertRaises(TypeError):
            row.delete_cells(column_family_id, columns)

    def test_delete_cells_all_columns(self):
        row_key = b"row_key"
        column_family_id = u"column_family_id"
        table = object()

        row = self._make_one(row_key, table)
        klass = self._get_target_class()
        self.assertEqual(row._pb_mutations, [])
        row.delete_cells(column_family_id, klass.ALL_COLUMNS)

        expected_pb = _MutationPB(
            delete_from_family=_MutationDeleteFromFamilyPB(family_name=column_family_id)
        )
        self.assertEqual(row._pb_mutations, [expected_pb])

    def test_delete_cells_no_columns(self):
        row_key = b"row_key"
        column_family_id = u"column_family_id"
        table = object()

        row = self._make_one(row_key, table)
        columns = []
        self.assertEqual(row._pb_mutations, [])
        row.delete_cells(column_family_id, columns)
        self.assertEqual(row._pb_mutations, [])

    def _delete_cells_helper(self, time_range=None):
        row_key = b"row_key"
        column = b"column"
        column_family_id = u"column_family_id"
        table = object()

        row = self._make_one(row_key, table)
        columns = [column]
        self.assertEqual(row._pb_mutations, [])
        row.delete_cells(column_family_id, columns, time_range=time_range)

        expected_pb = _MutationPB(
            delete_from_column=_MutationDeleteFromColumnPB(
                family_name=column_family_id, column_qualifier=column
            )
        )
        if time_range is not None:
            expected_pb.delete_from_column.time_range.CopyFrom(time_range.to_pb())
        self.assertEqual(row._pb_mutations, [expected_pb])

    def test_delete_cells_no_time_range(self):
        self._delete_cells_helper()

    def test_delete_cells_with_time_range(self):
        import datetime
        from google.cloud._helpers import _EPOCH
        from google.cloud.bigtable.row_filters import TimestampRange

        microseconds = 30871000  # Makes sure already milliseconds granularity
        start = _EPOCH + datetime.timedelta(microseconds=microseconds)
        time_range = TimestampRange(start=start)
        self._delete_cells_helper(time_range=time_range)

    def test_delete_cells_with_bad_column(self):
        # This makes sure a failure on one of the columns doesn't leave
        # the row's mutations in a bad state.
        row_key = b"row_key"
        column = b"column"
        column_family_id = u"column_family_id"
        table = object()

        row = self._make_one(row_key, table)
        columns = [column, object()]
        self.assertEqual(row._pb_mutations, [])
        with self.assertRaises(TypeError):
            row.delete_cells(column_family_id, columns)
        self.assertEqual(row._pb_mutations, [])

    def test_delete_cells_with_string_columns(self):
        row_key = b"row_key"
        column_family_id = u"column_family_id"
        column1 = u"column1"
        column1_bytes = b"column1"
        column2 = u"column2"
        column2_bytes = b"column2"
        table = object()

        row = self._make_one(row_key, table)
        columns = [column1, column2]
        self.assertEqual(row._pb_mutations, [])
        row.delete_cells(column_family_id, columns)

        expected_pb1 = _MutationPB(
            delete_from_column=_MutationDeleteFromColumnPB(
                family_name=column_family_id, column_qualifier=column1_bytes
            )
        )
        expected_pb2 = _MutationPB(
            delete_from_column=_MutationDeleteFromColumnPB(
                family_name=column_family_id, column_qualifier=column2_bytes
            )
        )
        self.assertEqual(row._pb_mutations, [expected_pb1, expected_pb2])

    def test_commit(self):
        project_id = "project-id"
        row_key = b"row_key"
        table_name = "projects/more-stuff"
        column_family_id = u"column_family_id"
        column = b"column"

        credentials = _make_credentials()
        client = self._make_client(
            project=project_id, credentials=credentials, admin=True
        )
        table = _Table(table_name, client=client)
        row = self._make_one(row_key, table)
        value = b"bytes-value"

        # Perform the method and check the result.
        row.set_cell(column_family_id, column, value)
        row.commit()
        self.assertEqual(table.mutated_rows, [row])


class TestConditionalRow(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row import ConditionalRow

        return ConditionalRow

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _get_target_client_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_client(self, *args, **kwargs):
        return self._get_target_client_class()(*args, **kwargs)

    def test_constructor(self):
        row_key = b"row_key"
        table = object()
        filter_ = object()

        row = self._make_one(row_key, table, filter_=filter_)
        self.assertEqual(row._row_key, row_key)
        self.assertIs(row._table, table)
        self.assertIs(row._filter, filter_)
        self.assertEqual(row._true_pb_mutations, [])
        self.assertEqual(row._false_pb_mutations, [])

    def test__get_mutations(self):
        row_key = b"row_key"
        filter_ = object()
        row = self._make_one(row_key, None, filter_=filter_)

        row._true_pb_mutations = true_mutations = object()
        row._false_pb_mutations = false_mutations = object()
        self.assertIs(true_mutations, row._get_mutations(True))
        self.assertIs(false_mutations, row._get_mutations(False))
        self.assertIs(false_mutations, row._get_mutations(None))

    def test_commit(self):
        from google.cloud.bigtable.row_filters import RowSampleFilter
        from google.cloud.bigtable_v2.gapic import bigtable_client

        project_id = "project-id"
        row_key = b"row_key"
        table_name = "projects/more-stuff"
        column_family_id1 = u"column_family_id1"
        column_family_id2 = u"column_family_id2"
        column_family_id3 = u"column_family_id3"
        column1 = b"column1"
        column2 = b"column2"

        api = bigtable_client.BigtableClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project=project_id, credentials=credentials, admin=True
        )
        table = _Table(table_name, client=client)
        row_filter = RowSampleFilter(0.33)
        row = self._make_one(row_key, table, filter_=row_filter)

        # Create request_pb
        value1 = b"bytes-value"

        # Create response_pb
        predicate_matched = True
        response_pb = _CheckAndMutateRowResponsePB(predicate_matched=predicate_matched)

        # Patch the stub used by the API method.
        api.transport.check_and_mutate_row.side_effect = [response_pb]
        client._table_data_client = api

        # Create expected_result.
        expected_result = predicate_matched

        # Perform the method and check the result.
        row.set_cell(column_family_id1, column1, value1, state=True)
        row.delete(state=False)
        row.delete_cell(column_family_id2, column2, state=True)
        row.delete_cells(column_family_id3, row.ALL_COLUMNS, state=True)
        result = row.commit()
        self.assertEqual(result, expected_result)
        self.assertEqual(row._true_pb_mutations, [])
        self.assertEqual(row._false_pb_mutations, [])

    def test_commit_too_many_mutations(self):
        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import row as MUT

        row_key = b"row_key"
        table = object()
        filter_ = object()
        row = self._make_one(row_key, table, filter_=filter_)
        row._true_pb_mutations = [1, 2, 3]
        num_mutations = len(row._true_pb_mutations)
        with _Monkey(MUT, MAX_MUTATIONS=num_mutations - 1):
            with self.assertRaises(ValueError):
                row.commit()

    def test_commit_no_mutations(self):
        from tests.unit._testing import _FakeStub

        project_id = "project-id"
        row_key = b"row_key"

        credentials = _make_credentials()
        client = self._make_client(
            project=project_id, credentials=credentials, admin=True
        )
        table = _Table(None, client=client)
        filter_ = object()
        row = self._make_one(row_key, table, filter_=filter_)
        self.assertEqual(row._true_pb_mutations, [])
        self.assertEqual(row._false_pb_mutations, [])

        # Patch the stub used by the API method.
        stub = _FakeStub()

        # Perform the method and check the result.
        result = row.commit()
        self.assertIsNone(result)
        # Make sure no request was sent.
        self.assertEqual(stub.method_calls, [])


class TestAppendRow(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.row import AppendRow

        return AppendRow

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _get_target_client_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_client(self, *args, **kwargs):
        return self._get_target_client_class()(*args, **kwargs)

    def test_constructor(self):
        row_key = b"row_key"
        table = object()

        row = self._make_one(row_key, table)
        self.assertEqual(row._row_key, row_key)
        self.assertIs(row._table, table)
        self.assertEqual(row._rule_pb_list, [])

    def test_clear(self):
        row_key = b"row_key"
        table = object()
        row = self._make_one(row_key, table)
        row._rule_pb_list = [1, 2, 3]
        row.clear()
        self.assertEqual(row._rule_pb_list, [])

    def test_append_cell_value(self):
        table = object()
        row_key = b"row_key"
        row = self._make_one(row_key, table)
        self.assertEqual(row._rule_pb_list, [])

        column = b"column"
        column_family_id = u"column_family_id"
        value = b"bytes-val"
        row.append_cell_value(column_family_id, column, value)
        expected_pb = _ReadModifyWriteRulePB(
            family_name=column_family_id, column_qualifier=column, append_value=value
        )
        self.assertEqual(row._rule_pb_list, [expected_pb])

    def test_increment_cell_value(self):
        table = object()
        row_key = b"row_key"
        row = self._make_one(row_key, table)
        self.assertEqual(row._rule_pb_list, [])

        column = b"column"
        column_family_id = u"column_family_id"
        int_value = 281330
        row.increment_cell_value(column_family_id, column, int_value)
        expected_pb = _ReadModifyWriteRulePB(
            family_name=column_family_id,
            column_qualifier=column,
            increment_amount=int_value,
        )
        self.assertEqual(row._rule_pb_list, [expected_pb])

    def test_commit(self):
        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import row as MUT
        from google.cloud.bigtable_v2.gapic import bigtable_client

        project_id = "project-id"
        row_key = b"row_key"
        table_name = "projects/more-stuff"
        column_family_id = u"column_family_id"
        column = b"column"

        api = bigtable_client.BigtableClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project=project_id, credentials=credentials, admin=True
        )
        table = _Table(table_name, client=client)
        row = self._make_one(row_key, table)

        # Create request_pb
        value = b"bytes-value"

        # Create expected_result.
        row_responses = []
        expected_result = object()

        # Patch API calls
        client._table_data_client = api

        def mock_parse_rmw_row_response(row_response):
            row_responses.append(row_response)
            return expected_result

        # Perform the method and check the result.
        with _Monkey(MUT, _parse_rmw_row_response=mock_parse_rmw_row_response):
            row.append_cell_value(column_family_id, column, value)
            result = row.commit()

        self.assertEqual(result, expected_result)
        self.assertEqual(row._rule_pb_list, [])

    def test_commit_no_rules(self):
        from tests.unit._testing import _FakeStub

        project_id = "project-id"
        row_key = b"row_key"

        credentials = _make_credentials()
        client = self._make_client(
            project=project_id, credentials=credentials, admin=True
        )
        table = _Table(None, client=client)
        row = self._make_one(row_key, table)
        self.assertEqual(row._rule_pb_list, [])

        # Patch the stub used by the API method.
        stub = _FakeStub()

        # Perform the method and check the result.
        result = row.commit()
        self.assertEqual(result, {})
        # Make sure no request was sent.
        self.assertEqual(stub.method_calls, [])

    def test_commit_too_many_mutations(self):
        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import row as MUT

        row_key = b"row_key"
        table = object()
        row = self._make_one(row_key, table)
        row._rule_pb_list = [1, 2, 3]
        num_mutations = len(row._rule_pb_list)
        with _Monkey(MUT, MAX_MUTATIONS=num_mutations - 1):
            with self.assertRaises(ValueError):
                row.commit()


class Test__parse_rmw_row_response(unittest.TestCase):
    def _call_fut(self, row_response):
        from google.cloud.bigtable.row import _parse_rmw_row_response

        return _parse_rmw_row_response(row_response)

    def test_it(self):
        from google.cloud._helpers import _datetime_from_microseconds

        col_fam1 = u"col-fam-id"
        col_fam2 = u"col-fam-id2"
        col_name1 = b"col-name1"
        col_name2 = b"col-name2"
        col_name3 = b"col-name3-but-other-fam"
        cell_val1 = b"cell-val"
        cell_val2 = b"cell-val-newer"
        cell_val3 = b"altcol-cell-val"
        cell_val4 = b"foo"

        microseconds = 1000871
        timestamp = _datetime_from_microseconds(microseconds)
        expected_output = {
            col_fam1: {
                col_name1: [(cell_val1, timestamp), (cell_val2, timestamp)],
                col_name2: [(cell_val3, timestamp)],
            },
            col_fam2: {col_name3: [(cell_val4, timestamp)]},
        }
        response_row = _RowPB(
            families=[
                _FamilyPB(
                    name=col_fam1,
                    columns=[
                        _ColumnPB(
                            qualifier=col_name1,
                            cells=[
                                _CellPB(value=cell_val1, timestamp_micros=microseconds),
                                _CellPB(value=cell_val2, timestamp_micros=microseconds),
                            ],
                        ),
                        _ColumnPB(
                            qualifier=col_name2,
                            cells=[
                                _CellPB(value=cell_val3, timestamp_micros=microseconds)
                            ],
                        ),
                    ],
                ),
                _FamilyPB(
                    name=col_fam2,
                    columns=[
                        _ColumnPB(
                            qualifier=col_name3,
                            cells=[
                                _CellPB(value=cell_val4, timestamp_micros=microseconds)
                            ],
                        )
                    ],
                ),
            ]
        )
        sample_input = _ReadModifyWriteRowResponsePB(row=response_row)
        self.assertEqual(expected_output, self._call_fut(sample_input))


class Test__parse_family_pb(unittest.TestCase):
    def _call_fut(self, family_pb):
        from google.cloud.bigtable.row import _parse_family_pb

        return _parse_family_pb(family_pb)

    def test_it(self):
        from google.cloud._helpers import _datetime_from_microseconds

        col_fam1 = u"col-fam-id"
        col_name1 = b"col-name1"
        col_name2 = b"col-name2"
        cell_val1 = b"cell-val"
        cell_val2 = b"cell-val-newer"
        cell_val3 = b"altcol-cell-val"

        microseconds = 5554441037
        timestamp = _datetime_from_microseconds(microseconds)
        expected_dict = {
            col_name1: [(cell_val1, timestamp), (cell_val2, timestamp)],
            col_name2: [(cell_val3, timestamp)],
        }
        expected_output = (col_fam1, expected_dict)
        sample_input = _FamilyPB(
            name=col_fam1,
            columns=[
                _ColumnPB(
                    qualifier=col_name1,
                    cells=[
                        _CellPB(value=cell_val1, timestamp_micros=microseconds),
                        _CellPB(value=cell_val2, timestamp_micros=microseconds),
                    ],
                ),
                _ColumnPB(
                    qualifier=col_name2,
                    cells=[_CellPB(value=cell_val3, timestamp_micros=microseconds)],
                ),
            ],
        )
        self.assertEqual(expected_output, self._call_fut(sample_input))


def _CheckAndMutateRowResponsePB(*args, **kw):
    from google.cloud.bigtable_v2.proto import bigtable_pb2 as messages_v2_pb2

    return messages_v2_pb2.CheckAndMutateRowResponse(*args, **kw)


def _ReadModifyWriteRowResponsePB(*args, **kw):
    from google.cloud.bigtable_v2.proto import bigtable_pb2 as messages_v2_pb2

    return messages_v2_pb2.ReadModifyWriteRowResponse(*args, **kw)


def _CellPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import data_pb2 as data_v2_pb2

    return data_v2_pb2.Cell(*args, **kw)


def _ColumnPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import data_pb2 as data_v2_pb2

    return data_v2_pb2.Column(*args, **kw)


def _FamilyPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import data_pb2 as data_v2_pb2

    return data_v2_pb2.Family(*args, **kw)


def _MutationPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import data_pb2 as data_v2_pb2

    return data_v2_pb2.Mutation(*args, **kw)


def _MutationSetCellPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import data_pb2 as data_v2_pb2

    return data_v2_pb2.Mutation.SetCell(*args, **kw)


def _MutationDeleteFromColumnPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import data_pb2 as data_v2_pb2

    return data_v2_pb2.Mutation.DeleteFromColumn(*args, **kw)


def _MutationDeleteFromFamilyPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import data_pb2 as data_v2_pb2

    return data_v2_pb2.Mutation.DeleteFromFamily(*args, **kw)


def _MutationDeleteFromRowPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import data_pb2 as data_v2_pb2

    return data_v2_pb2.Mutation.DeleteFromRow(*args, **kw)


def _RowPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import data_pb2 as data_v2_pb2

    return data_v2_pb2.Row(*args, **kw)


def _ReadModifyWriteRulePB(*args, **kw):
    from google.cloud.bigtable_v2.proto import data_pb2 as data_v2_pb2

    return data_v2_pb2.ReadModifyWriteRule(*args, **kw)


class _Instance(object):
    def __init__(self, client=None):
        self._client = client


class _Table(object):
    def __init__(self, name, client=None):
        self.name = name
        self._instance = _Instance(client)
        self.client = client
        self.mutated_rows = []

    def mutate_rows(self, rows):
        self.mutated_rows.extend(rows)
