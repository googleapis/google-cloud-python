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
