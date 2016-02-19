# Copyright 2016 Google Inc. All rights reserved.
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


class Test_make_row(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.happybase.table import make_row
        return make_row(*args, **kwargs)

    def test_it(self):
        with self.assertRaises(NotImplementedError):
            self._callFUT({}, False)


class Test_make_ordered_row(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.happybase.table import make_ordered_row
        return make_ordered_row(*args, **kwargs)

    def test_it(self):
        with self.assertRaises(NotImplementedError):
            self._callFUT([], False)


class TestTable(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.happybase.table import Table
        return Table

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        name = 'table-name'
        cluster = object()
        connection = _Connection(cluster)
        tables_constructed = []

        def make_low_level_table(*args, **kwargs):
            result = _MockLowLevelTable(*args, **kwargs)
            tables_constructed.append(result)
            return result

        with _Monkey(MUT, _LowLevelTable=make_low_level_table):
            table = self._makeOne(name, connection)
        self.assertEqual(table.name, name)
        self.assertEqual(table.connection, connection)

        table_instance, = tables_constructed
        self.assertEqual(table._low_level_table, table_instance)
        self.assertEqual(table_instance.args, (name, cluster))
        self.assertEqual(table_instance.kwargs, {})

    def test_constructor_null_connection(self):
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        self.assertEqual(table.name, name)
        self.assertEqual(table.connection, connection)
        self.assertEqual(table._low_level_table, None)

    def test___repr__(self):
        name = 'table-name'
        table = self._makeOne(name, None)
        self.assertEqual(repr(table), '<table.Table name=\'table-name\'>')

    def test_regions(self):
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)

        with self.assertRaises(NotImplementedError):
            table.regions()


class _Connection(object):

    def __init__(self, cluster):
        self._cluster = cluster


class _MockLowLevelTable(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
