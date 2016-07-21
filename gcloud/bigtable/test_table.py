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


class TestTable(unittest2.TestCase):

    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = ('projects/' + PROJECT_ID + '/instances/' + INSTANCE_ID)
    TABLE_ID = 'table-id'
    TABLE_NAME = INSTANCE_NAME + '/tables/' + TABLE_ID
    TIMEOUT_SECONDS = 1333
    ROW_KEY = b'row-key'
    FAMILY_NAME = u'family'
    QUALIFIER = b'qualifier'
    TIMESTAMP_MICROS = 100
    VALUE = b'value'

    def _getTargetClass(self):
        from gcloud.bigtable.table import Table
        return Table

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        table_id = 'table-id'
        instance = object()

        table = self._makeOne(table_id, instance)
        self.assertEqual(table.table_id, table_id)
        self.assertTrue(table._instance is instance)

    def test_name_property(self):
        table_id = 'table-id'
        instance_name = 'instance_name'

        instance = _Instance(instance_name)
        table = self._makeOne(table_id, instance)
        expected_name = instance_name + '/tables/' + table_id
        self.assertEqual(table.name, expected_name)

    def test_column_family_factory(self):
        from gcloud.bigtable.column_family import ColumnFamily

        table_id = 'table-id'
        gc_rule = object()
        table = self._makeOne(table_id, None)
        column_family_id = 'column_family_id'
        column_family = table.column_family(column_family_id, gc_rule=gc_rule)

        self.assertTrue(isinstance(column_family, ColumnFamily))
        self.assertEqual(column_family.column_family_id, column_family_id)
        self.assertTrue(column_family.gc_rule is gc_rule)
        self.assertEqual(column_family._table, table)

    def test_row_factory_direct(self):
        from gcloud.bigtable.row import DirectRow

        table_id = 'table-id'
        table = self._makeOne(table_id, None)
        row_key = b'row_key'
        row = table.row(row_key)

        self.assertTrue(isinstance(row, DirectRow))
        self.assertEqual(row._row_key, row_key)
        self.assertEqual(row._table, table)

    def test_row_factory_conditional(self):
        from gcloud.bigtable.row import ConditionalRow

        table_id = 'table-id'
        table = self._makeOne(table_id, None)
        row_key = b'row_key'
        filter_ = object()
        row = table.row(row_key, filter_=filter_)

        self.assertTrue(isinstance(row, ConditionalRow))
        self.assertEqual(row._row_key, row_key)
        self.assertEqual(row._table, table)

    def test_row_factory_append(self):
        from gcloud.bigtable.row import AppendRow

        table_id = 'table-id'
        table = self._makeOne(table_id, None)
        row_key = b'row_key'
        row = table.row(row_key, append=True)

        self.assertTrue(isinstance(row, AppendRow))
        self.assertEqual(row._row_key, row_key)
        self.assertEqual(row._table, table)

    def test_row_factory_failure(self):
        table = self._makeOne(self.TABLE_ID, None)
        with self.assertRaises(ValueError):
            table.row(b'row_key', filter_=object(), append=True)

    def test___eq__(self):
        instance = object()
        table1 = self._makeOne(self.TABLE_ID, instance)
        table2 = self._makeOne(self.TABLE_ID, instance)
        self.assertEqual(table1, table2)

    def test___eq__type_differ(self):
        table1 = self._makeOne(self.TABLE_ID, None)
        table2 = object()
        self.assertNotEqual(table1, table2)

    def test___ne__same_value(self):
        instance = object()
        table1 = self._makeOne(self.TABLE_ID, instance)
        table2 = self._makeOne(self.TABLE_ID, instance)
        comparison_val = (table1 != table2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        table1 = self._makeOne('table_id1', 'instance1')
        table2 = self._makeOne('table_id2', 'instance2')
        self.assertNotEqual(table1, table2)

    def _create_test_helper(self, initial_split_keys, column_families=()):
        from gcloud._helpers import _to_bytes
        from gcloud.bigtable._testing import _FakeStub

        client = _Client(timeout_seconds=self.TIMEOUT_SECONDS)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        table = self._makeOne(self.TABLE_ID, instance)

        # Create request_pb
        splits_pb = [
            _CreateTableRequestSplitPB(key=_to_bytes(key))
            for key in initial_split_keys or ()]
        table_pb = None
        if column_families:
            table_pb = _TablePB()
            for cf in column_families:
                cf_pb = table_pb.column_families[cf.column_family_id]
                if cf.gc_rule is not None:
                    cf_pb.gc_rule.MergeFrom(cf.gc_rule.to_pb())
        request_pb = _CreateTableRequestPB(
            initial_splits=splits_pb,
            parent=self.INSTANCE_NAME,
            table_id=self.TABLE_ID,
            table=table_pb,
        )

        # Create response_pb
        response_pb = _TablePB()

        # Patch the stub used by the API method.
        client._table_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # create() has no return value.

        # Perform the method and check the result.
        result = table.create(initial_split_keys=initial_split_keys,
                              column_families=column_families)
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'CreateTable',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])

    def test_create(self):
        initial_split_keys = None
        self._create_test_helper(initial_split_keys)

    def test_create_with_split_keys(self):
        initial_split_keys = [b's1', b's2']
        self._create_test_helper(initial_split_keys)

    def test_create_with_column_families(self):
        from gcloud.bigtable.column_family import ColumnFamily
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        cf_id1 = 'col-fam-id1'
        cf1 = ColumnFamily(cf_id1, None)
        cf_id2 = 'col-fam-id2'
        gc_rule = MaxVersionsGCRule(42)
        cf2 = ColumnFamily(cf_id2, None, gc_rule=gc_rule)

        initial_split_keys = None
        column_families = [cf1, cf2]
        self._create_test_helper(initial_split_keys,
                                 column_families=column_families)

    def _list_column_families_helper(self):
        from gcloud.bigtable._testing import _FakeStub

        client = _Client(timeout_seconds=self.TIMEOUT_SECONDS)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        table = self._makeOne(self.TABLE_ID, instance)

        # Create request_pb
        request_pb = _GetTableRequestPB(name=self.TABLE_NAME)

        # Create response_pb
        COLUMN_FAMILY_ID = 'foo'
        column_family = _ColumnFamilyPB()
        response_pb = _TablePB(
            column_families={COLUMN_FAMILY_ID: column_family},
        )

        # Patch the stub used by the API method.
        client._table_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = {
            COLUMN_FAMILY_ID: table.column_family(COLUMN_FAMILY_ID),
        }

        # Perform the method and check the result.
        result = table.list_column_families()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'GetTable',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])

    def test_list_column_families(self):
        self._list_column_families_helper()

    def test_delete(self):
        from google.protobuf import empty_pb2
        from gcloud.bigtable._testing import _FakeStub

        client = _Client(timeout_seconds=self.TIMEOUT_SECONDS)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        table = self._makeOne(self.TABLE_ID, instance)

        # Create request_pb
        request_pb = _DeleteTableRequestPB(name=self.TABLE_NAME)

        # Create response_pb
        response_pb = empty_pb2.Empty()

        # Patch the stub used by the API method.
        client._table_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # delete() has no return value.

        # Perform the method and check the result.
        result = table.delete()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'DeleteTable',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])

    def _read_row_helper(self, chunks, expected_result):
        from gcloud._testing import _Monkey
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable import table as MUT

        client = _Client(timeout_seconds=self.TIMEOUT_SECONDS)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        table = self._makeOne(self.TABLE_ID, instance)

        # Create request_pb
        request_pb = object()  # Returned by our mock.
        mock_created = []

        def mock_create_row_request(table_name, row_key, filter_):
            mock_created.append((table_name, row_key, filter_))
            return request_pb

        # Create response_iterator
        if chunks is None:
            response_iterator = iter(())  # no responses at all
        else:
            response_pb = _ReadRowsResponsePB(chunks=chunks)
            response_iterator = iter([response_pb])

        # Patch the stub used by the API method.
        client._data_stub = stub = _FakeStub(response_iterator)

        # Perform the method and check the result.
        filter_obj = object()
        with _Monkey(MUT, _create_row_request=mock_create_row_request):
            result = table.read_row(self.ROW_KEY, filter_=filter_obj)

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'ReadRows',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])
        self.assertEqual(mock_created,
                         [(table.name, self.ROW_KEY, filter_obj)])

    def test_read_row_miss_no__responses(self):
        self._read_row_helper(None, None)

    def test_read_row_miss_no_chunks_in_response(self):
        chunks = []
        self._read_row_helper(chunks, None)

    def test_read_row_complete(self):
        from gcloud.bigtable.row_data import Cell
        from gcloud.bigtable.row_data import PartialRowData

        chunk = _ReadRowsResponseCellChunkPB(
            row_key=self.ROW_KEY,
            family_name=self.FAMILY_NAME,
            qualifier=self.QUALIFIER,
            timestamp_micros=self.TIMESTAMP_MICROS,
            value=self.VALUE,
            commit_row=True,
        )
        chunks = [chunk]
        expected_result = PartialRowData(row_key=self.ROW_KEY)
        family = expected_result._cells.setdefault(self.FAMILY_NAME, {})
        column = family.setdefault(self.QUALIFIER, [])
        column.append(Cell.from_pb(chunk))
        self._read_row_helper(chunks, expected_result)

    def test_read_row_still_partial(self):
        chunk = _ReadRowsResponseCellChunkPB(
            row_key=self.ROW_KEY,
            family_name=self.FAMILY_NAME,
            qualifier=self.QUALIFIER,
            timestamp_micros=self.TIMESTAMP_MICROS,
            value=self.VALUE,
        )
        # No "commit row".
        chunks = [chunk]
        with self.assertRaises(ValueError):
            self._read_row_helper(chunks, None)

    def test_read_rows(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable._testing import _FakeStub
        from gcloud.bigtable.row_data import PartialRowsData
        from gcloud.bigtable import table as MUT

        client = _Client(timeout_seconds=self.TIMEOUT_SECONDS)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        table = self._makeOne(self.TABLE_ID, instance)

        # Create request_pb
        request_pb = object()  # Returned by our mock.
        mock_created = []

        def mock_create_row_request(table_name, **kwargs):
            mock_created.append((table_name, kwargs))
            return request_pb

        # Create response_iterator
        response_iterator = object()

        # Patch the stub used by the API method.
        client._data_stub = stub = _FakeStub(response_iterator)

        # Create expected_result.
        expected_result = PartialRowsData(response_iterator)

        # Perform the method and check the result.
        start_key = b'start-key'
        end_key = b'end-key'
        filter_obj = object()
        limit = 22
        with _Monkey(MUT, _create_row_request=mock_create_row_request):
            result = table.read_rows(
                start_key=start_key, end_key=end_key, filter_=filter_obj,
                limit=limit)

        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'ReadRows',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])
        created_kwargs = {
            'start_key': start_key,
            'end_key': end_key,
            'filter_': filter_obj,
            'limit': limit,
        }
        self.assertEqual(mock_created, [(table.name, created_kwargs)])

    def test_sample_row_keys(self):
        from gcloud.bigtable._testing import _FakeStub

        client = _Client(timeout_seconds=self.TIMEOUT_SECONDS)
        instance = _Instance(self.INSTANCE_NAME, client=client)
        table = self._makeOne(self.TABLE_ID, instance)

        # Create request_pb
        request_pb = _SampleRowKeysRequestPB(table_name=self.TABLE_NAME)

        # Create response_iterator
        response_iterator = object()  # Just passed to a mock.

        # Patch the stub used by the API method.
        client._data_stub = stub = _FakeStub(response_iterator)

        # Create expected_result.
        expected_result = response_iterator

        # Perform the method and check the result.
        result = table.sample_row_keys()
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'SampleRowKeys',
            (request_pb, self.TIMEOUT_SECONDS),
            {},
        )])


