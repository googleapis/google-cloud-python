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


import operator
import struct

import unittest2

from gcloud import _helpers
from gcloud.bigtable import client as client_mod
from gcloud.bigtable.happybase.connection import Connection
from gcloud.environment_vars import TESTS_PROJECT

from bigtable import _operation_wait
from system_test_utils import unique_resource_id


_PACK_I64 = struct.Struct('>q').pack
_FIRST_ELT = operator.itemgetter(0)
_helpers.PROJECT = TESTS_PROJECT
ZONE = 'us-central1-c'
CLUSTER_ID = 'gcloud-py' + unique_resource_id('-')
TABLE_NAME = 'table-name'
ALT_TABLE_NAME = 'other-table'
TTL_FOR_TEST = 3
COL_FAM1 = 'cf1'
COL_FAM2 = 'cf2'
COL_FAM3 = 'cf3'
FAMILIES = {
    COL_FAM1: {'max_versions': 10},
    COL_FAM2: {'max_versions': 1, 'time_to_live': TTL_FOR_TEST},
    COL_FAM3: {},  # use defaults
}
ROW_KEY1 = 'row-key1'
ROW_KEY2 = 'row-key2a'
ROW_KEY3 = 'row-key2b'
COL1 = COL_FAM1 + ':qual1'
COL2 = COL_FAM1 + ':qual2'
COL3 = COL_FAM2 + ':qual1'
COL4 = COL_FAM3 + ':qual3'


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CONNECTION = None
    TABLE = None


def set_connection():
    client = client_mod.Client(admin=True)
    cluster = client.cluster(ZONE, CLUSTER_ID)
    client.start()
    operation = cluster.create()
    if not _operation_wait(operation):
        raise RuntimeError('Cluster creation exceed 5 seconds.')
    Config.CONNECTION = Connection(cluster=cluster)


def setUpModule():
    set_connection()
    Config.CONNECTION.create_table(TABLE_NAME, FAMILIES)
    Config.TABLE = Config.CONNECTION.table(TABLE_NAME)


def tearDownModule():
    Config.CONNECTION.delete_table(TABLE_NAME)
    Config.CONNECTION._cluster.delete()
    Config.CONNECTION.close()


class TestConnection(unittest2.TestCase):

    def test_create_and_delete_table(self):
        connection = Config.CONNECTION

        self.assertFalse(ALT_TABLE_NAME in connection.tables())
        connection.create_table(ALT_TABLE_NAME, {COL_FAM1: {}})
        self.assertTrue(ALT_TABLE_NAME in connection.tables())
        connection.delete_table(ALT_TABLE_NAME)
        self.assertFalse(ALT_TABLE_NAME in connection.tables())

    def test_create_table_failure(self):
        connection = Config.CONNECTION

        self.assertFalse(ALT_TABLE_NAME in connection.tables())
        empty_families = {}
        with self.assertRaises(ValueError):
            connection.create_table(ALT_TABLE_NAME, empty_families)
        self.assertFalse(ALT_TABLE_NAME in connection.tables())


class BaseTableTest(unittest2.TestCase):

    def setUp(self):
        self.rows_to_delete = []

    def tearDown(self):
        for row_key in self.rows_to_delete:
            Config.TABLE.delete(row_key)


class TestTable_families(BaseTableTest):

    def test_families(self):
        families = Config.TABLE.families()

        self.assertEqual(set(families.keys()), set(FAMILIES.keys()))
        for col_fam, settings in FAMILIES.items():
            retrieved = families[col_fam]
            for key, value in settings.items():
                self.assertEqual(retrieved[key], value)


