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


class TestMutateRows(unittest.TestCase):
    from grpc import StatusCode

    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    TABLE_ID = 'table-id'
    ROW_KEY = b'row-key'
    ROW_KEY_1 = b'row-key-1'
    ROW_KEY_2 = b'row-key-2'
    FAMILY_NAME = u'family'
    QUALIFIER = b'qualifier'
    TIMESTAMP_MICROS = 100
    VALUE = b'value'
    RETRYABLE = StatusCode.DEADLINE_EXCEEDED.value[0]
    SUCCESS = StatusCode.OK.value[0]

    @mock.patch('google.auth.transport.grpc.secure_authorized_channel')
    def _make_channel(self, secure_authorized_channel):
        from google.api_core import grpc_helpers
        target = 'example.com:443'

        channel = grpc_helpers.create_channel(
            target, credentials=mock.sentinel.credentials)

        return channel

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
        from google.cloud.bigtable.mutation import MutateRows

        return MutateRows

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_retry_mutation(self):
        from google.cloud.bigtable.mutation import MutateRowsEntry
        from google.cloud.bigtable_v2 import BigtableClient

        channel = self._make_channel()
        client = BigtableClient(channel=channel)
        table_name = client.table_path(self.PROJECT_ID, self.INSTANCE_ID,
                                       self.TABLE_ID)

        response_1 = self._make_responses([self.SUCCESS, self.RETRYABLE])
        response_2 = self._make_responses([self.SUCCESS])

        client.bigtable_stub.MutateRows.side_effect = [[response_1],
                                                       [response_2]]

        mutate_rows = self._make_one(table_name=table_name, client=client)

        mutate_rows_entry = MutateRowsEntry(row_key=self.ROW_KEY_1)

        mutate_rows_entry.set_cell(
            self.FAMILY_NAME,
            self.QUALIFIER,
            self.VALUE,
            self.TIMESTAMP_MICROS
        )

        mutate_rows.add_row_mutations_entry(mutate_rows_entry)

        mutate_rows_entry = MutateRowsEntry(row_key=self.ROW_KEY_2)

        mutate_rows_entry.set_cell(
            self.FAMILY_NAME,
            self.QUALIFIER,
            self.VALUE,
            self.TIMESTAMP_MICROS
        )

        mutate_rows.add_row_mutations_entry(mutate_rows_entry)

        statuses = mutate_rows.mutate_rows()

        result = [status.code for status in statuses]
        expected_result = [self.SUCCESS, self.SUCCESS]

        self.assertEqual(result, expected_result)

    def test_set_cell_mutation(self):
        from google.cloud.bigtable.mutation import MutateRowsEntry
        from google.cloud.bigtable_v2 import BigtableClient

        channel = self._make_channel()
        client = BigtableClient(channel=channel)
        table_name = client.table_path(self.PROJECT_ID, self.INSTANCE_ID,
                                       self.TABLE_ID)

        response = self._make_responses([self.SUCCESS])

        client.bigtable_stub.MutateRows.side_effect = [[response]]

        mutate_rows = self._make_one(table_name=table_name, client=client)

        mutate_rows_entry = MutateRowsEntry(row_key=self.ROW_KEY)

        mutate_rows_entry.set_cell(
            self.FAMILY_NAME,
            self.QUALIFIER,
            self.VALUE,
            self.TIMESTAMP_MICROS
        )
        mutate_rows.add_row_mutations_entry(mutate_rows_entry)

        statuses = mutate_rows.mutate_rows(retry=False)

        result = [status.code for status in statuses]
        expected_result = [self.SUCCESS]

        self.assertEqual(result, expected_result)

    def test_delete_from_column_mutation(self):
        from google.cloud.bigtable.mutation import MutateRowsEntry
        from google.cloud.bigtable_v2 import BigtableClient

        channel = self._make_channel()
        client = BigtableClient(channel=channel)
        table_name = client.table_path(self.PROJECT_ID, self.INSTANCE_ID,
                                       self.TABLE_ID)

        response = self._make_responses([self.SUCCESS])

        client.bigtable_stub.MutateRows.side_effect = [[response]]

        mutate_rows = self._make_one(table_name=table_name, client=client)

        mutate_rows_entry = MutateRowsEntry(row_key=self.ROW_KEY)

        mutate_rows_entry.delete_from_column(
            self.FAMILY_NAME,
            self.QUALIFIER
        )
        mutate_rows.add_row_mutations_entry(mutate_rows_entry)

        statuses = mutate_rows.mutate_rows()

        result = [status.code for status in statuses]
        expected_result = [self.SUCCESS]

        self.assertEqual(result, expected_result)

    def test_delete_from_family_mutation(self):
        from google.cloud.bigtable.mutation import MutateRowsEntry
        from google.cloud.bigtable_v2 import BigtableClient

        channel = self._make_channel()
        client = BigtableClient(channel=channel)
        table_name = client.table_path(self.PROJECT_ID, self.INSTANCE_ID,
                                       self.TABLE_ID)

        response = self._make_responses([self.SUCCESS])

        client.bigtable_stub.MutateRows.side_effect = [[response]]

        mutate_rows = self._make_one(table_name=table_name, client=client)

        mutate_rows_entry = MutateRowsEntry(row_key=self.ROW_KEY)

        mutate_rows_entry.delete_from_family(
            self.FAMILY_NAME
        )
        mutate_rows.add_row_mutations_entry(mutate_rows_entry)

        statuses = mutate_rows.mutate_rows(retry=False)

        result = [status.code for status in statuses]
        expected_result = [self.SUCCESS]

        self.assertEqual(result, expected_result)

    def test_delete_from_row_mutation(self):
        from google.cloud.bigtable.mutation import MutateRowsEntry
        from google.cloud.bigtable_v2 import BigtableClient

        channel = self._make_channel()
        client = BigtableClient(channel=channel)
        table_name = client.table_path(self.PROJECT_ID, self.INSTANCE_ID,
                                       self.TABLE_ID)

        response = self._make_responses([self.SUCCESS])

        client.bigtable_stub.MutateRows.side_effect = [[response]]

        mutate_rows = self._make_one(table_name=table_name, client=client)

        mutate_rows_entry = MutateRowsEntry(row_key=self.ROW_KEY)

        mutate_rows_entry.delete_from_row()
        mutate_rows.add_row_mutations_entry(mutate_rows_entry)

        statuses = mutate_rows.mutate_rows(retry=False)

        result = [status.code for status in statuses]
        expected_result = [self.SUCCESS]

        self.assertEqual(result, expected_result)

    def test_mutation_runtime_error(self):
        from google.cloud.bigtable.mutation import MutateRowsEntry
        from google.cloud.bigtable_v2 import BigtableClient

        channel = self._make_channel()
        client = BigtableClient(channel=channel)
        table_name = client.table_path(self.PROJECT_ID, self.INSTANCE_ID,
                                       self.TABLE_ID)

        response = self._make_responses([self.SUCCESS])

        client.bigtable_stub.MutateRows.side_effect = [[response]]

        mutate_rows = self._make_one(table_name=table_name, client=client)

        mutate_rows_entry = MutateRowsEntry(row_key=self.ROW_KEY_1)

        mutate_rows_entry.set_cell(
            self.FAMILY_NAME,
            self.QUALIFIER,
            self.VALUE,
            self.TIMESTAMP_MICROS
        )

        mutate_rows.add_row_mutations_entry(mutate_rows_entry)

        mutate_rows_entry = MutateRowsEntry(row_key=self.ROW_KEY_2)

        mutate_rows_entry.set_cell(
            self.FAMILY_NAME,
            self.QUALIFIER,
            self.VALUE,
            self.TIMESTAMP_MICROS
        )

        mutate_rows.add_row_mutations_entry(mutate_rows_entry)

        with self.assertRaises(RuntimeError):
            mutate_rows.mutate_rows()

    def test_mutation_retry_error_with_no_retry_strategy(self):
        from google.cloud.bigtable.mutation import MutateRowsEntry
        from google.cloud.bigtable_v2 import BigtableClient

        channel = self._make_channel()
        client = BigtableClient(channel=channel)
        table_name = client.table_path(self.PROJECT_ID, self.INSTANCE_ID,
                                       self.TABLE_ID)

        response = self._make_responses([self.RETRYABLE])

        client.bigtable_stub.MutateRows.side_effect = [[response]]

        mutate_rows = self._make_one(table_name=table_name, client=client)

        mutate_rows_entry = MutateRowsEntry(row_key=self.ROW_KEY)

        mutate_rows_entry.set_cell(
            self.FAMILY_NAME,
            self.QUALIFIER,
            self.VALUE,
            self.TIMESTAMP_MICROS
        )

        mutate_rows.add_row_mutations_entry(mutate_rows_entry)

        statuses = mutate_rows.mutate_rows(retry=False)

        result = [status.code for status in statuses]
        expected_result = [self.RETRYABLE]

        self.assertEqual(result, expected_result)
