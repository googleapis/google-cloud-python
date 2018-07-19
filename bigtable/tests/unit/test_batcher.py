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


import unittest

import mock

from ._testing import _make_credentials


class TestMutationsBatcher(unittest.TestCase):
    from grpc import StatusCode

    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = ('projects/' + PROJECT_ID + '/instances/' + INSTANCE_ID)
    TABLE_ID = 'table-id'
    TABLE_NAME = INSTANCE_NAME + '/tables/' + TABLE_ID

    # RPC Status Codes
    SUCCESS = StatusCode.OK.value[0]
    RETRYABLE_1 = StatusCode.DEADLINE_EXCEEDED.value[0]
    RETRYABLE_2 = StatusCode.ABORTED.value[0]
    NON_RETRYABLE = StatusCode.CANCELLED.value[0]

    def _make_responses(self, codes):
        import six
        from google.cloud.bigtable_v2.proto.bigtable_pb2 import (
            MutateRowsResponse)
        from google.rpc.status_pb2 import Status

        entries = [MutateRowsResponse.Entry(
            index=i, status=Status(code=codes[i]))
            for i in six.moves.xrange(len(codes))]
        return MutateRowsResponse(entries=entries)

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.table import Table

        return Table

    def _make_table(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _get_target_client_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_client(self, *args, **kwargs):
        return self._get_target_client_class()(*args, **kwargs)

    def test_constructor(self):
        from google.cloud.bigtable.batcher import MutationsBatcher

        credentials = _make_credentials()
        client = self._make_client(project='project-id',
                                   credentials=credentials, admin=True)

        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        mutation_batcher = MutationsBatcher(table)
        self.assertEqual(table.table_id, mutation_batcher.table.table_id)

    def test_add_row(self):
        from google.cloud.bigtable.batcher import MutationsBatcher
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_table_admin_client)
        from google.cloud.bigtable_v2.gapic import (
            bigtable_client)

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = mock.create_autospec(
            bigtable_table_admin_client.BigtableTableAdminClient)
        credentials = _make_credentials()
        client = self._make_client(project='project-id',
                                   credentials=credentials, admin=True)
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        response = self._make_responses([self.SUCCESS])
        bigtable_stub = client._table_data_client.bigtable_stub
        bigtable_stub.MutateRows.side_effect = [[response, response]]
        mutation_batcher = MutationsBatcher(table)

        rows = [DirectRow(row_key=b'row_key_1', table=table),
                DirectRow(row_key=b'row_key_2', table=table)]
        rows[0].set_cell('cf1', b'c1', 1)
        rows[0].set_cell('cf1', b'c1', 2)
        rows[1].set_cell('cf1', b'c1', 3)
        rows[1].set_cell('cf1', b'c1', 4)

        for row in rows:
            mutation_batcher.add_row(row)

        with mock.patch('google.cloud.bigtable.table.Table.name',
                        new=self.TABLE_NAME):
            mutation_batcher.finish_batch()

        self.assertEqual(
            client._table_data_client.bigtable_stub.MutateRows.call_count, 1)

    def test_add_row_with_max_flush_count(self):
        from google.cloud.bigtable.batcher import MutationsBatcher
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_table_admin_client)
        from google.cloud.bigtable_v2.gapic import (
            bigtable_client)

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project='project-id',
                                   credentials=credentials, admin=True)
        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        response = self._make_responses([self.SUCCESS])
        bigtable_stub = client._table_data_client.bigtable_stub
        bigtable_stub.MutateRows.side_effect = [
            [response, response, response], [response]]
        mutation_batcher = MutationsBatcher(table, flush_count=3)

        rows = [DirectRow(row_key=b'row_key', table=table),
                DirectRow(row_key=b'row_key_2', table=table),
                DirectRow(row_key=b'row_key_3', table=table),
                DirectRow(row_key=b'row_key_4', table=table)]
        rows[0].set_cell('cf1', b'c1', 1)
        rows[1].set_cell('cf1', b'c1', 2)
        rows[2].set_cell('cf1', b'c1', 3)
        rows[3].set_cell('cf1', b'c1', 4)

        for row in rows:
            mutation_batcher.add_row(row)

        with mock.patch('google.cloud.bigtable.table.Table.name',
                        new=self.TABLE_NAME):
            mutation_batcher.finish_batch()

        self.assertEqual(
            client._table_data_client.bigtable_stub.MutateRows.call_count, 2)

    def test_add_row_with_max_mutationst(self):
        from google.cloud.bigtable.batcher import MutationsBatcher
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_table_admin_client)
        from google.cloud.bigtable_v2.gapic import (
            bigtable_client)

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project='project-id',
                                   credentials=credentials, admin=True)

        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        response = self._make_responses([self.SUCCESS])
        bigtable_stub = client._table_data_client.bigtable_stub
        bigtable_stub.MutateRows.side_effect = [[response], [response]]
        mutation_batcher = MutationsBatcher(table, max_mutations=2)

        rows = [DirectRow(row_key=b'row_key_1', table=table),
                DirectRow(row_key=b'row_key_2', table=table)]
        rows[0].set_cell('cf1', b'c1', 1)
        rows[0].set_cell('cf1', b'c1', 2)
        rows[1].set_cell('cf1', b'c1', 3)
        rows[1].set_cell('cf1', b'c1', 4)

        for row in rows:
            mutation_batcher.add_row(row)

        with mock.patch('google.cloud.bigtable.table.Table.name',
                        new=self.TABLE_NAME):
            mutation_batcher.finish_batch()

        self.assertEqual(
            client._table_data_client.bigtable_stub.MutateRows.call_count, 2)

    def test_add_row_with_max_row_bytes(self):
        from google.cloud.bigtable.batcher import MutationsBatcher
        from google.cloud.bigtable.row import DirectRow
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_table_admin_client)
        from google.cloud.bigtable_v2.gapic import (
            bigtable_client)

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(
            mock.Mock())
        credentials = _make_credentials()
        client = self._make_client(project='project-id',
                                   credentials=credentials, admin=True)

        client._table_data_client = data_api
        client._table_admin_client = table_api
        instance = client.instance(instance_id=self.INSTANCE_ID)
        table = self._make_table(self.TABLE_ID, instance)

        response = self._make_responses([self.SUCCESS])
        bigtable_stub = client._table_data_client.bigtable_stub
        bigtable_stub.MutateRows.side_effect = [[response], [response]]
        mutation_batcher = MutationsBatcher(table, max_row_bytes=2)

        number_of_bytes = 2 * 1024 * 1024
        max_value = b'1' * number_of_bytes

        rows = [DirectRow(row_key=b'row_key', table=table),
                DirectRow(row_key=b'row_key_2', table=table)]
        rows[0].set_cell('cf1', b'c1', 1)
        rows[0].set_cell('cf1', b'c1', max_value)
        rows[1].set_cell('cf1', b'c1', 3)
        rows[1].set_cell('cf1', b'c1', 4)

        for row in rows:
            mutation_batcher.add_row(row)

        with mock.patch('google.cloud.bigtable.table.Table.name',
                        new=self.TABLE_NAME):
            mutation_batcher.finish_batch()

        self.assertEqual(
            client._table_data_client.bigtable_stub.MutateRows.call_count, 2)