class TestTable_row(BaseTableTest):

    def test_row_when_empty(self):
        row1 = Config.TABLE.row(ROW_KEY1)
        row2 = Config.TABLE.row(ROW_KEY2)

        self.assertEqual(row1, {})
        self.assertEqual(row2, {})

    def test_row_with_columns(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        value3 = 'value3'
        value4 = 'value4'
        row1_data = {
            COL1: value1,
            COL2: value2,
            COL3: value3,
            COL4: value4,
        }

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)
        table.put(ROW_KEY1, row1_data)

        # Make sure the vanilla write succeeded.
        row1 = table.row(ROW_KEY1)
        self.assertEqual(row1, row1_data)

        # Pick out specific columns.
        row1_diff_fams = table.row(ROW_KEY1, columns=[COL1, COL4])
        self.assertEqual(row1_diff_fams, {COL1: value1, COL4: value4})
        row1_single_col = table.row(ROW_KEY1, columns=[COL3])
        self.assertEqual(row1_single_col, {COL3: value3})
        row1_col_fam = table.row(ROW_KEY1, columns=[COL_FAM1])
        self.assertEqual(row1_col_fam, {COL1: value1, COL2: value2})
        row1_fam_qual_overlap1 = table.row(ROW_KEY1, columns=[COL1, COL_FAM1])
        self.assertEqual(row1_fam_qual_overlap1, {COL1: value1, COL2: value2})
        row1_fam_qual_overlap2 = table.row(ROW_KEY1, columns=[COL_FAM1, COL1])
        self.assertEqual(row1_fam_qual_overlap2,
                         {COL1: value1, COL2: value2})
        row1_multiple_col_fams = table.row(ROW_KEY1,
                                           columns=[COL_FAM1, COL_FAM2])
        self.assertEqual(row1_multiple_col_fams,
                         {COL1: value1, COL2: value2, COL3: value3})

    def test_row_with_timestamp(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        value3 = 'value3'

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)
        table.put(ROW_KEY1, {COL1: value1})
        table.put(ROW_KEY1, {COL2: value2})
        table.put(ROW_KEY1, {COL3: value3})

        # Make sure the vanilla write succeeded.
        row1 = table.row(ROW_KEY1, include_timestamp=True)
        ts1 = row1[COL1][1]
        ts2 = row1[COL2][1]
        ts3 = row1[COL3][1]

        expected_row = {
            COL1: (value1, ts1),
            COL2: (value2, ts2),
            COL3: (value3, ts3),
        }
        self.assertEqual(row1, expected_row)

        # Make sure the timestamps are (strictly) ascending.
        self.assertTrue(ts1 < ts2 < ts3)

        # Use timestamps to retrieve row.
        first_two = table.row(ROW_KEY1, timestamp=ts2 + 1,
                              include_timestamp=True)
        self.assertEqual(first_two, {
            COL1: (value1, ts1),
            COL2: (value2, ts2),
        })
        first_one = table.row(ROW_KEY1, timestamp=ts2,
                              include_timestamp=True)
        self.assertEqual(first_one, {
            COL1: (value1, ts1),
        })


