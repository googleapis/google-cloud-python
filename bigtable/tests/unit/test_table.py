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
from google.api_core.exceptions import DeadlineExceeded


class Test___mutate_rows_request(unittest.TestCase):
    def _call_fut(self, table_name, rows):
        from google.cloud.bigtable.table import _mutate_rows_request

        return _mutate_rows_request(table_name, rows)

    @mock.patch("google.cloud.bigtable.table._MAX_BULK_MUTATIONS", new=3)
    def test__mutate_rows_too_many_mutations(self):
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable.table import TooManyMutationsError

        table = mock.Mock(name="table", spec=["name"])
        table.name = "table"
        rows = [
            DirectRow(row_key=b"row_key", table=table),
            DirectRow(row_key=b"row_key_2", table=table),
        ]
        rows[0].set_cell("cf1", b"c1", 1)
        rows[0].set_cell("cf1", b"c1", 2)
        rows[1].set_cell("cf1", b"c1", 3)
        rows[1].set_cell("cf1", b"c1", 4)
        with self.assertRaises(TooManyMutationsError):
            self._call_fut("table", rows)

    def test__mutate_rows_request(self):
        from google.cloud.bigtable.row import DirectRow

        table = mock.Mock(name="table", spec=["name"])
        table.name = "table"
        rows = [
            DirectRow(row_key=b"row_key", table=table),
            DirectRow(row_key=b"row_key_2"),
        ]
        rows[0].set_cell("cf1", b"c1", b"1")
        rows[1].set_cell("cf1", b"c1", b"2")
        result = self._call_fut("table", rows)

        expected_result = _mutate_rows_request_pb(table_name="table")
        entry1 = expected_result.entries.add()
        entry1.row_key = b"row_key"
        mutations1 = entry1.mutations.add()
        mutations1.set_cell.family_name = "cf1"
        mutations1.set_cell.column_qualifier = b"c1"
        mutations1.set_cell.timestamp_micros = -1
        mutations1.set_cell.value = b"1"
        entry2 = expected_result.entries.add()
        entry2.row_key = b"row_key_2"
        mutations2 = entry2.mutations.add()
        mutations2.set_cell.family_name = "cf1"
        mutations2.set_cell.column_qualifier = b"c1"
        mutations2.set_cell.timestamp_micros = -1
        mutations2.set_cell.value = b"2"

        self.assertEqual(result, expected_result)


class Test__check_row_table_name(unittest.TestCase):
    def _call_fut(self, table_name, row):
        from google.cloud.bigtable.table import _check_row_table_name

        return _check_row_table_name(table_name, row)

    def test_wrong_table_name(self):
        from google.cloud.bigtable.table import TableMismatchError
        from google.cloud.bigtable.row import DirectRow

        table = mock.Mock(name="table", spec=["name"])
        table.name = "table"
        row = DirectRow(row_key=b"row_key", table=table)
        with self.assertRaises(TableMismatchError):
            self._call_fut("other_table", row)

    def test_right_table_name(self):
        from google.cloud.bigtable.row import DirectRow

        table = mock.Mock(name="table", spec=["name"])
        table.name = "table"
        row = DirectRow(row_key=b"row_key", table=table)
        result = self._call_fut("table", row)
        self.assertFalse(result)


class Test__check_row_type(unittest.TestCase):
    def _call_fut(self, row):
        from google.cloud.bigtable.table import _check_row_type

        return _check_row_type(row)

    def test_test_wrong_row_type(self):
        from google.cloud.bigtable.row import ConditionalRow

        row = ConditionalRow(row_key=b"row_key", table="table", filter_=None)
        with self.assertRaises(TypeError):
            self._call_fut(row)

    def test_right_row_type(self):
        from google.cloud.bigtable.row import DirectRow

        row = DirectRow(row_key=b"row_key", table="table")
        result = self._call_fut(row)
        self.assertFalse(result)


