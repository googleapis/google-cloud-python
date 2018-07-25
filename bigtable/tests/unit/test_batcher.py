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

    TABLE_ID = 'table-id'
    TABLE_NAME = '/tables/' + TABLE_ID

    # RPC Status Codes
    SUCCESS = StatusCode.OK.value[0]

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

    @staticmethod
    def _get_target_batcher_class():
        from google.cloud.bigtable.batcher import MutationsBatcher

        return MutationsBatcher

    def _make_batcher(self, *args, **kwargs):
        return self._get_target_batcher_class()(*args, **kwargs)

    def _make_rows(self, table):
        from google.cloud.bigtable.row import DirectRow

        rows = [DirectRow(row_key=b'row_key', table=table),
                DirectRow(row_key=b'row_key_2', table=table),
                DirectRow(row_key=b'row_key_3', table=table),
                DirectRow(row_key=b'row_key_4', table=table)]
        rows[0].set_cell('cf1', b'c1', 1)
        rows[1].set_cell('cf1', b'c1', 2)
        rows[2].set_cell('cf1', b'c1', 3)
        rows[3].set_cell('cf1', b'c1', 4)

        return rows

    def test_constructor(self):
        from google.cloud.bigtable.batcher import MutationsBatcher

        credentials = _make_credentials()
        client = self._make_client(project='project-id',
                                   credentials=credentials, admin=True)

        instance = client.instance(instance_id='instance-id')
        table = self._make_table(self.TABLE_ID, instance)

        mutation_batcher = MutationsBatcher(table)
        self.assertEqual(table, mutation_batcher.table)

    def test_add_row(self):
        table = _Table(self.TABLE_NAME)
        mutation_batcher = self._make_batcher(table)

        rows = self._make_rows(table)

        for row in rows:
            mutation_batcher.mutate(row)

        mutation_batcher.flush()

        self.assertEqual(table.mutation_calls, 1)

    def test_flush_with_no_rows(self):
        table = _Table(self.TABLE_NAME)
        mutation_batcher = self._make_batcher(table)
        mutation_batcher.flush()

        self.assertEqual(table.mutation_calls, 0)

    def test_add_row_with_max_flush_count(self):
        table = _Table(self.TABLE_NAME)
        mutation_batcher = self._make_batcher(table, flush_count=3)

        rows = self._make_rows(table)

        for row in rows:
            mutation_batcher.mutate(row)

        mutation_batcher.flush()

        self.assertEqual(table.mutation_calls, 2)

    @mock.patch('google.cloud.bigtable.batcher.MAX_MUTATIONS', new=3)
    def test_add_row_with_max_mutations_failure(self):
        from google.cloud.bigtable.batcher import MaxMutaionsError

        table = _Table(self.TABLE_NAME)
        mutation_batcher = self._make_batcher(table)

        rows = self._make_rows(table)
        rows[0].set_cell('cf1', b'c1', 2)
        rows[0].set_cell('cf1', b'c1', 3)
        rows[0].set_cell('cf1', b'c1', 4)

        with self.assertRaises(MaxMutaionsError):
            mutation_batcher.mutate(rows[0])

    @mock.patch('google.cloud.bigtable.batcher.MAX_MUTATIONS', new=3)
    def test_add_row_with_max_mutations(self):
        table = _Table(self.TABLE_NAME)
        mutation_batcher = self._make_batcher(table)

        rows = self._make_rows(table)

        for row in rows:
            mutation_batcher.mutate(row)

        mutation_batcher.flush()

        self.assertEqual(table.mutation_calls, 2)

    def test_add_row_with_max_row_bytes(self):
        table = _Table(self.TABLE_NAME)
        mutation_batcher = self._make_batcher(table,
                                              max_row_bytes=1 * 1024 * 1024)

        number_of_bytes = 2 * 1024 * 1024
        max_value = b'1' * number_of_bytes

        rows = self._make_rows(table)
        rows[0].set_cell('cf1', b'c1', max_value)

        for row in rows:
            mutation_batcher.mutate(row)

        mutation_batcher.flush()

        self.assertEqual(table.mutation_calls, 2)


class _Instance(object):

    def __init__(self, client=None):
        self._client = client


class _Table(object):

    def __init__(self, name, client=None):
        self.name = name
        self._instance = _Instance(client)
        self.mutation_calls = 0

    def mutate_rows(self, rows):
        self.mutation_calls += 1
        return rows