class TestTable_rows(BaseTableTest):

    def test_rows(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        value3 = 'value3'
        row1_data = {COL1: value1, COL2: value2}
        row2_data = {COL1: value3}

        # Need to clean-up row1 and row2 after.
        self.rows_to_delete.append(ROW_KEY1)
        self.rows_to_delete.append(ROW_KEY2)
        table.put(ROW_KEY1, row1_data)
        table.put(ROW_KEY2, row2_data)

        rows = sorted(table.rows([ROW_KEY1, ROW_KEY2]), key=_FIRST_ELT)
        row1, row2 = rows
        self.assertEqual(row1, (ROW_KEY1, row1_data))
        self.assertEqual(row2, (ROW_KEY2, row2_data))

    def test_rows_with_returned_timestamps(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        value3 = 'value3'
        row1_data = {COL1: value1, COL2: value2}
        row2_data = {COL1: value3}

        # Need to clean-up row1 and row2 after.
        self.rows_to_delete.append(ROW_KEY1)
        self.rows_to_delete.append(ROW_KEY2)
        with table.batch() as batch:
            batch.put(ROW_KEY1, row1_data)
            batch.put(ROW_KEY2, row2_data)

        rows = sorted(table.rows([ROW_KEY1, ROW_KEY2], include_timestamp=True),
                      key=_FIRST_ELT)
        row1, row2 = rows
        self.assertEqual(row1[0], ROW_KEY1)
        self.assertEqual(row2[0], ROW_KEY2)

        # Drop the keys now that we have checked.
        _, row1 = row1
        _, row2 = row2

        ts = row1[COL1][1]
        # All will have the same timestamp since we used batch.
        expected_row1_result = {COL1: (value1, ts), COL2: (value2, ts)}
        self.assertEqual(row1, expected_row1_result)
        # NOTE: This method was written before Cloud Bigtable had the concept
        #       of batching, so each mutation is sent individually. (This
        #       will be the case until support for the MutateRows() RPC method
        #       is implemented.) Thus, the server-side timestamps correspond
        #       to separate calls to row.commit(). We could circumvent this by
        #       manually using the local time and storing it on mutations
        #       before sending.
        ts3 = row2[COL1][1]
        expected_row2_result = {COL1: (value3, ts3)}
        self.assertEqual(row2, expected_row2_result)

    def test_rows_with_columns(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        value3 = 'value3'
        row1_data = {COL1: value1, COL2: value2}
        row2_data = {COL1: value3}

        # Need to clean-up row1 and row2 after.
        self.rows_to_delete.append(ROW_KEY1)
        self.rows_to_delete.append(ROW_KEY2)
        table.put(ROW_KEY1, row1_data)
        table.put(ROW_KEY2, row2_data)

        # Filter a single column present in both rows.
        rows_col1 = sorted(table.rows([ROW_KEY1, ROW_KEY2], columns=[COL1]),
                           key=_FIRST_ELT)
        row1, row2 = rows_col1
        self.assertEqual(row1, (ROW_KEY1, {COL1: value1}))
        self.assertEqual(row2, (ROW_KEY2, {COL1: value3}))

        # Filter a column not present in one row.
        rows_col2 = table.rows([ROW_KEY1, ROW_KEY2], columns=[COL2])
        self.assertEqual(rows_col2, [(ROW_KEY1, {COL2: value2})])

        # Filter a column family.
        rows_col_fam1 = sorted(
            table.rows([ROW_KEY1, ROW_KEY2], columns=[COL_FAM1]),
            key=_FIRST_ELT)
        row1, row2 = rows_col_fam1
        self.assertEqual(row1, (ROW_KEY1, row1_data))
        self.assertEqual(row2, (ROW_KEY2, row2_data))

        # Filter a column family with no entries.
        rows_col_fam2 = table.rows([ROW_KEY1, ROW_KEY2], columns=[COL_FAM2])
        self.assertEqual(rows_col_fam2, [])

        # Filter a column family that overlaps with a column.
        rows_col_fam_overlap1 = sorted(table.rows([ROW_KEY1, ROW_KEY2],
                                                  columns=[COL1, COL_FAM1]),
                                       key=_FIRST_ELT)
        row1, row2 = rows_col_fam_overlap1
        self.assertEqual(row1, (ROW_KEY1, row1_data))
        self.assertEqual(row2, (ROW_KEY2, row2_data))

        # Filter a column family that overlaps with a column (opposite order).
        rows_col_fam_overlap2 = sorted(table.rows([ROW_KEY1, ROW_KEY2],
                                                  columns=[COL_FAM1, COL1]),
                                       key=_FIRST_ELT)
        row1, row2 = rows_col_fam_overlap2
        self.assertEqual(row1, (ROW_KEY1, row1_data))
        self.assertEqual(row2, (ROW_KEY2, row2_data))

    def test_rows_with_timestamp(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        value3 = 'value3'
        value4 = 'value4'

        # Need to clean-up row1 and row2 after.
        self.rows_to_delete.append(ROW_KEY1)
        self.rows_to_delete.append(ROW_KEY2)
        table.put(ROW_KEY1, {COL1: value1})
        table.put(ROW_KEY2, {COL1: value2})
        table.put(ROW_KEY1, {COL2: value3})
        table.put(ROW_KEY1, {COL4: value4})

        # Just grab the timestamps
        rows = sorted(table.rows([ROW_KEY1, ROW_KEY2], include_timestamp=True),
                      key=_FIRST_ELT)
        row1, row2 = rows
        self.assertEqual(row1[0], ROW_KEY1)
        self.assertEqual(row2[0], ROW_KEY2)
        _, row1 = row1
        _, row2 = row2
        ts1 = row1[COL1][1]
        ts2 = row2[COL1][1]
        ts3 = row1[COL2][1]
        ts4 = row1[COL4][1]

        # Make sure the timestamps are (strictly) ascending.
        self.assertTrue(ts1 < ts2 < ts3 < ts4)

        # Rows before the third timestamp (assumes exclusive endpoint).
        rows = sorted(table.rows([ROW_KEY1, ROW_KEY2], timestamp=ts3,
                                 include_timestamp=True),
                      key=_FIRST_ELT)
        row1, row2 = rows
        self.assertEqual(row1, (ROW_KEY1, {COL1: (value1, ts1)}))
        self.assertEqual(row2, (ROW_KEY2, {COL1: (value2, ts2)}))

        # All writes (bump the exclusive endpoint by 1 millisecond).
        rows = sorted(table.rows([ROW_KEY1, ROW_KEY2], timestamp=ts4 + 1,
                                 include_timestamp=True),
                      key=_FIRST_ELT)
        row1, row2 = rows
        row1_all_data = {
            COL1: (value1, ts1),
            COL2: (value3, ts3),
            COL4: (value4, ts4),
        }
        self.assertEqual(row1, (ROW_KEY1, row1_all_data))
        self.assertEqual(row2, (ROW_KEY2, {COL1: (value2, ts2)}))

        # First three writes, restricted to column 2.
        rows = table.rows([ROW_KEY1, ROW_KEY2], timestamp=ts4,
                          columns=[COL2], include_timestamp=True)
        self.assertEqual(rows, [(ROW_KEY1, {COL2: (value3, ts3)})])


class TestTable_cells(BaseTableTest):

    def test_cells(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        value3 = 'value3'

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)
        table.put(ROW_KEY1, {COL1: value1})
        table.put(ROW_KEY1, {COL1: value2})
        table.put(ROW_KEY1, {COL1: value3})

        # Check with no extra arguments.
        all_values = table.cells(ROW_KEY1, COL1)
        self.assertEqual(all_values, [value3, value2, value1])

        # Check the timestamp on all the cells.
        all_cells = table.cells(ROW_KEY1, COL1, include_timestamp=True)
        self.assertEqual(len(all_cells), 3)

        ts3 = all_cells[0][1]
        ts2 = all_cells[1][1]
        ts1 = all_cells[2][1]
        self.assertEqual(all_cells,
                         [(value3, ts3), (value2, ts2), (value1, ts1)])

        # Limit to the two latest cells.
        latest_two = table.cells(ROW_KEY1, COL1, include_timestamp=True,
                                 versions=2)
        self.assertEqual(latest_two, [(value3, ts3), (value2, ts2)])

        # Limit to cells before the 2nd timestamp (inclusive).
        first_two = table.cells(ROW_KEY1, COL1, include_timestamp=True,
                                timestamp=ts2 + 1)
        self.assertEqual(first_two, [(value2, ts2), (value1, ts1)])

        # Limit to cells before the 2nd timestamp (exclusive).
        first_cell = table.cells(ROW_KEY1, COL1, include_timestamp=True,
                                 timestamp=ts2)
        self.assertEqual(first_cell, [(value1, ts1)])


class TestTable_scan(BaseTableTest):

    def test_scan_when_empty(self):
        scan_result = list(Config.TABLE.scan())
        self.assertEqual(scan_result, [])

    def test_scan_single_row(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        row1_data = {COL1: value1, COL2: value2}

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)
        table.put(ROW_KEY1, row1_data)

        scan_result = list(table.scan())
        self.assertEqual(scan_result, [(ROW_KEY1, row1_data)])

        scan_result_cols = list(table.scan(columns=[COL1]))
        self.assertEqual(scan_result_cols, [(ROW_KEY1, {COL1: value1})])

        scan_result_ts = list(table.scan(include_timestamp=True))
        self.assertEqual(len(scan_result_ts), 1)
        only_row = scan_result_ts[0]
        self.assertEqual(only_row[0], ROW_KEY1)
        row_values = only_row[1]
        ts = row_values[COL1][1]
        self.assertEqual(row_values, {COL1: (value1, ts), COL2: (value2, ts)})

    def test_scan_filters(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        value3 = 'value3'
        value4 = 'value4'
        value5 = 'value5'
        value6 = 'value6'
        row1_data = {COL1: value1, COL2: value2}
        row2_data = {COL2: value3, COL3: value4}
        row3_data = {COL3: value5, COL4: value6}

        # Need to clean-up row1/2/3 after.
        self.rows_to_delete.append(ROW_KEY1)
        self.rows_to_delete.append(ROW_KEY2)
        self.rows_to_delete.append(ROW_KEY3)
        table.put(ROW_KEY1, row1_data)
        table.put(ROW_KEY2, row2_data)
        table.put(ROW_KEY3, row3_data)

        # Basic scan (no filters)
        scan_result = list(table.scan())
        self.assertEqual(scan_result, [
            (ROW_KEY1, row1_data),
            (ROW_KEY2, row2_data),
            (ROW_KEY3, row3_data),
        ])

        # Limit the size of the scan
        scan_result = list(table.scan(limit=1))
        self.assertEqual(scan_result, [
            (ROW_KEY1, row1_data),
        ])

        # Scan with a row prefix.
        prefix = ROW_KEY2[:-1]
        self.assertEqual(prefix, ROW_KEY3[:-1])
        scan_result_prefixed = list(table.scan(row_prefix=prefix))
        self.assertEqual(scan_result_prefixed, [
            (ROW_KEY2, row2_data),
            (ROW_KEY3, row3_data),
        ])

        # Make sure our keys are sorted in order
        row_keys = [ROW_KEY1, ROW_KEY2, ROW_KEY3]
        self.assertEqual(row_keys, sorted(row_keys))

        # row_start alone (inclusive)
        scan_result_row_start = list(table.scan(row_start=ROW_KEY2))
        self.assertEqual(scan_result_row_start, [
            (ROW_KEY2, row2_data),
            (ROW_KEY3, row3_data),
        ])

        # row_stop alone (exclusive)
        scan_result_row_stop = list(table.scan(row_stop=ROW_KEY2))
        self.assertEqual(scan_result_row_stop, [
            (ROW_KEY1, row1_data),
        ])

        # Both row_start and row_stop
        scan_result_row_stop_and_start = list(
            table.scan(row_start=ROW_KEY1, row_stop=ROW_KEY3))
        self.assertEqual(scan_result_row_stop_and_start, [
            (ROW_KEY1, row1_data),
            (ROW_KEY2, row2_data),
        ])

    def test_scan_timestamp(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        value3 = 'value3'
        value4 = 'value4'
        value5 = 'value5'
        value6 = 'value6'

        # Need to clean-up row1/2/3 after.
        self.rows_to_delete.append(ROW_KEY1)
        self.rows_to_delete.append(ROW_KEY2)
        self.rows_to_delete.append(ROW_KEY3)
        table.put(ROW_KEY3, {COL4: value6})
        table.put(ROW_KEY2, {COL3: value4})
        table.put(ROW_KEY2, {COL2: value3})
        table.put(ROW_KEY1, {COL2: value2})
        table.put(ROW_KEY3, {COL3: value5})
        table.put(ROW_KEY1, {COL1: value1})

        # Retrieve all the timestamps so we can filter with them.
        scan_result = list(table.scan(include_timestamp=True))
        self.assertEqual(len(scan_result), 3)
        row1, row2, row3 = scan_result
        self.assertEqual(row1[0], ROW_KEY1)
        self.assertEqual(row2[0], ROW_KEY2)
        self.assertEqual(row3[0], ROW_KEY3)

        # Drop the keys now that we have checked.
        _, row1 = row1
        _, row2 = row2
        _, row3 = row3

        # These are numbered in order of insertion, **not** in
        # the order of the values.
        ts1 = row3[COL4][1]
        ts2 = row2[COL3][1]
        ts3 = row2[COL2][1]
        ts4 = row1[COL2][1]
        ts5 = row3[COL3][1]
        ts6 = row1[COL1][1]

        self.assertEqual(row1, {COL1: (value1, ts6), COL2: (value2, ts4)})
        self.assertEqual(row2, {COL2: (value3, ts3), COL3: (value4, ts2)})
        self.assertEqual(row3, {COL3: (value5, ts5), COL4: (value6, ts1)})

        # All cells before ts1 (exclusive)
        scan_result_before_ts1 = list(table.scan(timestamp=ts1,
                                                 include_timestamp=True))
        self.assertEqual(scan_result_before_ts1, [])

        # All cells before ts2 (inclusive)
        scan_result_before_ts2 = list(table.scan(timestamp=ts2 + 1,
                                                 include_timestamp=True))
        self.assertEqual(scan_result_before_ts2, [
            (ROW_KEY2, {COL3: (value4, ts2)}),
            (ROW_KEY3, {COL4: (value6, ts1)}),
        ])

        # All cells before ts6 (exclusive)
        scan_result_before_ts6 = list(table.scan(timestamp=ts6,
                                                 include_timestamp=True))
        self.assertEqual(scan_result_before_ts6, [
            (ROW_KEY1, {COL2: (value2, ts4)}),
            (ROW_KEY2, {COL2: (value3, ts3), COL3: (value4, ts2)}),
            (ROW_KEY3, {COL3: (value5, ts5), COL4: (value6, ts1)}),
        ])


class TestTable_put(BaseTableTest):

    def test_put(self):
        value1 = 'value1'
        value2 = 'value2'
        row1_data = {COL1: value1, COL2: value2}

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)
        Config.TABLE.put(ROW_KEY1, row1_data)

        row1 = Config.TABLE.row(ROW_KEY1)
        self.assertEqual(row1, row1_data)

        # Check again, but this time with timestamps.
        row1 = Config.TABLE.row(ROW_KEY1, include_timestamp=True)
        timestamp1 = row1[COL1][1]
        timestamp2 = row1[COL2][1]
        self.assertEqual(timestamp1, timestamp2)

        row1_data_with_timestamps = {COL1: (value1, timestamp1),
                                     COL2: (value2, timestamp2)}
        self.assertEqual(row1, row1_data_with_timestamps)

    def test_put_with_timestamp(self):
        value1 = 'value1'
        value2 = 'value2'
        row1_data = {COL1: value1, COL2: value2}
        ts = 1461367402

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)
        Config.TABLE.put(ROW_KEY1, row1_data, timestamp=ts)

        # Check again, but this time with timestamps.
        row1 = Config.TABLE.row(ROW_KEY1, include_timestamp=True)
        row1_data_with_timestamps = {COL1: (value1, ts),
                                     COL2: (value2, ts)}
        self.assertEqual(row1, row1_data_with_timestamps)


class TestTable_delete(BaseTableTest):

    def test_delete(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        row1_data = {COL1: value1, COL2: value2}

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)
        table.put(ROW_KEY1, row1_data)

        row1 = table.row(ROW_KEY1)
        self.assertEqual(row1, row1_data)

        table.delete(ROW_KEY1)
        row1_after = table.row(ROW_KEY1)
        self.assertEqual(row1_after, {})

    def test_delete_with_columns(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        row1_data = {COL1: value1, COL2: value2}

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)
        table.put(ROW_KEY1, row1_data)

        row1 = table.row(ROW_KEY1)
        self.assertEqual(row1, row1_data)

        table.delete(ROW_KEY1, columns=[COL1])
        row1_after = table.row(ROW_KEY1)
        self.assertEqual(row1_after, {COL2: value2})

    def test_delete_with_column_family(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        value3 = 'value3'
        row1_data = {COL1: value1, COL2: value2, COL4: value3}

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)
        table.put(ROW_KEY1, row1_data)

        row1 = table.row(ROW_KEY1)
        self.assertEqual(row1, row1_data)

        table.delete(ROW_KEY1, columns=[COL_FAM1])
        row1_after = table.row(ROW_KEY1)
        self.assertEqual(row1_after, {COL4: value3})

    def test_delete_with_columns_family_overlap(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'
        row1_data = {COL1: value1, COL2: value2}

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)

        # First go-around, use [COL_FAM1, COL1]
        table.put(ROW_KEY1, row1_data)
        row1 = table.row(ROW_KEY1)
        self.assertEqual(row1, row1_data)

        table.delete(ROW_KEY1, columns=[COL_FAM1, COL1])
        row1_after = table.row(ROW_KEY1)
        self.assertEqual(row1_after, {})

        # Second go-around, use [COL1, COL_FAM1]
        table.put(ROW_KEY1, row1_data)
        row1 = table.row(ROW_KEY1)
        self.assertEqual(row1, row1_data)

        table.delete(ROW_KEY1, columns=[COL1, COL_FAM1])
        row1_after = table.row(ROW_KEY1)
        self.assertEqual(row1_after, {})

    def test_delete_with_timestamp(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)
        table.put(ROW_KEY1, {COL1: value1})
        table.put(ROW_KEY1, {COL2: value2})

        row1 = table.row(ROW_KEY1, include_timestamp=True)
        ts1 = row1[COL1][1]
        ts2 = row1[COL2][1]

        self.assertTrue(ts1 < ts2)

        # NOTE: The Cloud Bigtable "Mutation.DeleteFromRow" mutation does
        #       not support timestamps. Even attempting to send one
        #       conditionally(via CheckAndMutateRowRequest) deletes the
        #       entire row.
        # NOTE: Cloud Bigtable deletes **ALSO** use an inclusive timestamp
        #       at the endpoint, but only because we fake this when
        #       creating Batch._delete_range.
        table.delete(ROW_KEY1, columns=[COL1, COL2], timestamp=ts1 - 1)
        row1_after_early_delete = table.row(ROW_KEY1, include_timestamp=True)
        self.assertEqual(row1_after_early_delete, row1)

        # NOTE: Cloud Bigtable deletes **ALSO** use an inclusive timestamp
        #       at the endpoint, but only because we fake this when
        #       creating Batch._delete_range.
        table.delete(ROW_KEY1, columns=[COL1, COL2], timestamp=ts1)
        row1_after_incl_delete = table.row(ROW_KEY1, include_timestamp=True)
        self.assertEqual(row1_after_incl_delete, {COL2: (value2, ts2)})

    def test_delete_with_columns_and_timestamp(self):
        table = Config.TABLE
        value1 = 'value1'
        value2 = 'value2'

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)
        table.put(ROW_KEY1, {COL1: value1})
        table.put(ROW_KEY1, {COL2: value2})

        row1 = table.row(ROW_KEY1, include_timestamp=True)
        ts1 = row1[COL1][1]
        ts2 = row1[COL2][1]

        # Delete with conditions that have no matches.
        table.delete(ROW_KEY1, timestamp=ts1, columns=[COL2])
        row1_after_delete = table.row(ROW_KEY1, include_timestamp=True)
        # NOTE: COL2 is still present since it occurs after ts1 and
        #       COL1 is still present since it is not in `columns`.
        self.assertEqual(row1_after_delete, row1)

        # Delete with conditions that have no matches.
        # NOTE: Cloud Bigtable can't use a timestamp with column families
        #       since "Mutation.DeleteFromFamily" does not include a
        #       timestamp range.
        # NOTE: Cloud Bigtable deletes **ALSO** use an inclusive timestamp
        #       at the endpoint, but only because we fake this when
        #       creating Batch._delete_range.
        table.delete(ROW_KEY1, timestamp=ts1, columns=[COL1, COL2])
        row1_delete_fam = table.row(ROW_KEY1, include_timestamp=True)
        # NOTE: COL2 is still present since it occurs after ts1 and
        #       COL1 is still present since it is not in `columns`.
        self.assertEqual(row1_delete_fam, {COL2: (value2, ts2)})


class TestTableCounterMethods(BaseTableTest):

    def test_counter_get(self):
        table = Config.TABLE

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)

        self.assertEqual(table.row(ROW_KEY1, columns=[COL1]), {})
        initial_counter = table.counter_get(ROW_KEY1, COL1)
        self.assertEqual(initial_counter, 0)

        self.assertEqual(table.row(ROW_KEY1, columns=[COL1]),
                         {COL1: _PACK_I64(0)})

    def test_counter_inc(self):
        table = Config.TABLE

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)

        self.assertEqual(table.row(ROW_KEY1, columns=[COL1]), {})
        initial_counter = table.counter_get(ROW_KEY1, COL1)
        self.assertEqual(initial_counter, 0)

        inc_value = 10
        updated_counter = table.counter_inc(ROW_KEY1, COL1, value=inc_value)
        self.assertEqual(updated_counter, inc_value)

        # Check that the value is set (does not seem to occur on HBase).
        self.assertEqual(table.row(ROW_KEY1, columns=[COL1]),
                         {COL1: _PACK_I64(inc_value)})

    def test_counter_dec(self):
        table = Config.TABLE

        # Need to clean-up row1 after.
        self.rows_to_delete.append(ROW_KEY1)

        self.assertEqual(table.row(ROW_KEY1, columns=[COL1]), {})
        initial_counter = table.counter_get(ROW_KEY1, COL1)
        self.assertEqual(initial_counter, 0)

        dec_value = 10
        updated_counter = table.counter_dec(ROW_KEY1, COL1, value=dec_value)
        self.assertEqual(updated_counter, -dec_value)

        # Check that the value is set (does not seem to occur on HBase).
        self.assertEqual(table.row(ROW_KEY1, columns=[COL1]),
                         {COL1: _PACK_I64(-dec_value)})
