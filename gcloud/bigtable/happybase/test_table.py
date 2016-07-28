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
        instance = object()
        connection = _Connection(instance)
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
        self.assertEqual(table_instance.args, (name, instance))
        self.assertEqual(table_instance.kwargs, {})

    def test_constructor_null_connection(self):
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        self.assertEqual(table.name, name)
        self.assertEqual(table.connection, connection)
        self.assertEqual(table._low_level_table, None)

    def test_families(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        table._low_level_table = _MockLowLevelTable()

        # Mock the column families to be returned.
        col_fam_name = 'fam'
        gc_rule = object()
        col_fam = _MockLowLevelColumnFamily(col_fam_name, gc_rule=gc_rule)
        col_fams = {col_fam_name: col_fam}
        table._low_level_table.column_families = col_fams

        to_dict_result = object()
        to_dict_calls = []

        def mock_gc_rule_to_dict(gc_rule):
            to_dict_calls.append(gc_rule)
            return to_dict_result

        with _Monkey(MUT, _gc_rule_to_dict=mock_gc_rule_to_dict):
            result = table.families()

        self.assertEqual(result, {col_fam_name: to_dict_result})
        self.assertEqual(table._low_level_table.list_column_families_calls, 1)
        self.assertEqual(to_dict_calls, [gc_rule])

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

    def test_row_empty_row(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        table._low_level_table = _MockLowLevelTable()
        table._low_level_table.read_row_result = None

        # Set-up mocks.
        fake_filter = object()
        mock_filters = []

        def mock_filter_chain_helper(**kwargs):
            mock_filters.append(kwargs)
            return fake_filter

        row_key = 'row-key'
        timestamp = object()
        with _Monkey(MUT, _filter_chain_helper=mock_filter_chain_helper):
            result = table.row(row_key, timestamp=timestamp)

        # read_row_result == None --> No results.
        self.assertEqual(result, {})

        read_row_args = (row_key,)
        read_row_kwargs = {'filter_': fake_filter}
        self.assertEqual(table._low_level_table.read_row_calls, [
            (read_row_args, read_row_kwargs),
        ])

        expected_kwargs = {
            'filters': [],
            'versions': 1,
            'timestamp': timestamp,
        }
        self.assertEqual(mock_filters, [expected_kwargs])

    def test_row_with_columns(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        table._low_level_table = _MockLowLevelTable()
        table._low_level_table.read_row_result = None

        # Set-up mocks.
        fake_col_filter = object()
        mock_columns = []

        def mock_columns_filter_helper(*args):
            mock_columns.append(args)
            return fake_col_filter

        fake_filter = object()
        mock_filters = []

        def mock_filter_chain_helper(**kwargs):
            mock_filters.append(kwargs)
            return fake_filter

        row_key = 'row-key'
        columns = object()
        with _Monkey(MUT, _filter_chain_helper=mock_filter_chain_helper,
                     _columns_filter_helper=mock_columns_filter_helper):
            result = table.row(row_key, columns=columns)

        # read_row_result == None --> No results.
        self.assertEqual(result, {})

        read_row_args = (row_key,)
        read_row_kwargs = {'filter_': fake_filter}
        self.assertEqual(table._low_level_table.read_row_calls, [
            (read_row_args, read_row_kwargs),
        ])

        self.assertEqual(mock_columns, [(columns,)])
        expected_kwargs = {
            'filters': [fake_col_filter],
            'versions': 1,
            'timestamp': None,
        }
        self.assertEqual(mock_filters, [expected_kwargs])

    def test_row_with_results(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT
        from gcloud.bigtable.row_data import PartialRowData

        row_key = 'row-key'
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        table._low_level_table = _MockLowLevelTable()
        partial_row = PartialRowData(row_key)
        table._low_level_table.read_row_result = partial_row

        # Set-up mocks.
        fake_filter = object()
        mock_filters = []

        def mock_filter_chain_helper(**kwargs):
            mock_filters.append(kwargs)
            return fake_filter

        fake_pair = object()
        mock_cells = []

        def mock_cells_to_pairs(*args, **kwargs):
            mock_cells.append((args, kwargs))
            return [fake_pair]

        col_fam = u'cf1'
        qual = b'qual'
        fake_cells = object()
        partial_row._cells = {col_fam: {qual: fake_cells}}
        include_timestamp = object()
        with _Monkey(MUT, _filter_chain_helper=mock_filter_chain_helper,
                     _cells_to_pairs=mock_cells_to_pairs):
            result = table.row(row_key, include_timestamp=include_timestamp)

        # The results come from _cells_to_pairs.
        expected_result = {col_fam.encode('ascii') + b':' + qual: fake_pair}
        self.assertEqual(result, expected_result)

        read_row_args = (row_key,)
        read_row_kwargs = {'filter_': fake_filter}
        self.assertEqual(table._low_level_table.read_row_calls, [
            (read_row_args, read_row_kwargs),
        ])

        expected_kwargs = {
            'filters': [],
            'versions': 1,
            'timestamp': None,
        }
        self.assertEqual(mock_filters, [expected_kwargs])
        to_pairs_kwargs = {'include_timestamp': include_timestamp}
        self.assertEqual(mock_cells,
                         [((fake_cells,), to_pairs_kwargs)])

    def test_rows_empty_row(self):
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)

        result = table.rows([])
        self.assertEqual(result, [])

    def test_rows_with_columns(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        table._low_level_table = _MockLowLevelTable()
        rr_result = _MockPartialRowsData()
        table._low_level_table.read_rows_result = rr_result
        self.assertEqual(rr_result.consume_all_calls, 0)

        # Set-up mocks.
        fake_col_filter = object()
        mock_cols = []

        def mock_columns_filter_helper(*args):
            mock_cols.append(args)
            return fake_col_filter

        fake_rows_filter = object()
        mock_rows = []

        def mock_row_keys_filter_helper(*args):
            mock_rows.append(args)
            return fake_rows_filter

        fake_filter = object()
        mock_filters = []

        def mock_filter_chain_helper(**kwargs):
            mock_filters.append(kwargs)
            return fake_filter

        rows = ['row-key']
        columns = object()
        with _Monkey(MUT, _filter_chain_helper=mock_filter_chain_helper,
                     _row_keys_filter_helper=mock_row_keys_filter_helper,
                     _columns_filter_helper=mock_columns_filter_helper):
            result = table.rows(rows, columns=columns)

        # read_rows_result == Empty PartialRowsData --> No results.
        self.assertEqual(result, [])

        read_rows_args = ()
        read_rows_kwargs = {'filter_': fake_filter}
        self.assertEqual(table._low_level_table.read_rows_calls, [
            (read_rows_args, read_rows_kwargs),
        ])
        self.assertEqual(rr_result.consume_all_calls, 1)

        self.assertEqual(mock_cols, [(columns,)])
        self.assertEqual(mock_rows, [(rows,)])
        expected_kwargs = {
            'filters': [fake_col_filter, fake_rows_filter],
            'versions': 1,
            'timestamp': None,
        }
        self.assertEqual(mock_filters, [expected_kwargs])

    def test_rows_with_results(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT
        from gcloud.bigtable.row_data import PartialRowData

        row_key1 = 'row-key1'
        row_key2 = 'row-key2'
        rows = [row_key1, row_key2]
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        table._low_level_table = _MockLowLevelTable()

        row1 = PartialRowData(row_key1)
        # Return row1 but not row2
        rr_result = _MockPartialRowsData(rows={row_key1: row1})
        table._low_level_table.read_rows_result = rr_result
        self.assertEqual(rr_result.consume_all_calls, 0)

        # Set-up mocks.
        fake_rows_filter = object()
        mock_rows = []

        def mock_row_keys_filter_helper(*args):
            mock_rows.append(args)
            return fake_rows_filter

        fake_filter = object()
        mock_filters = []

        def mock_filter_chain_helper(**kwargs):
            mock_filters.append(kwargs)
            return fake_filter

        fake_pair = object()
        mock_cells = []

        def mock_cells_to_pairs(*args, **kwargs):
            mock_cells.append((args, kwargs))
            return [fake_pair]

        col_fam = u'cf1'
        qual = b'qual'
        fake_cells = object()
        row1._cells = {col_fam: {qual: fake_cells}}
        include_timestamp = object()
        with _Monkey(MUT, _row_keys_filter_helper=mock_row_keys_filter_helper,
                     _filter_chain_helper=mock_filter_chain_helper,
                     _cells_to_pairs=mock_cells_to_pairs):
            result = table.rows(rows, include_timestamp=include_timestamp)

        # read_rows_result == PartialRowsData with row_key1
        expected_result = {col_fam.encode('ascii') + b':' + qual: fake_pair}
        self.assertEqual(result, [(row_key1, expected_result)])

        read_rows_args = ()
        read_rows_kwargs = {'filter_': fake_filter}
        self.assertEqual(table._low_level_table.read_rows_calls, [
            (read_rows_args, read_rows_kwargs),
        ])
        self.assertEqual(rr_result.consume_all_calls, 1)

        self.assertEqual(mock_rows, [(rows,)])
        expected_kwargs = {
            'filters': [fake_rows_filter],
            'versions': 1,
            'timestamp': None,
        }
        self.assertEqual(mock_filters, [expected_kwargs])
        to_pairs_kwargs = {'include_timestamp': include_timestamp}
        self.assertEqual(mock_cells,
                         [((fake_cells,), to_pairs_kwargs)])

    def test_cells_empty_row(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        table._low_level_table = _MockLowLevelTable()
        table._low_level_table.read_row_result = None

        # Set-up mocks.
        fake_filter = object()
        mock_filters = []

        def mock_filter_chain_helper(**kwargs):
            mock_filters.append(kwargs)
            return fake_filter

        row_key = 'row-key'
        column = 'fam:col1'
        with _Monkey(MUT, _filter_chain_helper=mock_filter_chain_helper):
            result = table.cells(row_key, column)

        # read_row_result == None --> No results.
        self.assertEqual(result, [])

        read_row_args = (row_key,)
        read_row_kwargs = {'filter_': fake_filter}
        self.assertEqual(table._low_level_table.read_row_calls, [
            (read_row_args, read_row_kwargs),
        ])

        expected_kwargs = {
            'column': column,
            'versions': None,
            'timestamp': None,
        }
        self.assertEqual(mock_filters, [expected_kwargs])

    def test_cells_with_results(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT
        from gcloud.bigtable.row_data import PartialRowData

        row_key = 'row-key'
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        table._low_level_table = _MockLowLevelTable()
        partial_row = PartialRowData(row_key)
        table._low_level_table.read_row_result = partial_row

        # These are all passed to mocks.
        versions = object()
        timestamp = object()
        include_timestamp = object()

        # Set-up mocks.
        fake_filter = object()
        mock_filters = []

        def mock_filter_chain_helper(**kwargs):
            mock_filters.append(kwargs)
            return fake_filter

        fake_result = object()
        mock_cells = []

        def mock_cells_to_pairs(*args, **kwargs):
            mock_cells.append((args, kwargs))
            return fake_result

        col_fam = 'cf1'
        qual = 'qual'
        fake_cells = object()
        partial_row._cells = {col_fam: {qual: fake_cells}}
        column = col_fam + ':' + qual
        with _Monkey(MUT, _filter_chain_helper=mock_filter_chain_helper,
                     _cells_to_pairs=mock_cells_to_pairs):
            result = table.cells(row_key, column, versions=versions,
                                 timestamp=timestamp,
                                 include_timestamp=include_timestamp)

        self.assertEqual(result, fake_result)

        read_row_args = (row_key,)
        read_row_kwargs = {'filter_': fake_filter}
        self.assertEqual(table._low_level_table.read_row_calls, [
            (read_row_args, read_row_kwargs),
        ])

        filter_kwargs = {
            'column': column,
            'versions': versions,
            'timestamp': timestamp,
        }
        self.assertEqual(mock_filters, [filter_kwargs])
        to_pairs_kwargs = {'include_timestamp': include_timestamp}
        self.assertEqual(mock_cells,
                         [((fake_cells,), to_pairs_kwargs)])

    def test_scan_with_batch_size(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        warned = []

        def mock_warn(msg):
            warned.append(msg)

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        # Use unknown to force a TypeError, so we don't need to
        # stub out the rest of the method.
        with self.assertRaises(TypeError):
            with _Monkey(MUT, _WARN=mock_warn):
                list(table.scan(batch_size=object(), unknown=None))

        self.assertEqual(len(warned), 1)
        self.assertIn('batch_size', warned[0])

    def test_scan_with_scan_batching(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        warned = []

        def mock_warn(msg):
            warned.append(msg)

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        # Use unknown to force a TypeError, so we don't need to
        # stub out the rest of the method.
        with self.assertRaises(TypeError):
            with _Monkey(MUT, _WARN=mock_warn):
                list(table.scan(scan_batching=object(), unknown=None))

        self.assertEqual(len(warned), 1)
        self.assertIn('scan_batching', warned[0])

    def test_scan_with_sorted_columns(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        warned = []

        def mock_warn(msg):
            warned.append(msg)

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        # Use unknown to force a TypeError, so we don't need to
        # stub out the rest of the method.
        with self.assertRaises(TypeError):
            with _Monkey(MUT, _WARN=mock_warn):
                list(table.scan(sorted_columns=object(), unknown=None))

        self.assertEqual(len(warned), 1)
        self.assertIn('sorted_columns', warned[0])

    def test_scan_with_invalid_limit(self):
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        with self.assertRaises(ValueError):
            list(table.scan(limit=-10))

    def test_scan_with_row_prefix_and_row_start(self):
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        with self.assertRaises(ValueError):
            list(table.scan(row_prefix='a', row_stop='abc'))

    def test_scan_with_string_filter(self):
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        with self.assertRaises(TypeError):
            list(table.scan(filter='some-string'))

    def _scan_test_helper(self, row_limits=(None, None), row_prefix=None,
                          columns=None, filter_=None, timestamp=None,
                          include_timestamp=False, limit=None, rr_result=None,
                          expected_result=None):
        import types
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        name = 'table-name'
        row_start, row_stop = row_limits
        connection = None
        table = self._makeOne(name, connection)
        table._low_level_table = _MockLowLevelTable()
        rr_result = rr_result or _MockPartialRowsData()
        table._low_level_table.read_rows_result = rr_result
        self.assertEqual(rr_result.consume_next_calls, 0)

        # Set-up mocks.
        fake_col_filter = object()
        mock_columns = []

        def mock_columns_filter_helper(*args):
            mock_columns.append(args)
            return fake_col_filter

        fake_filter = object()
        mock_filters = []

        def mock_filter_chain_helper(**kwargs):
            mock_filters.append(kwargs)
            return fake_filter

        with _Monkey(MUT, _filter_chain_helper=mock_filter_chain_helper,
                     _columns_filter_helper=mock_columns_filter_helper):
            result = table.scan(row_start=row_start, row_stop=row_stop,
                                row_prefix=row_prefix, columns=columns,
                                filter=filter_, timestamp=timestamp,
                                include_timestamp=include_timestamp,
                                limit=limit)
            self.assertTrue(isinstance(result, types.GeneratorType))
            # Need to consume the result while the monkey patch is applied.
            # read_rows_result == Empty PartialRowsData --> No results.
            expected_result = expected_result or []
            self.assertEqual(list(result), expected_result)

        read_rows_args = ()
        if row_prefix:
            row_start = row_prefix
            row_stop = MUT._string_successor(row_prefix)
        read_rows_kwargs = {
            'end_key': row_stop,
            'filter_': fake_filter,
            'limit': limit,
            'start_key': row_start,
        }
        self.assertEqual(table._low_level_table.read_rows_calls, [
            (read_rows_args, read_rows_kwargs),
        ])
        self.assertEqual(rr_result.consume_next_calls,
                         rr_result.iterations + 1)

        if columns is not None:
            self.assertEqual(mock_columns, [(columns,)])
        else:
            self.assertEqual(mock_columns, [])

        filters = []
        if filter_ is not None:
            filters.append(filter_)
        if columns:
            filters.append(fake_col_filter)
        expected_kwargs = {
            'filters': filters,
            'versions': 1,
            'timestamp': timestamp,
        }
        self.assertEqual(mock_filters, [expected_kwargs])

    def test_scan_with_columns(self):
        columns = object()
        self._scan_test_helper(columns=columns)

    def test_scan_with_row_start_and_stop(self):
        row_start = 'bar'
        row_stop = 'foo'
        row_limits = (row_start, row_stop)
        self._scan_test_helper(row_limits=row_limits)

    def test_scan_with_row_prefix(self):
        row_prefix = 'row-prefi'
        self._scan_test_helper(row_prefix=row_prefix)

    def test_scan_with_filter(self):
        mock_filter = object()
        self._scan_test_helper(filter_=mock_filter)

    def test_scan_with_no_results(self):
        limit = 1337
        timestamp = object()
        self._scan_test_helper(timestamp=timestamp, limit=limit)

    def test_scan_with_results(self):
        from gcloud.bigtable.row_data import PartialRowData

        row_key1 = 'row-key1'
        row1 = PartialRowData(row_key1)
        rr_result = _MockPartialRowsData(rows={row_key1: row1}, iterations=1)

        include_timestamp = object()
        expected_result = [(row_key1, {})]
        self._scan_test_helper(include_timestamp=include_timestamp,
                               rr_result=rr_result,
                               expected_result=expected_result)

    def test_put(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT
        from gcloud.bigtable.happybase.table import _WAL_SENTINEL

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        batches_created = []

        def make_batch(*args, **kwargs):
            result = _MockBatch(*args, **kwargs)
            batches_created.append(result)
            return result

        row = 'row-key'
        data = {'fam:col': 'foo'}
        timestamp = None
        with _Monkey(MUT, Batch=make_batch):
            result = table.put(row, data, timestamp=timestamp)

        # There is no return value.
        self.assertEqual(result, None)

        # Check how the batch was created and used.
        batch, = batches_created
        self.assertTrue(isinstance(batch, _MockBatch))
        self.assertEqual(batch.args, (table,))
        expected_kwargs = {
            'timestamp': timestamp,
            'batch_size': None,
            'transaction': False,
            'wal': _WAL_SENTINEL,
        }
        self.assertEqual(batch.kwargs, expected_kwargs)
        # Make sure it was a successful context manager
        self.assertEqual(batch.exit_vals, [(None, None, None)])
        self.assertEqual(batch.put_args, [(row, data)])
        self.assertEqual(batch.delete_args, [])

    def test_delete(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT
        from gcloud.bigtable.happybase.table import _WAL_SENTINEL

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        batches_created = []

        def make_batch(*args, **kwargs):
            result = _MockBatch(*args, **kwargs)
            batches_created.append(result)
            return result

        row = 'row-key'
        columns = ['fam:col1', 'fam:col2']
        timestamp = None
        with _Monkey(MUT, Batch=make_batch):
            result = table.delete(row, columns=columns, timestamp=timestamp)

        # There is no return value.
        self.assertEqual(result, None)

        # Check how the batch was created and used.
        batch, = batches_created
        self.assertTrue(isinstance(batch, _MockBatch))
        self.assertEqual(batch.args, (table,))
        expected_kwargs = {
            'timestamp': timestamp,
            'batch_size': None,
            'transaction': False,
            'wal': _WAL_SENTINEL,
        }
        self.assertEqual(batch.kwargs, expected_kwargs)
        # Make sure it was a successful context manager
        self.assertEqual(batch.exit_vals, [(None, None, None)])
        self.assertEqual(batch.put_args, [])
        self.assertEqual(batch.delete_args, [(row, columns)])

    def test_batch(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import table as MUT

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)

        timestamp = object()
        batch_size = 42
        transaction = False  # Must be False when batch_size is non-null
        wal = object()

        with _Monkey(MUT, Batch=_MockBatch):
            result = table.batch(timestamp=timestamp, batch_size=batch_size,
                                 transaction=transaction, wal=wal)

        self.assertTrue(isinstance(result, _MockBatch))
        self.assertEqual(result.args, (table,))
        expected_kwargs = {
            'timestamp': timestamp,
            'batch_size': batch_size,
            'transaction': transaction,
            'wal': wal,
        }
        self.assertEqual(result.kwargs, expected_kwargs)

    def test_counter_get(self):
        klass = self._getTargetClass()
        counter_value = 1337

        class TableWithInc(klass):

            incremented = []
            value = counter_value

            def counter_inc(self, row, column, value=1):
                self.incremented.append((row, column, value))
                self.value += value
                return self.value

        name = 'table-name'
        connection = None
        table = TableWithInc(name, connection)

        row = 'row-key'
        column = 'fam:col1'
        self.assertEqual(TableWithInc.incremented, [])
        result = table.counter_get(row, column)
        self.assertEqual(result, counter_value)
        self.assertEqual(TableWithInc.incremented, [(row, column, 0)])

    def test_counter_dec(self):
        klass = self._getTargetClass()
        counter_value = 42

        class TableWithInc(klass):

            incremented = []
            value = counter_value

            def counter_inc(self, row, column, value=1):
                self.incremented.append((row, column, value))
                self.value += value
                return self.value

        name = 'table-name'
        connection = None
        table = TableWithInc(name, connection)

        row = 'row-key'
        column = 'fam:col1'
        dec_value = 987
        self.assertEqual(TableWithInc.incremented, [])
        result = table.counter_dec(row, column, value=dec_value)
        self.assertEqual(result, counter_value - dec_value)
        self.assertEqual(TableWithInc.incremented, [(row, column, -dec_value)])

    def _counter_inc_helper(self, row, column, value, commit_result):
        import six

        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)
        # Mock the return values.
        table._low_level_table = _MockLowLevelTable()
        table._low_level_table.row_values[row] = row_obj = _MockLowLevelRow(
            row, commit_result=commit_result)

        self.assertFalse(row_obj._append)
        result = table.counter_inc(row, column, value=value)
        self.assertTrue(row_obj._append)

        incremented_value = value + _MockLowLevelRow.COUNTER_DEFAULT
        self.assertEqual(result, incremented_value)

        # Check the row values returned.
        row_obj = table._low_level_table.row_values[row]
        if isinstance(column, six.binary_type):
            column = column.decode('utf-8')
        self.assertEqual(row_obj.counts,
                         {tuple(column.split(':')): incremented_value})

    def test_counter_set(self):
        name = 'table-name'
        connection = None
        table = self._makeOne(name, connection)

        row = 'row-key'
        column = 'fam:col1'
        value = 42
        with self.assertRaises(NotImplementedError):
            table.counter_set(row, column, value=value)

    def test_counter_inc(self):
        import struct

        row = 'row-key'
        col_fam = u'fam'
        col_qual = u'col1'
        column = col_fam + u':' + col_qual
        value = 42
        packed_value = struct.pack('>q', value)
        fake_timestamp = None
        commit_result = {
            col_fam: {
                col_qual: [(packed_value, fake_timestamp)],
            }
        }
        self._counter_inc_helper(row, column, value, commit_result)

    def test_counter_inc_column_bytes(self):
        import struct

        row = 'row-key'
        col_fam = b'fam'
        col_qual = b'col1'
        column = col_fam + b':' + col_qual
        value = 42
        packed_value = struct.pack('>q', value)
        fake_timestamp = None
        commit_result = {
            col_fam.decode('utf-8'): {
                col_qual.decode('utf-8'): [(packed_value, fake_timestamp)],
            }
        }
        self._counter_inc_helper(row, column, value, commit_result)

    def test_counter_inc_bad_result(self):
        row = 'row-key'
        col_fam = 'fam'
        col_qual = 'col1'
        column = col_fam + ':' + col_qual
        value = 42
        commit_result = None
        with self.assertRaises(TypeError):
            self._counter_inc_helper(row, column, value, commit_result)

    def test_counter_inc_result_key_error(self):
        row = 'row-key'
        col_fam = 'fam'
        col_qual = 'col1'
        column = col_fam + ':' + col_qual
        value = 42
        commit_result = {}
        with self.assertRaises(KeyError):
            self._counter_inc_helper(row, column, value, commit_result)

    def test_counter_inc_result_nested_key_error(self):
        row = 'row-key'
        col_fam = 'fam'
        col_qual = 'col1'
        column = col_fam + ':' + col_qual
        value = 42
        commit_result = {col_fam: {}}
        with self.assertRaises(KeyError):
            self._counter_inc_helper(row, column, value, commit_result)

    def test_counter_inc_result_non_unique_cell(self):
        row = 'row-key'
        col_fam = 'fam'
        col_qual = 'col1'
        column = col_fam + ':' + col_qual
        value = 42
        fake_timestamp = None
        packed_value = None
        commit_result = {
            col_fam: {
                col_qual: [
                    (packed_value, fake_timestamp),
                    (packed_value, fake_timestamp),
                ],
            }
        }
        with self.assertRaises(ValueError):
            self._counter_inc_helper(row, column, value, commit_result)


class Test__gc_rule_to_dict(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.happybase.table import _gc_rule_to_dict
        return _gc_rule_to_dict(*args, **kwargs)

    def test_with_null(self):
        gc_rule = None
        result = self._callFUT(gc_rule)
        self.assertEqual(result, {})

    def test_with_max_versions(self):
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        max_versions = 2
        gc_rule = MaxVersionsGCRule(max_versions)
        result = self._callFUT(gc_rule)
        expected_result = {'max_versions': max_versions}
        self.assertEqual(result, expected_result)

    def test_with_max_age(self):
        import datetime
        from gcloud.bigtable.column_family import MaxAgeGCRule

        time_to_live = 101
        max_age = datetime.timedelta(seconds=time_to_live)
        gc_rule = MaxAgeGCRule(max_age)
        result = self._callFUT(gc_rule)
        expected_result = {'time_to_live': time_to_live}
        self.assertEqual(result, expected_result)

    def test_with_non_gc_rule(self):
        gc_rule = object()
        result = self._callFUT(gc_rule)
        self.assertTrue(result is gc_rule)

    def test_with_gc_rule_union(self):
        from gcloud.bigtable.column_family import GCRuleUnion

        gc_rule = GCRuleUnion(rules=[])
        result = self._callFUT(gc_rule)
        self.assertTrue(result is gc_rule)

    def test_with_intersection_other_than_two(self):
        from gcloud.bigtable.column_family import GCRuleIntersection

        gc_rule = GCRuleIntersection(rules=[])
        result = self._callFUT(gc_rule)
        self.assertTrue(result is gc_rule)

    def test_with_intersection_two_max_num_versions(self):
        from gcloud.bigtable.column_family import GCRuleIntersection
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        rule1 = MaxVersionsGCRule(1)
        rule2 = MaxVersionsGCRule(2)
        gc_rule = GCRuleIntersection(rules=[rule1, rule2])
        result = self._callFUT(gc_rule)
        self.assertTrue(result is gc_rule)

    def test_with_intersection_two_rules(self):
        import datetime
        from gcloud.bigtable.column_family import GCRuleIntersection
        from gcloud.bigtable.column_family import MaxAgeGCRule
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        time_to_live = 101
        max_age = datetime.timedelta(seconds=time_to_live)
        rule1 = MaxAgeGCRule(max_age)
        max_versions = 2
        rule2 = MaxVersionsGCRule(max_versions)
        gc_rule = GCRuleIntersection(rules=[rule1, rule2])
        result = self._callFUT(gc_rule)
        expected_result = {
            'max_versions': max_versions,
            'time_to_live': time_to_live,
        }
        self.assertEqual(result, expected_result)

    def test_with_intersection_two_nested_rules(self):
        from gcloud.bigtable.column_family import GCRuleIntersection

        rule1 = GCRuleIntersection(rules=[])
        rule2 = GCRuleIntersection(rules=[])
        gc_rule = GCRuleIntersection(rules=[rule1, rule2])
        result = self._callFUT(gc_rule)
        self.assertTrue(result is gc_rule)


class Test__string_successor(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.happybase.table import _string_successor
        return _string_successor(*args, **kwargs)

    def test_with_alphanumeric(self):
        self.assertEqual(self._callFUT(b'boa'), b'bob')
        self.assertEqual(self._callFUT(b'abc1'), b'abc2')

    def test_with_last_byte(self):
        self.assertEqual(self._callFUT(b'boa\xff'), b'bob')

    def test_with_empty_string(self):
        self.assertEqual(self._callFUT(b''), b'')

    def test_with_all_last_bytes(self):
        self.assertEqual(self._callFUT(b'\xff\xff\xff'), b'')

    def test_with_unicode_input(self):
        self.assertEqual(self._callFUT(u'boa'), b'bob')


class Test__convert_to_time_range(unittest2.TestCase):

    def _callFUT(self, timestamp=None):
        from gcloud.bigtable.happybase.table import _convert_to_time_range
        return _convert_to_time_range(timestamp=timestamp)

    def test_null(self):
        timestamp = None
        result = self._callFUT(timestamp=timestamp)
        self.assertEqual(result, None)

    def test_invalid_type(self):
        timestamp = object()
        with self.assertRaises(TypeError):
            self._callFUT(timestamp=timestamp)

    def test_success(self):
        from gcloud._helpers import _datetime_from_microseconds
        from gcloud.bigtable.row_filters import TimestampRange

        timestamp = 1441928298571
        ts_dt = _datetime_from_microseconds(1000 * timestamp)
        result = self._callFUT(timestamp=timestamp)
        self.assertTrue(isinstance(result, TimestampRange))
        self.assertEqual(result.start, None)
        self.assertEqual(result.end, ts_dt)


class Test__cells_to_pairs(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.happybase.table import _cells_to_pairs
        return _cells_to_pairs(*args, **kwargs)

    def test_without_timestamp(self):
        from gcloud.bigtable.row_data import Cell

        value1 = 'foo'
        cell1 = Cell(value=value1, timestamp=None)
        value2 = 'bar'
        cell2 = Cell(value=value2, timestamp=None)

        result = self._callFUT([cell1, cell2])
        self.assertEqual(result, [value1, value2])

    def test_with_timestamp(self):
        from gcloud._helpers import _datetime_from_microseconds
        from gcloud.bigtable.row_data import Cell

        value1 = 'foo'
        ts1_millis = 1221934570148
        ts1 = _datetime_from_microseconds(ts1_millis * 1000)
        cell1 = Cell(value=value1, timestamp=ts1)

        value2 = 'bar'
        ts2_millis = 1221955575548
        ts2 = _datetime_from_microseconds(ts2_millis * 1000)
        cell2 = Cell(value=value2, timestamp=ts2)

        result = self._callFUT([cell1, cell2], include_timestamp=True)
        self.assertEqual(result,
                         [(value1, ts1_millis), (value2, ts2_millis)])


class Test__partial_row_to_dict(unittest2.TestCase):

    def _callFUT(self, partial_row_data, include_timestamp=False):
        from gcloud.bigtable.happybase.table import _partial_row_to_dict
        return _partial_row_to_dict(partial_row_data,
                                    include_timestamp=include_timestamp)

    def test_without_timestamp(self):
        from gcloud.bigtable.row_data import Cell
        from gcloud.bigtable.row_data import PartialRowData

        row_data = PartialRowData(b'row-key')
        val1 = b'hi-im-bytes'
        val2 = b'bi-im-hytes'
        row_data._cells[u'fam1'] = {
            b'col1': [Cell(val1, None)],
            b'col2': [Cell(val2, None)],
        }
        result = self._callFUT(row_data)
        expected_result = {
            b'fam1:col1': val1,
            b'fam1:col2': val2,
        }
        self.assertEqual(result, expected_result)

    def test_with_timestamp(self):
        from gcloud._helpers import _datetime_from_microseconds
        from gcloud.bigtable.row_data import Cell
        from gcloud.bigtable.row_data import PartialRowData

        row_data = PartialRowData(b'row-key')
        val1 = b'hi-im-bytes'
        ts1_millis = 1221934570148
        ts1 = _datetime_from_microseconds(ts1_millis * 1000)
        val2 = b'bi-im-hytes'
        ts2_millis = 1331934880000
        ts2 = _datetime_from_microseconds(ts2_millis * 1000)
        row_data._cells[u'fam1'] = {
            b'col1': [Cell(val1, ts1)],
            b'col2': [Cell(val2, ts2)],
        }
        result = self._callFUT(row_data, include_timestamp=True)
        expected_result = {
            b'fam1:col1': (val1, ts1_millis),
            b'fam1:col2': (val2, ts2_millis),
        }
        self.assertEqual(result, expected_result)


class Test__filter_chain_helper(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.happybase.table import _filter_chain_helper
        return _filter_chain_helper(*args, **kwargs)

    def test_no_filters(self):
        with self.assertRaises(ValueError):
            self._callFUT()

    def test_single_filter(self):
        from gcloud.bigtable.row_filters import CellsColumnLimitFilter

        versions = 1337
        result = self._callFUT(versions=versions)
        self.assertTrue(isinstance(result, CellsColumnLimitFilter))
        # Relies on the fact that RowFilter instances can
        # only have one value set.
        self.assertEqual(result.num_cells, versions)

    def test_existing_filters(self):
        from gcloud.bigtable.row_filters import CellsColumnLimitFilter

        filters = []
        versions = 1337
        result = self._callFUT(versions=versions, filters=filters)
        # Make sure filters has grown.
        self.assertEqual(filters, [result])

        self.assertTrue(isinstance(result, CellsColumnLimitFilter))
        # Relies on the fact that RowFilter instances can
        # only have one value set.
        self.assertEqual(result.num_cells, versions)

    def _column_helper(self, num_filters, versions=None, timestamp=None,
                       column=None, col_fam=None, qual=None):
        from gcloud.bigtable.row_filters import ColumnQualifierRegexFilter
        from gcloud.bigtable.row_filters import FamilyNameRegexFilter
        from gcloud.bigtable.row_filters import RowFilterChain

        if col_fam is None:
            col_fam = 'cf1'
        if qual is None:
            qual = 'qual'
        if column is None:
            column = col_fam + ':' + qual
        result = self._callFUT(column, versions=versions, timestamp=timestamp)
        self.assertTrue(isinstance(result, RowFilterChain))

        self.assertEqual(len(result.filters), num_filters)
        fam_filter = result.filters[0]
        qual_filter = result.filters[1]
        self.assertTrue(isinstance(fam_filter, FamilyNameRegexFilter))
        self.assertTrue(isinstance(qual_filter, ColumnQualifierRegexFilter))

        # Relies on the fact that RowFilter instances can
        # only have one value set.
        self.assertEqual(fam_filter.regex, col_fam.encode('utf-8'))
        self.assertEqual(qual_filter.regex, qual.encode('utf-8'))

        return result

    def test_column_only(self):
        self._column_helper(num_filters=2)

    def test_column_bytes(self):
        self._column_helper(num_filters=2, column=b'cfB:qualY',
                            col_fam=u'cfB', qual=u'qualY')

    def test_column_unicode(self):
        self._column_helper(num_filters=2, column=u'cfU:qualN',
                            col_fam=u'cfU', qual=u'qualN')

    def test_with_versions(self):
        from gcloud.bigtable.row_filters import CellsColumnLimitFilter

        versions = 11
        result = self._column_helper(num_filters=3, versions=versions)

        version_filter = result.filters[2]
        self.assertTrue(isinstance(version_filter, CellsColumnLimitFilter))
        # Relies on the fact that RowFilter instances can
        # only have one value set.
        self.assertEqual(version_filter.num_cells, versions)

    def test_with_timestamp(self):
        from gcloud._helpers import _datetime_from_microseconds
        from gcloud.bigtable.row_filters import TimestampRange
        from gcloud.bigtable.row_filters import TimestampRangeFilter

        timestamp = 1441928298571
        result = self._column_helper(num_filters=3, timestamp=timestamp)

        range_filter = result.filters[2]
        self.assertTrue(isinstance(range_filter, TimestampRangeFilter))
        # Relies on the fact that RowFilter instances can
        # only have one value set.
        time_range = range_filter.range_
        self.assertTrue(isinstance(time_range, TimestampRange))
        self.assertEqual(time_range.start, None)
        ts_dt = _datetime_from_microseconds(1000 * timestamp)
        self.assertEqual(time_range.end, ts_dt)

    def test_with_all_options(self):
        versions = 11
        timestamp = 1441928298571
        self._column_helper(num_filters=4, versions=versions,
                            timestamp=timestamp)


class Test__columns_filter_helper(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.happybase.table import _columns_filter_helper
        return _columns_filter_helper(*args, **kwargs)

    def test_no_columns(self):
        columns = []
        with self.assertRaises(ValueError):
            self._callFUT(columns)

    def test_single_column(self):
        from gcloud.bigtable.row_filters import FamilyNameRegexFilter

        col_fam = 'cf1'
        columns = [col_fam]
        result = self._callFUT(columns)
        expected_result = FamilyNameRegexFilter(col_fam)
        self.assertEqual(result, expected_result)

    def test_column_and_column_families(self):
        from gcloud.bigtable.row_filters import ColumnQualifierRegexFilter
        from gcloud.bigtable.row_filters import FamilyNameRegexFilter
        from gcloud.bigtable.row_filters import RowFilterChain
        from gcloud.bigtable.row_filters import RowFilterUnion

        col_fam1 = 'cf1'
        col_fam2 = 'cf2'
        col_qual2 = 'qual2'
        columns = [col_fam1, col_fam2 + ':' + col_qual2]
        result = self._callFUT(columns)

        self.assertTrue(isinstance(result, RowFilterUnion))
        self.assertEqual(len(result.filters), 2)
        filter1 = result.filters[0]
        filter2 = result.filters[1]

        self.assertTrue(isinstance(filter1, FamilyNameRegexFilter))
        self.assertEqual(filter1.regex, col_fam1.encode('utf-8'))

        self.assertTrue(isinstance(filter2, RowFilterChain))
        filter2a, filter2b = filter2.filters
        self.assertTrue(isinstance(filter2a, FamilyNameRegexFilter))
        self.assertEqual(filter2a.regex, col_fam2.encode('utf-8'))
        self.assertTrue(isinstance(filter2b, ColumnQualifierRegexFilter))
        self.assertEqual(filter2b.regex, col_qual2.encode('utf-8'))


class Test__row_keys_filter_helper(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.happybase.table import _row_keys_filter_helper
        return _row_keys_filter_helper(*args, **kwargs)

    def test_no_rows(self):
        row_keys = []
        with self.assertRaises(ValueError):
            self._callFUT(row_keys)

    def test_single_row(self):
        from gcloud.bigtable.row_filters import RowKeyRegexFilter

        row_key = b'row-key'
        row_keys = [row_key]
        result = self._callFUT(row_keys)
        expected_result = RowKeyRegexFilter(row_key)
        self.assertEqual(result, expected_result)

    def test_many_rows(self):
        from gcloud.bigtable.row_filters import RowFilterUnion
        from gcloud.bigtable.row_filters import RowKeyRegexFilter

        row_key1 = b'row-key1'
        row_key2 = b'row-key2'
        row_key3 = b'row-key3'
        row_keys = [row_key1, row_key2, row_key3]
        result = self._callFUT(row_keys)

        filter1 = RowKeyRegexFilter(row_key1)
        filter2 = RowKeyRegexFilter(row_key2)
        filter3 = RowKeyRegexFilter(row_key3)
        expected_result = RowFilterUnion(filters=[filter1, filter2, filter3])
        self.assertEqual(result, expected_result)


class _Connection(object):

    def __init__(self, instance):
        self._instance = instance


class _MockLowLevelColumnFamily(object):

    def __init__(self, column_family_id, gc_rule=None):
        self.column_family_id = column_family_id
        self.gc_rule = gc_rule


class _MockLowLevelTable(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.list_column_families_calls = 0
        self.column_families = {}
        self.row_values = {}
        self.read_row_calls = []
        self.read_row_result = None
        self.read_rows_calls = []
        self.read_rows_result = None

    def list_column_families(self):
        self.list_column_families_calls += 1
        return self.column_families

    def row(self, row_key, append=None):
        result = self.row_values[row_key]
        result._append = append
        return result

    def read_row(self, *args, **kwargs):
        self.read_row_calls.append((args, kwargs))
        return self.read_row_result

    def read_rows(self, *args, **kwargs):
        self.read_rows_calls.append((args, kwargs))
        return self.read_rows_result


class _MockLowLevelRow(object):

    COUNTER_DEFAULT = 0

    def __init__(self, row_key, commit_result=None):
        self.row_key = row_key
        self._append = False
        self.counts = {}
        self.commit_result = commit_result

    def increment_cell_value(self, column_family_id, column, int_value):
        count = self.counts.setdefault((column_family_id, column),
                                       self.COUNTER_DEFAULT)
        self.counts[(column_family_id, column)] = count + int_value

    def commit(self):
        return self.commit_result


class _MockBatch(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.exit_vals = []
        self.put_args = []
        self.delete_args = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit_vals.append((exc_type, exc_value, traceback))

    def put(self, *args):
        self.put_args.append(args)

    def delete(self, *args):
        self.delete_args.append(args)


class _MockPartialRowsData(object):

    def __init__(self, rows=None, iterations=0):
        self.rows = rows or {}
        self.consume_all_calls = 0
        self.consume_next_calls = 0
        self.iterations = iterations

    def consume_all(self):
        self.consume_all_calls += 1

    def consume_next(self):
        self.consume_next_calls += 1
        if self.consume_next_calls > self.iterations:
            raise StopIteration