class Test__create_row_request(unittest2.TestCase):

    def _callFUT(self, table_name, row_key=None, start_key=None, end_key=None,
                 filter_=None, limit=None):
        from gcloud.bigtable.table import _create_row_request
        return _create_row_request(
            table_name, row_key=row_key, start_key=start_key, end_key=end_key,
            filter_=filter_, limit=limit)

    def test_table_name_only(self):
        table_name = 'table_name'
        result = self._callFUT(table_name)
        expected_result = _ReadRowsRequestPB(
            table_name=table_name)
        self.assertEqual(result, expected_result)

    def test_row_key_row_range_conflict(self):
        with self.assertRaises(ValueError):
            self._callFUT(None, row_key=object(), end_key=object())

    def test_row_key(self):
        table_name = 'table_name'
        row_key = b'row_key'
        result = self._callFUT(table_name, row_key=row_key)
        expected_result = _ReadRowsRequestPB(
            table_name=table_name,
        )
        expected_result.rows.row_keys.append(row_key)
        self.assertEqual(result, expected_result)

    def test_row_range_start_key(self):
        table_name = 'table_name'
        start_key = b'start_key'
        result = self._callFUT(table_name, start_key=start_key)
        expected_result = _ReadRowsRequestPB(table_name=table_name)
        expected_result.rows.row_ranges.add(start_key_closed=start_key)
        self.assertEqual(result, expected_result)

    def test_row_range_end_key(self):
        table_name = 'table_name'
        end_key = b'end_key'
        result = self._callFUT(table_name, end_key=end_key)
        expected_result = _ReadRowsRequestPB(table_name=table_name)
        expected_result.rows.row_ranges.add(end_key_open=end_key)
        self.assertEqual(result, expected_result)

    def test_row_range_both_keys(self):
        table_name = 'table_name'
        start_key = b'start_key'
        end_key = b'end_key'
        result = self._callFUT(table_name, start_key=start_key,
                               end_key=end_key)
        expected_result = _ReadRowsRequestPB(table_name=table_name)
        expected_result.rows.row_ranges.add(
            start_key_closed=start_key, end_key_open=end_key)
        self.assertEqual(result, expected_result)

    def test_with_filter(self):
        from gcloud.bigtable.row_filters import RowSampleFilter
        table_name = 'table_name'
        row_filter = RowSampleFilter(0.33)
        result = self._callFUT(table_name, filter_=row_filter)
        expected_result = _ReadRowsRequestPB(
            table_name=table_name,
            filter=row_filter.to_pb(),
        )
        self.assertEqual(result, expected_result)

    def test_with_limit(self):
        table_name = 'table_name'
        limit = 1337
        result = self._callFUT(table_name, limit=limit)
        expected_result = _ReadRowsRequestPB(
            table_name=table_name,
            rows_limit=limit,
        )
        self.assertEqual(result, expected_result)


