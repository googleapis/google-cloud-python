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


class TestMutateRows(unittest.TestCase):
    from grpc import StatusCode

    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    TABLE_ID = 'table-id'
    ROW_KEY = 'row-key'
    ROW_KEY_1 = 'row-key-1'
    ROW_KEY_2 = 'row-key-2'
    FAMILY_NAME = 'family'
    QUALIFIER = 'qualifier'
    TIMESTAMP_MICROS = 100
    VALUE = 'value'
    RETRYABLE = StatusCode.DEADLINE_EXCEEDED.value[0]
    SUCCESS = StatusCode.OK.value[0]

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
        from google.cloud.bigtable.mutation import RowMutations

        return RowMutations

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @staticmethod
    def _get_client_class():
        from google.cloud.bigtable.client import Client

        return Client

    def _make_client(self, *args, **kwargs):
        return self._get_client_class()(*args, **kwargs)

    def test_set_cell(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_table_admin_client)

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(
            mock.Mock())

        credentials = _make_credentials()
        client = self._make_client(self.PROJECT_ID, credentials=credentials,
                                   admin=True)
        instance = client.instance(self.INSTANCE_ID)
        table = instance.table(self.TABLE_ID)

        client._table_data_client = data_api
        client._table_admin_client = table_api

        mutate_rows = self._make_one(row_key=self.ROW_KEY, table=table)

        mutate_rows.set_cell(
            self.FAMILY_NAME,
            self.QUALIFIER,
            self.VALUE,
            self.TIMESTAMP_MICROS
        )

        response = _MutateRowResponsePB()

        client._table_data_client.bigtable_stub.MutateRow.side_effect = ([[
            response]])

        expected_result = mutate_rows.mutate()

        self.assertEqual(response, expected_result[0])

    def test_delete_cells(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_table_admin_client)

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(
            mock.Mock())

        credentials = _make_credentials()
        client = self._make_client(self.PROJECT_ID, credentials=credentials,
                                   admin=True)
        instance = client.instance(self.INSTANCE_ID)
        table = instance.table(self.TABLE_ID)

        client._table_data_client = data_api
        client._table_admin_client = table_api

        mutate_rows = self._make_one(row_key=self.ROW_KEY, table=table)

        columns = ['column1', 'column2']

        mutate_rows.delete_cells(
            self.FAMILY_NAME,
            columns
        )

        response = _MutateRowResponsePB()

        client._table_data_client.bigtable_stub.MutateRow.side_effect = ([[
            response]])

        expected_result = mutate_rows.mutate()

        self.assertEqual(response, expected_result[0])

    def test_delete_from_family(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_table_admin_client)

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(
            mock.Mock())

        credentials = _make_credentials()
        client = self._make_client(self.PROJECT_ID, credentials=credentials,
                                   admin=True)
        instance = client.instance(self.INSTANCE_ID)
        table = instance.table(self.TABLE_ID)

        client._table_data_client = data_api
        client._table_admin_client = table_api

        mutate_rows = self._make_one(row_key=self.ROW_KEY, table=table)

        mutate_rows.delete_from_family(
            self.FAMILY_NAME
        )

        response = _MutateRowResponsePB()

        client._table_data_client.bigtable_stub.MutateRow.side_effect = ([[
            response]])

        expected_result = mutate_rows.mutate()

        self.assertEqual(response, expected_result[0])

    def test_delete(self):
        from google.cloud.bigtable_v2.gapic import bigtable_client
        from google.cloud.bigtable_admin_v2.gapic import (
            bigtable_table_admin_client)

        data_api = bigtable_client.BigtableClient(mock.Mock())
        table_api = bigtable_table_admin_client.BigtableTableAdminClient(
            mock.Mock())

        credentials = _make_credentials()
        client = self._make_client(self.PROJECT_ID, credentials=credentials,
                                   admin=True)
        instance = client.instance(self.INSTANCE_ID)
        table = instance.table(self.TABLE_ID)

        client._table_data_client = data_api
        client._table_admin_client = table_api

        mutate_rows = self._make_one(row_key=self.ROW_KEY)

        mutate_rows.delete()

        response = _MutateRowResponsePB()

        client._table_data_client.bigtable_stub.MutateRow.side_effect = ([[
            response]])

        expected_result = mutate_rows.mutate()

        self.assertEqual(response, expected_result[0])


def _MutateRowResponsePB(*args, **kw):
    from google.cloud.bigtable_v2.proto import (
        bigtable_pb2 as messages_v2_pb2)

    return messages_v2_pb2.MutateRowResponse(*args, **kw)
