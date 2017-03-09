# Copyright 2016 Google Inc.
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

import datetime
import operator
import os

import unittest

from google.cloud._helpers import _datetime_from_microseconds
from google.cloud._helpers import _microseconds_from_datetime
from google.cloud._helpers import UTC
from google.cloud.bigtable.client import Client
from google.cloud.bigtable.column_family import MaxVersionsGCRule
from google.cloud.bigtable.row_filters import ApplyLabelFilter
from google.cloud.bigtable.row_filters import ColumnQualifierRegexFilter
from google.cloud.bigtable.row_filters import RowFilterChain
from google.cloud.bigtable.row_filters import RowFilterUnion
from google.cloud.bigtable.row_data import Cell
from google.cloud.bigtable.row_data import PartialRowData
from google.cloud.environment_vars import BIGTABLE_EMULATOR

from test_utils.retry import RetryErrors
from test_utils.retry import RetryResult
from test_utils.system import EmulatorCreds
from test_utils.system import unique_resource_id


LOCATION_ID = 'us-central1-c'
INSTANCE_ID = 'g-c-p' + unique_resource_id('-')
TABLE_ID = 'google-cloud-python-test-table'
COLUMN_FAMILY_ID1 = u'col-fam-id1'
COLUMN_FAMILY_ID2 = u'col-fam-id2'
COL_NAME1 = b'col-name1'
COL_NAME2 = b'col-name2'
COL_NAME3 = b'col-name3-but-other-fam'
CELL_VAL1 = b'cell-val'
CELL_VAL2 = b'cell-val-newer'
CELL_VAL3 = b'altcol-cell-val'
CELL_VAL4 = b'foo'
ROW_KEY = b'row-key'
ROW_KEY_ALT = b'row-key-alt'
EXISTING_INSTANCES = []


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    INSTANCE = None
    IN_EMULATOR = False


def _wait_until_complete(operation, max_attempts=5):
    """Wait until an operation has completed.

    :type operation: :class:`google.cloud.operation.Operation`
    :param operation: Operation that has not completed.

    :type max_attempts: int
    :param max_attempts: (Optional) The maximum number of times to check if
                         the operation has completed. Defaults to 5.

    :rtype: bool
    :returns: Boolean indicating if the operation is complete.
    """

    def _operation_complete(result):
        return result

    retry = RetryResult(_operation_complete, max_tries=max_attempts)
    return retry(operation.poll)()


def _retry_on_unavailable(exc):
    """Retry only errors whose status code is 'UNAVAILABLE'."""
    from grpc import StatusCode
    return exc.code() == StatusCode.UNAVAILABLE


def setUpModule():
    from google.cloud.exceptions import GrpcRendezvous

    Config.IN_EMULATOR = os.getenv(BIGTABLE_EMULATOR) is not None

    if Config.IN_EMULATOR:
        credentials = EmulatorCreds()
        Config.CLIENT = Client(admin=True, credentials=credentials)
    else:
        Config.CLIENT = Client(admin=True)

    Config.INSTANCE = Config.CLIENT.instance(INSTANCE_ID, LOCATION_ID)

    if not Config.IN_EMULATOR:
        retry = RetryErrors(GrpcRendezvous,
                            error_predicate=_retry_on_unavailable)
        instances, failed_locations = retry(Config.CLIENT.list_instances)()

        if len(failed_locations) != 0:
            raise ValueError('List instances failed in module set up.')

        EXISTING_INSTANCES[:] = instances

        # After listing, create the test instance.
        created_op = Config.INSTANCE.create()
        if not _wait_until_complete(created_op):
            raise RuntimeError('Instance creation exceed 5 seconds.')


def tearDownModule():
    if not Config.IN_EMULATOR:
        Config.INSTANCE.delete()