class TestTable(unittest.TestCase):

    PROJECT_ID = "project-id"
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = "projects/" + PROJECT_ID + "/instances/" + INSTANCE_ID
    TABLE_ID = "table-id"
    TABLE_NAME = INSTANCE_NAME + "/tables/" + TABLE_ID
    ROW_KEY = b"row-key"
    ROW_KEY_1 = b"row-key-1"
    ROW_KEY_2 = b"row-key-2"
    ROW_KEY_3 = b"row-key-3"
    FAMILY_NAME = u"family"
    QUALIFIER = b"qualifier"
    TIMESTAMP_MICROS = 100
    VALUE = b"value"
    _json_tests = None

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.table import Table

        return Table

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _get_target_client_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_client(self, *args, **kwargs):
        return self._get_target_client_class()(*args, **kwargs)

    def test_constructor_w_admin(self):
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT_ID, credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)
        self.assertEqual(table.table_id, self.TABLE_ID)
        self.assertIs(table._instance._client, client)
        self.assertEqual(table.name, self.TABLE_NAME)

    def test_constructor_wo_admin(self):
        credentials = _make_credentials()
        client = self._make_client(
            project=self.PROJECT_ID, credentials=credentials, admin=False
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)
        self.assertEqual(table.table_id, self.TABLE_ID)
        self.assertIs(table._instance._client, client)
        self.assertEqual(table.name, self.TABLE_NAME)

    def test_row_factory_direct(self):
        from google.cloud.bigtable.row import DirectRow

        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)
        row_key = b"row_key"
        row = table.row(row_key)

        self.assertIsInstance(row, DirectRow)
        self.assertEqual(row._row_key, row_key)
        self.assertEqual(row._table, table)

    def test_row_factory_conditional(self):
        from google.cloud.bigtable.row import ConditionalRow

        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)
        row_key = b"row_key"
        filter_ = object()
        row = table.row(row_key, filter_=filter_)

        self.assertIsInstance(row, ConditionalRow)
        self.assertEqual(row._row_key, row_key)
        self.assertEqual(row._table, table)

    def test_row_factory_append(self):
        from google.cloud.bigtable.row import AppendRow

        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)
        row_key = b"row_key"
        row = table.row(row_key, append=True)

        self.assertIsInstance(row, AppendRow)
        self.assertEqual(row._row_key, row_key)
        self.assertEqual(row._table, table)

    def test_row_factory_failure(self):
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)
        with self.assertRaises(ValueError):
            table.row(b"row_key", filter_=object(), append=True)

    def test___eq__(self):
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table1 = self._make_one(self.TABLE_ID, instance)
        table2 = self._make_one(self.TABLE_ID, instance)
        self.assertEqual(table1, table2)

    def test___eq__type_differ(self):
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table1 = self._make_one(self.TABLE_ID, instance)
        table2 = object()
        self.assertNotEqual(table1, table2)

    def test___ne__same_value(self):
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table1 = self._make_one(self.TABLE_ID, instance)
        table2 = self._make_one(self.TABLE_ID, instance)
        comparison_val = table1 != table2
        self.assertFalse(comparison_val)

    def test___ne__(self):
        table1 = self._make_one("table_id1", None)
        table2 = self._make_one("table_id2", None)
        self.assertNotEqual(table1, table2)

    def _create_test_helper(self, split_keys=[], column_families={}):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client
        from google.cloud.bigtable_admin_v2.proto import table_pb2
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_table_admin_pb2 as table_admin_messages_v2_pb2,
        )
        from google.cloud.bigtable.column_family import ColumnFamily

        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        # Patch API calls
        client._table_admin_client = table_api

        # Perform the method and check the result.
        table.create(column_families=column_families, initial_split_keys=split_keys)

        families = {
            id: ColumnFamily(id, self, rule).to_pb()
            for (id, rule) in column_families.items()
        }

        split = table_admin_messages_v2_pb2.CreateTableRequest.Split
        splits = [split(key=split_key) for split_key in split_keys]

        table_api.create_table.assert_called_once_with(
            parent=self.INSTANCE_NAME,
            table=table_pb2.Table(column_families=families),
            table_id=self.TABLE_ID,
            initial_splits=splits,
        )

    def test_create(self):
        self._create_test_helper()

    def test_create_with_families(self):
        from google.cloud.bigtable.column_family import MaxVersionsGCRule

        families = {"family": MaxVersionsGCRule(5)}
        self._create_test_helper(column_families=families)

    def test_create_with_split_keys(self):
        self._create_test_helper(split_keys=[b"split1", b"split2", b"split3"])

    def test_exists(self):
        from google.cloud.bigtable_admin_v2.proto import table_pb2 as table_data_v2_pb2
        from google.cloud.bigtable_admin_v2.proto import (
            bigtable_table_admin_pb2 as table_messages_v1_pb2,
        )
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_instance_admin_client,
            bigtable_table_admin_client,
        )
        from google.api_core.exceptions import NotFound
        from google.api_core.exceptions import BadRequest

        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        instance_api = bigtable_instance_admin_client.BigtableInstanceAdminClient(
            mock.Mock()
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        # Create response_pb
        response_pb = table_messages_v1_pb2.ListTablesResponse(
            tables=[table_data_v2_pb2.Table(name=self.TABLE_NAME)]
        )

        # Patch API calls
        client._table_admin_client = table_api
        client._instance_admin_client = instance_api
        bigtable_table_stub = client._table_admin_client.transport
        bigtable_table_stub.get_table.side_effect = [
            response_pb,
            NotFound("testing"),
            BadRequest("testing"),
        ]

        # Perform the method and check the result.
        table1 = instance.table(self.TABLE_ID)
        table2 = instance.table("table-id2")

        result = table1.exists()
        self.assertEqual(True, result)

        result = table2.exists()
        self.assertEqual(False, result)

        with self.assertRaises(BadRequest):
            table2.exists()

    def test_delete(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        # Patch API calls
        client._table_admin_client = table_api

        # Create expected_result.
        expected_result = None  # delete() has no return value.

        # Perform the method and check the result.
        result = table.delete()
        self.assertEqual(result, expected_result)

    def _list_column_families_helper(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        # Create response_pb
        COLUMN_FAMILY_ID = "foo"
        column_family = _ColumnFamilyPB()
        response_pb = _TablePB(column_families={COLUMN_FAMILY_ID: column_family})

        # Patch the stub used by the API method.
        client._table_admin_client = table_api
        bigtable_table_stub = client._table_admin_client.transport
        bigtable_table_stub.get_table.side_effect = [response_pb]

        # Create expected_result.
        expected_result = {COLUMN_FAMILY_ID: table.column_family(COLUMN_FAMILY_ID)}

        # Perform the method and check the result.
        result = table.list_column_families()
        self.assertEqual(result, expected_result)

    def test_list_column_families(self):
        self._list_column_families_helper()

    def test_get_cluster_states(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client
        from google.cloud.bigtable.enums import Table as enum_table
        from google.cloud.bigtable.table import ClusterState

        INITIALIZING = enum_table.ReplicationState.INITIALIZING
        PLANNED_MAINTENANCE = enum_table.ReplicationState.PLANNED_MAINTENANCE
        READY = enum_table.ReplicationState.READY

        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        response_pb = _TablePB(
            cluster_states={
                "cluster-id1": _ClusterStatePB(INITIALIZING),
                "cluster-id2": _ClusterStatePB(PLANNED_MAINTENANCE),
                "cluster-id3": _ClusterStatePB(READY),
            }
        )

        # Patch the stub used by the API method.
        client._table_admin_client = table_api
        bigtable_table_stub = client._table_admin_client.transport
        bigtable_table_stub.get_table.side_effect = [response_pb]

        # build expected result
        expected_result = {
            u"cluster-id1": ClusterState(INITIALIZING),
            u"cluster-id2": ClusterState(PLANNED_MAINTENANCE),
            u"cluster-id3": ClusterState(READY),
        }

        # Perform the method and check the result.
        result = table.get_cluster_states()
        self.assertEqual(result, expected_result)

    def _read_row_helper(self, chunks, expected_result, app_profile_id=None):

        from google.cloud._testing import _Monkey
        from google.cloud.bigtable import table as MUT
        from google.cloud.bigtable.row_set import RowSet
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client
        from google.cloud.bigtable.row_filters import RowSampleFilter

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance, app_profile_id=app_profile_id)

        # Create request_pb
        request_pb = object()  # Returned by our mock.
        mock_created = []

        def mock_create_row_request(table_name, **kwargs):
            mock_created.append((table_name, kwargs))
            return request_pb

        # Create response_iterator
        if chunks is None:
            response_iterator = iter(())  # no responses at all
        else:
            response_pb = _ReadRowsResponsePB(chunks=chunks)
            response_iterator = iter([response_pb])

        # Patch the stub used by the API method.
        client._table_data_client = data_api
        client._table_admin_client = table_api
        client._table_data_client.transport.read_rows = mock.Mock(
            side_effect=[response_iterator]
        )

        # Perform the method and check the result.
        filter_obj = RowSampleFilter(0.33)
        result = None
        with _Monkey(MUT, _create_row_request=mock_create_row_request):
            result = table.read_row(self.ROW_KEY, filter_=filter_obj)
        row_set = RowSet()
        row_set.add_row_key(self.ROW_KEY)
        expected_request = [
            (
                table.name,
                {
                    "end_inclusive": False,
                    "row_set": row_set,
                    "app_profile_id": app_profile_id,
                    "end_key": None,
                    "limit": None,
                    "start_key": None,
                    "filter_": filter_obj,
                },
            )
        ]
        self.assertEqual(result, expected_result)
        self.assertEqual(mock_created, expected_request)

    def test_read_row_miss_no__responses(self):
        self._read_row_helper(None, None)

    def test_read_row_miss_no_chunks_in_response(self):
        chunks = []
        self._read_row_helper(chunks, None)

    def test_read_row_complete(self):
        from google.cloud.bigtable.row_data import Cell
        from google.cloud.bigtable.row_data import PartialRowData

        app_profile_id = "app-profile-id"
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
        self._read_row_helper(chunks, expected_result, app_profile_id)

    def test_read_row_more_than_one_row_returned(self):
        app_profile_id = "app-profile-id"
        chunk_1 = _ReadRowsResponseCellChunkPB(
            row_key=self.ROW_KEY,
            family_name=self.FAMILY_NAME,
            qualifier=self.QUALIFIER,
            timestamp_micros=self.TIMESTAMP_MICROS,
            value=self.VALUE,
            commit_row=True,
        )
        chunk_2 = _ReadRowsResponseCellChunkPB(
            row_key=self.ROW_KEY_2,
            family_name=self.FAMILY_NAME,
            qualifier=self.QUALIFIER,
            timestamp_micros=self.TIMESTAMP_MICROS,
            value=self.VALUE,
            commit_row=True,
        )

        chunks = [chunk_1, chunk_2]
        with self.assertRaises(ValueError):
            self._read_row_helper(chunks, None, app_profile_id)

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

    def test_mutate_rows(self):
        from google.rpc.status_pb2 import Status
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        instance = client.instance(instance_id=self.INSTANCE_ID)
        client._table_admin_client = table_api
        table = self._make_one(self.TABLE_ID, instance)

        response = [Status(code=0), Status(code=1)]

        mock_worker = mock.Mock(return_value=response)
        with mock.patch(
            "google.cloud.bigtable.table._RetryableMutateRowsWorker",
            new=mock.MagicMock(return_value=mock_worker),
        ):
            statuses = table.mutate_rows([mock.MagicMock(), mock.MagicMock()])
        result = [status.code for status in statuses]
        expected_result = [0, 1]

        self.assertEqual(result, expected_result)

    def test_read_rows(self):
        from google.cloud._testing import _Monkey
        from google.cloud.bigtable.row_data import PartialRowsData
        from google.cloud.bigtable import table as MUT
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        app_profile_id = "app-profile-id"
        table = self._make_one(self.TABLE_ID, instance, app_profile_id=app_profile_id)

        # Create request_pb
        request = retry = object()  # Returned by our mock.
        mock_created = []

        def mock_create_row_request(table_name, **kwargs):
            mock_created.append((table_name, kwargs))
            return request

        # Create expected_result.
        expected_result = PartialRowsData(
            client._table_data_client.transport.read_rows, request, retry
        )

        # Perform the method and check the result.
        start_key = b"start-key"
        end_key = b"end-key"
        filter_obj = object()
        limit = 22
        with _Monkey(MUT, _create_row_request=mock_create_row_request):
            result = table.read_rows(
                start_key=start_key,
                end_key=end_key,
                filter_=filter_obj,
                limit=limit,
                retry=retry,
            )

        self.assertEqual(result.rows, expected_result.rows)
        self.assertEqual(result.retry, expected_result.retry)
        created_kwargs = {
            "start_key": start_key,
            "end_key": end_key,
            "filter_": filter_obj,
            "limit": limit,
            "end_inclusive": False,
            "app_profile_id": app_profile_id,
            "row_set": None,
        }
        self.assertEqual(mock_created, [(table.name, created_kwargs)])

    def test_read_retry_rows(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client
        from google.api_core import retry

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        retry_read_rows = retry.Retry(predicate=_read_rows_retry_exception)

        # Create response_iterator
        chunk_1 = _ReadRowsResponseCellChunkPB(
            row_key=self.ROW_KEY_1,
            family_name=self.FAMILY_NAME,
            qualifier=self.QUALIFIER,
            timestamp_micros=self.TIMESTAMP_MICROS,
            value=self.VALUE,
            commit_row=True,
        )

        chunk_2 = _ReadRowsResponseCellChunkPB(
            row_key=self.ROW_KEY_2,
            family_name=self.FAMILY_NAME,
            qualifier=self.QUALIFIER,
            timestamp_micros=self.TIMESTAMP_MICROS,
            value=self.VALUE,
            commit_row=True,
        )

        response_1 = _ReadRowsResponseV2([chunk_1])
        response_2 = _ReadRowsResponseV2([chunk_2])
        response_failure_iterator_1 = _MockFailureIterator_1()
        response_failure_iterator_2 = _MockFailureIterator_2([response_1])
        response_iterator = _MockReadRowsIterator(response_2)

        # Patch the stub used by the API method.
        client._table_data_client.transport.read_rows = mock.Mock(
            side_effect=[
                response_failure_iterator_1,
                response_failure_iterator_2,
                response_iterator,
            ]
        )

        rows = []
        for row in table.read_rows(
            start_key=self.ROW_KEY_1, end_key=self.ROW_KEY_2, retry=retry_read_rows
        ):
            rows.append(row)

        result = rows[1]
        self.assertEqual(result.row_key, self.ROW_KEY_2)

    def test_yield_retry_rows(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client
        import warnings

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        # Create response_iterator
        chunk_1 = _ReadRowsResponseCellChunkPB(
            row_key=self.ROW_KEY_1,
            family_name=self.FAMILY_NAME,
            qualifier=self.QUALIFIER,
            timestamp_micros=self.TIMESTAMP_MICROS,
            value=self.VALUE,
            commit_row=True,
        )

        chunk_2 = _ReadRowsResponseCellChunkPB(
            row_key=self.ROW_KEY_2,
            family_name=self.FAMILY_NAME,
            qualifier=self.QUALIFIER,
            timestamp_micros=self.TIMESTAMP_MICROS,
            value=self.VALUE,
            commit_row=True,
        )

        response_1 = _ReadRowsResponseV2([chunk_1])
        response_2 = _ReadRowsResponseV2([chunk_2])
        response_failure_iterator_1 = _MockFailureIterator_1()
        response_failure_iterator_2 = _MockFailureIterator_2([response_1])
        response_iterator = _MockReadRowsIterator(response_2)

        # Patch the stub used by the API method.
        client._table_data_client.transport.read_rows = mock.Mock(
            side_effect=[
                response_failure_iterator_1,
                response_failure_iterator_2,
                response_iterator,
            ]
        )

        rows = []
        with warnings.catch_warnings(record=True) as warned:
            for row in table.yield_rows(
                start_key=self.ROW_KEY_1, end_key=self.ROW_KEY_2
            ):
                rows.append(row)

        self.assertEqual(len(warned), 1)
        self.assertIs(warned[0].category, DeprecationWarning)

        result = rows[1]
        self.assertEqual(result.row_key, self.ROW_KEY_2)

    def test_yield_rows_with_row_set(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client
        from google.cloud.bigtable.row_set import RowSet
        from google.cloud.bigtable.row_set import RowRange
        import warnings

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        # Create response_iterator
        chunk_1 = _ReadRowsResponseCellChunkPB(
            row_key=self.ROW_KEY_1,
            family_name=self.FAMILY_NAME,
            qualifier=self.QUALIFIER,
            timestamp_micros=self.TIMESTAMP_MICROS,
            value=self.VALUE,
            commit_row=True,
        )

        chunk_2 = _ReadRowsResponseCellChunkPB(
            row_key=self.ROW_KEY_2,
            family_name=self.FAMILY_NAME,
            qualifier=self.QUALIFIER,
            timestamp_micros=self.TIMESTAMP_MICROS,
            value=self.VALUE,
            commit_row=True,
        )

        chunk_3 = _ReadRowsResponseCellChunkPB(
            row_key=self.ROW_KEY_3,
            family_name=self.FAMILY_NAME,
            qualifier=self.QUALIFIER,
            timestamp_micros=self.TIMESTAMP_MICROS,
            value=self.VALUE,
            commit_row=True,
        )

        response_1 = _ReadRowsResponseV2([chunk_1])
        response_2 = _ReadRowsResponseV2([chunk_2])
        response_3 = _ReadRowsResponseV2([chunk_3])
        response_iterator = _MockReadRowsIterator(response_1, response_2, response_3)

        # Patch the stub used by the API method.
        client._table_data_client.transport.read_rows = mock.Mock(
            side_effect=[response_iterator]
        )

        rows = []
        row_set = RowSet()
        row_set.add_row_range(
            RowRange(start_key=self.ROW_KEY_1, end_key=self.ROW_KEY_2)
        )
        row_set.add_row_key(self.ROW_KEY_3)

        with warnings.catch_warnings(record=True) as warned:
            for row in table.yield_rows(row_set=row_set):
                rows.append(row)

        self.assertEqual(len(warned), 1)
        self.assertIs(warned[0].category, DeprecationWarning)

        self.assertEqual(rows[0].row_key, self.ROW_KEY_1)
        self.assertEqual(rows[1].row_key, self.ROW_KEY_2)
        self.assertEqual(rows[2].row_key, self.ROW_KEY_3)

    def test_sample_row_keys(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        # Create response_iterator
        response_iterator = object()  # Just passed to a mock.

        # Patch the stub used by the API method.
        inner_api_calls = client._table_data_client._inner_api_calls
        inner_api_calls["sample_row_keys"] = mock.Mock(
            side_effect=[[response_iterator]]
        )

        # Create expected_result.
        expected_result = response_iterator

        # Perform the method and check the result.
        result = table.sample_row_keys()
        self.assertEqual(result[0], expected_result)

    def test_truncate(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        data_api = mock.create_autospec(bigtable_client.BigtableClient)
        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        expected_result = None  # truncate() has no return value.
        with mock.patch("google.cloud.bigtable.table.Table.name", new=self.TABLE_NAME):
            result = table.truncate()

        table_api.drop_row_range.assert_called_once_with(
            name=self.TABLE_NAME, delete_all_data_from_table=True
        )

        self.assertEqual(result, expected_result)

    def test_truncate_w_timeout(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        data_api = mock.create_autospec(bigtable_client.BigtableClient)
        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        expected_result = None  # truncate() has no return value.

        timeout = 120
        result = table.truncate(timeout=timeout)

        self.assertEqual(result, expected_result)

    def test_drop_by_prefix(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        data_api = mock.create_autospec(bigtable_client.BigtableClient)
        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        expected_result = None  # drop_by_prefix() has no return value.

        row_key_prefix = "row-key-prefix"

        result = table.drop_by_prefix(row_key_prefix=row_key_prefix)

        self.assertEqual(result, expected_result)

    def test_drop_by_prefix_w_timeout(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        data_api = mock.create_autospec(bigtable_client.BigtableClient)
        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_one(self.TABLE_ID, instance)

        expected_result = None  # drop_by_prefix() has no return value.

        row_key_prefix = "row-key-prefix"

        timeout = 120
        result = table.drop_by_prefix(row_key_prefix=row_key_prefix, timeout=timeout)

        self.assertEqual(result, expected_result)

    def test_mutations_batcher_factory(self):
        flush_count = 100
        max_row_bytes = 1000
        table = self._make_one(self.TABLE_ID, None)
        mutation_batcher = table.mutations_batcher(
            flush_count=flush_count, max_row_bytes=max_row_bytes
        )

        self.assertEqual(mutation_batcher.table.table_id, self.TABLE_ID)
        self.assertEqual(mutation_batcher.flush_count, flush_count)
        self.assertEqual(mutation_batcher.max_row_bytes, max_row_bytes)


class Test__RetryableMutateRowsWorker(unittest.TestCase):
    from grpc import StatusCode

    PROJECT_ID = "project-id"
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = "projects/" + PROJECT_ID + "/instances/" + INSTANCE_ID
    TABLE_ID = "table-id"

    # RPC Status Codes
    SUCCESS = StatusCode.OK.value[0]
    RETRYABLE_1 = StatusCode.DEADLINE_EXCEEDED.value[0]
    RETRYABLE_2 = StatusCode.ABORTED.value[0]
    NON_RETRYABLE = StatusCode.CANCELLED.value[0]

    @staticmethod
    def _get_target_class_for_worker():
        from google.cloud.bigtable.table import _RetryableMutateRowsWorker

        return _RetryableMutateRowsWorker

    def _make_worker(self, *args, **kwargs):
        return self._get_target_class_for_worker()(*args, **kwargs)

    @staticmethod
    def _get_target_class_for_table():
        from google.cloud.bigtable.table import Table

        return Table

    def _make_table(self, *args, **kwargs):
        return self._get_target_class_for_table()(*args, **kwargs)

    @staticmethod
    def _get_target_client_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_client(self, *args, **kwargs):
        return self._get_target_client_class()(*args, **kwargs)

    def _make_responses_statuses(self, codes):
        from google.rpc.status_pb2 import Status

        response = [Status(code=code) for code in codes]
        return response

    def _make_responses(self, codes):
        import six
        from google.cloud.bigtable_v2.proto.bigtable_pb2 import MutateRowsResponse
        from google.rpc.status_pb2 import Status

        entries = [
            MutateRowsResponse.Entry(index=i, status=Status(code=codes[i]))
            for i in six.moves.xrange(len(codes))
        ]
        return MutateRowsResponse(entries=entries)

    def test_callable_empty_rows(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        data_api = mock.create_autospec(bigtable_client.BigtableClient)
        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        worker = self._make_worker(client, table.name, [])
        statuses = worker()

        self.assertEqual(len(statuses), 0)

    def test_callable_no_retry_strategy(self):
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        # Setup:
        #   - Mutate 3 rows.
        # Action:
        #   - Attempt to mutate the rows w/o any retry strategy.
        # Expectation:
        #   - Since no retry, should return statuses as they come back.
        #   - Even if there are retryable errors, no retry attempt is made.
        #   - State of responses_statuses should be
        #       [success, retryable, non-retryable]

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        row_1 = DirectRow(row_key=b"row_key", table=table)
        row_1.set_cell("cf", b"col", b"value1")
        row_2 = DirectRow(row_key=b"row_key_2", table=table)
        row_2.set_cell("cf", b"col", b"value2")
        row_3 = DirectRow(row_key=b"row_key_3", table=table)
        row_3.set_cell("cf", b"col", b"value3")

        response = self._make_responses(
            [self.SUCCESS, self.RETRYABLE_1, self.NON_RETRYABLE]
        )

        with mock.patch("google.cloud.bigtable.table.wrap_method") as patched:
            patched.return_value = mock.Mock(return_value=[response])

            worker = self._make_worker(client, table.name, [row_1, row_2, row_3])
            statuses = worker(retry=None)

        result = [status.code for status in statuses]
        expected_result = [self.SUCCESS, self.RETRYABLE_1, self.NON_RETRYABLE]

        client._table_data_client._inner_api_calls["mutate_rows"].assert_called_once()
        self.assertEqual(result, expected_result)

    def test_callable_retry(self):
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable.table import DEFAULT_RETRY
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        # Setup:
        #   - Mutate 3 rows.
        # Action:
        #   - Initial attempt will mutate all 3 rows.
        # Expectation:
        #   - First attempt will result in one retryable error.
        #   - Second attempt will result in success for the retry-ed row.
        #   - Check MutateRows is called twice.
        #   - State of responses_statuses should be
        #       [success, success, non-retryable]

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        row_1 = DirectRow(row_key=b"row_key", table=table)
        row_1.set_cell("cf", b"col", b"value1")
        row_2 = DirectRow(row_key=b"row_key_2", table=table)
        row_2.set_cell("cf", b"col", b"value2")
        row_3 = DirectRow(row_key=b"row_key_3", table=table)
        row_3.set_cell("cf", b"col", b"value3")

        response_1 = self._make_responses(
            [self.SUCCESS, self.RETRYABLE_1, self.NON_RETRYABLE]
        )
        response_2 = self._make_responses([self.SUCCESS])

        # Patch the stub used by the API method.
        client._table_data_client._inner_api_calls["mutate_rows"] = mock.Mock(
            side_effect=[[response_1], [response_2]]
        )

        retry = DEFAULT_RETRY.with_delay(initial=0.1)
        worker = self._make_worker(client, table.name, [row_1, row_2, row_3])
        statuses = worker(retry=retry)

        result = [status.code for status in statuses]
        expected_result = [self.SUCCESS, self.SUCCESS, self.NON_RETRYABLE]

        self.assertEqual(
            client._table_data_client._inner_api_calls["mutate_rows"].call_count, 2
        )
        self.assertEqual(result, expected_result)

    def test_do_mutate_retryable_rows_empty_rows(self):
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        worker = self._make_worker(client, table.name, [])
        statuses = worker._do_mutate_retryable_rows()

        self.assertEqual(len(statuses), 0)

    def test_do_mutate_retryable_rows(self):
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        # Setup:
        #   - Mutate 2 rows.
        # Action:
        #   - Initial attempt will mutate all 2 rows.
        # Expectation:
        #   - Expect [success, non-retryable]

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        row_1 = DirectRow(row_key=b"row_key", table=table)
        row_1.set_cell("cf", b"col", b"value1")
        row_2 = DirectRow(row_key=b"row_key_2", table=table)
        row_2.set_cell("cf", b"col", b"value2")

        response = self._make_responses([self.SUCCESS, self.NON_RETRYABLE])

        # Patch the stub used by the API method.
        inner_api_calls = client._table_data_client._inner_api_calls
        inner_api_calls["mutate_rows"] = mock.Mock(side_effect=[[response]])

        worker = self._make_worker(client, table.name, [row_1, row_2])
        statuses = worker._do_mutate_retryable_rows()

        result = [status.code for status in statuses]
        expected_result = [self.SUCCESS, self.NON_RETRYABLE]

        self.assertEqual(result, expected_result)

    def test_do_mutate_retryable_rows_retry(self):
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable.table import _BigtableRetryableError
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        # Setup:
        #   - Mutate 3 rows.
        # Action:
        #   - Initial attempt will mutate all 3 rows.
        # Expectation:
        #   - Second row returns retryable error code, so expect a raise.
        #   - State of responses_statuses should be
        #       [success, retryable, non-retryable]

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        row_1 = DirectRow(row_key=b"row_key", table=table)
        row_1.set_cell("cf", b"col", b"value1")
        row_2 = DirectRow(row_key=b"row_key_2", table=table)
        row_2.set_cell("cf", b"col", b"value2")
        row_3 = DirectRow(row_key=b"row_key_3", table=table)
        row_3.set_cell("cf", b"col", b"value3")

        response = self._make_responses(
            [self.SUCCESS, self.RETRYABLE_1, self.NON_RETRYABLE]
        )

        # Patch the stub used by the API method.
        inner_api_calls = client._table_data_client._inner_api_calls
        inner_api_calls["mutate_rows"] = mock.Mock(side_effect=[[response]])

        worker = self._make_worker(client, table.name, [row_1, row_2, row_3])

        with self.assertRaises(_BigtableRetryableError):
            worker._do_mutate_retryable_rows()

        statuses = worker.responses_statuses
        result = [status.code for status in statuses]
        expected_result = [self.SUCCESS, self.RETRYABLE_1, self.NON_RETRYABLE]

        self.assertEqual(result, expected_result)

    def test_do_mutate_retryable_rows_second_retry(self):
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable.table import _BigtableRetryableError
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        # Setup:
        #   - Mutate 4 rows.
        #   - First try results:
        #       [success, retryable, non-retryable, retryable]
        # Action:
        #   - Second try should re-attempt the 'retryable' rows.
        # Expectation:
        #   - After second try:
        #       [success, success, non-retryable, retryable]
        #   - One of the rows tried second time returns retryable error code,
        #     so expect a raise.
        #   - Exception contains response whose index should be '3' even though
        #     only two rows were retried.

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        row_1 = DirectRow(row_key=b"row_key", table=table)
        row_1.set_cell("cf", b"col", b"value1")
        row_2 = DirectRow(row_key=b"row_key_2", table=table)
        row_2.set_cell("cf", b"col", b"value2")
        row_3 = DirectRow(row_key=b"row_key_3", table=table)
        row_3.set_cell("cf", b"col", b"value3")
        row_4 = DirectRow(row_key=b"row_key_4", table=table)
        row_4.set_cell("cf", b"col", b"value4")

        response = self._make_responses([self.SUCCESS, self.RETRYABLE_1])

        # Patch the stub used by the API method.
        inner_api_calls = client._table_data_client._inner_api_calls
        inner_api_calls["mutate_rows"] = mock.Mock(side_effect=[[response]])

        worker = self._make_worker(client, table.name, [row_1, row_2, row_3, row_4])
        worker.responses_statuses = self._make_responses_statuses(
            [self.SUCCESS, self.RETRYABLE_1, self.NON_RETRYABLE, self.RETRYABLE_2]
        )

        with self.assertRaises(_BigtableRetryableError):
            worker._do_mutate_retryable_rows()

        statuses = worker.responses_statuses
        result = [status.code for status in statuses]
        expected_result = [
            self.SUCCESS,
            self.SUCCESS,
            self.NON_RETRYABLE,
            self.RETRYABLE_1,
        ]

        self.assertEqual(result, expected_result)

    def test_do_mutate_retryable_rows_second_try(self):
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        # Setup:
        #   - Mutate 4 rows.
        #   - First try results:
        #       [success, retryable, non-retryable, retryable]
        # Action:
        #   - Second try should re-attempt the 'retryable' rows.
        # Expectation:
        #   - After second try:
        #       [success, non-retryable, non-retryable, success]

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        row_1 = DirectRow(row_key=b"row_key", table=table)
        row_1.set_cell("cf", b"col", b"value1")
        row_2 = DirectRow(row_key=b"row_key_2", table=table)
        row_2.set_cell("cf", b"col", b"value2")
        row_3 = DirectRow(row_key=b"row_key_3", table=table)
        row_3.set_cell("cf", b"col", b"value3")
        row_4 = DirectRow(row_key=b"row_key_4", table=table)
        row_4.set_cell("cf", b"col", b"value4")

        response = self._make_responses([self.NON_RETRYABLE, self.SUCCESS])

        # Patch the stub used by the API method.
        inner_api_calls = client._table_data_client._inner_api_calls
        inner_api_calls["mutate_rows"] = mock.Mock(side_effect=[[response]])

        worker = self._make_worker(client, table.name, [row_1, row_2, row_3, row_4])
        worker.responses_statuses = self._make_responses_statuses(
            [self.SUCCESS, self.RETRYABLE_1, self.NON_RETRYABLE, self.RETRYABLE_2]
        )

        statuses = worker._do_mutate_retryable_rows()

        result = [status.code for status in statuses]
        expected_result = [
            self.SUCCESS,
            self.NON_RETRYABLE,
            self.NON_RETRYABLE,
            self.SUCCESS,
        ]

        self.assertEqual(result, expected_result)

    def test_do_mutate_retryable_rows_second_try_no_retryable(self):
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        # Setup:
        #   - Mutate 2 rows.
        #   - First try results: [success, non-retryable]
        # Action:
        #   - Second try has no row to retry.
        # Expectation:
        #   - After second try: [success, non-retryable]

        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient
        )
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        row_1 = DirectRow(row_key=b"row_key", table=table)
        row_1.set_cell("cf", b"col", b"value1")
        row_2 = DirectRow(row_key=b"row_key_2", table=table)
        row_2.set_cell("cf", b"col", b"value2")

        worker = self._make_worker(client, table.name, [row_1, row_2])
        worker.responses_statuses = self._make_responses_statuses(
            [self.SUCCESS, self.NON_RETRYABLE]
        )

        statuses = worker._do_mutate_retryable_rows()

        result = [status.code for status in statuses]
        expected_result = [self.SUCCESS, self.NON_RETRYABLE]

        self.assertEqual(result, expected_result)

    def test_do_mutate_retryable_rows_mismatch_num_responses(self):
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(
            project="project-id", credentials=credentials, admin=True
        )
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        row_1 = DirectRow(row_key=b"row_key", table=table)
        row_1.set_cell("cf", b"col", b"value1")
        row_2 = DirectRow(row_key=b"row_key_2", table=table)
        row_2.set_cell("cf", b"col", b"value2")

        response = self._make_responses([self.SUCCESS])

        # Patch the stub used by the API method.
        inner_api_calls = client._table_data_client._inner_api_calls
        inner_api_calls["mutate_rows"] = mock.Mock(side_effect=[[response]])

        worker = self._make_worker(client, table.name, [row_1, row_2])
        with self.assertRaises(RuntimeError):
            worker._do_mutate_retryable_rows()


class Test__create_row_request(unittest.TestCase):
    def _call_fut(
        self,
        table_name,
        start_key=None,
        end_key=None,
        filter_=None,
        limit=None,
        end_inclusive=False,
        app_profile_id=None,
        row_set=None,
    ):

        from google.cloud.bigtable.table import _create_row_request

        return _create_row_request(
            table_name,
            start_key=start_key,
            end_key=end_key,
            filter_=filter_,
            limit=limit,
            end_inclusive=end_inclusive,
            app_profile_id=app_profile_id,
            row_set=row_set,
        )

    def test_table_name_only(self):
        table_name = "table_name"
        result = self._call_fut(table_name)
        expected_result = _ReadRowsRequestPB(table_name=table_name)
        self.assertEqual(result, expected_result)

    def test_row_range_row_set_conflict(self):
        with self.assertRaises(ValueError):
            self._call_fut(None, end_key=object(), row_set=object())

    def test_row_range_start_key(self):
        table_name = "table_name"
        start_key = b"start_key"
        result = self._call_fut(table_name, start_key=start_key)
        expected_result = _ReadRowsRequestPB(table_name=table_name)
        expected_result.rows.row_ranges.add(start_key_closed=start_key)
        self.assertEqual(result, expected_result)

    def test_row_range_end_key(self):
        table_name = "table_name"
        end_key = b"end_key"
        result = self._call_fut(table_name, end_key=end_key)
        expected_result = _ReadRowsRequestPB(table_name=table_name)
        expected_result.rows.row_ranges.add(end_key_open=end_key)
        self.assertEqual(result, expected_result)

    def test_row_range_both_keys(self):
        table_name = "table_name"
        start_key = b"start_key"
        end_key = b"end_key"
        result = self._call_fut(table_name, start_key=start_key, end_key=end_key)
        expected_result = _ReadRowsRequestPB(table_name=table_name)
        expected_result.rows.row_ranges.add(
            start_key_closed=start_key, end_key_open=end_key
        )
        self.assertEqual(result, expected_result)

    def test_row_range_both_keys_inclusive(self):
        table_name = "table_name"
        start_key = b"start_key"
        end_key = b"end_key"
        result = self._call_fut(
            table_name, start_key=start_key, end_key=end_key, end_inclusive=True
        )
        expected_result = _ReadRowsRequestPB(table_name=table_name)
        expected_result.rows.row_ranges.add(
            start_key_closed=start_key, end_key_closed=end_key
        )
        self.assertEqual(result, expected_result)

    def test_with_filter(self):
        from google.cloud.bigtable.row_filters import RowSampleFilter

        table_name = "table_name"
        row_filter = RowSampleFilter(0.33)
        result = self._call_fut(table_name, filter_=row_filter)
        expected_result = _ReadRowsRequestPB(
            table_name=table_name, filter=row_filter.to_pb()
        )
        self.assertEqual(result, expected_result)

    def test_with_limit(self):
        table_name = "table_name"
        limit = 1337
        result = self._call_fut(table_name, limit=limit)
        expected_result = _ReadRowsRequestPB(table_name=table_name, rows_limit=limit)
        self.assertEqual(result, expected_result)

    def test_with_row_set(self):
        from google.cloud.bigtable.row_set import RowSet

        table_name = "table_name"
        row_set = RowSet()
        result = self._call_fut(table_name, row_set=row_set)
        expected_result = _ReadRowsRequestPB(table_name=table_name)
        self.assertEqual(result, expected_result)

    def test_with_app_profile_id(self):
        table_name = "table_name"
        limit = 1337
        app_profile_id = "app-profile-id"
        result = self._call_fut(table_name, limit=limit, app_profile_id=app_profile_id)
        expected_result = _ReadRowsRequestPB(
            table_name=table_name, rows_limit=limit, app_profile_id=app_profile_id
        )
        self.assertEqual(result, expected_result)


def _ReadRowsRequestPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import bigtable_pb2 as messages_v2_pb2

    return messages_v2_pb2.ReadRowsRequest(*args, **kw)


class Test_ClusterState(unittest.TestCase):
    def test___eq__(self):
        from google.cloud.bigtable.enums import Table as enum_table
        from google.cloud.bigtable.table import ClusterState

        READY = enum_table.ReplicationState.READY
        state1 = ClusterState(READY)
        state2 = ClusterState(READY)
        self.assertEqual(state1, state2)

    def test___eq__type_differ(self):
        from google.cloud.bigtable.enums import Table as enum_table
        from google.cloud.bigtable.table import ClusterState

        READY = enum_table.ReplicationState.READY
        state1 = ClusterState(READY)
        state2 = object()
        self.assertNotEqual(state1, state2)

    def test___ne__same_value(self):
        from google.cloud.bigtable.enums import Table as enum_table
        from google.cloud.bigtable.table import ClusterState

        READY = enum_table.ReplicationState.READY
        state1 = ClusterState(READY)
        state2 = ClusterState(READY)
        comparison_val = state1 != state2
        self.assertFalse(comparison_val)

    def test___ne__(self):
        from google.cloud.bigtable.enums import Table as enum_table
        from google.cloud.bigtable.table import ClusterState

        READY = enum_table.ReplicationState.READY
        INITIALIZING = enum_table.ReplicationState.INITIALIZING
        state1 = ClusterState(READY)
        state2 = ClusterState(INITIALIZING)
        self.assertNotEqual(state1, state2)

    def test__repr__(self):
        from google.cloud.bigtable.enums import Table as enum_table
        from google.cloud.bigtable.table import ClusterState

        STATE_NOT_KNOWN = enum_table.ReplicationState.STATE_NOT_KNOWN
        INITIALIZING = enum_table.ReplicationState.INITIALIZING
        PLANNED_MAINTENANCE = enum_table.ReplicationState.PLANNED_MAINTENANCE
        UNPLANNED_MAINTENANCE = enum_table.ReplicationState.UNPLANNED_MAINTENANCE
        READY = enum_table.ReplicationState.READY

        replication_dict = {
            STATE_NOT_KNOWN: "STATE_NOT_KNOWN",
            INITIALIZING: "INITIALIZING",
            PLANNED_MAINTENANCE: "PLANNED_MAINTENANCE",
            UNPLANNED_MAINTENANCE: "UNPLANNED_MAINTENANCE",
            READY: "READY",
        }

        self.assertEqual(
            str(ClusterState(STATE_NOT_KNOWN)), replication_dict[STATE_NOT_KNOWN]
        )
        self.assertEqual(
            str(ClusterState(INITIALIZING)), replication_dict[INITIALIZING]
        )
        self.assertEqual(
            str(ClusterState(PLANNED_MAINTENANCE)),
            replication_dict[PLANNED_MAINTENANCE],
        )
        self.assertEqual(
            str(ClusterState(UNPLANNED_MAINTENANCE)),
            replication_dict[UNPLANNED_MAINTENANCE],
        )
        self.assertEqual(str(ClusterState(READY)), replication_dict[READY])

        self.assertEqual(
            ClusterState(STATE_NOT_KNOWN).replication_state, STATE_NOT_KNOWN
        )
        self.assertEqual(ClusterState(INITIALIZING).replication_state, INITIALIZING)
        self.assertEqual(
            ClusterState(PLANNED_MAINTENANCE).replication_state, PLANNED_MAINTENANCE
        )
        self.assertEqual(
            ClusterState(UNPLANNED_MAINTENANCE).replication_state, UNPLANNED_MAINTENANCE
        )
        self.assertEqual(ClusterState(READY).replication_state, READY)


def _ReadRowsResponseCellChunkPB(*args, **kw):
    from google.cloud.bigtable_v2.proto import bigtable_pb2 as messages_v2_pb2

    family_name = kw.pop("family_name")
    qualifier = kw.pop("qualifier")
    message = messages_v2_pb2.ReadRowsResponse.CellChunk(*args, **kw)
    message.family_name.value = family_name
    message.qualifier.value = qualifier
    return message


def _ReadRowsResponsePB(*args, **kw):
    from google.cloud.bigtable_v2.proto import bigtable_pb2 as messages_v2_pb2

    return messages_v2_pb2.ReadRowsResponse(*args, **kw)


def _mutate_rows_request_pb(*args, **kw):
    from google.cloud.bigtable_v2.proto import bigtable_pb2 as data_messages_v2_pb2

    return data_messages_v2_pb2.MutateRowsRequest(*args, **kw)


class _MockReadRowsIterator(object):
    def __init__(self, *values):
        self.iter_values = iter(values)

    def next(self):
        return next(self.iter_values)

    __next__ = next


class _MockFailureIterator_1(object):
    def next(self):
        raise DeadlineExceeded("Failed to read from server")

    __next__ = next


class _MockFailureIterator_2(object):
    def __init__(self, *values):
        self.iter_values = values[0]
        self.calls = 0

    def next(self):
        self.calls += 1
        if self.calls == 1:
            return self.iter_values[0]
        else:
            raise DeadlineExceeded("Failed to read from server")

    __next__ = next


class _ReadRowsResponseV2(object):
    def __init__(self, chunks, last_scanned_row_key=""):
        self.chunks = chunks
        self.last_scanned_row_key = last_scanned_row_key


def _TablePB(*args, **kw):
    from google.cloud.bigtable_admin_v2.proto import table_pb2 as table_v2_pb2

    return table_v2_pb2.Table(*args, **kw)


def _ColumnFamilyPB(*args, **kw):
    from google.cloud.bigtable_admin_v2.proto import table_pb2 as table_v2_pb2

    return table_v2_pb2.ColumnFamily(*args, **kw)


def _ClusterStatePB(replication_state):
    from google.cloud.bigtable_admin_v2.proto import table_pb2 as table_v2_pb2

    return table_v2_pb2.Table.ClusterState(replication_state=replication_state)


def _read_rows_retry_exception(exc):
    return isinstance(exc, DeadlineExceeded)
