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

    def _getTargetClass(self):
        from gcloud.bigtable.table import Table
        return Table

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        table_id = 'table-id'
        cluster = object()

        table = self._makeOne(table_id, cluster)
        self.assertEqual(table.table_id, table_id)
        self.assertTrue(table._cluster is cluster)

    def test_name_property(self):
        table_id = 'table-id'
        cluster_name = 'cluster_name'

        cluster = _Cluster(cluster_name)
        table = self._makeOne(table_id, cluster)
        expected_name = cluster_name + '/tables/' + table_id
        self.assertEqual(table.name, expected_name)

    def test_column_family_factory(self):
        from gcloud.bigtable.column_family import ColumnFamily

        table_id = 'table-id'
        table = self._makeOne(table_id, None)
        column_family_id = 'column_family_id'
        column_family = table.column_family(column_family_id)

        self.assertTrue(isinstance(column_family, ColumnFamily))
        self.assertEqual(column_family.column_family_id, column_family_id)
        self.assertEqual(column_family._table, table)

    def test_row_factory(self):
        from gcloud.bigtable.row import Row

        table_id = 'table-id'
        table = self._makeOne(table_id, None)
        row_key = b'row_key'
        row = table.row(row_key)

        self.assertTrue(isinstance(row, Row))
        self.assertEqual(row._row_key, row_key)
        self.assertEqual(row._table, table)

    def test___eq__(self):
        table_id = 'table_id'
        cluster = object()
        table1 = self._makeOne(table_id, cluster)
        table2 = self._makeOne(table_id, cluster)
        self.assertEqual(table1, table2)

    def test___eq__type_differ(self):
        table1 = self._makeOne('table_id', None)
        table2 = object()
        self.assertNotEqual(table1, table2)

    def test___ne__same_value(self):
        table_id = 'table_id'
        cluster = object()
        table1 = self._makeOne(table_id, cluster)
        table2 = self._makeOne(table_id, cluster)
        comparison_val = (table1 != table2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        table1 = self._makeOne('table_id1', 'cluster1')
        table2 = self._makeOne('table_id2', 'cluster2')
        self.assertNotEqual(table1, table2)

    def _create_test_helper(self, initial_split_keys):
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)
        from gcloud.bigtable._generated import (
            bigtable_table_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub

        project_id = 'project-id'
        zone = 'zone'
        cluster_id = 'cluster-id'
        table_id = 'table-id'
        timeout_seconds = 150
        cluster_name = ('projects/' + project_id + '/zones/' + zone +
                        '/clusters/' + cluster_id)

        client = _Client(timeout_seconds=timeout_seconds)
        cluster = _Cluster(cluster_name, client=client)
        table = self._makeOne(table_id, cluster)

        # Create request_pb
        request_pb = messages_pb2.CreateTableRequest(
            initial_split_keys=initial_split_keys,
            name=cluster_name,
            table_id=table_id,
        )

        # Create response_pb
        response_pb = data_pb2.Table()

        # Patch the stub used by the API method.
        client._table_stub = stub = _FakeStub(response_pb)

        # Create expected_result.
        expected_result = None  # create() has no return value.

        # Perform the method and check the result.
        result = table.create(initial_split_keys=initial_split_keys)
        self.assertEqual(result, expected_result)
        self.assertEqual(stub.method_calls, [(
            'CreateTable',
            (request_pb, timeout_seconds),
            {},
        )])

    def test_create(self):
        initial_split_keys = None
        self._create_test_helper(initial_split_keys)

    def test_create_with_split_keys(self):
        initial_split_keys = ['s1', 's2']
        self._create_test_helper(initial_split_keys)

    def test_delete(self):
        from gcloud.bigtable._generated import (
            bigtable_table_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._generated import empty_pb2
        from gcloud.bigtable._testing import _FakeStub

        project_id = 'project-id'
        zone = 'zone'
        cluster_id = 'cluster-id'
        table_id = 'table-id'
        timeout_seconds = 871
        cluster_name = ('projects/' + project_id + '/zones/' + zone +
                        '/clusters/' + cluster_id)

        client = _Client(timeout_seconds=timeout_seconds)
        cluster = _Cluster(cluster_name, client=client)
        table = self._makeOne(table_id, cluster)

        # Create request_pb
        table_name = cluster_name + '/tables/' + table_id
        request_pb = messages_pb2.DeleteTableRequest(name=table_name)

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
            (request_pb, timeout_seconds),
            {},
        )])

    def test_sample_row_keys(self):
        from gcloud.bigtable._generated import (
            bigtable_service_messages_pb2 as messages_pb2)
        from gcloud.bigtable._testing import _FakeStub

        project_id = 'project-id'
        zone = 'zone'
        cluster_id = 'cluster-id'
        table_id = 'table-id'
        timeout_seconds = 1333

        client = _Client(timeout_seconds=timeout_seconds)
        cluster_name = ('projects/' + project_id + '/zones/' + zone +
                        '/clusters/' + cluster_id)
        cluster = _Cluster(cluster_name, client=client)
        table = self._makeOne(table_id, cluster)

        # Create request_pb
        table_name = cluster_name + '/tables/' + table_id
        request_pb = messages_pb2.SampleRowKeysRequest(table_name=table_name)

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
            (request_pb, timeout_seconds),
            {},
        )])


class _Client(object):

    data_stub = None
    cluster_stub = None
    operations_stub = None
    table_stub = None

    def __init__(self, timeout_seconds=None):
        self.timeout_seconds = timeout_seconds


class _Cluster(object):

    def __init__(self, name, client=None):
        self.name = name
        self._client = client