class TestInstanceAdminAPI(unittest.TestCase):

    def setUp(self):
        if Config.IN_EMULATOR:
            self.skipTest(
                'Instance Admin API not supported in Bigtable emulator')
        self.instances_to_delete = []

    def tearDown(self):
        for instance in self.instances_to_delete:
            instance.delete()

    def test_list_instances(self):
        instances, failed_locations = Config.CLIENT.list_instances()
        self.assertEqual(failed_locations, [])
        # We have added one new instance in `setUpModule`.
        self.assertEqual(len(instances), len(EXISTING_INSTANCES) + 1)
        for instance in instances:
            instance_existence = (instance in EXISTING_INSTANCES or
                                  instance == Config.INSTANCE)
            self.assertTrue(instance_existence)

    def test_reload(self):
        # Use same arguments as Config.INSTANCE (created in `setUpModule`)
        # so we can use reload() on a fresh instance.
        instance = Config.CLIENT.instance(INSTANCE_ID, LOCATION_ID)
        # Make sure metadata unset before reloading.
        instance.display_name = None

        instance.reload()
        self.assertEqual(instance.display_name, Config.INSTANCE.display_name)

    def test_create_instance(self):
        ALT_INSTANCE_ID = 'new' + unique_resource_id('-')
        instance = Config.CLIENT.instance(ALT_INSTANCE_ID, LOCATION_ID)
        operation = instance.create()
        # Make sure this instance gets deleted after the test case.
        self.instances_to_delete.append(instance)

        # We want to make sure the operation completes.
        self.assertTrue(_wait_until_complete(operation))

        # Create a new instance instance and make sure it is the same.
        instance_alt = Config.CLIENT.instance(ALT_INSTANCE_ID, LOCATION_ID)
        instance_alt.reload()

        self.assertEqual(instance, instance_alt)
        self.assertEqual(instance.display_name, instance_alt.display_name)

    def test_update(self):
        OLD_DISPLAY_NAME = Config.INSTANCE.display_name
        NEW_DISPLAY_NAME = 'Foo Bar Baz'
        Config.INSTANCE.display_name = NEW_DISPLAY_NAME
        Config.INSTANCE.update()

        # Create a new instance instance and reload it.
        instance_alt = Config.CLIENT.instance(INSTANCE_ID, None)
        self.assertNotEqual(instance_alt.display_name, NEW_DISPLAY_NAME)
        instance_alt.reload()
        self.assertEqual(instance_alt.display_name, NEW_DISPLAY_NAME)

        # Make sure to put the instance back the way it was for the
        # other test cases.
        Config.INSTANCE.display_name = OLD_DISPLAY_NAME
        Config.INSTANCE.update()


class TestTableAdminAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._table = Config.INSTANCE.table(TABLE_ID)
        cls._table.create()

    @classmethod
    def tearDownClass(cls):
        cls._table.delete()

    def setUp(self):
        self.tables_to_delete = []

    def tearDown(self):
        for table in self.tables_to_delete:
            table.delete()

    def test_list_tables(self):
        # Since `Config.INSTANCE` is newly created in `setUpModule`, the table
        # created in `setUpClass` here will be the only one.
        tables = Config.INSTANCE.list_tables()
        self.assertEqual(tables, [self._table])

    def test_create_table(self):
        temp_table_id = 'foo-bar-baz-table'
        temp_table = Config.INSTANCE.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        # First, create a sorted version of our expected result.
        name_attr = operator.attrgetter('name')
        expected_tables = sorted([temp_table, self._table], key=name_attr)

        # Then query for the tables in the instance and sort them by
        # name as well.
        tables = Config.INSTANCE.list_tables()
        sorted_tables = sorted(tables, key=name_attr)
        self.assertEqual(sorted_tables, expected_tables)

    def test_create_column_family(self):
        temp_table_id = 'foo-bar-baz-table'
        temp_table = Config.INSTANCE.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        self.assertEqual(temp_table.list_column_families(), {})
        gc_rule = MaxVersionsGCRule(1)
        column_family = temp_table.column_family(COLUMN_FAMILY_ID1,
                                                 gc_rule=gc_rule)
        column_family.create()

        col_fams = temp_table.list_column_families()

        self.assertEqual(len(col_fams), 1)
        retrieved_col_fam = col_fams[COLUMN_FAMILY_ID1]
        self.assertIs(retrieved_col_fam._table, column_family._table)
        self.assertEqual(retrieved_col_fam.column_family_id,
                         column_family.column_family_id)
        self.assertEqual(retrieved_col_fam.gc_rule, gc_rule)

    def test_update_column_family(self):
        temp_table_id = 'foo-bar-baz-table'
        temp_table = Config.INSTANCE.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        gc_rule = MaxVersionsGCRule(1)
        column_family = temp_table.column_family(COLUMN_FAMILY_ID1,
                                                 gc_rule=gc_rule)
        column_family.create()

        # Check that our created table is as expected.
        col_fams = temp_table.list_column_families()
        self.assertEqual(col_fams, {COLUMN_FAMILY_ID1: column_family})

        # Update the column family's GC rule and then try to update.
        column_family.gc_rule = None
        column_family.update()

        # Check that the update has propagated.
        col_fams = temp_table.list_column_families()
        self.assertIsNone(col_fams[COLUMN_FAMILY_ID1].gc_rule)

    def test_delete_column_family(self):
        temp_table_id = 'foo-bar-baz-table'
        temp_table = Config.INSTANCE.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        self.assertEqual(temp_table.list_column_families(), {})
        column_family = temp_table.column_family(COLUMN_FAMILY_ID1)
        column_family.create()

        # Make sure the family is there before deleting it.
        col_fams = temp_table.list_column_families()
        self.assertEqual(list(col_fams.keys()), [COLUMN_FAMILY_ID1])

        column_family.delete()
        # Make sure we have successfully deleted it.
        self.assertEqual(temp_table.list_column_families(), {})


class TestDataAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._table = table = Config.INSTANCE.table(TABLE_ID)
        table.create()
        table.column_family(COLUMN_FAMILY_ID1).create()
        table.column_family(COLUMN_FAMILY_ID2).create()

    @classmethod
    def tearDownClass(cls):
        # Will also delete any data contained in the table.
        cls._table.delete()

    def _maybe_emulator_skip(self, message):
        # NOTE: This method is necessary because ``Config.IN_EMULATOR``
        #       is set at runtime rather than import time, which means we
        #       can't use the @unittest.skipIf decorator.
        if Config.IN_EMULATOR:
            self.skipTest(message)

    def setUp(self):
        self.rows_to_delete = []

    def tearDown(self):
        for row in self.rows_to_delete:
            row.clear()
            row.delete()
            row.commit()

    def _write_to_row(self, row1=None, row2=None, row3=None, row4=None):
        timestamp1 = datetime.datetime.utcnow().replace(tzinfo=UTC)
        timestamp1_micros = _microseconds_from_datetime(timestamp1)
        # Truncate to millisecond granularity.
        timestamp1_micros -= (timestamp1_micros % 1000)
        timestamp1 = _datetime_from_microseconds(timestamp1_micros)
        # 1000 microseconds is a millisecond
        timestamp2 = timestamp1 + datetime.timedelta(microseconds=1000)
        timestamp3 = timestamp1 + datetime.timedelta(microseconds=2000)
        timestamp4 = timestamp1 + datetime.timedelta(microseconds=3000)
        if row1 is not None:
            row1.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL1,
                          timestamp=timestamp1)
        if row2 is not None:
            row2.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL2,
                          timestamp=timestamp2)
        if row3 is not None:
            row3.set_cell(COLUMN_FAMILY_ID1, COL_NAME2, CELL_VAL3,
                          timestamp=timestamp3)
        if row4 is not None:
            row4.set_cell(COLUMN_FAMILY_ID2, COL_NAME3, CELL_VAL4,
                          timestamp=timestamp4)

        # Create the cells we will check.
        cell1 = Cell(CELL_VAL1, timestamp1)
        cell2 = Cell(CELL_VAL2, timestamp2)
        cell3 = Cell(CELL_VAL3, timestamp3)
        cell4 = Cell(CELL_VAL4, timestamp4)
        return cell1, cell2, cell3, cell4

    def test_read_large_cell_limit(self):
        row = self._table.row(ROW_KEY)
        self.rows_to_delete.append(row)

        number_of_bytes = 10 * 1024 * 1024
        data = b'1' * number_of_bytes  # 10MB of 1's.
        row.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, data)
        row.commit()

        # Read back the contents of the row.
        partial_row_data = self._table.read_row(ROW_KEY)
        self.assertEqual(partial_row_data.row_key, ROW_KEY)
        cell = partial_row_data.cells[COLUMN_FAMILY_ID1]
        column = cell[COL_NAME1]
        self.assertEqual(len(column), 1)
        self.assertEqual(column[0].value, data)

    def test_read_row(self):
        row = self._table.row(ROW_KEY)
        self.rows_to_delete.append(row)

        cell1, cell2, cell3, cell4 = self._write_to_row(row, row, row, row)
        row.commit()

        # Read back the contents of the row.
        partial_row_data = self._table.read_row(ROW_KEY)
        self.assertEqual(partial_row_data.row_key, ROW_KEY)

        # Check the cells match.
        ts_attr = operator.attrgetter('timestamp')
        expected_row_contents = {
            COLUMN_FAMILY_ID1: {
                COL_NAME1: sorted([cell1, cell2], key=ts_attr, reverse=True),
                COL_NAME2: [cell3],
            },
            COLUMN_FAMILY_ID2: {
                COL_NAME3: [cell4],
            },
        }
        self.assertEqual(partial_row_data.cells, expected_row_contents)

    def test_read_rows(self):
        row = self._table.row(ROW_KEY)
        row_alt = self._table.row(ROW_KEY_ALT)
        self.rows_to_delete.extend([row, row_alt])

        cell1, cell2, cell3, cell4 = self._write_to_row(row, row_alt,
                                                        row, row_alt)
        row.commit()
        row_alt.commit()

        rows_data = self._table.read_rows()
        self.assertEqual(rows_data.rows, {})
        rows_data.consume_all()

        # NOTE: We should refrain from editing protected data on instances.
        #       Instead we should make the values public or provide factories
        #       for constructing objects with them.
        row_data = PartialRowData(ROW_KEY)
        row_data._chunks_encountered = True
        row_data._committed = True
        row_data._cells = {
            COLUMN_FAMILY_ID1: {
                COL_NAME1: [cell1],
                COL_NAME2: [cell3],
            },
        }

        row_alt_data = PartialRowData(ROW_KEY_ALT)
        row_alt_data._chunks_encountered = True
        row_alt_data._committed = True
        row_alt_data._cells = {
            COLUMN_FAMILY_ID1: {
                COL_NAME1: [cell2],
            },
            COLUMN_FAMILY_ID2: {
                COL_NAME3: [cell4],
            },
        }

        expected_rows = {
            ROW_KEY: row_data,
            ROW_KEY_ALT: row_alt_data,
        }
        self.assertEqual(rows_data.rows, expected_rows)

    def test_read_with_label_applied(self):
        self._maybe_emulator_skip('Labels not supported by Bigtable emulator')
        row = self._table.row(ROW_KEY)
        self.rows_to_delete.append(row)

        cell1, _, cell3, _ = self._write_to_row(row, None, row)
        row.commit()

        # Combine a label with column 1.
        label1 = u'label-red'
        label1_filter = ApplyLabelFilter(label1)
        col1_filter = ColumnQualifierRegexFilter(COL_NAME1)
        chain1 = RowFilterChain(filters=[col1_filter, label1_filter])

        # Combine a label with column 2.
        label2 = u'label-blue'
        label2_filter = ApplyLabelFilter(label2)
        col2_filter = ColumnQualifierRegexFilter(COL_NAME2)
        chain2 = RowFilterChain(filters=[col2_filter, label2_filter])

        # Bring our two labeled columns together.
        row_filter = RowFilterUnion(filters=[chain1, chain2])
        partial_row_data = self._table.read_row(ROW_KEY, filter_=row_filter)
        self.assertEqual(partial_row_data.row_key, ROW_KEY)

        cells_returned = partial_row_data.cells
        col_fam1 = cells_returned.pop(COLUMN_FAMILY_ID1)
        # Make sure COLUMN_FAMILY_ID1 was the only key.
        self.assertEqual(len(cells_returned), 0)

        cell1_new, = col_fam1.pop(COL_NAME1)
        cell3_new, = col_fam1.pop(COL_NAME2)
        # Make sure COL_NAME1 and COL_NAME2 were the only keys.
        self.assertEqual(len(col_fam1), 0)

        # Check that cell1 has matching values and gained a label.
        self.assertEqual(cell1_new.value, cell1.value)
        self.assertEqual(cell1_new.timestamp, cell1.timestamp)
        self.assertEqual(cell1.labels, [])
        self.assertEqual(cell1_new.labels, [label1])

        # Check that cell3 has matching values and gained a label.
        self.assertEqual(cell3_new.value, cell3.value)
        self.assertEqual(cell3_new.timestamp, cell3.timestamp)
        self.assertEqual(cell3.labels, [])
        self.assertEqual(cell3_new.labels, [label2])