def _CreateTableRequestPB(*args, **kw):
    from gcloud.bigtable._generated import (
        bigtable_table_admin_pb2 as table_admin_v2_pb2)
    return table_admin_v2_pb2.CreateTableRequest(*args, **kw)


def _CreateTableRequestSplitPB(*args, **kw):
    from gcloud.bigtable._generated import (
        bigtable_table_admin_pb2 as table_admin_v2_pb2)
    return table_admin_v2_pb2.CreateTableRequest.Split(*args, **kw)


def _DeleteTableRequestPB(*args, **kw):
    from gcloud.bigtable._generated import (
        bigtable_table_admin_pb2 as table_admin_v2_pb2)
    return table_admin_v2_pb2.DeleteTableRequest(*args, **kw)


def _GetTableRequestPB(*args, **kw):
    from gcloud.bigtable._generated import (
        bigtable_table_admin_pb2 as table_admin_v2_pb2)
    return table_admin_v2_pb2.GetTableRequest(*args, **kw)


def _ReadRowsRequestPB(*args, **kw):
    from gcloud.bigtable._generated import (
        bigtable_pb2 as messages_v2_pb2)
    return messages_v2_pb2.ReadRowsRequest(*args, **kw)


def _ReadRowsResponseCellChunkPB(*args, **kw):
    from gcloud.bigtable._generated import (
        bigtable_pb2 as messages_v2_pb2)
    family_name = kw.pop('family_name')
    qualifier = kw.pop('qualifier')
    message = messages_v2_pb2.ReadRowsResponse.CellChunk(*args, **kw)
    message.family_name.value = family_name
    message.qualifier.value = qualifier
    return message


def _ReadRowsResponsePB(*args, **kw):
    from gcloud.bigtable._generated import (
        bigtable_pb2 as messages_v2_pb2)
    return messages_v2_pb2.ReadRowsResponse(*args, **kw)


def _SampleRowKeysRequestPB(*args, **kw):
    from gcloud.bigtable._generated import (
        bigtable_pb2 as messages_v2_pb2)
    return messages_v2_pb2.SampleRowKeysRequest(*args, **kw)


def _TablePB(*args, **kw):
    from gcloud.bigtable._generated import (
        table_pb2 as table_v2_pb2)
    return table_v2_pb2.Table(*args, **kw)


def _ColumnFamilyPB(*args, **kw):
    from gcloud.bigtable._generated import (
        table_pb2 as table_v2_pb2)
    return table_v2_pb2.ColumnFamily(*args, **kw)


class _Client(object):

    data_stub = None
    instance_stub = None
    operations_stub = None
    table_stub = None

    def __init__(self, timeout_seconds=None):
        self.timeout_seconds = timeout_seconds


class _Instance(object):

    def __init__(self, name, client=None):
        self.name = name
        self._client = client
